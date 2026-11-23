from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import sys
from typing import Any

from med_autogrant.cli_rendering_parts import _render_text
from med_autogrant.domain_entry import dispatch_domain_request
from med_autogrant.domain_entry_catalog import SERVICE_SAFE_DOMAIN_COMMANDS
from med_autogrant.product_entry_parts.domain_handler import build_domain_handler_export
from med_autogrant.product_entry_parts.domain_handler_dispatch import dispatch_domain_handler_task
from med_autogrant.product_entry_parts.domain_memory_runtime import (
    build_domain_memory_writeback_decision,
    build_domain_memory_writeback_proposal,
    export_framework_knowledge_writeback_proposal,
    write_domain_memory_receipt_evidence,
)
from med_autogrant.product_entry_parts.owner_receipt_writers import (
    write_owner_receipt_evidence,
)
from med_autogrant.public_cli import (
    INTERNAL_TO_PUBLIC_COMMAND,
    PUBLIC_COMMAND_GROUP_SUMMARIES,
    PUBLIC_COMMAND_ORDER,
    PUBLIC_GROUP_COMMANDS,
)
from med_autogrant.workspace import load_workspace_document
from med_autogrant.workspace_types import WorkspaceError, WorkspaceStateError


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


@dataclass(frozen=True)
class DirectCommandSpec:
    help_text: str
    required_fields: tuple[str, ...] = ()
    optional_fields: tuple[str, ...] = ()


DIRECT_CLI_COMMANDS: dict[str, DirectCommandSpec] = {
    "domain-handler-export": DirectCommandSpec(
        "导出 OPL standard domain handler refs surface。",
        ("input_path",),
    ),
    "domain-handler-dispatch": DirectCommandSpec(
        "执行 OPL standard domain handler guarded action。",
        ("task_path",),
    ),
    "product-domain-memory-proposal": DirectCommandSpec(
        "生成 MAG-owned domain memory writeback proposal projection。",
        ("input_path", "workspace_root", "project_root", "stage_id", "source_ref", "lesson_summary",
         "knowledge_id", "scope_kind", "scope_id", "content_kind", "evidence_class", "review_requirement"),
        ("proposal_id",),
    ),
    "product-domain-memory-decision": DirectCommandSpec(
        "生成 MAG-owned domain memory accept/reject decision projection。",
        ("proposal_path", "decision", "decision_reason"),
    ),
    "product-domain-memory-export": DirectCommandSpec(
        "导出已校验的 Framework 六字段 knowledge writeback proposal JSON。",
        ("proposal_path",),
    ),
    "product-domain-memory-receipt-evidence": DirectCommandSpec(
        "把 MAG-owned domain memory accept/reject decision 写成 runtime receipt evidence。",
        ("decision_payload",),
        ("runtime_root",),
    ),
    "product-owner-receipt-evidence": DirectCommandSpec(
        "把 OPL-hosted stage attempt closeout 写成 MAG owner receipt runtime evidence。",
        ("input_path", "receipt_shape", "stage_id", "source_ref", "closeout_summary"),
        ("runtime_root", "receipt_id"),
    ),
}


def dispatch_cli_command(args: argparse.Namespace) -> dict[str, Any]:
    if args.command in SERVICE_SAFE_DOMAIN_COMMANDS:
        return handle_domain_command(args)
    return handle_direct_command(args)


def handle_domain_command(args: argparse.Namespace) -> dict[str, Any]:
    spec = SERVICE_SAFE_DOMAIN_COMMANDS[args.command]
    values = vars(args)
    request: dict[str, Any] = {"command": args.command}
    for field in spec.required_fields + spec.optional_fields:
        value = values.get(field)
        if value is not None:
            request[field] = value
    return dispatch_domain_request(request)


def handle_direct_command(args: argparse.Namespace) -> dict[str, Any]:
    command = args.command
    values = vars(args)
    if command == "domain-handler-export":
        return build_domain_handler_export(input_path=values["input_path"])
    if command == "domain-handler-dispatch":
        return dispatch_domain_handler_task(task_path=values["task_path"])
    if command == "product-domain-memory-proposal":
        return build_domain_memory_writeback_proposal(
            input_path=values["input_path"],
            stage_id=values["stage_id"],
            source_ref=values["source_ref"],
            lesson_summary=values["lesson_summary"],
            knowledge_id=values["knowledge_id"],
            scope_kind=values["scope_kind"],
            scope_id=values["scope_id"],
            content_kind=values["content_kind"],
            evidence_class=values["evidence_class"],
            review_requirement=values["review_requirement"],
            workspace_root=values["workspace_root"],
            project_root=values["project_root"],
            proposal_id=values.get("proposal_id"),
        )
    if command == "product-domain-memory-decision":
        return build_domain_memory_writeback_decision(
            proposal_path=values["proposal_path"],
            decision=values["decision"],
            decision_reason=values["decision_reason"],
        )
    if command == "product-domain-memory-export":
        return export_framework_knowledge_writeback_proposal(proposal_path=values["proposal_path"])
    if command == "product-domain-memory-receipt-evidence":
        return write_domain_memory_receipt_evidence(
            decision_payload=values["decision_payload"],
            runtime_root=values.get("runtime_root"),
        )
    if command == "product-owner-receipt-evidence":
        return write_owner_receipt_evidence(
            input_path=values["input_path"],
            receipt_shape=values["receipt_shape"],
            stage_id=values["stage_id"],
            source_ref=values["source_ref"],
            closeout_summary=values["closeout_summary"],
            runtime_root=values.get("runtime_root"),
            receipt_id=values.get("receipt_id"),
        )
    raise ValueError(f"unsupported direct CLI command: {command}")


def _extract_workspace_context_for_error(args: argparse.Namespace) -> dict[str, object]:
    input_path = vars(args).get("input_path")
    if not input_path:
        return {}
    try:
        document = load_workspace_document(input_path)
    except WorkspaceError:
        return {}
    return {
        "grant_run_id": document.get("grant_run_id"),
        "workspace_id": document.get("workspace_id"),
        "lifecycle_stage": document.get("lifecycle_stage"),
    }


def _extract_error_details(exc: WorkspaceError) -> list[dict[str, str]]:
    if not isinstance(exc, WorkspaceStateError):
        return []
    return [
        {
            "path": issue.path,
            "message": issue.message,
        }
        for issue in exc.errors
    ]


class _PublicCommandSubparsers:
    def __init__(
        self,
        root_subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    ) -> None:
        self._root_subparsers = root_subparsers
        self._group_subparsers: dict[
            str, argparse._SubParsersAction[argparse.ArgumentParser]
        ] = {}

    def add_parser(self, name: str, **kwargs: object) -> argparse.ArgumentParser:
        public_tokens = INTERNAL_TO_PUBLIC_COMMAND.get(name)
        if public_tokens is None:
            command = self._root_subparsers.add_parser(name, **kwargs)
            command.set_defaults(command=name)
            return command

        group, subcommand = public_tokens
        command = self._group_subparsers_for(group).add_parser(subcommand, **kwargs)
        command.set_defaults(command=name)
        return command

    def _group_subparsers_for(
        self,
        group: str,
    ) -> argparse._SubParsersAction[argparse.ArgumentParser]:
        existing = self._group_subparsers.get(group)
        if existing is not None:
            return existing
        group_parser = self._root_subparsers.add_parser(
            group,
            help=PUBLIC_COMMAND_GROUP_SUMMARIES[group],
        )
        group_subparsers = group_parser.add_subparsers(
            dest="public_command",
            required=True,
        )
        self._group_subparsers[group] = group_subparsers
        return group_subparsers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="medautogrant")
    root_subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers = _PublicCommandSubparsers(root_subparsers)

    for name in INTERNAL_TO_PUBLIC_COMMAND:
        domain_spec = SERVICE_SAFE_DOMAIN_COMMANDS.get(name)
        if domain_spec is not None:
            add_command(
                subparsers,
                name=name,
                help_text=domain_spec.help_text,
                required_fields=domain_spec.required_fields,
                optional_fields=domain_spec.optional_fields,
                exclusive_fields=domain_spec.exclusive_fields,
            )
            continue

        direct_spec = DIRECT_CLI_COMMANDS[name]
        add_command(
            subparsers,
            name=name,
            help_text=direct_spec.help_text,
            required_fields=direct_spec.required_fields,
            optional_fields=direct_spec.optional_fields,
        )
    return parser


def _print_public_help() -> None:
    lines = [
        "Usage: medautogrant <group> <command> [options]",
        "",
        "Med Auto Grant domain authority CLI",
        "Agent id: mag",
        "OPL public inspection: opl foundry agents inspect mag --json",
        "Authority boundary: MAG owns grant truth, quality/export verdicts, package authority, memory decisions, and owner receipts; OPL reads refs and projects state.",
        "",
        "Public command groups:",
    ]
    group_width = max(len(group) for group in PUBLIC_COMMAND_ORDER) + 2
    for group in PUBLIC_COMMAND_ORDER:
        lines.append(f"  {group:<{group_width}}{PUBLIC_COMMAND_GROUP_SUMMARIES[group]}")
    lines.extend(
        [
            "",
            "Examples:",
            "  medautogrant workspace validate --input <workspace-path> --format json",
            "  <med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli workspace validate --input <workspace-path> --format json",
            "  medautogrant pass revision --input <workspace-path> --output <output-path> --format json",
            "",
            "Use `medautogrant <group>` to inspect the available commands in that group.",
        ]
    )
    print("\n".join(lines))


def _print_public_group_help(group: str) -> None:
    summary = PUBLIC_COMMAND_GROUP_SUMMARIES[group]
    lines = [
        f"Usage: medautogrant {group} <command> [options]",
        "",
        summary,
        "",
        "Commands:",
    ]
    for subcommand in PUBLIC_GROUP_COMMANDS[group]:
        lines.append(f"  {subcommand}")
    print("\n".join(lines))


def _maybe_handle_public_help(argv: list[str]) -> int | None:
    if not argv or argv[0] in {"-h", "--help", "help"}:
        _print_public_help()
        return 0
    group = argv[0]
    if group in PUBLIC_GROUP_COMMANDS and (
        len(argv) == 1 or argv[1] in {"-h", "--help", "help"}
    ):
        _print_public_group_help(group)
        return 0
    return None


def entrypoint() -> None:
    raise SystemExit(main())


def main(argv: list[str] | None = None) -> int:
    resolved_argv = list(argv) if argv is not None else sys.argv[1:]
    help_result = _maybe_handle_public_help(resolved_argv)
    if help_result is not None:
        return help_result
    parser = build_parser()
    args = parser.parse_args(resolved_argv)
    try:
        payload = dispatch_cli_command(args)
    except WorkspaceError as exc:
        if args.format == "json":
            workspace_context = _extract_workspace_context_for_error(args)
            if isinstance(exc, WorkspaceStateError):
                workspace_context.setdefault("grant_run_id", exc.grant_run_id)
                workspace_context.setdefault("workspace_id", exc.workspace_id)
                workspace_context.setdefault("lifecycle_stage", exc.lifecycle_stage)
            print(
                json.dumps(
                    {
                        "ok": False,
                        "command": args.command,
                        "grant_run_id": workspace_context.get("grant_run_id"),
                        "workspace_id": workspace_context.get("workspace_id"),
                        "lifecycle_stage": workspace_context.get("lifecycle_stage"),
                        "error": str(exc),
                        "errors": _extract_error_details(exc),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            print(str(exc), file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(_render_text(args.command, payload))

    if args.command == "validate-workspace" and not payload["ok"]:
        return 1
    return 0


if __name__ == "__main__":
    entrypoint()
