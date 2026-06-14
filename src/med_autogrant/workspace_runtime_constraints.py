from __future__ import annotations

from typing import Any

from med_autogrant.workspace_index import _index_objects
from med_autogrant.workspace_reference_validation import (
    _draft_links_argument_chain,
    _draft_links_fit_mapping,
    _validate_reference_sets,
)
from med_autogrant.workspace_runtime_policy import _requirements_for_stage
from med_autogrant.workspace_runtime_selection import _resolve_runtime_selection
from med_autogrant.workspace_stage_validation import _validate_stage_requirements
from med_autogrant.workspace_types import ValidationIssue

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
