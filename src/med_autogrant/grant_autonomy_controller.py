from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from med_autogrant import grant_autonomy_parts as _grant_autonomy_parts
from med_autogrant.facade_exports import re_export_public_names
from med_autogrant.grant_autonomy_request import validate_grant_autonomy_request
from med_autogrant.grant_autonomy_start import _resolve_grant_autonomy_start
from med_autogrant.grant_governance_adapter import (
    apply_family_governance_to_controller_plan,
    prioritize_closure_package_queue,
)

re_export_public_names(_grant_autonomy_parts, globals())

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
    request_state = validate_grant_autonomy_request(request)
    if not request_state["ok"]:
        return request_state["report"]

    request_id = request_state["request_id"]
    start = request_state["start"]
    start_mode = request_state["start_mode"]
    goal = request_state["goal"]
    goal_target = request_state["goal_target"]
    max_rounds_or_cycles = request_state["max_rounds_or_cycles"]
    budget_max = request_state["budget_max"]
    require_zero_blockers = request_state["require_zero_blockers"]
    require_zero_evidence_gaps = request_state["require_zero_evidence_gaps"]
    controller_plan_input = request_state["controller_plan_input"]
    initial_blockers = request_state["initial_blockers"]
    initial_evidence_gaps = request_state["initial_evidence_gaps"]
    reselection_enabled = request_state["reselection_enabled"]
    rollback_enabled = request_state["rollback_enabled"]
    max_reselections = request_state["max_reselections"]
    max_rollbacks = request_state["max_rollbacks"]

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


    start_result = _resolve_grant_autonomy_start(
        request_id=request_id,
        start=start,
        start_mode=start_mode,
        goal=goal,
        max_rounds_or_cycles=max_rounds_or_cycles,
        budget_max=budget_max,
        initial_blockers=initial_blockers,
        initial_evidence_gaps=initial_evidence_gaps,
        action_trace=action_trace,
        reselection_decisions=reselection_decisions,
        rollback_decisions=rollback_decisions,
        tranche_history=tranche_history,
        spent_steps=spent_steps,
        completed_cycles=completed_cycles,
        latest_blocker_report=latest_blocker_report,
        unresolved_blockers=unresolved_blockers,
        evidence_gaps=evidence_gaps,
        latest_quality_closure_dossier=latest_quality_closure_dossier,
        closure_package_queue=closure_package_queue,
        active_closure_package=active_closure_package,
        reselection_count=reselection_count,
        rollback_count=rollback_count,
        selection_input=selection_input,
        workspace=workspace,
        explicit_controller_plan=explicit_controller_plan,
        controller_plan_input=controller_plan_input,
        selector=selector,
        initializer=initializer,
        discoverer=discoverer,
    )
    if not start_result["ok"]:
        return start_result["report"]

    initial_blockers = start_result["initial_blockers"]
    initial_evidence_gaps = start_result["initial_evidence_gaps"]
    action_trace = start_result["action_trace"]
    reselection_decisions = start_result["reselection_decisions"]
    rollback_decisions = start_result["rollback_decisions"]
    tranche_history = start_result["tranche_history"]
    spent_steps = start_result["spent_steps"]
    completed_cycles = start_result["completed_cycles"]
    latest_blocker_report = start_result["latest_blocker_report"]
    unresolved_blockers = start_result["unresolved_blockers"]
    evidence_gaps = start_result["evidence_gaps"]
    latest_quality_closure_dossier = start_result["latest_quality_closure_dossier"]
    closure_package_queue = start_result["closure_package_queue"]
    active_closure_package = start_result["active_closure_package"]
    reselection_count = start_result["reselection_count"]
    rollback_count = start_result["rollback_count"]
    selection_input = start_result["selection_input"]
    workspace = start_result["workspace"]
    explicit_controller_plan = start_result["explicit_controller_plan"]
    controller_plan_input = start_result["controller_plan_input"]
    max_rounds_or_cycles = start_result["max_rounds_or_cycles"]
    budget_max = start_result["budget_max"]

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
