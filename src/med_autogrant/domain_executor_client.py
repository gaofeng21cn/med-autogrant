from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from med_autogrant.workspace_types import WorkspaceStateError
from opl_framework.executor_client import run_agent_execution_request


ExecutorRunner = Callable[..., dict[str, Any]]

OPL_EXECUTOR_ADAPTER_OWNER = "one-person-lab"
OPL_EXECUTOR_ADAPTER_CONTRACT_REF = "contracts/opl-framework/family-executor-adapter-defaults.json"
OPL_AGENT_EXECUTION_REQUEST_CONTRACT = "AgentExecutionRequest"
OPL_AGENT_EXECUTION_RECEIPT_CONTRACT = "AgentExecutionReceipt"
OPL_EXECUTOR_TIMEOUT_SECONDS = 300.0
DEFAULT_EXECUTOR_SELECTION = "inherit_local_executor_default"


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

    receipt = _require_receipt(receipt, executor_kind=executor_kind)
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
    executor_kind = _require_string(receipt, "executor_kind", context="OPL executor receipt")
    proof = receipt.get("proof") if isinstance(receipt.get("proof"), dict) else {}
    contract = receipt.get("executor_contract") if isinstance(receipt.get("executor_contract"), dict) else {}
    payload: dict[str, Any] = {
        "kind": executor_kind,
        "mode": _require_string(receipt, "mode", context="OPL executor receipt"),
        "adapter_owner": OPL_EXECUTOR_ADAPTER_OWNER,
        "adapter_contract_ref": OPL_EXECUTOR_ADAPTER_CONTRACT_REF,
        "request_contract": OPL_AGENT_EXECUTION_REQUEST_CONTRACT,
        "receipt_contract": OPL_AGENT_EXECUTION_RECEIPT_CONTRACT,
        "fallback_allowed": False,
        "non_equivalence_notice": _require_string(
            receipt,
            "non_equivalence_notice",
            context="OPL executor receipt",
        ),
        "session_id": receipt.get("session_id") or proof.get("session_id"),
        "model": proof.get("model") or contract.get("model") or DEFAULT_EXECUTOR_SELECTION,
        "provider": proof.get("provider") or contract.get("provider"),
        "reasoning_effort": (
            proof.get("reasoning_effort")
            or contract.get("reasoning_effort")
            or DEFAULT_EXECUTOR_SELECTION
        ),
        "agent_execution_receipt": dict(receipt),
    }
    if executor_kind == "hermes_agent":
        payload.update(
            {
                "entrypoint": _require_string(contract, "entrypoint", context="Hermes contract"),
                "api_mode": contract.get("api_mode"),
                "full_agent_loop_proved": proof.get("full_agent_loop_proved") is True,
                "api_calls": _require_nonnegative_int(proof, "api_calls", context="Hermes proof"),
                "tool_call_count": _require_nonnegative_int(
                    proof,
                    "tool_call_count",
                    context="Hermes proof",
                ),
                "event_count": _require_nonnegative_int(proof, "event_count", context="Hermes proof"),
                "reasoning_semantics_status": _require_string(
                    proof,
                    "provider_reasoning_status",
                    context="Hermes proof",
                ),
                "event_stream": _require_object_list(proof, "event_stream", context="Hermes proof"),
            }
        )
        if not payload["full_agent_loop_proved"] or payload["tool_call_count"] <= 0:
            raise WorkspaceStateError("Hermes proof 必须证明完整 agent loop 和至少一个 tool call。")
    return payload


def _require_receipt(payload: Any, *, executor_kind: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise WorkspaceStateError("OPL executor client 返回的 receipt 必须是 object。")
    if payload.get("surface_kind") != "opl_agent_execution_receipt":
        raise WorkspaceStateError("OPL executor receipt.surface_kind 必须是 opl_agent_execution_receipt。")
    if payload.get("executor_kind") != executor_kind:
        raise WorkspaceStateError(f"OPL executor receipt.executor_kind 必须是 {executor_kind}。")
    if _require_nonnegative_int(payload, "exit_code", context="OPL executor receipt") != 0:
        raise WorkspaceStateError("OPL executor receipt.exit_code 必须是 0。")
    expected_notice = (
        "codex_cli_first_class_default"
        if executor_kind == "codex_cli"
        else "connectivity_lifecycle_receipt_audit_only"
    )
    if payload.get("non_equivalence_notice") != expected_notice:
        raise WorkspaceStateError(
            f"OPL executor receipt.non_equivalence_notice 必须是 {expected_notice}。"
        )
    return payload


def _require_object(payload: dict[str, Any], key: str, *, context: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise WorkspaceStateError(f"{context}.{key} 必须是 object。")
    return value


def _require_string(payload: dict[str, Any], key: str, *, context: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context}.{key} 必须是非空字符串。")
    return value.strip()


def _require_nonnegative_int(payload: dict[str, Any], key: str, *, context: str) -> int:
    value = payload.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise WorkspaceStateError(f"{context}.{key} 必须是非负整数。")
    return value


def _require_object_list(payload: dict[str, Any], key: str, *, context: str) -> list[dict[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise WorkspaceStateError(f"{context}.{key} 必须是 object list。")
    return value
