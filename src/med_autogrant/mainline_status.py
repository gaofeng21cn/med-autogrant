from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from med_autogrant.control_plane import read_current_program_contract
from med_autogrant.workspace import WorkspaceStateError


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
            "summary": "冻结真实上游 Hermes-Agent 连接证据，并把 runtime substrate owner 诚实切到上游。",
            "entry_points": [
                {
                    "name": "probe_upstream_hermes",
                    "command": "uv run python -m med_autogrant probe-upstream-hermes --format json",
                    "purpose": "核对真实 upstream Hermes-Agent 依赖、入口与 session substrate 证据。",
                },
                {
                    "name": "run_local",
                    "command": "uv run python -m med_autogrant run-local --input <workspace-path> --format json",
                    "purpose": "走当前 Hermes-backed substrate 的单次本地主循环。",
                },
            ],
            "exit_criteria": [
                "真实 upstream Hermes-Agent 依赖与连接证据已经冻结。",
                "run-local / resume-local 不再由 repo-local helper 主责 substrate durability。",
            ],
            "phase_docs": [
                "docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md",
                "docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md",
            ],
        },
        "P2": {
            "summary": "把 service-safe domain contract、product entry envelope 与 routing truth 收成稳定合同。",
            "entry_points": [
                {
                    "name": "stage_route_report",
                    "command": "uv run python -m med_autogrant stage-route-report --input <workspace-path> --format json",
                    "purpose": "查看当前 grant route truth 与推荐 route。",
                },
                {
                    "name": "build_product_entry",
                    "command": (
                        "uv run python -m med_autogrant build-product-entry "
                        "--input <workspace-path> --entry-mode direct --task-intent <task-intent> --format json"
                    ),
                    "purpose": "生成 direct / OPL 共用的 lightweight product entry envelope。",
                },
            ],
            "exit_criteria": [
                "MedAutoGrantDomainEntry、product-entry 与 executor_routing_contract 已共同冻结。",
                "hosted contract bundle 已显式导出 domain_entry_contract / schema_contract / authoring_contract。",
            ],
            "phase_docs": [
                "docs/specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md",
                "docs/specs/2026-04-12-author-side-executor-routing-contract-current-truth.md",
                "docs/specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md",
            ],
        },
        "P3": {
            "summary": "证明 hosted caller / future OPL caller 已可直接消费冻结合同，而无需 repo-local helper。",
            "entry_points": [
                {
                    "name": "build_hosted_contract_bundle",
                    "command": (
                        "uv run python -m med_autogrant build-hosted-contract-bundle "
                        "--final-package <final-package-path> --output <hosted-bundle-path> --format json"
                    ),
                    "purpose": "构造 hosted-friendly contract bundle 给外部 caller 消费。",
                },
                {
                    "name": "build_opl_handoff_entry",
                    "command": (
                        "uv run python -m med_autogrant build-product-entry "
                        "--input <workspace-path> --entry-mode opl-handoff --task-intent <task-intent> --format json"
                    ),
                    "purpose": "输出 future OPL handoff 可直接消费的 lightweight envelope。",
                },
            ],
            "exit_criteria": [
                "external caller 可以直接消费 domain_entry_contract / schema_contract / authoring_contract。",
                "hosted caller / OPL caller 不再需要 repo-local helper 才能构造 request。",
            ],
            "phase_docs": [
                "docs/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md",
                "docs/specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md",
            ],
        },
        "P4": {
            "summary": "把 direct grant product 面逐步收成当前用户 inbox shell，而不越界写成 mature Web UI 或 hosted runtime。",
            "entry_points": [
                {
                    "name": "mainline_status",
                    "command": "uv run python -m med_autogrant mainline-status --format json",
                    "purpose": "先看理想目标、阶段梯子、当前 tranche 与 remaining gaps。",
                },
                {
                    "name": "grant_cockpit",
                    "command": "uv run python -m med_autogrant grant-cockpit --input <workspace-path> --format json",
                    "purpose": "看 grant 当前 workspace overview、alerts 与只读 projection。",
                },
                {
                    "name": "grant_user_loop",
                    "command": (
                        "uv run python -m med_autogrant grant-user-loop "
                        "--input <workspace-path> --task-intent <task-intent> --format json"
                    ),
                    "purpose": "把 mainline snapshot、direct-entry composition 与推荐动作回路收成一处。",
                },
            ],
            "exit_criteria": [
                "用户不再需要自己拼 program docs 与 route commands 才能理解当前 grant 主线。",
                "当前 direct grant user loop 已能稳定暴露 mainline snapshot、entry shell 与 next action。",
                "这层 shell 仍然诚实保持 controller-owned，不越界声称 mature frontend / hosted runtime 已完成。",
            ],
            "phase_docs": [
                "docs/specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md",
                "docs/specs/2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md",
                "docs/specs/2026-04-12-p4b-direct-grant-entry-composition-current-truth.md",
                "docs/specs/2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md",
            ],
        },
    }


def _completed_tranches() -> list[dict[str, str]]:
    return [
        {
            "tranche_id": "P1",
            "title": "Hermes substrate cutover",
            "summary": "真实上游 Hermes-Agent substrate 已接住 runtime owner。",
        },
        {
            "tranche_id": "P2",
            "title": "service-safe domain contract convergence",
            "summary": "domain entry / product entry / executor routing 已共同冻结。",
        },
        {
            "tranche_id": "P3",
            "title": "hosted caller / OPL consumption proof",
            "summary": "external caller 已可直接消费 hosted bundle 与 domain entry contract。",
        },
        {
            "tranche_id": "P4.A",
            "title": "direct grant progress / cockpit projection",
            "summary": "grant-progress / grant-cockpit 已 landed 为 controller-owned projection。",
        },
        {
            "tranche_id": "P4.B",
            "title": "direct grant entry composition",
            "summary": "grant-direct-entry 已 landed，收成 direct / OPL 两份 shared envelope。",
        },
        {
            "tranche_id": "P4.C",
            "title": "mainline status and grant user loop",
            "summary": "mainline-status / mainline-phase / grant-user-loop 已 landed，收成当前 user inbox shell。",
        },
    ]


def _remaining_gaps() -> list[str]:
    return [
        "mature direct grant Web UI / hosted runtime 仍未 landed。",
        "direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / frozen 这些 pending route 仍不能被写成已 landed executor。",
        "当前 product 面仍然是 CLI/controller shell，而不是完整 standalone frontend。",
    ]


def _explicitly_not_now() -> list[str]:
    return [
        "把 OPL Gateway 写成本仓已 landed。",
        "提前扩 family、提前做 Human-in-the-loop sibling。",
        "把 repo-local helper 重新写回 runtime owner。",
    ]


def _next_focus() -> list[str]:
    return [
        "继续把 `grant-user-loop` 当作当前 direct grant user inbox shell，并保持主线 snapshot / route action / product entry truth 对齐。",
        "继续用 fresh proof 验证 critique / revision / final package / hosted contract bundle 在 Hermes substrate 上不漂移。",
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
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _utc_now(),
        "program_id": _nonempty_string(current_program.get("program_id"), context="CURRENT_PROGRAM.program_id"),
        "ideal_target": dict(ideal_target),
        "current_runtime_owner": {
            "current_owner_line": _nonempty_string(
                runtime_owner.get("current_owner_line"),
                context="CURRENT_PROGRAM.runtime_owner.current_owner_line",
            ),
            "active_phase": _nonempty_string(runtime_owner.get("active_phase"), context="CURRENT_PROGRAM.runtime_owner.active_phase"),
            "active_tranche": _nonempty_string(
                runtime_owner.get("active_tranche"),
                context="CURRENT_PROGRAM.runtime_owner.active_tranche",
            ),
        },
        "current_phase": current_phase,
        "phase_ladder": phase_ladder,
        "completed_tranches": _completed_tranches(),
        "remaining_gaps": _remaining_gaps(),
        "explicitly_not_now": _explicitly_not_now(),
        "next_focus": _next_focus(),
    }


def read_mainline_phase_status(selector: str) -> dict[str, Any]:
    resolved_selector = _nonempty_string(selector, context="mainline_phase.selector")
    status_payload = read_mainline_status()
    phase_ladder = list(status_payload["phase_ladder"])
    if resolved_selector == "current":
        phase = dict(status_payload["current_phase"])
    elif resolved_selector == "next":
        phase = next((dict(item) for item in phase_ladder if item["status"] == "next"), dict(status_payload["current_phase"]))
    else:
        phase = next((dict(item) for item in phase_ladder if item["phase_id"] == resolved_selector), None)
        if phase is None:
            raise WorkspaceStateError(f"mainline-phase 不支持 selector: {resolved_selector}")
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _utc_now(),
        "program_id": status_payload["program_id"],
        "current_runtime_owner": dict(status_payload["current_runtime_owner"]),
        "phase": phase,
    }


def render_mainline_status_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Mainline Status",
        "",
        f"- program_id: `{payload.get('program_id')}`",
        f"- active_phase: `{((payload.get('current_runtime_owner') or {}).get('active_phase') or 'unknown')}`",
        f"- active_tranche: `{((payload.get('current_runtime_owner') or {}).get('active_tranche') or 'unknown')}`",
        "",
        "## Ideal Target",
        "",
    ]
    ideal_target = dict(payload.get("ideal_target") or {})
    for key in ("family_top_entry", "domain_direct_entry", "runtime_substrate_owner", "authoring_truth_owner"):
        if ideal_target.get(key):
            lines.append(f"- {key}: `{ideal_target.get(key)}`")
    lines.extend(["", "## Phase Ladder", ""])
    for item in payload.get("phase_ladder") or []:
        lines.append(
            f"- `{item.get('phase_id')}` `{item.get('phase_name')}`: status=`{item.get('status')}`; {item.get('summary')}"
        )
    lines.extend(["", "## Completed Tranches", ""])
    for item in payload.get("completed_tranches") or []:
        lines.append(f"- `{item.get('tranche_id')}`: {item.get('summary')}")
    lines.extend(["", "## Remaining Gaps", ""])
    for item in payload.get("remaining_gaps") or []:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Focus", ""])
    for item in payload.get("next_focus") or []:
        lines.append(f"- {item}")
    return "\n".join(lines)


def render_mainline_phase_markdown(payload: dict[str, Any]) -> str:
    phase = dict(payload.get("phase") or {})
    lines = [
        "# Mainline Phase",
        "",
        f"- phase_id: `{phase.get('phase_id')}`",
        f"- phase_name: `{phase.get('phase_name')}`",
        f"- status: `{phase.get('status')}`",
    ]
    if phase.get("summary"):
        lines.append(f"- summary: {phase.get('summary')}")
    lines.extend(["", "## Entry Points", ""])
    for item in phase.get("entry_points") or []:
        lines.append(f"- `{item.get('name')}`: `{item.get('command')}`")
    lines.extend(["", "## Exit Criteria", ""])
    for item in phase.get("exit_criteria") or []:
        lines.append(f"- {item}")
    return "\n".join(lines)
