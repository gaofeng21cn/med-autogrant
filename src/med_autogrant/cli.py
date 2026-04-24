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

from opl_harness_shared.status_narration import build_status_narration_human_view


_WORKSPACE_STATUS_LABELS = {
    "attention_required": "需要处理",
    "healthy": "运行正常",
}

_PHASE_STATUS_LABELS = {
    "current": "当前阶段",
    "next": "下一阶段",
    "completed": "已完成",
}

_START_MODE_LABELS = {
    "open_frontdesk": "打开 frontdesk",
    "continue_grant_loop": "继续 grant loop",
    "build_direct_entry": "构建 direct entry",
}

_HUMAN_FIELD_LABELS = {
    "grant_run_id": "当前 grant run",
    "workspace_id": "当前 workspace",
    "lifecycle_stage": "当前阶段",
    "ok": "校验结果",
    "error_count": "错误数量",
    "mode": "当前模式",
    "selected_direction": "当前方向",
    "selected_question": "当前问题",
    "active_fit_mapping": "当前 fit 映射",
    "active_draft": "当前草稿",
    "active_critique_verdict": "当前批注结论",
    "critique_id": "当前批注编号",
    "draft_id": "当前草稿编号",
    "verdict": "当前结论",
    "overall_diagnosis": "整体诊断",
    "recommended_next_stage": "建议下一阶段",
    "active_tranche": "维护者参考 tranche",
    "next_action": "当前动作",
    "run_recommended_route": "推荐执行命令",
    "ready_to_try_now": "当前可直接尝试",
    "recommended_check_command": "前置检查命令",
    "recommended_start_command": "推荐启动命令",
    "manifest_kind": "manifest 类型",
    "active_phase": "维护者参考 phase",
    "entry_mode": "当前入口模式",
    "task_intent": "当前任务意图",
    "target_domain_id": "目标域",
    "checkpoint_status": "当前 checkpoint",
    "output_path": "输出位置",
    "output_dir": "输出位置",
    "program_id": "当前 program",
    "current_line": "当前 line",
    "current_focus": "当前 focus",
}

_HUMAN_TOKEN_FIELDS = {
    "lifecycle_stage",
    "recommended_next_stage",
    "checkpoint_status",
}


def _human_token_label(value: object) -> str | None:
    view = build_status_narration_human_view(None, fallback_current_stage=str(value or "").strip() or None)
    label = view.get("current_stage_label")
    return str(label).strip() or None


def _workspace_status_label(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "未知"
    return _WORKSPACE_STATUS_LABELS.get(text, text)


def _phase_status_label(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "未知"
    return _PHASE_STATUS_LABELS.get(text, text)


def _start_mode_label(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "未命名入口"
    return _START_MODE_LABELS.get(text, text.replace("_", " "))


def _entry_surface_label(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return "未命名入口"
    public_label = public_command_label(text.replace("_", "-"))
    if public_label != text.replace("_", "-"):
        return public_label
    return text.replace("_", " ")


def _field_label(field: str) -> str:
    return _HUMAN_FIELD_LABELS.get(field, field)


def _field_value(field: str, value: object) -> object:
    if field in _HUMAN_TOKEN_FIELDS:
        return _human_token_label(value) or value
    return value


def _render_field(field: str, value: object) -> str:
    return f"{_field_label(field)}: {_field_value(field, value)}"


def _render_shell_name(name: str) -> str:
    if name in _HUMAN_FIELD_LABELS:
        return _field_label(name)
    public_label = public_command_label(name.replace("_", "-"))
    if public_label != name.replace("_", "-"):
        return public_label
    return name


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


def _render_text(command: str, payload: dict[str, Any]) -> str:
    if command == "validate-workspace":
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("ok", payload["ok"]),
            _render_field("error_count", payload["error_count"]),
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
                _render_field("grant_run_id", payload["grant_run_id"]),
                _render_field("workspace_id", payload["workspace_id"]),
                _render_field("mode", payload["mode"]),
                _render_field("lifecycle_stage", payload["lifecycle_stage"]),
                _render_field("selected_direction", selected_direction),
                _render_field("selected_question", selected_question),
                _render_field("active_fit_mapping", active_fit_mapping),
                _render_field("active_draft", active_draft),
                _render_field("active_critique_verdict", active_critique_verdict),
            ]
        )

    if command == "grant-intake-audit":
        audit = payload["grant_intake_audit"]
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            f"intake_status: {audit['intake_status']}",
            f"当前判断: {audit['summary']}",
        ]
        for item in audit["blocking_gaps"]:
            lines.append(f"- blocker: {item}")
        return "\n".join(lines)

    if command == "grant-evidence-grounding":
        grounding = payload["grant_evidence_grounding"]
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            f"grounding_status: {grounding['grounding_status']}",
            f"当前判断: {grounding['summary']}",
        ]
        for item in grounding["evidence_gaps"]:
            lines.append(f"- gap: {item}")
        return "\n".join(lines)

    if command == "grant-quality-scorecard":
        scorecard = payload["grant_quality_scorecard"]
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            f"overall_status: {scorecard['overall_status']}",
            f"overall_score: {scorecard['overall_score']}",
            f"当前判断: {scorecard['summary']}",
        ]
        for item in scorecard["unresolved_hard_issues"]:
            lines.append(f"- hard_issue: {item}")
        return "\n".join(lines)

    if command == "grant-quality-closure-dossier":
        dossier = payload["grant_quality_closure_dossier"]
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            f"overall_status: {dossier['quality_summary']['overall_status']}",
            f"overall_score: {dossier['quality_summary']['overall_score']}",
            f"closure_package_count: {len(dossier['closure_packages'])}",
            f"当前判断: {dossier['quality_summary']['summary']}",
        ]
        for item in dossier["unclosed_hard_issues"]:
            lines.append(f"- hard_issue: {item}")
        return "\n".join(lines)

    if command == "grant-quality-diff":
        diff = payload["grant_quality_diff"]
        lines = [
            f"current_workspace_id: {diff['current_workspace_id']}",
            f"previous_workspace_id: {diff['previous_workspace_id']}",
            f"overall_progression: {diff['overall_progression']}",
            f"score_delta: {diff['score_delta']}",
        ]
        for item in diff["issue_progress"]["closed_issues"]:
            lines.append(f"- closed_issue: {item}")
        for item in diff["issue_progress"]["remaining_open_issues"]:
            lines.append(f"- remaining_issue: {item}")
        for item in diff["issue_progress"]["newly_opened_issues"]:
            lines.append(f"- new_issue: {item}")
        return "\n".join(lines)

    if command == "discover-funding-opportunities":
        discovery = payload["funding_landscape_discovery"]
        lines = [
            f"discovery_input_id: {payload['discovery_input_id']}",
            f"candidate_count: {discovery['candidate_count']}",
            f"当前判断: {discovery['discovery_summary']['decision']}",
        ]
        for item in discovery["funding_opportunity_pool"]:
            lines.append(f"- candidate: {item['brief_id']}")
        return "\n".join(lines)

    if command == "refresh-funding-opportunities-cache":
        snapshot = payload["cache_snapshot"]
        lines = [
            f"discovery_input_id: {payload['discovery_input_id']}",
            f"cache_path: {payload['cache_path']}",
            f"source_count: {snapshot['source_count']}",
            f"当前判断: cache refreshed",
        ]
        return "\n".join(lines)

    if command == "select-project-profile":
        selection = payload["project_profile_selection"]
        lines = [
            f"selection_input_id: {payload['selection_input_id']}",
            f"推荐 profile: {selection['recommended_project_profile']['profile_label']}",
            f"推荐 funding: {selection['recommended_funding_opportunity']['brief_id']}",
            f"当前判断: {selection['selection_summary']['selected_profile_preset_id']}",
        ]
        for code in selection["selection_summary"]["reason_codes"]:
            lines.append(f"- reason_code: {code}")
        return "\n".join(lines)

    if command == "initialize-intake-workspace":
        lines = [
            f"selection_input_id: {payload['selection_input_id']}",
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"output_path: {payload['output_path']}",
            f"推荐 profile: {payload['project_profile_selection']['recommended_project_profile']['profile_label']}",
        ]
        return "\n".join(lines)

    if command == "next-step":
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"当前阶段: {_human_token_label(payload['current_stage']) or payload['current_stage']}",
            f"下一阶段: {_human_token_label(payload['recommended_stage']) or payload['recommended_stage']}",
            f"当前判断: {payload['reason']}",
        ]
        for action in payload["actions"]:
            lines.append(f"- 建议动作: {action}")
        return "\n".join(lines)

    if command == "critique-summary":
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("critique_id", payload["critique_id"]),
            _render_field("draft_id", payload["draft_id"]),
            _render_field("verdict", payload["verdict"]),
            _render_field("overall_diagnosis", payload["overall_diagnosis"]),
            _render_field("recommended_next_stage", payload["recommended_next_stage"]),
        ]
        for item in payload["blocking_issues"]:
            lines.append(f"- {item}")
        return "\n".join(lines)

    if command == "stage-route-report":
        critique_summary = payload["route"].get("critique_summary")
        critique_verdict = critique_summary["verdict"] if isinstance(critique_summary, dict) else "n/a"
        lifecycle_stage = payload["lifecycle_stage"]
        recommended_stage = payload["route"]["next_step"]["recommended_stage"]
        checkpoint_status = payload["verification_checkpoint"]["checkpoint_status"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"当前阶段: {_human_token_label(lifecycle_stage) or lifecycle_stage}",
            f"下一阶段: {_human_token_label(recommended_stage) or recommended_stage}",
            f"当前 checkpoint: {_human_token_label(checkpoint_status) or checkpoint_status}",
            f"当前判断: 批注结论 {critique_verdict}",
        ]
        return "\n".join(lines)

    if command == "grant-progress":
        projection = payload["progress_projection"]
        human_view = build_status_narration_human_view(
            projection,
            fallback_current_stage=projection.get("current_stage"),
            fallback_latest_update=projection.get("current_stage_summary"),
            fallback_next_step=projection.get("next_system_action"),
            fallback_blockers=projection.get("current_blockers") or [],
        )
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"checkpoint_status: {projection['checkpoint_status']}",
            f"当前阶段: {human_view.get('current_stage_label') or projection['current_stage']}",
            f"当前判断: {human_view.get('status_summary') or human_view.get('latest_update') or projection['current_stage_summary']}",
            f"下一步建议: {human_view.get('next_step') or projection['next_system_action']}",
        ]
        for item in projection["current_blockers"]:
            lines.append(f"- blocker: {item}")
        return "\n".join(lines)

    if command == "grant-cockpit":
        cockpit = payload["grant_cockpit"]
        workspace_alerts = list(cockpit["workspace_alerts"])
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"当前状态: {_workspace_status_label(cockpit['workspace_status'])}",
        ]
        if workspace_alerts:
            lines.append(f"当前判断: {workspace_alerts[0]}")
        for item in workspace_alerts[1:]:
            lines.append(f"- 关注项: {item}")
        for name, command_line in cockpit["commands"].items():
            lines.append(f"- 可用命令 {name}: {command_line}")
        return "\n".join(lines)

    if command == "mainline-status":
        current_line = payload["current_line"]
        current_focus = payload["current_focus"]
        lines = [
            _render_field("program_id", payload["program_id"]),
            _render_field("current_line", current_line["current_owner_line"]),
            _render_field("current_focus", current_focus["summary"]),
        ]
        for item in current_focus["focus_items"]:
            lines.append(f"- 当前 focus 项: {item}")
        for item in payload["completed_records"]:
            lines.append(f"- 已完成 record {item['record_id']}: {item['summary']}")
        for item in payload["remaining_gaps"]:
            lines.append(f"- 剩余 gap: {item}")
        return "\n".join(lines)

    if command == "mainline-phase":
        reference = payload["maintainer_reference"]
        phase = reference["record_detail"]
        lines = [
            f"当前 line: {payload['current_line']['current_owner_line']}",
            f"维护参考 selector: {reference['selector']}",
            f"维护参考记录: {phase['phase_id']}",
            f"记录名称: {phase['phase_name']}",
            f"记录状态: {_phase_status_label(phase['status'])}",
        ]
        for item in phase["entry_points"]:
            lines.append(f"- 可用入口 {_entry_surface_label(item['name'])}: {item['command']}")
        return "\n".join(lines)

    if command == "grant-direct-entry":
        direct_entry = payload["grant_direct_entry"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"当前阶段: {_human_token_label(payload['lifecycle_stage']) or payload['lifecycle_stage']}",
            f"task_intent: {direct_entry['task_intent']}",
            f"当前状态: {_workspace_status_label(direct_entry['workspace_status'])}",
            (
                f"推荐执行路径: "
                f"{_human_token_label(direct_entry['recommended_executor_route']['route_id']) or direct_entry['recommended_executor_route']['route_id']}"
            ),
        ]
        workspace_alerts = list(direct_entry["workspace_alerts"])
        if workspace_alerts:
            lines.append(f"当前判断: {workspace_alerts[0]}")
        for item in workspace_alerts[1:]:
            lines.append(f"- 关注项: {item}")
        return "\n".join(lines)

    if command == "grant-user-loop":
        user_loop = payload["grant_user_loop"]
        focus_items = list(user_loop["mainline_snapshot"]["next_focus"])
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("draft_id", payload["draft_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("current_focus", focus_items[0] if focus_items else user_loop["mainline_snapshot"]["active_tranche"]),
            _render_field("next_action", user_loop["next_action"]["action_kind"]),
        ]
        if user_loop["next_action"]["command"] is not None:
            lines.append(f"- {_field_label('run_recommended_route')}: {user_loop['next_action']['command']}")
        for name, command_line in user_loop["user_loop"].items():
            if command_line is not None:
                lines.append(f"- {_render_shell_name(name)}: {command_line}")
        return "\n".join(lines)

    if command == "product-entry-manifest":
        manifest = payload["product_entry_manifest"]
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("draft_id", payload["draft_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("manifest_kind", manifest["manifest_kind"]),
            _render_field("current_line", manifest["runtime"]["current_owner_line"]),
            _render_field("current_focus", manifest["repo_mainline"]["phase_summary"]),
            _render_field("active_phase", manifest["repo_mainline"]["active_phase"]),
        ]
        for name, item in manifest["product_entry_shell"].items():
            lines.append(f"- {_render_shell_name(name)}: {item['command']}")
        return "\n".join(lines)

    if command == "product-frontdesk":
        frontdesk = payload["product_frontdesk"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"当前阶段: {_human_token_label(payload['lifecycle_stage']) or payload['lifecycle_stage']}",
            f"当前判断: {frontdesk['product_entry_status']['summary']}",
            f"前台入口命令: {frontdesk['summary']['frontdesk_command']}",
            f"推荐继续命令: {frontdesk['summary']['recommended_command']}",
            f"当前 loop 命令: {frontdesk['summary']['operator_loop_command']}",
        ]
        for name, item in frontdesk["entry_surfaces"].items():
            lines.append(f"- 可用入口 {name}: {item['command']}")
        return "\n".join(lines)

    if command == "product-preflight":
        preflight = payload["product_entry_preflight"]
        lines = [
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("draft_id", payload["draft_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("ready_to_try_now", preflight["ready_to_try_now"]),
            _render_field("recommended_check_command", preflight["recommended_check_command"]),
            _render_field("recommended_start_command", preflight["recommended_start_command"]),
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
            f"当前阶段: {_human_token_label(payload['lifecycle_stage']) or payload['lifecycle_stage']}",
            f"建议入口: {_start_mode_label(start_surface['recommended_mode_id'])}",
        ]
        for mode in start_surface["modes"]:
            lines.append(f"- 可用入口 {_start_mode_label(mode['mode_id'])}: {mode['command']}")
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

    if command in {"runtime-run", "runtime-resume"}:
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

    if command == "execute-critique-revision-loop":
        loop_report = payload["loop_report"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"loop_status: {loop_report['loop_status']}",
            f"termination_reason: {loop_report['termination_reason']}",
            f"completed_rounds: {loop_report['completed_rounds']}",
            f"output_dir: {payload['output_dir']}",
        ]
        return "\n".join(lines)

    if command == "execute-authoring-mainline-loop":
        loop_report = payload["mainline_loop_report"]
        lines = [
            f"grant_run_id: {payload['grant_run_id']}",
            f"workspace_id: {payload['workspace_id']}",
            f"draft_id: {payload['draft_id']}",
            f"lifecycle_stage: {payload['lifecycle_stage']}",
            f"loop_status: {loop_report['loop_status']}",
            f"termination_reason: {loop_report['termination_reason']}",
            f"completed_cycles: {loop_report['completed_cycles']}",
            f"output_dir: {payload['output_dir']}",
        ]
        return "\n".join(lines)

    if command == "execute-grant-autonomy-controller":
        report = payload["grant_autonomy_controller_report"]
        lines = [
            f"controller_status: {report['controller_status']}",
            f"termination_reason: {report['termination_reason']}",
            f"completed_cycles: {report['completed_cycles']}",
            f"unresolved_blockers: {len(report['unresolved_blockers'])}",
            f"evidence_gaps: {len(report['evidence_gaps'])}",
            f"output_dir: {payload['output_dir']}",
        ]
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
            _render_field("grant_run_id", payload["grant_run_id"]),
            _render_field("workspace_id", payload["workspace_id"]),
            _render_field("draft_id", payload["draft_id"]),
            _render_field("lifecycle_stage", payload["lifecycle_stage"]),
            _render_field("entry_mode", product_entry["entry_mode"]),
            _render_field("task_intent", product_entry["task_intent"]),
            _render_field("target_domain_id", product_entry["target_domain_id"]),
            _render_field("checkpoint_status", product_entry["stage_snapshot"]["checkpoint_status"]),
            _render_field("output_path", payload["output_path"]),
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
