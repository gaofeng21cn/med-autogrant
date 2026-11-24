from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from med_autogrant.workspace_reference_validation import _draft_sections_link_object
from med_autogrant.workspace_types import ValidationIssue


class _GateRule(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    gate_name: str
    message_template: str


class _StageContractPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    required_gates: tuple[_GateRule, ...] = ()
    allowed_draft_statuses: frozenset[str] = frozenset()
    draft_status_message: str = ""
    require_application_drafts: bool = False
    require_mentor_critiques: bool = False
    require_nonempty_revision_plan_items: bool = False
    require_presubmission_frozen: bool = False
    allowed_critique_verdicts: frozenset[str] = frozenset()
    critique_verdict_message: str = ""
    require_draft_sections: bool = False


class _DraftSnapshot(BaseModel):
    model_config = ConfigDict(extra="allow")

    draft_id: Any = None
    status: Any = None
    version_label: Any = None
    sections: Any = None


class _RevisionPlanSnapshot(BaseModel):
    model_config = ConfigDict(extra="allow")

    execution_status: Any = "planned"
    items: Any = None
    pre_revision_version_label: Any = None
    post_revision_version_label: Any = None
    comparison_summary: Any = None


class _CritiqueSnapshot(BaseModel):
    model_config = ConfigDict(extra="allow")

    verdict: Any = None
    forced_rollback_stage: Any = None
    forced_rollback_reason: Any = None
    reviewed_revision_plan_id: Any = None
    blocking_issues: Any = None
    necessity_scientific_value: Any = Field(default_factory=dict)
    applicant_fit: Any = Field(default_factory=dict)
    feasibility: Any = Field(default_factory=dict)


class _ForcedRollbackRule(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    allowed_targets: frozenset[str]
    invalid_target_message: str


_CORE_GATES = (
    _GateRule(gate_name="direction_frozen", message_template="{stage} 阶段前必须先冻结 direction_frozen。"),
    _GateRule(
        gate_name="scientific_question_frozen",
        message_template="{stage} 阶段前必须先冻结 scientific_question_frozen。",
    ),
    _GateRule(
        gate_name="argument_chain_frozen",
        message_template="{stage} 阶段前必须先冻结 argument_chain_frozen。",
    ),
)
_FIT_GATE = _GateRule(
    gate_name="fit_alignment_frozen",
    message_template="{stage} 阶段前必须先冻结申请人适配度映射。",
)
_OUTLINE_GATE = _GateRule(
    gate_name="outline_frozen",
    message_template="{stage} 阶段前必须先冻结提纲。",
)

_EMPTY_STAGE_POLICY = _StageContractPolicy()
_STAGE_POLICIES: dict[str, _StageContractPolicy] = {
    "fit_alignment": _StageContractPolicy(required_gates=_CORE_GATES),
    "outline": _StageContractPolicy(
        required_gates=(*_CORE_GATES, _FIT_GATE),
        allowed_draft_statuses=frozenset({"outline"}),
        draft_status_message="outline 阶段的激活草稿 status 必须为 outline。",
    ),
    "drafting": _StageContractPolicy(
        required_gates=(*_CORE_GATES, _FIT_GATE, _OUTLINE_GATE),
        allowed_draft_statuses=frozenset({"draft"}),
        draft_status_message="drafting 阶段的激活草稿 status 必须为 draft。",
        require_application_drafts=True,
        require_draft_sections=True,
    ),
    "critique": _StageContractPolicy(
        required_gates=(*_CORE_GATES, _FIT_GATE, _OUTLINE_GATE),
        allowed_draft_statuses=frozenset({"draft", "revised"}),
        draft_status_message="critique 阶段的激活草稿 status 必须为 draft 或 revised。",
        require_mentor_critiques=True,
        require_nonempty_revision_plan_items=True,
        require_draft_sections=True,
    ),
    "revision": _StageContractPolicy(
        required_gates=(*_CORE_GATES, _FIT_GATE, _OUTLINE_GATE),
        allowed_draft_statuses=frozenset({"draft", "revised"}),
        draft_status_message="revision 阶段的激活草稿 status 必须为 draft 或 revised。",
        require_mentor_critiques=True,
        require_nonempty_revision_plan_items=True,
        allowed_critique_verdicts=frozenset({"major_revision", "minor_revision"}),
        critique_verdict_message="revision 阶段的激活批注 verdict 必须为 major_revision 或 minor_revision。",
        require_draft_sections=True,
    ),
    "frozen": _StageContractPolicy(
        required_gates=(*_CORE_GATES, _FIT_GATE, _OUTLINE_GATE),
        allowed_draft_statuses=frozenset({"frozen"}),
        draft_status_message="frozen 阶段的激活草稿 status 必须为 frozen。",
        require_mentor_critiques=True,
        require_nonempty_revision_plan_items=True,
        require_presubmission_frozen=True,
        allowed_critique_verdicts=frozenset({"ready_for_submission"}),
        critique_verdict_message="frozen 阶段的激活批注 verdict 必须为 ready_for_submission。",
        require_draft_sections=True,
    ),
}

_CRITIQUE_WEIGHT_SPEC: tuple[tuple[str, int], ...] = (
    ("necessity_scientific_value", 60),
    ("applicant_fit", 30),
    ("feasibility", 10),
)
_FORBIDDEN_ROLLBACK_VERDICTS: dict[str, str] = {
    "minor_revision": "minor_revision 不得携带 forced_rollback_stage。",
    "ready_for_submission": "ready_for_submission 不得携带 forced_rollback_stage。",
}
_FORCED_ROLLBACK_RULES: dict[str, _ForcedRollbackRule] = {
    "major_reframe": _ForcedRollbackRule(
        allowed_targets=frozenset({"direction_screening", "question_refinement"}),
        invalid_target_message="verdict=major_reframe 时 forced_rollback_stage 只能是 direction_screening 或 question_refinement。",
    ),
    "major_revision": _ForcedRollbackRule(
        allowed_targets=frozenset({"argument_building", "fit_alignment"}),
        invalid_target_message="verdict=major_revision 时 forced_rollback_stage 只能是 argument_building 或 fit_alignment。",
    ),
}


def _find_active_draft(document: dict[str, Any], selection: dict[str, Any]) -> dict[str, Any] | None:
    active_draft_id = selection.get("active_draft_id")
    if not isinstance(active_draft_id, str):
        return None
    for item in document.get("application_drafts", []):
        if isinstance(item, dict) and item.get("draft_id") == active_draft_id:
            return item
    return None


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
    gates = document.get("gates") if isinstance(document.get("gates"), dict) else {}
    selection = document.get("current_selection") if isinstance(document.get("current_selection"), dict) else {}
    active_draft_raw = _find_active_draft(document, selection)
    policy = _STAGE_POLICIES.get(stage, _EMPTY_STAGE_POLICY) if isinstance(stage, str) else _EMPTY_STAGE_POLICY

    draft_view = _DraftSnapshot.model_validate(active_draft_raw) if isinstance(active_draft_raw, dict) else None
    revision_view = (
        _RevisionPlanSnapshot.model_validate(active_revision_plan)
        if isinstance(active_revision_plan, dict)
        else None
    )
    reviewed_view = (
        _RevisionPlanSnapshot.model_validate(reviewed_revision_plan)
        if isinstance(reviewed_revision_plan, dict)
        else None
    )
    critique_view = (
        _CritiqueSnapshot.model_validate(active_critique)
        if isinstance(active_critique, dict)
        else None
    )

    for rule in policy.required_gates:
        if not gates.get(rule.gate_name):
            issues.append(
                ValidationIssue(
                    path=f"gates.{rule.gate_name}",
                    message=rule.message_template.format(stage=stage),
                )
            )

    _validate_stage_material_requirements(
        document=document,
        stage=stage,
        policy=policy,
        gates=gates,
        draft_view=draft_view,
        revision_view=revision_view,
        critique_view=critique_view,
        issues=issues,
    )
    if policy.require_draft_sections and active_draft_raw is not None and draft_view is not None:
        _validate_active_draft_sections(
            stage=stage,
            active_draft=active_draft_raw,
            draft_view=draft_view,
            selected_question_id=selected_question_id,
            active_argument_chain_id=active_argument_chain_id,
            active_fit_mapping_id=active_fit_mapping_id,
            issues=issues,
        )
    if draft_view is not None and revision_view is not None:
        _validate_revision_transition_contract(
            stage=stage,
            draft_view=draft_view,
            revision_view=revision_view,
            critique_view=critique_view,
            reviewed_view=reviewed_view,
            issues=issues,
        )
    if critique_view is not None:
        _validate_forced_rollback_contract(critique_view=critique_view, issues=issues)
    _validate_presubmission_gate_contract(
        stage=stage,
        gates=gates,
        draft_view=draft_view,
        revision_view=revision_view,
        critique_view=critique_view,
        issues=issues,
    )
    if critique_view is not None:
        _validate_critique_weight_contract(critique_view=critique_view, issues=issues)


def _validate_stage_material_requirements(
    *,
    document: dict[str, Any],
    stage: Any,
    policy: _StageContractPolicy,
    gates: dict[str, Any],
    draft_view: _DraftSnapshot | None,
    revision_view: _RevisionPlanSnapshot | None,
    critique_view: _CritiqueSnapshot | None,
    issues: list[ValidationIssue],
) -> None:
    if policy.require_application_drafts and not document.get("application_drafts"):
        issues.append(
            ValidationIssue(
                path="application_drafts",
                message="drafting 阶段不能缺少 ApplicationDraft。",
            )
        )
    if policy.require_mentor_critiques and not document.get("mentor_critiques"):
        issues.append(
            ValidationIssue(
                path="mentor_critiques",
                message=f"{stage} 阶段不能缺少 MentorCritique。",
            )
        )
    if policy.require_nonempty_revision_plan_items:
        revision_items = revision_view.items if revision_view is not None else None
        if not isinstance(revision_items, list) or not revision_items:
            issues.append(
                ValidationIssue(
                    path="revision_plans",
                    message=f"{stage} 阶段必须存在非空 RevisionPlan。",
                )
            )
    if policy.require_presubmission_frozen and not gates.get("presubmission_frozen"):
        issues.append(
            ValidationIssue(
                path="gates.presubmission_frozen",
                message="frozen 阶段必须已经冻结 presubmission 版本。",
            )
        )
    if (
        policy.allowed_critique_verdicts
        and critique_view is not None
        and critique_view.verdict not in policy.allowed_critique_verdicts
    ):
        issues.append(
            ValidationIssue(
                path="mentor_critiques.verdict",
                message=policy.critique_verdict_message,
            )
        )
    if (
        policy.allowed_draft_statuses
        and draft_view is not None
        and draft_view.status not in policy.allowed_draft_statuses
    ):
        issues.append(
            ValidationIssue(
                path="application_drafts.status",
                message=policy.draft_status_message,
            )
        )


def _validate_active_draft_sections(
    *,
    stage: Any,
    active_draft: dict[str, Any],
    draft_view: _DraftSnapshot,
    selected_question_id: str | None,
    active_argument_chain_id: str | None,
    active_fit_mapping_id: str | None,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(draft_view.sections, list) or not draft_view.sections:
        issues.append(
            ValidationIssue(
                path="application_drafts.sections",
                message=f"{stage} 阶段的激活草稿必须包含非空 sections。",
            )
        )
        return
    for object_id, label in (
        (selected_question_id, "ScientificQuestionCard"),
        (active_argument_chain_id, "ArgumentChain"),
        (active_fit_mapping_id, "ApplicantFitMapping"),
    ):
        if object_id is not None and not _draft_sections_link_object(active_draft, object_id):
            issues.append(
                ValidationIssue(
                    path="application_drafts.sections",
                    message=f"{stage} 阶段的激活草稿 sections 必须显式链接当前 {label}。",
                )
            )


def _validate_critique_weight_contract(
    *,
    critique_view: _CritiqueSnapshot,
    issues: list[ValidationIssue],
) -> None:
    for field, expected in _CRITIQUE_WEIGHT_SPEC:
        criterion = getattr(critique_view, field)
        weight = criterion.get("weight") if isinstance(criterion, dict) else None
        if weight != expected:
            issues.append(
                ValidationIssue(
                    path=f"mentor_critiques.{field}",
                    message=f"{field} 的权重必须固定为 {expected}。",
                )
            )


def _validate_revision_transition_contract(
    *,
    stage: Any,
    draft_view: _DraftSnapshot,
    revision_view: _RevisionPlanSnapshot,
    critique_view: _CritiqueSnapshot | None,
    reviewed_view: _RevisionPlanSnapshot | None,
    issues: list[ValidationIssue],
) -> None:
    draft_status = draft_view.status
    draft_version_label = draft_view.version_label
    execution_status = revision_view.execution_status
    reviewed_revision_plan_id = critique_view.reviewed_revision_plan_id if critique_view is not None else None
    has_completed_reviewed_revision = (
        reviewed_view is not None and reviewed_view.execution_status == "completed"
    )

    if (
        draft_status == "revised"
        and execution_status != "completed"
        and not (stage == "critique" and reviewed_revision_plan_id is not None and has_completed_reviewed_revision)
    ):
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

    evidence = revision_view if execution_status == "completed" else reviewed_view
    if evidence is None:
        return

    pre_label = evidence.pre_revision_version_label
    post_label = evidence.post_revision_version_label
    summary = evidence.comparison_summary

    if not isinstance(pre_label, str) or not pre_label:
        issues.append(
            ValidationIssue(
                path="revision_plans.pre_revision_version_label",
                message="revised 草稿必须声明 pre_revision_version_label。",
            )
        )
    if not isinstance(post_label, str) or not post_label:
        issues.append(
            ValidationIssue(
                path="revision_plans.post_revision_version_label",
                message="revised 草稿必须声明 post_revision_version_label。",
            )
        )
    if not isinstance(summary, str) or not summary.strip():
        issues.append(
            ValidationIssue(
                path="revision_plans.comparison_summary",
                message="revised 草稿必须提供非空 comparison_summary。",
            )
        )
    if isinstance(pre_label, str) and isinstance(post_label, str):
        if pre_label == post_label:
            issues.append(
                ValidationIssue(
                    path="revision_plans.post_revision_version_label",
                    message="post_revision_version_label 必须与 pre_revision_version_label 不同。",
                )
            )
        if draft_version_label != post_label:
            issues.append(
                ValidationIssue(
                    path="application_drafts.version_label",
                    message="激活草稿的 version_label 必须等于 post_revision_version_label。",
                )
            )


def _validate_forced_rollback_contract(
    *,
    critique_view: _CritiqueSnapshot,
    issues: list[ValidationIssue],
) -> None:
    verdict = critique_view.verdict
    rollback_stage = critique_view.forced_rollback_stage
    rollback_reason = critique_view.forced_rollback_reason

    if rollback_stage is None:
        if isinstance(rollback_reason, str) and rollback_reason.strip():
            issues.append(
                ValidationIssue(
                    path="mentor_critiques.forced_rollback_reason",
                    message="forced_rollback_stage 缺失时不得单独提供 forced_rollback_reason。",
                )
            )
        return

    if not isinstance(rollback_reason, str) or not rollback_reason.strip():
        issues.append(
            ValidationIssue(
                path="mentor_critiques.forced_rollback_reason",
                message="forced_rollback_stage 存在时必须提供非空 forced_rollback_reason。",
            )
        )

    if isinstance(verdict, str) and verdict in _FORBIDDEN_ROLLBACK_VERDICTS:
        issues.append(
            ValidationIssue(
                path="mentor_critiques.forced_rollback_stage",
                message=_FORBIDDEN_ROLLBACK_VERDICTS[verdict],
            )
        )
        return

    rule = _FORCED_ROLLBACK_RULES.get(verdict) if isinstance(verdict, str) else None
    if rule is None:
        issues.append(
            ValidationIssue(
                path="mentor_critiques.forced_rollback_stage",
                message="只有 major_reframe 或 major_revision 才允许携带 forced_rollback_stage。",
            )
        )
        return

    if rollback_stage not in rule.allowed_targets:
        issues.append(
            ValidationIssue(
                path="mentor_critiques.forced_rollback_stage",
                message=rule.invalid_target_message,
            )
        )


def _validate_presubmission_gate_contract(
    *,
    stage: Any,
    gates: dict[str, Any],
    draft_view: _DraftSnapshot | None,
    revision_view: _RevisionPlanSnapshot | None,
    critique_view: _CritiqueSnapshot | None,
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

    if stage != "frozen" or critique_view is None:
        return

    if revision_view is None or revision_view.execution_status != "completed":
        issues.append(
            ValidationIssue(
                path="revision_plans.execution_status",
                message="frozen 阶段的激活 RevisionPlan.execution_status 必须为 completed。",
            )
        )

    if (
        revision_view is not None
        and draft_view is not None
        and revision_view.post_revision_version_label != draft_view.version_label
    ):
        issues.append(
            ValidationIssue(
                path="revision_plans.post_revision_version_label",
                message="frozen 阶段的激活 RevisionPlan.post_revision_version_label 必须等于激活草稿 version_label。",
            )
        )

    if critique_view.blocking_issues:
        issues.append(
            ValidationIssue(
                path="mentor_critiques.blocking_issues",
                message="frozen 阶段的激活批注 blocking_issues 必须为空。",
            )
        )

    for field, _ in _CRITIQUE_WEIGHT_SPEC:
        criterion = getattr(critique_view, field)
        if isinstance(criterion, dict) and criterion.get("blocking_issues"):
            issues.append(
                ValidationIssue(
                    path=f"mentor_critiques.{field}.blocking_issues",
                    message=f"frozen 阶段的 {field}.blocking_issues 必须为空。",
                )
            )
