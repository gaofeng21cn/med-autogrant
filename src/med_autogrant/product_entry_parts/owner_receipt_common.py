from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.control_plane import resolve_runtime_state_root
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


OWNER_RECEIPT_EVIDENCE_KIND = "mag_owner_receipt_evidence"
RECEIPT_RECONCILIATION_PROOF_KIND = "mag_controlled_soak_receipt_reconciliation_proof"
RECEIPT_RECONCILIATION_INVENTORY_KIND = "mag_controlled_soak_receipt_reconciliation_inventory"
PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_PROJECTION_KIND = (
    "mag_production_live_acceptance_receipt_projection"
)

RECEIPT_SHAPES = ("domain_owner_receipt", "typed_blocker", "no_regression_evidence")
FORBIDDEN_WRITE_KEYS = (
    "repo_receipt_instance_written",
    "grant_truth_written",
    "grant_artifact_written",
    "memory_body_written",
    "fundability_verdict_written",
    "authoring_quality_verdict_written",
    "submission_ready_export_verdict_written",
)
STAGE_IDS = (
    "call_and_candidate_intake",
    "fundability_strategy",
    "specific_aims_and_structure",
    "proposal_authoring",
    "review_and_rebuttal",
    "package_and_submit_ready",
)
PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_SHAPES = ("domain_owner_receipt", "typed_blocker")
PATCH_LOOP_REF_KEYS = (
    "blocked_suite_result_ref",
    "developer_patch_work_order_ref",
    "patch_traceability_matrix_ref",
    "target_repo_verification_refs",
    "target_runtime_read_model_consumption_ref",
    "workspace_environment_proof_ref",
    "no_forbidden_write_proof_ref",
    "target_owner_receipt_or_typed_blocker_ref",
    "patch_absorption_ref",
    "worktree_cleanup_ref",
    "agent_lab_re_evaluation_ref",
)
PATCH_LOOP_REF_LIST_KEYS = ("target_repo_verification_refs",)


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


def read_forbidden_write_proof(
    payload: Mapping[str, Any],
    *,
    field_name: str = "forbidden_write_proof",
    context: str,
) -> dict[str, bool]:
    raw = payload.get(field_name)
    if not isinstance(raw, Mapping):
        raise WorkspaceStateError(f"{context} 缺少 forbidden_write_proof。")
    return {key: bool(raw.get(key)) for key in FORBIDDEN_WRITE_KEYS}


def opl_receipt_ref_consumption() -> dict[str, bool | str]:
    return {
        "role": "receipt_ref_consumer_only",
        "consumes_receipt_ref_only": True,
        "can_write_grant_truth": False,
        "can_write_memory_body": False,
        "can_declare_export_ready": False,
    }


def write_receipt(path: Path, receipt: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 receipt evidence 失败: {path}") from exc


def require_owner_receipt_evidence(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("surface_kind") != OWNER_RECEIPT_EVIDENCE_KIND:
        raise WorkspaceStateError("owner_receipt_evidence.surface_kind 必须是 mag_owner_receipt_evidence。")
    if payload.get("owner") != TARGET_DOMAIN_ID or payload.get("target_domain_id") != TARGET_DOMAIN_ID:
        raise WorkspaceStateError("owner_receipt_evidence.owner 和 target_domain_id 必须都是 med-autogrant。")
    if any(read_forbidden_write_proof(payload, context="owner_receipt_evidence").values()):
        raise WorkspaceStateError("owner_receipt_evidence 不能包含 MAG/OPL forbidden write。")
    return payload


def require_mapping_payload(payload: Mapping[str, Any], *, context: str) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 JSON object。")
    return payload


def require_nonempty_string_from_receipt(receipt: Mapping[str, Any], key: str) -> str:
    return _require_nonempty_string(receipt.get(key), field_name=key)
