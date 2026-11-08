"""Build the drafting authoring stage document."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from opl_framework.executor_client import run_agent_execution_request

from med_autogrant.authoring_executor_parts import (
    _build_drafting_prompt,
    _bump_version_label,
    _finalize_execution_workspace,
    _fresh_metadata,
    _require_known_string_list,
    _require_mapping,
    _require_nonempty_string,
    _require_object_list,
    _run_executor_generation,
    _validate_schema_payload,
)
from med_autogrant.workspace_projection_parts import _build_workspace_state
from med_autogrant.workspace_reference_validation import _collect_known_ids
from med_autogrant.workspace_types import WorkspaceStateError

from . import ExecutorRunner

def build_drafting_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    executor_runner: ExecutorRunner = run_agent_execution_request,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    selected_direction = state.selected_direction
    selected_question = state.selected_question
    active_argument_chain = state.active_argument_chain
    active_fit_mapping = state.active_fit_mapping
    active_draft = state.active_draft
    if (
        selected_direction is None
        or selected_question is None
        or active_argument_chain is None
        or active_fit_mapping is None
        or active_draft is None
    ):
        raise WorkspaceStateError("drafting 需要当前 workspace 已具备 direction / question / argument / fit / draft。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_drafting_prompt(
        input_path=input_path,
        active_draft=active_draft,
        selected_question=selected_question,
        active_argument_chain=active_argument_chain,
        active_fit_mapping=active_fit_mapping,
        known_ids=known_ids,
    )
    domain_payload, executor_payload = _run_executor_generation(
        prompt=prompt,
        input_path=input_path,
        route_id="drafting",
        executor_runner=executor_runner,
    )
    raw_draft = _require_mapping(domain_payload, "application_draft", context="drafting payload")
    raw_sections = _require_object_list(raw_draft, "sections", context="drafting payload.application_draft")
    if not raw_sections:
        raise WorkspaceStateError("drafting 需要输出非空正文 sections。")

    sections = []
    for raw_section in raw_sections:
        section = {
            "section_key": _require_nonempty_string(raw_section, "section_key", context="draft section"),
            "section_title": _require_nonempty_string(raw_section, "section_title", context="draft section"),
            "text": _require_nonempty_string(raw_section, "text", context="draft section"),
            "linked_object_ids": _require_known_string_list(
                raw_section,
                "linked_object_ids",
                known_ids=set(known_ids),
                context="draft section",
            ),
        }
        sections.append(section)

    draft = deepcopy(active_draft)
    draft["metadata"] = _fresh_metadata(document)
    draft["project_title"] = _require_nonempty_string(raw_draft, "project_title", context="application draft")
    draft["version_label"] = _bump_version_label(str(active_draft.get("version_label") or "v0.1"))
    draft["status"] = "draft"
    draft["sections"] = sections
    _validate_schema_payload(
        draft,
        schema_file="application-draft.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="drafting",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "drafting"
    next_workspace["application_drafts"] = [draft]
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": selected_question["question_id"],
        "active_fit_mapping_id": active_fit_mapping["fit_mapping_id"],
        "active_draft_id": draft["draft_id"],
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": True,
        "fit_alignment_frozen": True,
        "outline_frozen": True,
        "presubmission_frozen": False,
    }
    next_workspace = _finalize_execution_workspace(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": draft["draft_id"],
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "drafting_execution": {
            "executor": executor_payload,
            "draft_id": draft["draft_id"],
            "version_label": draft["version_label"],
            "section_count": len(sections),
        },
        "drafting_workspace": next_workspace,
    }

