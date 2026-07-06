from __future__ import annotations

import argparse
from typing import Any


EXECUTOR_KIND_CHOICES = ("codex_cli", "hermes_agent")


def _add_format_argument(command: argparse.ArgumentParser) -> None:
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.add_argument(
        "--json",
        action="store_const",
        const="json",
        dest="format",
        help="Alias for --format json.",
    )


def _add_workspace_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
    command.set_defaults(handler=handler)

def _add_simple_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    _add_format_argument(command)
    command.set_defaults(handler=handler)

def _add_phase_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--phase", required=True)
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    command.add_argument("--opl-stage-attempt", required=True)
    _add_format_argument(command)
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
    command.add_argument("--opl-stage-attempt", required=True)
    _add_format_argument(command)
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
    command.add_argument("--opl-stage-attempt", required=True)
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
    command.set_defaults(handler=handler)

def _add_domain_handler_export_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    _add_format_argument(command)
    command.set_defaults(handler=handler)

def _add_domain_handler_dispatch_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--task", required=True)
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
    command.set_defaults(handler=handler)


def _add_product_manifest_sustained_consumption_payload_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--owner-payload-response", required=True)
    command.add_argument("--workspace-receipt-scaleout-evidence", required=True)
    command.add_argument("--operator-payload", required=True)
    _add_format_argument(command)
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
    _add_format_argument(command)
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
    _add_format_argument(command)
    command.set_defaults(handler=handler)
