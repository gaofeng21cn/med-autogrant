from __future__ import annotations

from pathlib import Path

import pytest

from med_autogrant.control_plane import read_program_id
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
