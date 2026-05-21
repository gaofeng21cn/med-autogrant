from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from med_autogrant.grant_autonomy_parts import (
    _decision_action,
    _decision_reason,
    _dedupe,
    _default_progress_reason,
    _extract_mapping,
    _goal_satisfied,
    _hydrate_controller_plan_quality_state,
    _normalize_quality_output,
    _resolve_inline_controller_action,
    _resolve_inline_controller_reason,
    _resolve_terminal_reason,
)
from med_autogrant.grant_autonomy_loop_parts import (
    GrantAutonomyLoopContext,
    append_tranche_history,
)
from med_autogrant.grant_autonomy_trace import spend_budget_step
from med_autogrant.grant_governance_adapter import (
    apply_family_governance_to_controller_plan,
    prioritize_closure_package_queue,
)

Selector = Callable[[dict[str, Any]], dict[str, Any]]
Initializer = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]
MainlineRunner = Callable[[dict[str, Any]], dict[str, Any]]
QualityEvaluator = Callable[[dict[str, Any]], dict[str, Any]]


def run_grant_autonomy_loop(
    *,
    request_id: str,
    start_mode: str,
    goal: dict[str, Any],
    goal_target: str,
    max_rounds_or_cycles: int,
    budget_max: int,
    spent_steps: int,
    initial_blockers: list[str],
    initial_evidence_gaps: list[str],
    action_trace: list[dict[str, Any]],
    reselection_decisions: list[dict[str, Any]],
    rollback_decisions: list[dict[str, Any]],
    tranche_history: list[dict[str, Any]],
    completed_cycles: int,
    latest_blocker_report: dict[str, Any],
    unresolved_blockers: list[str],
    evidence_gaps: list[str],
    latest_quality_closure_dossier: dict[str, Any] | None,
    closure_package_queue: list[dict[str, Any]],
    active_closure_package: dict[str, Any] | None,
    controller_plan: dict[str, Any],
    selection_input: dict[str, Any] | None,
    workspace: dict[str, Any] | None,
    explicit_controller_plan: bool,
    reselection_enabled: bool,
    rollback_enabled: bool,
    max_reselections: int,
    max_rollbacks: int,
    reselection_count: int,
    rollback_count: int,
    selector: Selector,
    initializer: Initializer,
    mainline_runner: MainlineRunner,
    quality_evaluator: QualityEvaluator,
) -> dict[str, Any]:
    loop_context = GrantAutonomyLoopContext(
        request_id=request_id,
        start_mode=start_mode,
        goal=goal,
        max_rounds_or_cycles=max_rounds_or_cycles,
        budget_max=budget_max,
        initial_blockers=initial_blockers,
        initial_evidence_gaps=initial_evidence_gaps,
        action_trace=action_trace,
        reselection_decisions=reselection_decisions,
        rollback_decisions=rollback_decisions,
    )

    def spend_budget(*, step_action: str, cycle: int | None) -> bool:
        nonlocal spent_steps
        ok, spent_steps = spend_budget_step(
            spent_steps=spent_steps,
            budget_max=budget_max,
            action_trace=action_trace,
            step_action=step_action,
            cycle=cycle,
        )
        return ok

    def fail_closed(
        *,
        termination_reason: str,
        include_controller_state: bool = False,
        include_quality_state: bool = False,
    ) -> dict[str, Any]:
        return loop_context.fail_closed_report(
            spent_steps=spent_steps,
            termination_reason=termination_reason,
            completed_cycles=completed_cycles,
            workspace=workspace,
            latest_blocker_report=latest_blocker_report,
            unresolved_blockers=unresolved_blockers,
            evidence_gaps=evidence_gaps,
            controller_plan=controller_plan if include_controller_state else None,
            tranche_history=tranche_history if include_controller_state else None,
            latest_quality_closure_dossier=(
                latest_quality_closure_dossier if include_quality_state else None
            ),
            closure_package_queue=closure_package_queue if include_quality_state else None,
            active_closure_package=active_closure_package if include_quality_state else None,
        )

    def record_history(
        *,
        cycle: int,
        quality_status: str,
        next_controller_action: str,
        gate_status: str,
        decision_reason: str,
        termination_reason: str,
        include_quality_state: bool = False,
    ) -> None:
        append_tranche_history(
            tranche_history,
            cycle=cycle,
            controller_plan=controller_plan,
            quality_status=quality_status,
            unresolved_blockers=unresolved_blockers,
            evidence_gaps=evidence_gaps,
            next_controller_action=next_controller_action,
            gate_status=gate_status,
            decision_reason=decision_reason,
            termination_reason=termination_reason,
            latest_quality_closure_dossier=(
                latest_quality_closure_dossier if include_quality_state else None
            ),
            closure_package_queue=closure_package_queue if include_quality_state else None,
            active_closure_package=active_closure_package if include_quality_state else None,
        )

    cycle_start = completed_cycles + 1
    for cycle in range(cycle_start, max_rounds_or_cycles + 1):
        completed_cycles = cycle

        if not spend_budget(step_action="quality_evaluator", cycle=cycle):
            return fail_closed(termination_reason="budget_exhausted")
        try:
            quality_output = quality_evaluator(workspace)
        except Exception:
            return fail_closed(termination_reason="quality_evaluator_callback_error")
        normalized_quality = _normalize_quality_output(quality_output)
        if normalized_quality is None:
            return fail_closed(termination_reason="quality_evaluator_unstructured_result")

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
            record_history(
                cycle=cycle,
                quality_status=quality_status,
                next_controller_action="fail_closed",
                gate_status="failed_closed",
                decision_reason=failure_reason,
                termination_reason="quality_fail_closed",
                include_quality_state=True,
            )
            return fail_closed(
                termination_reason="quality_fail_closed",
                include_controller_state=True,
                include_quality_state=True,
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
                record_history(
                    cycle=cycle,
                    quality_status=quality_status,
                    next_controller_action="fail_closed",
                    gate_status="failed_closed",
                    decision_reason="blockers_not_cleared",
                    termination_reason="blockers_not_cleared",
                )
                return fail_closed(
                    termination_reason="blockers_not_cleared",
                    include_controller_state=True,
                    include_quality_state=True,
                )
            if effective_require_zero_evidence_gaps and evidence_gaps:
                record_history(
                    cycle=cycle,
                    quality_status=quality_status,
                    next_controller_action="fail_closed",
                    gate_status="failed_closed",
                    decision_reason="evidence_gaps_not_cleared",
                    termination_reason="evidence_gaps_not_cleared",
                )
                return fail_closed(
                    termination_reason="evidence_gaps_not_cleared",
                    include_controller_state=True,
                    include_quality_state=True,
                )
            record_history(
                cycle=cycle,
                quality_status=quality_status,
                next_controller_action="stop_success",
                gate_status="passed",
                decision_reason="tranche_success_gate_satisfied",
                termination_reason="goal_reached",
            )
            return loop_context.success_report(
                spent_steps=spent_steps,
                controller_status=quality_status,
                termination_reason="goal_reached",
                completed_cycles=completed_cycles,
                workspace=workspace,
                latest_blocker_report=latest_blocker_report,
                unresolved_blockers=unresolved_blockers,
                evidence_gaps=evidence_gaps,
                controller_plan=controller_plan,
                tranche_history=tranche_history,
                latest_quality_closure_dossier=latest_quality_closure_dossier,
                closure_package_queue=closure_package_queue,
                active_closure_package=active_closure_package,
            )

        if cycle == max_rounds_or_cycles:
            terminal_reason = _resolve_terminal_reason(unresolved_blockers, evidence_gaps)
            record_history(
                cycle=cycle,
                quality_status=quality_status,
                next_controller_action="fail_closed",
                gate_status="blocked" if terminal_reason != "max_rounds_or_cycles_exhausted" else "failed_closed",
                decision_reason=terminal_reason,
                termination_reason=terminal_reason,
            )
            return fail_closed(
                termination_reason=terminal_reason,
                include_controller_state=True,
                include_quality_state=True,
            )

        if mainline_output is None:
            if not spend_budget(step_action="mainline_runner", cycle=cycle):
                return fail_closed(termination_reason="budget_exhausted")
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
                return fail_closed(termination_reason="mainline_runner_callback_error")
            if not isinstance(mainline_output, dict):
                return fail_closed(termination_reason="mainline_runner_unstructured_result")

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
                record_history(
                    cycle=cycle,
                    quality_status=quality_status,
                    next_controller_action="rollback_upstream",
                    gate_status="failed_closed",
                    decision_reason=rollback_reason,
                    termination_reason="rollback_policy_disallowed",
                )
                return fail_closed(
                    termination_reason="rollback_policy_disallowed",
                    include_controller_state=True,
                )
            if rollback_count >= max_rollbacks:
                record_history(
                    cycle=cycle,
                    quality_status=quality_status,
                    next_controller_action="rollback_upstream",
                    gate_status="failed_closed",
                    decision_reason=rollback_reason,
                    termination_reason="rollback_budget_exhausted",
                )
                return fail_closed(
                    termination_reason="rollback_budget_exhausted",
                    include_controller_state=True,
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
                record_history(
                    cycle=cycle,
                    quality_status=quality_status,
                    next_controller_action="reselect_project_profile",
                    gate_status="failed_closed",
                    decision_reason=decision_reason,
                    termination_reason="reselection_policy_disallowed",
                )
                return fail_closed(
                    termination_reason="reselection_policy_disallowed",
                    include_controller_state=True,
                )
            if selection_input is None:
                record_history(
                    cycle=cycle,
                    quality_status=quality_status,
                    next_controller_action="reselect_project_profile",
                    gate_status="failed_closed",
                    decision_reason=decision_reason,
                    termination_reason="reselection_requires_selection_input",
                )
                return fail_closed(
                    termination_reason="reselection_requires_selection_input",
                    include_controller_state=True,
                )
            if reselection_count >= max_reselections:
                record_history(
                    cycle=cycle,
                    quality_status=quality_status,
                    next_controller_action="reselect_project_profile",
                    gate_status="failed_closed",
                    decision_reason=decision_reason,
                    termination_reason="reselection_budget_exhausted",
                )
                return fail_closed(
                    termination_reason="reselection_budget_exhausted",
                    include_controller_state=True,
                )

            if not spend_budget(step_action="selector", cycle=cycle):
                return fail_closed(termination_reason="budget_exhausted")
            try:
                reselection_output = selector(selection_input)
            except Exception:
                return fail_closed(termination_reason="selector_callback_error")
            if not isinstance(reselection_output, dict):
                return fail_closed(termination_reason="selector_unstructured_result")

            if not spend_budget(step_action="initializer", cycle=cycle):
                return fail_closed(termination_reason="budget_exhausted")
            try:
                reinit_output = initializer(selection_input, reselection_output)
            except Exception:
                return fail_closed(termination_reason="initializer_callback_error")
            reselected_workspace = _extract_mapping(
                reinit_output,
                preferred_keys=("workspace", "initialized_workspace"),
            )
            if reselected_workspace is None:
                return fail_closed(termination_reason="initializer_unstructured_result")
            record_history(
                cycle=cycle,
                quality_status=quality_status,
                next_controller_action="reselect_project_profile",
                gate_status="open",
                decision_reason=decision_reason,
                termination_reason="in_progress",
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
            return fail_closed(termination_reason="mainline_runner_missing_workspace")
        record_history(
            cycle=cycle,
            quality_status=quality_status,
            next_controller_action="rollback_upstream" if rollback_reason else "continue_mainline",
            gate_status="open",
            decision_reason=rollback_reason or _default_progress_reason(quality_status, unresolved_blockers, evidence_gaps),
            termination_reason="in_progress",
        )
        workspace = next_workspace

    return fail_closed(
        termination_reason=_resolve_terminal_reason(unresolved_blockers, evidence_gaps),
        include_controller_state=True,
    )
