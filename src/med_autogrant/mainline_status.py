from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from med_autogrant.control_plane import read_current_program_contract
from med_autogrant.public_cli import public_cli_command
from med_autogrant.workspace_types import WorkspaceStateError


SCHEMA_VERSION = 1


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _nonempty_string(value: Any, *, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少合法字符串字段。")
    return value.strip()


def _phase_details() -> dict[str, dict[str, Any]]:
    return {
        "P1": {
            "summary": "旧上游 Hermes-Agent 和本地 journal runtime 只保留 history/proof 语境；默认 session/runtime shell 交给 OPL generated/hosted surface。",
            "entry_points": [
                {
                    "name": "opl_generated_session_shell",
                    "command": "opl generated surface: mag/product-entry-session",
                    "purpose": "由 OPL 生成或托管 session/resume shell；MAG 只返回 grant locator、receipt、verdict refs 与 authority actions。",
                },
                {
                    "name": "grant_authority_entry",
                    "command": public_cli_command("stage-route-report", "--input", "<workspace-path>", "--format", "json"),
                    "purpose": "读取 MAG grant route truth；通用 run/resume/attempt ledger 不再作为 MAG 默认 callable surface。",
                },
            ],
            "exit_criteria": [
                "真实 upstream Hermes-Agent 依赖与连接证据只作为 history/proof/provenance 读取。",
                "runtime-run / runtime-resume / probe-upstream-hermes 不再进入 MAG public CLI、domain-entry catalog、product-entry schema 或 hosted bundle。",
            ],
            "phase_docs": [
                "human_doc:2026_04_11_upstream_hermes_agent_truth_reset_current_truth",
                "human_doc:2026_04_12_upstream_hermes_agent_fast_cutover_current_truth",
            ],
        },
        "P2": {
            "summary": "把 service-safe domain contract、product entry envelope 与 routing truth 收成稳定合同。",
            "entry_points": [
                {
                    "name": "stage_route_report",
                    "command": public_cli_command(
                        "stage-route-report", "--input", "<workspace-path>", "--format", "json"
                    ),
                    "purpose": "查看当前 grant route truth 与推荐 route。",
                },
                {
                    "name": "build_product_entry",
                    "command": public_cli_command(
                        "build-product-entry",
                        "--input",
                        "<workspace-path>",
                        "--entry-mode",
                        "direct",
                        "--task-intent",
                        "<task-intent>",
                        "--format",
                        "json",
                    ),
                    "purpose": "生成 direct / OPL 共用的 lightweight product entry envelope。",
                },
            ],
            "exit_criteria": [
                "MedAutoGrantDomainEntry、product-entry 与 executor_routing_contract 已共同冻结。",
                "hosted contract bundle 已显式导出 domain_entry_contract / schema_contract / authoring_contract。",
            ],
            "phase_docs": [
                "human_doc:2026_04_12_schema_backed_product_entry_and_routing_contract_current_truth",
                "human_doc:2026_04_12_author_side_executor_routing_contract_current_truth",
                "human_doc:2026_04_12_hosted_contract_bundle_entry_and_route_catalog_current_truth",
            ],
        },
        "P3": {
            "summary": "证明 hosted caller / future OPL caller 已可直接消费冻结合同，而无需 repo-local helper。",
            "entry_points": [
                {
                    "name": "build_hosted_contract_bundle",
                    "command": public_cli_command(
                        "build-hosted-contract-bundle",
                        "--final-package",
                        "<final-package-path>",
                        "--output",
                        "<hosted-bundle-path>",
                        "--format",
                        "json",
                    ),
                    "purpose": "构造 hosted-friendly contract bundle 给外部 caller 消费。",
                },
                {
                    "name": "build_opl_handoff_entry",
                    "command": public_cli_command(
                        "build-product-entry",
                        "--input",
                        "<workspace-path>",
                        "--entry-mode",
                        "opl-handoff",
                        "--task-intent",
                        "<task-intent>",
                        "--format",
                        "json",
                    ),
                    "purpose": "输出 future OPL handoff 可直接消费的 lightweight envelope。",
                },
            ],
            "exit_criteria": [
                "external caller 可以直接消费 domain_entry_contract / schema_contract / authoring_contract。",
                "hosted caller / OPL caller 不再需要 repo-local helper 才能构造 request。",
            ],
            "phase_docs": [
                "human_doc:2026_04_12_hosted_caller_consumption_proof_current_truth",
                "human_doc:2026_04_12_hosted_contract_bundle_entry_and_route_catalog_current_truth",
            ],
        },
        "P4": {
            "summary": "把 direct grant product 面逐步收成当前用户 inbox shell，并以 authoring quality 作为主任务完成语义。",
            "entry_points": [
                {
                    "name": "mainline_status",
                    "command": public_cli_command("mainline-status", "--format", "json"),
                    "purpose": "先看理想目标、阶段梯子、当前 tranche 与 remaining gaps。",
                },
                {
                    "name": "grant_cockpit",
                    "command": public_cli_command(
                        "grant-cockpit", "--input", "<workspace-path>", "--format", "json"
                    ),
                    "purpose": "看 grant 当前 workspace overview、alerts 与只读 projection。",
                },
                {
                    "name": "grant_user_loop",
                    "command": public_cli_command(
                        "grant-user-loop",
                        "--input",
                        "<workspace-path>",
                        "--task-intent",
                        "<task-intent>",
                        "--format",
                        "json",
                    ),
                    "purpose": "把 mainline snapshot、direct-entry composition 与推荐动作回路收成一处。",
                },
                {
                    "name": "build_submission_ready_package",
                    "command": public_cli_command(
                        "build-submission-ready-package",
                        "--input",
                        "<workspace-path>",
                        "--output-dir",
                        "<submission-ready-output-dir>",
                        "--format",
                        "json",
                    ),
                    "purpose": "对已冻结且材料齐备的 workspace 一次性导出本地 submission-ready 交付目录。",
                },
            ],
            "exit_criteria": [
                "用户不再需要自己拼 program docs 与 route commands 才能理解当前 grant 主线。",
                "当前 direct grant user loop 已能稳定暴露 mainline snapshot、entry shell 与 next action。",
                "对满足冻结 gate 与材料完备条件的 workspace，当前系统已能 fail-closed 地一键导出本地 submission-ready 包。",
                "主任务完成判据保持正文科学性与 authoring quality 优先，不把 submission-ready 导出写成唯一完成条件。",
                "形式审查与客观补件默认进入 TODO 与显式唤醒链路，只有直接破坏科学论证时才升级为 blocker。",
                "已锁定 funder/family 的任务线维持同一 funder 语义闭环推进，不做 opportunistic 跨 funder 切换。",
                "这层 shell 仍然诚实保持 controller-owned，不越界声称 mature frontend / hosted runtime 已完成。",
            ],
            "phase_docs": [
                "human_doc:2026_04_12_opl_aligned_ideal_target_and_phase_map_current_truth",
                "human_doc:2026_04_12_p4a_direct_grant_cockpit_and_progress_projection_current_truth",
                "human_doc:2026_04_12_p4b_direct_grant_entry_composition_current_truth",
                "human_doc:2026_04_12_p4c_mainline_status_and_grant_user_loop_current_truth",
                "human_doc:2026_04_13_full_grant_authoring_executor_current_truth",
                "human_doc:2026_04_13_p4e_schema_backed_product_status_and_manifest_current_truth",
                "human_doc:2026_04_13_p4f_local_submission_ready_package_current_truth",
            ],
        },
    }


def _completed_records() -> list[dict[str, str]]:
    return [
        {
            "record_id": "P1",
            "title": "explicit Hermes proof lane",
            "summary": "真实上游 Hermes-Agent 只保留为显式 proof lane；默认 runtime owner 是 Codex CLI。",
        },
        {
            "record_id": "P2",
            "title": "service-safe domain contract convergence",
            "summary": "domain entry / product entry / executor routing 已共同冻结。",
        },
        {
            "record_id": "P3",
            "title": "hosted caller / OPL consumption proof",
            "summary": "external caller 已可直接消费 hosted bundle 与 domain entry contract。",
        },
        {
            "record_id": "P4.A",
            "title": "direct grant progress / cockpit projection",
            "summary": "grant-progress / grant-cockpit 已 landed 为 controller-owned projection。",
        },
        {
            "record_id": "P4.B",
            "title": "direct grant entry composition",
            "summary": "grant-direct-entry 已 landed，收成 direct / OPL 两份 shared envelope。",
        },
        {
            "record_id": "P4.C",
            "title": "mainline status and grant user loop",
            "summary": "mainline-status / mainline-phase / grant-user-loop 已 landed，收成当前 user inbox shell。",
        },
        {
            "record_id": "P4.D",
            "title": "full grant authoring executor landing",
            "summary": "direction_screening -> frozen 的全链 authoring executor 已 landed 到 service-safe command surface。",
        },
        {
            "record_id": "P4.E",
            "title": "schema-backed product status and manifest contract landing",
            "summary": "product-entry-manifest / product-status 已 landed 为独立 schema-backed、generation-time fail-closed 的 direct product status contract。",
        },
        {
            "record_id": "P4.F",
            "title": "local submission-ready package landing",
            "summary": "build-submission-ready-package 已 landed，可对满足冻结与材料完备条件的 workspace 一键导出本地 submission-ready 交付目录。",
        },
        {
            "record_id": "P4.G",
            "title": "authoring-quality-first completion semantics alignment",
            "summary": "主任务完成语义已收口到正文科学性与 authoring quality；submission-ready 导出、形式补件与 funder continuity 语义已统一对齐。",
        },
    ]


def _remaining_gaps() -> list[str]:
    return [
        "mature direct grant Web UI / hosted runtime 仍未 landed。",
        "真实 OPL stage attempt 长跑、human-gate signal/query 与 App 可视化仍未由本仓证明。",
        "当前 product 面仍然是 CLI/controller shell，而不是完整 standalone frontend。",
        "图件生成、Word/PDF 定稿与最终版式审查仍未产品化。",
        "不会凭空补齐真实预实验、代表作、在研项目与图片素材。",
        "外部官网提交流程仍未执行，当前只导出本地 submission-ready package。",
    ]


def _explicitly_not_now() -> list[str]:
    return [
        "把 OPL stage-led framework 写成由 MAG 仓持有或已完成 production long-run soak。",
        "提前扩 family、提前做 Human-in-the-loop sibling。",
        "把 repo-local helper 重新写回 runtime owner。",
        "把本地 submission-ready package 写成已完成外部官网提交。",
        "把形式审查/客观补件默认写成正文 authoring 硬阻塞。",
        "把已锁定 funder 任务线写成 opportunistic 跨 funder 切换。",
    ]


def _next_focus() -> list[str]:
    return [
        "继续把 `product-entry-manifest` / `product-status` 当作当前 direct grant product entry surface contract，并让 `grant-progress`、`grant-cockpit`、`grant-direct-entry` 与 `grant-user-loop` 继续对齐同一份 product entry surface truth。",
        "继续把 `family_orchestration` companion 从 action graph / human gate preview 深压到 family product-entry manifest v2、event envelope 与 checkpoint lineage contract，并保持 route status 直接读取共享 author-side route truth。",
        "把形式审查/客观补件统一收口到 TODO 与显式唤醒链路，并仅在直接破坏科学论证时升级为 blocker。",
        "对已锁定 funder/family 的任务线保持 continuity，不引入 opportunistic 跨 funder 切换叙事。",
    ]


def _resolve_phase_ladder(current_program: dict[str, Any]) -> list[dict[str, Any]]:
    details = _phase_details()
    phase_map = current_program.get("phase_map")
    if not isinstance(phase_map, list):
        raise WorkspaceStateError("CURRENT_PROGRAM contract 缺少合法 phase_map。")

    ladder: list[dict[str, Any]] = []
    for item in phase_map:
        if not isinstance(item, dict):
            raise WorkspaceStateError("CURRENT_PROGRAM contract phase_map 元素必须是 object。")
        phase_id = _nonempty_string(item.get("phase_id"), context="CURRENT_PROGRAM.phase_map.phase_id")
        phase_name = _nonempty_string(item.get("phase_name"), context="CURRENT_PROGRAM.phase_map.phase_name")
        status = _nonempty_string(item.get("status"), context="CURRENT_PROGRAM.phase_map.status")
        detail = details.get(phase_id)
        if detail is None:
            raise WorkspaceStateError(f"未登记的 mainline phase: {phase_id}")
        ladder.append(
            {
                "phase_id": phase_id,
                "phase_name": phase_name,
                "status": status,
                "usable_now": True,
                "summary": detail["summary"],
                "entry_points": list(detail["entry_points"]),
                "exit_criteria": list(detail["exit_criteria"]),
                "phase_docs": list(detail["phase_docs"]),
            }
        )
    return ladder


def _resolve_current_phase(*, phase_ladder: list[dict[str, Any]], active_phase: str) -> dict[str, Any]:
    active_phase_id = _nonempty_string(active_phase, context="CURRENT_PROGRAM.runtime_owner.active_phase").split()[0]
    for phase in phase_ladder:
        if phase["phase_id"] == active_phase_id:
            return dict(phase)
    raise WorkspaceStateError(f"active_phase 没有对应的 phase ladder 卡片: {active_phase}")


def read_mainline_status() -> dict[str, Any]:
    current_program = read_current_program_contract()
    runtime_owner = current_program.get("runtime_owner")
    ideal_target = current_program.get("ideal_target")
    if not isinstance(runtime_owner, dict):
        raise WorkspaceStateError("CURRENT_PROGRAM contract 缺少合法 runtime_owner。")
    if not isinstance(ideal_target, dict):
        raise WorkspaceStateError("CURRENT_PROGRAM contract 缺少合法 ideal_target。")

    phase_ladder = _resolve_phase_ladder(current_program)
    current_phase = _resolve_current_phase(
        phase_ladder=phase_ladder,
        active_phase=_nonempty_string(runtime_owner.get("active_phase"), context="CURRENT_PROGRAM.runtime_owner.active_phase"),
    )
    current_owner_line = _nonempty_string(
        runtime_owner.get("current_owner_line"),
        context="CURRENT_PROGRAM.runtime_owner.current_owner_line",
    )
    active_phase = _nonempty_string(runtime_owner.get("active_phase"), context="CURRENT_PROGRAM.runtime_owner.active_phase")
    active_tranche = _nonempty_string(
        runtime_owner.get("active_tranche"),
        context="CURRENT_PROGRAM.runtime_owner.active_tranche",
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _utc_now(),
        "program_id": _nonempty_string(current_program.get("program_id"), context="CURRENT_PROGRAM.program_id"),
        "ideal_target": dict(ideal_target),
        "current_line": {
            "current_owner_line": current_owner_line,
        },
        "current_focus": {
            "summary": _nonempty_string(current_phase.get("summary"), context="mainline.current_focus.summary"),
            "focus_items": _next_focus(),
        },
        "completed_records": _completed_records(),
        "remaining_gaps": _remaining_gaps(),
        "maintainer_references": {
            "runtime_owner": {
                "current_owner_line": current_owner_line,
                "active_phase": active_phase,
                "active_tranche": active_tranche,
            },
            "current_record_detail": current_phase,
            "phase_ladder": phase_ladder,
            "explicitly_not_now": _explicitly_not_now(),
        },
    }


def read_mainline_phase_status(selector: str) -> dict[str, Any]:
    resolved_selector = _nonempty_string(selector, context="mainline_phase.selector")
    status_payload = read_mainline_status()
    maintainer_references = dict(status_payload["maintainer_references"])
    current_record_detail = dict(maintainer_references["current_record_detail"])
    phase_ladder = list(maintainer_references["phase_ladder"])
    if resolved_selector == "current":
        record_detail = dict(current_record_detail)
    elif resolved_selector == "next":
        record_detail = next((dict(item) for item in phase_ladder if item["status"] == "next"), dict(current_record_detail))
    else:
        record_detail = next((dict(item) for item in phase_ladder if item["phase_id"] == resolved_selector), None)
        if record_detail is None:
            raise WorkspaceStateError(f"mainline-phase 不支持 selector: {resolved_selector}")
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _utc_now(),
        "program_id": status_payload["program_id"],
        "current_line": dict(status_payload["current_line"]),
        "maintainer_reference": {
            "selector": resolved_selector,
            "record_detail": record_detail,
        },
    }


def render_mainline_status_markdown(payload: dict[str, Any]) -> str:
    current_line = dict(payload.get("current_line") or {})
    current_focus = dict(payload.get("current_focus") or {})
    maintainer_references = dict(payload.get("maintainer_references") or {})
    runtime_owner = dict(maintainer_references.get("runtime_owner") or {})
    lines = [
        "# Mainline Status",
        "",
        f"- 当前 program: `{payload.get('program_id')}`",
        f"- 当前 line: `{current_line.get('current_owner_line') or 'unknown'}`",
        f"- 当前 focus: `{current_focus.get('summary') or 'unknown'}`",
        "",
        "## Ideal Target",
        "",
    ]
    ideal_target = dict(payload.get("ideal_target") or {})
    for key in ("family_top_entry", "domain_direct_entry", "runtime_substrate_owner", "authoring_truth_owner"):
        if ideal_target.get(key):
            lines.append(f"- {key}: `{ideal_target.get(key)}`")
    lines.extend(["", "## Current Focus Items", ""])
    for item in current_focus.get("focus_items") or []:
        lines.append(f"- {item}")
    lines.extend(["", "## Completed Records", ""])
    for item in payload.get("completed_records") or []:
        lines.append(f"- `{item.get('record_id')}`: {item.get('summary')}")
    lines.extend(["", "## Remaining Gaps", ""])
    for item in payload.get("remaining_gaps") or []:
        lines.append(f"- {item}")
    lines.extend(["", "## Maintainer References", ""])
    lines.append(f"- active_phase: `{runtime_owner.get('active_phase') or 'unknown'}`")
    lines.append(f"- active_tranche: `{runtime_owner.get('active_tranche') or 'unknown'}`")
    lines.append(
        f"- detail query: `{public_cli_command('mainline-phase', '--phase', 'current', '--format', 'json')}`"
    )
    return "\n".join(lines)


def render_mainline_phase_markdown(payload: dict[str, Any]) -> str:
    reference = dict(payload.get("maintainer_reference") or {})
    record_detail = dict(reference.get("record_detail") or {})
    current_line = dict(payload.get("current_line") or {})
    lines = [
        "# Mainline Maintainer Reference",
        "",
        f"- 当前 line: `{current_line.get('current_owner_line') or 'unknown'}`",
        f"- 维护参考 selector: `{reference.get('selector') or 'unknown'}`",
        f"- 维护参考记录: `{record_detail.get('phase_id')}`",
        f"- 记录名称: `{record_detail.get('phase_name')}`",
        f"- 记录状态: `{record_detail.get('status')}`",
    ]
    if record_detail.get("summary"):
        lines.append(f"- 当前摘要: {record_detail.get('summary')}")
    lines.extend(["", "## Entry Points", ""])
    for item in record_detail.get("entry_points") or []:
        lines.append(f"- `{item.get('name')}`: `{item.get('command')}`")
    lines.extend(["", "## Exit Criteria", ""])
    for item in record_detail.get("exit_criteria") or []:
        lines.append(f"- {item}")
    return "\n".join(lines)
