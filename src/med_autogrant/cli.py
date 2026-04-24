from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap

_editable_shared_bootstrap.ensure_editable_dependency_paths()

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

from med_autogrant.cli_rendering import (
    _extract_error_details,
    _extract_workspace_context_for_error,
    _field_label,
    _field_value,
    _render_field,
    _render_shell_name,
    _render_text,
)




LEGACY_PUBLIC_COMMANDS = set(INTERNAL_TO_PUBLIC_COMMAND)


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
        "grant-intake-audit",
        handle_grant_intake_audit,
        "输出 grant intake audit surface。",
    )
    _add_workspace_command(
        subparsers,
        "grant-evidence-grounding",
        handle_grant_evidence_grounding,
        "输出 grant evidence grounding surface。",
    )
    _add_workspace_command(
        subparsers,
        "grant-quality-scorecard",
        handle_grant_quality_scorecard,
        "输出当前版本的质量治理 scorecard。",
    )
    _add_workspace_command(
        subparsers,
        "grant-quality-closure-dossier",
        handle_grant_quality_closure_dossier,
        "输出当前版本的质量 closure dossier。",
    )
    _add_quality_diff_command(
        subparsers,
        "grant-quality-diff",
        handle_grant_quality_diff,
        "对比两个版本的质量 scorecard 与问题关闭进度。",
    )
    _add_workspace_command(
        subparsers,
        "discover-funding-opportunities",
        handle_discover_funding_opportunities,
        "从材料与方向 hint 发现 funding opportunity pool。",
    )
    _add_refresh_cache_command(
        subparsers,
        "refresh-funding-opportunities-cache",
        handle_refresh_funding_opportunities_cache,
        "刷新官方 funding discovery cache，支持默认 runtime-state 落点。",
    )
    _add_workspace_command(
        subparsers,
        "select-project-profile",
        handle_select_project_profile,
        "从材料池与 funding pool 中选择推荐 project profile。",
    )
    _add_output_workspace_command(
        subparsers,
        "initialize-intake-workspace",
        handle_initialize_intake_workspace,
        "根据推荐 project profile 初始化 input_intake workspace。",
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
        "输出当前 repo 主线的 current line / current focus / completed records / remaining gaps。",
    )
    _add_phase_command(
        subparsers,
        "mainline-phase",
        handle_mainline_phase,
        "输出 maintainer reference 下某个记录卡片的入口与退出条件。",
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
        "skill-catalog",
        handle_skill_catalog,
        "输出单个 Med Auto Grant app skill 及其 machine-readable command contract。",
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
        "runtime-run",
        handle_runtime_run,
        "运行本地 runtime 单次主循环。",
    )
    _add_resume_runtime_command(
        subparsers,
        "runtime-resume",
        handle_runtime_resume,
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
    _add_critique_loop_command(
        subparsers,
        "execute-critique-revision-loop",
        handle_execute_critique_revision_loop,
        "执行多轮 critique/revision closed loop，直到通过或 fail-closed 停止。",
    )
    _add_mainline_loop_command(
        subparsers,
        "execute-authoring-mainline-loop",
        handle_execute_authoring_mainline_loop,
        "执行跨 question/argument/fit/drafting/critique/revision/frozen 的全链路主线 loop。",
    )
    _add_grant_autonomy_controller_command(
        subparsers,
        "execute-grant-autonomy-controller",
        handle_execute_grant_autonomy_controller,
        "执行长期自治 controller，调度 pre-workspace、mainline 与 quality gate。",
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
    command.add_argument("--executor")
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
    command.add_argument("--executor")
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


def handle_grant_intake_audit(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "grant-intake-audit", "input_path": args.input})


def handle_grant_evidence_grounding(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "grant-evidence-grounding", "input_path": args.input})


def handle_grant_quality_scorecard(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "grant-quality-scorecard", "input_path": args.input})


def handle_grant_quality_closure_dossier(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "grant-quality-closure-dossier", "input_path": args.input})


def handle_grant_quality_diff(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "grant-quality-diff",
            "input_path": args.input,
            "previous_input_path": args.previous_input,
        }
    )


def handle_discover_funding_opportunities(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "discover-funding-opportunities", "input_path": args.input})


def handle_refresh_funding_opportunities_cache(args: argparse.Namespace) -> dict[str, Any]:
    request: dict[str, Any] = {
        "command": "refresh-funding-opportunities-cache",
        "input_path": args.input,
    }
    if args.output is not None:
        request["output_path"] = args.output
    return _domain_entry().dispatch(request)


def handle_select_project_profile(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "select-project-profile", "input_path": args.input})


def handle_initialize_intake_workspace(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "initialize-intake-workspace",
            "input_path": args.input,
            "output_path": args.output,
        }
    )


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


def handle_skill_catalog(args: argparse.Namespace) -> dict[str, Any]:
    return _product_entry().build_skill_catalog(
        input_path=args.input,
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


def handle_runtime_run(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch(
        {
            "command": "runtime-run",
            "input_path": args.input,
            "journal_path": args.journal,
        }
    )


def handle_runtime_resume(args: argparse.Namespace) -> dict[str, Any]:
    return _domain_entry().dispatch({"command": "runtime-resume", "journal_path": args.journal})


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


def handle_execute_critique_revision_loop(args: argparse.Namespace) -> dict[str, Any]:
    request: dict[str, Any] = {
        "command": "execute-critique-revision-loop",
        "input_path": args.input,
        "output_dir": args.output_dir,
        "max_rounds": args.max_rounds,
    }
    if args.executor is not None:
        request["executor_kind"] = args.executor
    return _domain_entry().dispatch(request)


def handle_execute_authoring_mainline_loop(args: argparse.Namespace) -> dict[str, Any]:
    request: dict[str, Any] = {
        "command": "execute-authoring-mainline-loop",
        "input_path": args.input,
        "output_dir": args.output_dir,
        "max_cycles": args.max_cycles,
    }
    if args.executor is not None:
        request["executor_kind"] = args.executor
    return _domain_entry().dispatch(request)


def handle_execute_grant_autonomy_controller(args: argparse.Namespace) -> dict[str, Any]:
    request: dict[str, Any] = {
        "command": "execute-grant-autonomy-controller",
        "input_path": args.input,
        "output_dir": args.output_dir,
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
