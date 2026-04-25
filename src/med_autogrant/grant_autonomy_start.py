from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from med_autogrant.grant_autonomy_parts import *  # noqa: F401,F403

Discoverer = Callable[[dict[str, Any]], dict[str, Any]]
Selector = Callable[[dict[str, Any]], dict[str, Any]]
Initializer = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]


def _start_fail(**kwargs: Any) -> dict[str, Any]:
    return {"ok": False, "report": _fail_closed_report(**kwargs)}


def _resolve_grant_autonomy_start(
    *,
    request_id: str,
    start: dict[str, Any],
    start_mode: str,
    goal: dict[str, Any],
    max_rounds_or_cycles: int,
    budget_max: int,
    initial_blockers: list[str],
    initial_evidence_gaps: list[str],
    action_trace: list[dict[str, Any]],
    reselection_decisions: list[dict[str, Any]],
    rollback_decisions: list[dict[str, Any]],
    tranche_history: list[dict[str, Any]],
    spent_steps: int,
    completed_cycles: int,
    latest_blocker_report: dict[str, Any],
    unresolved_blockers: list[str],
    evidence_gaps: list[str],
    latest_quality_closure_dossier: dict[str, Any] | None,
    closure_package_queue: list[dict[str, Any]],
    active_closure_package: dict[str, Any] | None,
    reselection_count: int,
    rollback_count: int,
    selection_input: dict[str, Any] | None,
    workspace: dict[str, Any] | None,
    explicit_controller_plan: bool,
    controller_plan_input: Any,
    selector: Selector,
    initializer: Initializer,
    discoverer: Discoverer | None,
) -> dict[str, Any]:
    if start_mode == "controller_report":
        additional_budget_max = budget_max
        additional_cycles = max_rounds_or_cycles
        resume_seed = _normalize_resume_seed_from_report(start.get("controller_report"))
        if resume_seed is None:
            return _start_fail(
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
            return _start_fail(
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
            return _start_fail(
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
            return _start_fail(
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
            return _start_fail(
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
                return _start_fail(
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
                return _start_fail(
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
                return _start_fail(
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
                return _start_fail(
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
                return _start_fail(
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
                return _start_fail(
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
            return _start_fail(
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
            return _start_fail(
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
            return _start_fail(
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
            return _start_fail(
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
            return _start_fail(
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
            return _start_fail(
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
        return _start_fail(
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

    return {
    "ok": True,
    "initial_blockers": initial_blockers,
    "initial_evidence_gaps": initial_evidence_gaps,
    "action_trace": action_trace,
    "reselection_decisions": reselection_decisions,
    "rollback_decisions": rollback_decisions,
    "tranche_history": tranche_history,
    "spent_steps": spent_steps,
    "completed_cycles": completed_cycles,
    "latest_blocker_report": latest_blocker_report,
    "unresolved_blockers": unresolved_blockers,
    "evidence_gaps": evidence_gaps,
    "latest_quality_closure_dossier": latest_quality_closure_dossier,
    "closure_package_queue": closure_package_queue,
    "active_closure_package": active_closure_package,
    "reselection_count": reselection_count,
    "rollback_count": rollback_count,
    "selection_input": selection_input,
    "workspace": workspace,
    "explicit_controller_plan": explicit_controller_plan,
    "controller_plan_input": controller_plan_input,
    "max_rounds_or_cycles": max_rounds_or_cycles,
    "budget_max": budget_max,
    }
