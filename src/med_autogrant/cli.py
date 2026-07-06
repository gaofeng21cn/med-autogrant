from __future__ import annotations

import argparse
import json
import sys

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from med_autogrant.public_cli import (
    INTERNAL_TO_PUBLIC_COMMAND,
    PUBLIC_COMMAND_GROUP_SUMMARIES,
    PUBLIC_COMMAND_ORDER,
    PUBLIC_GROUP_COMMANDS,
)
from med_autogrant.workspace import load_workspace_document
from med_autogrant.workspace_types import WorkspaceError, WorkspaceStateError
from med_autogrant.cli_rendering_parts import _render_text
from med_autogrant.cli_parts import handlers, parser_adders


RETIRED_FLAT_COMMANDS = frozenset(INTERNAL_TO_PUBLIC_COMMAND)


def _extract_workspace_context_for_error(args: argparse.Namespace) -> dict[str, object]:
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

    parser_adders._add_simple_command(
        subparsers,
        "foundry-status",
        handlers.handle_foundry_status,
        "输出 MAG 的 OPL Foundry Agent series 状态。",
    )
    parser_adders._add_simple_command(
        subparsers,
        "foundry-inspect",
        handlers.handle_foundry_inspect,
        "检查 MAG 的 Foundry Agent identity、输入输出与 authority profile。",
    )
    parser_adders._add_simple_command(
        subparsers,
        "foundry-interfaces",
        handlers.handle_foundry_interfaces,
        "列出 MAG 的 Foundry Agent public interface grammar。",
    )
    parser_adders._add_simple_command(
        subparsers,
        "foundry-validate",
        handlers.handle_foundry_validate,
        "校验 MAG 的 Foundry Agent series contract 与 CLI command surface。",
    )
    parser_adders._add_simple_command(
        subparsers,
        "foundry-doctor",
        handlers.handle_foundry_doctor,
        "输出 MAG 的 Foundry Agent authority/currentness diagnostic。",
    )
    parser_adders._add_simple_command(
        subparsers,
        "foundry-peers",
        handlers.handle_foundry_peers,
        "列出同系列 Foundry Agent peers 与 MAG topology profile。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "validate-workspace",
        handlers.handle_validate_workspace,
        "校验 NSFC workspace。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "summarize-workspace",
        handlers.handle_summarize_workspace,
        "输出当前 workspace 摘要。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "grant-intake-audit",
        handlers.handle_grant_intake_audit,
        "输出 grant intake audit surface。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "grant-evidence-grounding",
        handlers.handle_grant_evidence_grounding,
        "输出 grant evidence grounding surface。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "grant-quality-scorecard",
        handlers.handle_grant_quality_scorecard,
        "输出当前版本的质量治理 scorecard。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "grant-quality-closure-dossier",
        handlers.handle_grant_quality_closure_dossier,
        "输出当前版本的质量 closure dossier。",
    )
    parser_adders._add_quality_diff_command(
        subparsers,
        "grant-quality-diff",
        handlers.handle_grant_quality_diff,
        "对比两个版本的质量 scorecard 与问题关闭进度。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "discover-funding-opportunities",
        handlers.handle_discover_funding_opportunities,
        "从材料与方向 hint 发现 funding opportunity pool。",
    )
    parser_adders._add_refresh_cache_command(
        subparsers,
        "refresh-funding-opportunities-cache",
        handlers.handle_refresh_funding_opportunities_cache,
        "刷新官方 funding discovery cache，支持默认 runtime-state 落点。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "select-project-profile",
        handlers.handle_select_project_profile,
        "从材料池与 funding pool 中选择推荐 project profile。",
    )
    parser_adders._add_initialize_intake_workspace_command(
        subparsers,
        "initialize-intake-workspace",
        handlers.handle_initialize_intake_workspace,
        "根据推荐 project profile 初始化 input_intake workspace。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "next-step",
        handlers.handle_next_step,
        "输出当前 workspace 的下一步建议。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "critique-summary",
        handlers.handle_critique_summary,
        "输出当前激活导师批注摘要。",
    )
    parser_adders._add_workspace_command(
        subparsers,
        "stage-route-report",
        handlers.handle_stage_route_report,
        "按固定 stage route 聚合输出当前 workspace 状态。",
    )
    parser_adders._add_simple_command(
        subparsers,
        "mainline-status",
        handlers.handle_mainline_status,
        "输出当前 repo 主线的 current line / current focus / completed records / remaining gaps。",
    )
    parser_adders._add_phase_command(
        subparsers,
        "mainline-phase",
        handlers.handle_mainline_phase,
        "输出 maintainer reference 下某个记录卡片的入口与退出条件。",
    )
    parser_adders._add_domain_handler_export_command(
        subparsers,
        "domain-handler-export",
        handlers.handle_domain_handler_export,
        "导出 OPL standard domain handler refs surface。",
    )
    parser_adders._add_domain_handler_dispatch_command(
        subparsers,
        "domain-handler-dispatch",
        handlers.handle_domain_handler_dispatch,
        "执行 OPL standard domain handler guarded action。",
    )
    parser_adders._add_artifact_bundle_command(
        subparsers,
        "execute-direction-screening-pass",
        handlers.handle_execute_direction_screening_pass,
        "执行方向筛选 pass，生成 direction_screening workspace。",
    )
    parser_adders._add_artifact_bundle_command(
        subparsers,
        "execute-question-refinement-pass",
        handlers.handle_execute_question_refinement_pass,
        "执行科学问题提纯 pass，生成 question_refinement workspace。",
    )
    parser_adders._add_artifact_bundle_command(
        subparsers,
        "execute-argument-building-pass",
        handlers.handle_execute_argument_building_pass,
        "执行立项依据构建 pass，生成 argument_building workspace。",
    )
    parser_adders._add_artifact_bundle_command(
        subparsers,
        "execute-fit-alignment-pass",
        handlers.handle_execute_fit_alignment_pass,
        "执行 applicant-problem fit 对齐 pass，生成 fit_alignment workspace。",
    )
    parser_adders._add_artifact_bundle_command(
        subparsers,
        "execute-outline-pass",
        handlers.handle_execute_outline_pass,
        "执行提纲冻结 pass，生成 outline workspace。",
    )
    parser_adders._add_artifact_bundle_command(
        subparsers,
        "execute-drafting-pass",
        handlers.handle_execute_drafting_pass,
        "执行正文起草 pass，生成 drafting workspace。",
    )
    parser_adders._add_artifact_bundle_command(
        subparsers,
        "build-artifact-bundle",
        handlers.handle_build_artifact_bundle,
        "把当前 workspace 的已冻结对象写成本地 artifact bundle。",
    )
    parser_adders._add_revision_executor_command(
        subparsers,
        "execute-critique-pass",
        handlers.handle_execute_critique_pass,
        "通过 Codex CLI critique executor 生成导师式批注与 revision plan。",
    )
    parser_adders._add_critique_loop_command(
        subparsers,
        "execute-critique-revision-loop",
        handlers.handle_execute_critique_revision_loop,
        "执行多轮 critique/revision closed loop，直到通过或 fail-closed 停止。",
    )
    parser_adders._add_mainline_loop_command(
        subparsers,
        "execute-authoring-mainline-loop",
        handlers.handle_execute_authoring_mainline_loop,
        "执行跨 question/argument/fit/drafting/critique/revision/frozen 的全链路主线 loop。",
    )
    parser_adders._add_grant_autonomy_controller_command(
        subparsers,
        "execute-grant-autonomy-controller",
        handlers.handle_execute_grant_autonomy_controller,
        "执行长期自治 controller，调度 pre-workspace、mainline 与 quality gate。",
    )
    parser_adders._add_revision_executor_command(
        subparsers,
        "execute-revision-pass",
        handlers.handle_execute_revision_pass,
        "按冻结的 section-level deterministic contract 执行 revision pass。",
    )
    parser_adders._add_artifact_bundle_command(
        subparsers,
        "execute-freeze-pass",
        handlers.handle_execute_freeze_pass,
        "执行送审前冻结 pass，生成 frozen workspace。",
    )
    parser_adders._add_final_package_command(
        subparsers,
        "build-final-package",
        handlers.handle_build_final_package,
        "把 freeze-ready / submission-frozen workspace 写成本地 final package。",
    )
    parser_adders._add_hosted_contract_bundle_command(
        subparsers,
        "build-hosted-contract-bundle",
        handlers.handle_build_hosted_contract_bundle,
        "把 final package 写成 hosted-friendly contract bundle。",
    )
    parser_adders._add_submission_ready_package_command(
        subparsers,
        "build-submission-ready-package",
        handlers.handle_build_submission_ready_package,
        "把 frozen workspace 一次性写成 submission-ready 本地交付目录。",
    )
    parser_adders._add_product_domain_memory_proposal_command(
        subparsers,
        "product-domain-memory-proposal",
        handlers.handle_product_domain_memory_proposal,
        "生成 MAG-owned domain memory writeback proposal projection。",
    )
    parser_adders._add_product_domain_memory_decision_command(
        subparsers,
        "product-domain-memory-decision",
        handlers.handle_product_domain_memory_decision,
        "生成 MAG-owned domain memory accept/reject decision projection。",
    )
    parser_adders._add_product_domain_memory_receipt_evidence_command(
        subparsers,
        "product-domain-memory-receipt-evidence",
        handlers.handle_product_domain_memory_receipt_evidence,
        "把 MAG-owned domain memory accept/reject decision 写成 runtime receipt evidence。",
    )
    parser_adders._add_product_owner_receipt_evidence_command(
        subparsers,
        "product-owner-receipt-evidence",
        handlers.handle_product_owner_receipt_evidence,
        "把 OPL-hosted stage attempt closeout 写成 MAG owner receipt runtime evidence。",
    )
    parser_adders._add_product_live_acceptance_receipt_command(
        subparsers,
        "production-live-acceptance-receipt",
        handlers.handle_product_live_acceptance_receipt,
        "把 MAG owner receipt、OPL Agent Lab suite result 与 opl-meta-agent coordination 对账成 production live acceptance receipt projection。",
    )
    parser_adders._add_product_codex_stage_receipts_command(
        subparsers,
        "codex-stage-receipts",
        handlers.handle_product_codex_stage_receipts,
        "把 Codex executor attempt 与独立 review attempt refs 聚合成 stage receipt bundle。",
    )
    parser_adders._add_product_receipt_readiness_command(
        subparsers,
        "receipt-readiness",
        handlers.handle_product_receipt_readiness,
        "把 MAG owner/memory/package/lifecycle receipt refs 聚合成 OPL 可消费 readiness projection。",
    )
    parser_adders._add_product_opl_owner_payload_response_command(
        subparsers,
        "opl-owner-payload-response",
        handlers.handle_product_opl_owner_payload_response,
        "把 MAG receipt/typed-blocker refs 聚合成 OPL owner-payload workorder 可消费 response。",
    )
    parser_adders._add_product_manifest_sustained_consumption_payload_command(
        subparsers,
        "manifest-sustained-consumption-payload",
        handlers.handle_product_manifest_sustained_consumption_payload,
        "校验 App/operator 或 default caller 对 MAG manifest owner-payload 的 sustained consumption refs payload。",
    )
    parser_adders._add_product_physical_morphology_guard_command(
        subparsers,
        "physical-morphology-guard",
        handlers.handle_product_physical_morphology_guard,
        "把 MAG source morphology 分类 refs 聚合成 physical morphology guard projection。",
    )
    parser_adders._add_simple_command(
        subparsers,
        "source-purity-guard-readback",
        handlers.handle_product_source_purity_guard_readback,
        "输出 MAG strict source-purity no-second-truth guard readback。",
    )
    parser_adders._add_product_executor_first_closeout_bundle_command(
        subparsers,
        "executor-first-closeout-bundle",
        handlers.handle_product_executor_first_closeout_bundle,
        "把 Codex receipt、operator closeout、physical guard 与可选 evidence/readiness refs 聚合成 executor-first closeout bundle。",
    )
    return parser

def _print_public_help() -> None:
    lines = [
        "Usage: medautogrant <group> <command> [options]",
        "",
        "Series: OPL Foundry Agent",
        "Agent id: medautogrant",
        "Ordinary path: workspace/work/stage/run/vault/handoff/connect",
        "Executable command surface: medautogrant",
        "Brand shorthand: mag (package alias; do not use as PATH readiness evidence on macOS)",
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
            "  medautogrant foundry status --format json",
            "  <med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli foundry status --json",
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
