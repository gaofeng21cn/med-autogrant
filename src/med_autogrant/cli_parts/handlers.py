from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from med_autogrant.foundry_series_cli import (
    build_foundry_series_doctor,
    build_foundry_series_inspect,
    build_foundry_series_interfaces,
    build_foundry_series_peers,
    build_foundry_series_status,
    build_foundry_series_validate,
)
from med_autogrant import mainline_status
from med_autogrant.product_entry_parts.codex_stage_receipts import (
    build_codex_stage_execution_receipt_bundle,
)
from med_autogrant.product_entry_parts.executor_first_closeout_bundle import (
    build_executor_first_closeout_bundle,
)
from med_autogrant.product_entry_parts.physical_morphology_guard import (
    build_physical_morphology_guard_projection,
)
from med_autogrant.product_entry_parts.receipt_readiness import (
    build_receipt_readiness_projection,
)
from med_autogrant.product_entry_parts.source_purity_guard_readback import (
    build_source_purity_guard_readback,
)


def handle_foundry_status(args: argparse.Namespace) -> dict[str, Any]:
    return build_foundry_series_status()


def handle_foundry_inspect(args: argparse.Namespace) -> dict[str, Any]:
    return build_foundry_series_inspect()


def handle_foundry_interfaces(args: argparse.Namespace) -> dict[str, Any]:
    return build_foundry_series_interfaces()


def handle_foundry_validate(args: argparse.Namespace) -> dict[str, Any]:
    return build_foundry_series_validate()


def handle_foundry_doctor(args: argparse.Namespace) -> dict[str, Any]:
    return build_foundry_series_doctor()


def handle_foundry_peers(args: argparse.Namespace) -> dict[str, Any]:
    return build_foundry_series_peers()


def handle_validate_workspace(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "validate-workspace", "input_path": args.input})


def handle_summarize_workspace(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "summarize-workspace", "input_path": args.input})


def handle_grant_intake_audit(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "grant-intake-audit", "input_path": args.input})


def handle_grant_evidence_grounding(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "grant-evidence-grounding", "input_path": args.input})


def handle_grant_quality_scorecard(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "grant-quality-scorecard", "input_path": args.input})


def handle_grant_quality_closure_dossier(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "grant-quality-closure-dossier", "input_path": args.input})


def handle_grant_quality_diff(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "grant-quality-diff",
            "input_path": args.input,
            "previous_input_path": args.previous_input,
        }
    )


def handle_discover_funding_opportunities(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "discover-funding-opportunities", "input_path": args.input})


def handle_refresh_funding_opportunities_cache(args: argparse.Namespace) -> dict[str, Any]:
    request: dict[str, Any] = {
        "command": "refresh-funding-opportunities-cache",
        "input_path": args.input,
    }
    if args.output is not None:
        request["output_path"] = args.output
    return _domain_entry().dispatch(request)


def handle_select_project_profile(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "select-project-profile", "input_path": args.input})


def handle_initialize_intake_workspace(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "initialize-intake-workspace",
            "input_path": args.input,
            "output_path": args.output,
            "workspace_root": getattr(args, "workspace_root", None),
            "initialize_git": not getattr(args, "no_git", False),
        }
    )


def handle_next_step(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "next-step", "input_path": args.input})


def handle_critique_summary(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "critique-summary", "input_path": args.input})


def handle_stage_route_report(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "stage-route-report", "input_path": args.input})


def handle_mainline_status(args: argparse.Namespace) -> dict[str, Any]:
    return mainline_status.read_mainline_status()


def handle_mainline_phase(args: argparse.Namespace) -> dict[str, Any]:
    return mainline_status.read_mainline_phase_status(args.phase)


def handle_domain_handler_export(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_domain_handler_export(input_path=args.input)


def handle_domain_handler_dispatch(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().dispatch_domain_handler_task(task_path=args.task)


def handle_product_domain_memory_proposal(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_domain_memory_writeback_proposal(
        input_path=args.input,
        stage_id=args.stage_id,
        source_ref=args.source_ref,
        lesson_summary=args.lesson_summary,
        proposal_id=args.proposal_id,
    )


def handle_product_domain_memory_decision(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_domain_memory_writeback_decision(
        proposal_path=args.proposal,
        decision=args.decision,
        decision_reason=args.decision_reason,
        memory_id=args.memory_id,
    )


def handle_product_domain_memory_receipt_evidence(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().write_domain_memory_receipt_evidence(
        decision_payload=args.decision,
        runtime_root=args.runtime_root,
    )


def handle_product_owner_receipt_evidence(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().write_owner_receipt_evidence(
        input_path=args.input,
        receipt_shape=args.receipt_shape,
        stage_id=args.stage_id,
        source_ref=args.source_ref,
        closeout_summary=args.closeout_summary,
        runtime_root=args.runtime_root,
        receipt_id=args.receipt_id,
    )


def handle_product_live_acceptance_receipt(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_production_live_acceptance_receipt_projection(
        owner_receipt_evidence=_read_json_object(args.owner_receipt_evidence),
        agent_lab_suite_result=_read_json_object(args.agent_lab_suite_result),
        meta_agent_coordination_result=_read_json_object(args.meta_agent_coordination_result),
    )


def handle_product_receipt_readiness(args: argparse.Namespace) -> dict[str, Any]:
    return build_receipt_readiness_projection(
        owner_receipt_evidence_items=[
            _read_json_object(receipt_path)
            for receipt_path in args.owner_receipt_evidence
        ],
        memory_receipt_items=[
            _read_json_object(receipt_path)
            for receipt_path in args.memory_receipt
        ],
        package_lifecycle_items=[
            _read_json_object(lifecycle_path)
            for lifecycle_path in args.package_lifecycle
        ],
        lifecycle_receipt_items=[
            _read_json_object(receipt_path)
            for receipt_path in args.lifecycle_receipt
        ],
    )


def handle_product_codex_stage_receipts(args: argparse.Namespace) -> dict[str, Any]:
    return build_codex_stage_execution_receipt_bundle(
        stage_id=args.stage_id,
        execution_attempts=[
            _read_json_object(attempt_path)
            for attempt_path in args.execution_attempt
        ],
        review_attempts=[
            _read_json_object(attempt_path)
            for attempt_path in args.review_attempt
        ],
    )


def handle_product_opl_owner_payload_response(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_opl_owner_payload_response(
        production_acceptance=_read_json_object(args.production_acceptance),
        external_evidence_receipt_ledger=_read_json_object(args.external_evidence_receipt_ledger),
        receipt_readiness_projection=_read_json_object(args.receipt_readiness_projection),
    )


def handle_product_manifest_sustained_consumption_payload(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_manifest_sustained_consumption_payload_response(
        owner_payload_response=_read_json_object(args.owner_payload_response),
        workspace_receipt_scaleout_evidence=_read_json_object(
            args.workspace_receipt_scaleout_evidence
        ),
        operator_payload=_read_json_object(args.operator_payload),
    )


def handle_product_physical_morphology_guard(args: argparse.Namespace) -> dict[str, Any]:
    return build_physical_morphology_guard_projection(
        source_items=[
            _read_json_object(source_item_path)
            for source_item_path in args.source_item
        ],
        external_evidence_refs=args.external_evidence_ref or [],
    )


def handle_product_source_purity_guard_readback(args: argparse.Namespace) -> dict[str, Any]:
    return build_source_purity_guard_readback()


def handle_product_executor_first_closeout_bundle(args: argparse.Namespace) -> dict[str, Any]:
    external_evidence_consumption_ledger = None
    if args.external_evidence_consumption_ledger is not None:
        external_evidence_consumption_ledger = _read_json_object(
            args.external_evidence_consumption_ledger
        )
    receipt_readiness_projection = None
    if args.receipt_readiness_projection is not None:
        receipt_readiness_projection = _read_json_object(args.receipt_readiness_projection)
    return build_executor_first_closeout_bundle(
        codex_stage_execution_receipt_bundle=_read_json_object(
            args.codex_stage_execution_receipt_bundle
        ),
        operator_closeout_readiness_projection=_read_json_object(
            args.operator_closeout_readiness_projection
        ),
        physical_morphology_guard_projection=_read_json_object(
            args.physical_morphology_guard_projection
        ),
        external_evidence_consumption_ledger=external_evidence_consumption_ledger,
        receipt_readiness_projection=receipt_readiness_projection,
    )


def handle_build_artifact_bundle(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "build-artifact-bundle",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


def handle_execute_direction_screening_pass(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "execute-direction-screening-pass",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


def handle_execute_question_refinement_pass(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "execute-question-refinement-pass",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


def handle_execute_argument_building_pass(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "execute-argument-building-pass",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


def handle_execute_fit_alignment_pass(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "execute-fit-alignment-pass",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


def handle_execute_outline_pass(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "execute-outline-pass",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


def handle_execute_drafting_pass(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "execute-drafting-pass",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


def handle_execute_critique_pass(args: argparse.Namespace) -> dict[str, Any]:
    request = {
        "command": "execute-critique-pass",
        "input_path": args.input,
        "output_path": args.output,
    }
    if args.executor is not None:
        request["executor_kind"] = args.executor
    return _domain_entry().dispatch(request)


def handle_execute_critique_revision_loop(args: argparse.Namespace) -> dict[str, Any]:
    request: dict[str, Any] = {
        "command": "execute-critique-revision-loop",
        "input_path": args.input,
        "output_dir": args.output_dir,
        "max_rounds": args.max_rounds,
        "opl_stage_attempt": _read_json_object(args.opl_stage_attempt),
    }
    if args.executor is not None:
        request["executor_kind"] = args.executor
    return _domain_entry().dispatch(request)


def handle_execute_authoring_mainline_loop(args: argparse.Namespace) -> dict[str, Any]:
    request: dict[str, Any] = {
        "command": "execute-authoring-mainline-loop",
        "input_path": args.input,
        "output_dir": args.output_dir,
        "max_cycles": args.max_cycles,
        "opl_stage_attempt": _read_json_object(args.opl_stage_attempt),
    }
    if args.executor is not None:
        request["executor_kind"] = args.executor
    return _domain_entry().dispatch(request)


def handle_execute_grant_autonomy_controller(args: argparse.Namespace) -> dict[str, Any]:
    request: dict[str, Any] = {
        "command": "execute-grant-autonomy-controller",
        "input_path": args.input,
        "output_dir": args.output_dir,
        "opl_stage_attempt": _read_json_object(args.opl_stage_attempt),
    }
    if args.executor is not None:
        request["executor_kind"] = args.executor
    return _domain_entry().dispatch(request)


def handle_execute_revision_pass(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "execute-revision-pass",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


def handle_execute_freeze_pass(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "execute-freeze-pass",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


def handle_build_final_package(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "build-final-package",
            "input_path": args.input,
            "artifact_bundle_path": args.artifact_bundle,
            "output_path": args.output,
        }
    )


def handle_build_hosted_contract_bundle(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "build-hosted-contract-bundle",
            "final_package_path": args.final_package,
            "output_path": args.output,
        }
    )


def handle_build_submission_ready_package(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "build-submission-ready-package",
            "input_path": args.input,
            "output_dir": args.output_dir,
        }
    )


def _domain_entry() -> Any:
    from med_autogrant import domain_entry

    return domain_entry.MedAutoGrantDomainEntry()


def _product_entry() -> Any:
    from med_autogrant import product_entry

    return product_entry.MedAutoGrantProductEntry()


def _read_json_object(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object at {path}.")
    return payload
