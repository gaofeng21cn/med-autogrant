from __future__ import annotations

import argparse
import json
import sys

from med_autogrant.cli_parts import parser_adders
from med_autogrant.cli_parts.handlers import DIRECT_CLI_COMMANDS, dispatch_cli_command
from med_autogrant.cli_rendering_parts import _render_text
from med_autogrant.domain_entry_catalog import SERVICE_SAFE_DOMAIN_COMMANDS
from med_autogrant.public_cli import (
    INTERNAL_TO_PUBLIC_COMMAND,
    PUBLIC_COMMAND_GROUP_SUMMARIES,
    PUBLIC_COMMAND_ORDER,
    PUBLIC_GROUP_COMMANDS,
)
from med_autogrant.workspace import load_workspace_document
from med_autogrant.workspace_types import WorkspaceError, WorkspaceStateError


RETIRED_FLAT_COMMANDS = frozenset(INTERNAL_TO_PUBLIC_COMMAND)


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
            parser_adders.add_command(
                subparsers,
                name=name,
                help_text=domain_spec.help_text,
                required_fields=domain_spec.required_fields,
                optional_fields=domain_spec.optional_fields,
                exclusive_fields=domain_spec.exclusive_fields,
            )
            continue

        direct_spec = DIRECT_CLI_COMMANDS[name]
        parser_adders.add_command(
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


def _reject_retired_flat_command(argv: list[str]) -> None:
    if not argv:
        return
    if argv[0] in RETIRED_FLAT_COMMANDS:
        raise SystemExit(f"argument command: invalid choice: '{argv[0]}'")


def entrypoint() -> None:
    raise SystemExit(main())


def main(argv: list[str] | None = None) -> int:
    resolved_argv = list(argv) if argv is not None else sys.argv[1:]
    help_result = _maybe_handle_public_help(resolved_argv)
    if help_result is not None:
        return help_result
    _reject_retired_flat_command(resolved_argv)
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
