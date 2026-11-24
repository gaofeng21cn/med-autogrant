from __future__ import annotations

from pathlib import Path

import pytest

from med_autogrant.control_plane import (
    read_program_id,
    resolve_runtime_state_root,
    runtime_state_display_path,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


def test_read_program_id_fails_closed_when_contract_is_missing(tmp_path: Path) -> None:
    with pytest.raises(WorkspaceFileError, match="未找到 repo-tracked CURRENT_PROGRAM contract"):
        read_program_id(repo_root=tmp_path)


def test_read_program_id_fails_closed_when_program_id_is_missing(tmp_path: Path) -> None:
    contract_path = tmp_path / "contracts" / "runtime-program" / "current-program.json"
    contract_path.parent.mkdir(parents=True)
    contract_path.write_text("{}", encoding="utf-8")

    with pytest.raises(WorkspaceStateError, match="CURRENT_PROGRAM contract 缺少合法 program_id"):
        read_program_id(repo_root=tmp_path)


def test_runtime_state_root_uses_canonical_opl_state_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "ignored-codex-home"))
    monkeypatch.delenv("MED_AUTOGRANT_RUNTIME_STATE_ROOT", raising=False)
    monkeypatch.delenv("OPL_STATE_DIR", raising=False)
    monkeypatch.delenv("OPL_DATA_DIR", raising=False)

    assert ".codex" not in str(resolve_runtime_state_root())
    assert runtime_state_display_path() == "$OPL_STATE_DIR/domains/med-autogrant/runtime-state/"
    assert (
        runtime_state_display_path("receipts")
        == "$OPL_STATE_DIR/domains/med-autogrant/runtime-state/receipts"
    )

    opl_state = tmp_path / "opl-state"
    monkeypatch.setenv("OPL_STATE_DIR", str(opl_state))
    assert resolve_runtime_state_root() == (opl_state / "domains" / "med-autogrant" / "runtime-state").resolve()

    explicit_mag = tmp_path / "mag-override"
    monkeypatch.setenv("MED_AUTOGRANT_RUNTIME_STATE_ROOT", str(explicit_mag))
    assert resolve_runtime_state_root() == explicit_mag.resolve()
