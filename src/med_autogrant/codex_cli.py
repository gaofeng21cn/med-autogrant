from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from med_autogrant.workspace_types import WorkspaceStateError


DEFAULT_CODEX_COMMAND = ("codex",)
INHERIT_LOCAL_CODEX_DEFAULT = "inherit_local_codex_default"
DEFAULT_CODEX_MODEL = INHERIT_LOCAL_CODEX_DEFAULT
DEFAULT_CODEX_REASONING_EFFORT = INHERIT_LOCAL_CODEX_DEFAULT
DEFAULT_CODEX_TIMEOUT_MS = 300_000


def read_codex_cli_contract(env: dict[str, str] | None = None) -> dict[str, Any]:
    resolved_env = env or os.environ
    command = _parse_codex_command(resolved_env.get("MED_AUTOGRANT_CODEX_COMMAND"))
    model = _parse_optional_override(resolved_env.get("MED_AUTOGRANT_CODEX_MODEL"))
    reasoning_effort = _parse_optional_override(
        resolved_env.get("MED_AUTOGRANT_CODEX_REASONING_EFFORT")
    )
    return {
        "command": command,
        "model": model,
        "reasoning_effort": reasoning_effort,
        "model_selection": model or DEFAULT_CODEX_MODEL,
        "reasoning_selection": reasoning_effort or DEFAULT_CODEX_REASONING_EFFORT,
        "sandbox": str(
            resolved_env.get("MED_AUTOGRANT_CODEX_SANDBOX") or "read-only"
        ).strip()
        or "read-only",
    }


def run_codex_exec(
    prompt: str,
    *,
    cwd: str | Path,
    timeout_ms: int = DEFAULT_CODEX_TIMEOUT_MS,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    contract = read_codex_cli_contract(env)
    resolved_cwd = Path(cwd).expanduser().resolve()
    if not resolved_cwd.exists():
        raise WorkspaceStateError(f"Codex CLI working directory 不存在: {resolved_cwd}")

    with tempfile.TemporaryDirectory(prefix="med-autogrant-codex-") as tmp_dir:
        last_message_path = Path(tmp_dir) / "last-message.json"
        command = [
            *contract["command"],
            "exec",
            "--json",
            "--ephemeral",
            "--cd",
            str(resolved_cwd),
            "--skip-git-repo-check",
            "-s",
            contract["sandbox"],
            "-c",
            'approval_policy="never"',
        ]
        if contract["reasoning_effort"] is not None:
            command.extend(
                [
                    "-c",
                    f'model_reasoning_effort="{contract["reasoning_effort"]}"',
                ]
            )
        if contract["model"] is not None:
            command.extend(["--model", contract["model"]])
        command.extend(
            [
                "--output-last-message",
                str(last_message_path),
                "-",
            ]
        )
        process = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=max(timeout_ms / 1000, 1),
            env=env,
        )
        if process.returncode != 0:
            detail = _extract_codex_error(process.stdout, process.stderr)
            raise WorkspaceStateError(f"Codex CLI critique 执行失败: {detail}")
        if not last_message_path.exists():
            raise WorkspaceStateError("Codex CLI 未产出 final message，无法解析 critique 结果。")
        try:
            return _parse_json_message(last_message_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise WorkspaceStateError(
                "Codex CLI final message 不是合法 JSON object，无法继续 critique pass。"
            ) from exc


def _parse_codex_command(value: str | None) -> tuple[str, ...]:
    if value is None or not value.strip():
        return DEFAULT_CODEX_COMMAND

    raw = value.strip()
    if raw.startswith("["):
        parsed = json.loads(raw)
        if not isinstance(parsed, list) or not parsed:
            raise WorkspaceStateError(
                "MED_AUTOGRANT_CODEX_COMMAND 若使用 JSON array，必须是非空字符串数组。"
            )
        command = tuple(str(item).strip() for item in parsed if str(item).strip())
        if not command:
            raise WorkspaceStateError(
                "MED_AUTOGRANT_CODEX_COMMAND 若使用 JSON array，不能在清洗后为空。"
            )
        return command

    return (raw,)


def _parse_optional_override(value: str | None) -> str | None:
    text = str(value or "").strip()
    return text or None


def _parse_json_message(message: str) -> dict[str, Any]:
    stripped = message.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    payload = json.loads(stripped)
    if not isinstance(payload, dict):
        raise WorkspaceStateError("Codex CLI final message 顶层必须是 JSON object。")
    return payload


def _extract_codex_error(stdout: str, stderr: str) -> str:
    stderr_text = stderr.strip()
    if stderr_text:
        return stderr_text
    stdout_text = stdout.strip()
    if stdout_text:
        return stdout_text.splitlines()[-1]
    return "unknown codex exec failure"
