from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


PROJECT_SLUG = "med-autogrant"
CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH = Path("contracts") / "runtime-program" / "current-program.json"


def resolve_codex_home() -> Path:
    explicit_home = os.environ.get("CODEX_HOME", "").strip()
    if explicit_home:
        return Path(explicit_home).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def resolve_runtime_state_root() -> Path:
    explicit_root = os.environ.get("MED_AUTOGRANT_RUNTIME_STATE_ROOT", "").strip()
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()
    return resolve_codex_home() / "projects" / PROJECT_SLUG / "runtime-state"


def runtime_state_display_path(*segments: str) -> str:
    base = Path("$CODEX_HOME") / "projects" / PROJECT_SLUG / "runtime-state"
    if not segments:
        return base.as_posix() + "/"
    return base.joinpath(*segments).as_posix()


def resolve_current_program_contract_path(*, repo_root: Path | None = None) -> Path:
    resolved_repo_root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    contract_path = resolved_repo_root / CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH
    if not contract_path.exists():
        raise WorkspaceFileError(f"未找到 repo-tracked CURRENT_PROGRAM contract: {contract_path}")
    return contract_path


def read_current_program_contract(*, repo_root: Path | None = None) -> dict[str, Any]:
    contract_path = resolve_current_program_contract_path(repo_root=repo_root)
    try:
        payload = json.loads(contract_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"CURRENT_PROGRAM contract JSON 解析失败: {contract_path}") from exc

    if not isinstance(payload, dict):
        raise WorkspaceStateError(f"CURRENT_PROGRAM contract 顶层必须是 JSON object: {contract_path}")
    return payload


def read_program_id(*, repo_root: Path | None = None) -> str:
    payload = read_current_program_contract(repo_root=repo_root)
    program_id = payload.get("program_id")
    if not isinstance(program_id, str) or not program_id:
        contract_path = resolve_current_program_contract_path(repo_root=repo_root)
        raise WorkspaceStateError(f"CURRENT_PROGRAM contract 缺少合法 program_id: {contract_path}")
    return program_id
