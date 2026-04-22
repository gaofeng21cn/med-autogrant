from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable


Discoverer = Callable[[dict[str, Any]], dict[str, Any]]
Selector = Callable[[dict[str, Any]], dict[str, Any]]
Initializer = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
MainlineRunner = Callable[[dict[str, Any]], dict[str, Any]]
QualityEvaluator = Callable[[dict[str, Any]], dict[str, Any]]

_CONTROLLER_STATUSES = {
    "submission_grade_candidate",
    "near_submission_candidate",
    "failed_closed",
}
_QUALITY_STATUSES = {
    "submission_grade_candidate",
    "near_submission_candidate",
    "not_ready",
}


def run_grant_autonomy_controller(
    *,
    request: dict[str, Any],
    selector: Selector,
    initializer: Initializer,
    mainline_runner: MainlineRunner,
    quality_evaluator: QualityEvaluator,
    discoverer: Discoverer | None = None,
) -> dict[str, Any]:
    if not isinstance(request, dict):
        return _fail_closed_report(
            request_id="",
            started_from_mode="unknown",
            goal={},
            max_rounds_or_cycles=0,
            budget_max=0,
            spent_steps=0,
            termination_reason="invalid_request_object",
            blocker_queue=[],
            evidence_gap_queue=[],
        )

    request_id = _normalized_string(request.get("request_id"))
    start = request.get("start")
    goal = request.get("goal")
    max_rounds_or_cycles = request.get("max_rounds_or_cycles")
    budget = request.get("budget")

    if not isinstance(start, dict) or not isinstance(goal, dict) or not isinstance(budget, dict):
        return _fail_closed_report(
            request_id=request_id,
            started_from_mode="unknown",
            goal=deepcopy(goal) if isinstance(goal, dict) else {},
            max_rounds_or_cycles=0,
            budget_max=0,
            spent_steps=0,
            termination_reason="missing_required_input",
            blocker_queue=[],
            evidence_gap_queue=[],
        )

    start_mode = _normalized_string(start.get("mode"))
    goal_target = _normalized_string(goal.get("target_status"))
    if goal_target not in {"submission_grade_candidate", "near_submission_candidate"}:
        return _fail_closed_report(
            request_id=request_id,
            started_from_mode=start_mode or "unknown",
            goal=deepcopy(goal),
            max_rounds_or_cycles=0,
            budget_max=0,
            spent_steps=0,
            termination_reason="invalid_goal_target",
            blocker_queue=[],
            evidence_gap_queue=[],
        )
    if not isinstance(max_rounds_or_cycles, int) or max_rounds_or_cycles <= 0:
        return _fail_closed_report(
            request_id=request_id,
            started_from_mode=start_mode or "unknown",
            goal=deepcopy(goal),
            max_rounds_or_cycles=0,
            budget_max=0,
            spent_steps=0,
            termination_reason="invalid_max_rounds_or_cycles",
            blocker_queue=[],
            evidence_gap_queue=[],
        )

    budget_max = budget.get("max_total_steps")
    if not isinstance(budget_max, int) or budget_max <= 0:
        return _fail_closed_report(
            request_id=request_id,
            started_from_mode=start_mode or "unknown",
            goal=deepcopy(goal),
            max_rounds_or_cycles=max_rounds_or_cycles,
            budget_max=0,
            spent_steps=0,
            termination_reason="invalid_budget",
            blocker_queue=[],
            evidence_gap_queue=[],
        )

    stop_conditions = request.get("stop_conditions")
    if not isinstance(stop_conditions, dict):
        return _fail_closed_report(
            request_id=request_id,
            started_from_mode=start_mode or "unknown",
            goal=deepcopy(goal),
            max_rounds_or_cycles=max_rounds_or_cycles,
            budget_max=budget_max,
            spent_steps=0,
            termination_reason="missing_required_input",
            blocker_queue=[],
            evidence_gap_queue=[],
        )
    require_zero_blockers = bool(stop_conditions.get("require_zero_blockers", True))
    require_zero_evidence_gaps = bool(stop_conditions.get("require_zero_evidence_gaps", True))

    initial_blockers = _string_list(request.get("blocker_queue"))
    initial_evidence_gaps = _string_list(request.get("evidence_gap_queue"))
    if initial_blockers is None or initial_evidence_gaps is None:
        return _fail_closed_report(
            request_id=request_id,
            started_from_mode=start_mode or "unknown",
            goal=deepcopy(goal),
            max_rounds_or_cycles=max_rounds_or_cycles,
            budget_max=budget_max,
            spent_steps=0,
            termination_reason="missing_required_input",
            blocker_queue=[],
            evidence_gap_queue=[],
        )

    reselection_policy = request.get("reselection_policy")
    rollback_policy = request.get("rollback_policy")
    if not isinstance(reselection_policy, dict) or not isinstance(rollback_policy, dict):
        return _fail_closed_report(
            request_id=request_id,
            started_from_mode=start_mode or "unknown",
            goal=deepcopy(goal),
            max_rounds_or_cycles=max_rounds_or_cycles,
            budget_max=budget_max,
            spent_steps=0,
            termination_reason="missing_required_input",
            blocker_queue=initial_blockers,
            evidence_gap_queue=initial_evidence_gaps,
        )

    reselection_enabled = bool(reselection_policy.get("enabled", False))
    rollback_enabled = bool(rollback_policy.get("enabled", False))
    max_reselections = reselection_policy.get("max_reselections", 0)
    max_rollbacks = rollback_policy.get("max_rollbacks", 0)
    if not isinstance(max_reselections, int) or max_reselections < 0:
        max_reselections = 0
    if not isinstance(max_rollbacks, int) or max_rollbacks < 0:
        max_rollbacks = 0

    action_trace: list[dict[str, Any]] = []
    reselection_decisions: list[dict[str, Any]] = []
    rollback_decisions: list[dict[str, Any]] = []
    spent_steps = 0
    reselection_count = 0
    rollback_count = 0
    completed_cycles = 0
    latest_blocker_report: dict[str, Any] = {}
    unresolved_blockers = list(initial_blockers)
    evidence_gaps = list(initial_evidence_gaps)

    selection_input: dict[str, Any] | None = None
    workspace: dict[str, Any] | None = None

    def spend_budget(*, step_action: str, cycle: int | None) -> bool:
        nonlocal spent_steps
        if spent_steps + 1 > budget_max:
            return False
        spent_steps += 1
        action_trace.append(
            {
                "step_action": step_action,
                "cycle": cycle,
                "step_index": spent_steps,
                "result": "executed",
            }
        )
        return True

    if start_mode == "workspace":
        seed_workspace = start.get("workspace")
        if not isinstance(seed_workspace, dict):
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="missing_required_input",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )
        workspace = deepcopy(seed_workspace)
    elif start_mode in {"selection_input", "discovery_input"}:
        if start_mode == "selection_input":
            seed_selection_input = start.get("selection_input")
            if not isinstance(seed_selection_input, dict):
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="missing_required_input",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                )
            selection_input = deepcopy(seed_selection_input)
        else:
            discovery_input = start.get("discovery_input")
            if not isinstance(discovery_input, dict):
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="missing_required_input",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                )
            if discoverer is None:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="discoverer_required_but_missing",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                )
            if not spend_budget(step_action="discoverer", cycle=None):
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="budget_exhausted",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                )
            try:
                discovery_output = discoverer(discovery_input)
            except Exception:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="discoverer_callback_error",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                )
            selection_input = _extract_mapping(
                discovery_output,
                preferred_keys=("selection_input", "project_profile_selection_input"),
            )
            if selection_input is None:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="discoverer_unstructured_result",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                )

        if not spend_budget(step_action="selector", cycle=None):
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="budget_exhausted",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )
        try:
            selection_output = selector(selection_input)
        except Exception:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="selector_callback_error",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )
        if not isinstance(selection_output, dict):
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="selector_unstructured_result",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )

        if not spend_budget(step_action="initializer", cycle=None):
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="budget_exhausted",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )
        try:
            initializer_output = initializer(selection_input, selection_output)
        except Exception:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="initializer_callback_error",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )
        workspace = _extract_mapping(
            initializer_output,
            preferred_keys=("workspace", "initialized_workspace"),
        )
        if workspace is None:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="initializer_unstructured_result",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )
    else:
        return _fail_closed_report(
            request_id=request_id,
            started_from_mode=start_mode or "unknown",
            goal=deepcopy(goal),
            max_rounds_or_cycles=max_rounds_or_cycles,
            budget_max=budget_max,
            spent_steps=spent_steps,
            termination_reason="unsupported_start_mode",
            blocker_queue=initial_blockers,
            evidence_gap_queue=initial_evidence_gaps,
            action_trace=action_trace,
            reselection_decisions=reselection_decisions,
            rollback_decisions=rollback_decisions,
        )

    for cycle in range(1, max_rounds_or_cycles + 1):
        completed_cycles = cycle

        if not spend_budget(step_action="quality_evaluator", cycle=cycle):
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="budget_exhausted",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
                blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
            )
        try:
            quality_output = quality_evaluator(workspace)
        except Exception:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="quality_evaluator_callback_error",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
                blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
            )
        normalized_quality = _normalize_quality_output(quality_output)
        if normalized_quality is None:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="quality_evaluator_unstructured_result",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
                blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
            )

        latest_blocker_report = normalized_quality["blocker_report"]
        if cycle == 1:
            unresolved_blockers = _dedupe(initial_blockers + normalized_quality["unresolved_blockers"])
            evidence_gaps = _dedupe(initial_evidence_gaps + normalized_quality["evidence_gaps"])
        else:
            unresolved_blockers = _dedupe(normalized_quality["unresolved_blockers"])
            evidence_gaps = _dedupe(normalized_quality["evidence_gaps"])
        quality_status = normalized_quality["quality_status"]

        if _goal_satisfied(goal_target=goal_target, quality_status=quality_status):
            if require_zero_blockers and unresolved_blockers:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="blockers_not_cleared",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            if require_zero_evidence_gaps and evidence_gaps:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="evidence_gaps_not_cleared",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            return _build_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                controller_status=quality_status,
                termination_reason="goal_reached",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
            )

        if cycle == max_rounds_or_cycles:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason=_resolve_terminal_reason(unresolved_blockers, evidence_gaps),
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
                blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
            )

        if not spend_budget(step_action="mainline_runner", cycle=cycle):
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="budget_exhausted",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
                blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
            )
        try:
            mainline_output = mainline_runner(
                {
                    "workspace": deepcopy(workspace),
                    "cycle": cycle,
                    "goal": deepcopy(goal),
                    "blocker_queue": list(unresolved_blockers),
                    "evidence_gap_queue": list(evidence_gaps),
                }
            )
        except Exception:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="mainline_runner_callback_error",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
                blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
            )
        if not isinstance(mainline_output, dict):
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="mainline_runner_unstructured_result",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
                blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
            )

        rollback_action = _decision_action(mainline_output.get("rollback_decision"))
        if rollback_action == "rollback":
            allowed = rollback_enabled and rollback_count < max_rollbacks
            rollback_decisions.append(
                {
                    "cycle": cycle,
                    "action": rollback_action,
                    "accepted": allowed,
                    "reason": _decision_reason(mainline_output.get("rollback_decision")),
                }
            )
            if not rollback_enabled:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="rollback_policy_disallowed",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            if rollback_count >= max_rollbacks:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="rollback_budget_exhausted",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            rollback_count += 1

        reselection_action = _decision_action(mainline_output.get("reselection_decision"))
        if reselection_action == "reselect":
            decision_reason = _decision_reason(mainline_output.get("reselection_decision"))
            accepted = reselection_enabled and reselection_count < max_reselections and selection_input is not None
            reselection_decisions.append(
                {
                    "cycle": cycle,
                    "action": reselection_action,
                    "accepted": accepted,
                    "reason": decision_reason,
                }
            )
            if not reselection_enabled:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="reselection_policy_disallowed",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            if selection_input is None:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="reselection_requires_selection_input",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            if reselection_count >= max_reselections:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="reselection_budget_exhausted",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )

            if not spend_budget(step_action="selector", cycle=cycle):
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="budget_exhausted",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            try:
                reselection_output = selector(selection_input)
            except Exception:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="selector_callback_error",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            if not isinstance(reselection_output, dict):
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="selector_unstructured_result",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )

            if not spend_budget(step_action="initializer", cycle=cycle):
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="budget_exhausted",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            try:
                reinit_output = initializer(selection_input, reselection_output)
            except Exception:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="initializer_callback_error",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            reselected_workspace = _extract_mapping(
                reinit_output,
                preferred_keys=("workspace", "initialized_workspace"),
            )
            if reselected_workspace is None:
                return _fail_closed_report(
                    request_id=request_id,
                    started_from_mode=start_mode,
                    goal=deepcopy(goal),
                    max_rounds_or_cycles=max_rounds_or_cycles,
                    budget_max=budget_max,
                    spent_steps=spent_steps,
                    termination_reason="initializer_unstructured_result",
                    blocker_queue=initial_blockers,
                    evidence_gap_queue=initial_evidence_gaps,
                    action_trace=action_trace,
                    reselection_decisions=reselection_decisions,
                    rollback_decisions=rollback_decisions,
                    completed_cycles=completed_cycles,
                    final_workspace=workspace,
                    blocker_report=latest_blocker_report,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                )
            workspace = reselected_workspace
            reselection_count += 1
            continue

        next_workspace = _extract_mapping(mainline_output, preferred_keys=("workspace", "final_workspace"))
        if next_workspace is None:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="mainline_runner_missing_workspace",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
                blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
            )
        workspace = next_workspace

    return _fail_closed_report(
        request_id=request_id,
        started_from_mode=start_mode,
        goal=deepcopy(goal),
        max_rounds_or_cycles=max_rounds_or_cycles,
        budget_max=budget_max,
        spent_steps=spent_steps,
        termination_reason=_resolve_terminal_reason(unresolved_blockers, evidence_gaps),
        blocker_queue=initial_blockers,
        evidence_gap_queue=initial_evidence_gaps,
        action_trace=action_trace,
        reselection_decisions=reselection_decisions,
        rollback_decisions=rollback_decisions,
        completed_cycles=completed_cycles,
        final_workspace=workspace,
        blocker_report=latest_blocker_report,
        unresolved_blockers=unresolved_blockers,
        evidence_gaps=evidence_gaps,
    )


def _build_report(
    *,
    request_id: str,
    started_from_mode: str,
    goal: dict[str, Any],
    max_rounds_or_cycles: int,
    budget_max: int,
    spent_steps: int,
    controller_status: str,
    termination_reason: str,
    blocker_queue: list[str],
    evidence_gap_queue: list[str],
    blocker_report: dict[str, Any] | None = None,
    unresolved_blockers: list[str] | None = None,
    evidence_gaps: list[str] | None = None,
    action_trace: list[dict[str, Any]] | None = None,
    reselection_decisions: list[dict[str, Any]] | None = None,
    rollback_decisions: list[dict[str, Any]] | None = None,
    completed_cycles: int = 0,
    final_workspace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if controller_status not in _CONTROLLER_STATUSES:
        controller_status = "failed_closed"
    goal_payload = _normalize_goal(goal)
    unresolved = list(unresolved_blockers or [])
    gaps = list(evidence_gaps or [])
    latest_report = deepcopy(blocker_report) if isinstance(blocker_report, dict) else {}
    return {
        "surface_kind": "grant_autonomy_controller_report",
        "controller_version": 1,
        "request_id": request_id,
        "controller_status": controller_status,
        "termination_reason": termination_reason,
        "started_from_mode": started_from_mode,
        "goal": goal_payload,
        "completed_cycles": completed_cycles,
        "max_rounds_or_cycles": max_rounds_or_cycles,
        "budget": {
            "max_total_steps": budget_max,
            "spent_steps": spent_steps,
            "remaining_steps": max(0, budget_max - spent_steps),
            "exhausted": spent_steps >= budget_max,
        },
        "blocker_report": {
            "initial_blocker_queue": list(blocker_queue),
            "initial_evidence_gap_queue": list(evidence_gap_queue),
            "latest_quality_blocker_report": latest_report,
            "unresolved_blocker_count": len(unresolved),
            "evidence_gap_count": len(gaps),
        },
        "unresolved_blockers": unresolved,
        "evidence_gaps": gaps,
        "action_trace": deepcopy(action_trace or []),
        "reselection_decisions": deepcopy(reselection_decisions or []),
        "rollback_decisions": deepcopy(rollback_decisions or []),
        "final_workspace": deepcopy(final_workspace) if isinstance(final_workspace, dict) else {},
    }


def _fail_closed_report(
    *,
    request_id: str,
    started_from_mode: str,
    goal: dict[str, Any],
    max_rounds_or_cycles: int,
    budget_max: int,
    spent_steps: int,
    termination_reason: str,
    blocker_queue: list[str],
    evidence_gap_queue: list[str],
    blocker_report: dict[str, Any] | None = None,
    unresolved_blockers: list[str] | None = None,
    evidence_gaps: list[str] | None = None,
    action_trace: list[dict[str, Any]] | None = None,
    reselection_decisions: list[dict[str, Any]] | None = None,
    rollback_decisions: list[dict[str, Any]] | None = None,
    completed_cycles: int = 0,
    final_workspace: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return _build_report(
        request_id=request_id,
        started_from_mode=started_from_mode,
        goal=goal,
        max_rounds_or_cycles=max_rounds_or_cycles,
        budget_max=budget_max,
        spent_steps=spent_steps,
        controller_status="failed_closed",
        termination_reason=termination_reason,
        blocker_queue=blocker_queue,
        evidence_gap_queue=evidence_gap_queue,
        blocker_report=blocker_report,
        unresolved_blockers=unresolved_blockers,
        evidence_gaps=evidence_gaps,
        action_trace=action_trace,
        reselection_decisions=reselection_decisions,
        rollback_decisions=rollback_decisions,
        completed_cycles=completed_cycles,
        final_workspace=final_workspace,
    )


def _normalized_string(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def _string_list(value: Any) -> list[str] | None:
    if not isinstance(value, list):
        return None
    normalized: list[str] = []
    for item in value:
        item_text = _normalized_string(item)
        if not item_text:
            return None
        normalized.append(item_text)
    return normalized


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for item in values:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _extract_mapping(payload: Any, *, preferred_keys: tuple[str, ...]) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    for key in preferred_keys:
        if key in payload:
            value = payload[key]
            if isinstance(value, dict):
                return deepcopy(value)
            return None
    return deepcopy(payload)


def _normalize_quality_output(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    quality_status = _normalized_string(payload.get("quality_status"))
    blocker_report = payload.get("blocker_report")
    unresolved_blockers = _string_list(payload.get("unresolved_blockers"))
    evidence_gaps = _string_list(payload.get("evidence_gaps"))
    if quality_status not in _QUALITY_STATUSES:
        return None
    if not isinstance(blocker_report, dict):
        return None
    if unresolved_blockers is None or evidence_gaps is None:
        return None
    return {
        "quality_status": quality_status,
        "blocker_report": deepcopy(blocker_report),
        "unresolved_blockers": unresolved_blockers,
        "evidence_gaps": evidence_gaps,
    }


def _goal_satisfied(*, goal_target: str, quality_status: str) -> bool:
    if goal_target == "submission_grade_candidate":
        return quality_status == "submission_grade_candidate"
    if goal_target == "near_submission_candidate":
        return quality_status in {"near_submission_candidate", "submission_grade_candidate"}
    return False


def _decision_action(payload: Any) -> str:
    if not isinstance(payload, dict):
        return "none"
    action = _normalized_string(payload.get("action"))
    if not action:
        return "none"
    return action


def _decision_reason(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    return _normalized_string(payload.get("reason"))


def _resolve_terminal_reason(unresolved_blockers: list[str], evidence_gaps: list[str]) -> str:
    if unresolved_blockers:
        return "blockers_not_cleared"
    if evidence_gaps:
        return "evidence_gaps_not_cleared"
    return "max_rounds_or_cycles_exhausted"


def _normalize_goal(goal: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(goal, dict):
        return {
            "target_status": "submission_grade_candidate",
            "summary": "unspecified_goal",
        }
    target_status = _normalized_string(goal.get("target_status"))
    if target_status not in {"submission_grade_candidate", "near_submission_candidate"}:
        target_status = "submission_grade_candidate"
    summary = _normalized_string(goal.get("summary"))
    if not summary:
        summary = "unspecified_goal"
    normalized: dict[str, Any] = {
        "target_status": target_status,
        "summary": summary,
    }
    acceptance = goal.get("acceptance_criteria")
    if isinstance(acceptance, list):
        normalized_acceptance = [item for item in (_normalized_string(v) for v in acceptance) if item]
        if normalized_acceptance:
            normalized["acceptance_criteria"] = normalized_acceptance
    return normalized
