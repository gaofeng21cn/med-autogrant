from __future__ import annotations

from copy import deepcopy
from typing import Any

from med_autogrant.grant_governance_adapter import (
    apply_family_governance_to_controller_plan,
    prioritize_closure_package_queue,
)

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
_CONTROLLER_ACTIONS = {
    "continue_mainline",
    "stop_success",
    "rollback_upstream",
    "reselect_project_profile",
    "fail_closed",
}
_GATE_STATUSES = {
    "open",
    "passed",
    "blocked",
    "failed_closed",
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
    evidence_supply_queue = _normalize_evidence_supply_queue(payload.get("evidence_supply_queue"))
    quality_closure_dossier = _normalize_quality_closure_dossier(payload.get("quality_closure_dossier"))
    if evidence_supply_queue is None or quality_closure_dossier is None:
        return None
    return {
        "quality_status": quality_status,
        "blocker_report": deepcopy(blocker_report),
        "unresolved_blockers": unresolved_blockers,
        "evidence_gaps": evidence_gaps,
        "evidence_supply_queue": evidence_supply_queue,
        "quality_closure_dossier": quality_closure_dossier,
    }

def _normalize_quality_closure_dossier(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    if payload.get("surface_kind") != "grant_quality_closure_dossier":
        return None
    if payload.get("dossier_version") != 1:
        return None
    workspace_surface_kind = _normalized_string(payload.get("workspace_surface_kind"))
    grant_run_id = _normalized_string(payload.get("grant_run_id"))
    workspace_id = _normalized_string(payload.get("workspace_id"))
    lifecycle_stage = _normalized_string(payload.get("lifecycle_stage"))
    draft_id_raw = payload.get("draft_id")
    draft_id = None
    if draft_id_raw is not None:
        draft_id = _normalized_string(draft_id_raw) or None
    quality_summary = _normalize_quality_summary(payload.get("quality_summary"))
    unclosed_hard_issues = _string_list(payload.get("unclosed_hard_issues"))
    evidence_supply_queue_summary = payload.get("evidence_supply_queue_summary")
    closure_packages = _normalize_closure_package_queue(payload.get("closure_packages"))
    if workspace_surface_kind != "nsfc_workspace":
        return None
    if not grant_run_id or not workspace_id or not lifecycle_stage:
        return None
    if quality_summary is None or unclosed_hard_issues is None:
        return None
    if not isinstance(evidence_supply_queue_summary, dict) or closure_packages is None:
        return None
    return {
        "surface_kind": "grant_quality_closure_dossier",
        "dossier_version": 1,
        "workspace_surface_kind": "nsfc_workspace",
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "draft_id": draft_id,
        "quality_summary": quality_summary,
        "unclosed_hard_issues": unclosed_hard_issues,
        "evidence_supply_queue_summary": deepcopy(evidence_supply_queue_summary),
        "closure_packages": closure_packages,
    }

def _normalize_quality_summary(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    overall_status = _normalized_string(payload.get("overall_status"))
    overall_score = payload.get("overall_score")
    summary = _normalized_string(payload.get("summary"))
    loop_gate = payload.get("loop_gate")
    if overall_status not in {"blocked", "near_submission_candidate", "submission_grade_candidate"}:
        return None
    if not isinstance(overall_score, int):
        return None
    if not summary or not isinstance(loop_gate, dict):
        return None
    gate_action = _normalized_string(loop_gate.get("action"))
    gate_reason = _normalized_string(loop_gate.get("reason"))
    gate_stage = _normalized_string(loop_gate.get("recommended_stage")) or None
    if gate_action not in {"ready_for_submission", "continue", "rollback_required"}:
        return None
    if not gate_reason:
        return None
    return {
        "overall_status": overall_status,
        "overall_score": max(0, min(overall_score, 100)),
        "summary": summary,
        "loop_gate": {
            "action": gate_action,
            "recommended_stage": gate_stage,
            "reason": gate_reason,
        },
    }

def _normalize_closure_package_queue(payload: Any) -> list[dict[str, Any]] | None:
    if not isinstance(payload, list):
        return None
    normalized: list[dict[str, Any]] = []
    for item in payload:
        package = _normalize_closure_package(item)
        if package is None:
            return None
        normalized.append(package)
    return normalized

def _normalize_closure_package(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    closure_id = _normalized_string(payload.get("closure_id"))
    summary = _normalized_string(payload.get("summary"))
    severity = _normalized_string(payload.get("severity"))
    action = _normalized_string(payload.get("action"))
    target_stage = _normalized_string(payload.get("target_stage")) or None
    required_input_ids = _string_list(payload.get("required_input_ids"))
    evidence_refs = _string_list(payload.get("evidence_refs"))
    linked_issue_ids = _string_list(payload.get("linked_issue_ids"))
    blocking_reasons = _string_list(payload.get("blocking_reasons"))
    evidence_obligations = payload.get("evidence_obligations")
    acceptance_signals = payload.get("acceptance_signals")
    if not closure_id or not summary:
        return None
    if severity not in {"hard", "gap"}:
        return None
    if action not in _CONTROLLER_ACTIONS - {"stop_success"}:
        return None
    if (
        required_input_ids is None
        or evidence_refs is None
        or linked_issue_ids is None
        or blocking_reasons is None
    ):
        return None
    if not isinstance(evidence_obligations, list) or not isinstance(acceptance_signals, list):
        return None
    if any(not isinstance(item, dict) for item in evidence_obligations):
        return None
    if any(not isinstance(item, dict) for item in acceptance_signals):
        return None
    return {
        "closure_id": closure_id,
        "summary": summary,
        "severity": severity,
        "target_stage": target_stage,
        "action": action,
        "required_input_ids": required_input_ids,
        "evidence_refs": evidence_refs,
        "linked_issue_ids": linked_issue_ids,
        "blocking_reasons": blocking_reasons,
        "evidence_obligations": deepcopy(evidence_obligations),
        "acceptance_signals": deepcopy(acceptance_signals),
    }

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

def _normalize_controller_plan(
    payload: Any,
    *,
    goal: dict[str, Any],
    require_zero_blockers: bool,
    require_zero_evidence_gaps: bool,
) -> dict[str, Any]:
    goal_payload = _normalize_goal(goal)
    source = payload if isinstance(payload, dict) else {}
    current_tranche = _normalized_string(source.get("current_tranche"))
    if not current_tranche:
        current_tranche = (
            "submission_readiness"
            if goal_payload["target_status"] == "submission_grade_candidate"
            else "quality_closure"
        )
    tranche_objective = _normalized_string(source.get("tranche_objective"))
    if not tranche_objective:
        tranche_objective = f"advance_to_{goal_payload['target_status']}"
    gate_source = source.get("tranche_success_gate") if isinstance(source.get("tranche_success_gate"), dict) else {}
    gate_target = _normalized_string(gate_source.get("target_status"))
    if gate_target not in {"submission_grade_candidate", "near_submission_candidate"}:
        gate_target = goal_payload["target_status"]
    acceptance = gate_source.get("acceptance_criteria")
    if not isinstance(acceptance, list):
        acceptance = goal_payload.get("acceptance_criteria")
    normalized_acceptance = [item for item in (_normalized_string(v) for v in (acceptance or [])) if item]
    tranche_success_gate: dict[str, Any] = {
        "target_status": gate_target,
        "requires_zero_blockers": bool(gate_source.get("requires_zero_blockers", require_zero_blockers)),
        "requires_zero_evidence_gaps": bool(gate_source.get("requires_zero_evidence_gaps", require_zero_evidence_gaps)),
    }
    if normalized_acceptance:
        tranche_success_gate["acceptance_criteria"] = normalized_acceptance
    return {
        "current_tranche": current_tranche,
        "tranche_objective": tranche_objective,
        "tranche_success_gate": tranche_success_gate,
    }

def _normalize_evidence_supply_queue(payload: Any) -> list[dict[str, Any]] | None:
    if payload is None:
        return []
    if not isinstance(payload, list):
        return None
    normalized: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict):
            return None
        gap_id = _normalized_string(item.get("gap_id"))
        controller_action_hint = _normalize_controller_action_hint(item.get("controller_action_hint"))
        gap_kind = _normalized_string(item.get("gap_kind"))
        gap_summary = _normalized_string(item.get("gap_summary"))
        required_input_ids = _string_list(item.get("required_input_ids"))
        linked_issue_ids = _string_list(item.get("linked_issue_ids"))
        if not gap_id or controller_action_hint is None or not gap_kind:
            return None
        if required_input_ids is None or linked_issue_ids is None:
            return None
        normalized.append(
            {
                "gap_id": gap_id,
                "controller_action_hint": controller_action_hint,
                "gap_kind": gap_kind,
                "gap_summary": gap_summary,
                "required_input_ids": required_input_ids,
                "linked_issue_ids": linked_issue_ids,
            }
        )
    return normalized

def _normalize_controller_action_hint(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    action = _normalized_string(payload.get("action"))
    summary = _normalized_string(payload.get("summary"))
    source_surface = _normalized_string(payload.get("source_surface"))
    if action not in _CONTROLLER_ACTIONS - {"stop_success"}:
        return None
    if not summary or not source_surface:
        return None
    return {
        "action": action,
        "summary": summary,
        "target_stage": _normalized_string(payload.get("target_stage")) or None,
        "source_surface": source_surface,
    }

def _active_closure_package_action(active_closure_package: dict[str, Any] | None) -> str | None:
    if not isinstance(active_closure_package, dict):
        return None
    action = _normalized_string(active_closure_package.get("action"))
    if action not in _CONTROLLER_ACTIONS - {"stop_success"}:
        return None
    return action

def _closure_package_queue_ids(closure_package_queue: list[dict[str, Any]] | None) -> list[str]:
    return [
        closure_id
        for item in closure_package_queue or []
        for closure_id in [_normalized_string(item.get("closure_id"))]
        if closure_id
    ]

def _hydrate_controller_plan_quality_state(
    controller_plan: dict[str, Any] | None,
    *,
    quality_closure_dossier: dict[str, Any] | None,
    closure_package_queue: list[dict[str, Any]] | None,
    active_closure_package: dict[str, Any] | None,
) -> dict[str, Any]:
    hydrated = deepcopy(controller_plan) if isinstance(controller_plan, dict) else {}
    quality_summary = deepcopy(hydrated.get("quality_summary"))
    if isinstance(quality_closure_dossier, dict):
        quality_summary = deepcopy(quality_closure_dossier.get("quality_summary"))
    closure_ids = list(hydrated.get("closure_package_queue_ids") or [])
    if closure_package_queue is not None:
        closure_ids = _closure_package_queue_ids(closure_package_queue)
    active_closure_package_id = hydrated.get("active_closure_package_id")
    active_closure_package_action = hydrated.get("active_closure_package_action")
    active_closure_package_target_stage = hydrated.get("active_closure_package_target_stage")
    if isinstance(active_closure_package, dict):
        active_closure_package_id = _normalized_string(active_closure_package.get("closure_id")) or None
        active_closure_package_action = _active_closure_package_action(active_closure_package)
        active_closure_package_target_stage = _normalized_string(active_closure_package.get("target_stage")) or None
    hydrated["quality_summary"] = deepcopy(quality_summary)
    hydrated["closure_package_queue_ids"] = closure_ids
    hydrated["active_closure_package_id"] = active_closure_package_id
    hydrated["active_closure_package_action"] = active_closure_package_action
    hydrated["active_closure_package_target_stage"] = active_closure_package_target_stage
    return hydrated

def _resolve_inline_controller_action(
    *,
    normalized_quality: dict[str, Any],
) -> str:
    active_action = _active_closure_package_action(normalized_quality.get("active_closure_package"))
    if active_action in {"fail_closed", "reselect_project_profile"}:
        return active_action
    action_hints = [
        item["controller_action_hint"]["action"]
        for item in normalized_quality.get("evidence_supply_queue", [])
        if item["controller_action_hint"]["action"] in {"reselect_project_profile"}
    ]
    return action_hints[0] if action_hints else ""

def _resolve_inline_controller_reason(
    *,
    normalized_quality: dict[str, Any],
    unresolved_blockers: list[str],
    evidence_gaps: list[str],
) -> str:
    active_closure_package = normalized_quality.get("active_closure_package")
    if isinstance(active_closure_package, dict):
        summary = _normalized_string(active_closure_package.get("summary"))
        if summary:
            return summary
        blocking_reasons = _string_list(active_closure_package.get("blocking_reasons"))
        if blocking_reasons:
            return blocking_reasons[0]
    supply_queue = normalized_quality.get("evidence_supply_queue", [])
    if supply_queue:
        first = supply_queue[0]
        summary = first["controller_action_hint"].get("summary")
        if isinstance(summary, str) and summary.strip():
            return summary.strip()
        if first["gap_kind"] == "funding_profile_mismatch":
            return "quality_supply_requires_reselection"
        gap_summary = first.get("gap_summary")
        if isinstance(gap_summary, str) and gap_summary.strip():
            return gap_summary.strip()
        return first["gap_kind"]
    return _default_progress_reason(normalized_quality["quality_status"], unresolved_blockers, evidence_gaps)

def _build_tranche_history_entry(
    *,
    cycle: int,
    controller_plan: dict[str, Any],
    quality_status: str,
    unresolved_blockers: list[str],
    evidence_gaps: list[str],
    next_controller_action: str,
    gate_status: str,
    decision_reason: str,
    termination_reason: str,
    quality_closure_dossier: dict[str, Any] | None = None,
    closure_package_queue: list[dict[str, Any]] | None = None,
    active_closure_package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    hydrated_plan = _hydrate_controller_plan_quality_state(
        controller_plan,
        quality_closure_dossier=quality_closure_dossier,
        closure_package_queue=closure_package_queue,
        active_closure_package=active_closure_package,
    )
    action = next_controller_action if next_controller_action in _CONTROLLER_ACTIONS else "continue_mainline"
    normalized_gate_status = gate_status if gate_status in _GATE_STATUSES else "open"
    normalized_quality_status = quality_status if quality_status in _QUALITY_STATUSES else "unknown"
    reason = _normalized_string(decision_reason) or termination_reason or "controller_progression"
    tranche_success_gate = hydrated_plan.get("tranche_success_gate")
    return {
        "cycle": cycle,
        "current_tranche": hydrated_plan.get("current_tranche") or "submission_readiness",
        "tranche_objective": hydrated_plan.get("tranche_objective") or "advance_to_submission_grade_candidate",
        "tranche_success_gate": deepcopy(tranche_success_gate) if isinstance(tranche_success_gate, dict) else {},
        "gate_status": normalized_gate_status,
        "next_controller_action": action,
        "decision_reason": reason,
        "quality_status": normalized_quality_status,
        "unresolved_blockers": list(unresolved_blockers),
        "evidence_gaps": list(evidence_gaps),
        "quality_summary": deepcopy(hydrated_plan.get("quality_summary")),
        "closure_package_queue_ids": list(hydrated_plan.get("closure_package_queue_ids") or []),
        "active_closure_package_id": hydrated_plan.get("active_closure_package_id"),
        "active_closure_package_action": hydrated_plan.get("active_closure_package_action"),
        "active_closure_package_target_stage": hydrated_plan.get("active_closure_package_target_stage"),
        "termination_reason": termination_reason or "in_progress",
    }

def _default_progress_reason(quality_status: str, unresolved_blockers: list[str], evidence_gaps: list[str]) -> str:
    if unresolved_blockers:
        return unresolved_blockers[0]
    if evidence_gaps:
        return evidence_gaps[0]
    if quality_status == "not_ready":
        return "quality_gate_open"
    return "controller_progression"

def _finalize_controller_plan(
    payload: dict[str, Any] | None,
    *,
    goal: dict[str, Any],
    controller_status: str,
    termination_reason: str,
    completed_cycles: int,
    unresolved_blockers: list[str],
    evidence_gaps: list[str],
    tranche_history: list[dict[str, Any]],
    latest_quality_closure_dossier: dict[str, Any] | None = None,
    closure_package_queue: list[dict[str, Any]] | None = None,
    active_closure_package: dict[str, Any] | None = None,
) -> dict[str, Any]:
    base_plan = _normalize_controller_plan(
        payload,
        goal=goal,
        require_zero_blockers=True,
        require_zero_evidence_gaps=True,
    )
    base_plan = _hydrate_controller_plan_quality_state(
        base_plan,
        quality_closure_dossier=latest_quality_closure_dossier,
        closure_package_queue=closure_package_queue,
        active_closure_package=active_closure_package,
    )
    latest_history = tranche_history[-1] if tranche_history else {}
    decision_basis = {
        "cycle": int(latest_history.get("cycle") or completed_cycles or 0),
        "gate_status": latest_history.get("gate_status") or ("passed" if controller_status != "failed_closed" else "failed_closed"),
        "quality_status": latest_history.get("quality_status") or "unknown",
        "unresolved_blockers": list(latest_history.get("unresolved_blockers") or unresolved_blockers),
        "evidence_gaps": list(latest_history.get("evidence_gaps") or evidence_gaps),
        "quality_summary": deepcopy(latest_history.get("quality_summary")) if latest_history else deepcopy(base_plan.get("quality_summary")),
        "closure_package_queue_ids": list(
            latest_history.get("closure_package_queue_ids")
            or base_plan.get("closure_package_queue_ids")
            or []
        ),
        "active_closure_package_id": latest_history.get("active_closure_package_id", base_plan.get("active_closure_package_id")),
        "active_closure_package_action": latest_history.get("active_closure_package_action", base_plan.get("active_closure_package_action")),
        "active_closure_package_target_stage": latest_history.get(
            "active_closure_package_target_stage",
            base_plan.get("active_closure_package_target_stage"),
        ),
        "decision_reason": _normalized_string(latest_history.get("decision_reason"))
        or termination_reason
        or "controller_not_started",
        "termination_reason": termination_reason or "controller_not_started",
    }
    next_action = "stop_success" if controller_status != "failed_closed" else "fail_closed"
    base_plan["next_controller_action"] = next_action
    base_plan["decision_basis"] = decision_basis
    return base_plan

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

__all__ = [name for name in globals() if name.startswith("_") and not name.startswith("__")]
