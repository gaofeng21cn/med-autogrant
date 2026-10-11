"""Build the outline authoring stage document."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from opl_framework.executor_client import run_agent_execution_request

from med_autogrant.authoring_executor_parts import (
    _build_outline_prompt,
    _finalize_execution_workspace,
    _fresh_metadata,
    _next_versioned_id,
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

def build_outline_execution_document(
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
    if (
        selected_direction is None
        or selected_question is None
        or active_argument_chain is None
        or active_fit_mapping is None
    ):
        raise WorkspaceStateError("outline 需要当前 workspace 已具备 direction / question / argument / fit。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_outline_prompt(
        input_path=input_path,
        selected_question=selected_question,
        active_argument_chain=active_argument_chain,
        active_fit_mapping=active_fit_mapping,
        known_ids=known_ids,
    )
    domain_payload, executor_payload = _run_executor_generation(
        prompt=prompt,
        input_path=input_path,
        route_id="outline",
        executor_runner=executor_runner,
    )
    raw_draft = _require_mapping(domain_payload, "application_draft", context="outline payload")
    raw_outline = _require_object_list(raw_draft, "outline", context="outline payload.application_draft")
    if not raw_outline:
        raise WorkspaceStateError("outline 需要输出非空提纲。")

    existing_draft_ids = [
        item.get("draft_id")
        for item in document.get("application_drafts", [])
        if isinstance(item, dict) and isinstance(item.get("draft_id"), str)
    ]
    draft_id = state.active_draft["draft_id"] if isinstance(state.active_draft, dict) else _next_versioned_id("draft", existing_draft_ids)
    outline = []
    for raw_section in raw_outline:
        section = {
            "section_key": _require_nonempty_string(raw_section, "section_key", context="draft outline item"),
            "section_title": _require_nonempty_string(raw_section, "section_title", context="draft outline item"),
            "core_claim": _require_nonempty_string(raw_section, "core_claim", context="draft outline item"),
            "linked_object_ids": _require_known_string_list(
                raw_section,
                "linked_object_ids",
                known_ids=set(known_ids),
                context="draft outline item",
            ),
        }
        outline.append(section)

    draft = {
        "metadata": _fresh_metadata(document),
        "draft_id": draft_id,
        "version_label": "v0.1",
        "project_title": _require_nonempty_string(raw_draft, "project_title", context="application draft"),
        "status": "outline",
        "frozen_question_id": selected_question["question_id"],
        "outline": outline,
        "sections": [],
    }
    _validate_schema_payload(
        draft,
        schema_file="application-draft.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="outline",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "outline"
    next_workspace["application_drafts"] = [draft]
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": selected_question["question_id"],
        "active_fit_mapping_id": active_fit_mapping["fit_mapping_id"],
        "active_draft_id": draft_id,
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
        "draft_id": draft_id,
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "outline_execution": {
            "executor": executor_payload,
            "active_fit_mapping_id": active_fit_mapping["fit_mapping_id"],
            "draft_id": draft_id,
            "outline_count": len(outline),
        },
        "outline_workspace": next_workspace,
    }



