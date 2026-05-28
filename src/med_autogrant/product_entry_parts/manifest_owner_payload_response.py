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
MANIFEST_SUSTAINED_CONSUMPTION_EVIDENCE_REF = (
    "contracts/production_acceptance/"
    "mag-manifest-sustained-consumption-evidence-20260528.json"
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
    manifest_sustained_consumption_evidence = _read_json_object(
        MANIFEST_SUSTAINED_CONSUMPTION_EVIDENCE_REF
    )
    manifest_sustained_consumption_payload_response = dict(
        _require_mapping(
            manifest_sustained_consumption_evidence,
            "manifest_sustained_consumption_payload_response",
            context="manifest_sustained_consumption_evidence",
        )
    )

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
        "manifest_sustained_consumption_evidence_ref": (
            MANIFEST_SUSTAINED_CONSUMPTION_EVIDENCE_REF
        ),
    }
    owner_payload_response["workspace_receipt_scaleout_evidence_ref"] = (
        WORKSPACE_RECEIPT_SCALEOUT_REF
    )
    owner_payload_response["manifest_sustained_consumption_evidence_ref"] = (
        MANIFEST_SUSTAINED_CONSUMPTION_EVIDENCE_REF
    )
    owner_payload_response["manifest_sustained_consumption_payload_response"] = (
        manifest_sustained_consumption_payload_response
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
    owner_payload_response["manifest_consumer_evidence"] = _manifest_consumer_evidence(
        owner_payload_response,
        workspace_scaleout_evidence,
        manifest_sustained_consumption_evidence,
    )

    return {
        "owner_payload_response": owner_payload_response,
        "workspace_receipt_scaleout_evidence": workspace_scaleout_evidence,
        "manifest_sustained_consumption_evidence": manifest_sustained_consumption_evidence,
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


def _manifest_consumer_evidence(
    owner_payload_response: Mapping[str, Any],
    workspace_scaleout_evidence: Mapping[str, Any],
    manifest_sustained_consumption_evidence: Mapping[str, Any],
) -> dict[str, Any]:
    scaleout_summary = _require_mapping(
        workspace_scaleout_evidence,
        "workspace_receipt_scaleout",
        context="workspace_receipt_scaleout_evidence",
    )
    stage_payload = _require_mapping(
        owner_payload_response,
        "stage_expected_receipt_payload_summary",
        context="owner_payload_response",
    )
    manifest_payload_response = _require_mapping(
        manifest_sustained_consumption_evidence,
        "manifest_sustained_consumption_payload_response",
        context="manifest_sustained_consumption_evidence",
    )
    return {
        "surface_kind": "mag_manifest_owner_payload_consumer_evidence",
        "version": "v1",
        "state": "manifest_owner_payload_response_consumed_refs_only",
        "consumer": "one_person_lab_app_operator_manifest",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "consumed_surface_refs": {
            "owner_payload_response_ref": "/product_entry_manifest/owner_payload_response",
            "workspace_receipt_scaleout_evidence_ref": (
                "/product_entry_manifest/workspace_receipt_scaleout_evidence"
            ),
            "stage_expected_receipt_payload_summary_ref": (
                "/product_entry_manifest/owner_payload_response/"
                "stage_expected_receipt_payload_summary"
            ),
            "manifest_sustained_consumption_evidence_ref": (
                "/product_entry_manifest/manifest_sustained_consumption_evidence"
            ),
            "manifest_sustained_consumption_payload_response_ref": (
                "/product_entry_manifest/manifest_sustained_consumption_evidence/"
                "manifest_sustained_consumption_payload_response"
            ),
        },
        "consumed_fields": [
            "domain_owner_receipt_refs",
            "owner_chain_refs",
            "typed_blocker_refs",
            "no_regression_evidence_refs",
            "stage_expected_receipt_payload_summary",
            "workspace_receipt_scaleout_summary",
            "manifest_sustained_consumption_payload_response",
        ],
        "observed_counts": {
            "domain_owner_receipt_ref_count": len(
                _string_list(owner_payload_response.get("domain_owner_receipt_refs"))
            ),
            "owner_chain_ref_count": len(
                _string_list(owner_payload_response.get("owner_chain_refs"))
            ),
            "typed_blocker_ref_count": len(
                _string_list(owner_payload_response.get("typed_blocker_refs"))
            ),
            "no_regression_evidence_ref_count": len(
                _string_list(owner_payload_response.get("no_regression_evidence_refs"))
            ),
            "stage_expected_receipt_payload_stage_count": stage_payload.get("stage_count"),
            "workspace_count": scaleout_summary.get("workspace_count"),
            "count_only_scaleout_total_receipt_ref_count": scaleout_summary.get(
                "total_receipt_ref_count"
            ),
            "manifest_sustained_consumption_payload_response_count": 1,
        },
        "manifest_sustained_consumption_payload_status": manifest_payload_response.get("status"),
        "manifest_sustained_consumption_recommended_payload_path": (
            manifest_payload_response.get("recommended_payload_path")
        ),
        "manifest_sustained_consumption_operator_payload_submitted": bool(
            manifest_payload_response.get("operator_payload_submitted")
        ),
        "human_gate_blocker_refs": list(_string_list(owner_payload_response.get("typed_blocker_refs"))),
        "sustained_consumption_followthrough_workorder": (
            _sustained_consumption_followthrough_workorder()
        ),
        "projection_policy": (
            "default_manifest_consumer_reads_owner_payload_refs_and_count_only_scaleout_"
            "without_submitting_operator_payload_or_claiming_ready"
        ),
        "operator_payload_submitted": False,
        "count_only_scaleout_snapshot_is_receipt_refs": False,
        "claims_sustained_app_consumption_complete": False,
        "claims_grant_ready": False,
        "claims_quality_ready": False,
        "claims_export_ready": False,
        "claims_submission_ready": False,
        "claims_provider_long_soak_complete": False,
        "authority_boundary": {
            "owner": TARGET_DOMAIN_ID,
            "refs_only": True,
            "app_operator_consumes_manifest_refs_only": True,
            "can_write_grant_truth": False,
            "can_read_memory_body": False,
            "can_read_artifact_body": False,
            "can_create_owner_receipt": False,
            "can_submit_operator_payload": False,
            "can_declare_app_sustained_consumption_complete": False,
            "can_declare_submission_ready": False,
            "typed_blocker_is_submission_ready": False,
        },
    }


def _sustained_consumption_followthrough_workorder() -> dict[str, Any]:
    required_refs = [
        "app_operator_consumption_ref",
        "default_caller_consumption_ref",
        "owner_payload_response_ref",
        "workspace_receipt_scaleout_evidence_ref",
        "no_forbidden_write_ref",
        "long_soak_or_typed_blocker_ref",
    ]
    allowed_operator_payload_fields = [*required_refs, "typed_blocker_refs"]
    return {
        "surface_kind": "mag_manifest_sustained_consumption_followthrough_workorder",
        "version": "v1",
        "status": "requires_real_app_operator_or_default_caller_payload",
        "authority_command": "authority manifest-consumption-payload",
        "authority_command_internal": "manifest-sustained-consumption-payload",
        "payload_owner": "app_operator_or_release_default_caller",
        "accepted_payload_path_policy": (
            "real_app_operator_or_default_caller_consumption_refs_or_domain_owned_typed_blocker"
        ),
        "required_operator_payload_refs": required_refs,
        "allowed_operator_payload_fields": allowed_operator_payload_fields,
        "payload_template": {ref: [] for ref in required_refs},
        "accepted_payload_paths": {
            "sustained_consumption_refs_path": {
                "required_operator_payload_refs": required_refs,
                "requires_long_soak_or_typed_blocker_ref": True,
                "typed_blocker_refs_must_be_absent": True,
                "closes_grant_ready": False,
                "closes_submission_ready": False,
                "closes_provider_long_soak": False,
            },
            "typed_blocker_path": {
                "required_operator_payload_refs": ["typed_blocker_refs"],
                "success_claimed": False,
                "closes_grant_ready": False,
                "closes_submission_ready": False,
                "closes_provider_long_soak": False,
            },
        },
        "empty_payload_template_is_success_evidence": False,
        "rejects_unknown_operator_payload_fields": True,
        "operator_payload_submitted": False,
        "claims_sustained_app_consumption_complete": False,
        "claims_grant_ready": False,
        "claims_submission_ready": False,
        "claims_provider_long_soak_complete": False,
        "authority_boundary": {
            "owner": TARGET_DOMAIN_ID,
            "refs_only": True,
            "can_write_grant_truth": False,
            "can_read_memory_body": False,
            "can_read_artifact_body": False,
            "can_create_owner_receipt": False,
            "can_submit_operator_payload": False,
            "can_declare_app_sustained_consumption_complete": False,
            "can_declare_submission_ready": False,
            "can_declare_provider_long_soak_complete": False,
        },
    }


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item.strip()]


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
