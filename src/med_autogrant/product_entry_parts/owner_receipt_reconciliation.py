from __future__ import annotations

from typing import Any, Mapping, Sequence

from med_autogrant.product_entry_parts.owner_receipt_common import (
    RECEIPT_RECONCILIATION_INVENTORY_KIND,
    RECEIPT_RECONCILIATION_PROOF_KIND,
    RECEIPT_SHAPES,
    forbidden_write_proof,
    require_choice,
    require_nonempty_string_from_receipt,
    require_owner_receipt_evidence,
)
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
)
from med_autogrant.product_entry_parts.typed_blocker_projection import (
    build_typed_blocker_projection,
    package_submission_ready_human_gate_authority_boundary,
)
from med_autogrant.workspace_types import WorkspaceStateError
from opl_harness_shared.owner_evidence import (
    build_owner_evidence_reconciliation_inventory,
    build_owner_evidence_reconciliation_proof,
)


_RECEIPT_RECONCILIATION_PROOF_PROFILE = {
    "surface_kind": RECEIPT_RECONCILIATION_PROOF_KIND,
    "state": "probe_reconciled_not_live_soak_complete",
    "domain_id": TARGET_DOMAIN_ID,
    "probe_scope": "controlled_soak_deferred_blocker_receipt_reconciliation",
    "source_refs": [
        "/product_entry_manifest/controlled_soak_no_regression_attempt",
        "/product_entry_manifest/controlled_stage_attempt_projection",
        "/product_entry_manifest/owner_receipt_contract",
        "domain handler-dispatch stage-attempt/closeout",
        "product owner-receipt-evidence",
    ],
    "owner_receipt_field": "mag_owner_receipt",
}
_RECEIPT_RECONCILIATION_INVENTORY_PROFILE = {
    "surface_kind": RECEIPT_RECONCILIATION_INVENTORY_KIND,
    "state": "read_projection_only_not_live_soak_complete",
    "domain_id": TARGET_DOMAIN_ID,
    "owner_receipt_field": "mag_owner_receipt",
}


def build_controlled_soak_receipt_reconciliation_proof(
    *,
    owner_receipt_evidence: Mapping[str, Any],
    opl_ledger_ref: str,
    domain_handler_closeout_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    receipt = require_owner_receipt_evidence(owner_receipt_evidence)
    resolved_ledger_ref = _require_nonempty_string(opl_ledger_ref, field_name="opl_ledger_ref")
    closeout_result = dict(domain_handler_closeout_result or {})
    receipt_ref = require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
    receipt_shape = require_choice(
        require_nonempty_string_from_receipt(receipt, "receipt_shape"),
        choices=RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    authority_boundary = _authority_boundary(receipt)
    try:
        payload = build_owner_evidence_reconciliation_proof(
            profile=_RECEIPT_RECONCILIATION_PROOF_PROFILE,
            owner_receipt_projection={
                "receipt_ref": receipt_ref,
                "receipt_id": require_nonempty_string_from_receipt(receipt, "receipt_id"),
                "receipt_shape": receipt_shape,
                "stage_id": require_nonempty_string_from_receipt(receipt, "stage_id"),
                "source_ref": require_nonempty_string_from_receipt(receipt, "source_ref"),
                "owner_receipt_contract_ref": require_nonempty_string_from_receipt(
                    receipt,
                    "owner_receipt_contract_ref",
                ),
            },
            ledger_ref=resolved_ledger_ref,
            typed_blocker=_reconciled_typed_blocker(receipt, closeout_result),
            no_regression_evidence_refs=_reconciled_no_regression_evidence_refs(
                receipt,
                closeout_result,
            ),
            closeout_payload_consumed=bool(closeout_result),
            receipt_ref_matches_closeout=_receipt_ref_matches_domain_handler(
                receipt_ref,
                closeout_result,
            ),
            authority_boundary=authority_boundary,
            forbidden_write_proof=dict(receipt["forbidden_write_proof"]),
        )
    except ValueError as exc:
        raise WorkspaceStateError(str(exc)) from exc
    return {
        "ok": True,
        "command": "controlled-soak-receipt-reconciliation-proof",
        "receipt_reconciliation_proof": payload,
    }


def build_controlled_soak_receipt_reconciliation_inventory(
    *,
    owner_receipt_evidence_items: Sequence[Mapping[str, Any]],
    opl_ledger_ref: str,
    domain_handler_closeout_results: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    resolved_ledger_ref = _require_nonempty_string(opl_ledger_ref, field_name="opl_ledger_ref")
    if not owner_receipt_evidence_items:
        raise WorkspaceStateError("owner_receipt_evidence_items 至少需要一条 receipt evidence。")
    closeout_by_receipt_ref = _index_closeout_results_by_receipt_ref(
        domain_handler_closeout_results or []
    )
    proofs: list[dict[str, Any]] = []
    for receipt_payload in owner_receipt_evidence_items:
        receipt = require_owner_receipt_evidence(receipt_payload)
        receipt_ref = require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
        proof = build_controlled_soak_receipt_reconciliation_proof(
            owner_receipt_evidence=receipt,
            opl_ledger_ref=resolved_ledger_ref,
            domain_handler_closeout_result=closeout_by_receipt_ref.get(receipt_ref),
        )["receipt_reconciliation_proof"]
        proofs.append(proof)
    try:
        payload = build_owner_evidence_reconciliation_inventory(
            profile=_RECEIPT_RECONCILIATION_INVENTORY_PROFILE,
            proofs=proofs,
            ledger_ref=resolved_ledger_ref,
            closeout_result_count=len(closeout_by_receipt_ref),
            authority_boundary=_authority_boundary(),
            forbidden_write_proof=forbidden_write_proof(),
        )
    except ValueError as exc:
        raise WorkspaceStateError(str(exc)) from exc
    return {
        "ok": True,
        "command": "controlled-soak-receipt-reconciliation-inventory",
        "receipt_reconciliation_inventory": payload,
    }


def _authority_boundary(receipt: Mapping[str, Any] | None = None) -> dict[str, Any]:
    boundary = {
        "mag_owner_receipt_authority": True,
        "opl_ref_consumer_only": True,
        "can_declare_fundability_ready": False,
        "can_declare_authoring_quality_ready": False,
        "can_declare_submission_ready_export": False,
    }
    if receipt is not None:
        boundary.update(package_submission_ready_human_gate_authority_boundary(receipt))
    return boundary


def _index_closeout_results_by_receipt_ref(
    closeout_results: Sequence[Mapping[str, Any]],
) -> dict[str, Mapping[str, Any]]:
    indexed: dict[str, Mapping[str, Any]] = {}
    for closeout in closeout_results:
        receipt_ref = closeout.get("receipt_ref")
        if not isinstance(receipt_ref, str) or not receipt_ref.strip():
            raise WorkspaceStateError("domain_handler_closeout_result.receipt_ref 必须是非空字符串。")
        if receipt_ref in indexed:
            raise WorkspaceStateError(f"domain_handler_closeout_result.receipt_ref 重复: {receipt_ref}")
        indexed[receipt_ref] = closeout
    return indexed


def _receipt_ref_matches_domain_handler(
    receipt_ref: str,
    closeout_result: Mapping[str, Any],
) -> bool | None:
    if not closeout_result:
        return None
    return closeout_result.get("receipt_ref") == receipt_ref


def _reconciled_typed_blocker(
    receipt: Mapping[str, Any],
    closeout_result: Mapping[str, Any],
) -> dict[str, Any] | None:
    domain_handler_blocker = closeout_result.get("typed_blocker")
    if isinstance(domain_handler_blocker, Mapping):
        return dict(domain_handler_blocker)
    return build_typed_blocker_projection(
        receipt,
        blocker_kind="mag_stage_attempt_owner_receipt_required",
    )


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
        receipt_ref = require_nonempty_string_from_receipt(receipt, "receipt_instance_ref")
        if receipt_ref not in refs:
            refs.append(receipt_ref)
    return refs
