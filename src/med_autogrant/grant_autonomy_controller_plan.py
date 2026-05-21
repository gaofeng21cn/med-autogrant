from __future__ import annotations

from copy import deepcopy
from typing import Any

from med_autogrant.grant_autonomy_common import (
    _CONTROLLER_ACTIONS,
    _GATE_STATUSES,
    _QUALITY_STATUSES,
    _normalized_string,
    _string_list,
)


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
