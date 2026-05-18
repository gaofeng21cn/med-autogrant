from __future__ import annotations

from typing import Any

from med_autogrant.grant_quality import (
    build_grant_quality_closure_dossier,
    build_grant_quality_scorecard,
)
from med_autogrant.stage_router import _build_forced_rollback_actions


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
