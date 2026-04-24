from __future__ import annotations

import hashlib
from typing import Any, Iterable, Mapping

from med_autogrant.grant_quality_closure import *  # noqa: F401,F403
from med_autogrant import grant_quality_assessment as _grant_quality_assessment
from med_autogrant import grant_quality_closure as _grant_quality_closure
from med_autogrant.grant_quality_assessment import *  # noqa: F401,F403
from med_autogrant.grant_quality_parts import *  # noqa: F401,F403

from med_autogrant.workspace import (
    WorkspaceStateError,
    _build_workspace_state,
    build_critique_summary,
    build_grant_evidence_grounding,
    build_grant_intake_audit,
)


REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}
_QUALITY_CONTROLLER_ACTIONS = {
    "continue_mainline",
    "rollback_upstream",
    "reselect_project_profile",
    "fail_closed",
}

_QUALITY_DIMENSION_SPECS: tuple[dict[str, str], ...] = (
    {
        "dimension_id": "scientific_question_validity",
        "label": "科学问题成立性",
        "rollback_stage": "question_refinement",
    },
    {
        "dimension_id": "necessity_value_closure",
        "label": "必要性与科学价值闭合度",
        "rollback_stage": "argument_building",
    },
    {
        "dimension_id": "applicant_fit",
        "label": "申请人适配度",
        "rollback_stage": "fit_alignment",
    },
    {
        "dimension_id": "technical_feasibility",
        "label": "技术路线可行性",
        "rollback_stage": "fit_alignment",
    },
    {
        "dimension_id": "claim_evidence_coverage",
        "label": "claim-evidence coverage",
        "rollback_stage": "argument_building",
    },
    {
        "dimension_id": "unresolved_hard_issues",
        "label": "未关闭硬伤",
        "rollback_stage": "revision",
    },
    {
        "dimension_id": "version_issue_closure",
        "label": "版本间问题关闭情况",
        "rollback_stage": "revision",
    },
)
_grant_quality_assessment._QUALITY_DIMENSION_SPECS = _QUALITY_DIMENSION_SPECS



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
    overall_status = _resolve_overall_status(
        overall_score=overall_score,
        lifecycle_stage=lifecycle_stage,
        blocked_dimensions=blocked_dimensions,
        unresolved_hard_issues=unresolved_hard_issues,
    )
    loop_gate = _build_loop_gate(
        lifecycle_stage=lifecycle_stage,
        overall_status=overall_status,
        overall_score=overall_score,
        blocked_dimensions=blocked_dimensions,
        unresolved_hard_issues=unresolved_hard_issues,
    )

    summary = _build_scorecard_summary(
        overall_status=overall_status,
        overall_score=overall_score,
        blocked_dimensions=blocked_dimensions,
        unresolved_hard_issues=unresolved_hard_issues,
    )

    return {
        "surface_kind": "grant_quality_scorecard",
        "scorecard_version": 1,
        "workspace_surface_kind": "nsfc_workspace",
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "lifecycle_stage": lifecycle_stage,
        "draft_id": _read_active_draft_id(document),
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




























































def _build_issue(
    *,
    dimension_id: str,
    summary: str,
    severity: str,
    source_surface: str,
    rollback_stage: str | None,
    evidence_refs: list[str],
    context: dict[str, Any],
) -> dict[str, Any]:
    normalized = " ".join(summary.split()).strip().lower()
    digest = hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:12]
    closure_status = "blocked" if severity == "hard" else "evidence_required"
    recommended_closure_action = _build_recommended_closure_action(
        dimension_id=dimension_id,
        summary=summary,
        severity=severity,
        rollback_stage=rollback_stage,
        context=context,
    )
    evidence_obligations = _build_issue_evidence_obligations(
        dimension_id=dimension_id,
        summary=summary,
        severity=severity,
        evidence_refs=evidence_refs,
        context=context,
    )
    lineage_basis = _build_issue_lineage_basis(
        dimension_id=dimension_id,
        summary=summary,
        severity=severity,
        recommended_closure_action=recommended_closure_action,
        evidence_obligations=evidence_obligations,
    )
    return {
        "issue_id": f"{dimension_id}:{digest}",
        "lineage_id": _build_issue_lineage_id(lineage_basis),
        "lineage_basis": lineage_basis,
        "dimension_id": dimension_id,
        "summary": summary,
        "status": "open",
        "severity": severity,
        "source_surface": source_surface,
        "rollback_stage": rollback_stage,
        "closure_status": closure_status,
        "blocking_reason": summary if severity == "hard" else None,
        "evidence_obligations": evidence_obligations,
        "recommended_closure_action": recommended_closure_action,
    }


def _build_recommended_closure_action(
    *,
    dimension_id: str,
    summary: str,
    severity: str,
    rollback_stage: str | None,
    context: dict[str, Any],
) -> dict[str, Any]:
    repair_summaries = _dimension_repair_summaries(dimension_id, context=context)
    revision_items = _relevant_revision_items(dimension_id, context=context)
    revision_plan = _active_revision_plan(context)

    action_summary = summary
    source_surface = dimension_id
    if repair_summaries:
        action_summary = repair_summaries[0]
        source_surface = "critique_summary"
    elif revision_items:
        action_summary = _nonempty_string(revision_items[0].get("action")) or summary
        source_surface = "revision_plan"
    elif dimension_id == "version_issue_closure" and revision_plan is not None:
        next_focus = _read_nonempty_string_list(revision_plan.get("next_review_focus"))
        if next_focus:
            action_summary = next_focus[0]
            source_surface = "revision_plan"

    target_stage = rollback_stage or _nonempty_string(context["document"].get("lifecycle_stage"))
    if severity == "gap" and target_stage is None:
        target_stage = "revision"
    return {
        "action": _resolve_issue_controller_action(severity=severity, target_stage=target_stage),
        "summary": action_summary,
        "target_stage": target_stage,
        "source_surface": source_surface,
    }


def _resolve_issue_controller_action(*, severity: str, target_stage: str | None) -> str:
    if severity == "hard":
        return "rollback_upstream"
    if target_stage is None:
        return "continue_mainline"
    return "continue_mainline"


def _build_issue_evidence_obligations(
    *,
    dimension_id: str,
    summary: str,
    severity: str,
    evidence_refs: list[str],
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    obligations: list[dict[str, Any]] = []
    revision_items = _relevant_revision_items(dimension_id, context=context)
    for item in revision_items:
        item_id = _nonempty_string(item.get("item_id")) or f"{dimension_id}-revision-item"
        action_summary = _nonempty_string(item.get("action")) or summary
        obligations.append(
            {
                "obligation_id": f"{dimension_id}:{item_id}",
                "summary": action_summary,
                "required_input_ids": _read_nonempty_string_list(item.get("required_input_ids")),
                "evidence_refs": list(evidence_refs),
                "satisfaction_criteria": _nonempty_string(item.get("done_criteria")),
                "source_surface": "revision_plan",
            }
        )

    if obligations:
        return obligations

    repair_summaries = _dimension_repair_summaries(dimension_id, context=context)
    if repair_summaries:
        return [
            {
                "obligation_id": f"{dimension_id}:repair:{_stable_digest(repair_summaries[0])}",
                "summary": repair_summaries[0],
                "required_input_ids": _default_obligation_input_ids(dimension_id, context=context),
                "evidence_refs": list(evidence_refs),
                "satisfaction_criteria": None,
                "source_surface": "critique_summary",
            }
        ]

    return [
        {
            "obligation_id": f"{dimension_id}:issue:{_stable_digest(summary)}",
            "summary": summary,
            "required_input_ids": _default_obligation_input_ids(dimension_id, context=context),
            "evidence_refs": list(evidence_refs),
            "satisfaction_criteria": None,
            "source_surface": dimension_id if severity == "hard" else "evidence_grounding",
        }
    ]


def _build_issue_lineage_basis(
    *,
    dimension_id: str,
    summary: str,
    severity: str,
    recommended_closure_action: dict[str, Any],
    evidence_obligations: list[dict[str, Any]],
) -> dict[str, Any]:
    obligation_ids = [
        obligation_id
        for item in evidence_obligations
        if isinstance(item, dict)
        for obligation_id in [_nonempty_string(item.get("obligation_id"))]
        if obligation_id is not None
    ]
    required_input_ids = _dedupe_preserve_order(
        input_id
        for item in evidence_obligations
        if isinstance(item, dict)
        for input_id in _read_nonempty_string_list(item.get("required_input_ids"))
    )
    target_stage = _nonempty_string(recommended_closure_action.get("target_stage"))
    source_surface = _nonempty_string(recommended_closure_action.get("source_surface")) or dimension_id
    action_summary = _nonempty_string(recommended_closure_action.get("summary"))

    if obligation_ids:
        anchor_ref = obligation_ids[0]
        if ":rev-item-" in anchor_ref:
            anchor_kind = "revision_item"
        elif ":repair:" in anchor_ref:
            anchor_kind = "critique_repair"
        else:
            anchor_kind = "required_input_set"
            anchor_ref = _required_input_anchor_ref(dimension_id=dimension_id, required_input_ids=required_input_ids)
    elif required_input_ids:
        anchor_kind = "required_input_set"
        anchor_ref = _required_input_anchor_ref(dimension_id=dimension_id, required_input_ids=required_input_ids)
    elif action_summary is not None:
        anchor_kind = "closure_action"
        anchor_ref = (
            f"{dimension_id}:action:{_stable_digest('|'.join([source_surface, target_stage or '', action_summary, severity]))}"
        )
    else:
        anchor_kind = "summary_fallback"
        anchor_ref = f"{dimension_id}:summary:{_stable_digest(summary)}"

    return {
        "anchor_kind": anchor_kind,
        "anchor_ref": anchor_ref,
        "source_surface": source_surface,
        "target_stage": target_stage,
        "required_input_ids": required_input_ids,
    }


def _build_issue_lineage_id(lineage_basis: dict[str, Any]) -> str:
    return f"{lineage_basis['anchor_kind']}:{lineage_basis['anchor_ref']}"


def _required_input_anchor_ref(*, dimension_id: str, required_input_ids: list[str]) -> str:
    normalized_inputs = "|".join(required_input_ids)
    return f"{dimension_id}:inputs:{_stable_digest(normalized_inputs)}"


def _relevant_revision_items(dimension_id: str, *, context: dict[str, Any]) -> list[dict[str, Any]]:
    revision_plan = _active_revision_plan(context)
    if revision_plan is None:
        return []

    items = [
        item
        for item in revision_plan.get("items") or []
        if isinstance(item, dict)
    ]
    if dimension_id in {"scientific_question_validity", "necessity_value_closure"}:
        return [
            item
            for item in items
            if _nonempty_string(item.get("action_type")) == "rebuild_argument"
            or _nonempty_string(item.get("target_ref")) == "section:basis"
        ]
    if dimension_id == "applicant_fit":
        return [
            item
            for item in items
            if _nonempty_string(item.get("action_type")) == "tighten_fit"
            or _nonempty_string(item.get("target_ref")) == "section:foundation"
        ]
    if dimension_id in {"unresolved_hard_issues", "version_issue_closure"}:
        high_priority_items = [
            item
            for item in items
            if _nonempty_string(item.get("priority")) == "p0"
        ]
        return high_priority_items or items
    return []


def _dimension_repair_summaries(dimension_id: str, *, context: dict[str, Any]) -> list[str]:
    critique_summary = context["critique_summary"]
    if critique_summary is None:
        return []
    if dimension_id in {"scientific_question_validity", "necessity_value_closure"}:
        return _read_nonempty_string_list(critique_summary.get("logic_chain_repairs"))
    if dimension_id == "applicant_fit":
        return _read_nonempty_string_list(critique_summary.get("applicant_fit_repairs"))
    return []


def _default_obligation_input_ids(dimension_id: str, *, context: dict[str, Any]) -> list[str]:
    state = context["state"]
    if dimension_id == "scientific_question_validity":
        return _dedupe_preserve_order(
            _read_object_id(state.selected_question, "question_id")
            + _read_object_id(state.selected_direction, "direction_id")
        )
    if dimension_id == "necessity_value_closure":
        return _dedupe_preserve_order(
            _read_object_id(state.active_argument_chain, "argument_chain_id")
            + _read_object_id(state.selected_question, "question_id")
        )
    if dimension_id in {"applicant_fit", "technical_feasibility"}:
        return _dedupe_preserve_order(
            _read_object_id(state.active_fit_mapping, "fit_mapping_id")
            + _read_object_id(state.active_draft, "draft_id")
        )
    if dimension_id == "claim_evidence_coverage":
        return _dedupe_preserve_order(
            _read_object_id(state.active_draft, "draft_id")
            + _read_object_id(state.selected_question, "question_id")
            + _read_object_id(state.active_argument_chain, "argument_chain_id")
            + _read_object_id(state.active_fit_mapping, "fit_mapping_id")
        )
    if dimension_id in {"unresolved_hard_issues", "version_issue_closure"}:
        return _dedupe_preserve_order(
            _read_object_id(state.active_revision_plan, "revision_plan_id")
            + _read_object_id(state.active_draft, "draft_id")
        )
    return []


def _read_object_id(payload: dict[str, Any] | None, key: str) -> list[str]:
    if not isinstance(payload, dict):
        return []
    value = _nonempty_string(payload.get(key))
    return [value] if value is not None else []


def _active_revision_plan(context: dict[str, Any]) -> dict[str, Any] | None:
    revision_plan = context["state"].active_revision_plan
    return revision_plan if isinstance(revision_plan, dict) else None


def _stable_digest(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]
















































for _name in (
    "_build_issue",
    "_build_issue_evidence_obligations",
    "_build_issue_lineage_basis",
    "_build_recommended_closure_action",
    "_default_obligation_input_ids",
    "_dimension_repair_summaries",
    "_relevant_revision_items",
    "_resolve_issue_controller_action",
    "_stable_digest",
):
    setattr(_grant_quality_assessment, _name, globals()[_name])
    setattr(_grant_quality_closure, _name, globals()[_name])
