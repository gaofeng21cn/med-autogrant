from __future__ import annotations

from copy import deepcopy
from typing import Any

from med_autogrant.grant_autonomy_common import (
    _CONTROLLER_ACTIONS,
    _CONTROLLER_STATUSES,
    _normalized_string,
    _string_list,
)
from med_autogrant.grant_autonomy_controller_plan import (
    _finalize_controller_plan,
    _normalize_goal,
)
from med_autogrant.grant_autonomy_quality_payload import (
    _normalize_closure_package,
    _normalize_closure_package_queue,
    _normalize_quality_closure_dossier,
)

_AUTHORITY_RETURN_SHAPES = [
    "domain_owner_receipt",
    "typed_blocker",
    "no_regression_evidence",
]


def _build_controller_execution_boundary() -> dict[str, Any]:
    return {
        "surface_kind": "mag_autonomy_controller_execution_boundary",
        "execution_scope": "bounded_single_opl_provider_attempt",
        "mag_role": "refs_only_domain_authority_action_target",
        "post_start_residency_owner": "one-person-lab",
        "attempt_ledger_owner": "one-person-lab",
        "stage_transition_authority": "one-person-lab",
        "controller_status_role": "mag_domain_controller_result_not_opl_stage_terminal",
        "max_domain_cycles_per_invocation": 1,
        "mag_long_running_driver": False,
        "mag_scheduler_daemon_owner": False,
        "mag_owns_attempt_ledger": False,
        "mag_writes_stage_current_pointer": False,
        "mag_writes_stage_terminal_state": False,
        "mag_selects_next_opl_stage": False,
        "requires_opl_stage_transition_authority": True,
    }


def _build_authority_return(*, termination_reason: str) -> dict[str, Any]:
    if termination_reason == "goal_reached":
        result_shape = "no_regression_evidence"
        refs = {
            "no_regression_evidence_ref": (
                "no-regression:mag/autonomy-controller/bounded-attempt-goal-reached"
            )
        }
    else:
        result_shape = "typed_blocker"
        refs = {
            "typed_blocker_ref": (
                "typed-blocker:mag/autonomy-controller/opl-provider-attempt-required"
                if termination_reason == "opl_provider_attempt_required"
                else f"typed-blocker:mag/autonomy-controller/{termination_reason}"
            )
        }
    return {
        "surface_kind": "mag_autonomy_controller_authority_return",
        "allowed_return_shapes": list(_AUTHORITY_RETURN_SHAPES),
        "result_shape": result_shape,
        "body_policy": "refs_only_no_runtime_or_grant_body",
        "refs": refs,
        "authority_boundary": {
            "mag_writes_opl_attempt_ledger": False,
            "mag_runs_scheduler_daemon": False,
            "mag_returns_runtime_or_grant_body": False,
            "stage_transition_authority": "one-person-lab",
            "controller_status_role": "mag_domain_controller_result_not_opl_stage_terminal",
            "mag_writes_stage_current_pointer": False,
            "mag_writes_stage_terminal_state": False,
            "mag_selects_next_opl_stage": False,
            "requires_opl_stage_transition_authority": True,
        },
    }


def _build_controller_checkpoint(
    *,
    request_id: str,
    final_workspace: dict[str, Any],
    completed_cycles: int,
    spent_steps: int,
    next_controller_action: Any,
) -> dict[str, Any]:
    workspace_id = _normalized_string(final_workspace.get("workspace_id")) or "unknown_workspace"
    request_part = request_id or "unknown_request"
    checkpoint_id = f"grant_autonomy_controller_checkpoint:v1:{request_part}:{workspace_id}:cycles={completed_cycles}:steps={spent_steps}"
    next_action = _normalized_string(next_controller_action)
    if next_action not in _CONTROLLER_ACTIONS:
        next_action = "continue_mainline"
    return {
        "checkpoint_id": checkpoint_id,
        "resume_start_mode": "controller_report",
        "workspace_id": workspace_id,
        "completed_cycles": int(completed_cycles) if isinstance(completed_cycles, int) and completed_cycles >= 0 else 0,
        "next_controller_action": next_action,
    }


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
    controller_plan: dict[str, Any] | None = None,
    tranche_history: list[dict[str, Any]] | None = None,
    completed_cycles: int = 0,
    final_workspace: dict[str, Any] | None = None,
    latest_quality_closure_dossier: dict[str, Any] | None = None,
    closure_package_queue: list[dict[str, Any]] | None = None,
    active_closure_package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if controller_status not in _CONTROLLER_STATUSES:
        controller_status = "failed_closed"
    goal_payload = _normalize_goal(goal)
    unresolved = list(unresolved_blockers or [])
    gaps = list(evidence_gaps or [])
    latest_report = deepcopy(blocker_report) if isinstance(blocker_report, dict) else {}
    final_workspace_payload = deepcopy(final_workspace) if isinstance(final_workspace, dict) else {}
    latest_dossier_payload = (
        deepcopy(latest_quality_closure_dossier)
        if isinstance(latest_quality_closure_dossier, dict)
        else None
    )
    closure_queue_payload = deepcopy(closure_package_queue or [])
    active_closure_payload = deepcopy(active_closure_package) if isinstance(active_closure_package, dict) else None
    tranche_plan_payload = _finalize_controller_plan(
        controller_plan,
        goal=goal_payload,
        controller_status=controller_status,
        termination_reason=termination_reason,
        completed_cycles=completed_cycles,
        unresolved_blockers=unresolved,
        evidence_gaps=gaps,
        tranche_history=tranche_history or [],
        latest_quality_closure_dossier=latest_dossier_payload,
        closure_package_queue=closure_queue_payload,
        active_closure_package=active_closure_payload,
    )
    controller_checkpoint = _build_controller_checkpoint(
        request_id=request_id,
        final_workspace=final_workspace_payload,
        completed_cycles=completed_cycles,
        spent_steps=spent_steps,
        next_controller_action=tranche_plan_payload.get("next_controller_action"),
    )
    return {
        "surface_kind": "grant_autonomy_controller_report",
        "controller_version": 3,
        "controller_checkpoint": controller_checkpoint,
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
        "latest_quality_closure_dossier": latest_dossier_payload,
        "closure_package_queue": closure_queue_payload,
        "active_closure_package": active_closure_payload,
        "controller_plan": tranche_plan_payload,
        "tranche_history": deepcopy(tranche_history or []),
        "final_workspace": final_workspace_payload,
        "controller_execution_boundary": _build_controller_execution_boundary(),
        "authority_return": _build_authority_return(
            termination_reason=termination_reason,
        ),
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
    controller_plan: dict[str, Any] | None = None,
    tranche_history: list[dict[str, Any]] | None = None,
    completed_cycles: int = 0,
    final_workspace: dict[str, Any] | None = None,
    latest_quality_closure_dossier: dict[str, Any] | None = None,
    closure_package_queue: list[dict[str, Any]] | None = None,
    active_closure_package: dict[str, Any] | None = None,
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
        controller_plan=controller_plan,
        tranche_history=tranche_history,
        completed_cycles=completed_cycles,
        final_workspace=final_workspace,
        latest_quality_closure_dossier=latest_quality_closure_dossier,
        closure_package_queue=closure_package_queue,
        active_closure_package=active_closure_package,
    )


def _normalize_resume_seed_from_report(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    if payload.get("surface_kind") != "grant_autonomy_controller_report":
        return None
    controller_version = payload.get("controller_version")
    if controller_version not in {2, 3}:
        return None

    final_workspace = payload.get("final_workspace")
    if not isinstance(final_workspace, dict):
        return None
    completed_cycles = payload.get("completed_cycles")
    if not isinstance(completed_cycles, int) or completed_cycles < 0:
        return None

    budget = payload.get("budget")
    if not isinstance(budget, dict):
        return None
    spent_steps = budget.get("spent_steps")
    if not isinstance(spent_steps, int) or spent_steps < 0:
        return None

    action_trace = payload.get("action_trace")
    if not isinstance(action_trace, list):
        return None
    copied_trace: list[dict[str, Any]] = []
    max_step_index = 0
    for item in action_trace:
        if not isinstance(item, dict):
            return None
        step_index = item.get("step_index")
        if not isinstance(step_index, int) or step_index < 1:
            return None
        if step_index > max_step_index:
            max_step_index = step_index
        copied_trace.append(deepcopy(item))
    if spent_steps and max_step_index != spent_steps:
        return None
    if not spent_steps and copied_trace:
        return None

    blocker_report = payload.get("blocker_report")
    if not isinstance(blocker_report, dict):
        return None
    initial_blocker_queue = _string_list(blocker_report.get("initial_blocker_queue"))
    initial_evidence_gap_queue = _string_list(blocker_report.get("initial_evidence_gap_queue"))
    if initial_blocker_queue is None or initial_evidence_gap_queue is None:
        return None
    latest_quality_blocker_report = blocker_report.get("latest_quality_blocker_report")
    if not isinstance(latest_quality_blocker_report, dict):
        latest_quality_blocker_report = {}

    unresolved_blockers = _string_list(payload.get("unresolved_blockers"))
    evidence_gaps = _string_list(payload.get("evidence_gaps"))
    if unresolved_blockers is None or evidence_gaps is None:
        return None

    reselection_decisions = payload.get("reselection_decisions")
    rollback_decisions = payload.get("rollback_decisions")
    if not isinstance(reselection_decisions, list) or not isinstance(rollback_decisions, list):
        return None
    copied_reselection = []
    for item in reselection_decisions:
        if not isinstance(item, dict):
            return None
        copied_reselection.append(deepcopy(item))
    copied_rollback = []
    for item in rollback_decisions:
        if not isinstance(item, dict):
            return None
        copied_rollback.append(deepcopy(item))

    tranche_history = payload.get("tranche_history")
    if not isinstance(tranche_history, list):
        return None
    copied_tranche_history: list[dict[str, Any]] = []
    for item in tranche_history:
        if not isinstance(item, dict):
            return None
        copied_tranche_history.append(deepcopy(item))

    controller_plan = payload.get("controller_plan")
    if not isinstance(controller_plan, dict):
        return None
    controller_plan_input = {
        "current_tranche": controller_plan.get("current_tranche"),
        "tranche_objective": controller_plan.get("tranche_objective"),
        "tranche_success_gate": controller_plan.get("tranche_success_gate"),
    }

    selection_input: dict[str, Any] | None = None
    workspace_selection = final_workspace.get("selection")
    if isinstance(workspace_selection, dict):
        selection_input = deepcopy(workspace_selection)

    reselection_count = sum(
        1
        for item in copied_reselection
        if item.get("action") == "reselect" and item.get("accepted") is True
    )
    rollback_count = sum(
        1
        for item in copied_rollback
        if item.get("action") == "rollback" and item.get("accepted") is True
    )
    latest_quality_closure_dossier = None
    closure_package_queue: list[dict[str, Any]] = []
    active_closure_package = None
    if controller_version >= 3:
        latest_quality_closure_dossier = _normalize_quality_closure_dossier(payload.get("latest_quality_closure_dossier"))
        if payload.get("latest_quality_closure_dossier") is not None and latest_quality_closure_dossier is None:
            return None
        normalized_queue = _normalize_closure_package_queue(payload.get("closure_package_queue"))
        if normalized_queue is None:
            return None
        closure_package_queue = normalized_queue
        active_payload = payload.get("active_closure_package")
        if active_payload is not None:
            active_closure_package = _normalize_closure_package(active_payload)
            if active_closure_package is None:
                return None
    return {
        "final_workspace": deepcopy(final_workspace),
        "controller_plan_input": controller_plan_input,
        "completed_cycles": completed_cycles,
        "spent_steps": spent_steps,
        "action_trace": copied_trace,
        "reselection_decisions": copied_reselection,
        "rollback_decisions": copied_rollback,
        "reselection_count": reselection_count,
        "rollback_count": rollback_count,
        "tranche_history": copied_tranche_history,
        "initial_blocker_queue": initial_blocker_queue,
        "initial_evidence_gap_queue": initial_evidence_gap_queue,
        "latest_quality_blocker_report": deepcopy(latest_quality_blocker_report),
        "unresolved_blockers": unresolved_blockers,
        "evidence_gaps": evidence_gaps,
        "latest_quality_closure_dossier": latest_quality_closure_dossier,
        "closure_package_queue": closure_package_queue,
        "active_closure_package": active_closure_package,
        "selection_input": selection_input,
    }
