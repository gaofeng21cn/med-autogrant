from __future__ import annotations

from copy import deepcopy
import json
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any


JsonObject = dict[str, Any]
WorkspaceMutator = Callable[[JsonObject], None]


def load_workspace(path: Path) -> JsonObject:
    return json.loads(path.read_text(encoding="utf-8"))


def write_mutated_workspace(
    source_path: Path,
    mutator: WorkspaceMutator,
    *,
    filename: str,
    tmp_root: Path | None = None,
) -> Path:
    payload = deepcopy(load_workspace(source_path))
    mutator(payload)
    root = tmp_root if tmp_root is not None else Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
    root.mkdir(parents=True, exist_ok=True)
    output_path = root / filename
    output_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return output_path


def write_empty_revision_items_workspace(source_path: Path, *, tmp_root: Path | None = None) -> Path:
    return write_mutated_workspace(
        source_path,
        lambda payload: payload["revision_plans"][0].__setitem__("items", []),
        filename="invalid-workspace.json",
        tmp_root=tmp_root,
    )


def write_outline_only_critique_workspace(source_path: Path, *, tmp_root: Path | None = None) -> Path:
    def mutate(payload: JsonObject) -> None:
        payload["application_drafts"][0]["status"] = "outline"
        payload["application_drafts"][0]["sections"] = []

    return write_mutated_workspace(
        source_path,
        mutate,
        filename="outline-only-critique-workspace.json",
        tmp_root=tmp_root,
    )


def write_revision_outline_workspace(source_path: Path, *, tmp_root: Path | None = None) -> Path:
    def mutate(payload: JsonObject) -> None:
        payload["lifecycle_stage"] = "revision"
        payload["application_drafts"][0]["status"] = "outline"

    return write_mutated_workspace(
        source_path,
        mutate,
        filename="revision-outline-workspace.json",
        tmp_root=tmp_root,
    )


def write_revision_completed_without_revised_workspace(
    source_path: Path,
    *,
    tmp_root: Path | None = None,
) -> Path:
    def mutate(payload: JsonObject) -> None:
        payload["lifecycle_stage"] = "revision"
        payload["revision_plans"][0]["execution_status"] = "completed"
        payload["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        payload["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        payload["revision_plans"][0]["comparison_summary"] = "已按批注完成修订，但尚未切换草稿状态。"

    return write_mutated_workspace(
        source_path,
        mutate,
        filename="revision-completed-without-revised.json",
        tmp_root=tmp_root,
    )


def write_completed_revision_workspace(source_path: Path, *, tmp_root: Path | None = None) -> Path:
    def mutate(payload: JsonObject) -> None:
        payload["lifecycle_stage"] = "revision"
        payload["application_drafts"][0]["status"] = "revised"
        payload["application_drafts"][0]["version_label"] = "v0.4"
        payload["revision_plans"][0]["execution_status"] = "completed"
        payload["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        payload["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        payload["revision_plans"][0]["comparison_summary"] = "已根据 major_revision 完成立项依据与机制链条修订。"

    return write_mutated_workspace(
        source_path,
        mutate,
        filename="revision-completed.json",
        tmp_root=tmp_root,
    )
