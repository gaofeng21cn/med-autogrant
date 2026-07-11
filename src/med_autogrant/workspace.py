from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from opl_framework.workspace_boundary import (
    DEFAULT_WORKSPACE_DOCUMENT,
    resolve_workspace_document_path,
)

from med_autogrant.workspace_projection_parts import (
    _build_workspace_state,
    _serialize_argument_chain,
    _serialize_critique,
    _serialize_direction,
    _serialize_draft,
    _serialize_fit_mapping,
    _serialize_question,
    _serialize_reviewed_revision_evidence,
    _serialize_revision_plan,
)
from med_autogrant.workspace_surface_builders import (
    _build_project_profile_summary,
    build_critique_summary,
    build_grant_evidence_grounding,
    build_grant_intake_audit,
)
from med_autogrant.workspace_types import (
    WorkspaceFileError,
    WorkspaceStateError,
)
from med_autogrant.workspace_validation import validate_workspace_document


def load_workspace_document(path: str | Path) -> dict[str, Any]:
    workspace_path = resolve_workspace_document_path(
        path,
        default_filename=DEFAULT_WORKSPACE_DOCUMENT,
    )
    try:
        payload = json.loads(workspace_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 workspace 文件: {workspace_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"workspace JSON 解析失败: {workspace_path}") from exc
    if not isinstance(payload, dict):
        raise WorkspaceFileError("workspace 顶层必须是 JSON object。")
    return payload


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


def materialize_workspace_surfaces(document: dict[str, Any]) -> dict[str, Any]:
    document["grant_intake_audit"] = build_grant_intake_audit(document)
    document["grant_evidence_grounding"] = build_grant_evidence_grounding(document)
    return document
