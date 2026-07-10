from __future__ import annotations

import argparse
from typing import Any


EXECUTOR_KIND_CHOICES = ("codex_cli", "hermes_agent")

FIELD_ARGUMENTS: dict[str, tuple[tuple[str, ...], dict[str, Any]]] = {
    "input_path": (("--input",), {}),
    "previous_input_path": (("--previous-input",), {}),
    "output_path": (("--output",), {}),
    "workspace_root": (("--workspace-root",), {}),
    "initialize_git": (("--no-git",), {"action": "store_false", "default": True}),
    "output_dir": (("--output-dir",), {}),
    "opl_stage_attempt": (("--opl-stage-attempt",), {}),
    "max_rounds": (("--max-rounds",), {"type": int, "default": 3}),
    "max_cycles": (("--max-cycles",), {"type": int, "default": 8}),
    "executor_kind": (("--executor",), {"choices": EXECUTOR_KIND_CHOICES}),
    "artifact_bundle_path": (("--artifact-bundle",), {}),
    "final_package_path": (("--final-package",), {}),
    "selector": (("--phase",), {}),
    "task_path": (("--task",), {}),
    "stage_id": (("--stage-id",), {}),
    "source_ref": (("--source-ref",), {}),
    "lesson_summary": (("--lesson-summary",), {}),
    "proposal_id": (("--proposal-id",), {}),
    "proposal_path": (("--proposal",), {}),
    "decision": (("--decision",), {"choices": ("accepted", "rejected")}),
    "decision_reason": (("--decision-reason",), {}),
    "memory_id": (("--memory-id",), {}),
    "decision_payload": (("--decision",), {}),
    "runtime_root": (("--runtime-root",), {}),
    "receipt_shape": (
        ("--receipt-shape",),
        {"choices": ("domain_owner_receipt", "typed_blocker", "no_regression_evidence")},
    ),
    "closeout_summary": (("--closeout-summary",), {}),
    "receipt_id": (("--receipt-id",), {}),
    "execution_attempts": (("--execution-attempt",), {"action": "append"}),
    "review_attempts": (("--review-attempt",), {"action": "append", "default": []}),
}


def add_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    *,
    name: str,
    handler: Any,
    help_text: str,
    required_fields: tuple[str, ...] = (),
    optional_fields: tuple[str, ...] = (),
    exclusive_fields: tuple[str, ...] = (),
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    exclusive = (
        command.add_mutually_exclusive_group(required=True) if exclusive_fields else None
    )
    exclusive_field_set = set(exclusive_fields)

    for field in required_fields + optional_fields:
        container = exclusive if field in exclusive_field_set else command
        _add_field(
            container,
            field,
            required=field in required_fields and field not in exclusive_field_set,
        )

    command.add_argument("--format", choices=("json", "text"), default="json")
    command.add_argument(
        "--json",
        action="store_const",
        const="json",
        dest="format",
        help="Alias for --format json.",
    )
    command.set_defaults(handler=handler)


def _add_field(container: Any, field: str, *, required: bool) -> None:
    flags, configured_options = FIELD_ARGUMENTS[field]
    options = {"dest": field, **configured_options}
    if required:
        options["required"] = True
    container.add_argument(*flags, **options)
