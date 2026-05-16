from __future__ import annotations

from typing import Any, Mapping, Sequence

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.workspace_types import WorkspaceStateError


LIFECYCLE_RECEIPT_BUNDLE_KIND = "mag_lifecycle_receipt_bundle"
LIFECYCLE_RECEIPT_EVIDENCE_KIND = "mag_lifecycle_receipt_evidence"

_LIFECYCLE_OPERATIONS = ("cleanup", "restore", "retention")
_READY_CLAIM_KEYS = (
    "grant_ready",
    "fundability_ready",
    "quality_ready",
    "export_ready",
    "submission_ready_export",
    "production_soak_complete",
    "claims_grant_ready",
    "claims_fundability_ready",
    "claims_authoring_quality_ready",
    "claims_submission_ready_export",
)
_FORBIDDEN_WRITE_KEYS = (
    "repo_receipt_instance_written",
    "grant_truth_written",
    "grant_artifact_written",
    "memory_body_written",
    "fundability_verdict_written",
    "authoring_quality_verdict_written",
    "submission_ready_export_verdict_written",
)


def build_lifecycle_receipt_bundle(
    *,
    lifecycle_receipt_evidence_items: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    if not lifecycle_receipt_evidence_items:
        raise WorkspaceStateError("lifecycle_receipt_evidence_items 至少需要一条 receipt evidence。")

    items_by_operation: dict[str, Mapping[str, Any]] = {}
    for payload in lifecycle_receipt_evidence_items:
        receipt = _require_lifecycle_receipt_evidence(payload)
        operation = _require_nonempty_string_from_mapping(
            receipt,
            "operation",
            context="lifecycle_receipt_evidence",
        )
        if operation not in _LIFECYCLE_OPERATIONS:
            raise WorkspaceStateError(f"lifecycle operation 不支持: {operation}")
        if operation in items_by_operation:
            raise WorkspaceStateError(f"lifecycle operation 重复: {operation}")
        items_by_operation[operation] = receipt

    missing_operations = [
        operation for operation in _LIFECYCLE_OPERATIONS if operation not in items_by_operation
    ]
    if missing_operations:
        raise WorkspaceStateError(
            "lifecycle receipt bundle 缺少 operation: " + ", ".join(missing_operations)
        )

    items = [
        _project_lifecycle_receipt(items_by_operation[operation])
        for operation in _LIFECYCLE_OPERATIONS
    ]
    receipt_refs = {
        item["operation"]: item["receipt_ref"]
        for item in items
    }
    payload = {
        "surface_kind": LIFECYCLE_RECEIPT_BUNDLE_KIND,
        "version": "v1",
        "state": "cleanup_restore_retention_refs_ready_for_opl_shell",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "summary": {
            "item_count": len(items),
            "operations_present": [item["operation"] for item in items],
            "missing_operations": [],
            "typed_blocker_count": sum(
                1 for item in items if item["receipt_shape"] == "typed_blocker"
            ),
            "no_regression_evidence_count": sum(
                1 for item in items if item["receipt_shape"] == "no_regression_evidence"
            ),
        },
        "receipt_refs": receipt_refs,
        "items": items,
        "claims": {
            "claims_production_long_run_soak_complete": False,
            "claims_grant_fundability_ready": False,
            "claims_authoring_quality_ready": False,
            "claims_submission_ready_export": False,
        },
        "authority_boundary": {
            "mag_lifecycle_receipt_authority": True,
            "opl_ref_consumer_only": True,
            "mag_implements_opl_lifecycle_shell": False,
            "mag_writes_opl_lifecycle_ledger": False,
            "opl_can_delete_grant_artifacts": False,
            "opl_can_restore_grant_artifacts": False,
            "opl_can_set_retention_for_grant_truth": False,
            "can_declare_fundability_ready": False,
            "can_declare_authoring_quality_ready": False,
            "can_declare_submission_ready_export": False,
        },
        "forbidden_write_proof": _forbidden_write_proof(),
        "opl_consumption": {
            "role": "lifecycle_receipt_ref_consumer_only",
            "consumes_cleanup_restore_retention_refs": True,
            "mag_writes_opl_runtime": False,
            "mag_runs_opl_lifecycle_shell": False,
            "can_write_grant_truth": False,
            "can_write_memory_body": False,
            "can_declare_export_ready": False,
        },
    }
    return {
        "ok": True,
        "command": "lifecycle-receipt-bundle",
        "lifecycle_receipt_bundle": payload,
    }


def _require_lifecycle_receipt_evidence(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("surface_kind") != LIFECYCLE_RECEIPT_EVIDENCE_KIND:
        raise WorkspaceStateError(
            "lifecycle_receipt_evidence.surface_kind 必须是 mag_lifecycle_receipt_evidence。"
        )
    forbidden = _require_mapping(
        payload,
        "forbidden_write_proof",
        context="lifecycle_receipt_evidence",
    )
    if any(bool(forbidden.get(key)) for key in _FORBIDDEN_WRITE_KEYS):
        raise WorkspaceStateError("lifecycle_receipt_evidence 不能包含 forbidden write。")
    if any(bool(payload.get(key)) for key in _READY_CLAIM_KEYS):
        raise WorkspaceStateError("lifecycle_receipt_evidence 不能声明 grant readiness。")
    claims = payload.get("claims")
    if isinstance(claims, Mapping) and any(bool(claims.get(key)) for key in _READY_CLAIM_KEYS):
        raise WorkspaceStateError("lifecycle_receipt_evidence.claims 不能声明 grant readiness。")
    return payload


def _project_lifecycle_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "operation": _require_nonempty_string_from_mapping(
            receipt,
            "operation",
            context="lifecycle_receipt_evidence",
        ),
        "receipt_ref": _require_nonempty_string_from_mapping(
            receipt,
            "receipt_instance_ref",
            context="lifecycle_receipt_evidence",
        ),
        "receipt_id": _require_nonempty_string_from_mapping(
            receipt,
            "receipt_id",
            context="lifecycle_receipt_evidence",
        ),
        "receipt_shape": _require_nonempty_string_from_mapping(
            receipt,
            "receipt_shape",
            context="lifecycle_receipt_evidence",
        ),
        "source_ref": _require_nonempty_string_from_mapping(
            receipt,
            "source_ref",
            context="lifecycle_receipt_evidence",
        ),
        "owner_receipt_contract_ref": _require_nonempty_string_from_mapping(
            receipt,
            "owner_receipt_contract_ref",
            context="lifecycle_receipt_evidence",
        ),
        "lifecycle_guarded_apply_proof_ref": _require_nonempty_string_from_mapping(
            receipt,
            "lifecycle_guarded_apply_proof_ref",
            context="lifecycle_receipt_evidence",
        ),
        "artifact_mutation": _require_nonempty_string_from_mapping(
            receipt,
            "artifact_mutation",
            context="lifecycle_receipt_evidence",
        ),
        "memory_mutation": _require_nonempty_string_from_mapping(
            receipt,
            "memory_mutation",
            context="lifecycle_receipt_evidence",
        ),
        "lifecycle_mutation": _require_nonempty_string_from_mapping(
            receipt,
            "lifecycle_mutation",
            context="lifecycle_receipt_evidence",
        ),
        "repo_tracked": bool(receipt.get("repo_tracked", False)),
    }


def _forbidden_write_proof() -> dict[str, bool]:
    return {
        "repo_receipt_instance_written": False,
        "grant_truth_written": False,
        "grant_artifact_written": False,
        "memory_body_written": False,
        "fundability_verdict_written": False,
        "authoring_quality_verdict_written": False,
        "submission_ready_export_verdict_written": False,
    }


__all__ = [
    "LIFECYCLE_RECEIPT_BUNDLE_KIND",
    "build_lifecycle_receipt_bundle",
]
