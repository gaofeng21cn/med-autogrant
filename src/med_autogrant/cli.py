from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from med_autogrant import mainline_status
from med_autogrant.domain_entry import MedAutoGrantDomainEntry
from med_autogrant.product_entry import MedAutoGrantProductEntry
from med_autogrant.public_cli import (
    INTERNAL_TO_PUBLIC_COMMAND,
    PUBLIC_COMMAND_GROUP_SUMMARIES,
    PUBLIC_COMMAND_ORDER,
    PUBLIC_GROUP_COMMANDS,
    PUBLIC_TO_INTERNAL_COMMAND,
    public_command_label,
)
from med_autogrant.workspace import (
    WorkspaceError,
    WorkspaceStateError,
    load_workspace_document,
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
    _add_workspace_command(
        subparsers,
        "grant-progress",
        handle_grant_progress,
        "输出 grant 当前阶段的人话 progress projection。",
    )
    _add_workspace_command(
        subparsers,
        "grant-cockpit",
        handle_grant_cockpit,
        "输出 grant 当前的只读 cockpit projection。",
    )
    _add_simple_command(
        subparsers,
        "mainline-status",
        handle_mainline_status,
        "输出当前 repo 主线阶段、理想目标与 remaining gaps。",
    )
    _add_phase_command(
        subparsers,
        "mainline-phase",
        handle_mainline_phase,
        "输出某个 mainline phase 的当前入口与退出条件。",
    )
    _add_direct_entry_command(
        subparsers,
        "grant-direct-entry",
        handle_grant_direct_entry,
        "输出 direct grant product entry composition，复用 progress/cockpit 与 direct / OPL entry envelope。",
    )
    _add_direct_entry_command(
        subparsers,
        "grant-user-loop",
        handle_grant_user_loop,
        "输出当前 direct grant user loop，组合 mainline snapshot、direct entry 与 next action。",
    )
    _add_manifest_command(
        subparsers,
        "product-entry-manifest",
        handle_product_entry_manifest,
        "输出当前 direct grant product-entry manifest，收口 repo 主线、当前壳与 shared handoff 模板。",
    )
    _add_manifest_command(
        subparsers,
        "product-frontdesk",
        handle_product_frontdesk,
        "输出 controller-owned 的 direct grant product frontdesk。",
    )
    _add_workspace_command(
        subparsers,
        "product-preflight",
        handle_product_preflight,
        "输出 direct grant frontdoor 的前置检查。",
    )
    _add_manifest_command(
        subparsers,
        "product-start",
        handle_product_start,
        "输出当前 direct grant product-entry start surface。",
    )
    _add_simple_command(
        subparsers,
        "probe-upstream-hermes",
        handle_probe_upstream_hermes,
        "探测真实上游 Hermes-Agent 依赖、入口与 session substrate。",
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
        "execute-direction-screening-pass",
        handle_execute_direction_screening_pass,
        "执行方向筛选 pass，生成 direction_screening workspace。",
    )
    _add_artifact_bundle_command(
        subparsers,
        "execute-question-refinement-pass",
        handle_execute_question_refinement_pass,
        "执行科学问题提纯 pass，生成 question_refinement workspace。",
    )
    _add_artifact_bundle_command(
        subparsers,
        "execute-argument-building-pass",
        handle_execute_argument_building_pass,
        "执行立项依据构建 pass，生成 argument_building workspace。",
    )
    _add_artifact_bundle_command(
        subparsers,
        "execute-fit-alignment-pass",
        handle_execute_fit_alignment_pass,
        "执行 applicant-problem fit 对齐 pass，生成 fit_alignment workspace。",
    )
    _add_artifact_bundle_command(
        subparsers,
        "execute-outline-pass",
        handle_execute_outline_pass,
        "执行提纲冻结 pass，生成 outline workspace。",
    )
    _add_artifact_bundle_command(
        subparsers,
        "execute-drafting-pass",
        handle_execute_drafting_pass,
        "执行正文起草 pass，生成 drafting workspace。",
    )
    _add_artifact_bundle_command(
        subparsers,
        "build-artifact-bundle",
        handle_build_artifact_bundle,
        "把当前 workspace 的已冻结对象写成本地 artifact bundle。",
    )
    _add_revision_executor_command(
        subparsers,
        "execute-critique-pass",
        handle_execute_critique_pass,
        "通过 Codex CLI critique executor 生成导师式批注与 revision plan。",
    )
    _add_revision_executor_command(
        subparsers,
        "execute-revision-pass",
        handle_execute_revision_pass,
        "按冻结的 section-level deterministic contract 执行 revision pass。",
    )
    _add_artifact_bundle_command(
        subparsers,
        "execute-freeze-pass",
        handle_execute_freeze_pass,
        "执行送审前冻结 pass，生成 frozen workspace。",
    )
    _add_final_package_command(
        subparsers,
        "build-final-package",
        handle_build_final_package,
        "把 freeze-ready / submission-frozen workspace 写成本地 final package。",
    )
    _add_hosted_contract_bundle_command(
        subparsers,
        "build-hosted-contract-bundle",
        handle_build_hosted_contract_bundle,
        "把 final package 写成 hosted-friendly contract bundle。",
    )
    _add_submission_ready_package_command(
        subparsers,
        "build-submission-ready-package",
        handle_build_submission_ready_package,
        "把 frozen workspace 一次性写成 submission-ready 本地交付目录。",
    )
    _add_product_entry_command(
        subparsers,
        "build-product-entry",
        handle_build_product_entry,
        "构建可直接进入或供 OPL handoff 复用的轻量 product entry envelope。",
    )
    return parser


LEGACY_PUBLIC_COMMANDS = set(INTERNAL_TO_PUBLIC_COMMAND)


def _print_public_help() -> None:
    lines = [
        "Usage: medautogrant <group> <command> [options]",
        "",
        "Public command groups:",
    ]
    for group in PUBLIC_COMMAND_ORDER:
        lines.append(f"  {group:<10}{PUBLIC_COMMAND_GROUP_SUMMARIES[group]}")
    lines.extend(
        [
            "",
            "Examples:",
            "  medautogrant workspace validate --input <workspace-path> --format json",
            "  medautogrant product build-entry --input <workspace-path> --entry-mode direct --task-intent <task-intent> --format json",
            "  medautogrant runtime probe-hermes --format json",
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
    if group in PUBLIC_GROUP_COMMANDS and (len(argv) == 1 or argv[1] in {"-h", "--help", "help"}):
        _print_public_group_help(group)
        return 0
    return None


def _normalize_public_command_argv(argv: list[str]) -> list[str]:
    if not argv:
        return argv
    if argv[0] in LEGACY_PUBLIC_COMMANDS:
        raise SystemExit(
            f"Legacy flat command `{argv[0]}` has been removed. Use `{public_command_label(argv[0])}` instead."
        )
    if len(argv) >= 2 and (argv[0], argv[1]) in PUBLIC_TO_INTERNAL_COMMAND:
        return [PUBLIC_TO_INTERNAL_COMMAND[(argv[0], argv[1])], *argv[2:]]
    return argv


def entrypoint() -> None:
    raise SystemExit(main())


def main(argv: list[str] | None = None) -> int:
    resolved_argv = list(argv) if argv is not None else sys.argv[1:]
    help_result = _maybe_handle_public_help(resolved_argv)
    if help_result is not None:
        return help_result
    parser = build_parser()
    args = parser.parse_args(_normalize_public_command_argv(resolved_argv))
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
    return _domain_entry().dispatch({"command": "validate-workspace", "input_path": args.input})


def handle_summarize_workspace(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "summarize-workspace", "input_path": args.input})


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


def handle_product_entry_manifest(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_product_entry_manifest(
        input_path=args.input,
        funding_call=args.funding_call,
    )


def handle_product_frontdesk(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_product_frontdesk(
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


def handle_probe_upstream_hermes(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "probe-upstream-hermes"})


def handle_run_local(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "run-local",
            "input_path": args.input,
            "journal_path": args.journal,
        }
    )


def handle_resume_local(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "resume-local", "journal_path": args.journal})


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


def _domain_entry() -> MedAutoGrantDomainEntry:
    return MedAutoGrantDomainEntry()


def _product_entry() -> MedAutoGrantProductEntry:
    return MedAutoGrantProductEntry()


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


def _add_revision_executor_command(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    name: str,
    handler: Any,
    help_text: str,
) -> None:
    command = subparsers.add_parser(name, help=help_text)
    command.add_argument("--input", required=True)
    command.add_argument("--output", required=True)
    command.add_argument("--executor")
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

    if command == "grant-progress":
        projection = payload["progress_projection"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"checkpoint_status: {projection['checkpoint_status']}",
            f"recommended_next_stage: {projection['recommended_next_stage']}",
            f"current_stage_summary: {projection['current_stage_summary']}",
            f"next_system_action: {projection['next_system_action']}",
        ]
        for item in projection["current_blockers"]:
            lines.append(f"- blocker: {item}")
        return "\n".join(lines)

    if command == "grant-cockpit":
        cockpit = payload["grant_cockpit"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"workspace_status: {cockpit['workspace_status']}",
        ]
        for item in cockpit["workspace_alerts"]:
            lines.append(f"- alert: {item}")
        for name, command_line in cockpit["commands"].items():
            lines.append(f"- {name}: {command_line}")
        return "\n".join(lines)

    if command == "mainline-status":
        lines = [
            f"program_id: {payload['program_id']}",
            f"active_phase: {payload['current_runtime_owner']['active_phase']}",
            f"active_tranche: {payload['current_runtime_owner']['active_tranche']}",
        ]
        for item in payload["next_focus"]:
            lines.append(f"- next_focus: {item}")
        return "\n".join(lines)

    if command == "mainline-phase":
        phase = payload["phase"]
        lines = [
            f"phase_id: {phase['phase_id']}",
            f"phase_name: {phase['phase_name']}",
            f"status: {phase['status']}",
        ]
        for item in phase["entry_points"]:
            lines.append(f"- {item['name']}: {item['command']}")
        return "\n".join(lines)

    if command == "grant-direct-entry":
        direct_entry = payload["grant_direct_entry"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"task_intent: {direct_entry['task_intent']}",
            f"workspace_status: {direct_entry['workspace_status']}",
            f"recommended_route: {direct_entry['recommended_executor_route']['route_id']}",
        ]
        for item in direct_entry["workspace_alerts"]:
            lines.append(f"- alert: {item}")
        return "\n".join(lines)

    if command == "grant-user-loop":
        user_loop = payload["grant_user_loop"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"active_tranche: {user_loop['mainline_snapshot']['active_tranche']}",
            f"next_action: {user_loop['next_action']['action_kind']}",
        ]
        if user_loop["next_action"]["command"] is not None:
            lines.append(f"- run_recommended_route: {user_loop['next_action']['command']}")
        for name, command_line in user_loop["user_loop"].items():
            if command_line is not None:
                lines.append(f"- {name}: {command_line}")
        return "\n".join(lines)

    if command == "product-entry-manifest":
        manifest = payload["product_entry_manifest"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"manifest_kind: {manifest['manifest_kind']}",
            f"active_phase: {manifest['repo_mainline']['active_phase']}",
            f"active_tranche: {manifest['repo_mainline']['active_tranche']}",
        ]
        for name, item in manifest["product_entry_shell"].items():
            lines.append(f"- {name}: {item['command']}")
        return "\n".join(lines)

    if command == "product-frontdesk":
        frontdesk = payload["product_frontdesk"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"frontdesk_command: {frontdesk['summary']['frontdesk_command']}",
            f"recommended_command: {frontdesk['summary']['recommended_command']}",
            f"operator_loop_command: {frontdesk['summary']['operator_loop_command']}",
        ]
        for name, item in frontdesk["entry_surfaces"].items():
            lines.append(f"- {name}: {item['command']}")
        return "\n".join(lines)

    if command == "product-preflight":
        preflight = payload["product_entry_preflight"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"ready_to_try_now: {preflight['ready_to_try_now']}",
            f"recommended_check_command: {preflight['recommended_check_command']}",
            f"recommended_start_command: {preflight['recommended_start_command']}",
        ]
        for item in preflight["checks"]:
            lines.append(
                f"- {item['check_id']}: {item['status']} (blocking={item['blocking']}) -> {item['command']}"
            )
        return "\n".join(lines)

    if command == "product-start":
        start_surface = payload["product_entry_start"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"recommended_mode_id: {start_surface['recommended_mode_id']}",
        ]
        for mode in start_surface["modes"]:
            lines.append(f"- {mode['mode_id']}: {mode['command']}")
        return "\n".join(lines)

    if command == "probe-upstream-hermes":
        lines = [
            f"package_version: {payload['package_version']}",
            f"hermes_command: {payload['hermes_command']}",
            f"runtime_root: {payload['runtime_root']}",
            f"state_db_path: {payload['state_db_path']}",
        ]
        for name, target in payload["entrypoints"].items():
            lines.append(f"- {name}: {target}")
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

    if command in {
        "execute-direction-screening-pass",
        "execute-question-refinement-pass",
        "execute-argument-building-pass",
        "execute-fit-alignment-pass",
        "execute-outline-pass",
        "execute-drafting-pass",
        "execute-freeze-pass",
    }:
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"output_path: {payload['output_path']}",
        ]
        return "\n".join(lines)

    if command == "execute-critique-pass":
        critique_execution = payload["critique_execution"]
        executor = critique_execution.get("executor", {})
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"output_path: {payload['output_path']}",
            f"executor_kind: {executor.get('kind')}",
            f"critique_id: {critique_execution['critique_id']}",
            f"active_revision_plan_id: {critique_execution['active_revision_plan_id']}",
            f"verdict: {critique_execution['verdict']}",
        ]
        if executor.get("mode"):
            lines.append(f"executor_mode: {executor['mode']}")
        if executor.get("session_id"):
            lines.append(f"executor_session_id: {executor['session_id']}")
        return "\n".join(lines)

    if command == "execute-revision-pass":
        revision_execution = payload["revision_execution"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"output_path: {payload['output_path']}",
            f"active_revision_plan_id: {revision_execution['active_revision_plan_id']}",
            f"post_revision_version_label: {revision_execution['post_revision_version_label']}",
        ]
        return "\n".join(lines)

    if command == "build-final-package":
        final_package = payload["final_package"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"output_path: {payload['output_path']}",
            f"package_kind: {final_package['package_kind']}",
            f"checkpoint_status: {final_package['checkpoint_summary']['checkpoint_status']}",
        ]
        return "\n".join(lines)

    if command == "build-hosted-contract-bundle":
        hosted_contract_bundle = payload["hosted_contract_bundle"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"output_path: {payload['output_path']}",
            f"bundle_kind: {hosted_contract_bundle['bundle_kind']}",
            f"program_id: {hosted_contract_bundle['execution_identity']['program_id']}",
        ]
        return "\n".join(lines)

    if command == "build-submission-ready-package":
        submission_ready_package = payload["submission_ready_package"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"output_dir: {payload['output_dir']}",
            f"readiness_verdict: {submission_ready_package['readiness_verdict']}",
            f"blocking_issue_count: {submission_ready_package['audit_summary']['blocking_issue_count']}",
        ]
        return "\n".join(lines)

    if command == "build-product-entry":
        product_entry = payload["product_entry"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"entry_mode: {product_entry['entry_mode']}",
            f"task_intent: {product_entry['task_intent']}",
            f"target_domain_id: {product_entry['target_domain_id']}",
            f"checkpoint_status: {product_entry['stage_snapshot']['checkpoint_status']}",
            f"output_path: {payload['output_path']}",
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
