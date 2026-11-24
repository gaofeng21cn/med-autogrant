from __future__ import annotations

from typing import Any

from med_autogrant.grant_quality_parts import _dedupe_preserve_order

from . import REVIEW_CONTEXT_STAGES, QualityContext, _QUALITY_DIMENSION_SPECS
from .issue_lineage import _build_issue


def _finalize_dimension(
    *,
    dimension_id: str,
    summary: str,
    score: int,
    blockers: list[str],
    evidence_gaps: list[str],
    evidence_refs: list[str] | None = None,
    context: QualityContext,
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
    ai_reviewer_required: bool = False,
) -> str:
    if ai_reviewer_required:
        return "blocked"
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
    ai_reviewer_required: bool = False,
) -> dict[str, Any]:
    if ai_reviewer_required:
        return {
            "action": "continue",
            "recommended_stage": "critique",
            "reason": "AI reviewer-backed critique is required before grant quality can be marked near-submission or submission-grade.",
        }
    if blocked_dimensions:
        blocker = blocked_dimensions[0]
        recommended_stage = blocker.get("rollback_stage") or "revision"
        reason = blocker["blocking_issues"][0]
        return {
            "action": "route_back_recommended",
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
    ai_reviewer_required: bool = False,
) -> str:
    if ai_reviewer_required:
        return f"当前版本结构质量得分 {overall_score}，但缺少 AI reviewer-backed critique，不能给出 submission-grade 或 near-submission 质量判断。"
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
