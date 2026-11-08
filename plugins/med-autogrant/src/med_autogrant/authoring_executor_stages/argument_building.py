"""Build the argument building authoring stage document."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from opl_framework.executor_client import run_agent_execution_request

from med_autogrant.authoring_executor_parts import (
    _build_argument_building_prompt,
    _finalize_execution_workspace,
    _fresh_metadata,
    _next_versioned_id,
    _optional_string,
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

def build_argument_building_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    executor_runner: ExecutorRunner = run_agent_execution_request,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    selected_direction = state.selected_direction
    selected_question = state.selected_question
    if selected_direction is None or selected_question is None:
        raise WorkspaceStateError("argument building 需要当前 workspace 已绑定 direction 与 question。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_argument_building_prompt(
        input_path=input_path,
        selected_direction=selected_direction,
        selected_question=selected_question,
        known_ids=known_ids,
    )
    domain_payload, executor_payload = _run_executor_generation(
        prompt=prompt,
        input_path=input_path,
        route_id="argument_building",
        executor_runner=executor_runner,
    )
    raw_argument = _require_mapping(
        domain_payload,
        "argument_chain",
        context="argument building payload",
    )
    existing_argument_ids = [
        item.get("argument_chain_id")
        for item in document.get("argument_chains", [])
        if isinstance(item, dict) and isinstance(item.get("argument_chain_id"), str)
    ]
    argument_chain_id = _next_versioned_id("argument", existing_argument_ids)
    argument_chain = {
        "metadata": _fresh_metadata(document),
        "argument_chain_id": argument_chain_id,
        "scientific_question_id": selected_question["question_id"],
        "background_claim": _require_nonempty_string(raw_argument, "background_claim", context="argument chain"),
        "field_gap": _require_nonempty_string(raw_argument, "field_gap", context="argument chain"),
        "necessity_claim": _require_nonempty_string(raw_argument, "necessity_claim", context="argument chain"),
        "uniqueness_claim": _require_nonempty_string(raw_argument, "uniqueness_claim", context="argument chain"),
        "route_justification": _require_nonempty_string(raw_argument, "route_justification", context="argument chain"),
        "non_arbitrary_route_reason": _optional_string(raw_argument, "non_arbitrary_route_reason"),
        "if_not_done_loss": _require_nonempty_string(raw_argument, "if_not_done_loss", context="argument chain"),
        "linked_evidence_ids": _require_known_string_list(
            raw_argument,
            "linked_evidence_ids",
            known_ids=set(known_ids),
            context="argument chain",
        ),
    }
    _validate_schema_payload(
        argument_chain,
        schema_file="argument-chain.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="argument_building",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "argument_building"
    next_workspace["argument_chains"] = [argument_chain]
    next_workspace["applicant_fit_mappings"] = []
    next_workspace["application_drafts"] = []
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": selected_question["question_id"],
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": True,
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
        "argument_building_execution": {
            "executor": executor_payload,
            "selected_question_id": selected_question["question_id"],
            "argument_chain_id": argument_chain_id,
        },
        "argument_building_workspace": next_workspace,
    }



