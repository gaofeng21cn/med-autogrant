from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.ai_first_boundaries import active_critique_ai_review_provenance
from med_autogrant.grant_quality_assessment import (
    _QUALITY_DIMENSION_SPECS,
    _build_dimension_assessment,
    _build_loop_gate,
    _build_scorecard_summary,
    _resolve_overall_status,
    _resolve_quality_progression,
)
from med_autogrant.grant_quality_closure import _build_quality_closure_packages
from med_autogrant.grant_quality_parts import (
    _build_evidence_supply_progress,
    _build_evidence_supply_queue,
    _build_funding_profile_mismatch_gap,
    _build_issue_closure_progress_entries,
    _dedupe_preserve_order,
    _ensure_mapping,
    _nonempty_string,
    _open_issue_lineage_map,
    _read_active_draft_id,
    _read_critique_summary,
    _read_nonempty_string_list,
)

from med_autogrant.workspace import (
    build_critique_summary,
    build_grant_evidence_grounding,
    build_grant_intake_audit,
)
from med_autogrant.workspace_projection_parts import _build_workspace_state
from med_autogrant.workspace_types import WorkspaceStateError


def build_grant_quality_scorecard(document: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise TypeError("quality scorecard 输入必须是 workspace object。")

    state = _build_workspace_state(document)
    intake_audit = _ensure_mapping(document.get("grant_intake_audit")) or build_grant_intake_audit(document)
    evidence_grounding = (
        _ensure_mapping(document.get("grant_evidence_grounding")) or build_grant_evidence_grounding(document)
    )
    critique_summary = _read_critique_summary(document)

    dimension_context = {
        "document": document,
        "state": state,
        "intake_audit": intake_audit,
        "evidence_grounding": evidence_grounding,
        "critique_summary": critique_summary,
    }
    dimensions = [
        _build_dimension_assessment(spec["dimension_id"], context=dimension_context)
        for spec in _QUALITY_DIMENSION_SPECS
    ]
    tracked_issues = [
        issue
        for dimension in dimensions
        for issue in dimension["tracked_issues"]
    ]
    evidence_supply_queue = _build_evidence_supply_queue(tracked_issues)
    funding_profile_mismatch_gap = _build_funding_profile_mismatch_gap(document)
    if funding_profile_mismatch_gap is not None:
        evidence_supply_queue.append(funding_profile_mismatch_gap)
    unresolved_hard_issues = [
        issue["summary"]
        for issue in tracked_issues
        if issue["status"] == "open" and issue["severity"] == "hard"
    ]
    unresolved_hard_issues = _dedupe_preserve_order(unresolved_hard_issues)

    overall_score = round(sum(int(item["score"]) for item in dimensions) / len(dimensions))
    blocked_dimensions = [item for item in dimensions if item["status"] == "blocked"]
    lifecycle_stage = _nonempty_string(document.get("lifecycle_stage")) or "unknown"
    assessment_provenance = active_critique_ai_review_provenance(document)
    overall_status = _resolve_overall_status(
        overall_score=overall_score,
        lifecycle_stage=lifecycle_stage,
        blocked_dimensions=blocked_dimensions,
        unresolved_hard_issues=unresolved_hard_issues,
        ai_reviewer_required=bool(assessment_provenance["ai_reviewer_required"]),
    )
    loop_gate = _build_loop_gate(
        lifecycle_stage=lifecycle_stage,
        overall_status=overall_status,
        overall_score=overall_score,
        blocked_dimensions=blocked_dimensions,
        unresolved_hard_issues=unresolved_hard_issues,
        ai_reviewer_required=bool(assessment_provenance["ai_reviewer_required"]),
    )

    summary = _build_scorecard_summary(
        overall_status=overall_status,
        overall_score=overall_score,
        blocked_dimensions=blocked_dimensions,
        unresolved_hard_issues=unresolved_hard_issues,
        ai_reviewer_required=bool(assessment_provenance["ai_reviewer_required"]),
    )

    return {
        "surface_kind": "grant_quality_scorecard",
        "scorecard_version": 1,
        "workspace_surface_kind": "nsfc_workspace",
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "lifecycle_stage": lifecycle_stage,
        "draft_id": _read_active_draft_id(document),
        "assessment_owner": assessment_provenance["assessment_owner"],
        "ai_reviewer_required": assessment_provenance["ai_reviewer_required"],
        "review_artifact_ref": assessment_provenance["review_artifact_ref"],
        "independent_review_evidence": assessment_provenance["independent_review_evidence"],
        "ai_reviewer_blocker_reason": assessment_provenance["ai_reviewer_blocker_reason"],
        "overall_status": overall_status,
        "overall_score": overall_score,
        "summary": summary,
        "dimensions": [
            {
                key: value
                for key, value in item.items()
                if key != "tracked_issues"
            }
            for item in dimensions
        ],
        "unresolved_hard_issues": unresolved_hard_issues,
        "tracked_issues": tracked_issues,
        "evidence_supply_queue": evidence_supply_queue,
        "loop_gate": loop_gate,
    }


def build_grant_quality_closure_dossier(document: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise TypeError("quality closure dossier 输入必须是 workspace object。")

    scorecard = build_grant_quality_scorecard(document)
    evidence_supply_queue = [
        dict(item)
        for item in scorecard["evidence_supply_queue"]
        if isinstance(item, Mapping)
    ]
    tracked_issues = [
        dict(item)
        for item in scorecard["tracked_issues"]
        if isinstance(item, Mapping)
    ]
    return {
        "surface_kind": "grant_quality_closure_dossier",
        "dossier_version": 1,
        "workspace_surface_kind": scorecard["workspace_surface_kind"],
        "grant_run_id": scorecard["grant_run_id"],
        "workspace_id": scorecard["workspace_id"],
        "lifecycle_stage": scorecard["lifecycle_stage"],
        "draft_id": scorecard["draft_id"],
        "quality_summary": {
            "overall_status": scorecard["overall_status"],
            "overall_score": scorecard["overall_score"],
            "summary": scorecard["summary"],
            "loop_gate": scorecard["loop_gate"],
            "assessment_owner": scorecard["assessment_owner"],
            "ai_reviewer_required": scorecard["ai_reviewer_required"],
            "review_artifact_ref": scorecard["review_artifact_ref"],
            "independent_review_evidence": scorecard["independent_review_evidence"],
            "ai_reviewer_blocker_reason": scorecard["ai_reviewer_blocker_reason"],
        },
        "unclosed_hard_issues": list(scorecard["unresolved_hard_issues"]),
        "evidence_supply_queue_summary": _build_evidence_supply_queue_summary(evidence_supply_queue),
        "closure_packages": _build_quality_closure_packages(
            tracked_issues=tracked_issues,
            evidence_supply_queue=evidence_supply_queue,
        ),
    }


def build_grant_quality_diff(
    *,
    current_document: dict[str, Any],
    previous_document: dict[str, Any],
) -> dict[str, Any]:
    current_scorecard = build_grant_quality_scorecard(current_document)
    previous_scorecard = build_grant_quality_scorecard(previous_document)

    current_open_issues = _open_issue_lineage_map(current_scorecard["tracked_issues"])
    previous_open_issues = _open_issue_lineage_map(previous_scorecard["tracked_issues"])

    closed_issue_ids = [issue_id for issue_id in previous_open_issues if issue_id not in current_open_issues]
    remaining_issue_ids = [issue_id for issue_id in previous_open_issues if issue_id in current_open_issues]
    new_issue_ids = [issue_id for issue_id in current_open_issues if issue_id not in previous_open_issues]
    issue_closure_progress = _build_issue_closure_progress_entries(
        previous_open_issues=previous_open_issues,
        current_open_issues=current_open_issues,
    )
    evidence_supply_progress = _build_evidence_supply_progress(
        previous_queue=previous_scorecard["evidence_supply_queue"],
        current_queue=current_scorecard["evidence_supply_queue"],
    )

    score_delta = current_scorecard["overall_score"] - previous_scorecard["overall_score"]
    overall_progression = _resolve_quality_progression(
        score_delta=score_delta,
        closed_issue_ids=closed_issue_ids,
        remaining_issue_ids=remaining_issue_ids,
        new_issue_ids=new_issue_ids,
    )

    current_dimensions = {
        item["dimension_id"]: item
        for item in current_scorecard["dimensions"]
    }
    previous_dimensions = {
        item["dimension_id"]: item
        for item in previous_scorecard["dimensions"]
    }

    return {
        "surface_kind": "grant_quality_diff",
        "diff_version": 1,
        "workspace_surface_kind": "nsfc_workspace",
        "current_workspace_id": current_scorecard["workspace_id"],
        "previous_workspace_id": previous_scorecard["workspace_id"],
        "current_lifecycle_stage": current_scorecard["lifecycle_stage"],
        "previous_lifecycle_stage": previous_scorecard["lifecycle_stage"],
        "current_overall_status": current_scorecard["overall_status"],
        "previous_overall_status": previous_scorecard["overall_status"],
        "current_overall_score": current_scorecard["overall_score"],
        "previous_overall_score": previous_scorecard["overall_score"],
        "score_delta": score_delta,
        "overall_progression": overall_progression,
        "dimension_deltas": [
            {
                "dimension_id": spec["dimension_id"],
                "label": spec["label"],
                "current_score": current_dimensions[spec["dimension_id"]]["score"],
                "previous_score": previous_dimensions[spec["dimension_id"]]["score"],
                "score_delta": (
                    current_dimensions[spec["dimension_id"]]["score"]
                    - previous_dimensions[spec["dimension_id"]]["score"]
                ),
                "current_status": current_dimensions[spec["dimension_id"]]["status"],
                "previous_status": previous_dimensions[spec["dimension_id"]]["status"],
            }
            for spec in _QUALITY_DIMENSION_SPECS
        ],
        "issue_progress": {
            "closed_issues": [previous_open_issues[issue_id]["summary"] for issue_id in closed_issue_ids],
            "remaining_open_issues": [current_open_issues[issue_id]["summary"] for issue_id in remaining_issue_ids],
            "newly_opened_issues": [current_open_issues[issue_id]["summary"] for issue_id in new_issue_ids],
            "issue_closure_progress": issue_closure_progress,
        },
        "evidence_supply_progress": evidence_supply_progress,
        "current_loop_gate": current_scorecard["loop_gate"],
        "previous_loop_gate": previous_scorecard["loop_gate"],
    }


def _build_evidence_supply_queue_summary(
    evidence_supply_queue: list[dict[str, Any]],
) -> dict[str, Any]:
    outstanding_gap_ids = [
        gap_id
        for item in evidence_supply_queue
        for gap_id in [_nonempty_string(item.get("gap_id"))]
        if gap_id is not None
    ]
    return {
        "total_gap_count": len(outstanding_gap_ids),
        "outstanding_gap_ids": outstanding_gap_ids,
        "status_counts": _build_supply_status_counts(evidence_supply_queue),
        "kind_counts": _build_supply_kind_counts(evidence_supply_queue),
    }


def _build_supply_status_counts(evidence_supply_queue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped_gap_ids: dict[str, list[str]] = {}
    ordered_statuses: list[str] = []
    for item in evidence_supply_queue:
        status = _nonempty_string(item.get("supply_status"))
        gap_id = _nonempty_string(item.get("gap_id"))
        if status is None or gap_id is None:
            continue
        if status not in grouped_gap_ids:
            grouped_gap_ids[status] = []
            ordered_statuses.append(status)
        grouped_gap_ids[status].append(gap_id)
    return [
        {
            "supply_status": status,
            "count": len(grouped_gap_ids[status]),
            "gap_ids": grouped_gap_ids[status],
        }
        for status in ordered_statuses
    ]


def _build_supply_kind_counts(evidence_supply_queue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped_gap_ids: dict[str, list[str]] = {}
    ordered_kinds: list[str] = []
    for item in evidence_supply_queue:
        gap_kind = _nonempty_string(item.get("gap_kind"))
        gap_id = _nonempty_string(item.get("gap_id"))
        if gap_kind is None or gap_id is None:
            continue
        if gap_kind not in grouped_gap_ids:
            grouped_gap_ids[gap_kind] = []
            ordered_kinds.append(gap_kind)
        grouped_gap_ids[gap_kind].append(gap_id)
    return [
        {
            "gap_kind": gap_kind,
            "count": len(grouped_gap_ids[gap_kind]),
            "gap_ids": grouped_gap_ids[gap_kind],
        }
        for gap_kind in ordered_kinds
    ]
