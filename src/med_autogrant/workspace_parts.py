from __future__ import annotations

from datetime import datetime
from typing import Any

from med_autogrant.workspace_types import ValidationIssue, WorkspaceContext, WorkspaceState
from med_autogrant.workspace_projection_parts import *  # noqa: F401,F403

REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}

def _validate_runtime_constraints(document: dict[str, Any]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    stage = document.get("lifecycle_stage")

    directions = _index_objects(document.get("direction_hypotheses"), "direction_id", "direction_hypotheses", issues)
    questions = _index_objects(document.get("scientific_question_cards"), "question_id", "scientific_question_cards", issues)
    argument_chains = _index_objects(document.get("argument_chains"), "argument_chain_id", "argument_chains", issues)
    fit_mappings = _index_objects(document.get("applicant_fit_mappings"), "fit_mapping_id", "applicant_fit_mappings", issues)
    drafts = _index_objects(document.get("application_drafts"), "draft_id", "application_drafts", issues)
    critiques = _index_objects(document.get("mentor_critiques"), "critique_id", "mentor_critiques", issues)
    revision_plans = _index_objects(document.get("revision_plans"), "revision_plan_id", "revision_plans", issues)

    requires_direction = stage in {
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
    requires_question = stage in {
        "question_refinement",
        "argument_building",
        "fit_alignment",
        "outline",
        "drafting",
        "critique",
        "revision",
        "frozen",
    }
    requires_argument_chain = stage in {
        "argument_building",
        "fit_alignment",
        "outline",
        "drafting",
        "critique",
        "revision",
        "frozen",
    }
    requires_fit_mapping = stage in {
        "fit_alignment",
        "outline",
        "drafting",
        "critique",
        "revision",
        "frozen",
    }
    requires_draft = stage in {"outline", "drafting", "critique", "revision", "frozen"}
    requires_revision_plan = stage in {"critique", "revision", "frozen"}

    selected_directions = [
        item["direction_id"]
        for item in document.get("direction_hypotheses", [])
        if isinstance(item, dict) and item.get("decision_status") == "selected"
    ]
    if stage in {"direction_screening", "question_refinement"}:
        direction_count = len(document.get("direction_hypotheses", []))
        if direction_count < 2 or direction_count > 5:
            issues.append(
                ValidationIssue(
                    path="direction_hypotheses",
                    message="P2.A 方向阶段必须保留 2 到 5 个 DirectionHypothesis。",
                )
            )

    selection = document.get("current_selection", {})
    selected_direction_id = selection.get("selected_direction_id")
    selected_question_id = selection.get("selected_question_id")
    active_fit_mapping_id = selection.get("active_fit_mapping_id")
    active_draft_id = selection.get("active_draft_id")
    active_revision_plan_id = selection.get("active_revision_plan_id")

    if requires_direction and len(selected_directions) != 1:
        issues.append(
            ValidationIssue(
                path="direction_hypotheses",
                message="必须且只能有一个 decision_status=selected 的 DirectionHypothesis。",
            )
        )

    selected_direction = directions.get(selected_direction_id) if isinstance(selected_direction_id, str) else None
    if requires_direction and selected_direction_id is None:
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

    selected_question = questions.get(selected_question_id) if isinstance(selected_question_id, str) else None
    if requires_question and selected_question_id is None:
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

    active_argument_chain = None
    if selected_question is not None and requires_argument_chain:
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
    if requires_fit_mapping and active_fit_mapping_id is None:
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
    if requires_draft and active_draft_id is None:
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
    if requires_revision_plan and active_revision_plan_id is None:
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

def _validate_stage_requirements(
    document: dict[str, Any],
    *,
    selected_question_id: str | None,
    active_argument_chain_id: str | None,
    active_fit_mapping_id: str | None,
    active_revision_plan: dict[str, Any] | None,
    active_critique: dict[str, Any] | None,
    reviewed_revision_plan: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    stage = document.get("lifecycle_stage")
    gates = document.get("gates", {})
    selection = document.get("current_selection", {})
    active_draft = None
    active_draft_id = selection.get("active_draft_id")
    if isinstance(active_draft_id, str):
        for item in document.get("application_drafts", []):
            if isinstance(item, dict) and item.get("draft_id") == active_draft_id:
                active_draft = item
                break
    if stage in {"fit_alignment", "outline", "drafting", "critique", "revision", "frozen"}:
        for gate_name in ("direction_frozen", "scientific_question_frozen", "argument_chain_frozen"):
            if not gates.get(gate_name):
                issues.append(
                    ValidationIssue(
                        path=f"gates.{gate_name}",
                        message=f"{stage} 阶段前必须先冻结 {gate_name}。",
                    )
                )
    if stage in {"outline", "drafting", "critique", "revision", "frozen"} and not gates.get("fit_alignment_frozen"):
        issues.append(
            ValidationIssue(
                path="gates.fit_alignment_frozen",
                message=f"{stage} 阶段前必须先冻结申请人适配度映射。",
            )
        )
    if stage in {"drafting", "critique", "revision", "frozen"} and not gates.get("outline_frozen"):
        issues.append(
            ValidationIssue(
                path="gates.outline_frozen",
                message=f"{stage} 阶段前必须先冻结提纲。",
            )
        )
    if stage == "outline" and active_draft is not None and active_draft.get("status") != "outline":
        issues.append(
            ValidationIssue(
                path="application_drafts.status",
                message="outline 阶段的激活草稿 status 必须为 outline。",
            )
        )
    if stage == "drafting" and not document.get("application_drafts"):
        issues.append(
            ValidationIssue(
                path="application_drafts",
                message="drafting 阶段不能缺少 ApplicationDraft。",
            )
        )
    if stage == "drafting" and active_draft is not None and active_draft.get("status") != "draft":
        issues.append(
            ValidationIssue(
                path="application_drafts.status",
                message="drafting 阶段的激活草稿 status 必须为 draft。",
            )
        )
    if stage in {"critique", "revision", "frozen"} and not document.get("mentor_critiques"):
        issues.append(
            ValidationIssue(
                path="mentor_critiques",
                message=f"{stage} 阶段不能缺少 MentorCritique。",
            )
        )
    if stage in {"critique", "revision", "frozen"}:
        revision_items = active_revision_plan.get("items") if isinstance(active_revision_plan, dict) else None
        if not isinstance(revision_items, list) or not revision_items:
            issues.append(
                ValidationIssue(
                    path="revision_plans",
                    message=f"{stage} 阶段必须存在非空 RevisionPlan。",
                )
            )
    if stage == "frozen" and not gates.get("presubmission_frozen"):
        issues.append(
            ValidationIssue(
                path="gates.presubmission_frozen",
                message="frozen 阶段必须已经冻结 presubmission 版本。",
            )
        )
    if stage == "frozen" and active_critique is not None and active_critique.get("verdict") != "ready_for_submission":
        issues.append(
            ValidationIssue(
                path="mentor_critiques.verdict",
                message="frozen 阶段的激活批注 verdict 必须为 ready_for_submission。",
            )
        )
    if stage == "revision" and active_critique is not None and active_critique.get("verdict") not in {"major_revision", "minor_revision"}:
        issues.append(
            ValidationIssue(
                path="mentor_critiques.verdict",
                message="revision 阶段的激活批注 verdict 必须为 major_revision 或 minor_revision。",
            )
        )
    if stage in {"critique", "revision"} and active_draft is not None and active_draft.get("status") not in {"draft", "revised"}:
        issues.append(
            ValidationIssue(
                path="application_drafts.status",
                message=f"{stage} 阶段的激活草稿 status 必须为 draft 或 revised。",
            )
        )
    if stage == "frozen" and active_draft is not None and active_draft.get("status") != "frozen":
        issues.append(
            ValidationIssue(
                path="application_drafts.status",
                message="frozen 阶段的激活草稿 status 必须为 frozen。",
            )
        )
    if stage in {"drafting", "critique", "revision", "frozen"} and active_draft is not None:
        sections = active_draft.get("sections")
        if not isinstance(sections, list) or not sections:
            issues.append(
                ValidationIssue(
                    path="application_drafts.sections",
                    message=f"{stage} 阶段的激活草稿必须包含非空 sections。",
                )
            )
        else:
            if selected_question_id is not None and not _draft_sections_link_object(active_draft, selected_question_id):
                issues.append(
                    ValidationIssue(
                        path="application_drafts.sections",
                        message=f"{stage} 阶段的激活草稿 sections 必须显式链接当前 ScientificQuestionCard。",
                    )
                )
            if active_argument_chain_id is not None and not _draft_sections_link_object(active_draft, active_argument_chain_id):
                issues.append(
                    ValidationIssue(
                        path="application_drafts.sections",
                        message=f"{stage} 阶段的激活草稿 sections 必须显式链接当前 ArgumentChain。",
                    )
                )
            if active_fit_mapping_id is not None and not _draft_sections_link_object(active_draft, active_fit_mapping_id):
                issues.append(
                    ValidationIssue(
                        path="application_drafts.sections",
                        message=f"{stage} 阶段的激活草稿 sections 必须显式链接当前 ApplicantFitMapping。",
                    )
                )
    _validate_revision_transition_contract(
        stage=stage,
        active_draft=active_draft,
        active_revision_plan=active_revision_plan,
        active_critique=active_critique,
        reviewed_revision_plan=reviewed_revision_plan,
        issues=issues,
    )
    _validate_forced_rollback_contract(active_critique=active_critique, issues=issues)
    _validate_presubmission_gate_contract(
        stage=stage,
        gates=gates,
        active_draft=active_draft,
        active_revision_plan=active_revision_plan,
        active_critique=active_critique,
        issues=issues,
    )
    if active_critique is not None:
        for field, expected in (
            ("necessity_scientific_value", 60),
            ("applicant_fit", 30),
            ("feasibility", 10),
        ):
            criterion = active_critique.get(field, {})
            if criterion.get("weight") != expected:
                issues.append(
                    ValidationIssue(
                        path=f"mentor_critiques.{field}",
                        message=f"{field} 的权重必须固定为 {expected}。",
                    )
                )

def _validate_revision_transition_contract(
    *,
    stage: Any,
    active_draft: dict[str, Any] | None,
    active_revision_plan: dict[str, Any] | None,
    active_critique: dict[str, Any] | None,
    reviewed_revision_plan: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    if active_draft is None or active_revision_plan is None:
        return

    draft_status = active_draft.get("status")
    draft_version_label = active_draft.get("version_label")
    execution_status = active_revision_plan.get("execution_status", "planned")
    pre_revision_version_label = active_revision_plan.get("pre_revision_version_label")
    post_revision_version_label = active_revision_plan.get("post_revision_version_label")
    comparison_summary = active_revision_plan.get("comparison_summary")
    reviewed_revision_plan_id = active_critique.get("reviewed_revision_plan_id") if isinstance(active_critique, dict) else None
    reviewed_execution_status = None
    if isinstance(reviewed_revision_plan, dict):
        reviewed_execution_status = reviewed_revision_plan.get("execution_status", "planned")
    has_completed_reviewed_revision = reviewed_execution_status == "completed"

    if draft_status == "revised" and execution_status != "completed":
        if not (stage == "critique" and reviewed_revision_plan_id is not None and has_completed_reviewed_revision):
            issues.append(
                ValidationIssue(
                    path="revision_plans.execution_status",
                    message="激活草稿 status=revised 时，RevisionPlan.execution_status 必须为 completed。",
                )
            )

    if execution_status == "completed":
        expected_draft_status = "frozen" if stage == "frozen" else "revised"
        if draft_status != expected_draft_status:
            issues.append(
                ValidationIssue(
                    path="application_drafts.status",
                    message=(
                        "frozen 阶段的 completed revision 必须对应 status=frozen 的激活草稿。"
                        if stage == "frozen"
                        else "revision plan 已标记 completed 时，激活草稿 status 必须显式切换为 revised。"
                    ),
                )
            )

    revision_evidence = active_revision_plan if execution_status == "completed" else reviewed_revision_plan
    if not isinstance(revision_evidence, dict):
        return

    evidence_pre_revision_version_label = revision_evidence.get("pre_revision_version_label")
    evidence_post_revision_version_label = revision_evidence.get("post_revision_version_label")
    evidence_comparison_summary = revision_evidence.get("comparison_summary")

    if not isinstance(evidence_pre_revision_version_label, str) or not evidence_pre_revision_version_label:
        issues.append(
            ValidationIssue(
                path="revision_plans.pre_revision_version_label",
                message="revised 草稿必须声明 pre_revision_version_label。",
            )
        )
    if not isinstance(evidence_post_revision_version_label, str) or not evidence_post_revision_version_label:
        issues.append(
            ValidationIssue(
                path="revision_plans.post_revision_version_label",
                message="revised 草稿必须声明 post_revision_version_label。",
            )
        )
    if not isinstance(evidence_comparison_summary, str) or not evidence_comparison_summary.strip():
        issues.append(
            ValidationIssue(
                path="revision_plans.comparison_summary",
                message="revised 草稿必须提供非空 comparison_summary。",
            )
        )
    if isinstance(evidence_pre_revision_version_label, str) and isinstance(evidence_post_revision_version_label, str):
        if evidence_pre_revision_version_label == evidence_post_revision_version_label:
            issues.append(
                ValidationIssue(
                    path="revision_plans.post_revision_version_label",
                    message="post_revision_version_label 必须与 pre_revision_version_label 不同。",
                )
            )
        if draft_version_label != evidence_post_revision_version_label:
            issues.append(
                ValidationIssue(
                    path="application_drafts.version_label",
                    message="激活草稿的 version_label 必须等于 post_revision_version_label。",
                )
            )

def _validate_forced_rollback_contract(
    *,
    active_critique: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(active_critique, dict):
        return

    verdict = active_critique.get("verdict")
    forced_rollback_stage = active_critique.get("forced_rollback_stage")
    forced_rollback_reason = active_critique.get("forced_rollback_reason")

    if forced_rollback_stage is None:
        if isinstance(forced_rollback_reason, str) and forced_rollback_reason.strip():
            issues.append(
                ValidationIssue(
                    path="mentor_critiques.forced_rollback_reason",
                    message="forced_rollback_stage 缺失时不得单独提供 forced_rollback_reason。",
                )
            )
        return

    if not isinstance(forced_rollback_reason, str) or not forced_rollback_reason.strip():
        issues.append(
            ValidationIssue(
                path="mentor_critiques.forced_rollback_reason",
                message="forced_rollback_stage 存在时必须提供非空 forced_rollback_reason。",
            )
        )

    if verdict == "minor_revision":
        issues.append(
            ValidationIssue(
                path="mentor_critiques.forced_rollback_stage",
                message="minor_revision 不得携带 forced_rollback_stage。",
            )
        )
        return

    if verdict == "ready_for_submission":
        issues.append(
            ValidationIssue(
                path="mentor_critiques.forced_rollback_stage",
                message="ready_for_submission 不得携带 forced_rollback_stage。",
            )
        )
        return

    allowed_targets_by_verdict = {
        "major_reframe": {"direction_screening", "question_refinement"},
        "major_revision": {"argument_building", "fit_alignment"},
    }
    allowed_targets = allowed_targets_by_verdict.get(verdict)
    if allowed_targets is None:
        issues.append(
            ValidationIssue(
                path="mentor_critiques.forced_rollback_stage",
                message="只有 major_reframe 或 major_revision 才允许携带 forced_rollback_stage。",
            )
        )
        return

    if forced_rollback_stage not in allowed_targets:
        issues.append(
            ValidationIssue(
                path="mentor_critiques.forced_rollback_stage",
                message=(
                    "verdict=major_reframe 时 forced_rollback_stage 只能是 direction_screening 或 question_refinement。"
                    if verdict == "major_reframe"
                    else "verdict=major_revision 时 forced_rollback_stage 只能是 argument_building 或 fit_alignment。"
                ),
            )
        )

def _validate_presubmission_gate_contract(
    *,
    stage: Any,
    gates: dict[str, Any],
    active_draft: dict[str, Any] | None,
    active_revision_plan: dict[str, Any] | None,
    active_critique: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    presubmission_frozen = bool(gates.get("presubmission_frozen"))
    if stage != "frozen" and presubmission_frozen:
        issues.append(
            ValidationIssue(
                path="gates.presubmission_frozen",
                message="只有 frozen 阶段才允许将 presubmission_frozen 置为 true。",
            )
        )
        return

    if stage != "frozen" or not isinstance(active_critique, dict):
        return

    if not isinstance(active_revision_plan, dict) or active_revision_plan.get("execution_status") != "completed":
        issues.append(
            ValidationIssue(
                path="revision_plans.execution_status",
                message="frozen 阶段的激活 RevisionPlan.execution_status 必须为 completed。",
            )
        )

    if (
        isinstance(active_revision_plan, dict)
        and isinstance(active_draft, dict)
        and active_revision_plan.get("post_revision_version_label") != active_draft.get("version_label")
    ):
        issues.append(
            ValidationIssue(
                path="revision_plans.post_revision_version_label",
                message="frozen 阶段的激活 RevisionPlan.post_revision_version_label 必须等于激活草稿 version_label。",
            )
        )

    if active_critique.get("blocking_issues"):
        issues.append(
            ValidationIssue(
                path="mentor_critiques.blocking_issues",
                message="frozen 阶段的激活批注 blocking_issues 必须为空。",
            )
        )

    for field in ("necessity_scientific_value", "applicant_fit", "feasibility"):
        criterion = active_critique.get(field, {})
        if isinstance(criterion, dict) and criterion.get("blocking_issues"):
            issues.append(
                ValidationIssue(
                    path=f"mentor_critiques.{field}.blocking_issues",
                    message=f"frozen 阶段的 {field}.blocking_issues 必须为空。",
                )
            )

def _validate_reference_sets(document: dict[str, Any], issues: list[ValidationIssue]) -> None:
    known_ids = _collect_known_ids(document)
    fields_to_scan = [
        ("direction_hypotheses", "required_evidence_ids"),
        ("scientific_question_cards", "linked_evidence_ids"),
        ("argument_chains", "linked_evidence_ids"),
        ("applicant_fit_mappings", "linked_evidence_ids"),
        ("application_drafts", "outline", "linked_object_ids"),
        ("application_drafts", "sections", "linked_object_ids"),
        ("revision_plans", "items", "required_input_ids"),
        ("preliminary_evidence_pack", "evidence_items", "supports"),
    ]
    for spec in fields_to_scan:
        if len(spec) == 2:
            collection_name, field_name = spec
            for index, item in enumerate(document.get(collection_name, [])):
                if not isinstance(item, dict):
                    continue
                _validate_reference_list(
                    item.get(field_name),
                    known_ids,
                    f"{collection_name}[{index}].{field_name}",
                    issues,
                )
            continue

        parent_name, collection_name, field_name = spec
        parent = document.get(parent_name)
        if isinstance(parent, list):
            parents = parent
        elif isinstance(parent, dict):
            parents = [parent]
        else:
            parents = []
        for parent_index, parent_item in enumerate(parents):
            nested_items = parent_item.get(collection_name, []) if isinstance(parent_item, dict) else []
            for index, item in enumerate(nested_items):
                if not isinstance(item, dict):
                    continue
                _validate_reference_list(
                    item.get(field_name),
                    known_ids,
                    f"{parent_name}[{parent_index}].{collection_name}[{index}].{field_name}",
                    issues,
                )

def _validate_reference_list(
    values: Any,
    known_ids: set[str],
    path: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(values, list):
        return
    for index, ref_id in enumerate(values):
        if isinstance(ref_id, str) and ref_id not in known_ids:
            issues.append(
                ValidationIssue(
                    path=f"{path}[{index}]",
                    message="引用了不存在的对象或证据 ID。",
                )
            )

def _collect_known_ids(document: dict[str, Any]) -> set[str]:
    known_ids: set[str] = set()

    def add_id(value: Any) -> None:
        if isinstance(value, str) and value:
            known_ids.add(value)

    collections = [
        ("direction_hypotheses", "direction_id"),
        ("scientific_question_cards", "question_id"),
        ("argument_chains", "argument_chain_id"),
        ("applicant_fit_mappings", "fit_mapping_id"),
        ("application_drafts", "draft_id"),
        ("mentor_critiques", "critique_id"),
        ("revision_plans", "revision_plan_id"),
    ]
    for collection_name, key in collections:
        for item in document.get(collection_name, []):
            if isinstance(item, dict):
                add_id(item.get(key))

    for output in document.get("track_record", {}).get("representative_outputs", []):
        if isinstance(output, dict):
            add_id(output.get("output_id"))
            evidence = output.get("evidence")
            if isinstance(evidence, dict):
                add_id(evidence.get("evidence_id"))

    for project in document.get("active_project_set", {}).get("projects", []):
        if isinstance(project, dict):
            add_id(project.get("project_id"))
            for evidence in project.get("linked_evidence", []):
                if isinstance(evidence, dict):
                    add_id(evidence.get("evidence_id"))

    for evidence_item in document.get("preliminary_evidence_pack", {}).get("evidence_items", []):
        if isinstance(evidence_item, dict):
            add_id(evidence_item.get("item_id"))
            evidence = evidence_item.get("evidence")
            if isinstance(evidence, dict):
                add_id(evidence.get("evidence_id"))

    return known_ids

def _draft_links_argument_chain(draft: dict[str, Any], argument_chain_id: str) -> bool:
    for section_group in ("outline", "sections"):
        for item in draft.get(section_group, []):
            if not isinstance(item, dict):
                continue
            linked_ids = item.get("linked_object_ids", [])
            if isinstance(linked_ids, list) and argument_chain_id in linked_ids:
                return True
    return False

def _draft_links_fit_mapping(draft: dict[str, Any], fit_mapping_id: str) -> bool:
    for section_group in ("outline", "sections"):
        for item in draft.get(section_group, []):
            if not isinstance(item, dict):
                continue
            linked_ids = item.get("linked_object_ids", [])
            if isinstance(linked_ids, list) and fit_mapping_id in linked_ids:
                return True
    return False

def _draft_sections_link_object(draft: dict[str, Any], object_id: str) -> bool:
    for item in draft.get("sections", []):
        if not isinstance(item, dict):
            continue
        linked_ids = item.get("linked_object_ids", [])
        if isinstance(linked_ids, list) and object_id in linked_ids:
            return True
    return False




























__all__ = [name for name in globals() if name.startswith("_") and not name.startswith("__")]
