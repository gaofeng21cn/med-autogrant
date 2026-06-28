from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = "contracts/runtime-program/opl-family-contract-adoption.json"


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _contract() -> dict[str, object]:
    return json.loads(_read(CONTRACT_PATH))


def test_mag_adoption_contract_consumes_opl_scheduler_replacement_without_generic_owner() -> None:
    contract = _contract()
    thinning = contract["mag_consumer_thinning_contract"]

    assert thinning["surface_kind"] == "mag_consumer_thinning_contract"
    assert thinning["manifest_surface_ref"] == "/product_entry_manifest/mag_consumer_thinning_contract"
    assert thinning["consumes_opl_family_primitive"] == "family_scheduler_replacement"
    assert thinning["adapter_role"] == "domain_authority_pack_with_thin_program_surface"
    assert thinning["active_caller_owner"] == "med-autogrant"
    assert thinning["active_caller_surface"] == "mag_direct_domain_entry_until_opl_caller_evidence"
    assert thinning["mag_owned_outputs"] == [
        "grant_owned_refs",
        "owner_receipt",
        "typed_blocker",
        "verdict_refs",
        "domain_action_metadata",
    ]
    assert thinning["forbidden_mag_generic_owner_roles"] == [
        "generic_scheduler_owner",
        "generic_daemon_owner",
        "generic_lifecycle_owner",
        "generic_queue_owner",
        "generic_attempt_ledger_owner",
        "generic_state_machine_runner_owner",
        "generic_workspace_source_intake_owner",
        "generic_memory_transport_owner",
        "generic_artifact_gallery_owner",
        "generic_operator_workbench_owner",
        "generic_observability_slo_owner",
    ]
    assert thinning["thin_surface_output_guard_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard"
    )
    assert thinning["standard_agent_scaffold_alignment_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/standard_agent_scaffold_alignment"
    )
    assert thinning["opl_family_conflict_blocker_projection_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/opl_family_conflict_blocker_projection"
    )
    assert thinning["opl_runtime_observability_consumption_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/opl_runtime_observability_consumption"
    )
    assert thinning["privatized_functional_module_audit_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/privatized_functional_module_audit"
    )
    assert thinning["external_evidence_request_pack_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/external_evidence_request_pack"
    )
    assert thinning["external_evidence_receipt_ledger"]["ledger_ref"] == (
        "contracts/external_evidence/mag-evidence-receipt-ledger.json"
    )
    assert thinning["external_evidence_receipt_ledger"]["grant_stage_controlled_attempt_closeout_ref"] == (
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/"
        "grant_stage_controlled_attempt_closeout"
    )
    assert thinning["functional_followthrough_gap_classification_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/"
        "functional_followthrough_gap_classification"
    )
    followthrough = thinning["functional_followthrough_gap_classification"]
    assert followthrough["state"] == "mag_handler_boundary_ready_external_evidence_gated"
    assert followthrough["standard_agent_source_shape_status"] == "landed"
    assert (
        followthrough["current_mag_source_role"]
        == "declarative_pack_domain_handler_refs_only_adapter_or_minimal_authority"
    )
    assert followthrough["mag_functional_structure_gap_count"] == 0
    assert followthrough["remaining_mag_functional_structure_gap_ids"] == []
    assert followthrough["remaining_mag_functional_structure_gaps"] == []
    assert followthrough["closed_classification_surface_ids"] == [
        "P1_adapter_thinning_and_pack_input",
        "P2_package_export_artifact_lifecycle_handoff",
        "P3_grant_strategy_memory_locator_writeback_handoff",
        "P4_skeleton_generated_surface_and_legacy_retirement",
    ]
    assert followthrough["reclassified_testing_evidence_gap_ids"] == [
        "real_workspace_memory_body_migration_and_retrieval_writeback_apply",
        "real_workspace_package_lifecycle_and_cleanup_restore_retention_receipts",
        "opl_generated_surface_production_consumption_no_regression",
        "focused_opl_hosted_receipt_verification",
        "continuous_live_receipt_reconciliation",
        "long_run_live_soak_and_no_forbidden_write_proof",
    ]
    assert followthrough["authority_boundary"]["mag_repo_functional_structure_gaps_zero"] is True
    assert followthrough["authority_boundary"]["mag_repo_active_source_shape_landed"] is True
    assert followthrough["authority_boundary"]["classification_closed"] is True
    assert followthrough["authority_boundary"]["followthrough_gaps_open"] is False
    assert followthrough["authority_boundary"]["claims_opl_descriptor_source_available"] is True
    assert followthrough["authority_boundary"]["claims_opl_replacement_exists"] is True
    assert followthrough["authority_boundary"]["claims_domain_repo_physical_delete_authorized"] is False
    assert followthrough["authority_boundary"]["claims_production_long_run_soak_complete"] is False
    assert thinning["consumed_opl_projection_surfaces"] == [
        "family_conflict_envelope",
        "stage_attempt_usage_projection",
        "stage_attempt_control_loop_projection",
        "runtime_observability_export",
        "family_product_operator_projection",
    ]
    audit = thinning["privatized_functional_module_audit"]
    assert audit["state"] == "manifest_projected_for_opl_unified_audit"
    assert audit["classification_buckets"] == [
        "declarative_pack_surface",
        "refs_only_adapter",
        "minimal_authority_function",
        "legacy_proof_tombstone",
    ]
    assert len(audit["declarative_pack_surfaces"]) == 3
    assert len(audit["refs_only_adapter_surfaces"]) == 5
    assert len(audit["mag_owned_grant_authority_surfaces"]) == 6
    assert len(audit["retire_or_tombstone_surfaces"]) == 6
    no_active_caller_summary = audit["no_active_caller_evidence_summary"]
    assert no_active_caller_summary["retired_surface_count"] == 6
    assert no_active_caller_summary["no_active_caller_observed_count"] == 6
    assert no_active_caller_summary["physical_delete_authorized"] is False
    assert audit["private_platform_retirement_owner_evidence"][
        "status"
    ] == "no_active_caller_evidence_observed_not_delete_authorized"
    assert audit["private_platform_retirement_owner_evidence"][
        "physical_delete_authorized"
    ] is False
    assert audit["domain_authority_do_not_retire"] == [
        "grant_lifecycle_stage",
        "package_readiness_submission_ready",
        "fundability_verdict",
        "authoring_quality_verdict",
        "submission_ready_export_verdict",
        "grant_transition_oracle",
        "owner_receipt",
        "grant_strategy_memory_accept_reject",
    ]
    assert "workspace_source_intake_shell" in audit["opl_must_absorb_code_surfaces"]
    assert "generic_scheduler_daemon" in audit["opl_must_absorb_code_surfaces"]
    assert audit["mag_thin_adapter_code_surfaces"] == [
        "product_entry_manifest_builder",
        "domain_handler_guarded_domain_adapter",
        "domain_entry",
        "receipt_schema_and_writer",
        "grant_transition_oracle",
        "refs_only_projection_builders",
        "focused_contract_tests",
    ]
    assert audit["representative_private_functional_surfaces"] == {
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
            "migration_action": "OPL_owns_generic_executor_adapter_MAG_keeps_only_compact_history_index_refs",
        },
    }
    assert audit["audit_refs"]["external_evidence_request_pack_ref"] == (
        "/product_entry_manifest/mag_consumer_thinning_contract/external_evidence_request_pack"
    )
    assert audit["audit_refs"]["grant_stage_controlled_attempt_closeout_ref"] == (
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/"
        "grant_stage_controlled_attempt_closeout"
    )
    evidence_pack = thinning["external_evidence_request_pack"]
    assert evidence_pack["surface_kind"] == "mag_external_evidence_request_pack"
    assert evidence_pack["state"] == "request_pack_declared_external_evidence_not_claimed"
    assert evidence_pack["required_request_ids"] == [
        "opl_generated_hosted_caller_pack_consumption",
        "app_workbench_package_ref_consumption",
        "production_default_caller_release_dist_consumption",
        "owner_receipt_typed_blocker_ref_roundtrip",
        "continuous_no_forbidden_write_guard",
        "direct_hosted_parity_no_regression",
        "temporal_provider_long_soak_receipt_reconciliation",
    ]
    assert evidence_pack["forbidden_completion_claims"]["claims_opl_replacement_exists"] is False
    assert (
        evidence_pack["forbidden_completion_claims"]["claims_production_long_run_soak_complete"]
        is False
    )
    assert evidence_pack["authority_boundary"]["mag_request_pack_only"] is True
    assert evidence_pack["authority_boundary"]["mag_implements_opl_runtime"] is False
    assert evidence_pack["authority_boundary"]["mag_implements_app_workbench"] is False
    assert evidence_pack["authority_boundary"]["mag_claims_external_evidence_exists"] is False
    assert thinning["domain_handler_output_policy"] == "grant_refs_and_receipts_only_no_generic_runtime_state"
    assert thinning["private_functional_state_output_classes_forbidden"] == [
        "local_runtime_journal_state",
        "local_attempt_record_state",
        "attention_queue_state",
        "stage_attempt_records_state",
        "package_lifecycle_state",
        "source_intake_state",
        "operator_workbench_state",
        "scheduler_daemon_state",
        "hermes_state_db_runtime_state",
    ]
    assert thinning["knowledge_only_repository"] is False
    assert thinning["retains_domain_program_surfaces"] is True
    assert thinning["authority_boundary"] == {
        "grant_truth_owner": "med-autogrant",
        "grant_memory_body_owner": "med-autogrant",
        "quality_verdict_owner": "med-autogrant",
        "export_authority_owner": "med-autogrant",
        "owner_receipt_authority": "med-autogrant",
        "safe_action_refs_owner": "med-autogrant",
        "opl_family_scheduler_replacement_owner": "one-person-lab",
        "mag_implements_generic_scheduler": False,
        "mag_implements_generic_daemon": False,
        "mag_implements_generic_lifecycle_owner": False,
        "mag_implements_generic_queue": False,
        "mag_implements_generic_attempt_ledger": False,
        "mag_implements_generic_runner": False,
        "mag_implements_app_workbench": False,
        "mag_implements_generic_workspace_source_intake": False,
        "mag_implements_generic_memory_transport": False,
        "mag_implements_generic_artifact_gallery": False,
        "mag_implements_generic_operator_workbench": False,
        "mag_implements_generic_observability_slo": False,
        "mag_can_emit_private_functional_state": False,
        "mag_can_emit_local_attempt_record_state": False,
        "mag_can_emit_source_intake_state": False,
        "mag_can_emit_package_lifecycle_state": False,
        "mag_can_emit_hermes_state_db_runtime_state": False,
        "provider_completion_is_grant_ready": False,
        "mag_executes_opl_repair": False,
    }
    assert thinning["claims_opl_replacement_exists"] is True
    assert thinning["claims_domain_repo_physical_delete_authorized"] is False
    assert thinning["claims_production_long_run_soak_complete"] is False
    assert thinning["mag_rebuilds_opl_runtime"] is False
