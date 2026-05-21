from __future__ import annotations

from copy import deepcopy
from typing import Any

from med_autogrant.grant_autonomy_common import (
    _CONTROLLER_ACTIONS,
    _QUALITY_STATUSES,
    _normalized_string,
    _string_list,
)


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
        "assessment_owner": _normalized_string(payload.get("assessment_owner")) or None,
        "ai_reviewer_required": (
            payload.get("ai_reviewer_required")
            if isinstance(payload.get("ai_reviewer_required"), bool)
            else None
        ),
        "review_artifact_ref": _normalized_string(payload.get("review_artifact_ref")) or None,
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
