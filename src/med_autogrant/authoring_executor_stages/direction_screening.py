"""Build the direction screening authoring stage document."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from opl_framework.executor_client import run_agent_execution_request

from med_autogrant.authoring_executor_parts import (
    _allocate_sequence_ids,
    _build_direction_screening_prompt,
    _finalize_execution_workspace,
    _fresh_metadata,
    _normalize_direction_status,
    _optional_string,
    _require_known_string_list,
    _require_nonempty_string,
    _require_nonnegative_int,
    _require_object_list,
    _run_executor_generation,
    _validate_schema_payload,
)
from med_autogrant.workspace_reference_validation import _collect_known_ids
from med_autogrant.workspace_types import WorkspaceStateError

from . import ExecutorRunner

def build_direction_screening_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    executor_runner: ExecutorRunner = run_agent_execution_request,
) -> dict[str, Any]:
    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_direction_screening_prompt(
        input_path=input_path,
        known_ids=known_ids,
    )
    domain_payload, executor_payload = _run_executor_generation(
        prompt=prompt,
        input_path=input_path,
        route_id="direction_screening",
        executor_runner=executor_runner,
    )
    selected_direction_index = _require_nonnegative_int(
        domain_payload,
        "selected_direction_index",
        context="direction screening payload",
    )
    raw_directions = _require_object_list(
        domain_payload,
        "direction_hypotheses",
        context="direction screening payload",
    )
    if not raw_directions:
        raise WorkspaceStateError("direction screening 必须输出至少一个可论证方向。")
    if selected_direction_index >= len(raw_directions):
        raise WorkspaceStateError("selected_direction_index 超出 direction_hypotheses 范围。")

    existing_direction_ids = [
        item.get("direction_id")
        for item in document.get("direction_hypotheses", [])
        if isinstance(item, dict) and isinstance(item.get("direction_id"), str)
    ]
    direction_ids = _allocate_sequence_ids("direction", len(raw_directions), existing_direction_ids)
    normalized_directions: list[dict[str, Any]] = []
    selected_direction_id = direction_ids[selected_direction_index]
    for index, raw_direction in enumerate(raw_directions):
        direction = {
            "metadata": _fresh_metadata(document),
            "direction_id": direction_ids[index],
            "title": _require_nonempty_string(raw_direction, "title", context="direction hypothesis"),
            "rationale": _require_nonempty_string(raw_direction, "rationale", context="direction hypothesis"),
            "knowledge_gap_summary": _require_nonempty_string(
                raw_direction,
                "knowledge_gap_summary",
                context="direction hypothesis",
            ),
            "applicant_fit_summary": _require_nonempty_string(
                raw_direction,
                "applicant_fit_summary",
                context="direction hypothesis",
            ),
            "novelty_angle": _optional_string(raw_direction, "novelty_angle"),
            "risk_summary": _optional_string(raw_direction, "risk_summary"),
            "required_evidence_ids": _require_known_string_list(
                raw_direction,
                "required_evidence_ids",
                known_ids=set(known_ids),
                context="direction hypothesis",
            ),
            "decision_status": "selected" if index == selected_direction_index else _normalize_direction_status(raw_direction),
        }
        _validate_schema_payload(
            direction,
            schema_file="direction-hypothesis.schema.json",
            grant_run_id=document["grant_run_id"],
            workspace_id=document["workspace_id"],
            lifecycle_stage="direction_screening",
        )
        normalized_directions.append(direction)

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "direction_screening"
    next_workspace["direction_hypotheses"] = normalized_directions
    next_workspace["scientific_question_cards"] = []
    next_workspace["argument_chains"] = []
    next_workspace["applicant_fit_mappings"] = []
    next_workspace["application_drafts"] = []
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction_id,
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": False,
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
        "direction_screening_execution": {
            "executor": executor_payload,
            "selected_direction_id": selected_direction_id,
            "direction_count": len(normalized_directions),
        },
        "direction_screening_workspace": next_workspace,
    }



