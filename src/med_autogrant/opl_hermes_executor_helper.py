#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from med_autogrant.hermes_native_executor import run_hermes_agent_exec
from med_autogrant.workspace_types import WorkspaceStateError


def main() -> int:
    try:
        request = _read_request()
        receipt = run_mag_hermes_executor_request(request)
    except WorkspaceStateError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"MAG OPL Hermes helper failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, ensure_ascii=False))
    return 0


def run_mag_hermes_executor_request(request: dict[str, Any]) -> dict[str, Any]:
    if request.get("executor_kind") != "hermes_agent":
        raise WorkspaceStateError("MAG OPL Hermes helper 只接受 hermes_agent request。")
    prompt = _require_string(request, "prompt")
    cwd = Path(_require_string(request, "cwd")).expanduser().resolve()
    domain_payload = _require_object(request, "domain_payload")
    route_id = _require_string(domain_payload, "route_id")
    if route_id != "critique":
        raise WorkspaceStateError("MAG OPL Hermes helper 只支持 critique route。")

    result = run_hermes_agent_exec(prompt, cwd=cwd)
    receipt = _require_object(result, "agent_execution_receipt")
    receipt["executor_contract"] = _require_object(result, "contract")
    receipt["closeout_packet"] = {
        "surface_kind": "mag_critique_closeout_packet",
        "mentor_critique": _require_object(_require_object(result, "payload"), "mentor_critique"),
        "revision_plan": _require_object(_require_object(result, "payload"), "revision_plan"),
    }
    return receipt


def _read_request() -> dict[str, Any]:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError("MAG OPL Hermes helper request 不是合法 JSON。") from exc
    if not isinstance(payload, dict):
        raise WorkspaceStateError("MAG OPL Hermes helper request 必须是 object。")
    return payload


def _require_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"MAG OPL Hermes helper request 缺少字符串字段: {key}。")
    return value.strip()


def _require_object(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise WorkspaceStateError(f"MAG OPL Hermes helper request 缺少 object 字段: {key}。")
    return value


if __name__ == "__main__":
    raise SystemExit(main())
