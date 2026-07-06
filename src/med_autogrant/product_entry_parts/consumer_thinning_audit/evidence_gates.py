from __future__ import annotations

from typing import Any

NO_ACTIVE_CALLER_REFS_ONLY_AUTHORITY_BOUNDARY = {
    "refs_only": True,
    "can_authorize_physical_delete": False,
    "can_create_owner_receipt": False,
    "can_create_typed_blocker": False,
    "can_write_grant_truth": False,
    "can_claim_domain_ready": False,
    "can_claim_production_ready": False,
}


def build_no_active_caller_refs_only_authority_boundary() -> dict[str, bool]:
    return dict(NO_ACTIVE_CALLER_REFS_ONLY_AUTHORITY_BOUNDARY)


def build_default_caller_deletion_bridge_exit_gate(
    *,
    module_id: str,
    classification: str,
    current_surface_refs: list[str],
    mag_retained_authority: list[str],
) -> dict[str, Any]:
    is_authority = classification == "minimal_authority_function"
    return {
        "surface_kind": "mag_default_caller_deletion_bridge_exit_gate",
        "gate_id": f"mag.default_caller_deletion.{module_id}.bridge_exit.v1",
        "bridge_owner": "med-autogrant",
        "replacement_owner": "one-person-lab",
        "current_status": (
            "retained_mag_authority"
            if is_authority
            else "bridge_until_explicit_owner_receipt_authorizes_physical_delete"
        ),
        "required_before_retire": [] if is_authority else [
            "domain_authority_refs_preserved",
            "no_forbidden_write_proof_recorded",
            "explicit_owner_receipt_authorizes_physical_delete",
        ],
        "current_surface_refs": list(current_surface_refs),
        "retained_mag_authority": list(mag_retained_authority),
        "default_caller_deletion_evidence_scope": (
            "domain_owned_typed_blocker_and_no_forbidden_write_refs_only_no_physical_delete_authorization"
        ),
        "typed_blocker_refs": [
            (
                "typed-blocker:mag/default-caller-deletion/"
                f"{module_id}/physical-delete-requires-explicit-owner-receipt"
            )
        ],
        "no_forbidden_write_refs": [
            f"no-forbidden-write:mag/default-caller-deletion/{module_id}/refs-only-boundary"
        ],
        "no_forbidden_write_evidence_refs": [
            f"no-forbidden-write:mag/default-caller-deletion/{module_id}/refs-only-boundary"
        ],
        "provenance_refs": list(current_surface_refs),
        "domain_repo_physical_delete_authorized": False,
        "physical_delete_authorized_by_refs": False,
        "mag_can_write_generic_runtime": False,
        "mag_can_own_generated_default_caller": False,
        "opl_can_write_grant_truth": False,
        "opl_can_declare_fundability_or_export_verdict": False,
        "opl_can_issue_mag_owner_receipt": False,
    }


def build_legacy_exit_gate(
    *,
    gate_id: str,
    replacement_primitives: list[str],
    exit_action: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_legacy_surface_exit_gate",
        "gate_id": gate_id,
        "gate_status": "mag_handler_boundary_ready_external_caller_evidence_required",
        "replacement_owner": "one-person-lab",
        "replacement_primitives": replacement_primitives,
        "required_evidence": [
            "no_active_caller_scan",
            "replacement_surface_consumes_mag_refs",
            "direct_mag_domain_handler_no_regression",
            "history_or_tombstone_ref",
        ],
        "satisfied_evidence_refs": {
            "no_active_caller_scan": (
                "/product_entry_manifest/physical_skeleton_follow_through/"
                "active_path_current_role_guard"
            ),
            "replacement_surface_consumes_mag_refs": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff"
            ),
            "direct_mag_domain_handler_no_regression": (
                "tests/product_entry_cases/test_domain_handler.py"
            ),
            "history_or_tombstone_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "privatized_functional_module_audit"
            ),
        },
        "exit_action": exit_action,
        "claims_exit_complete": False,
        "claims_production_long_run_soak_complete": False,
        "mag_handler_boundary_ready": True,
        "external_opl_generated_or_hosted_caller_evidence_required": True,
        "authority_boundary": {
            "mag_can_keep_compatibility_alias": False,
            "mag_can_keep_generic_runtime_owner": False,
            "mag_keeps_safe_action_refs": True,
            "opl_can_write_grant_truth": False,
            "opl_can_declare_verdict": False,
        },
    }


def build_no_active_caller_evidence(
    *,
    module_id: str,
    active_callers: list[str],
    active_caller_status: str,
    evidence_refs: list[str],
) -> dict[str, Any]:
    no_active_caller = not active_callers
    return {
        "surface_kind": "mag_retired_surface_no_active_caller_evidence",
        "evidence_id": f"mag.retired_surface.{module_id}.no_active_caller.v1",
        "module_id": module_id,
        "status": (
            "no_active_caller_observed"
            if no_active_caller
            else "active_caller_present_delete_blocked"
        ),
        "no_active_caller_observed": no_active_caller,
        "active_caller_count": len(active_callers),
        "active_callers": list(active_callers),
        "active_caller_status": active_caller_status,
        "scan_ref": (
            "/product_entry_manifest/physical_skeleton_follow_through/"
            "active_path_current_role_guard"
        ),
        "evidence_refs": list(evidence_refs),
        "physical_delete_authorized": False,
        "claim_status": "no_active_caller_evidence_observed_not_delete_authorized",
        "authority_boundary": build_no_active_caller_refs_only_authority_boundary(),
    }
