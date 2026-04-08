from __future__ import annotations

import argparse
import json
import sys
from typing import Any

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
    validation = validate_workspace_document(document)
    if not validation.ok:
        first = validation.errors[0]
        raise WorkspaceStateError(
            f"{first.path}: {first.message}",
            errors=validation.errors,
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    validation_payload = validation.to_dict(document)
    summary = summarize_workspace_document(document)
    next_step = determine_next_step(document)
    route: dict[str, Any] = {
        "validate_workspace": validation_payload,
        "summarize_workspace": summary,
        "next_step": next_step,
    }
    critique_summary: dict[str, Any] | None = None
    if document["lifecycle_stage"] in {"critique", "revision", "frozen"}:
        critique_summary = build_critique_summary(document)
        critique_summary["recommended_next_stage"] = next_step["recommended_stage"]
        route["critique_summary"] = critique_summary
    return {
        "ok": True,
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "lifecycle_stage": document["lifecycle_stage"],
        "route": route,
        "verification_checkpoint": _build_verification_checkpoint(
            document=document,
            validation_payload=validation_payload,
            summary=summary,
            next_step=next_step,
            critique_summary=critique_summary,
        ),
    }


def _build_verification_checkpoint(
    *,
    document: dict[str, Any],
    validation_payload: dict[str, Any],
    summary: dict[str, Any],
    next_step: dict[str, Any],
    critique_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    current_selection = summary.get("current_selection")
    active_draft = summary.get("active_draft")
    active_critique = summary.get("active_critique")
    forced_rollback_stage = next_step.get("forced_rollback_stage")
    if forced_rollback_stage is None and isinstance(critique_summary, dict):
        forced_rollback_stage = critique_summary.get("forced_rollback_stage")

    forced_rollback_reason = None
    if isinstance(critique_summary, dict):
        forced_rollback_reason = critique_summary.get("forced_rollback_reason")
    elif isinstance(active_critique, dict):
        forced_rollback_reason = active_critique.get("forced_rollback_reason")

    presubmission_frozen = bool(summary.get("gates", {}).get("presubmission_frozen"))
    if presubmission_frozen:
        checkpoint_status = "submission_frozen"
    elif forced_rollback_stage:
        checkpoint_status = "rollback_required"
    else:
        checkpoint_status = "forward_progress"

    return {
        "checkpoint_status": checkpoint_status,
        "validation_ok": bool(validation_payload.get("ok")),
        "identity": {
            "grant_run_id": document["grant_run_id"],
            "workspace_id": document["workspace_id"],
            "draft_id": active_draft.get("id") if isinstance(active_draft, dict) else None,
            "active_revision_plan_id": (
                current_selection.get("active_revision_plan_id")
                if isinstance(current_selection, dict)
                else None
            ),
            "reviewed_revision_plan_id": (
                critique_summary.get("reviewed_revision_plan_id")
                if isinstance(critique_summary, dict)
                else None
            ),
        },
        "route_alignment": {
            "lifecycle_stage": document["lifecycle_stage"],
            "recommended_next_stage": next_step["recommended_stage"],
            "forced_rollback_stage": forced_rollback_stage,
            "forced_rollback_reason": forced_rollback_reason,
            "presubmission_frozen": presubmission_frozen,
        },
        "review_checkpoint": {
            "critique_id": critique_summary.get("critique_id") if isinstance(critique_summary, dict) else None,
            "reviewed_revision_evidence": summary.get("reviewed_revision_evidence"),
            "blocking_issue_count": (
                len(critique_summary.get("blocking_issues", []))
                if isinstance(critique_summary, dict)
                else 0
            ),
        },
    }


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
