from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]

META_FILES = {
    "tests/test_program_control_surfaces.py",
    "tests/test_repository_hygiene.py",
}


def _relative_test_path(item: pytest.Item) -> str:
    path = Path(str(item.fspath)).resolve()
    return path.relative_to(REPO_ROOT).as_posix()


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    del config
    for item in items:
        if _relative_test_path(item) in META_FILES:
            item.add_marker(pytest.mark.meta)
