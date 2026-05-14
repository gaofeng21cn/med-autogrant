from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from med_autogrant.control_plane import resolve_runtime_state_root
from med_autogrant.grant_quality import (
    build_grant_quality_closure_dossier,
    build_grant_quality_scorecard,
)
from med_autogrant.domain_runtime_parts.contracts import (
    build_executor_routing_contract as _build_executor_routing_contract,
    validate_executor_routing_contract as _validate_executor_routing_contract,
)
from med_autogrant.stage_router import _build_forced_rollback_actions

from .shared import LocalRuntimeStateError


def build_validation_failed_route_report(
    *,
    document: dict[str, Any],
    validation: Any,
) -> dict[str, Any]:
    lifecycle_stage = document.get("lifecycle_stage")
    validation_payload = validation.to_dict(document)
    reason = validation.errors[0].message if validation.errors else "workspace validation failed"
    checkpoint_status = None
    return {
        "ok": False,
        "grant_run_id": document.get("grant_run_id"),
        "workspace_id": document.get("workspace_id"),
        "lifecycle_stage": lifecycle_stage,
        "route": {
            "validate_workspace": validation_payload,
            "summarize_workspace": None,
            "next_step": {
                "grant_run_id": document.get("grant_run_id"),
                "workspace_id": document.get("workspace_id"),
                "presubmission_frozen": bool(document.get("gates", {}).get("presubmission_frozen")),
                "current_stage": lifecycle_stage,
                "recommended_stage": lifecycle_stage,
                "reason": reason,
                "actions": [],
                "requires_human_confirmation": False,
            },
            "critique_summary": None,
        },
        "checkpoint_status": checkpoint_status,
        "verification_checkpoint": {
            "checkpoint_status": checkpoint_status,
            "validation_ok": False,
            "identity": {
                "grant_run_id": document.get("grant_run_id"),
                "workspace_id": document.get("workspace_id"),
                "draft_id": None,
                "active_revision_plan_id": None,
                "reviewed_revision_plan_id": None,
            },
            "route_alignment": {
                "lifecycle_stage": lifecycle_stage,
                "recommended_next_stage": lifecycle_stage,
                "forced_rollback_stage": None,
                "forced_rollback_reason": None,
                "presubmission_frozen": bool(document.get("gates", {}).get("presubmission_frozen")),
            },
            "review_checkpoint": {
                "critique_id": None,
                "reviewed_revision_evidence": None,
                "blocking_issue_count": None,
            },
        },
    }


def derive_stop_reason(route_report: dict[str, Any]) -> dict[str, Any]:
    next_step = route_report["route"]["next_step"]
    checkpoint = route_report["verification_checkpoint"]
    checkpoint_status = checkpoint["checkpoint_status"]
    route_alignment = checkpoint["route_alignment"]
    forced_rollback_stage = route_alignment.get("forced_rollback_stage")
    forced_rollback_reason = route_alignment.get("forced_rollback_reason")
    requires_human_confirmation = bool(next_step.get("requires_human_confirmation"))

    if checkpoint_status == "submission_frozen":
        code = "presubmission_frozen"
    elif forced_rollback_stage or checkpoint_status == "rollback_required":
        code = "rollback_required"
    elif checkpoint_status == "freeze_ready":
        code = "freeze_ready"
    elif requires_human_confirmation:
        code = "human_confirmation_required"
    else:
        code = "stage_action_required"

    return {
        "code": code,
        "reason": next_step["reason"],
        "current_stage": next_step["current_stage"],
        "recommended_next_stage": next_step["recommended_stage"],
        "checkpoint_status": checkpoint_status,
        "requires_human_confirmation": requires_human_confirmation,
        "forced_rollback_stage": forced_rollback_stage,
        "forced_rollback_reason": forced_rollback_reason,
    }


def derive_stage_action_envelope(
    *,
    route_report: dict[str, Any],
    stop_reason: dict[str, Any],
    journal_path: Path,
) -> dict[str, Any] | None:
    if stop_reason.get("code") != "stage_action_required":
        return None

    summary = route_report["route"]["summarize_workspace"]
    next_step = route_report["route"]["next_step"]
    checkpoint = route_report["verification_checkpoint"]
    selection = summary.get("current_selection") or {}
    actions = next_step.get("actions") or []
    executor_routing_contract = _build_executor_routing_contract(
        current_stage=next_step["current_stage"],
        recommended_next_stage=next_step["recommended_stage"],
    )
    _validate_executor_routing_contract(
        executor_routing_contract,
        current_stage=next_step["current_stage"],
        recommended_next_stage=next_step["recommended_stage"],
        include_route_catalog=False,
        grant_run_id=route_report["grant_run_id"],
        workspace_id=route_report["workspace_id"],
        lifecycle_stage=next_step["current_stage"],
    )

    return {
        "envelope_version": 1,
        "status": "action_required",
        "grant_run_id": route_report["grant_run_id"],
        "workspace_id": route_report["workspace_id"],
        "draft_id": checkpoint["identity"]["draft_id"],
        "current_stage": next_step["current_stage"],
        "recommended_next_stage": next_step["recommended_stage"],
        "checkpoint_status": checkpoint["checkpoint_status"],
        "requires_human_confirmation": bool(next_step.get("requires_human_confirmation")),
        "selection": {
            "selected_direction_id": selection.get("selected_direction_id"),
            "selected_question_id": selection.get("selected_question_id"),
            "active_fit_mapping_id": selection.get("active_fit_mapping_id"),
            "active_draft_id": selection.get("active_draft_id"),
            "active_revision_plan_id": selection.get("active_revision_plan_id"),
        },
        "action_items": [
            {
                "index": index,
                "instruction": instruction,
            }
            for index, instruction in enumerate(actions, start=1)
        ],
        "route_reason": next_step["reason"],
        "executor_routing_contract": executor_routing_contract,
        "resume_decision": {
            "command": "runtime-resume",
            "journal_path": str(journal_path),
            "append_attempt": True,
            "reuse_grant_run_id": True,
        },
    }


def _resolve_journal_path(*, document: dict[str, Any], journal_path: str | Path | None) -> Path:
    if journal_path is not None:
        return Path(journal_path).expanduser().resolve()
    grant_run_id = document.get("grant_run_id")
    if not isinstance(grant_run_id, str) or not grant_run_id:
        raise LocalRuntimeStateError("workspace 缺少 grant_run_id，无法推导默认 journal 路径。")
    return (_default_journal_root() / f"{grant_run_id}.json").resolve()


def _default_journal_root() -> Path:
    return resolve_runtime_state_root() / "sessions"


def _apply_quality_gate_to_route(
    *,
    route: dict[str, Any],
    quality_scorecard: dict[str, Any] | None,
) -> dict[str, Any]:
    resolved_route = dict(route)
    quality_payload = quality_scorecard if isinstance(quality_scorecard, dict) else {}
    quality_gate = quality_payload.get("loop_gate")
    if not isinstance(quality_gate, dict):
        return resolved_route

    resolved_route["quality_gate"] = dict(quality_gate)
    gate_action = str(quality_gate.get("action") or "").strip()
    gate_reason = str(quality_gate.get("reason") or "").strip()
    gate_stage = str(quality_gate.get("recommended_stage") or "").strip()
    route_stage = str(resolved_route.get("recommended_stage") or "").strip()

    if gate_action == "rollback_required" and gate_stage and gate_stage != route_stage:
        resolved_route["recommended_stage"] = gate_stage
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} 质量 gate 要求回退：{gate_reason}".strip()
        resolved_route["actions"] = _build_forced_rollback_actions(gate_stage)
        resolved_route["requires_human_confirmation"] = gate_stage in {
            "direction_screening",
            "question_refinement",
        }
        return resolved_route

    if gate_action == "continue" and route_stage in {"frozen", "ready_for_submission"} and gate_stage:
        resolved_route["recommended_stage"] = gate_stage
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} 质量 gate 暂不允许停止：{gate_reason}".strip()
        return resolved_route

    if gate_action == "ready_for_submission" and gate_reason:
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} {gate_reason}".strip()
    return resolved_route


def _build_autonomy_quality_evaluator_output(workspace: dict[str, Any]) -> dict[str, Any]:
    scorecard = build_grant_quality_scorecard(workspace)
    closure_dossier = build_grant_quality_closure_dossier(workspace)
    overall_status = str(scorecard.get("overall_status") or "")
    ai_reviewer_required = bool(scorecard.get("ai_reviewer_required"))
    quality_status = overall_status if not ai_reviewer_required and overall_status in {
        "submission_grade_candidate",
        "near_submission_candidate",
    } else "not_ready"
    tracked_issues = scorecard.get("tracked_issues") if isinstance(scorecard.get("tracked_issues"), list) else []
    evidence_supply_queue = scorecard.get("evidence_supply_queue") if isinstance(scorecard.get("evidence_supply_queue"), list) else []
    unresolved_blockers = list(scorecard.get("unresolved_hard_issues") or [])
    if ai_reviewer_required:
        unresolved_blockers.append(
            "AI reviewer-backed critique is required before grant quality can be marked near-submission or submission-grade."
        )
    unresolved_blockers.extend(
        str(issue.get("summary") or "")
        for issue in tracked_issues
        if isinstance(issue, dict)
        and issue.get("status") == "open"
        and issue.get("severity") == "hard"
    )
    dimensions = scorecard.get("dimensions") if isinstance(scorecard.get("dimensions"), list) else []
    evidence_gaps: list[str] = []
    for dimension in dimensions:
        if not isinstance(dimension, dict):
            continue
        for gap in dimension.get("evidence_gaps") or []:
            if isinstance(gap, str) and gap.strip():
                evidence_gaps.append(gap.strip())
    for item in evidence_supply_queue:
        if not isinstance(item, dict):
            continue
        gap_summary = str(item.get("gap_summary") or "").strip()
        supply_status = str(item.get("supply_status") or "").strip()
        if not gap_summary:
            continue
        if supply_status in {"blocked", "reselection_required"}:
            unresolved_blockers.append(gap_summary)
        else:
            evidence_gaps.append(gap_summary)

    return {
        "quality_status": quality_status,
        "blocker_report": scorecard,
        "unresolved_blockers": _dedupe_strings(unresolved_blockers),
        "evidence_gaps": _dedupe_strings(evidence_gaps),
        "evidence_supply_queue": evidence_supply_queue,
        "quality_closure_dossier": closure_dossier,
    }


build_autonomy_quality_evaluator_output = _build_autonomy_quality_evaluator_output


def _dedupe_strings(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        deduped.append(text)
    return deduped


def _looks_like_workspace(payload: dict[str, Any]) -> bool:
    return all(isinstance(payload.get(field), str) and payload[field] for field in (
        "grant_run_id",
        "workspace_id",
        "lifecycle_stage",
    ))
