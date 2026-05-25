from __future__ import annotations

import argparse
from typing import Any


EXECUTOR_KIND_CHOICES = ("codex_cli", "hermes_agent")


def _add_workspace_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_output_workspace_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--output", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_initialize_intake_workspace_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    output_target = command.add_mutually_exclusive_group(required=True)
    output_target.add_argument("--output")
    output_target.add_argument("--workspace-root")
    command.add_argument("--no-git", action="store_true")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_refresh_cache_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--output")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_quality_diff_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--previous-input", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_simple_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_phase_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--phase", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_direct_entry_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--task-intent", required=True)
    command.add_argument("--funding-call")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_manifest_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--funding-call")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_artifact_bundle_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--output", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_revision_executor_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--output", required=True)
    command.add_argument("--executor", choices=EXECUTOR_KIND_CHOICES)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_critique_loop_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--output-dir", required=True)
    command.add_argument("--max-rounds", type=int, default=3)
    command.add_argument("--executor", choices=EXECUTOR_KIND_CHOICES)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_mainline_loop_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--output-dir", required=True)
    command.add_argument("--max-cycles", type=int, default=8)
    command.add_argument("--executor", choices=EXECUTOR_KIND_CHOICES)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_grant_autonomy_controller_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--output-dir", required=True)
    command.add_argument("--executor", choices=EXECUTOR_KIND_CHOICES)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_final_package_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--artifact-bundle", required=True)
    command.add_argument("--output", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_hosted_contract_bundle_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--final-package", required=True)
    command.add_argument("--output", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_submission_ready_package_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--output-dir", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_product_entry_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--entry-mode", required=True, choices=("direct", "opl-handoff"))
    command.add_argument("--task-intent", required=True)
    command.add_argument("--funding-call")
    command.add_argument("--output")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_domain_handler_export_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_domain_handler_dispatch_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--task", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_product_domain_memory_proposal_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--stage-id", required=True)
    command.add_argument("--source-ref", required=True)
    command.add_argument("--lesson-summary", required=True)
    command.add_argument("--proposal-id")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_product_domain_memory_decision_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--proposal", required=True)
    command.add_argument("--decision", required=True, choices=("accepted", "rejected"))
    command.add_argument("--decision-reason", required=True)
    command.add_argument("--memory-id")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_product_domain_memory_receipt_evidence_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--decision", required=True)
    command.add_argument("--runtime-root")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_product_owner_receipt_evidence_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument(
        "--receipt-shape",
        required=True,
        choices=("domain_owner_receipt", "typed_blocker", "no_regression_evidence"),
    )
    command.add_argument("--stage-id", required=True)
    command.add_argument("--source-ref", required=True)
    command.add_argument("--closeout-summary", required=True)
    command.add_argument("--runtime-root")
    command.add_argument("--receipt-id")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)

def _add_product_lifecycle_receipt_evidence_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--operation", required=True, choices=("cleanup", "restore", "retention"))
    command.add_argument(
        "--receipt-shape",
        required=True,
        choices=("domain_owner_receipt", "typed_blocker", "no_regression_evidence"),
    )
    command.add_argument("--source-ref", required=True)
    command.add_argument("--closeout-summary", required=True)
    command.add_argument("--runtime-root")
    command.add_argument("--receipt-id")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_receipt_reconciliation_proof_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--owner-receipt-evidence", required=True)
    command.add_argument("--opl-ledger-ref", required=True)
    command.add_argument("--domain_handler-closeout-result")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_receipt_reconciliation_inventory_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--owner-receipt-evidence", required=True, action="append")
    command.add_argument("--opl-ledger-ref", required=True)
    command.add_argument("--domain_handler-closeout-result", action="append")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_live_acceptance_receipt_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--owner-receipt-evidence", required=True)
    command.add_argument("--agent-lab-suite-result", required=True)
    command.add_argument("--meta-agent-coordination-result", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_focused_hosted_receipt_verification_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--owner-receipt-evidence", required=True)
    command.add_argument("--opl-attempt-evidence", required=True)
    command.add_argument("--domain_handler-closeout-result")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_lifecycle_receipt_bundle_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--lifecycle-receipt-evidence", required=True, action="append")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_memory_receipt_projection_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--receipt", required=True, action="append")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_package_lifecycle_handoff_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--package-refs", required=True)
    command.add_argument("--gap-report", required=True)
    command.add_argument("--export-verdict", required=True)
    command.add_argument("--manual-portal-boundary", required=True)
    command.add_argument("--lifecycle-receipt-refs", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_receipt_readiness_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--owner-receipt-evidence", required=True, action="append")
    command.add_argument("--memory-receipt", required=True, action="append")
    command.add_argument("--package-lifecycle", required=True, action="append")
    command.add_argument("--lifecycle-receipt", required=True, action="append")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_continuous_receipt_reconciliation_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--hosted-receipt-verification", required=True, action="append")
    command.add_argument("--receipt-reconciliation-inventory", required=True)
    command.add_argument("--receipt-observability-summary")
    command.add_argument("--stage-attempt-observability-projection")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_codex_stage_receipts_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--stage-id", required=True)
    command.add_argument("--execution-attempt", required=True, action="append")
    command.add_argument("--review-attempt", action="append", default=[])
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_operator_closeout_readiness_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--production-acceptance", required=True)
    command.add_argument("--external-evidence-receipt-ledger", required=True)
    command.add_argument("--receipt-readiness-projection", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_opl_owner_payload_response_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--production-acceptance", required=True)
    command.add_argument("--external-evidence-receipt-ledger", required=True)
    command.add_argument("--receipt-readiness-projection", required=True)
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_physical_morphology_guard_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--source-item", required=True, action="append")
    command.add_argument("--external-evidence-ref", action="append", default=[])
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_product_executor_first_closeout_bundle_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--codex-stage-execution-receipt-bundle", required=True)
    command.add_argument("--operator-closeout-readiness-projection", required=True)
    command.add_argument("--physical-morphology-guard-projection", required=True)
    command.add_argument("--external-evidence-consumption-ledger")
    command.add_argument("--receipt-readiness-projection")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)
