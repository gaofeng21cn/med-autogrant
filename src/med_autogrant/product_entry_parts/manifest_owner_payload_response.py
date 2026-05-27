from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.opl_owner_payload_response import (
    build_opl_owner_payload_response,
)
from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_mapping
from med_autogrant.workspace_types import WorkspaceStateError


REPO_ROOT = Path(__file__).resolve().parents[3]
PRODUCTION_ACCEPTANCE_REF = "contracts/production_acceptance/mag-production-acceptance.json"
EXTERNAL_EVIDENCE_LEDGER_REF = "contracts/external_evidence/mag-evidence-receipt-ledger.json"
WORKSPACE_RECEIPT_SCALEOUT_REF = (
    "contracts/production_acceptance/mag-workspace-receipt-scaleout-evidence-20260527.json"
)
_REQUIRED_CATEGORIES = (
    "owner_receipt",
    "memory_accept_reject",
    "package_export_lifecycle",
    "cleanup_restore_retention_lifecycle",
)


def build_manifest_owner_payload_surfaces() -> dict[str, Any]:
    production_acceptance = _read_json_object(PRODUCTION_ACCEPTANCE_REF)
    external_evidence_ledger = _read_json_object(EXTERNAL_EVIDENCE_LEDGER_REF)
    workspace_scaleout_evidence = _read_json_object(WORKSPACE_RECEIPT_SCALEOUT_REF)

    owner_payload_response = build_opl_owner_payload_response(
        production_acceptance=production_acceptance,
        external_evidence_receipt_ledger=external_evidence_ledger,
        receipt_readiness_projection=_manifest_receipt_readiness_projection(
            workspace_scaleout_evidence
        ),
    )
    owner_payload_response["source_surface_refs"] = {
        "production_acceptance_ref": PRODUCTION_ACCEPTANCE_REF,
        "external_evidence_ledger_ref": EXTERNAL_EVIDENCE_LEDGER_REF,
        "workspace_receipt_scaleout_evidence_ref": WORKSPACE_RECEIPT_SCALEOUT_REF,
    }
    owner_payload_response["workspace_receipt_scaleout_evidence_ref"] = (
        WORKSPACE_RECEIPT_SCALEOUT_REF
    )
    owner_payload_response["workspace_receipt_scaleout_summary"] = dict(
        _require_mapping(
            workspace_scaleout_evidence,
            "workspace_receipt_scaleout",
            context="workspace_receipt_scaleout_evidence",
        )
    )
    owner_payload_response["workspace_receipt_scaleout_owner_payload_response_summary"] = dict(
        _require_mapping(
            workspace_scaleout_evidence,
            "owner_payload_response",
            context="workspace_receipt_scaleout_evidence",
        )
    )
    owner_payload_response["manifest_projection_policy"] = (
        "default_manifest_refs_only_owner_payload_response_with_count_only_scaleout_provenance"
    )
    owner_payload_response["operator_payload_submitted"] = False
    owner_payload_response["workspace_receipt_scaleout_count_snapshot_is_receipt_refs"] = False

    return {
        "owner_payload_response": owner_payload_response,
        "workspace_receipt_scaleout_evidence": workspace_scaleout_evidence,
    }


def _manifest_receipt_readiness_projection(
    workspace_scaleout_evidence: Mapping[str, Any],
) -> dict[str, Any]:
    scaleout_summary = _require_mapping(
        workspace_scaleout_evidence,
        "workspace_receipt_scaleout",
        context="workspace_receipt_scaleout_evidence",
    )
    return {
        "surface_kind": "mag_receipt_readiness_projection",
        "version": "v1",
        "state": "manifest_owner_payload_refs_ready_workspace_receipt_scaleout_count_only",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "required_categories": list(_REQUIRED_CATEGORIES),
        "missing_categories": [],
        "summary": {
            "required_category_count": len(_REQUIRED_CATEGORIES),
            "covered_category_count": scaleout_summary.get("covered_category_count"),
            "missing_category_count": scaleout_summary.get("missing_category_count"),
            "total_receipt_ref_count": 0,
            "count_only_scaleout_total_receipt_ref_count": scaleout_summary.get(
                "total_receipt_ref_count"
            ),
        },
        "receipt_refs": {category_id: [] for category_id in _REQUIRED_CATEGORIES},
        "projection_policy": (
            "manifest_default_does_not_replay_workspace_receipt_instances_"
            "count_only_scaleout_snapshot_kept_as_provenance"
        ),
        "authority_boundary": {
            "mag_owns_receipt_readiness_projection": True,
            "projection_scope": "manifest_owner_payload_response_default",
            "refs_only_projection": True,
            "workspace_scaleout_snapshot_is_count_only": True,
            "can_declare_fundability_ready": False,
            "can_declare_quality_ready": False,
            "can_declare_export_ready": False,
            "can_declare_submission_ready": False,
        },
    }


def _read_json_object(relative_path: str) -> dict[str, Any]:
    path = REPO_ROOT / relative_path
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise WorkspaceStateError(f"无法读取 MAG owner-payload contract: {relative_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(f"MAG owner-payload contract 不是合法 JSON: {relative_path}") from exc
    if not isinstance(payload, dict):
        raise WorkspaceStateError(f"MAG owner-payload contract 必须是 JSON object: {relative_path}")
    return payload


__all__ = [
    "build_manifest_owner_payload_surfaces",
]
