from __future__ import annotations

import json
import copy
from pathlib import Path
from typing import Any

from med_autogrant import workspace_parts as _workspace_parts
from med_autogrant import workspace_projection_parts as _workspace_projection_parts
from med_autogrant.facade_exports import re_export_public_names
from med_autogrant.workspace_validation import _SchemaSubsetValidator, _validate_schema
from med_autogrant.workspace_parts import (
    _collect_known_ids,
    _validate_reference_sets,
    _validate_runtime_constraints,
    _validate_stage_requirements,
)
from med_autogrant.workspace_projection_parts import (
    _EVIDENCE_TRUST_LEVELS,
    _build_workspace_state,
    _collect_trust_ranked_evidence,
    _require_workspace_context,
    _serialize_argument_chain,
    _serialize_critique,
    _serialize_direction,
    _serialize_draft,
    _serialize_fit_mapping,
    _serialize_question,
    _serialize_reviewed_revision_evidence,
    _serialize_revision_plan,
)
from med_autogrant.workspace_types import (
    ValidationIssue,
    ValidationResult,
    WorkspaceContext,
    WorkspaceError,
    WorkspaceFileError,
    WorkspaceState,
    WorkspaceStateError,
)
from med_autogrant.workspace_scaffold import resolve_mag_workspace_document_path
from med_autogrant.workspace_validation import validate_workspace_document

re_export_public_names(_workspace_parts, globals())
re_export_public_names(_workspace_projection_parts, globals())


def load_workspace_document(path: str | Path) -> dict[str, Any]:
    workspace_path = resolve_mag_workspace_document_path(path)
    try:
        payload = json.loads(workspace_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 workspace 文件: {workspace_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"workspace JSON 解析失败: {workspace_path}") from exc
    if not isinstance(payload, dict):
        raise WorkspaceFileError("workspace 顶层必须是 JSON object。")
    return payload


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
        required_trace_fields = {
            "family_id",
            "family_label",
            "funder",
            "admission_status",
            "template_strategy",
            "review_grammar",
            "evidence_policy",
            "governance_policy",
            "family_compatibility_hooks",
        }
        if required_trace_fields.issubset(family_trace):
            summary["grant_family_grammar"] = {
                "family_id": family_trace["family_id"],
                "family_label": family_trace["family_label"],
                "funder": family_trace["funder"],
                "admission_status": family_trace["admission_status"],
                "template_strategy": copy.deepcopy(family_trace["template_strategy"]),
                "review_grammar": copy.deepcopy(family_trace["review_grammar"]),
                "evidence_policy": copy.deepcopy(family_trace["evidence_policy"]),
                "governance_policy": copy.deepcopy(family_trace["governance_policy"]),
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



































































