from __future__ import annotations

import argparse
import json
import sys

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from med_autogrant.public_cli import (
    PUBLIC_COMMAND_GROUP_SUMMARIES,
    PUBLIC_COMMAND_ORDER,
    PUBLIC_GROUP_COMMANDS,
    PUBLIC_THREE_TOKEN_COMMANDS,
    PUBLIC_TO_INTERNAL_COMMAND,
)
from med_autogrant.workspace_types import WorkspaceError, WorkspaceStateError

from med_autogrant.cli_rendering import (
    _extract_error_details,
    _extract_workspace_context_for_error,
)
from med_autogrant.cli_rendering_parts import _render_text
from med_autogrant.cli_parts.handlers import (
    handle_build_artifact_bundle,
    handle_build_final_package,
    handle_build_hosted_contract_bundle,
    handle_build_submission_ready_package,
    handle_critique_summary,
    handle_discover_funding_opportunities,
    handle_domain_handler_dispatch,
    handle_domain_handler_export,
    handle_execute_argument_building_pass,
    handle_execute_authoring_mainline_loop,
    handle_execute_critique_pass,
    handle_execute_critique_revision_loop,
    handle_execute_direction_screening_pass,
    handle_execute_drafting_pass,
    handle_execute_fit_alignment_pass,
    handle_execute_freeze_pass,
    handle_execute_grant_autonomy_controller,
    handle_execute_outline_pass,
    handle_execute_question_refinement_pass,
    handle_execute_revision_pass,
    handle_grant_evidence_grounding,
    handle_grant_intake_audit,
    handle_grant_quality_closure_dossier,
    handle_grant_quality_diff,
    handle_grant_quality_scorecard,
    handle_initialize_intake_workspace,
    handle_mainline_phase,
    handle_mainline_status,
    handle_next_step,
    handle_product_codex_stage_receipts,
    handle_product_domain_memory_decision,
    handle_product_domain_memory_proposal,
    handle_product_domain_memory_receipt_evidence,
    handle_product_executor_first_closeout_bundle,
    handle_product_live_acceptance_receipt,
    handle_product_manifest_sustained_consumption_payload,
    handle_product_opl_owner_payload_response,
    handle_product_owner_receipt_evidence,
    handle_product_physical_morphology_guard,
    handle_product_receipt_readiness,
    handle_refresh_funding_opportunities_cache,
    handle_select_project_profile,
    handle_stage_route_report,
    handle_summarize_workspace,
    handle_validate_workspace,
)
from med_autogrant.cli_parts.parser_adders import (
    _add_artifact_bundle_command,
    _add_critique_loop_command,
    _add_domain_handler_dispatch_command,
    _add_domain_handler_export_command,
    _add_final_package_command,
    _add_grant_autonomy_controller_command,
    _add_hosted_contract_bundle_command,
    _add_initialize_intake_workspace_command,
    _add_mainline_loop_command,
    _add_output_workspace_command,
    _add_phase_command,
    _add_product_codex_stage_receipts_command,
    _add_product_domain_memory_decision_command,
    _add_product_domain_memory_proposal_command,
    _add_product_domain_memory_receipt_evidence_command,
    _add_product_executor_first_closeout_bundle_command,
    _add_product_live_acceptance_receipt_command,
    _add_product_manifest_sustained_consumption_payload_command,
    _add_product_opl_owner_payload_response_command,
    _add_product_owner_receipt_evidence_command,
    _add_product_physical_morphology_guard_command,
    _add_product_receipt_readiness_command,
    _add_quality_diff_command,
    _add_refresh_cache_command,
    _add_revision_executor_command,
    _add_simple_command,
    _add_submission_ready_package_command,
    _add_workspace_command,
)


RETIRED_FLAT_COMMANDS = frozenset(PUBLIC_TO_INTERNAL_COMMAND.values())


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
    _add_initialize_intake_workspace_command(
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
    _add_domain_handler_export_command(
        subparsers,
        "domain-handler-export",
        handle_domain_handler_export,
        "导出 OPL standard domain handler refs surface。",
    )
    _add_domain_handler_dispatch_command(
        subparsers,
        "domain-handler-dispatch",
        handle_domain_handler_dispatch,
        "执行 OPL standard domain handler guarded action。",
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
    _add_product_domain_memory_proposal_command(
        subparsers,
        "product-domain-memory-proposal",
        handle_product_domain_memory_proposal,
        "生成 MAG-owned domain memory writeback proposal projection。",
    )
    _add_product_domain_memory_decision_command(
        subparsers,
        "product-domain-memory-decision",
        handle_product_domain_memory_decision,
        "生成 MAG-owned domain memory accept/reject decision projection。",
    )
    _add_product_domain_memory_receipt_evidence_command(
        subparsers,
        "product-domain-memory-receipt-evidence",
        handle_product_domain_memory_receipt_evidence,
        "把 MAG-owned domain memory accept/reject decision 写成 runtime receipt evidence。",
    )
    _add_product_owner_receipt_evidence_command(
        subparsers,
        "product-owner-receipt-evidence",
        handle_product_owner_receipt_evidence,
        "把 OPL-hosted stage attempt closeout 写成 MAG owner receipt runtime evidence。",
    )
    _add_product_live_acceptance_receipt_command(
        subparsers,
        "production-live-acceptance-receipt",
        handle_product_live_acceptance_receipt,
        "把 MAG owner receipt、OPL Agent Lab suite result 与 opl-meta-agent coordination 对账成 production live acceptance receipt projection。",
    )
    _add_product_codex_stage_receipts_command(
        subparsers,
        "codex-stage-receipts",
        handle_product_codex_stage_receipts,
        "把 Codex executor attempt 与独立 review attempt refs 聚合成 stage receipt bundle。",
    )
    _add_product_receipt_readiness_command(
        subparsers,
        "receipt-readiness",
        handle_product_receipt_readiness,
        "把 MAG owner/memory/package/lifecycle receipt refs 聚合成 OPL 可消费 readiness projection。",
    )
    _add_product_opl_owner_payload_response_command(
        subparsers,
        "opl-owner-payload-response",
        handle_product_opl_owner_payload_response,
        "把 MAG receipt/typed-blocker refs 聚合成 OPL owner-payload workorder 可消费 response。",
    )
    _add_product_manifest_sustained_consumption_payload_command(
        subparsers,
        "manifest-sustained-consumption-payload",
        handle_product_manifest_sustained_consumption_payload,
        "校验 App/operator 或 default caller 对 MAG manifest owner-payload 的 sustained consumption refs payload。",
    )
    _add_product_physical_morphology_guard_command(
        subparsers,
        "physical-morphology-guard",
        handle_product_physical_morphology_guard,
        "把 MAG source morphology 分类 refs 聚合成 physical morphology guard projection。",
    )
    _add_product_executor_first_closeout_bundle_command(
        subparsers,
        "executor-first-closeout-bundle",
        handle_product_executor_first_closeout_bundle,
        "把 Codex receipt、operator closeout、physical guard 与可选 evidence/readiness refs 聚合成 executor-first closeout bundle。",
    )
    return parser

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
    if group in PUBLIC_GROUP_COMMANDS and (len(argv) == 1 or argv[1] in {"-h", "--help", "help"}):
        _print_public_group_help(group)
        return 0
    return None


def _normalize_public_command_argv(argv: list[str]) -> list[str]:
    if not argv:
        return argv
    if argv[0] in RETIRED_FLAT_COMMANDS:
        raise SystemExit(f"argument command: invalid choice: '{argv[0]}'")
    if len(argv) >= 3 and (argv[0], argv[1], argv[2]) in PUBLIC_THREE_TOKEN_COMMANDS:
        return [PUBLIC_THREE_TOKEN_COMMANDS[(argv[0], argv[1], argv[2])], *argv[3:]]
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



if __name__ == "__main__":
    entrypoint()
