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
LIFECYCLE_RECEIPT_EVIDENCE_KIND = "mag_lifecycle_receipt_evidence"
RECEIPT_RECONCILIATION_PROOF_KIND = "mag_controlled_soak_receipt_reconciliation_proof"

_RECEIPT_SHAPES = ("domain_owner_receipt", "typed_blocker", "no_regression_evidence")
_STAGE_IDS = (
    "call_and_candidate_intake",
    "fundability_strategy",
    "specific_aims_and_structure",
    "proposal_authoring",
    "review_and_rebuttal",
    "package_and_submit_ready",
)
_LIFECYCLE_OPERATIONS = ("cleanup", "restore", "retention")


def write_owner_receipt_evidence(
    *,
    input_path: str | Path,
    receipt_shape: str,
    stage_id: str,
    source_ref: str,
    closeout_summary: str,
    runtime_root: str | Path | None = None,
    receipt_id: str | None = None,
    closeout_refs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    resolved_stage_id = _require_choice(stage_id, choices=_STAGE_IDS, field_name="stage_id")
    resolved_shape = _require_choice(
        receipt_shape,
        choices=_RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    resolved_source_ref = _require_nonempty_string(source_ref, field_name="source_ref")
    resolved_summary = _require_nonempty_string(closeout_summary, field_name="closeout_summary")
    resolved_receipt_id = receipt_id or f"{resolved_stage_id}-{resolved_shape}"
    runtime_state_root = _resolve_runtime_root(runtime_root)
    receipt_path = runtime_state_root / "receipts" / "owner-receipts" / f"{resolved_receipt_id}.json"
    receipt = {
        "surface_kind": OWNER_RECEIPT_EVIDENCE_KIND,
        "version": "v1",
        "receipt_id": f"mag.owner_receipt.{resolved_receipt_id}",
        "state": "runtime_receipt_instance_written",
        "receipt_shape": resolved_shape,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "stage_id": resolved_stage_id,
        "source_ref": resolved_source_ref,
        "closeout_summary": resolved_summary,
        "workspace_locator": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": str(resolved_input_path),
            "repo_tracked": False,
        },
        "receipt_instance_ref": str(receipt_path),
        "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
        "source_refs": [
            "/product_entry_manifest/controlled_stage_attempt_projection",
            "/product_entry_manifest/owner_receipt_contract",
            "/product_entry_manifest/controlled_domain_memory_apply_proof",
            "/product_entry_manifest/artifact_locator_contract",
            "/product_entry_manifest/grant_authoring_readiness",
        ],
        "artifact_mutation": "none",
        "memory_mutation": "none",
        "lifecycle_mutation": "none",
        "repo_tracked": False,
        "forbidden_write_proof": _forbidden_write_proof(),
        "opl_consumption": _opl_receipt_ref_consumption(),
        "closeout_refs": dict(closeout_refs or {}),
    }
    _write_receipt(receipt_path, receipt)
    return {
        "ok": True,
        "command": "owner-receipt-evidence",
        "owner_receipt_evidence": receipt,
    }


def write_lifecycle_receipt_evidence(
    *,
    input_path: str | Path,
    operation: str,
    receipt_shape: str,
    source_ref: str,
    closeout_summary: str,
    runtime_root: str | Path | None = None,
    receipt_id: str | None = None,
) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    resolved_operation = _require_choice(
        operation,
        choices=_LIFECYCLE_OPERATIONS,
        field_name="operation",
    )
    resolved_shape = _require_choice(
        receipt_shape,
        choices=_RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    resolved_source_ref = _require_nonempty_string(source_ref, field_name="source_ref")
    resolved_summary = _require_nonempty_string(closeout_summary, field_name="closeout_summary")
    resolved_receipt_id = receipt_id or f"{resolved_operation}-{resolved_shape}"
    runtime_state_root = _resolve_runtime_root(runtime_root)
    receipt_path = runtime_state_root / "receipts" / "lifecycle" / f"{resolved_receipt_id}.json"
    receipt = {
        "surface_kind": LIFECYCLE_RECEIPT_EVIDENCE_KIND,
        "version": "v1",
        "receipt_id": f"mag.lifecycle.receipt.{resolved_receipt_id}",
        "state": "runtime_receipt_instance_written",
        "operation": resolved_operation,
        "receipt_shape": resolved_shape,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "source_ref": resolved_source_ref,
        "closeout_summary": resolved_summary,
        "workspace_locator": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": str(resolved_input_path),
            "repo_tracked": False,
        },
        "receipt_instance_ref": str(receipt_path),
        "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
        "lifecycle_guarded_apply_proof_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
        "source_refs": [
            "/product_entry_manifest/lifecycle_guarded_apply_proof",
            "/product_entry_manifest/owner_receipt_contract",
            "/product_entry_manifest/artifact_locator_contract",
            "/product_entry_manifest/runtime_control/restore_point",
        ],
        "artifact_mutation": "none",
        "memory_mutation": "none",
        "lifecycle_mutation": "receipt_metadata_only",
        "repo_tracked": False,
        "forbidden_write_proof": _forbidden_write_proof(),
        "opl_consumption": _opl_receipt_ref_consumption(),
    }
    _write_receipt(receipt_path, receipt)
    return {
        "ok": True,
        "command": "lifecycle-receipt-evidence",
        "lifecycle_receipt_evidence": receipt,
    }


def build_controlled_soak_receipt_reconciliation_proof(
    *,
    owner_receipt_evidence: Mapping[str, Any],
    opl_ledger_ref: str,
    sidecar_closeout_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    receipt = _require_owner_receipt_evidence(owner_receipt_evidence)
    resolved_ledger_ref = _require_nonempty_string(opl_ledger_ref, field_name="opl_ledger_ref")
    closeout_result = dict(sidecar_closeout_result or {})
    receipt_ref = _require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
    receipt_shape = _require_choice(
        _require_nonempty_string_from_receipt(receipt, "receipt_shape"),
        choices=_RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    typed_blocker = _reconciled_typed_blocker(receipt, closeout_result)
    evidence_refs = _reconciled_no_regression_evidence_refs(receipt, closeout_result)
    payload = {
        "surface_kind": RECEIPT_RECONCILIATION_PROOF_KIND,
        "version": "v1",
        "state": "probe_reconciled_not_live_soak_complete",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "probe_scope": "controlled_soak_deferred_blocker_receipt_reconciliation",
        "claims_production_long_run_soak_complete": False,
        "rebuilds_opl_runtime": False,
        "source_refs": [
            "/product_entry_manifest/controlled_soak_no_regression_attempt",
            "/product_entry_manifest/controlled_stage_attempt_projection",
            "/product_entry_manifest/owner_receipt_contract",
            "product sidecar-dispatch stage-attempt/closeout",
            "product owner-receipt-evidence",
        ],
        "opl_ledger": {
            "ledger_ref": resolved_ledger_ref,
            "role": "external_ref_for_reconciliation_only",
            "mag_writes_opl_ledger": False,
            "opl_holds_grant_truth": False,
        },
        "mag_owner_receipt": {
            "receipt_ref": receipt_ref,
            "receipt_id": _require_nonempty_string_from_receipt(receipt, "receipt_id"),
            "receipt_shape": receipt_shape,
            "stage_id": _require_nonempty_string_from_receipt(receipt, "stage_id"),
            "source_ref": _require_nonempty_string_from_receipt(receipt, "source_ref"),
            "owner_receipt_contract_ref": _require_nonempty_string_from_receipt(
                receipt,
                "owner_receipt_contract_ref",
            ),
        },
        "typed_blocker": typed_blocker,
        "no_regression_evidence": {
            "evidence_refs": evidence_refs,
            "present": bool(evidence_refs),
            "repo_tracked_projection_only": True,
        },
        "reconciliation": {
            "status": _reconciliation_status(receipt_shape, typed_blocker, evidence_refs),
            "receipt_ref_matches_sidecar": _receipt_ref_matches_sidecar(receipt_ref, closeout_result),
            "opl_ledger_ref_matches_receipt_source": (
                resolved_ledger_ref == _require_nonempty_string_from_receipt(receipt, "source_ref")
            ),
            "closeout_payload_consumed": bool(closeout_result),
        },
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "opl_ref_consumer_only": True,
            "can_declare_fundability_ready": False,
            "can_declare_authoring_quality_ready": False,
            "can_declare_submission_ready_export": False,
        },
        "forbidden_write_proof": dict(receipt["forbidden_write_proof"]),
    }
    return {
        "ok": True,
        "command": "controlled-soak-receipt-reconciliation-proof",
        "receipt_reconciliation_proof": payload,
    }


def _resolve_runtime_root(runtime_root: str | Path | None) -> Path:
    if runtime_root is not None:
        return Path(runtime_root).expanduser().resolve()
    return resolve_runtime_state_root()


def _require_choice(value: str, *, choices: tuple[str, ...], field_name: str) -> str:
    resolved = _require_nonempty_string(value, field_name=field_name)
    if resolved not in choices:
        raise WorkspaceStateError(f"{field_name} 不支持: {resolved}。只允许 {', '.join(choices)}。")
    return resolved


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


def _opl_receipt_ref_consumption() -> dict[str, bool | str]:
    return {
        "role": "receipt_ref_consumer_only",
        "consumes_receipt_ref_only": True,
        "can_write_grant_truth": False,
        "can_write_memory_body": False,
        "can_declare_export_ready": False,
    }


def _write_receipt(path: Path, receipt: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 receipt evidence 失败: {path}") from exc


def _require_owner_receipt_evidence(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("surface_kind") != OWNER_RECEIPT_EVIDENCE_KIND:
        raise WorkspaceStateError("owner_receipt_evidence.surface_kind 必须是 mag_owner_receipt_evidence。")
    forbidden = payload.get("forbidden_write_proof")
    if not isinstance(forbidden, Mapping):
        raise WorkspaceStateError("owner_receipt_evidence 缺少 forbidden_write_proof。")
    if any(bool(forbidden.get(key)) for key in (
        "repo_receipt_instance_written",
        "grant_truth_written",
        "grant_artifact_written",
        "memory_body_written",
        "fundability_verdict_written",
        "authoring_quality_verdict_written",
        "submission_ready_export_verdict_written",
    )):
        raise WorkspaceStateError("owner_receipt_evidence 不能包含 MAG/OPL forbidden write。")
    return payload


def _require_nonempty_string_from_receipt(receipt: Mapping[str, Any], key: str) -> str:
    return _require_nonempty_string(receipt.get(key), field_name=key)


def _receipt_ref_matches_sidecar(receipt_ref: str, closeout_result: Mapping[str, Any]) -> bool | None:
    if not closeout_result:
        return None
    return closeout_result.get("receipt_ref") == receipt_ref


def _reconciled_typed_blocker(
    receipt: Mapping[str, Any],
    closeout_result: Mapping[str, Any],
) -> dict[str, Any] | None:
    sidecar_blocker = closeout_result.get("typed_blocker")
    if isinstance(sidecar_blocker, Mapping):
        return dict(sidecar_blocker)
    if receipt.get("receipt_shape") != "typed_blocker":
        return None
    return {
        "blocker_kind": "mag_stage_attempt_owner_receipt_required",
        "owner": TARGET_DOMAIN_ID,
        "receipt_ref": receipt["receipt_instance_ref"],
        "source_ref": receipt["source_ref"],
        "next_action": "Route the blocker back to MAG owner surface before mutating grant truth, memory body, or artifact content.",
    }


def _reconciled_no_regression_evidence_refs(
    receipt: Mapping[str, Any],
    closeout_result: Mapping[str, Any],
) -> list[str]:
    refs: list[str] = []
    receipt_refs = closeout_result.get("receipt_refs")
    if isinstance(receipt_refs, Mapping):
        no_regression_ref = receipt_refs.get("no_regression_evidence_ref")
        if isinstance(no_regression_ref, str) and no_regression_ref:
            refs.append(no_regression_ref)
    if receipt.get("receipt_shape") == "no_regression_evidence":
        receipt_ref = _require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
        if receipt_ref not in refs:
            refs.append(receipt_ref)
    return refs


def _reconciliation_status(
    receipt_shape: str,
    typed_blocker: Mapping[str, Any] | None,
    evidence_refs: list[str],
) -> str:
    if receipt_shape == "typed_blocker" and typed_blocker is not None:
        return "typed_blocker_reconciled"
    if receipt_shape == "no_regression_evidence" and evidence_refs:
        return "no_regression_evidence_reconciled"
    return "domain_owner_receipt_reconciled"
