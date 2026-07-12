from __future__ import annotations

from typing import Any

from med_autogrant.domain_runtime_parts.shared import (
    DOMAIN_AUTHORITY_SURFACE_REF,
    GENERATED_SESSION_RESUME_SURFACE_REF,
    GENERATED_SESSION_SURFACE_REF,
)


HOSTED_CONTRACT_VERSION = 1
HOSTED_CONTRACT_KIND = "hosted_contract_bundle"


def build_hosted_contract_bundle_document(
    *,
    final_package: dict[str, Any],
    program_id: str,
    runtime_substrate_contract: dict[str, Any],
    runtime_state_contract: dict[str, Any],
    operator_contract: dict[str, Any],
    domain_entry_contract: dict[str, Any],
    schema_contract: dict[str, Any],
    authoring_contract: dict[str, Any],
) -> dict[str, Any]:
    return {
        "contract_version": HOSTED_CONTRACT_VERSION,
        "bundle_kind": HOSTED_CONTRACT_KIND,
        "formal_entry_matrix": {
            "default_formal_entry": "CLI",
            "supported_protocol_layer": "MCP",
        },
        "execution_identity": {
            "grant_run_id": final_package["grant_run_id"],
            "workspace_id": final_package["workspace_id"],
            "draft_id": final_package["draft_id"],
            "program_id": program_id,
        },
        "runtime_substrate_contract": runtime_substrate_contract,
        "runtime_state_contract": runtime_state_contract,
        "session_contract": {
            "session_handle_kind": "grant_run_id",
            "session_owner": "one-person-lab",
            "generated_session_surface_ref": GENERATED_SESSION_SURFACE_REF,
            "generated_resume_surface_ref": GENERATED_SESSION_RESUME_SURFACE_REF,
            "domain_authority_surface_ref": DOMAIN_AUTHORITY_SURFACE_REF,
            "required_mag_authority_surfaces": [
                "build-artifact-bundle",
                "build-final-package",
                "build-submission-ready-package",
                "owner_receipt_contract",
                "ai_route_policy",
            ],
        },
        "operator_contract": operator_contract,
        "state_contract": {
            "workspace_surface_kind": "nsfc_workspace",
            "session_surface_kind": "opl_generated_session_surface",
            "domain_authority_surface_kind": "owner_receipt_contract",
            "artifact_bundle_kind": "artifact_bundle",
            "final_package_kind": "final_package",
        },
        "artifact_contract": {
            "artifact_bundle_manifest_kind": "artifact_bundle_manifest",
            "final_package_manifest_kind": "freeze_manifest",
            "lineage_fields": list(final_package["lineage"].keys()),
        },
        "audit_contract": {
            "verification_checkpoint_kind": "verification_checkpoint",
            "checkpoint_status_kind": "checkpoint_status",
            "reviewed_revision_evidence_kind": "reviewed_revision_evidence",
        },
        "domain_entry_contract": domain_entry_contract,
        "schema_contract": schema_contract,
        "authoring_contract": authoring_contract,
    }
