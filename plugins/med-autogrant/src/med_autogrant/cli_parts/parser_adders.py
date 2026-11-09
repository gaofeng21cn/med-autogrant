from __future__ import annotations

import argparse
from typing import Any


EXECUTOR_KIND_CHOICES = ("codex_cli", "hermes_agent")

FIELD_ARGUMENTS: dict[str, tuple[tuple[str, ...], dict[str, Any]]] = {
    "workspace_id": (("--workspace-id",), {}),
    "grant_run_id": (("--grant-run-id",), {}),
    "revision": (("--revision",), {}),
    "request_id": (("--request-id",), {}),
    "note": (("--note",), {}),
    "input_path": (("--input",), {}),
    "previous_input_path": (("--previous-input",), {}),
    "output_path": (("--output",), {}),
    "project_root": (("--project-root",), {}),
    "workspace_root": (("--workspace-root",), {}),
    "initialize_git": (("--no-git",), {"action": "store_false", "default": True}),
    "output_dir": (("--output-dir",), {}),
    "executor_kind": (("--executor",), {"choices": EXECUTOR_KIND_CHOICES}),
    "artifact_bundle_path": (("--artifact-bundle",), {}),
    "final_package_path": (("--final-package",), {}),
    "selector": (("--phase",), {}),
    "task_path": (("--task",), {}),
    "stage_id": (("--stage-id",), {}),
    "source_ref": (("--source-ref",), {}),
    "lesson_summary": (("--lesson-summary",), {}),
    "knowledge_id": (("--knowledge-id",), {}),
    "scope_kind": (("--scope-kind",), {"choices": ("product", "owner", "topic", "project")}),
    "scope_id": (("--scope-id",), {}),
    "content_kind": (("--content-kind",), {"choices": ("mechanism", "policy", "state", "decision")}),
    "evidence_class": (("--evidence-class",), {}),
    "review_requirement": (("--review-requirement",), {}),
    "proposal_id": (("--proposal-id",), {}),
    "proposal_path": (("--proposal",), {}),
    "decision": (("--decision",), {"choices": ("accepted", "rejected")}),
    "decision_reason": (("--decision-reason",), {}),
    "decision_payload": (("--decision",), {}),
    "runtime_root": (("--runtime-root",), {}),
    "receipt_shape": (
        ("--receipt-shape",),
        {"choices": ("domain_owner_receipt", "typed_blocker", "no_regression_evidence")},
    ),
    "closeout_summary": (("--closeout-summary",), {}),
    "receipt_id": (("--receipt-id",), {}),
}


def add_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    *,
    name: str,
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


def _add_field(container: Any, field: str, *, required: bool) -> None:
    flags, configured_options = FIELD_ARGUMENTS[field]
    options = {"dest": field, **configured_options}
    if required:
        options["required"] = True
    container.add_argument(*flags, **options)
