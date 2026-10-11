"""Build the fit alignment authoring stage document."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from opl_framework.executor_client import run_agent_execution_request

from med_autogrant.authoring_executor_parts import (
    _build_fit_alignment_prompt,
    _finalize_execution_workspace,
    _fresh_metadata,
    _next_versioned_id,
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

def build_fit_alignment_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    executor_runner: ExecutorRunner = run_agent_execution_request,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    selected_direction = state.selected_direction
    selected_question = state.selected_question
    active_argument_chain = state.active_argument_chain
    if selected_direction is None or selected_question is None or active_argument_chain is None:
        raise WorkspaceStateError("fit alignment 需要当前 workspace 已具备 direction / question / argument。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_fit_alignment_prompt(
        input_path=input_path,
        selected_question=selected_question,
        active_argument_chain=active_argument_chain,
        known_ids=known_ids,
    )
    domain_payload, executor_payload = _run_executor_generation(
        prompt=prompt,
        input_path=input_path,
        route_id="fit_alignment",
        executor_runner=executor_runner,
    )
    raw_fit_mapping = _require_mapping(
        domain_payload,
        "applicant_fit_mapping",
        context="fit alignment payload",
    )
    existing_fit_ids = [
        item.get("fit_mapping_id")
        for item in document.get("applicant_fit_mappings", [])
        if isinstance(item, dict) and isinstance(item.get("fit_mapping_id"), str)
    ]
    fit_mapping_id = _next_versioned_id("fit", existing_fit_ids)
    fit_mapping = {
        "metadata": _fresh_metadata(document),
        "fit_mapping_id": fit_mapping_id,
        "scientific_question_id": selected_question["question_id"],
        "argument_chain_id": active_argument_chain["argument_chain_id"],
        "applicant_fit_summary": _require_nonempty_string(
            raw_fit_mapping,
            "applicant_fit_summary",
            context="applicant fit mapping",
        ),
        "unique_advantage": _require_nonempty_string(
            raw_fit_mapping,
            "unique_advantage",
            context="applicant fit mapping",
        ),
        "methods_readiness": _require_nonempty_string(
            raw_fit_mapping,
            "methods_readiness",
            context="applicant fit mapping",
        ),
        "resource_readiness": _require_nonempty_string(
            raw_fit_mapping,
            "resource_readiness",
            context="applicant fit mapping",
        ),
        "risk_mitigation": _require_nonempty_string(
            raw_fit_mapping,
            "risk_mitigation",
            context="applicant fit mapping",
        ),
        "linked_evidence_ids": _require_known_string_list(
            raw_fit_mapping,
            "linked_evidence_ids",
            known_ids=set(known_ids),
            context="applicant fit mapping",
        ),
    }
    _validate_schema_payload(
        fit_mapping,
        schema_file="applicant-fit-mapping.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="fit_alignment",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "fit_alignment"
    next_workspace["applicant_fit_mappings"] = [fit_mapping]
    next_workspace["application_drafts"] = []
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": selected_question["question_id"],
        "active_fit_mapping_id": fit_mapping_id,
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": True,
        "fit_alignment_frozen": True,
        "outline_frozen": False,
        "presubmission_frozen": False,
    }
    next_workspace = _finalize_execution_workspace(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": None,
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "fit_alignment_execution": {
            "executor": executor_payload,
            "selected_question_id": selected_question["question_id"],
            "active_fit_mapping_id": fit_mapping_id,
        },
        "fit_alignment_workspace": next_workspace,
    }



