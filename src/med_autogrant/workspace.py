from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from med_autogrant.schema_loader import SchemaStore


class WorkspaceError(Exception):
    """Workspace 相关错误。"""


class WorkspaceFileError(WorkspaceError):
    """Workspace 文件读写错误。"""


class WorkspaceStateError(WorkspaceError):
    """Workspace 状态不满足运行时约束。"""

    def __init__(
        self,
        message: str,
        *,
        errors: list[ValidationIssue] | None = None,
        grant_run_id: str | None = None,
        workspace_id: str | None = None,
        lifecycle_stage: str | None = None,
    ) -> None:
        super().__init__(message)
        self.errors = list(errors or [])
        self.grant_run_id = grant_run_id
        self.workspace_id = workspace_id
        self.lifecycle_stage = lifecycle_stage


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    errors: list[ValidationIssue]

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def error_count(self) -> int:
        return len(self.errors)

    def to_dict(self, document: dict[str, Any] | None = None) -> dict[str, Any]:
        grant_run_id = None
        workspace_id = None
        lifecycle_stage = None
        if isinstance(document, dict):
            grant_run_id = document.get("grant_run_id")
            workspace_id = document.get("workspace_id")
            lifecycle_stage = document.get("lifecycle_stage")
        return {
            "ok": self.ok,
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
            "error_count": self.error_count,
            "errors": [
                {
                    "path": issue.path,
                    "message": issue.message,
                }
                for issue in self.errors
            ],
        }


@dataclass(frozen=True)
class WorkspaceContext:
    document: dict[str, Any]
    selected_direction: dict[str, Any]
    selected_question: dict[str, Any]
    active_argument_chain: dict[str, Any]
    active_fit_mapping: dict[str, Any]
    active_draft: dict[str, Any]
    active_revision_plan: dict[str, Any]
    active_critique: dict[str, Any]
    reviewed_revision_plan: dict[str, Any] | None


@dataclass(frozen=True)
class WorkspaceState:
    document: dict[str, Any]
    current_selection: dict[str, Any]
    selected_direction: dict[str, Any] | None
    selected_question: dict[str, Any] | None
    active_argument_chain: dict[str, Any] | None
    active_fit_mapping: dict[str, Any] | None
    active_draft: dict[str, Any] | None
    active_revision_plan: dict[str, Any] | None
    active_critique: dict[str, Any] | None
    reviewed_revision_plan: dict[str, Any] | None


_EVIDENCE_TRUST_LEVELS: tuple[str, ...] = (
    "trusted",
    "usable_with_verification",
    "reference_only",
    "stale_or_conflicting",
    "missing_context",
)
_EVIDENCE_TRUST_RANK: dict[str, int] = {
    trust_level: index + 1 for index, trust_level in enumerate(_EVIDENCE_TRUST_LEVELS)
}


def load_workspace_document(path: str | Path) -> dict[str, Any]:
    workspace_path = Path(path)
    try:
        payload = json.loads(workspace_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 workspace 文件: {workspace_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"workspace JSON 解析失败: {workspace_path}") from exc
    if not isinstance(payload, dict):
        raise WorkspaceFileError("workspace 顶层必须是 JSON object。")
    return payload


def validate_workspace_document(document: dict[str, Any]) -> ValidationResult:
    issues: list[ValidationIssue] = []
    issues.extend(_validate_schema(document))
    if not issues:
        issues.extend(_validate_runtime_constraints(document))
    return ValidationResult(errors=issues)


def _build_project_profile_summary(document: dict[str, Any]) -> dict[str, Any]:
    project_profile = document["project_profile"]
    template_profile = project_profile["template_profile"]
    collaboration_preferences = project_profile["collaboration_preferences"]
    critique_policy = project_profile["critique_policy"]
    funding_brief = document["funding_opportunity_brief"]
    summary = {
        "profile_id": project_profile["profile_id"],
        "preset_id": project_profile["preset_id"],
        "profile_label": project_profile["profile_label"],
        "project_kind": project_profile["project_kind"],
        "template_family": project_profile["template_family"],
        "selection_mode": project_profile["selection_mode"],
        "summary": project_profile["summary"],
        "funding_program": funding_brief["brief_id"],
        "funder": funding_brief["funder"],
        "program_family": funding_brief["program_family"],
        "template_id": template_profile["template_id"],
        "template_label": template_profile["template_label"],
        "collaboration_mode": collaboration_preferences["collaboration_mode"],
        "author_touchpoints": list(collaboration_preferences.get("author_touchpoints", [])),
        "evidence_policy": collaboration_preferences["evidence_policy"],
        "drafting_voice": collaboration_preferences["drafting_voice"],
        "critique_policy_preset_id": critique_policy["preset_id"],
        "critique_policy_id": critique_policy["policy_id"],
    }
    family_trace = project_profile.get("family_grammar_trace")
    if isinstance(family_trace, dict):
        summary["family_grammar_trace"] = copy.deepcopy(family_trace)
    family_grammar = project_profile.get("grant_family_grammar")
    if isinstance(family_grammar, dict):
        summary["grant_family_grammar"] = copy.deepcopy(family_grammar)
    elif isinstance(family_trace, dict):
        summary["grant_family_grammar"] = {
            "family_id": family_trace["family_id"],
            "family_label": family_trace["family_label"],
            "funder": family_trace["funder"],
            "admission_status": family_trace["admission_status"],
            "template_strategy": copy.deepcopy(family_trace["template_strategy"]),
            "review_grammar": copy.deepcopy(family_trace["review_grammar"]),
            "evidence_policy": copy.deepcopy(family_trace["evidence_policy"]),
            "family_compatibility_hooks": copy.deepcopy(family_trace["family_compatibility_hooks"]),
            "governance_entry_points": [
                "grant-quality-scorecard",
                "grant-quality-diff",
                "execute-grant-autonomy-controller",
            ],
        }
    return summary


def summarize_workspace_document(document: dict[str, Any]) -> dict[str, Any]:
    state = _build_workspace_state(document)
    grant_intake_audit = build_grant_intake_audit(document)
    grant_evidence_grounding = build_grant_evidence_grounding(document)
    project_profile_summary = _build_project_profile_summary(document)
    return {
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "mode": document["mode"],
        "lifecycle_stage": document["lifecycle_stage"],
        "gates": dict(document["gates"]),
        "project_profile": project_profile_summary,
        "current_selection": {
            "selected_direction_id": state.current_selection.get("selected_direction_id"),
            "selected_question_id": state.current_selection.get("selected_question_id"),
            "active_fit_mapping_id": state.current_selection.get("active_fit_mapping_id"),
            "active_draft_id": state.current_selection.get("active_draft_id"),
            "active_revision_plan_id": state.current_selection.get("active_revision_plan_id"),
        },
        "intake_snapshot": {
            "applicant_id": document["applicant_profile"]["applicant_id"],
            "applicant_name": document["applicant_profile"]["applicant_name"],
            "project_profile_id": project_profile_summary["profile_id"],
            "project_profile_preset_id": project_profile_summary["preset_id"],
            "project_profile_label": project_profile_summary["profile_label"],
            "representative_output_count": len(document["track_record"].get("representative_outputs", [])),
            "active_project_count": len(document["active_project_set"].get("projects", [])),
            "preliminary_evidence_count": len(document["preliminary_evidence_pack"].get("evidence_items", [])),
            "funding_program": document["funding_opportunity_brief"]["brief_id"],
        },
        "grant_intake_audit": grant_intake_audit,
        "grant_evidence_grounding": grant_evidence_grounding,
        "direction_hypotheses": {
            "count": len(document.get("direction_hypotheses", [])),
            "selected_direction_id": state.current_selection.get("selected_direction_id"),
        },
        "scientific_question_cards": {
            "count": len(document.get("scientific_question_cards", [])),
            "selected_question_id": state.current_selection.get("selected_question_id"),
        },
        "selected_direction": _serialize_direction(state.selected_direction),
        "selected_question": _serialize_question(state.selected_question),
        "active_argument_chain": _serialize_argument_chain(state.active_argument_chain),
        "active_fit_mapping": _serialize_fit_mapping(state.active_fit_mapping),
        "active_draft": _serialize_draft(state.active_draft),
        "active_revision_plan": _serialize_revision_plan(state.active_revision_plan),
        "active_critique": _serialize_critique(state.active_critique),
        "reviewed_revision_evidence": _serialize_reviewed_revision_evidence(state.reviewed_revision_plan),
    }


def build_grant_intake_audit(document: dict[str, Any]) -> dict[str, Any]:
    workspace_id = document["workspace_id"]
    grant_run_id = document["grant_run_id"]
    lifecycle_stage = document["lifecycle_stage"]
    project_profile_summary = _build_project_profile_summary(document)

    representative_outputs = document["track_record"].get("representative_outputs", [])
    active_projects = document["active_project_set"].get("projects", [])
    preliminary_items = document["preliminary_evidence_pack"].get("evidence_items", [])
    mandatory_sections = document["funding_opportunity_brief"].get("mandatory_sections", [])

    blocking_gaps: list[str] = []
    if not representative_outputs:
        blocking_gaps.append("缺少可直接回指申请人基础的代表性成果。")
    if not active_projects:
        blocking_gaps.append("缺少可直接支撑当前申请的在研项目与资源锚点。")
    if not preliminary_items:
        blocking_gaps.append("缺少可支撑方向筛选的前期证据。")
    if not mandatory_sections:
        blocking_gaps.append("FundingOpportunityBrief 缺少 mandatory_sections。")

    evidence_entries = _collect_trust_ranked_evidence(document)
    trust_summary = {
        trust_level: sum(1 for item in evidence_entries if item["trust_level"] == trust_level)
        for trust_level in _EVIDENCE_TRUST_LEVELS
    }

    intake_sections = [
        _build_intake_section(
            workspace_id=workspace_id,
            section_id="applicant_profile",
            status="ready",
            trust_level="trusted",
            summary="申请人身份、研究方向与方法栈已具备基础 framing 条件。",
        ),
        _build_intake_section(
            workspace_id=workspace_id,
            section_id="project_profile",
            status="ready",
            trust_level="trusted",
            summary=(
                f"当前采用 {project_profile_summary['profile_label']}，模板为 "
                f"{project_profile_summary['template_label']}，批注口径为 "
                f"{project_profile_summary['critique_policy_id']}。"
            ),
        ),
        _build_intake_section(
            workspace_id=workspace_id,
            section_id="track_record",
            status="ready" if representative_outputs else "needs_completion",
            trust_level="trusted" if representative_outputs else "missing_context",
            summary=(
                f"已绑定 {len(representative_outputs)} 条代表性成果，可回指申请人前期积累。"
                if representative_outputs
                else "尚未绑定可直接回指当前申请的代表性成果。"
            ),
            missing_items=[] if representative_outputs else ["representative_outputs"],
        ),
        _build_intake_section(
            workspace_id=workspace_id,
            section_id="active_project_set",
            status="ready" if active_projects else "needs_completion",
            trust_level="trusted" if active_projects else "missing_context",
            summary=(
                f"已绑定 {len(active_projects)} 个在研项目/资源锚点。"
                if active_projects
                else "尚未绑定可复用的在研项目或资源。"
            ),
            missing_items=[] if active_projects else ["projects"],
        ),
        _build_intake_section(
            workspace_id=workspace_id,
            section_id="preliminary_evidence_pack",
            status="ready" if preliminary_items else "needs_completion",
            trust_level=(
                _trust_level_from_preliminary_item(preliminary_items[0]) if preliminary_items else "missing_context"
            ),
            summary=(
                f"已绑定 {len(preliminary_items)} 条前期证据，可进入方向筛选。"
                if preliminary_items
                else "尚未形成可用于方向筛选的前期证据。"
            ),
            missing_items=[] if preliminary_items else ["evidence_items"],
        ),
        _build_intake_section(
            workspace_id=workspace_id,
            section_id="funding_opportunity_brief",
            status="ready" if mandatory_sections else "needs_completion",
            trust_level="trusted" if mandatory_sections else "missing_context",
            summary=(
                f"已冻结 {len(mandatory_sections)} 项申报硬约束。"
                if mandatory_sections
                else "FundingOpportunityBrief 尚未冻结 mandatory_sections。"
            ),
            missing_items=[] if mandatory_sections else ["mandatory_sections"],
        ),
    ]

    overall_readiness = "ready_for_direction_screening" if not blocking_gaps else "needs_intake_completion"
    readiness_summary = (
        "intake 已具备方向筛选与证据 grounding 的最小闭环。"
        if overall_readiness == "ready_for_direction_screening"
        else "intake 仍有关键缺口，需先补齐基础材料再进入方向筛选。"
    )
    readiness = {
        "applicant_profile_ready": True,
        "project_profile_ready": True,
        "track_record_ready": bool(representative_outputs),
        "active_project_set_ready": bool(active_projects),
        "preliminary_evidence_ready": bool(preliminary_items),
        "funding_opportunity_ready": bool(mandatory_sections),
        "ready_for_direction_screening": overall_readiness == "ready_for_direction_screening",
    }
    return {
        "surface_kind": "grant_intake_audit",
        "audit_kind": "grant_intake_audit",
        "audit_version": 1,
        "workspace_surface_kind": "nsfc_workspace",
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "applicant_profile_id": document["applicant_profile"]["applicant_id"],
        "project_profile_id": project_profile_summary["profile_id"],
        "track_record_id": document["track_record"]["track_record_id"],
        "active_project_set_id": document["active_project_set"]["project_set_id"],
        "preliminary_evidence_pack_id": document["preliminary_evidence_pack"]["evidence_pack_id"],
        "funding_opportunity_id": document["funding_opportunity_brief"]["brief_id"],
        "project_profile_summary": project_profile_summary,
        "intake_status": "ready" if readiness["ready_for_direction_screening"] else "needs_completion",
        "inventory": {
            "representative_output_count": len(representative_outputs),
            "active_project_count": len(active_projects),
            "preliminary_evidence_count": len(preliminary_items),
            "primary_evidence_count": len(_collect_primary_evidence_ids(document)),
        },
        "readiness": readiness,
        "summary": readiness_summary,
        "overall_readiness": overall_readiness,
        "blocking_gaps": blocking_gaps,
        "trust_summary": trust_summary,
        "intake_sections": intake_sections,
    }


def build_grant_evidence_grounding(document: dict[str, Any]) -> dict[str, Any]:
    grant_run_id = document["grant_run_id"]
    workspace_id = document["workspace_id"]
    lifecycle_stage = document["lifecycle_stage"]
    funding_program = document["funding_opportunity_brief"]["brief_id"]
    project_profile_summary = _build_project_profile_summary(document)
    evidence_entries = _collect_trust_ranked_evidence(document)
    selection_context = _selection_context(document)

    evidence_gaps: list[str] = []
    if not any(item["source_type"] == "publication" for item in evidence_entries):
        evidence_gaps.append("缺少可直接代表申请人积累的 publication 级证据。")
    if not any(item["source_type"] == "project" for item in evidence_entries):
        evidence_gaps.append("缺少可直接约束技术路线的 project 级证据。")
    if not any(item["source_type"] == "preliminary_result" for item in evidence_entries):
        evidence_gaps.append("缺少可直接锚定科学问题的前期结果证据。")

    ready_for_direction_screening = not evidence_gaps
    has_selection_context = any(value is not None for value in selection_context.values())
    if ready_for_direction_screening:
        grounding_status = "selection_grounded" if has_selection_context else "intake_grounded"
    else:
        grounding_status = "grounding_incomplete"
    summary = (
        "证据 grounding 已能同时支撑科学问题、申请人适配度与技术路线三条主线。"
        if ready_for_direction_screening
        else "证据 grounding 仍不完整，尚未同时覆盖科学问题、申请人适配度与技术路线。"
    )
    return {
        "surface_kind": "grant_evidence_grounding",
        "grounding_kind": "grant_evidence_grounding",
        "grounding_version": 1,
        "workspace_surface_kind": "nsfc_workspace",
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "scope_kind": "grant_route_scope",
        "funding_program": funding_program,
        "project_profile_summary": project_profile_summary,
        "summary": summary,
        "grounding_status": grounding_status,
        "ready_for_direction_screening": ready_for_direction_screening,
        "selection_context": selection_context,
        "evidence_inventory": {
            "representative_output_evidence_ids": _track_record_evidence_ids(document),
            "active_project_evidence_ids": _active_project_evidence_ids(document),
            "preliminary_evidence_ids": _preliminary_evidence_ids(document),
            "preliminary_evidence_item_ids": _preliminary_evidence_item_ids(document),
            "primary_evidence_ids": _collect_primary_evidence_ids(document),
        },
        "selection_evidence_map": {
            "selected_direction_evidence_ids": _selected_direction_evidence_ids(document, selection_context),
            "selected_question_evidence_ids": _selected_question_evidence_ids(document, selection_context),
            "active_argument_chain_evidence_ids": _active_argument_chain_evidence_ids(document, selection_context),
            "active_fit_mapping_evidence_ids": _active_fit_mapping_evidence_ids(document, selection_context),
        },
        "trust_ranked_evidence": evidence_entries,
        "evidence_gaps": evidence_gaps,
    }


def materialize_workspace_surfaces(document: dict[str, Any]) -> dict[str, Any]:
    document["grant_intake_audit"] = build_grant_intake_audit(document)
    document["grant_evidence_grounding"] = build_grant_evidence_grounding(document)
    return document


def build_critique_summary(document: dict[str, Any]) -> dict[str, Any]:
    context = _require_workspace_context(document)
    critique = context.active_critique
    revision_plan = context.active_revision_plan
    draft = context.active_draft
    return {
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "mode": document["mode"],
        "lifecycle_stage": document["lifecycle_stage"],
        "selected_direction_id": context.selected_direction["direction_id"],
        "selected_question_id": context.selected_question["question_id"],
        "draft_id": critique["draft_id"],
        "draft_status": draft["status"],
        "draft_version_label": draft["version_label"],
        "critique_id": critique["critique_id"],
        "reviewed_revision_plan_id": critique.get("reviewed_revision_plan_id"),
        "revision_plan_id": revision_plan["revision_plan_id"],
        "execution_status": revision_plan.get("execution_status", "planned"),
        "pre_revision_version_label": revision_plan.get("pre_revision_version_label"),
        "post_revision_version_label": revision_plan.get("post_revision_version_label"),
        "comparison_summary": revision_plan.get("comparison_summary"),
        "reviewed_revision_evidence": _serialize_reviewed_revision_evidence(context.reviewed_revision_plan),
        "overall_diagnosis": critique["overall_diagnosis"],
        "current_scientific_question": critique["current_scientific_question"],
        "suggested_question": critique["suggested_question"],
        "verdict": critique["verdict"],
        "forced_rollback_stage": critique.get("forced_rollback_stage"),
        "forced_rollback_reason": critique.get("forced_rollback_reason"),
        "presubmission_frozen": bool(document["gates"].get("presubmission_frozen")),
        "necessity_scientific_value": dict(critique["necessity_scientific_value"]),
        "applicant_fit": dict(critique["applicant_fit"]),
        "feasibility": dict(critique["feasibility"]),
        "blocking_issues": list(critique.get("blocking_issues", [])),
        "logic_chain_repairs": list(critique.get("logic_chain_repairs", [])),
        "applicant_fit_repairs": list(critique.get("applicant_fit_repairs", [])),
        "next_review_focus": list(revision_plan.get("next_review_focus", [])),
    }


def _validate_schema(document: dict[str, Any]) -> list[ValidationIssue]:
    validator = _SchemaSubsetValidator(SchemaStore())
    return validator.validate(document, "nsfc-workspace.schema.json")


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


def _build_workspace_state(document: dict[str, Any]) -> WorkspaceState:
    result = validate_workspace_document(document)
    if not result.ok:
        first = result.errors[0]
        raise WorkspaceStateError(
            f"{first.path}: {first.message}",
            errors=result.errors,
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    selection = document["current_selection"]
    direction_by_id = {item["direction_id"]: item for item in document.get("direction_hypotheses", []) if isinstance(item, dict)}
    question_by_id = {item["question_id"]: item for item in document.get("scientific_question_cards", []) if isinstance(item, dict)}
    fit_mapping_by_id = {
        item["fit_mapping_id"]: item for item in document.get("applicant_fit_mappings", []) if isinstance(item, dict)
    }
    draft_by_id = {item["draft_id"]: item for item in document.get("application_drafts", []) if isinstance(item, dict)}
    critique_by_id = {item["critique_id"]: item for item in document.get("mentor_critiques", []) if isinstance(item, dict)}
    revision_plan_by_id = {item["revision_plan_id"]: item for item in document.get("revision_plans", []) if isinstance(item, dict)}

    selected_direction = direction_by_id.get(selection.get("selected_direction_id"))
    selected_question = question_by_id.get(selection.get("selected_question_id"))
    active_fit_mapping = fit_mapping_by_id.get(selection.get("active_fit_mapping_id"))
    active_draft = draft_by_id.get(selection.get("active_draft_id"))
    active_revision_plan = revision_plan_by_id.get(selection.get("active_revision_plan_id"))
    active_critique = None
    reviewed_revision_plan = None
    if active_revision_plan is not None:
        active_critique = critique_by_id.get(active_revision_plan.get("critique_id"))
        if active_critique is not None:
            reviewed_revision_plan = revision_plan_by_id.get(active_critique.get("reviewed_revision_plan_id"))

    active_argument_chain = None
    if selected_question is not None:
        active_argument_chain = next(
            (
                item
                for item in document.get("argument_chains", [])
                if isinstance(item, dict) and item.get("scientific_question_id") == selected_question["question_id"]
            ),
            None,
        )

    return WorkspaceState(
        document=document,
        current_selection=selection,
        selected_direction=selected_direction,
        selected_question=selected_question,
        active_argument_chain=active_argument_chain,
        active_fit_mapping=active_fit_mapping,
        active_draft=active_draft,
        active_revision_plan=active_revision_plan,
        active_critique=active_critique,
        reviewed_revision_plan=reviewed_revision_plan,
    )


def _serialize_direction(direction: dict[str, Any] | None) -> dict[str, Any] | None:
    if direction is None:
        return None
    return {
        "id": direction["direction_id"],
        "title": direction["title"],
        "decision_status": direction["decision_status"],
    }


def _serialize_question(question: dict[str, Any] | None) -> dict[str, Any] | None:
    if question is None:
        return None
    return {
        "id": question["question_id"],
        "core_question": question["core_question"],
        "knowledge_boundary": question["knowledge_boundary"],
    }


def _serialize_argument_chain(argument_chain: dict[str, Any] | None) -> dict[str, Any] | None:
    if argument_chain is None:
        return None
    return {
        "id": argument_chain["argument_chain_id"],
        "necessity_claim": argument_chain["necessity_claim"],
    }


def _serialize_fit_mapping(fit_mapping: dict[str, Any] | None) -> dict[str, Any] | None:
    if fit_mapping is None:
        return None
    return {
        "id": fit_mapping["fit_mapping_id"],
        "argument_chain_id": fit_mapping["argument_chain_id"],
        "applicant_fit_summary": fit_mapping["applicant_fit_summary"],
        "unique_advantage": fit_mapping["unique_advantage"],
    }


def _serialize_draft(draft: dict[str, Any] | None) -> dict[str, Any] | None:
    if draft is None:
        return None
    return {
        "id": draft["draft_id"],
        "version_label": draft["version_label"],
        "status": draft["status"],
        "project_title": draft["project_title"],
        "outline_count": len(draft.get("outline", [])),
        "section_count": len(draft.get("sections", [])),
    }


def _serialize_revision_plan(revision_plan: dict[str, Any] | None) -> dict[str, Any] | None:
    if revision_plan is None:
        return None
    return {
        "id": revision_plan["revision_plan_id"],
        "item_count": len(revision_plan["items"]),
        "execution_status": revision_plan.get("execution_status", "planned"),
        "pre_revision_version_label": revision_plan.get("pre_revision_version_label"),
        "post_revision_version_label": revision_plan.get("post_revision_version_label"),
        "comparison_summary": revision_plan.get("comparison_summary"),
        "next_review_focus_count": len(revision_plan.get("next_review_focus", [])),
    }


def _serialize_critique(critique: dict[str, Any] | None) -> dict[str, Any] | None:
    if critique is None:
        return None
    return {
        "id": critique["critique_id"],
        "verdict": critique["verdict"],
        "reviewed_revision_plan_id": critique.get("reviewed_revision_plan_id"),
        "forced_rollback_stage": critique.get("forced_rollback_stage"),
        "forced_rollback_reason": critique.get("forced_rollback_reason"),
        "blocking_issue_count": len(critique.get("blocking_issues", [])),
    }


def _serialize_reviewed_revision_evidence(revision_plan: dict[str, Any] | None) -> dict[str, Any] | None:
    if revision_plan is None:
        return None
    return {
        "revision_plan_id": revision_plan["revision_plan_id"],
        "source_critique_id": revision_plan["critique_id"],
        "execution_status": revision_plan.get("execution_status", "planned"),
        "pre_revision_version_label": revision_plan.get("pre_revision_version_label"),
        "post_revision_version_label": revision_plan.get("post_revision_version_label"),
        "comparison_summary": revision_plan.get("comparison_summary"),
    }


def _build_intake_section(
    *,
    workspace_id: str,
    section_id: str,
    status: str,
    trust_level: str,
    summary: str,
    missing_items: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "status": status,
        "trust_level": trust_level,
        "summary": summary,
        "linked_refs": [
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::{section_id}",
                "label": section_id,
            }
        ],
        "missing_items": list(missing_items or []),
    }


def _selection_context(document: dict[str, Any]) -> dict[str, Any]:
    selection = document.get("current_selection")
    if not isinstance(selection, dict):
        selection = {}
    return {
        "selected_direction_id": selection.get("selected_direction_id"),
        "selected_question_id": selection.get("selected_question_id"),
        "active_fit_mapping_id": selection.get("active_fit_mapping_id"),
        "active_draft_id": selection.get("active_draft_id"),
        "active_revision_plan_id": selection.get("active_revision_plan_id"),
    }


def _track_record_evidence_ids(document: dict[str, Any]) -> list[str]:
    evidence_ids: set[str] = set()
    for output in document.get("track_record", {}).get("representative_outputs", []):
        if not isinstance(output, dict):
            continue
        evidence = output.get("evidence")
        evidence_id = evidence.get("evidence_id") if isinstance(evidence, dict) else None
        if isinstance(evidence_id, str) and evidence_id.strip():
            evidence_ids.add(evidence_id.strip())
    return sorted(evidence_ids)


def _active_project_evidence_ids(document: dict[str, Any]) -> list[str]:
    evidence_ids: set[str] = set()
    for project in document.get("active_project_set", {}).get("projects", []):
        if not isinstance(project, dict):
            continue
        for evidence in project.get("linked_evidence", []):
            if not isinstance(evidence, dict):
                continue
            evidence_id = evidence.get("evidence_id")
            if isinstance(evidence_id, str) and evidence_id.strip():
                evidence_ids.add(evidence_id.strip())
    return sorted(evidence_ids)


def _preliminary_evidence_ids(document: dict[str, Any]) -> list[str]:
    evidence_ids: set[str] = set()
    for item in document.get("preliminary_evidence_pack", {}).get("evidence_items", []):
        if not isinstance(item, dict):
            continue
        evidence = item.get("evidence")
        evidence_id = evidence.get("evidence_id") if isinstance(evidence, dict) else None
        if isinstance(evidence_id, str) and evidence_id.strip():
            evidence_ids.add(evidence_id.strip())
    return sorted(evidence_ids)


def _preliminary_evidence_item_ids(document: dict[str, Any]) -> list[str]:
    item_ids: set[str] = set()
    for item in document.get("preliminary_evidence_pack", {}).get("evidence_items", []):
        if not isinstance(item, dict):
            continue
        item_id = item.get("item_id")
        if isinstance(item_id, str) and item_id.strip():
            item_ids.add(item_id.strip())
    return sorted(item_ids)


def _collect_primary_evidence_ids(document: dict[str, Any]) -> list[str]:
    return sorted(
        set(
            _track_record_evidence_ids(document)
            + _active_project_evidence_ids(document)
            + _preliminary_evidence_ids(document)
        )
    )


def _selected_direction_evidence_ids(document: dict[str, Any], selection_context: dict[str, Any]) -> list[str]:
    selected_direction_id = selection_context.get("selected_direction_id")
    if not isinstance(selected_direction_id, str) or not selected_direction_id.strip():
        return []
    for item in document.get("direction_hypotheses", []):
        if isinstance(item, dict) and item.get("direction_id") == selected_direction_id:
            return _string_list(item.get("required_evidence_ids"))
    return []


def _selected_question_evidence_ids(document: dict[str, Any], selection_context: dict[str, Any]) -> list[str]:
    selected_question_id = selection_context.get("selected_question_id")
    if not isinstance(selected_question_id, str) or not selected_question_id.strip():
        return []
    for item in document.get("scientific_question_cards", []):
        if isinstance(item, dict) and item.get("question_id") == selected_question_id:
            return _string_list(item.get("linked_evidence_ids"))
    return []


def _active_argument_chain_evidence_ids(document: dict[str, Any], selection_context: dict[str, Any]) -> list[str]:
    selected_question_id = selection_context.get("selected_question_id")
    if not isinstance(selected_question_id, str) or not selected_question_id.strip():
        return []
    for item in document.get("argument_chains", []):
        if isinstance(item, dict) and item.get("scientific_question_id") == selected_question_id:
            return _string_list(item.get("linked_evidence_ids"))
    return []


def _active_fit_mapping_evidence_ids(document: dict[str, Any], selection_context: dict[str, Any]) -> list[str]:
    active_fit_mapping_id = selection_context.get("active_fit_mapping_id")
    if not isinstance(active_fit_mapping_id, str) or not active_fit_mapping_id.strip():
        return []
    for item in document.get("applicant_fit_mappings", []):
        if isinstance(item, dict) and item.get("fit_mapping_id") == active_fit_mapping_id:
            return _string_list(item.get("linked_evidence_ids"))
    return []


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted({item.strip() for item in value if isinstance(item, str) and item.strip()})


def _collect_trust_ranked_evidence(document: dict[str, Any]) -> list[dict[str, Any]]:
    workspace_id = document["workspace_id"]
    entries: list[dict[str, Any]] = []

    for output in document["track_record"].get("representative_outputs", []):
        output_id = output.get("output_id")
        if not isinstance(output_id, str) or not output_id.strip():
            continue
        evidence = output.get("evidence")
        trust_level = "trusted" if isinstance(evidence, dict) else "missing_context"
        entries.append(
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::track_record.representative_outputs::{output_id}",
                "label": output.get("title") or output_id,
                "trust_level": trust_level,
                "trust_rank": _EVIDENCE_TRUST_RANK[trust_level],
                "trust_note": (
                    "代表性成果可直接回指申请人既有积累。"
                    if isinstance(evidence, dict)
                    else "代表性成果缺少结构化 evidence 指针。"
                ),
                "source_type": (evidence or {}).get("source_type", "publication") if isinstance(evidence, dict) else "publication",
                "supports": ["applicant_fit", "scientific_question", "technical_route"],
                "_source_priority": 1,
            }
        )

    for project in document["active_project_set"].get("projects", []):
        project_id = project.get("project_id")
        if not isinstance(project_id, str) or not project_id.strip():
            continue
        linked_evidence = project.get("linked_evidence")
        has_linked_evidence = isinstance(linked_evidence, list) and bool(linked_evidence)
        trust_level = "trusted" if has_linked_evidence else "missing_context"
        entries.append(
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::active_project_set.projects::{project_id}",
                "label": project.get("title") or project_id,
                "trust_level": trust_level,
                "trust_rank": _EVIDENCE_TRUST_RANK[trust_level],
                "trust_note": (
                    "在研项目可直接约束技术路线与资源可用性。"
                    if has_linked_evidence
                    else "在研项目缺少结构化 linked_evidence。"
                ),
                "source_type": "project",
                "supports": ["applicant_fit", "technical_route"],
                "_source_priority": 2,
            }
        )

    for item in document["preliminary_evidence_pack"].get("evidence_items", []):
        item_id = item.get("item_id")
        if not isinstance(item_id, str) or not item_id.strip():
            continue
        trust_level = _trust_level_from_preliminary_item(item)
        entries.append(
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::preliminary_evidence_pack.evidence_items::{item_id}",
                "label": item.get("title") or item_id,
                "trust_level": trust_level,
                "trust_rank": _EVIDENCE_TRUST_RANK[trust_level],
                "trust_note": _trust_note_from_preliminary_item(item),
                "source_type": "preliminary_result",
                "supports": ["scientific_question", "technical_route"],
                "_source_priority": 3,
            }
        )

    ordered_entries = sorted(
        entries,
        key=lambda item: (
            int(item["trust_rank"]),
            int(item["_source_priority"]),
            str(item["ref"]),
        ),
    )
    for item in ordered_entries:
        item.pop("_source_priority", None)
    return ordered_entries


def _trust_level_from_preliminary_item(item: dict[str, Any]) -> str:
    strength = item.get("strength")
    if strength == "strong":
        return "trusted"
    if strength == "moderate":
        return "usable_with_verification"
    if strength == "weak":
        return "reference_only"
    return "missing_context"


def _trust_note_from_preliminary_item(item: dict[str, Any]) -> str:
    trust_level = _trust_level_from_preliminary_item(item)
    if trust_level == "trusted":
        return "前期结果强度足够，可直接进入 route grounding。"
    if trust_level == "usable_with_verification":
        return "前期结果可用，但仍需在后续论证中显式补足功能验证。"
    if trust_level == "reference_only":
        return "前期结果强度偏弱，仅适合作为方向线索。"
    return "前期结果缺少可判定的强度信息。"


def _index_objects(
    items: Any,
    key_name: str,
    scope_name: str,
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    if not isinstance(items, list):
        return indexed
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        key = item.get(key_name)
        if not isinstance(key, str) or not key:
            continue
        if key in indexed:
            issues.append(
                ValidationIssue(
                    path=f"{scope_name}[{index}].{key_name}",
                    message=f"{key_name} 不能重复。",
                )
            )
            continue
        indexed[key] = item
    return indexed


def _require_workspace_context(document: dict[str, Any]) -> WorkspaceContext:
    state = _build_workspace_state(document)
    if (
        state.selected_direction is None
        or state.selected_question is None
        or state.active_argument_chain is None
        or state.active_fit_mapping is None
        or state.active_draft is None
        or state.active_revision_plan is None
        or state.active_critique is None
    ):
        issue = ValidationIssue(
            path="lifecycle_stage",
            message="当前 workspace 尚未具备 critique/revision 所需的完整下游上下文。",
        )
        raise WorkspaceStateError(
            f"{issue.path}: {issue.message}",
            errors=[issue],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )
    return WorkspaceContext(
        document=document,
        selected_direction=state.selected_direction,
        selected_question=state.selected_question,
        active_argument_chain=state.active_argument_chain,
        active_fit_mapping=state.active_fit_mapping,
        active_draft=state.active_draft,
        active_revision_plan=state.active_revision_plan,
        active_critique=state.active_critique,
        reviewed_revision_plan=state.reviewed_revision_plan,
    )


class _SchemaSubsetValidator:
    def __init__(self, store: SchemaStore) -> None:
        self._store = store
        self._cache: dict[str, dict[str, Any]] = {}

    def validate(self, document: Any, schema_file: str) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        schema = self._load_schema(schema_file)
        self._validate_node(document, schema, schema_file, "", issues)
        return issues

    def _load_schema(self, file_name: str) -> dict[str, Any]:
        if file_name not in self._cache:
            self._cache[file_name] = self._store.load_json(file_name)
        return self._cache[file_name]

    def _resolve_ref(self, ref: str, base_file: str) -> tuple[dict[str, Any], str]:
        file_name, _, fragment = ref.partition("#")
        target_file = file_name or base_file
        schema = self._load_schema(target_file)
        if fragment:
            schema = self._resolve_pointer(schema, fragment)
        if not isinstance(schema, dict):
            raise WorkspaceStateError(f"无法解析 schema ref: {ref}")
        return schema, target_file

    def _resolve_pointer(self, schema: dict[str, Any], fragment: str) -> dict[str, Any]:
        pointer = fragment.removeprefix("/")
        current: Any = schema
        if not pointer:
            return schema
        for part in pointer.split("/"):
            token = part.replace("~1", "/").replace("~0", "~")
            current = current[token]
        if not isinstance(current, dict):
            raise WorkspaceStateError("schema pointer 未指向 object。")
        return current

    def _validate_node(
        self,
        value: Any,
        schema: dict[str, Any],
        base_file: str,
        path: str,
        issues: list[ValidationIssue],
    ) -> None:
        if "$ref" in schema:
            resolved, resolved_file = self._resolve_ref(schema["$ref"], base_file)
            merged = dict(resolved)
            for key, item in schema.items():
                if key != "$ref":
                    merged[key] = item
            self._validate_node(value, merged, resolved_file, path, issues)
            return

        resolved_type = self._resolve_schema_type(value=value, schema=schema, path=path, issues=issues)
        if resolved_type == "object":
            if not isinstance(value, dict):
                issues.append(ValidationIssue(path or "$", "必须是 object。"))
                return
            required = schema.get("required", [])
            for name in required:
                if name not in value:
                    issues.append(ValidationIssue(_join_path(path, name), "缺少必填字段。"))
            properties = schema.get("properties", {})
            if schema.get("additionalProperties") is False:
                for extra in value.keys() - properties.keys():
                    issues.append(ValidationIssue(_join_path(path, extra), "存在未声明字段。"))
            for name, child_schema in properties.items():
                if name in value:
                    self._validate_node(value[name], child_schema, base_file, _join_path(path, name), issues)
        elif resolved_type == "array":
            if not isinstance(value, list):
                issues.append(ValidationIssue(path or "$", "必须是 array。"))
                return
            min_items = schema.get("minItems")
            if isinstance(min_items, int) and len(value) < min_items:
                issues.append(ValidationIssue(path or "$", f"数组长度必须至少为 {min_items}。"))
            item_schema = schema.get("items")
            if isinstance(item_schema, dict):
                for index, item in enumerate(value):
                    self._validate_node(item, item_schema, base_file, f"{path}[{index}]" if path else f"[{index}]", issues)
        elif resolved_type == "string":
            if not isinstance(value, str):
                issues.append(ValidationIssue(path or "$", "必须是 string。"))
                return
            min_length = schema.get("minLength")
            if isinstance(min_length, int) and len(value) < min_length:
                issues.append(ValidationIssue(path or "$", f"字符串长度必须至少为 {min_length}。"))
            if schema.get("format") == "date-time":
                try:
                    datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    issues.append(ValidationIssue(path or "$", "必须是合法的 date-time。"))
        elif resolved_type == "integer":
            if isinstance(value, bool) or not isinstance(value, int):
                issues.append(ValidationIssue(path or "$", "必须是 integer。"))
                return
            minimum = schema.get("minimum")
            maximum = schema.get("maximum")
            if isinstance(minimum, int) and value < minimum:
                issues.append(ValidationIssue(path or "$", f"必须大于等于 {minimum}。"))
            if isinstance(maximum, int) and value > maximum:
                issues.append(ValidationIssue(path or "$", f"必须小于等于 {maximum}。"))
        elif resolved_type == "boolean":
            if not isinstance(value, bool):
                issues.append(ValidationIssue(path or "$", "必须是 boolean。"))
                return
        elif resolved_type == "null":
            if value is not None:
                issues.append(ValidationIssue(path or "$", "必须是 null。"))
                return

        const_value = schema.get("const")
        if const_value is not None and value != const_value:
            issues.append(ValidationIssue(path or "$", f"必须等于 {const_value!r}。"))
        enum_values = schema.get("enum")
        if isinstance(enum_values, list) and value not in enum_values:
            issues.append(ValidationIssue(path or "$", "取值不在允许枚举内。"))

    def _resolve_schema_type(
        self,
        *,
        value: Any,
        schema: dict[str, Any],
        path: str,
        issues: list[ValidationIssue],
    ) -> str | None:
        expected_type = schema.get("type")
        if isinstance(expected_type, str):
            return expected_type
        if not isinstance(expected_type, list):
            return None

        allowed_types = [item for item in expected_type if isinstance(item, str)]
        if not allowed_types:
            return None

        actual_type = self._infer_json_type(value)
        if actual_type in allowed_types:
            return actual_type

        issues.append(
            ValidationIssue(
                path or "$",
                f"必须是 {' 或 '.join(allowed_types)}。",
            )
        )
        return None

    def _infer_json_type(self, value: Any) -> str | None:
        if value is None:
            return "null"
        if isinstance(value, dict):
            return "object"
        if isinstance(value, list):
            return "array"
        if isinstance(value, str):
            return "string"
        if isinstance(value, bool):
            return "boolean"
        if isinstance(value, int):
            return "integer"
        return None


def _join_path(prefix: str, name: str) -> str:
    return f"{prefix}.{name}" if prefix else name
