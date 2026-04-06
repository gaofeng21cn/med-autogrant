from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from med_autogrant.stage_router import determine_next_step
from med_autogrant.workspace import (
    WorkspaceError,
    build_critique_summary,
    load_workspace_document,
    summarize_workspace_document,
    validate_workspace_document,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="medautogrant")
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_workspace_command(
        subparsers,
        "validate-workspace",
        handle_validate_workspace,
        "校验 NSFC workspace。",
    )
    _add_workspace_command(
        subparsers,
        "summarize-workspace",
        handle_summarize_workspace,
        "输出当前 workspace 摘要。",
    )
    _add_workspace_command(
        subparsers,
        "next-step",
        handle_next_step,
        "输出当前 workspace 的下一步建议。",
    )
    _add_workspace_command(
        subparsers,
        "critique-summary",
        handle_critique_summary,
        "输出当前激活导师批注摘要。",
    )
    return parser


def entrypoint() -> None:
    raise SystemExit(main())


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = args.handler(args)
    except WorkspaceError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(_render_text(args.command, payload))

    if args.command == "validate-workspace" and not payload["ok"]:
        return 1
    return 0


def handle_validate_workspace(args: argparse.Namespace) -> dict[str, Any]:
    document = load_workspace_document(args.input)
    result = validate_workspace_document(document)
    return result.to_dict(document)


def handle_summarize_workspace(args: argparse.Namespace) -> dict[str, Any]:
    document = load_workspace_document(args.input)
    return summarize_workspace_document(document)


def handle_next_step(args: argparse.Namespace) -> dict[str, Any]:
    document = load_workspace_document(args.input)
    return determine_next_step(document)


def handle_critique_summary(args: argparse.Namespace) -> dict[str, Any]:
    document = load_workspace_document(args.input)
    payload = build_critique_summary(document)
    payload["recommended_next_stage"] = determine_next_step(document)["recommended_stage"]
    return payload


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


def _render_text(command: str, payload: dict[str, Any]) -> str:
    if command == "validate-workspace":
        lines = [
            f"workspace_id: {payload['workspace_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"ok: {payload['ok']}",
            f"error_count: {payload['error_count']}",
        ]
        for item in payload["errors"]:
            lines.append(f"- {item['path']}: {item['message']}")
        return "\n".join(lines)

    if command == "summarize-workspace":
        return "\n".join(
            [
                f"workspace_id: {payload['workspace_id']}",
                f"mode: {payload['mode']}",
                f"lifecycle_stage: {payload['lifecycle_stage']}",
                f"selected_direction: {payload['selected_direction']['title']}",
                f"selected_question: {payload['selected_question']['core_question']}",
                f"active_draft: {payload['active_draft']['project_title']}",
                f"active_critique_verdict: {payload['active_critique']['verdict']}",
            ]
        )

    if command == "next-step":
        lines = [
            f"current_stage: {payload['current_stage']}",
            f"recommended_stage: {payload['recommended_stage']}",
            f"reason: {payload['reason']}",
        ]
        for action in payload["actions"]:
            lines.append(f"- {action}")
        return "\n".join(lines)

    if command == "critique-summary":
        lines = [
            f"critique_id: {payload['critique_id']}",
            f"draft_id: {payload['draft_id']}",
            f"verdict: {payload['verdict']}",
            f"overall_diagnosis: {payload['overall_diagnosis']}",
            f"recommended_next_stage: {payload['recommended_next_stage']}",
        ]
        for item in payload["blocking_issues"]:
            lines.append(f"- {item}")
        return "\n".join(lines)

    raise ValueError(f"未知命令: {command}")


if __name__ == "__main__":
    entrypoint()
