from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from med_autogrant.workspace_index import _index_objects
from med_autogrant.workspace_reference_validation import (
    _draft_links_argument_chain,
    _draft_links_fit_mapping,
    _validate_reference_sets,
)
from med_autogrant.workspace_stage_validation import _validate_stage_requirements
from med_autogrant.workspace_types import ValidationIssue

_STAGE_ORDER: tuple[str, ...] = (
    "input_intake",
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
)
_STAGE_RANK: dict[str, int] = {name: idx for idx, name in enumerate(_STAGE_ORDER)}


class _WorkspaceRuntimeRequirements(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    direction: bool = False
    question: bool = False
    argument_chain: bool = False
    fit_mapping: bool = False
    draft: bool = False
    revision_plan: bool = False
    direction_count: bool = False
    critique_question_anchor: bool = False


class _CurrentSelectionSnapshot(BaseModel):
    model_config = ConfigDict(extra="allow")

    selected_direction_id: Any = None
    selected_question_id: Any = None
    active_fit_mapping_id: Any = None
    active_draft_id: Any = None
    active_revision_plan_id: Any = None


class _SelectionBindingRule(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    selection_field: str
    object_label: str


_EMPTY_REQUIREMENTS = _WorkspaceRuntimeRequirements()
_STAGE_REQUIREMENTS: dict[str, _WorkspaceRuntimeRequirements] = {
    stage: _WorkspaceRuntimeRequirements(
        direction=rank >= _STAGE_RANK["direction_screening"],
        question=rank >= _STAGE_RANK["question_refinement"],
        argument_chain=rank >= _STAGE_RANK["argument_building"],
        fit_mapping=rank >= _STAGE_RANK["fit_alignment"],
        draft=rank >= _STAGE_RANK["outline"],
        revision_plan=rank >= _STAGE_RANK["critique"],
        direction_count=stage in {"direction_screening", "question_refinement"},
        critique_question_anchor=rank >= _STAGE_RANK["critique"],
    )
    for stage, rank in _STAGE_RANK.items()
}

_DIRECTION_BINDING = _SelectionBindingRule(
    selection_field="selected_direction_id",
    object_label="DirectionHypothesis",
)
_QUESTION_BINDING = _SelectionBindingRule(
    selection_field="selected_question_id",
    object_label="ScientificQuestionCard",
)
_FIT_MAPPING_BINDING = _SelectionBindingRule(
    selection_field="active_fit_mapping_id",
    object_label="ApplicantFitMapping",
)
_DRAFT_BINDING = _SelectionBindingRule(
    selection_field="active_draft_id",
    object_label="ApplicationDraft",
)
_REVISION_PLAN_BINDING = _SelectionBindingRule(
    selection_field="active_revision_plan_id",
    object_label="RevisionPlan",
)


def _requirements_for_stage(stage: Any) -> _WorkspaceRuntimeRequirements:
    if isinstance(stage, str):
        return _STAGE_REQUIREMENTS.get(stage, _EMPTY_REQUIREMENTS)
    return _EMPTY_REQUIREMENTS


def _resolve_bound_object(
    *,
    stage: Any,
    required: bool,
    rule: _SelectionBindingRule,
    selected_id: Any,
    objects: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    resolved = objects.get(selected_id) if isinstance(selected_id, str) else None
    path = f"current_selection.{rule.selection_field}"
    if required and selected_id is None:
        issues.append(
            ValidationIssue(
                path=path,
                message=f"{stage} 阶段必须显式绑定当前 {rule.object_label}。",
            )
        )
    elif selected_id is not None and resolved is None:
        issues.append(
            ValidationIssue(
                path=path,
                message=f"未找到对应的 {rule.object_label}。",
            )
        )
    return resolved


def _selected_direction_count(document: dict[str, Any]) -> int:
    return sum(
        1
        for item in document.get("direction_hypotheses", [])
        if isinstance(item, dict) and item.get("decision_status") == "selected"
    )


def _resolve_active_argument_chain(
    document: dict[str, Any],
    *,
    selected_question: dict[str, Any] | None,
    selected_question_id: Any,
    required: bool,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    if selected_question is None or not required:
        return None
    matches = [
        item
        for item in document.get("argument_chains", [])
        if isinstance(item, dict) and item.get("scientific_question_id") == selected_question_id
    ]
    if not matches:
        issues.append(
            ValidationIssue(
                path="argument_chains",
                message="当前选中问题缺少对应的 ArgumentChain。",
            )
        )
        return None
    if len(matches) > 1:
        issues.append(
            ValidationIssue(
                path="argument_chains",
                message="当前选中问题只能对应一个激活中的 ArgumentChain。",
            )
        )
        return None
    return matches[0]


def _validate_critique_and_rereview_links(
    *,
    active_revision_plan: dict[str, Any],
    active_draft: dict[str, Any] | None,
    critiques: dict[str, dict[str, Any]],
    revision_plans: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    active_critique = critiques.get(active_revision_plan.get("critique_id"))
    if active_critique is None:
        issues.append(
            ValidationIssue(
                path="revision_plans",
                message="激活修订计划引用了不存在的 MentorCritique。",
            )
        )
        return None, None

    if active_draft is not None and active_critique.get("draft_id") != active_draft.get("draft_id"):
        issues.append(
            ValidationIssue(
                path="mentor_critiques",
                message="激活批注必须与当前激活草稿一致。",
            )
        )

    reviewed_plan_id = active_critique.get("reviewed_revision_plan_id")
    if reviewed_plan_id is None:
        return active_critique, None

    reviewed_plan = revision_plans.get(reviewed_plan_id)
    if reviewed_plan is None:
        issues.append(
            ValidationIssue(
                path="mentor_critiques.reviewed_revision_plan_id",
                message="re-review 批注必须引用已存在的已完成 RevisionPlan。",
            )
        )
        return active_critique, None

    if active_draft is not None and reviewed_plan.get("draft_id") != active_draft.get("draft_id"):
        issues.append(
            ValidationIssue(
                path="mentor_critiques.reviewed_revision_plan_id",
                message="re-review 批注引用的 RevisionPlan 必须回指当前激活草稿。",
            )
        )
    if reviewed_plan.get("execution_status") != "completed":
        issues.append(
            ValidationIssue(
                path="mentor_critiques.reviewed_revision_plan_id",
                message="re-review 批注引用的 RevisionPlan 必须已经 completed。",
            )
        )

    expected_version = active_draft.get("version_label") if active_draft is not None else None
    version_anchor = "当前激活草稿版本"
    if active_revision_plan.get("execution_status") == "completed":
        expected_version = active_revision_plan.get("pre_revision_version_label")
        version_anchor = "当前激活 RevisionPlan.pre_revision_version_label"
    if (
        isinstance(expected_version, str)
        and reviewed_plan.get("post_revision_version_label") != expected_version
    ):
        issues.append(
            ValidationIssue(
                path="mentor_critiques.reviewed_revision_plan_id",
                message=f"re-review 批注引用的 RevisionPlan 必须与{version_anchor}一致。",
            )
        )
    return active_critique, reviewed_plan


def _validate_runtime_constraints(document: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    stage = document.get("lifecycle_stage")
    requirements = _requirements_for_stage(stage)

    directions = _index_objects(document.get("direction_hypotheses"), "direction_id", "direction_hypotheses", issues)
    questions = _index_objects(document.get("scientific_question_cards"), "question_id", "scientific_question_cards", issues)
    _index_objects(document.get("argument_chains"), "argument_chain_id", "argument_chains", issues)
    fit_mappings = _index_objects(document.get("applicant_fit_mappings"), "fit_mapping_id", "applicant_fit_mappings", issues)
    drafts = _index_objects(document.get("application_drafts"), "draft_id", "application_drafts", issues)
    critiques = _index_objects(document.get("mentor_critiques"), "critique_id", "mentor_critiques", issues)
    revision_plans = _index_objects(document.get("revision_plans"), "revision_plan_id", "revision_plans", issues)

    raw_selection = document.get("current_selection")
    selection = _CurrentSelectionSnapshot.model_validate(raw_selection if isinstance(raw_selection, dict) else {})

    if requirements.direction_count and len(document.get("direction_hypotheses", [])) < 1:
        issues.append(
            ValidationIssue(
                path="direction_hypotheses",
                message="P2.A 方向阶段必须保留至少一个可论证 DirectionHypothesis。",
            )
        )
    if requirements.direction and _selected_direction_count(document) != 1:
        issues.append(
            ValidationIssue(
                path="direction_hypotheses",
                message="必须且只能有一个 decision_status=selected 的 DirectionHypothesis。",
            )
        )

    selected_direction = _resolve_bound_object(
        stage=stage,
        required=requirements.direction,
        rule=_DIRECTION_BINDING,
        selected_id=selection.selected_direction_id,
        objects=directions,
        issues=issues,
    )
    if selected_direction is not None and selected_direction.get("decision_status") != "selected":
        issues.append(
            ValidationIssue(
                path="current_selection.selected_direction_id",
                message="当前选中方向必须处于 selected 状态。",
            )
        )

    selected_question = _resolve_bound_object(
        stage=stage,
        required=requirements.question,
        rule=_QUESTION_BINDING,
        selected_id=selection.selected_question_id,
        objects=questions,
        issues=issues,
    )
    if (
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

    active_argument_chain = _resolve_active_argument_chain(
        document,
        selected_question=selected_question,
        selected_question_id=selection.selected_question_id,
        required=requirements.argument_chain,
        issues=issues,
    )

    active_fit_mapping = _resolve_bound_object(
        stage=stage,
        required=requirements.fit_mapping,
        rule=_FIT_MAPPING_BINDING,
        selected_id=selection.active_fit_mapping_id,
        objects=fit_mappings,
        issues=issues,
    )
    if (
        active_fit_mapping is not None
        and selection.selected_question_id is not None
        and active_fit_mapping.get("scientific_question_id") != selection.selected_question_id
    ):
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

    active_draft = _resolve_bound_object(
        stage=stage,
        required=requirements.draft,
        rule=_DRAFT_BINDING,
        selected_id=selection.active_draft_id,
        objects=drafts,
        issues=issues,
    )
    if (
        active_draft is not None
        and selection.selected_question_id is not None
        and active_draft.get("frozen_question_id") != selection.selected_question_id
    ):
        issues.append(
            ValidationIssue(
                path="application_drafts",
                message="激活草稿冻结的问题必须与当前选中问题一致。",
            )
        )
    if (
        active_draft is not None
        and active_argument_chain is not None
        and not _draft_links_argument_chain(active_draft, active_argument_chain["argument_chain_id"])
    ):
        issues.append(
            ValidationIssue(
                path="application_drafts",
                message="激活草稿必须显式链接当前问题对应的 ArgumentChain。",
            )
        )
    if (
        active_draft is not None
        and active_fit_mapping is not None
        and not _draft_links_fit_mapping(active_draft, active_fit_mapping["fit_mapping_id"])
    ):
        issues.append(
            ValidationIssue(
                path="application_drafts",
                message="激活草稿必须显式链接当前问题对应的 ApplicantFitMapping。",
            )
        )

    active_revision_plan = _resolve_bound_object(
        stage=stage,
        required=requirements.revision_plan,
        rule=_REVISION_PLAN_BINDING,
        selected_id=selection.active_revision_plan_id,
        objects=revision_plans,
        issues=issues,
    )
    if (
        active_revision_plan is not None
        and active_draft is not None
        and active_revision_plan.get("draft_id") != active_draft.get("draft_id")
    ):
        issues.append(
            ValidationIssue(
                path="revision_plans",
                message="激活修订计划必须回指当前激活草稿。",
            )
        )

    active_critique: dict[str, Any] | None = None
    reviewed_revision_plan: dict[str, Any] | None = None
    if active_revision_plan is not None:
        active_critique, reviewed_revision_plan = _validate_critique_and_rereview_links(
            active_revision_plan=active_revision_plan,
            active_draft=active_draft,
            critiques=critiques,
            revision_plans=revision_plans,
            issues=issues,
        )

    if (
        requirements.critique_question_anchor
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
        selected_question_id=selection.selected_question_id if isinstance(selection.selected_question_id, str) else None,
        active_argument_chain_id=active_argument_chain.get("argument_chain_id") if isinstance(active_argument_chain, dict) else None,
        active_fit_mapping_id=active_fit_mapping.get("fit_mapping_id") if isinstance(active_fit_mapping, dict) else None,
        active_revision_plan=active_revision_plan,
        active_critique=active_critique,
        reviewed_revision_plan=reviewed_revision_plan,
        issues=issues,
    )

    return issues
