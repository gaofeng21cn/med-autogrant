from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.grant_quality_parts import (
    _dedupe_preserve_order,
    _ensure_mapping,
    _flatten_to_strings,
    _nonempty_string,
    _read_nested_string_list,
    _read_nonempty_string_list,
    _safe_int,
)

REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}

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

__all__ = [name for name in globals() if name.startswith("_") and not name.startswith("__")]
