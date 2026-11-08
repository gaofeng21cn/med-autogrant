from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from opl_framework.executor_client import run_agent_execution_request

from med_autogrant.authoring_executor_parts import (
    _build_strategy_authoring_prompt,
    _require_mapping,
    _run_executor_generation,
)
from med_autogrant.workspace_reference_validation import _collect_known_ids

from . import ExecutorRunner
from .passes import (
    build_argument_building_execution_document,
    build_direction_screening_execution_document,
    build_drafting_execution_document,
    build_fit_alignment_execution_document,
    build_outline_execution_document,
    build_question_refinement_execution_document,
)


def build_strategy_authoring_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    executor_runner: ExecutorRunner = run_agent_execution_request,
) -> dict[str, Any]:
    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_strategy_authoring_prompt(input_path=input_path, known_ids=known_ids)
    domain_payload, executor_payload = _run_executor_generation(
        prompt=prompt,
        input_path=input_path,
        route_id="strategy_authoring",
        executor_runner=executor_runner,
    )

    base_receipt = deepcopy(executor_payload["agent_execution_receipt"])

    def checkpoint_runner(route_id: str, checkpoint_payload: dict[str, Any]) -> ExecutorRunner:
        def run(_request: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
            receipt = deepcopy(base_receipt)
            receipt["closeout_packet"] = {
                "surface_kind": "domain_stage_closeout_packet",
                "route_id": route_id,
                "domain_output_kind": "mag_authoring_output",
                "domain_output": checkpoint_payload,
            }
            return receipt

        return run

    direction = build_direction_screening_execution_document(
        document=document,
        input_path=input_path,
        executor_runner=checkpoint_runner(
            "direction_screening",
            {
                "selected_direction_index": domain_payload.get("selected_direction_index"),
                "direction_hypotheses": domain_payload.get("direction_hypotheses"),
            },
        ),
    )
    question = build_question_refinement_execution_document(
        document=direction["direction_screening_workspace"],
        input_path=input_path,
        executor_runner=checkpoint_runner(
            "question_refinement",
            {"scientific_question_card": domain_payload.get("scientific_question_card")},
        ),
    )
    argument = build_argument_building_execution_document(
        document=question["question_refinement_workspace"],
        input_path=input_path,
        executor_runner=checkpoint_runner(
            "argument_building",
            {"argument_chain": domain_payload.get("argument_chain")},
        ),
    )
    fit = build_fit_alignment_execution_document(
        document=argument["argument_building_workspace"],
        input_path=input_path,
        executor_runner=checkpoint_runner(
            "fit_alignment",
            {"applicant_fit_mapping": domain_payload.get("applicant_fit_mapping")},
        ),
    )
    fit_workspace = fit["fit_alignment_workspace"]
    bound_application_draft = deepcopy(
        _require_mapping(domain_payload, "application_draft", context="strategy authoring payload")
    )
    strategy_object_ids = [
        fit_workspace["current_selection"]["selected_question_id"],
        fit_workspace["argument_chains"][0]["argument_chain_id"],
        fit_workspace["current_selection"]["active_fit_mapping_id"],
    ]
    for item in [
        *bound_application_draft.get("outline", []),
        *bound_application_draft.get("sections", []),
    ]:
        if isinstance(item, dict):
            item["linked_object_ids"] = list(dict.fromkeys([
                *item.get("linked_object_ids", []),
                *strategy_object_ids,
            ]))
    outline = build_outline_execution_document(
        document=fit_workspace,
        input_path=input_path,
        executor_runner=checkpoint_runner(
            "outline",
            {"application_draft": bound_application_draft},
        ),
    )
    drafting = build_drafting_execution_document(
        document=outline["outline_workspace"],
        input_path=input_path,
        executor_runner=checkpoint_runner(
            "drafting",
            {"application_draft": bound_application_draft},
        ),
    )
    workspace = drafting["drafting_workspace"]
    return {
        "grant_run_id": workspace["grant_run_id"],
        "workspace_id": workspace["workspace_id"],
        "draft_id": workspace["current_selection"]["active_draft_id"],
        "lifecycle_stage": workspace["lifecycle_stage"],
        "strategy_authoring_execution": {
            "executor": executor_payload,
            "checkpoint_routes": [
                "direction_screening",
                "question_refinement",
                "argument_building",
                "fit_alignment",
                "outline",
                "drafting",
            ],
            "observed_codex_invocation_count": 1,
            "invocation_count_is_success_condition": False,
            "checkpoint_projection_mode": "deterministic_contract_projection",
            "attempt_retry_and_route_back_allowed": True,
            "draft_id": workspace["current_selection"]["active_draft_id"],
        },
        "strategy_authoring_workspace": workspace,
    }
