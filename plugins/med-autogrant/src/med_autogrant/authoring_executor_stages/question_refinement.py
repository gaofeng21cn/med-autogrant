"""Build the question refinement authoring stage document."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from opl_framework.executor_client import run_agent_execution_request

from med_autogrant.authoring_executor_parts import (
    _build_question_refinement_prompt,
    _finalize_execution_workspace,
    _fresh_metadata,
    _next_versioned_id,
    _optional_string,
    _optional_string_list,
    _require_known_string_list,
    _require_mapping,
    _require_nonempty_string,
    _run_executor_generation,
    _validate_schema_payload,
)
from med_autogrant.workspace_projection_parts import _build_workspace_state
from med_autogrant.workspace_reference_validation import _collect_known_ids
from med_autogrant.workspace_types import WorkspaceStateError

from . import ExecutorRunner

def build_question_refinement_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    executor_runner: ExecutorRunner = run_agent_execution_request,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    selected_direction = state.selected_direction
    if selected_direction is None:
        raise WorkspaceStateError("question refinement 需要当前 workspace 已绑定 selected direction。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_question_refinement_prompt(
        input_path=input_path,
        selected_direction=selected_direction,
        known_ids=known_ids,
    )
    domain_payload, executor_payload = _run_executor_generation(
        prompt=prompt,
        input_path=input_path,
        route_id="question_refinement",
        executor_runner=executor_runner,
    )
    raw_question = _require_mapping(
        domain_payload,
        "scientific_question_card",
        context="question refinement payload",
    )
    existing_question_ids = [
        item.get("question_id")
        for item in document.get("scientific_question_cards", [])
        if isinstance(item, dict) and isinstance(item.get("question_id"), str)
    ]
    question_id = _next_versioned_id("question", existing_question_ids)
    question = {
        "metadata": _fresh_metadata(document),
        "question_id": question_id,
        "parent_direction_id": selected_direction["direction_id"],
        "phenomenon": _optional_string(raw_question, "phenomenon"),
        "knowledge_boundary": _require_nonempty_string(
            raw_question,
            "knowledge_boundary",
            context="scientific question card",
        ),
        "unknown_mechanism": _require_nonempty_string(
            raw_question,
            "unknown_mechanism",
            context="scientific question card",
        ),
        "core_question": _require_nonempty_string(raw_question, "core_question", context="scientific question card"),
        "subquestions": _optional_string_list(raw_question, "subquestions"),
        "falsifiable_statement": _require_nonempty_string(
            raw_question,
            "falsifiable_statement",
            context="scientific question card",
        ),
        "proposed_breakthrough_angle": _require_nonempty_string(
            raw_question,
            "proposed_breakthrough_angle",
            context="scientific question card",
        ),
        "why_not_engineering": _require_nonempty_string(
            raw_question,
            "why_not_engineering",
            context="scientific question card",
        ),
        "why_now": _optional_string(raw_question, "why_now"),
        "linked_evidence_ids": _require_known_string_list(
            raw_question,
            "linked_evidence_ids",
            known_ids=set(known_ids),
            context="scientific question card",
        ),
    }
    _validate_schema_payload(
        question,
        schema_file="scientific-question-card.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="question_refinement",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "question_refinement"
    next_workspace["scientific_question_cards"] = [question]
    next_workspace["argument_chains"] = []
    next_workspace["applicant_fit_mappings"] = []
    next_workspace["application_drafts"] = []
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": question_id,
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": False,
        "fit_alignment_frozen": False,
        "outline_frozen": False,
        "presubmission_frozen": False,
    }
    next_workspace = _finalize_execution_workspace(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": None,
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "question_refinement_execution": {
            "executor": executor_payload,
            "selected_direction_id": selected_direction["direction_id"],
            "selected_question_id": question_id,
        },
        "question_refinement_workspace": next_workspace,
    }



