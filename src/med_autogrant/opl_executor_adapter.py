from __future__ import annotations

import json
import os
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import Any

from med_autogrant.runtime_defaults import parse_opl_command
from med_autogrant.workspace_types import WorkspaceStateError


def run_opl_agent_executor(
    request: dict[str, Any],
    *,
    cwd: str | Path,
    env: dict[str, str] | None = None,
    timeout_ms: int = 300_000,
) -> dict[str, Any]:
    resolved_cwd = Path(cwd).expanduser().resolve()
    if not resolved_cwd.exists():
        raise WorkspaceStateError(f"OPL executor adapter working directory 不存在: {resolved_cwd}")

    with tempfile.TemporaryDirectory(prefix="med-autogrant-opl-executor-") as tmp_dir:
        tmp_path = Path(tmp_dir)
        request_path = tmp_path / "agent-execution-request.json"
        request_path.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
        command = [
            *parse_opl_command(env),
            "executor",
            "run",
            "--request",
            str(request_path),
        ]
        child_env = dict(os.environ)
        if env is not None:
            child_env.update(env)
        if request.get("executor_kind") == "hermes_agent" and "OPL_HERMES_AGENT_EXECUTOR_BIN" not in child_env:
            child_env["OPL_HERMES_AGENT_EXECUTOR_BIN"] = _write_hermes_helper_shim(tmp_path)
        try:
            process = subprocess.run(
                command,
                text=True,
                capture_output=True,
                timeout=max(timeout_ms / 1000, 1),
                env=child_env,
                cwd=resolved_cwd,
            )
        except subprocess.TimeoutExpired as exc:
            raise WorkspaceStateError("OPL executor adapter 超时，未回退到 Codex CLI。") from exc
        except OSError as exc:
            raise WorkspaceStateError(f"OPL executor adapter 不可用: {exc}") from exc

    if process.returncode != 0:
        detail = process.stderr.strip() or process.stdout.strip() or "unknown OPL executor failure"
        raise WorkspaceStateError(f"OPL executor adapter 执行失败: {detail}")
    try:
        payload = json.loads(process.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError("OPL executor adapter 未返回合法 JSON receipt envelope。") from exc
    if not isinstance(payload, dict):
        raise WorkspaceStateError("OPL executor adapter 返回值必须是 object。")
    receipt = payload.get("agent_execution_receipt")
    if not isinstance(receipt, dict):
        raise WorkspaceStateError("OPL executor adapter 返回值缺少 agent_execution_receipt。")
    return receipt


def _write_hermes_helper_shim(tmp_path: Path) -> str:
    shim = tmp_path / "mag-opl-hermes-executor"
    shim.write_text(
        textwrap.dedent(
            f"""\
            #!/bin/sh
            exec /usr/bin/env python3 {_hermes_helper_path()}
            """
        ),
        encoding="utf-8",
    )
    shim.chmod(0o700)
    return str(shim)


def _hermes_helper_path() -> str:
    return str(Path(__file__).resolve().parent / "opl_hermes_executor_helper.py")
