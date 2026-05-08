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
FAMILY_ACTION_CATALOG_OWNER_COMMIT = "2b08c7efd8acd80355e870087d4ce5be7b45d4d1"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def inspect_current_repo_family_shared_alignment(
    *,
    repo_root_override: Path | str | None = None,
    owner_repo_root: Path | str | None = None,
    owner_repo: str = OWNER_REPO,
) -> dict[str, Any]:
    resolved_repo_root = Path(repo_root_override).expanduser().resolve() if repo_root_override else _repo_root()
    inspection = _inspect_current_repo_family_shared_alignment(
        repo_root=resolved_repo_root,
        consumer_repo_id=CONSUMER_REPO_ID,
        owner_repo_root=owner_repo_root,
        owner_repo=owner_repo,
    )
    if all(
        item.get("pins") == [FAMILY_ACTION_CATALOG_OWNER_COMMIT]
        for item in inspection.get("findings", [])
    ):
        inspection["owner_commit"] = FAMILY_ACTION_CATALOG_OWNER_COMMIT
        for item in inspection["findings"]:
            item["status"] = "aligned"
        inspection["status"] = "aligned"
    return inspection
