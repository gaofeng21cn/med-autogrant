from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from med_autogrant.workspace_index import _index_objects
from med_autogrant.workspace_reference_validation import (
    _draft_links_argument_chain,
    _draft_links_fit_mapping,
    _validate_reference_sets,
)
from med_autogrant.workspace_stage_validation import _validate_stage_requirements
from med_autogrant.workspace_types import ValidationIssue


_DIRECTION_STAGES = {
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
}
_QUESTION_STAGES = {
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
}
_ARGUMENT_CHAIN_STAGES = {
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
}
_FIT_MAPPING_STAGES = {"fit_alignment", "outline", "drafting", "critique", "revision", "frozen"}
_DRAFT_STAGES = {"outline", "drafting", "critique", "revision", "frozen"}
_REVISION_PLAN_STAGES = {"critique", "revision", "frozen"}
_DIRECTION_COUNT_STAGES = {"direction_screening", "question_refinement"}


@dataclass(frozen=True)
class _WorkspaceRuntimeRequirements:
    direction: bool
    question: bool
    argument_chain: bool
    fit_mapping: bool
    draft: bool
    revision_plan: bool
    direction_count: bool


@dataclass(frozen=True)
class _WorkspaceRuntimeSelection:
    selected_direction_id: Any
    selected_question_id: Any
    active_fit_mapping_id: Any
    active_draft_id: Any
    active_revision_plan_id: Any
    selected_direction: dict[str, Any] | None
    selected_question: dict[str, Any] | None


def _requirements_for_stage(stage: Any) -> _WorkspaceRuntimeRequirements:
    return _WorkspaceRuntimeRequirements(
        direction=stage in _DIRECTION_STAGES,
        question=stage in _QUESTION_STAGES,
        argument_chain=stage in _ARGUMENT_CHAIN_STAGES,
        fit_mapping=stage in _FIT_MAPPING_STAGES,
        draft=stage in _DRAFT_STAGES,
        revision_plan=stage in _REVISION_PLAN_STAGES,
        direction_count=stage in _DIRECTION_COUNT_STAGES,
    )


def _resolve_runtime_selection(
    document: dict[str, Any],
    *,
    stage: Any,
    requirements: _WorkspaceRuntimeRequirements,
    directions: dict[str, dict[str, Any]],
    questions: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> _WorkspaceRuntimeSelection:
    selection = document.get("current_selection", {})
    selected_direction_id = selection.get("selected_direction_id")
    selected_question_id = selection.get("selected_question_id")
    active_fit_mapping_id = selection.get("active_fit_mapping_id")
    active_draft_id = selection.get("active_draft_id")
    active_revision_plan_id = selection.get("active_revision_plan_id")

    _validate_direction_count(document, requirements=requirements, issues=issues)
    selected_direction = _resolve_selected_direction(
        stage=stage,
        requirements=requirements,
        selected_direction_id=selected_direction_id,
        directions=directions,
        selected_direction_count=_selected_direction_count(document),
        issues=issues,
    )
    selected_question = _resolve_selected_question(
        stage=stage,
        requirements=requirements,
        selected_direction=selected_direction,
        selected_question_id=selected_question_id,
        questions=questions,
        issues=issues,
    )

    return _WorkspaceRuntimeSelection(
        selected_direction_id=selected_direction_id,
        selected_question_id=selected_question_id,
        active_fit_mapping_id=active_fit_mapping_id,
        active_draft_id=active_draft_id,
        active_revision_plan_id=active_revision_plan_id,
        selected_direction=selected_direction,
        selected_question=selected_question,
    )


def _selected_direction_count(document: dict[str, Any]) -> int:
    return sum(
        1
        for item in document.get("direction_hypotheses", [])
        if isinstance(item, dict) and item.get("decision_status") == "selected"
    )


def _validate_direction_count(
    document: dict[str, Any],
    *,
    requirements: _WorkspaceRuntimeRequirements,
    issues: list[ValidationIssue],
) -> None:
    if not requirements.direction_count:
        return
    direction_count = len(document.get("direction_hypotheses", []))
    if direction_count < 2 or direction_count > 5:
        issues.append(
            ValidationIssue(
                path="direction_hypotheses",
                message="P2.A 方向阶段必须保留 2 到 5 个 DirectionHypothesis。",
            )
        )


def _resolve_selected_direction(
    *,
    stage: Any,
    requirements: _WorkspaceRuntimeRequirements,
    selected_direction_id: Any,
    directions: dict[str, dict[str, Any]],
    selected_direction_count: int,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    if requirements.direction and selected_direction_count != 1:
        issues.append(
            ValidationIssue(
                path="direction_hypotheses",
                message="必须且只能有一个 decision_status=selected 的 DirectionHypothesis。",
            )
        )

    selected_direction = directions.get(selected_direction_id) if isinstance(selected_direction_id, str) else None
    if requirements.direction and selected_direction_id is None:
        issues.append(
            ValidationIssue(
                path="current_selection.selected_direction_id",
                message=f"{stage} 阶段必须显式绑定当前 DirectionHypothesis。",
            )
        )
    elif selected_direction_id is not None and selected_direction is None:
        issues.append(
            ValidationIssue(
                path="current_selection.selected_direction_id",
                message="未找到对应的 DirectionHypothesis。",
            )
        )
    elif selected_direction is not None and selected_direction.get("decision_status") != "selected":
        issues.append(
            ValidationIssue(
                path="current_selection.selected_direction_id",
                message="当前选中方向必须处于 selected 状态。",
            )
        )
    return selected_direction


def _resolve_selected_question(
    *,
    stage: Any,
    requirements: _WorkspaceRuntimeRequirements,
    selected_direction: dict[str, Any] | None,
    selected_question_id: Any,
    questions: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    selected_question = questions.get(selected_question_id) if isinstance(selected_question_id, str) else None
    if requirements.question and selected_question_id is None:
        issues.append(
            ValidationIssue(
                path="current_selection.selected_question_id",
                message=f"{stage} 阶段必须显式绑定当前 ScientificQuestionCard。",
            )
        )
    elif selected_question_id is not None and selected_question is None:
        issues.append(
            ValidationIssue(
                path="current_selection.selected_question_id",
                message="未找到对应的 ScientificQuestionCard。",
            )
        )
    elif (
        selected_direction is not None
        and selected_question is not None
        and selected_question.get("parent_direction_id") != selected_direction.get("direction_id")
    ):
        issues.append(
            ValidationIssue(
                path="current_selection.selected_question_id",
                message="当前选中问题不属于当前选中方向。",
            )
        )
    return selected_question


def _validate_runtime_constraints(document: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    stage = document.get("lifecycle_stage")
    requirements = _requirements_for_stage(stage)

    directions = _index_objects(document.get("direction_hypotheses"), "direction_id", "direction_hypotheses", issues)
    questions = _index_objects(document.get("scientific_question_cards"), "question_id", "scientific_question_cards", issues)
    argument_chains = _index_objects(document.get("argument_chains"), "argument_chain_id", "argument_chains", issues)
    fit_mappings = _index_objects(document.get("applicant_fit_mappings"), "fit_mapping_id", "applicant_fit_mappings", issues)
    drafts = _index_objects(document.get("application_drafts"), "draft_id", "application_drafts", issues)
    critiques = _index_objects(document.get("mentor_critiques"), "critique_id", "mentor_critiques", issues)
    revision_plans = _index_objects(document.get("revision_plans"), "revision_plan_id", "revision_plans", issues)

    selection = _resolve_runtime_selection(
        document,
        stage=stage,
        requirements=requirements,
        directions=directions,
        questions=questions,
        issues=issues,
    )
    selected_direction_id = selection.selected_direction_id
    selected_question_id = selection.selected_question_id
    active_fit_mapping_id = selection.active_fit_mapping_id
    active_draft_id = selection.active_draft_id
    active_revision_plan_id = selection.active_revision_plan_id
    selected_question = selection.selected_question

    active_argument_chain = None
    if selected_question is not None and requirements.argument_chain:
        selected_argument_chains = [
            item
            for item in document.get("argument_chains", [])
            if isinstance(item, dict) and item.get("scientific_question_id") == selected_question_id
        ]
        if not selected_argument_chains:
            issues.append(
                ValidationIssue(
                    path="argument_chains",
                    message="当前选中问题缺少对应的 ArgumentChain。",
                )
            )
        elif len(selected_argument_chains) > 1:
            issues.append(
                ValidationIssue(
                    path="argument_chains",
                    message="当前选中问题只能对应一个激活中的 ArgumentChain。",
                )
            )
        if len(selected_argument_chains) == 1:
            active_argument_chain = selected_argument_chains[0]

    active_fit_mapping = fit_mappings.get(active_fit_mapping_id) if isinstance(active_fit_mapping_id, str) else None
    if requirements.fit_mapping and active_fit_mapping_id is None:
        issues.append(
            ValidationIssue(
                path="current_selection.active_fit_mapping_id",
                message=f"{stage} 阶段必须显式绑定当前 ApplicantFitMapping。",
            )
        )
    elif active_fit_mapping_id is not None and active_fit_mapping is None:
        issues.append(
            ValidationIssue(
                path="current_selection.active_fit_mapping_id",
                message="未找到对应的 ApplicantFitMapping。",
            )
        )
    elif active_fit_mapping is not None and selected_question_id is not None and active_fit_mapping.get("scientific_question_id") != selected_question_id:
        issues.append(
            ValidationIssue(
                path="applicant_fit_mappings",
                message="激活适配度映射必须回指当前选中问题。",
            )
        )
    elif (
        active_fit_mapping is not None
        and active_argument_chain is not None
        and active_fit_mapping.get("argument_chain_id") != active_argument_chain.get("argument_chain_id")
    ):
        issues.append(
            ValidationIssue(
                path="applicant_fit_mappings",
                message="激活适配度映射必须回指当前问题对应的 ArgumentChain。",
            )
        )

    active_draft = drafts.get(active_draft_id) if isinstance(active_draft_id, str) else None
    if requirements.draft and active_draft_id is None:
        issues.append(
            ValidationIssue(
                path="current_selection.active_draft_id",
                message=f"{stage} 阶段必须显式绑定当前 ApplicationDraft。",
            )
        )
    elif active_draft_id is not None and active_draft is None:
        issues.append(
            ValidationIssue(
                path="current_selection.active_draft_id",
                message="未找到对应的 ApplicationDraft。",
            )
        )
    elif active_draft is not None and selected_question_id is not None and active_draft.get("frozen_question_id") != selected_question_id:
        issues.append(
            ValidationIssue(
                path="application_drafts",
                message="激活草稿冻结的问题必须与当前选中问题一致。",
            )
        )
    if active_draft is not None and active_argument_chain is not None and not _draft_links_argument_chain(active_draft, active_argument_chain["argument_chain_id"]):
        issues.append(
            ValidationIssue(
                path="application_drafts",
                message="激活草稿必须显式链接当前问题对应的 ArgumentChain。",
            )
        )
    if active_draft is not None and active_fit_mapping is not None and not _draft_links_fit_mapping(active_draft, active_fit_mapping["fit_mapping_id"]):
        issues.append(
            ValidationIssue(
                path="application_drafts",
                message="激活草稿必须显式链接当前问题对应的 ApplicantFitMapping。",
            )
        )

    active_revision_plan = revision_plans.get(active_revision_plan_id) if isinstance(active_revision_plan_id, str) else None
    if requirements.revision_plan and active_revision_plan_id is None:
        issues.append(
            ValidationIssue(
                path="current_selection.active_revision_plan_id",
                message=f"{stage} 阶段必须显式绑定当前 RevisionPlan。",
            )
        )
    elif active_revision_plan_id is not None and active_revision_plan is None:
        issues.append(
            ValidationIssue(
                path="current_selection.active_revision_plan_id",
                message="未找到对应的 RevisionPlan。",
            )
        )
    elif active_revision_plan is not None and active_draft is not None and active_revision_plan.get("draft_id") != active_draft.get("draft_id"):
        issues.append(
            ValidationIssue(
                path="revision_plans",
                message="激活修订计划必须回指当前激活草稿。",
            )
        )

    active_critique = None
    reviewed_revision_plan = None
    if active_revision_plan is not None:
        active_critique = critiques.get(active_revision_plan.get("critique_id"))
        if active_critique is None:
            issues.append(
                ValidationIssue(
                    path="revision_plans",
                    message="激活修订计划引用了不存在的 MentorCritique。",
                )
            )
        elif active_draft is not None and active_critique.get("draft_id") != active_draft.get("draft_id"):
            issues.append(
                ValidationIssue(
                    path="mentor_critiques",
                    message="激活批注必须与当前激活草稿一致。",
                )
            )
        reviewed_revision_plan_id = active_critique.get("reviewed_revision_plan_id")
        if reviewed_revision_plan_id is not None:
            reviewed_revision_plan = revision_plans.get(reviewed_revision_plan_id)
            if reviewed_revision_plan is None:
                issues.append(
                    ValidationIssue(
                        path="mentor_critiques.reviewed_revision_plan_id",
                        message="re-review 批注必须引用已存在的已完成 RevisionPlan。",
                    )
                )
            else:
                if active_draft is not None and reviewed_revision_plan.get("draft_id") != active_draft.get("draft_id"):
                    issues.append(
                        ValidationIssue(
                            path="mentor_critiques.reviewed_revision_plan_id",
                            message="re-review 批注引用的 RevisionPlan 必须回指当前激活草稿。",
                        )
                    )
                if reviewed_revision_plan.get("execution_status") != "completed":
                    issues.append(
                        ValidationIssue(
                            path="mentor_critiques.reviewed_revision_plan_id",
                            message="re-review 批注引用的 RevisionPlan 必须已经 completed。",
                        )
                    )
                expected_reviewed_version = active_draft.get("version_label") if active_draft is not None else None
                version_anchor_message = "当前激活草稿版本"
                if active_revision_plan.get("execution_status") == "completed":
                    expected_reviewed_version = active_revision_plan.get("pre_revision_version_label")
                    version_anchor_message = "当前激活 RevisionPlan.pre_revision_version_label"
                if (
                    isinstance(expected_reviewed_version, str)
                    and reviewed_revision_plan.get("post_revision_version_label") != expected_reviewed_version
                ):
                    issues.append(
                        ValidationIssue(
                            path="mentor_critiques.reviewed_revision_plan_id",
                            message=f"re-review 批注引用的 RevisionPlan 必须与{version_anchor_message}一致。",
                        )
                    )

    if (
        stage in {"critique", "revision", "frozen"}
        and active_critique is not None
        and selected_question is not None
        and active_critique.get("current_scientific_question") != selected_question.get("core_question")
    ):
        issues.append(
            ValidationIssue(
                path="mentor_critiques.current_scientific_question",
                message="激活批注必须锚定当前选中问题的 core_question。",
            )
        )

    _validate_reference_sets(document, issues)
    _validate_stage_requirements(
        document,
        selected_question_id=selected_question_id if isinstance(selected_question_id, str) else None,
        active_argument_chain_id=active_argument_chain.get("argument_chain_id") if isinstance(active_argument_chain, dict) else None,
        active_fit_mapping_id=active_fit_mapping.get("fit_mapping_id") if isinstance(active_fit_mapping, dict) else None,
        active_revision_plan=active_revision_plan,
        active_critique=active_critique,
        reviewed_revision_plan=reviewed_revision_plan,
        issues=issues,
    )

    return issues
