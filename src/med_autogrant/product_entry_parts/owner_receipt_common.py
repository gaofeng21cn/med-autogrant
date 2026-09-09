from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from opl_framework.json_io import write_json_object_atomic

from med_autogrant.control_plane import resolve_runtime_state_root
from med_autogrant.product_entry_parts.primitives import (
    _require_nonempty_string,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


OWNER_RECEIPT_EVIDENCE_KIND = "mag_owner_receipt_evidence"

RECEIPT_SHAPES = ("domain_owner_receipt", "typed_blocker", "no_regression_evidence")
STAGE_IDS = (
    "call_and_candidate_intake",
    "fundability_strategy",
    "specific_aims_and_structure",
    "proposal_authoring",
    "review_and_rebuttal",
    "package_and_submit_ready",
)


def resolve_receipt_runtime_root(runtime_root: str | Path | None) -> Path:
    if runtime_root is not None:
        return Path(runtime_root).expanduser().resolve()
    return resolve_runtime_state_root()


def require_choice(value: str, *, choices: tuple[str, ...], field_name: str) -> str:
    resolved = _require_nonempty_string(value, field_name=field_name)
    if resolved not in choices:
        raise WorkspaceStateError(f"{field_name} 不支持: {resolved}。只允许 {', '.join(choices)}。")
    return resolved


def forbidden_write_proof() -> dict[str, bool]:
    return {
        "repo_receipt_instance_written": False,
        "grant_truth_written": False,
        "grant_artifact_written": False,
        "memory_body_written": False,
        "fundability_verdict_written": False,
        "authoring_quality_verdict_written": False,
        "submission_ready_export_verdict_written": False,
    }


def opl_receipt_ref_consumption() -> dict[str, bool | str]:
    return {
        "role": "receipt_ref_consumer_only",
        "consumes_receipt_ref_only": True,
        "can_write_grant_truth": False,
        "can_write_memory_body": False,
        "can_declare_export_ready": False,
    }


def write_receipt(path: Path, receipt: Mapping[str, Any]) -> None:
    try:
        write_json_object_atomic(path, receipt)
    except OSError as exc:
        raise WorkspaceFileError(f"写入 receipt evidence 失败: {path}") from exc
