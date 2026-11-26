from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from med_autogrant._opl_helpers.runtime_state_paths import (
    domain_runtime_state_display_path,
    resolve_domain_runtime_state_root,
)

from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


PROJECT_SLUG = "med-autogrant"
CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH = Path("contracts") / "runtime-program" / "current-program.json"


def resolve_runtime_state_root() -> Path:
    return resolve_domain_runtime_state_root(
        PROJECT_SLUG,
        explicit_env="MED_AUTOGRANT_RUNTIME_STATE_ROOT",
    )


def runtime_state_display_path(*segments: str) -> str:
    return domain_runtime_state_display_path(PROJECT_SLUG, *segments)


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
