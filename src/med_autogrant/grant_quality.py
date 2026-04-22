from __future__ import annotations

import hashlib
from typing import Any, Iterable, Mapping

from med_autogrant.workspace import (
    WorkspaceStateError,
    _build_workspace_state,
    build_critique_summary,
    build_grant_evidence_grounding,
    build_grant_intake_audit,
)


REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}

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


def _build_dimension_assessment(dimension_id: str, *, context: dict[str, Any]) -> dict[str, Any]:
    if dimension_id == "scientific_question_validity":
        return _assess_scientific_question_validity(context)
    if dimension_id == "necessity_value_closure":
        return _assess_necessity_value_closure(context)
    if dimension_id == "applicant_fit":
        return _assess_applicant_fit(context)
    if dimension_id == "technical_feasibility":
        return _assess_technical_feasibility(context)
    if dimension_id == "claim_evidence_coverage":
        return _assess_claim_evidence_coverage(context)
    if dimension_id == "unresolved_hard_issues":
        return _assess_unresolved_hard_issues(context)
    if dimension_id == "version_issue_closure":
        return _assess_version_issue_closure(context)
    raise ValueError(f"未知 quality dimension: {dimension_id}")


def _assess_scientific_question_validity(context: dict[str, Any]) -> dict[str, Any]:
    state = context["state"]
    critique_summary = context["critique_summary"]
    selected_question = state.selected_question
    if not isinstance(selected_question, dict):
        return _finalize_dimension(
            dimension_id="scientific_question_validity",
            summary="当前缺少已冻结 scientific question，质量治理无法确认问题成立性。",
            score=0,
            blockers=["缺少已冻结 scientific question。"],
            evidence_gaps=["selected_question 未生成。"],
            context=context,
        )

    required_fields = (
        "core_question",
        "knowledge_boundary",
        "unknown_mechanism",
        "falsifiable_statement",
        "why_not_engineering",
        "why_now",
    )
    missing_fields = [
        field_name
        for field_name in required_fields
        if not _nonempty_string(selected_question.get(field_name))
    ]
    structural_score = round((len(required_fields) - len(missing_fields)) / len(required_fields) * 100)
    linked_evidence_ids = _read_nonempty_string_list(selected_question.get("linked_evidence_ids"))
    if linked_evidence_ids:
        structural_score = min(100, structural_score + 10)

    blockers: list[str] = []
    evidence_gaps: list[str] = []
    if missing_fields:
        evidence_gaps.append(f"scientific question 缺少字段: {', '.join(missing_fields)}")

    if critique_summary is not None:
        forced_rollback_stage = critique_summary.get("forced_rollback_stage")
        verdict = critique_summary.get("verdict")
        if forced_rollback_stage in {"direction_screening", "question_refinement"}:
            blockers.append(str(critique_summary.get("forced_rollback_reason") or critique_summary["overall_diagnosis"]))
        elif verdict == "major_reframe":
            blockers.append(str(critique_summary["overall_diagnosis"]))

    if not linked_evidence_ids:
        evidence_gaps.append("scientific question 尚未绑定直接证据。")

    summary = "科学问题已具备知识边界、未知机制与可证伪表述。" if not blockers else "科学问题仍存在会触发上游回退的硬伤。"
    return _finalize_dimension(
        dimension_id="scientific_question_validity",
        summary=summary,
        score=structural_score,
        blockers=blockers,
        evidence_gaps=evidence_gaps,
        evidence_refs=linked_evidence_ids,
        context=context,
    )


def _assess_necessity_value_closure(context: dict[str, Any]) -> dict[str, Any]:
    state = context["state"]
    critique_summary = context["critique_summary"]
    evidence_grounding = context["evidence_grounding"]
    argument_chain = state.active_argument_chain
    if not isinstance(argument_chain, dict):
        return _finalize_dimension(
            dimension_id="necessity_value_closure",
            summary="当前缺少 argument chain，无法判断必要性与科学价值是否闭合。",
            score=0,
            blockers=["缺少 argument chain。"],
            evidence_gaps=["argument chain 未生成。"],
            context=context,
        )

    required_fields = (
        "field_gap",
        "necessity_claim",
        "route_justification",
        "non_arbitrary_route_reason",
        "if_not_done_loss",
    )
    missing_fields = [
        field_name
        for field_name in required_fields
        if not _nonempty_string(argument_chain.get(field_name))
    ]
    structural_score = round((len(required_fields) - len(missing_fields)) / len(required_fields) * 100)
    linked_evidence_ids = _read_nonempty_string_list(argument_chain.get("linked_evidence_ids"))
    if linked_evidence_ids:
        structural_score = min(100, structural_score + 8)

    blockers: list[str] = []
    evidence_gaps: list[str] = []
    if critique_summary is not None:
        necessity_payload = critique_summary.get("necessity_scientific_value") or {}
        critique_score = _safe_int(necessity_payload.get("score"))
        if critique_score is not None:
            structural_score = round((structural_score + critique_score) / 2)
        blockers.extend(_read_nonempty_string_list(necessity_payload.get("blocking_issues")))
    if missing_fields:
        evidence_gaps.append(f"necessity chain 缺少字段: {', '.join(missing_fields)}")

    active_argument_evidence = _read_nested_string_list(
        evidence_grounding,
        "selection_evidence_map",
        "active_argument_chain_evidence_ids",
    )
    if not active_argument_evidence:
        evidence_gaps.append("argument chain 尚未绑定直接证据。")

    summary = "必要性链条已把 field gap、机制缺口与路线必要性闭合。" if not blockers else "必要性链条仍有未关闭硬伤。"
    return _finalize_dimension(
        dimension_id="necessity_value_closure",
        summary=summary,
        score=structural_score,
        blockers=blockers,
        evidence_gaps=evidence_gaps,
        evidence_refs=_dedupe_preserve_order(linked_evidence_ids + active_argument_evidence),
        context=context,
    )


def _assess_applicant_fit(context: dict[str, Any]) -> dict[str, Any]:
    state = context["state"]
    critique_summary = context["critique_summary"]
    fit_mapping = state.active_fit_mapping
    if not isinstance(fit_mapping, dict):
        return _finalize_dimension(
            dimension_id="applicant_fit",
            summary="当前缺少 applicant fit mapping，无法确认申请人与问题的适配度。",
            score=0,
            blockers=["缺少 applicant fit mapping。"],
            evidence_gaps=["fit mapping 未生成。"],
            context=context,
        )

    required_fields = (
        "applicant_fit_summary",
        "unique_advantage",
        "methods_readiness",
        "resource_readiness",
    )
    missing_fields = [
        field_name
        for field_name in required_fields
        if not _nonempty_string(fit_mapping.get(field_name))
    ]
    structural_score = round((len(required_fields) - len(missing_fields)) / len(required_fields) * 100)
    linked_evidence_ids = _read_nonempty_string_list(fit_mapping.get("linked_evidence_ids"))
    if linked_evidence_ids:
        structural_score = min(100, structural_score + 10)

    blockers: list[str] = []
    evidence_gaps: list[str] = []
    if critique_summary is not None:
        applicant_fit_payload = critique_summary.get("applicant_fit") or {}
        critique_score = _safe_int(applicant_fit_payload.get("score"))
        if critique_score is not None:
            structural_score = round((structural_score + critique_score) / 2)
        blockers.extend(_read_nonempty_string_list(applicant_fit_payload.get("blocking_issues")))
    if missing_fields:
        evidence_gaps.append(f"applicant fit 缺少字段: {', '.join(missing_fields)}")
    if not linked_evidence_ids:
        evidence_gaps.append("applicant fit mapping 尚未绑定直接证据。")

    summary = "申请人基础、资源与当前问题已形成直接映射。" if not blockers else "申请人与问题的适配度仍不够直接。"
    return _finalize_dimension(
        dimension_id="applicant_fit",
        summary=summary,
        score=structural_score,
        blockers=blockers,
        evidence_gaps=evidence_gaps,
        evidence_refs=linked_evidence_ids,
        context=context,
    )


def _assess_technical_feasibility(context: dict[str, Any]) -> dict[str, Any]:
    state = context["state"]
    critique_summary = context["critique_summary"]
    fit_mapping = state.active_fit_mapping
    if not isinstance(fit_mapping, dict):
        return _finalize_dimension(
            dimension_id="technical_feasibility",
            summary="当前缺少 fit mapping，无法确认技术路线可行性。",
            score=0,
            blockers=["缺少技术路线映射。"],
            evidence_gaps=["fit mapping 未生成。"],
            context=context,
        )

    required_fields = (
        "methods_readiness",
        "resource_readiness",
        "risk_mitigation",
    )
    missing_fields = [
        field_name
        for field_name in required_fields
        if not _nonempty_string(fit_mapping.get(field_name))
    ]
    structural_score = round((len(required_fields) - len(missing_fields)) / len(required_fields) * 100)
    blockers: list[str] = []
    evidence_gaps: list[str] = []
    if critique_summary is not None:
        feasibility_payload = critique_summary.get("feasibility") or {}
        critique_score = _safe_int(feasibility_payload.get("score"))
        if critique_score is not None:
            structural_score = round((structural_score + critique_score) / 2)
        blockers.extend(_read_nonempty_string_list(feasibility_payload.get("blocking_issues")))
    if missing_fields:
        evidence_gaps.append(f"feasibility 缺少字段: {', '.join(missing_fields)}")
    summary = "技术路线已经具备方法、资源与风险缓释描述。" if not blockers else "技术路线仍有未关闭的可行性硬伤。"
    return _finalize_dimension(
        dimension_id="technical_feasibility",
        summary=summary,
        score=structural_score,
        blockers=blockers,
        evidence_gaps=evidence_gaps,
        evidence_refs=_read_nonempty_string_list(fit_mapping.get("linked_evidence_ids")),
        context=context,
    )


def _assess_claim_evidence_coverage(context: dict[str, Any]) -> dict[str, Any]:
    evidence_grounding = context["evidence_grounding"]
    state = context["state"]
    selection_map = _ensure_mapping(evidence_grounding.get("selection_evidence_map")) or {}
    expected_groups = {
        "selected_direction": bool(state.selected_direction),
        "selected_question": bool(state.selected_question),
        "active_argument_chain": bool(state.active_argument_chain),
        "active_fit_mapping": bool(state.active_fit_mapping),
    }
    group_coverage = {
        "selected_direction": bool(_read_nonempty_string_list(selection_map.get("selected_direction_evidence_ids"))),
        "selected_question": bool(_read_nonempty_string_list(selection_map.get("selected_question_evidence_ids"))),
        "active_argument_chain": bool(_read_nonempty_string_list(selection_map.get("active_argument_chain_evidence_ids"))),
        "active_fit_mapping": bool(_read_nonempty_string_list(selection_map.get("active_fit_mapping_evidence_ids"))),
    }
    relevant_group_count = sum(1 for required in expected_groups.values() if required)
    covered_group_count = sum(
        1
        for group_name, required in expected_groups.items()
        if required and group_coverage[group_name]
    )

    draft = state.active_draft
    sections = draft.get("sections") if isinstance(draft, dict) else []
    section_count = len(sections) if isinstance(sections, list) else 0
    traced_section_count = sum(
        1
        for item in sections
        if _read_nonempty_string_list(_ensure_mapping(item).get("linked_object_ids"))
    )
    group_score = 100 if relevant_group_count == 0 else round(covered_group_count / relevant_group_count * 100)
    section_score = 100 if section_count == 0 else round(traced_section_count / section_count * 100)
    score = round((group_score + section_score) / 2)

    evidence_gaps = _read_nonempty_string_list(evidence_grounding.get("evidence_gaps"))
    for group_name, required in expected_groups.items():
        if required and not group_coverage[group_name]:
            evidence_gaps.append(f"{group_name} 尚未形成直接 evidence coverage。")
    if section_count and traced_section_count < section_count:
        evidence_gaps.append("部分草稿章节缺少 linked_object_ids，claim traceability 不完整。")
    blockers = [
        item
        for item in evidence_gaps
        if "尚未形成直接 evidence coverage" in item
    ]

    summary = (
        "关键主张已具备 evidence coverage 与草稿 traceability。"
        if not blockers
        else "关键主张仍存在 evidence coverage 缺口。"
    )
    evidence_refs = _read_nested_string_list(evidence_grounding, "evidence_inventory", "primary_evidence_ids")
    return _finalize_dimension(
        dimension_id="claim_evidence_coverage",
        summary=summary,
        score=score,
        blockers=blockers,
        evidence_gaps=evidence_gaps,
        evidence_refs=evidence_refs,
        context=context,
    )


def _assess_unresolved_hard_issues(context: dict[str, Any]) -> dict[str, Any]:
    intake_audit = context["intake_audit"]
    evidence_grounding = context["evidence_grounding"]
    critique_summary = context["critique_summary"]
    hard_issues = _read_nonempty_string_list(intake_audit.get("blocking_gaps"))
    hard_issues.extend(_read_nonempty_string_list(evidence_grounding.get("evidence_gaps")))
    if critique_summary is not None:
        hard_issues.extend(_read_nonempty_string_list(critique_summary.get("blocking_issues")))
    hard_issues = _dedupe_preserve_order(hard_issues)
    score = max(0, 100 - 20 * len(hard_issues))
    summary = "当前未发现新的 hard blocker。" if not hard_issues else "当前仍有未关闭 hard blocker。"
    return _finalize_dimension(
        dimension_id="unresolved_hard_issues",
        summary=summary,
        score=score,
        blockers=hard_issues,
        evidence_gaps=[],
        context=context,
    )


def _assess_version_issue_closure(context: dict[str, Any]) -> dict[str, Any]:
    state = context["state"]
    revision_plan = state.active_revision_plan
    if not isinstance(revision_plan, dict):
        lifecycle_stage = _nonempty_string(context["document"].get("lifecycle_stage")) or "unknown"
        score = 100 if lifecycle_stage == "frozen" else 80
        return _finalize_dimension(
            dimension_id="version_issue_closure",
            summary="当前没有待执行 revision plan。"
            if lifecycle_stage == "frozen"
            else "当前尚未进入 revision issue closure 追踪面。",
            score=score,
            blockers=[],
            evidence_gaps=[],
            context=context,
        )

    execution_status = _nonempty_string(revision_plan.get("execution_status")) or "planned"
    next_review_focus = _read_nonempty_string_list(revision_plan.get("next_review_focus"))
    items = revision_plan.get("items") or []
    high_priority_items = [
        item
        for item in items
        if _nonempty_string(_ensure_mapping(item).get("priority")) == "p0"
    ]

    blockers: list[str] = []
    if execution_status != "completed":
        blockers.extend(next_review_focus)
        blockers.extend(_read_nonempty_string_list(_ensure_mapping(item).get("action")) for item in high_priority_items)

    blockers = _flatten_to_strings(blockers)
    if execution_status == "completed":
        score = 90 if _nonempty_string(revision_plan.get("comparison_summary")) else 75
    else:
        score = 45 if blockers else 55
    summary = (
        "当前 revision plan 已形成 comparison summary，可追溯版本间问题关闭情况。"
        if execution_status == "completed"
        else "当前 revision plan 仍有待关闭问题。"
    )
    return _finalize_dimension(
        dimension_id="version_issue_closure",
        summary=summary,
        score=score,
        blockers=blockers,
        evidence_gaps=[],
        context=context,
    )


def _finalize_dimension(
    *,
    dimension_id: str,
    summary: str,
    score: int,
    blockers: list[str],
    evidence_gaps: list[str],
    evidence_refs: list[str] | None = None,
    context: dict[str, Any],
) -> dict[str, Any]:
    spec = next(item for item in _QUALITY_DIMENSION_SPECS if item["dimension_id"] == dimension_id)
    resolved_blockers = _dedupe_preserve_order(blockers)
    resolved_gaps = _dedupe_preserve_order(evidence_gaps)
    resolved_refs = _dedupe_preserve_order(evidence_refs or [])
    status = _resolve_dimension_status(
        score=score,
        blockers=resolved_blockers,
        evidence_gaps=resolved_gaps,
    )
    tracked_issues = [
        _build_issue(
            dimension_id=dimension_id,
            summary=item,
            severity="hard",
            source_surface=dimension_id,
            rollback_stage=spec["rollback_stage"],
            evidence_refs=resolved_refs,
            context=context,
        )
        for item in resolved_blockers
    ]
    tracked_issues.extend(
        _build_issue(
            dimension_id=dimension_id,
            summary=item,
            severity="gap",
            source_surface=dimension_id,
            rollback_stage=None,
            evidence_refs=resolved_refs,
            context=context,
        )
        for item in resolved_gaps
        if item not in resolved_blockers
    )
    return {
        "dimension_id": dimension_id,
        "label": spec["label"],
        "status": status,
        "score": max(0, min(int(score), 100)),
        "summary": summary,
        "blocking_issues": resolved_blockers,
        "evidence_gaps": resolved_gaps,
        "evidence_refs": resolved_refs,
        "rollback_stage": spec["rollback_stage"] if resolved_blockers else None,
        "tracked_issues": tracked_issues,
    }


def _resolve_dimension_status(*, score: int, blockers: list[str], evidence_gaps: list[str]) -> str:
    if blockers:
        return "blocked"
    if score < 70:
        return "fragile"
    if evidence_gaps or score < 85:
        return "watch"
    return "strong"


def _resolve_overall_status(
    *,
    overall_score: int,
    lifecycle_stage: str,
    blocked_dimensions: list[dict[str, Any]],
    unresolved_hard_issues: list[str],
) -> str:
    if blocked_dimensions:
        return "blocked"
    if (
        lifecycle_stage == "frozen"
        and overall_score >= 85
        and not unresolved_hard_issues
    ):
        return "submission_grade_candidate"
    if overall_score >= 70:
        return "near_submission_candidate"
    return "blocked"


def _build_loop_gate(
    *,
    lifecycle_stage: str,
    overall_status: str,
    overall_score: int,
    blocked_dimensions: list[dict[str, Any]],
    unresolved_hard_issues: list[str],
) -> dict[str, Any]:
    if blocked_dimensions:
        blocker = blocked_dimensions[0]
        recommended_stage = blocker.get("rollback_stage") or "revision"
        reason = blocker["blocking_issues"][0]
        return {
            "action": "rollback_required",
            "recommended_stage": recommended_stage,
            "reason": reason,
        }
    if overall_status == "submission_grade_candidate":
        return {
            "action": "ready_for_submission",
            "recommended_stage": None,
            "reason": "质量 scorecard 已满足 submission-grade candidate 的 stop gate。",
        }
    recommended_stage = "revision" if lifecycle_stage in REVIEW_CONTEXT_STAGES else lifecycle_stage
    if overall_score < 70 and not unresolved_hard_issues:
        recommended_stage = "argument_building"
    reason = "仍需继续关闭剩余问题后再尝试 submission gate。"
    if unresolved_hard_issues:
        reason = unresolved_hard_issues[0]
    return {
        "action": "continue",
        "recommended_stage": recommended_stage,
        "reason": reason,
    }


def _build_scorecard_summary(
    *,
    overall_status: str,
    overall_score: int,
    blocked_dimensions: list[dict[str, Any]],
    unresolved_hard_issues: list[str],
) -> str:
    if overall_status == "submission_grade_candidate":
        return f"当前版本质量得分 {overall_score}，已达到 submission-grade candidate。"
    if blocked_dimensions:
        return (
            f"当前版本质量得分 {overall_score}，仍被 {blocked_dimensions[0]['label']} 的硬伤卡住；"
            f"首个 blocker: {blocked_dimensions[0]['blocking_issues'][0]}"
        )
    if unresolved_hard_issues:
        return f"当前版本质量得分 {overall_score}，仍需继续关闭 {len(unresolved_hard_issues)} 项硬伤。"
    return f"当前版本质量得分 {overall_score}，已接近 submission gate，但仍需继续打磨。"


def _resolve_quality_progression(
    *,
    score_delta: int,
    closed_issue_ids: list[str],
    remaining_issue_ids: list[str],
    new_issue_ids: list[str],
) -> str:
    if new_issue_ids:
        return "mixed"
    if score_delta > 0 or closed_issue_ids:
        return "improved"
    if score_delta < 0 and not closed_issue_ids:
        return "regressed"
    if new_issue_ids and remaining_issue_ids:
        return "mixed"
    return "stable"


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
        "summary": action_summary,
        "target_stage": target_stage,
        "source_surface": source_surface,
    }


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


def _build_evidence_supply_queue(tracked_issues: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped_issues: dict[str, list[dict[str, Any]]] = {}
    ordered_gap_ids: list[str] = []
    for tracked_issue in tracked_issues:
        issue = dict(tracked_issue)
        gap_id = _nonempty_string(issue.get("lineage_id")) or _nonempty_string(issue.get("issue_id"))
        if gap_id is None:
            continue
        if gap_id not in grouped_issues:
            grouped_issues[gap_id] = []
            ordered_gap_ids.append(gap_id)
        grouped_issues[gap_id].append(issue)
    return [
        _build_evidence_supply_queue_item(
            gap_id=gap_id,
            issues=grouped_issues[gap_id],
        )
        for gap_id in ordered_gap_ids
    ]


def _build_evidence_supply_queue_item(*, gap_id: str, issues: list[dict[str, Any]]) -> dict[str, Any]:
    severities = _dedupe_preserve_order(
        severity
        for issue in issues
        for severity in [_nonempty_string(issue.get("severity"))]
        if severity is not None
    )
    if severities == ["hard"]:
        gap_kind = "hard_blocker"
    elif severities == ["gap"]:
        gap_kind = "evidence_gap"
    else:
        gap_kind = "mixed_gap"

    issue_summaries = _dedupe_preserve_order(
        summary
        for issue in issues
        for summary in [_nonempty_string(issue.get("summary"))]
        if summary is not None
    )
    linked_issue_ids = _dedupe_preserve_order(
        issue_id
        for issue in issues
        for issue_id in [_nonempty_string(issue.get("issue_id"))]
        if issue_id is not None
    )
    blocking_reasons = _dedupe_preserve_order(
        reason
        for issue in issues
        for reason in [_nonempty_string(issue.get("blocking_reason"))]
        if reason is not None
    )
    source_surfaces = _dedupe_preserve_order(
        source_surface
        for issue in issues
        for source_surface in [_nonempty_string(issue.get("source_surface"))]
        if source_surface is not None
    )
    closure_statuses = _dedupe_preserve_order(
        closure_status
        for issue in issues
        for closure_status in [_nonempty_string(issue.get("closure_status"))]
        if closure_status is not None
    )
    if closure_statuses == ["blocked"]:
        supply_status = "blocked"
    elif closure_statuses == ["evidence_required"]:
        supply_status = "evidence_required"
    else:
        supply_status = "mixed"

    required_input_ids: list[str] = []
    evidence_refs: list[str] = []
    supply_actions = _collect_supply_actions(
        issues=issues,
        required_input_ids=required_input_ids,
        evidence_refs=evidence_refs,
    )
    required_input_ids = _dedupe_preserve_order(required_input_ids)
    evidence_refs = _dedupe_preserve_order(evidence_refs)
    controller_action_hint = _resolve_controller_action_hint(issues)
    if not supply_actions:
        supply_actions = [
            {
                "obligation_id": f"{gap_id}:fallback-action",
                "summary": controller_action_hint["summary"],
                "required_input_ids": list(required_input_ids),
                "evidence_refs": list(evidence_refs),
                "satisfaction_criteria": None,
                "source_surface": controller_action_hint["source_surface"],
            }
        ]

    return {
        "gap_id": gap_id,
        "gap_kind": gap_kind,
        "gap_summary": issue_summaries[0] if issue_summaries else gap_id,
        "supply_status": supply_status,
        "controller_action_hint": controller_action_hint,
        "required_input_ids": required_input_ids,
        "linked_issue_ids": linked_issue_ids,
        "linked_issue_summaries": issue_summaries,
        "blocking_reasons": blocking_reasons,
        "supply_actions": supply_actions,
        "evidence_refs": evidence_refs,
        "source_surfaces": source_surfaces,
    }


def _collect_supply_actions(
    *,
    issues: list[dict[str, Any]],
    required_input_ids: list[str],
    evidence_refs: list[str],
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    seen_action_ids: set[str] = set()
    for issue in issues:
        lineage_basis = _ensure_mapping(issue.get("lineage_basis")) or {}
        required_input_ids.extend(_read_nonempty_string_list(lineage_basis.get("required_input_ids")))
        obligations = issue.get("evidence_obligations")
        if not isinstance(obligations, list):
            continue
        for obligation in obligations:
            obligation_payload = _ensure_mapping(obligation)
            if obligation_payload is None:
                continue
            obligation_id = _nonempty_string(obligation_payload.get("obligation_id"))
            if obligation_id is None or obligation_id in seen_action_ids:
                continue
            seen_action_ids.add(obligation_id)
            obligation_required_inputs = _read_nonempty_string_list(obligation_payload.get("required_input_ids"))
            obligation_evidence_refs = _read_nonempty_string_list(obligation_payload.get("evidence_refs"))
            required_input_ids.extend(obligation_required_inputs)
            evidence_refs.extend(obligation_evidence_refs)
            actions.append(
                {
                    "obligation_id": obligation_id,
                    "summary": _nonempty_string(obligation_payload.get("summary")) or obligation_id,
                    "required_input_ids": obligation_required_inputs,
                    "evidence_refs": obligation_evidence_refs,
                    "satisfaction_criteria": _nonempty_string(obligation_payload.get("satisfaction_criteria")),
                    "source_surface": _nonempty_string(obligation_payload.get("source_surface")) or "grant_quality",
                }
            )
    return actions


def _resolve_controller_action_hint(issues: list[dict[str, Any]]) -> dict[str, Any]:
    prioritized_issues = sorted(
        issues,
        key=lambda item: 0 if _nonempty_string(item.get("severity")) == "hard" else 1,
    )
    for issue in prioritized_issues:
        action_hint = _ensure_mapping(issue.get("recommended_closure_action"))
        if action_hint is None:
            continue
        summary = _nonempty_string(action_hint.get("summary")) or _nonempty_string(issue.get("summary"))
        source_surface = _nonempty_string(action_hint.get("source_surface")) or _nonempty_string(issue.get("source_surface"))
        if summary is None or source_surface is None:
            continue
        return {
            "summary": summary,
            "target_stage": _nonempty_string(action_hint.get("target_stage")),
            "source_surface": source_surface,
        }
    fallback_issue = prioritized_issues[0] if prioritized_issues else {}
    return {
        "summary": _nonempty_string(fallback_issue.get("summary")) or "补齐证据供给项。",
        "target_stage": _nonempty_string(fallback_issue.get("rollback_stage")),
        "source_surface": _nonempty_string(fallback_issue.get("source_surface")) or "grant_quality",
    }


def _build_evidence_supply_progress(
    *,
    previous_queue: list[dict[str, Any]],
    current_queue: list[dict[str, Any]],
) -> dict[str, Any]:
    previous_gap_map = _build_evidence_supply_map(previous_queue)
    current_gap_map = _build_evidence_supply_map(current_queue)
    closed_gap_ids = [gap_id for gap_id in previous_gap_map if gap_id not in current_gap_map]
    remaining_gap_ids = [gap_id for gap_id in previous_gap_map if gap_id in current_gap_map]
    new_gap_ids = [gap_id for gap_id in current_gap_map if gap_id not in previous_gap_map]
    ordered_gap_ids = list(previous_gap_map.keys())
    ordered_gap_ids.extend(gap_id for gap_id in current_gap_map if gap_id not in previous_gap_map)
    return {
        "closed_gaps": closed_gap_ids,
        "remaining_open_gaps": remaining_gap_ids,
        "newly_opened_gaps": new_gap_ids,
        "gap_progress": [
            _build_evidence_supply_gap_progress_entry(
                gap_id=gap_id,
                previous_gap=previous_gap_map.get(gap_id),
                current_gap=current_gap_map.get(gap_id),
            )
            for gap_id in ordered_gap_ids
        ],
    }


def _build_evidence_supply_map(queue: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        gap_id: dict(item)
        for item in queue
        for gap_id in [_nonempty_string(item.get("gap_id"))]
        if gap_id is not None
    }


def _build_evidence_supply_gap_progress_entry(
    *,
    gap_id: str,
    previous_gap: dict[str, Any] | None,
    current_gap: dict[str, Any] | None,
) -> dict[str, Any]:
    if previous_gap is not None and current_gap is None:
        transition = "closed"
        supply_delta = "supply_closed"
    elif previous_gap is None and current_gap is not None:
        transition = "newly_opened"
        supply_delta = "new_gap_opened"
    else:
        transition = "still_open"
        supply_delta = _resolve_supply_delta(
            previous_supply_status=_nonempty_string((previous_gap or {}).get("supply_status")),
            current_supply_status=_nonempty_string((current_gap or {}).get("supply_status")),
            previous_required_input_ids=_read_nonempty_string_list((previous_gap or {}).get("required_input_ids")),
            current_required_input_ids=_read_nonempty_string_list((current_gap or {}).get("required_input_ids")),
        )

    return {
        "gap_id": gap_id,
        "transition": transition,
        "previous_gap_kind": _nonempty_string((previous_gap or {}).get("gap_kind")),
        "current_gap_kind": _nonempty_string((current_gap or {}).get("gap_kind")),
        "previous_supply_status": _nonempty_string((previous_gap or {}).get("supply_status")),
        "current_supply_status": _nonempty_string((current_gap or {}).get("supply_status")),
        "previous_required_input_ids": _read_nonempty_string_list((previous_gap or {}).get("required_input_ids")),
        "current_required_input_ids": _read_nonempty_string_list((current_gap or {}).get("required_input_ids")),
        "previous_linked_issue_ids": _read_nonempty_string_list((previous_gap or {}).get("linked_issue_ids")),
        "current_linked_issue_ids": _read_nonempty_string_list((current_gap or {}).get("linked_issue_ids")),
        "previous_controller_action_hint": _optional_action_hint((previous_gap or {}).get("controller_action_hint")),
        "current_controller_action_hint": _optional_action_hint((current_gap or {}).get("controller_action_hint")),
        "supply_delta": supply_delta,
    }


def _optional_action_hint(value: Any) -> dict[str, Any] | None:
    action_hint = _ensure_mapping(value)
    if action_hint is None:
        return None
    summary = _nonempty_string(action_hint.get("summary"))
    source_surface = _nonempty_string(action_hint.get("source_surface"))
    if summary is None or source_surface is None:
        return None
    return {
        "summary": summary,
        "target_stage": _nonempty_string(action_hint.get("target_stage")),
        "source_surface": source_surface,
    }


def _resolve_supply_delta(
    *,
    previous_supply_status: str | None,
    current_supply_status: str | None,
    previous_required_input_ids: list[str],
    current_required_input_ids: list[str],
) -> str:
    rank = {
        "blocked": 2,
        "mixed": 2,
        "evidence_required": 1,
    }
    previous_rank = rank.get(previous_supply_status or "")
    current_rank = rank.get(current_supply_status or "")
    if previous_rank is not None and current_rank is not None:
        if current_rank < previous_rank:
            return "progressed"
        if current_rank > previous_rank:
            return "regressed"

    previous_inputs = set(previous_required_input_ids)
    current_inputs = set(current_required_input_ids)
    if current_inputs < previous_inputs:
        return "progressed"
    if previous_inputs < current_inputs:
        return "regressed"
    return "unchanged"


def _open_issue_lineage_map(tracked_issues: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in tracked_issues:
        if _nonempty_string(item.get("status")) != "open":
            continue
        lineage_id = _nonempty_string(item.get("lineage_id"))
        if lineage_id is None:
            continue
        result[lineage_id] = dict(item)
    return result


def _build_issue_closure_progress_entries(
    *,
    previous_open_issues: Mapping[str, dict[str, Any]],
    current_open_issues: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    ordered_issue_ids = list(previous_open_issues.keys())
    ordered_issue_ids.extend(issue_id for issue_id in current_open_issues if issue_id not in previous_open_issues)
    return [
        _build_issue_closure_progress_entry(
            lineage_id=issue_id,
            previous_issue=previous_open_issues.get(issue_id),
            current_issue=current_open_issues.get(issue_id),
        )
        for issue_id in ordered_issue_ids
    ]


def _build_issue_closure_progress_entry(
    *,
    lineage_id: str,
    previous_issue: dict[str, Any] | None,
    current_issue: dict[str, Any] | None,
) -> dict[str, Any]:
    issue = current_issue or previous_issue or {}
    previous_issue_id = _nonempty_string(previous_issue.get("issue_id")) if previous_issue else None
    current_issue_id = _nonempty_string(current_issue.get("issue_id")) if current_issue else None
    previous_summary = _nonempty_string(previous_issue.get("summary")) if previous_issue else None
    current_summary = _nonempty_string(current_issue.get("summary")) if current_issue else None
    previous_closure_status = _nonempty_string(previous_issue.get("closure_status")) if previous_issue else None
    current_closure_status = _nonempty_string(current_issue.get("closure_status")) if current_issue else None
    if previous_issue is not None and current_issue is None:
        transition = "closed"
        closure_delta = "issue_closed"
    elif previous_issue is None and current_issue is not None:
        transition = "newly_opened"
        closure_delta = "new_blocker_opened" if current_issue.get("severity") == "hard" else "new_gap_opened"
    else:
        transition = "still_open"
        closure_delta = _resolve_issue_closure_delta(
            previous_closure_status=previous_closure_status,
            current_closure_status=current_closure_status,
        )
    return {
        "issue_id": current_issue_id or previous_issue_id,
        "lineage_id": lineage_id,
        "lineage_basis": dict(issue.get("lineage_basis") or {}),
        "previous_issue_id": previous_issue_id,
        "current_issue_id": current_issue_id,
        "previous_summary": previous_summary,
        "current_summary": current_summary,
        "dimension_id": issue.get("dimension_id"),
        "summary": current_summary or previous_summary,
        "severity": issue.get("severity"),
        "transition": transition,
        "previous_closure_status": previous_closure_status,
        "current_closure_status": current_closure_status,
        "blocking_reason": (
            _nonempty_string(current_issue.get("blocking_reason")) if current_issue else None
        ) or (
            _nonempty_string(previous_issue.get("blocking_reason")) if previous_issue else None
        ),
        "closure_delta": closure_delta,
    }


def _resolve_issue_closure_delta(
    *,
    previous_closure_status: str | None,
    current_closure_status: str | None,
) -> str:
    rank = {
        "blocked": 2,
        "evidence_required": 1,
    }
    previous_rank = rank.get(previous_closure_status or "")
    current_rank = rank.get(current_closure_status or "")
    if previous_rank is None or current_rank is None or previous_rank == current_rank:
        return "unchanged"
    if current_rank < previous_rank:
        return "progressed"
    return "regressed"


def _read_critique_summary(document: dict[str, Any]) -> dict[str, Any] | None:
    lifecycle_stage = _nonempty_string(document.get("lifecycle_stage"))
    if lifecycle_stage not in REVIEW_CONTEXT_STAGES:
        return None
    try:
        return build_critique_summary(document)
    except WorkspaceStateError:
        return None


def _read_active_draft_id(document: Mapping[str, Any]) -> str | None:
    selection = _ensure_mapping(document.get("current_selection")) or {}
    return _nonempty_string(selection.get("active_draft_id"))


def _ensure_mapping(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def _safe_int(value: Any) -> int | None:
    return value if isinstance(value, int) else None


def _nonempty_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None


def _read_nonempty_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = _nonempty_string(item)
        if text is not None:
            result.append(text)
    return result


def _read_nested_string_list(payload: Mapping[str, Any], parent_key: str, child_key: str) -> list[str]:
    parent = _ensure_mapping(payload.get(parent_key))
    if parent is None:
        return []
    return _read_nonempty_string_list(parent.get(child_key))


def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in values:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def _flatten_to_strings(values: Iterable[Any]) -> list[str]:
    result: list[str] = []
    for item in values:
        if isinstance(item, list):
            result.extend(_flatten_to_strings(item))
            continue
        text = _nonempty_string(item)
        if text is not None:
            result.append(text)
    return result
