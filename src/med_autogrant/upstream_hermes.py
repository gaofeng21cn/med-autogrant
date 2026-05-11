from __future__ import annotations

import hashlib
import importlib
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from med_autogrant.control_plane import resolve_runtime_state_root
from med_autogrant.workspace_types import WorkspaceError


class HermesDependencyError(WorkspaceError):
    """真实上游 Hermes-Agent 依赖或入口不可用。"""


def probe_upstream_hermes() -> dict[str, Any]:
    hermes_cli = _import_upstream_module("hermes_cli")
    _import_upstream_module("run_agent")
    _import_upstream_module("hermes_state")
    _import_upstream_module("acp_adapter.session")
    _import_upstream_module("acp_adapter.server")

    runtime_root = resolve_upstream_hermes_runtime_root()
    hermes_command = _resolve_hermes_command()
    if hermes_command is None:
        raise HermesDependencyError("未找到上游 Hermes CLI 入口：期望当前 Python 环境或 PATH 中存在 `hermes` 命令。")

    return {
        "ok": True,
        "command": "probe-upstream-hermes",
        "package_version": getattr(hermes_cli, "__version__", "unknown"),
        "hermes_command": str(hermes_command),
        "runtime_root": str(runtime_root),
        "state_db_path": str((runtime_root / "state.db").resolve()),
        "entrypoints": {
            "cli": "hermes",
            "acp": "hermes acp",
            "agent": "run_agent.AIAgent",
            "session_db": "hermes_state.SessionDB",
            "session_manager": "acp_adapter.session.SessionManager",
        },
    }


class MagGrantRunLedger:
    """Record MAG runtime attempts without requiring an optional external executor."""

    def __init__(self) -> None:
        self._ledger_root = (resolve_runtime_state_root() / "sessions").resolve()
        self._ledger_root.mkdir(parents=True, exist_ok=True)

    def record_attempt(
        self,
        *,
        grant_run_id: str | None,
        workspace_id: str | None,
        trigger: str,
        journal_path: Path,
        lifecycle_stage: str | None,
        stop_reason: dict[str, Any],
        stage_action_envelope: dict[str, Any] | None,
        route_report: dict[str, Any],
    ) -> int:
        session_id, session_handle_kind = _resolve_session_handle(
            grant_run_id=grant_run_id,
            journal_path=journal_path,
        )
        ledger_path = self._ledger_root / f"{session_id}.json"
        ledger = self._read_ledger(ledger_path)
        attempts = ledger.setdefault("attempts", [])
        if not isinstance(attempts, list):
            raise WorkspaceError(f"MAG runtime attempt ledger attempts 不是 list: {ledger_path}")

        attempt_index = _count_matching_attempts(attempts, journal_path=journal_path) + 1
        attempts.append(
            {
                "attempt_index": attempt_index,
                "trigger": trigger,
                "grant_run_id": grant_run_id,
                "workspace_id": workspace_id,
                "journal_path": str(journal_path),
                "lifecycle_stage": lifecycle_stage,
                "stop_reason": stop_reason,
                "stage_action_envelope": stage_action_envelope,
                "route_report": route_report,
            }
        )
        ledger.update(
            {
                "surface_kind": "mag_runtime_attempt_ledger",
                "session_id": session_id,
                "session_handle_kind": session_handle_kind,
                "grant_run_id": grant_run_id,
                "workspace_id": workspace_id,
            }
        )
        _write_json(ledger_path, ledger)
        return attempt_index

    def _read_ledger(self, ledger_path: Path) -> dict[str, Any]:
        if not ledger_path.exists():
            return {"surface_kind": "mag_runtime_attempt_ledger", "attempts": []}
        try:
            payload = json.loads(ledger_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise WorkspaceError(f"MAG runtime attempt ledger JSON 解析失败: {ledger_path}") from exc
        if not isinstance(payload, dict):
            raise WorkspaceError(f"MAG runtime attempt ledger 顶层必须是 object: {ledger_path}")
        return payload


class HermesGrantRunLedger:
    """Explicit optional proof ledger backed by real upstream Hermes session substrate."""

    SESSION_SOURCE = "med-autogrant"
    SESSION_MODEL = "med-autogrant/grant-runtime"

    def __init__(self) -> None:
        hermes_state = _import_upstream_module("hermes_state")

        self._runtime_root = resolve_upstream_hermes_runtime_root()
        self._runtime_root.mkdir(parents=True, exist_ok=True)
        self._session_db = hermes_state.SessionDB(db_path=self._runtime_root / "state.db")

    def record_attempt(
        self,
        *,
        grant_run_id: str | None,
        workspace_id: str | None,
        trigger: str,
        journal_path: Path,
        lifecycle_stage: str | None,
        stop_reason: dict[str, Any],
        stage_action_envelope: dict[str, Any] | None,
        route_report: dict[str, Any],
    ) -> int:
        session_id, session_handle_kind = _resolve_session_handle(
            grant_run_id=grant_run_id,
            journal_path=journal_path,
        )

        model_config = {
            "session_handle_kind": session_handle_kind,
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "journal_path": str(journal_path),
            "runtime_root": str(self._runtime_root),
        }
        self._session_db.create_session(
            session_id=session_id,
            source=self.SESSION_SOURCE,
            model=self.SESSION_MODEL,
            model_config=model_config,
        )
        self._session_db.reopen_session(session_id)

        attempt_index = self._count_attempts(session_id, journal_path=journal_path) + 1
        attempt_payload = {
            "attempt_index": attempt_index,
            "trigger": trigger,
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "journal_path": str(journal_path),
            "lifecycle_stage": lifecycle_stage,
            "stop_reason": stop_reason,
            "stage_action_envelope": stage_action_envelope,
            "route_report": route_report,
        }
        self._session_db.append_message(
            session_id=session_id,
            role="assistant",
            content=json.dumps(attempt_payload, ensure_ascii=False),
            tool_name=trigger,
            finish_reason=stop_reason.get("code"),
        )
        return attempt_index

    def _count_attempts(self, session_id: str, *, journal_path: Path) -> int:
        messages = self._session_db.get_messages(session_id)
        count = 0
        expected_journal_path = str(journal_path)
        for message in messages:
            if message.get("tool_name") not in {
                "run-local",
                "resume-local",
                "runtime-run",
                "runtime-resume",
            }:
                continue
            content = message.get("content")
            if not isinstance(content, str) or not content:
                continue
            try:
                payload = json.loads(content)
            except json.JSONDecodeError:
                continue
            if payload.get("journal_path") == expected_journal_path:
                count += 1
        return count


def _import_upstream_module(module_name: str) -> Any:
    if module_name == "hermes_state":
        _ensure_hermes_constants_runtime_root()
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        raise HermesDependencyError(
            f"缺少上游 Hermes-Agent 依赖模块 `{module_name}`。请先在当前 Python 环境安装真实上游 Hermes-Agent。"
        ) from exc


def _ensure_hermes_constants_runtime_root() -> None:
    try:
        hermes_constants = importlib.import_module("hermes_constants")
    except ModuleNotFoundError:
        return
    if hasattr(hermes_constants, "get_hermes_home"):
        return

    def get_hermes_home() -> Path:
        return resolve_upstream_hermes_runtime_root()

    setattr(hermes_constants, "get_hermes_home", get_hermes_home)


def _resolve_hermes_command() -> Path | None:
    executable_dir = Path(sys.executable).resolve().parent
    sibling = executable_dir / "hermes"
    if sibling.exists():
        return sibling.resolve()

    hermes_on_path = shutil.which("hermes")
    if hermes_on_path:
        return Path(hermes_on_path).expanduser().resolve()
    return None


def _resolve_session_handle(*, grant_run_id: str | None, journal_path: Path) -> tuple[str, str]:
    if isinstance(grant_run_id, str) and grant_run_id:
        return grant_run_id, "grant_run_id"

    journal_digest = hashlib.sha256(str(journal_path).encode("utf-8")).hexdigest()
    return f"med-autogrant-validation-failed-{journal_digest}", "journal_path"


def _count_matching_attempts(attempts: list[Any], *, journal_path: Path) -> int:
    expected_journal_path = str(journal_path)
    count = 0
    for attempt in attempts:
        if isinstance(attempt, dict) and attempt.get("journal_path") == expected_journal_path:
            count += 1
    return count


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_upstream_hermes_runtime_root() -> Path:
    explicit_root = os.environ.get("MED_AUTOGRANT_HERMES_HOME", "").strip()
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    return (resolve_runtime_state_root() / "hermes").resolve()
