from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.owner_receipt_common import (
    OWNER_RECEIPT_EVIDENCE_KIND,
    RECEIPT_SHAPES,
    STAGE_IDS,
    forbidden_write_proof,
    opl_receipt_ref_consumption,
    require_choice,
    resolve_receipt_runtime_root,
    write_receipt,
)
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
)


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
    resolved_stage_id = require_choice(stage_id, choices=STAGE_IDS, field_name="stage_id")
    resolved_shape = require_choice(
        receipt_shape,
        choices=RECEIPT_SHAPES,
        field_name="receipt_shape",
    )
    resolved_source_ref = _require_nonempty_string(source_ref, field_name="source_ref")
    resolved_summary = _require_nonempty_string(closeout_summary, field_name="closeout_summary")
    resolved_receipt_id = receipt_id or f"{resolved_stage_id}-{resolved_shape}"
    runtime_state_root = resolve_receipt_runtime_root(runtime_root)
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
        "owner_receipt_contract_ref": "contracts/owner_receipt_contract.json",
        "source_refs": [
            "agent/stages/manifest.json",
            "/product_entry_manifest/family_stage_control_plane",
            "contracts/owner_receipt_contract.json",
            "contracts/artifact_locator_contract.json",
            "contracts/functional_privatization_audit.json",
        ],
        "artifact_mutation": "none",
        "memory_mutation": "none",
        "lifecycle_mutation": "none",
        "repo_tracked": False,
        "forbidden_write_proof": forbidden_write_proof(),
        "opl_consumption": opl_receipt_ref_consumption(),
        "closeout_refs": dict(closeout_refs or {}),
    }
    write_receipt(receipt_path, receipt)
    return {
        "ok": True,
        "command": "owner-receipt-evidence",
        "owner_receipt_evidence": receipt,
    }
