from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from med_autogrant.workspace_types import WorkspaceStateError
from opl_framework.executor_client import (
    project_agent_execution_receipt_metadata,
    require_agent_execution_receipt,
    run_agent_execution_request,
)


ExecutorRunner = Callable[..., dict[str, Any]]

OPL_EXECUTOR_TIMEOUT_SECONDS = 300.0


def run_domain_executor(
    *,
    prompt: str,
    input_path: str | Path,
    executor_kind: str,
    route_id: str,
    closeout_surface_kind: str,
    domain_output_kind: str,
    executor_runner: ExecutorRunner = run_agent_execution_request,
) -> tuple[dict[str, Any], dict[str, Any]]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    try:
        receipt = executor_runner(
            {
                "executor_kind": executor_kind,
                "mode": "agent_loop" if executor_kind == "hermes_agent" else "structured_call",
                "prompt": prompt,
                "cwd": str(resolved_input_path.parent),
                "json": True,
                "domain_payload": {
                    "domain_id": "med-autogrant",
                    "route_id": route_id,
                    "input_path": str(resolved_input_path),
                    "closeout_surface_kind": closeout_surface_kind,
                    "domain_output_kind": domain_output_kind,
                },
            },
            timeout_seconds=OPL_EXECUTOR_TIMEOUT_SECONDS,
        )
    except (RuntimeError, TimeoutError, ValueError) as exc:
        raise WorkspaceStateError(f"OPL executor client 执行失败: {exc}") from exc

    try:
        receipt = require_agent_execution_receipt(
            receipt,
            expected_executor_kind=executor_kind,
        )
    except (RuntimeError, TypeError, ValueError) as exc:
        raise WorkspaceStateError(f"OPL executor receipt 校验失败: {exc}") from exc
    closeout = _require_object(receipt, "closeout_packet", context="OPL executor receipt")
    if closeout.get("surface_kind") != closeout_surface_kind:
        raise WorkspaceStateError(
            f"OPL executor receipt closeout_packet.surface_kind 必须是 {closeout_surface_kind}。"
        )
    if closeout.get("route_id") != route_id:
        raise WorkspaceStateError(f"OPL executor receipt closeout_packet.route_id 必须是 {route_id}。")
    if closeout.get("domain_output_kind") != domain_output_kind:
        raise WorkspaceStateError(
            f"OPL executor receipt closeout_packet.domain_output_kind 必须是 {domain_output_kind}。"
        )
    domain_output = _require_object(closeout, "domain_output", context="MAG executor closeout packet")
    return domain_output, build_executor_payload(receipt)


def build_executor_payload(receipt: dict[str, Any]) -> dict[str, Any]:
    executor_kind = receipt.get("executor_kind")
    if not isinstance(executor_kind, str) or not executor_kind.strip():
        raise WorkspaceStateError("OPL executor receipt.executor_kind 必须是非空字符串。")
    try:
        return project_agent_execution_receipt_metadata(
            receipt,
            expected_executor_kind=executor_kind.strip(),
        )
    except (RuntimeError, TypeError, ValueError) as exc:
        message = str(exc)
        if executor_kind == "hermes_agent" and (
            "full agent loop" in message or "tool call" in message
        ):
            raise WorkspaceStateError(
                "Hermes proof 必须证明完整 agent loop 和至少一个 tool call。"
            ) from exc
        raise WorkspaceStateError(f"OPL executor receipt 校验失败: {message}") from exc


def _require_object(payload: dict[str, Any], key: str, *, context: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise WorkspaceStateError(f"{context}.{key} 必须是 object。")
    return value
