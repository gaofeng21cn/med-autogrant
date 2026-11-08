from __future__ import annotations

from typing import Any

from med_autogrant.workspace_reference_validation import _draft_sections_link_object
from med_autogrant.workspace_types import ValidationIssue

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
    active_draft = _find_active_draft(document, selection)

    _validate_stage_gate_prerequisites(stage=stage, gates=gates, issues=issues)
    _validate_stage_material_requirements(
        document=document,
        stage=stage,
        gates=gates,
        active_draft=active_draft,
        active_revision_plan=active_revision_plan,
        active_critique=active_critique,
        issues=issues,
    )
    _validate_active_draft_sections(
        stage=stage,
        active_draft=active_draft,
        selected_question_id=selected_question_id,
        active_argument_chain_id=active_argument_chain_id,
        active_fit_mapping_id=active_fit_mapping_id,
        issues=issues,
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
        _validate_critique_weight_contract(active_critique=active_critique, issues=issues)


def _find_active_draft(document: dict[str, Any], selection: dict[str, Any]) -> dict[str, Any] | None:
    active_draft_id = selection.get("active_draft_id")
    if not isinstance(active_draft_id, str):
        return None
    for item in document.get("application_drafts", []):
        if isinstance(item, dict) and item.get("draft_id") == active_draft_id:
            return item
    return None


def _validate_stage_gate_prerequisites(
    *,
    stage: Any,
    gates: dict[str, Any],
    issues: list[ValidationIssue],
) -> None:
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


def _validate_stage_material_requirements(
    *,
    document: dict[str, Any],
    stage: Any,
    gates: dict[str, Any],
    active_draft: dict[str, Any] | None,
    active_revision_plan: dict[str, Any] | None,
    active_critique: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
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


def _validate_active_draft_sections(
    *,
    stage: Any,
    active_draft: dict[str, Any] | None,
    selected_question_id: str | None,
    active_argument_chain_id: str | None,
    active_fit_mapping_id: str | None,
    issues: list[ValidationIssue],
) -> None:
    if stage not in {"drafting", "critique", "revision", "frozen"} or active_draft is None:
        return
    sections = active_draft.get("sections")
    if not isinstance(sections, list) or not sections:
        issues.append(
            ValidationIssue(
                path="application_drafts.sections",
                message=f"{stage} 阶段的激活草稿必须包含非空 sections。",
            )
        )
        return
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


def _validate_critique_weight_contract(
    *,
    active_critique: dict[str, Any],
    issues: list[ValidationIssue],
) -> None:
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
