from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from opl_harness_shared.family_shared_release import (  # noqa: E402
    inspect_current_repo_family_shared_alignment as _inspect_current_repo_family_shared_alignment,
)


CONSUMER_REPO_ID = "medautogrant"
OWNER_REPO = "one-person-lab"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def inspect_current_repo_family_shared_alignment() -> dict[str, Any]:
    return _inspect_current_repo_family_shared_alignment(
        repo_root=_repo_root(),
        consumer_repo_id=CONSUMER_REPO_ID,
        owner_repo=OWNER_REPO,
    )
