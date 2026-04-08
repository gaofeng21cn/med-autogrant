from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from med_autogrant.artifact_bundle import build_artifact_bundle_payload
from med_autogrant.local_runtime import resume_local_runtime, run_local_runtime
from med_autogrant.route_report import build_stage_route_report
from med_autogrant.stage_router import determine_next_step
from med_autogrant.workspace import (
    WorkspaceError,
    WorkspaceStateError,
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
    _add_workspace_command(
        subparsers,
        "stage-route-report",
        handle_stage_route_report,
        "按固定 stage route 聚合输出当前 workspace 状态。",
    )
    _add_runtime_entry_command(
        subparsers,
        "run-local",
        handle_run_local,
        "运行本地 runtime 单次主循环。",
    )
    _add_resume_runtime_command(
        subparsers,
        "resume-local",
        handle_resume_local,
        "从 durable run journal 恢复本地 runtime 单次主循环。",
    )
    _add_artifact_bundle_command(
        subparsers,
        "build-artifact-bundle",
        handle_build_artifact_bundle,
        "把当前 workspace 的已冻结对象写成本地 artifact bundle。",
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


def handle_stage_route_report(args: argparse.Namespace) -> dict[str, Any]:
    document = load_workspace_document(args.input)
    return build_stage_route_report(document)


def handle_run_local(args: argparse.Namespace) -> dict[str, Any]:
    return run_local_runtime(input_path=args.input, journal_path=args.journal)


def handle_resume_local(args: argparse.Namespace) -> dict[str, Any]:
    return resume_local_runtime(journal_path=args.journal)


def handle_build_artifact_bundle(args: argparse.Namespace) -> dict[str, Any]:
    document = load_workspace_document(args.input)
    return build_artifact_bundle_payload(document, output_path=args.output)


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


def _add_runtime_entry_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--journal")
    command.add_argument("--format", choices=("json", "text"), default="json")
    command.set_defaults(handler=handler)


def _add_resume_runtime_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--journal", required=True)
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


def _render_text(command: str, payload: dict[str, Any]) -> str:
    if command == "validate-workspace":
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"ok: {payload['ok']}",
            f"error_count: {payload['error_count']}",
        ]
        for item in payload["errors"]:
            lines.append(f"- {item['path']}: {item['message']}")
        return "\n".join(lines)

    if command == "summarize-workspace":
        selected_direction = payload["selected_direction"]["title"] if payload["selected_direction"] is not None else "none"
        selected_question = (
            payload["selected_question"]["core_question"] if payload["selected_question"] is not None else "none"
        )
        active_fit_mapping = (
            payload["active_fit_mapping"]["id"] if payload["active_fit_mapping"] is not None else "none"
        )
        active_draft = payload["active_draft"]["project_title"] if payload["active_draft"] is not None else "none"
        active_critique_verdict = payload["active_critique"]["verdict"] if payload["active_critique"] is not None else "none"
        return "\n".join(
            [
                f"grant_run_id: {payload['grant_run_id']}",
                f"workspace_id: {payload['workspace_id']}",
                f"mode: {payload['mode']}",
                f"lifecycle_stage: {payload['lifecycle_stage']}",
                f"selected_direction: {selected_direction}",
                f"selected_question: {selected_question}",
                f"active_fit_mapping: {active_fit_mapping}",
                f"active_draft: {active_draft}",
                f"active_critique_verdict: {active_critique_verdict}",
            ]
        )

    if command == "next-step":
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"current_stage: {payload['current_stage']}",
            f"recommended_stage: {payload['recommended_stage']}",
            f"reason: {payload['reason']}",
        ]
        for action in payload["actions"]:
            lines.append(f"- {action}")
        return "\n".join(lines)

    if command == "critique-summary":
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"critique_id: {payload['critique_id']}",
            f"draft_id: {payload['draft_id']}",
            f"verdict: {payload['verdict']}",
            f"overall_diagnosis: {payload['overall_diagnosis']}",
            f"recommended_next_stage: {payload['recommended_next_stage']}",
        ]
        for item in payload["blocking_issues"]:
            lines.append(f"- {item}")
        return "\n".join(lines)

    if command == "stage-route-report":
        critique_summary = payload["route"].get("critique_summary")
        critique_verdict = critique_summary["verdict"] if isinstance(critique_summary, dict) else "n/a"
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"route_ok: {payload['ok']}",
            f"checkpoint_status: {payload['verification_checkpoint']['checkpoint_status']}",
            f"recommended_stage: {payload['route']['next_step']['recommended_stage']}",
            f"critique_verdict: {critique_verdict}",
        ]
        return "\n".join(lines)

    if command in {"run-local", "resume-local"}:
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"stop_reason: {payload['stop_reason']['code']}",
            f"checkpoint_status: {payload['stop_reason']['checkpoint_status']}",
            f"recommended_next_stage: {payload['stop_reason']['recommended_next_stage']}",
            f"journal_path: {payload['journal_path']}",
        ]
        return "\n".join(lines)

    if command == "build-artifact-bundle":
        bundle = payload["bundle"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"output_path: {payload['output_path']}",
            f"bundle_kind: {bundle['bundle_kind']}",
            f"outline_count: {bundle['bundle_summary']['outline_count']}",
            f"section_count: {bundle['bundle_summary']['section_count']}",
        ]
        return "\n".join(lines)

    raise ValueError(f"未知命令: {command}")


def _extract_workspace_context_for_error(args: argparse.Namespace) -> dict[str, Any]:
    input_path = getattr(args, "input", None)
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


if __name__ == "__main__":
    entrypoint()
