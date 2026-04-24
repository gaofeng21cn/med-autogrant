from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from med_autogrant.grant_autonomy_parts import *  # noqa: F401,F403
from med_autogrant.grant_governance_adapter import (
    apply_family_governance_to_controller_plan,
    prioritize_closure_package_queue,
)

Discoverer = Callable[[dict[str, Any]], dict[str, Any]]
Selector = Callable[[dict[str, Any]], dict[str, Any]]
Initializer = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
MainlineRunner = Callable[[dict[str, Any]], dict[str, Any]]
QualityEvaluator = Callable[[dict[str, Any]], dict[str, Any]]

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
    controller_plan_input = request.get("controller_plan")

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
    tranche_history: list[dict[str, Any]] = []
    spent_steps = 0
    reselection_count = 0
    rollback_count = 0
    completed_cycles = 0
    latest_blocker_report: dict[str, Any] = {}
    unresolved_blockers = list(initial_blockers)
    evidence_gaps = list(initial_evidence_gaps)
    latest_quality_closure_dossier: dict[str, Any] | None = None
    closure_package_queue: list[dict[str, Any]] = []
    active_closure_package: dict[str, Any] | None = None

    selection_input: dict[str, Any] | None = None
    workspace: dict[str, Any] | None = None
    explicit_controller_plan = isinstance(controller_plan_input, dict)

    if start_mode == "controller_report":
        additional_budget_max = budget_max
        additional_cycles = max_rounds_or_cycles
        resume_seed = _normalize_resume_seed_from_report(start.get("controller_report"))
        if resume_seed is None:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="invalid_controller_report",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )

        report_initial_blockers = resume_seed["initial_blocker_queue"]
        report_initial_evidence_gaps = resume_seed["initial_evidence_gap_queue"]
        if initial_blockers and initial_blockers != report_initial_blockers:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="resume_input_queue_mismatch",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )
        if initial_evidence_gaps and initial_evidence_gaps != report_initial_evidence_gaps:
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="resume_input_queue_mismatch",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )

        initial_blockers = report_initial_blockers
        initial_evidence_gaps = report_initial_evidence_gaps
        action_trace = resume_seed["action_trace"]
        reselection_decisions = resume_seed["reselection_decisions"]
        rollback_decisions = resume_seed["rollback_decisions"]
        tranche_history = resume_seed["tranche_history"]
        spent_steps = resume_seed["spent_steps"]
        completed_cycles = resume_seed["completed_cycles"]
        latest_blocker_report = resume_seed["latest_quality_blocker_report"]
        unresolved_blockers = resume_seed["unresolved_blockers"]
        evidence_gaps = resume_seed["evidence_gaps"]
        latest_quality_closure_dossier = resume_seed["latest_quality_closure_dossier"]
        closure_package_queue = resume_seed["closure_package_queue"]
        active_closure_package = resume_seed["active_closure_package"]
        reselection_count = resume_seed["reselection_count"]
        rollback_count = resume_seed["rollback_count"]
        workspace = resume_seed["final_workspace"]
        selection_input = resume_seed.get("selection_input")

        budget_max = spent_steps + additional_budget_max
        max_rounds_or_cycles = completed_cycles + additional_cycles
        if not explicit_controller_plan:
            controller_plan_input = resume_seed["controller_plan_input"]
        explicit_controller_plan = True

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

    if start_mode == "controller_report":
        if not isinstance(workspace, dict):
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="invalid_controller_report",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
                action_trace=action_trace,
                reselection_decisions=reselection_decisions,
                rollback_decisions=rollback_decisions,
            )
    elif start_mode == "workspace":
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

    controller_plan = _normalize_controller_plan(
        controller_plan_input,
        goal=goal,
        require_zero_blockers=require_zero_blockers,
        require_zero_evidence_gaps=require_zero_evidence_gaps,
    )
    controller_plan = apply_family_governance_to_controller_plan(
        controller_plan,
        workspace=workspace,
        explicit_controller_plan=explicit_controller_plan,
    )

    cycle_start = completed_cycles + 1
    for cycle in range(cycle_start, max_rounds_or_cycles + 1):
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
        latest_quality_closure_dossier = normalized_quality["quality_closure_dossier"]
        closure_package_queue = prioritize_closure_package_queue(
            latest_quality_closure_dossier.get("closure_packages"),
            workspace=workspace,
        )
        active_closure_package = deepcopy(closure_package_queue[0]) if closure_package_queue else None
        normalized_quality["active_closure_package"] = deepcopy(active_closure_package)
        if cycle == 1:
            unresolved_blockers = _dedupe(initial_blockers + normalized_quality["unresolved_blockers"])
            evidence_gaps = _dedupe(initial_evidence_gaps + normalized_quality["evidence_gaps"])
        else:
            unresolved_blockers = _dedupe(normalized_quality["unresolved_blockers"])
            evidence_gaps = _dedupe(normalized_quality["evidence_gaps"])
        quality_status = normalized_quality["quality_status"]
        controller_plan = _hydrate_controller_plan_quality_state(
            controller_plan,
            quality_closure_dossier=latest_quality_closure_dossier,
            closure_package_queue=closure_package_queue,
            active_closure_package=active_closure_package,
        )
        effective_require_zero_blockers = bool(controller_plan["tranche_success_gate"]["requires_zero_blockers"])
        effective_require_zero_evidence_gaps = bool(controller_plan["tranche_success_gate"]["requires_zero_evidence_gaps"])
        inline_controller_action = _resolve_inline_controller_action(
            normalized_quality=normalized_quality,
        )
        if inline_controller_action == "fail_closed":
            failure_reason = _resolve_inline_controller_reason(
                normalized_quality=normalized_quality,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
            )
            tranche_history.append(
                _build_tranche_history_entry(
                    cycle=cycle,
                    controller_plan=controller_plan,
                    quality_status=quality_status,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                    next_controller_action="fail_closed",
                    gate_status="failed_closed",
                    decision_reason=failure_reason,
                    termination_reason="quality_fail_closed",
                    quality_closure_dossier=latest_quality_closure_dossier,
                    closure_package_queue=closure_package_queue,
                    active_closure_package=active_closure_package,
                )
            )
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason="quality_fail_closed",
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
                controller_plan=controller_plan,
                tranche_history=tranche_history,
                latest_quality_closure_dossier=latest_quality_closure_dossier,
                closure_package_queue=closure_package_queue,
                active_closure_package=active_closure_package,
            )
        if inline_controller_action == "reselect_project_profile":
            mainline_output = {
                "reselection_decision": {
                    "action": "reselect",
                    "reason": _resolve_inline_controller_reason(
                        normalized_quality=normalized_quality,
                        unresolved_blockers=unresolved_blockers,
                        evidence_gaps=evidence_gaps,
                    ),
                },
                "workspace": deepcopy(workspace),
            }
        else:
            mainline_output = None

        if _goal_satisfied(goal_target=goal_target, quality_status=quality_status) and mainline_output is None:
            if effective_require_zero_blockers and unresolved_blockers:
                tranche_history.append(
                    _build_tranche_history_entry(
                        cycle=cycle,
                        controller_plan=controller_plan,
                        quality_status=quality_status,
                        unresolved_blockers=unresolved_blockers,
                        evidence_gaps=evidence_gaps,
                        next_controller_action="fail_closed",
                        gate_status="failed_closed",
                        decision_reason="blockers_not_cleared",
                        termination_reason="blockers_not_cleared",
                    )
                )
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
                    controller_plan=controller_plan,
                    tranche_history=tranche_history,
                    latest_quality_closure_dossier=latest_quality_closure_dossier,
                    closure_package_queue=closure_package_queue,
                    active_closure_package=active_closure_package,
                )
            if effective_require_zero_evidence_gaps and evidence_gaps:
                tranche_history.append(
                    _build_tranche_history_entry(
                        cycle=cycle,
                        controller_plan=controller_plan,
                        quality_status=quality_status,
                        unresolved_blockers=unresolved_blockers,
                        evidence_gaps=evidence_gaps,
                        next_controller_action="fail_closed",
                        gate_status="failed_closed",
                        decision_reason="evidence_gaps_not_cleared",
                        termination_reason="evidence_gaps_not_cleared",
                    )
                )
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
                    controller_plan=controller_plan,
                    tranche_history=tranche_history,
                    latest_quality_closure_dossier=latest_quality_closure_dossier,
                    closure_package_queue=closure_package_queue,
                    active_closure_package=active_closure_package,
                )
            tranche_history.append(
                _build_tranche_history_entry(
                    cycle=cycle,
                    controller_plan=controller_plan,
                    quality_status=quality_status,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                    next_controller_action="stop_success",
                    gate_status="passed",
                    decision_reason="tranche_success_gate_satisfied",
                    termination_reason="goal_reached",
                )
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
                controller_plan=controller_plan,
                tranche_history=tranche_history,
                completed_cycles=completed_cycles,
                final_workspace=workspace,
                latest_quality_closure_dossier=latest_quality_closure_dossier,
                closure_package_queue=closure_package_queue,
                active_closure_package=active_closure_package,
            )

        if cycle == max_rounds_or_cycles:
            terminal_reason = _resolve_terminal_reason(unresolved_blockers, evidence_gaps)
            tranche_history.append(
                _build_tranche_history_entry(
                    cycle=cycle,
                    controller_plan=controller_plan,
                    quality_status=quality_status,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                    next_controller_action="fail_closed",
                    gate_status="blocked" if terminal_reason != "max_rounds_or_cycles_exhausted" else "failed_closed",
                    decision_reason=terminal_reason,
                    termination_reason=terminal_reason,
                )
            )
            return _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode,
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=spent_steps,
                termination_reason=terminal_reason,
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
                controller_plan=controller_plan,
                tranche_history=tranche_history,
                latest_quality_closure_dossier=latest_quality_closure_dossier,
                closure_package_queue=closure_package_queue,
                active_closure_package=active_closure_package,
            )

        if mainline_output is None:
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
                        "controller_plan": deepcopy(controller_plan),
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

        rollback_reason = ""
        rollback_action = _decision_action(mainline_output.get("rollback_decision"))
        if rollback_action == "rollback":
            rollback_reason = _decision_reason(mainline_output.get("rollback_decision"))
            allowed = rollback_enabled and rollback_count < max_rollbacks
            rollback_decisions.append(
                {
                    "cycle": cycle,
                    "action": rollback_action,
                    "accepted": allowed,
                    "reason": rollback_reason,
                }
            )
            if not rollback_enabled:
                tranche_history.append(
                    _build_tranche_history_entry(
                        cycle=cycle,
                        controller_plan=controller_plan,
                        quality_status=quality_status,
                        unresolved_blockers=unresolved_blockers,
                        evidence_gaps=evidence_gaps,
                        next_controller_action="rollback_upstream",
                        gate_status="failed_closed",
                        decision_reason=rollback_reason,
                        termination_reason="rollback_policy_disallowed",
                    )
                )
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
                    controller_plan=controller_plan,
                    tranche_history=tranche_history,
                )
            if rollback_count >= max_rollbacks:
                tranche_history.append(
                    _build_tranche_history_entry(
                        cycle=cycle,
                        controller_plan=controller_plan,
                        quality_status=quality_status,
                        unresolved_blockers=unresolved_blockers,
                        evidence_gaps=evidence_gaps,
                        next_controller_action="rollback_upstream",
                        gate_status="failed_closed",
                        decision_reason=rollback_reason,
                        termination_reason="rollback_budget_exhausted",
                    )
                )
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
                    controller_plan=controller_plan,
                    tranche_history=tranche_history,
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
                tranche_history.append(
                    _build_tranche_history_entry(
                        cycle=cycle,
                        controller_plan=controller_plan,
                        quality_status=quality_status,
                        unresolved_blockers=unresolved_blockers,
                        evidence_gaps=evidence_gaps,
                        next_controller_action="reselect_project_profile",
                        gate_status="failed_closed",
                        decision_reason=decision_reason,
                        termination_reason="reselection_policy_disallowed",
                    )
                )
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
                    controller_plan=controller_plan,
                    tranche_history=tranche_history,
                )
            if selection_input is None:
                tranche_history.append(
                    _build_tranche_history_entry(
                        cycle=cycle,
                        controller_plan=controller_plan,
                        quality_status=quality_status,
                        unresolved_blockers=unresolved_blockers,
                        evidence_gaps=evidence_gaps,
                        next_controller_action="reselect_project_profile",
                        gate_status="failed_closed",
                        decision_reason=decision_reason,
                        termination_reason="reselection_requires_selection_input",
                    )
                )
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
                    controller_plan=controller_plan,
                    tranche_history=tranche_history,
                )
            if reselection_count >= max_reselections:
                tranche_history.append(
                    _build_tranche_history_entry(
                        cycle=cycle,
                        controller_plan=controller_plan,
                        quality_status=quality_status,
                        unresolved_blockers=unresolved_blockers,
                        evidence_gaps=evidence_gaps,
                        next_controller_action="reselect_project_profile",
                        gate_status="failed_closed",
                        decision_reason=decision_reason,
                        termination_reason="reselection_budget_exhausted",
                    )
                )
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
                    controller_plan=controller_plan,
                    tranche_history=tranche_history,
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
            tranche_history.append(
                _build_tranche_history_entry(
                    cycle=cycle,
                    controller_plan=controller_plan,
                    quality_status=quality_status,
                    unresolved_blockers=unresolved_blockers,
                    evidence_gaps=evidence_gaps,
                    next_controller_action="reselect_project_profile",
                    gate_status="open",
                    decision_reason=decision_reason,
                    termination_reason="in_progress",
                )
            )
            workspace = reselected_workspace
            controller_plan = apply_family_governance_to_controller_plan(
                controller_plan,
                workspace=workspace,
                explicit_controller_plan=explicit_controller_plan,
            )
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
        tranche_history.append(
            _build_tranche_history_entry(
                cycle=cycle,
                controller_plan=controller_plan,
                quality_status=quality_status,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
                next_controller_action="rollback_upstream" if rollback_reason else "continue_mainline",
                gate_status="open",
                decision_reason=rollback_reason or _default_progress_reason(quality_status, unresolved_blockers, evidence_gaps),
                termination_reason="in_progress",
            )
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
        controller_plan=controller_plan,
        tranche_history=tranche_history,
    )
