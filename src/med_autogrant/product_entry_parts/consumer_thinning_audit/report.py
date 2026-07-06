from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.consumer_thinning_audit.classification import (
    build_declarative_pack_surfaces,
    build_mag_owned_grant_authority_surfaces,
    build_refs_only_adapter_surfaces,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit.evidence_gates import (
    build_no_active_caller_refs_only_authority_boundary,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit.retired_surfaces import (
    build_retire_or_tombstone_surfaces,
)
from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


def build_privatized_functional_module_audit() -> dict[str, Any]:
    retire_or_tombstone_surfaces = build_retire_or_tombstone_surfaces()
    no_active_caller_evidence_summary = _build_no_active_caller_evidence_summary(
        retire_or_tombstone_surfaces
    )
    return {
        "surface_kind": "mag_privatized_functional_module_audit",
        "audit_id": "mag.privatized_functional_module_audit.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "state": "manifest_projected_for_opl_unified_audit",
        "standard_agent_source_shape_status": "landed",
        "mag_repo_active_source_shape_landed": True,
        "claims_descriptor_source_available_for_opl_generation": True,
        "classification_policy": (
            "classify_private_functional_surfaces_as_pack_refs_authority_or_legacy_proof"
        ),
        "opl_unified_audit_read_model": True,
        "claims_generic_runtime_removed_from_mag": False,
        "claims_opl_replacement_exists": True,
        "claims_domain_repo_physical_delete_authorized": False,
        "claims_production_long_run_soak_complete": False,
        "classification_buckets": [
            "declarative_pack_surface",
            "refs_only_adapter",
            "minimal_authority_function",
            "legacy_proof_tombstone",
        ],
        "declarative_pack_surfaces": build_declarative_pack_surfaces(),
        "refs_only_adapter_surfaces": build_refs_only_adapter_surfaces(),
        "mag_owned_grant_authority_surfaces": build_mag_owned_grant_authority_surfaces(),
        "retire_or_tombstone_surfaces": retire_or_tombstone_surfaces,
        "no_active_caller_evidence_summary": no_active_caller_evidence_summary,
        "private_platform_retirement_owner_evidence": {
            "surface_kind": "mag_private_platform_retirement_owner_evidence",
            "status": (
                "no_active_caller_evidence_observed_not_delete_authorized"
                if no_active_caller_evidence_summary[
                    "all_retired_surfaces_have_no_active_caller_evidence"
                ]
                else "active_caller_evidence_required"
            ),
            "accepted_ref_shapes": [
                "physical_delete_authorization_ref",
                "keep_as_authority_adapter_ref",
                "typed_blocker_ref",
                "owner_acceptance_ref",
            ],
            "observed_ref_shapes": ["no_active_caller_scan_ref"],
            "no_active_caller_evidence_summary_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "privatized_functional_module_audit/no_active_caller_evidence_summary"
            ),
            "physical_delete_authorized": False,
            "ready_claim_authorized": False,
            "next_owner_action": (
                "mag_owner_record_physical_delete_authorization_keep_adapter_or_typed_blocker"
            ),
            "authority_boundary": build_no_active_caller_refs_only_authority_boundary(),
        },
        "domain_authority_do_not_retire": [
            "grant_lifecycle_stage",
            "package_readiness_submission_ready",
            "fundability_verdict",
            "authoring_quality_verdict",
            "submission_ready_export_verdict",
            "grant_transition_oracle",
            "owner_receipt",
            "grant_strategy_memory_accept_reject",
        ],
        "opl_must_absorb_code_surfaces": [
            "workspace_source_intake_shell",
            "session_ledger",
            "attention_queue",
            "typed_queue",
            "stage_attempt_records",
            "generic_lifecycle_adapter",
            "artifact_package_lifecycle_shell",
            "runtime_observability_export",
            "operator_workbench_shell",
            "generic_scheduler_daemon",
        ],
        "mag_thin_adapter_code_surfaces": [
            "product_entry_manifest_builder",
            "domain_handler_guarded_domain_adapter",
            "domain_entry",
            "receipt_schema_and_writer",
            "grant_transition_oracle",
            "refs_only_projection_builders",
            "focused_contract_tests",
        ],
        "representative_private_functional_surfaces": {
            "legacy_local_runtime_history_attempt_record": {
                "module_ref": "legacy_local_runtime_history_attempt_record",
                "active_caller_status": (
                    "legacy_local_runtime_history_attempt_record_absent_no_active_caller"
                ),
                "migration_action": (
                    "OPL_owns_session_records_MAG_deleted_local_runtime_history_attempt_record_code"
                ),
            },
            "domain_handler_dispatch_product_shell": {
                "module_ref": "domain_handler_product_status_shell",
                "active_caller_status": "active_refs_only_domain_domain_handler_adapter",
                "migration_action": (
                    "OPL_generates_product_operator_shell_and_generic_dispatch_actions_"
                    "MAG_keeps_guarded_domain_adapter_refs"
                ),
            },
            "closed_default_path_history_index": {
                "module_ref": "closed_default_path_history_index",
                "active_caller_status": "closed_default_paths_absent_no_active_caller",
                "migration_action": (
                    "OPL_owns_generic_executor_adapter_MAG_keeps_only_compact_history_index_refs"
                ),
            },
        },
        "audit_refs": {
            "manifest_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
            "domain_handler_projection_ref": "/domain_handler_export/mag_consumer_thinning_contract",
            "consumer_thinning_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
            "external_evidence_receipt_ledger_ref": (
                "contracts/external_evidence/mag-evidence-receipt-ledger.json"
            ),
            "external_evidence_request_pack_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "external_evidence_request_pack"
            ),
            "grant_stage_controlled_attempt_closeout_ref": (
                "contracts/external_evidence/mag-evidence-receipt-ledger.json#/"
                "grant_stage_controlled_attempt_closeout"
            ),
            "thin_output_guard_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard"
            ),
            "ideal_state_ref": "/product_entry_manifest/ideal_state_closure_status",
            "generated_surface_bridge_exit_gate_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff/bridge_exit_gate"
            ),
        },
        "fail_closed_rules": {
            "delete_grant_lifecycle_stage_as_generic_lifecycle": False,
            "delete_package_readiness_as_generic_package_lifecycle": False,
            "delete_fundability_or_quality_verdict_as_generic_readiness": False,
            "provider_completion_is_grant_ready": False,
            "opl_observability_can_create_verdict": False,
            "mag_can_rebuild_generic_runtime": False,
        },
    }


def _build_no_active_caller_evidence_summary(
    retire_or_tombstone_surfaces: list[dict[str, Any]],
) -> dict[str, Any]:
    observed_module_ids = [
        item["module_id"]
        for item in retire_or_tombstone_surfaces
        if item.get("no_active_caller_observed") is True
    ]
    active_caller_module_ids = [
        item["module_id"]
        for item in retire_or_tombstone_surfaces
        if item.get("no_active_caller_observed") is not True
    ]
    return {
        "surface_kind": "mag_retired_surfaces_no_active_caller_evidence_summary",
        "status": (
            "all_retired_surfaces_no_active_caller_observed"
            if not active_caller_module_ids
            else "active_caller_evidence_required"
        ),
        "retired_surface_count": len(retire_or_tombstone_surfaces),
        "no_active_caller_observed_count": len(observed_module_ids),
        "active_caller_present_count": len(active_caller_module_ids),
        "all_retired_surfaces_have_no_active_caller_evidence": not active_caller_module_ids,
        "observed_module_ids": observed_module_ids,
        "active_caller_module_ids": active_caller_module_ids,
        "scan_ref": (
            "/product_entry_manifest/physical_skeleton_follow_through/"
            "active_path_current_role_guard"
        ),
        "physical_delete_authorized": False,
        "claim_status": "no_active_caller_evidence_observed_not_delete_authorized",
        "authority_boundary": build_no_active_caller_refs_only_authority_boundary(),
    }
