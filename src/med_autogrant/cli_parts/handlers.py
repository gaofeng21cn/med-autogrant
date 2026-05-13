from __future__ import annotations

import argparse
from typing import Any

from med_autogrant import mainline_status
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


def handle_grant_progress(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().read_grant_progress(input_path=args.input)


def handle_grant_cockpit(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().read_grant_cockpit(input_path=args.input)


def handle_mainline_status(args: argparse.Namespace) -> dict[str, Any]:
    return mainline_status.read_mainline_status()


def handle_mainline_phase(args: argparse.Namespace) -> dict[str, Any]:
    return mainline_status.read_mainline_phase_status(args.phase)


def handle_grant_direct_entry(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_grant_direct_entry(
        input_path=args.input,
        task_intent=args.task_intent,
        funding_call=args.funding_call,
    )


def handle_grant_user_loop(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_grant_user_loop(
        input_path=args.input,
        task_intent=args.task_intent,
        funding_call=args.funding_call,
    )


def handle_skill_catalog(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_skill_catalog(
        input_path=args.input,
        funding_call=args.funding_call,
    )


def handle_product_entry_manifest(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_product_entry_manifest(
        input_path=args.input,
        funding_call=args.funding_call,
    )


def handle_product_status(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_product_status(
        input_path=args.input,
        funding_call=args.funding_call,
    )


def handle_product_preflight(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_product_entry_preflight(
        input_path=args.input,
    )


def handle_product_start(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_product_entry_start(
        input_path=args.input,
        funding_call=args.funding_call,
    )


def handle_product_sidecar_export(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_sidecar_export(input_path=args.input)


def handle_product_sidecar_dispatch(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().dispatch_sidecar_task(task_path=args.task)


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


def handle_probe_upstream_hermes(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "probe-upstream-hermes"})


def handle_runtime_run(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "runtime-run",
            "input_path": args.input,
            "journal_path": args.journal,
        }
    )


def handle_runtime_resume(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "runtime-resume", "journal_path": args.journal})


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
    }
    if args.executor is not None:
        request["executor_kind"] = args.executor
    return _domain_entry().dispatch(request)


def handle_execute_grant_autonomy_controller(args: argparse.Namespace) -> dict[str, Any]:
    request: dict[str, Any] = {
        "command": "execute-grant-autonomy-controller",
        "input_path": args.input,
        "output_dir": args.output_dir,
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


def handle_build_product_entry(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build(
        input_path=args.input,
        entry_mode=args.entry_mode,
        task_intent=args.task_intent,
        output_path=args.output,
        funding_call=args.funding_call,
    )


def _domain_entry() -> Any:
    from med_autogrant import domain_entry

    return domain_entry.MedAutoGrantDomainEntry()


def _product_entry() -> Any:
    from med_autogrant import product_entry

    return product_entry.MedAutoGrantProductEntry()
