from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID
from med_autogrant.product_entry_parts.consumer_thinning_audit import (
    _build_privatized_functional_module_audit,
)
from med_autogrant.product_entry_parts.consumer_thinning_pack import (
    MAG_MINIMAL_AUTHORITY_FUNCTION_IDS,
    build_declarative_grant_pack_compiler_input,
    build_external_evidence_request_pack,
    build_generated_hosted_default_caller_proof,
    build_generated_surface_handoff,
    build_mag_minimal_authority_functions,
    build_mag_minimal_authority_surface_taxonomy,
)
from med_autogrant.product_entry_parts.consumer_thinning_shell import (
    FORBIDDEN_MAG_GENERIC_OWNER_ROLES,
    MAG_THIN_SURFACE_OUTPUT_CLASSES,
    build_consumed_opl_standard_surfaces,
    build_functional_harness_consumer_coverage,
    build_opl_family_conflict_blocker_projection,
    build_opl_replacement_expectations,
    build_opl_runtime_observability_consumption,
    build_standard_agent_scaffold_alignment,
    build_thin_surface_output_guard,
)

MAG_FUNCTIONAL_STRUCTURE_GAP_IDS = (
    "P1_adapter_thinning_and_pack_input",
    "P2_package_export_artifact_lifecycle_handoff",
    "P3_grant_strategy_memory_locator_writeback_handoff",
    "P4_skeleton_generated_surface_and_legacy_retirement",
)

MAG_RECLASSIFIED_EVIDENCE_GAP_IDS = (
    "real_workspace_memory_body_migration_and_retrieval_writeback_apply",
    "real_workspace_package_lifecycle_and_cleanup_restore_retention_receipts",
    "opl_generated_surface_production_consumption_no_regression",
    "focused_opl_hosted_receipt_verification",
    "continuous_live_receipt_reconciliation",
    "long_run_live_soak_and_no_forbidden_write_proof",
)


def build_mag_consumer_thinning_contract(
    *,
    physical_skeleton_follow_through: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    active_path_scan = {}
    if physical_skeleton_follow_through is not None:
        candidate = physical_skeleton_follow_through.get("active_path_scan_no_legacy_default_caller")
        if isinstance(candidate, Mapping):
            active_path_scan = dict(candidate)
    return {
        "surface_kind": "mag_consumer_thinning_contract",
        "version": "v1",
        "contract_id": "mag.consumer_thinning.contract.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "adapter_role": "domain_authority_pack_with_thin_program_surface",
        "active_caller_owner": "med-autogrant",
        "active_caller_surface": "mag_direct_domain_entry_until_opl_caller_evidence",
        "domain_handler_target": TARGET_DOMAIN_ID,
        "domain_handler_owner": TARGET_DOMAIN_ID,
        "state": "mag_handler_boundary_ready_external_caller_evidence_gated",
        "standard_agent_source_shape_status": "landed",
        "mag_repo_active_source_shape_landed": True,
        "current_mag_source_role": (
            "declarative_pack_domain_handler_refs_only_adapter_or_minimal_authority"
        ),
        "consumes_opl_family_primitive": "family_scheduler_replacement",
        "claims_opl_descriptor_source_available": True,
        "claims_opl_replacement_exists": False,
        "claims_production_long_run_soak_complete": False,
        "sidecar_contract_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
        "consumed_opl_standard_surfaces": build_consumed_opl_standard_surfaces(),
        "opl_family_conflict_blocker_projection": build_opl_family_conflict_blocker_projection(),
        "opl_runtime_observability_consumption": build_opl_runtime_observability_consumption(),
        "functional_harness_consumer_coverage": build_functional_harness_consumer_coverage(),
        "privatized_functional_module_audit": _build_privatized_functional_module_audit(),
        "declarative_grant_pack_compiler_input": build_declarative_grant_pack_compiler_input(),
        "generated_surface_handoff": build_generated_surface_handoff(),
        "generated_hosted_default_caller_proof": build_generated_hosted_default_caller_proof(),
        "external_evidence_request_pack": build_external_evidence_request_pack(),
        "route_stage_handoff_boundary": _build_route_stage_handoff_boundary(),
        "minimal_authority_functions": build_mag_minimal_authority_functions(),
        "minimal_authority_surface_taxonomy": build_mag_minimal_authority_surface_taxonomy(),
        "minimal_authority_function_ids": list(MAG_MINIMAL_AUTHORITY_FUNCTION_IDS),
        "functional_followthrough_gap_classification": (
            _build_functional_followthrough_gap_classification()
        ),
        "bridge_exit_gate_refs": {
            "generated_surface_bridge_exit_gate_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff/bridge_exit_gate"
            ),
            "privatized_functional_module_audit_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "privatized_functional_module_audit"
            ),
            "legacy_exit_gate_policy": "delete_or_history_tombstone_after_replacement_proof",
            "claims_all_bridge_exits_complete": False,
            "mag_handler_boundary_ready": True,
            "external_opl_generated_or_hosted_caller_evidence_required": True,
        },
        "allowed_return_shapes": [
            "domain_owner_receipt",
            "typed_blocker",
            "no_regression_evidence",
        ],
        "mag_owned_outputs": list(MAG_THIN_SURFACE_OUTPUT_CLASSES),
        "thin_surface_output_guard": build_thin_surface_output_guard(),
        "standard_agent_scaffold_alignment": build_standard_agent_scaffold_alignment(),
        "exposed_sidecar_return_refs": {
            "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
            "controlled_stage_attempt_projection_ref": (
                "/product_entry_manifest/controlled_stage_attempt_projection"
            ),
            "controlled_domain_memory_apply_proof_ref": (
                "/product_entry_manifest/controlled_domain_memory_apply_proof"
            ),
            "lifecycle_guarded_apply_proof_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
            "grant_transition_oracle_ref": "/product_entry_manifest/grant_transition_oracle",
            "functional_harness_consumer_coverage_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "functional_harness_consumer_coverage"
            ),
            "privatized_functional_module_audit_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "privatized_functional_module_audit"
            ),
            "declarative_grant_pack_compiler_input_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "declarative_grant_pack_compiler_input"
            ),
            "generated_surface_handoff_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff"
            ),
            "generated_hosted_default_caller_proof_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_hosted_default_caller_proof"
            ),
            "generated_surface_bridge_exit_gate_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff/bridge_exit_gate"
            ),
            "functional_followthrough_gap_classification_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "functional_followthrough_gap_classification"
            ),
            "external_evidence_request_pack_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "external_evidence_request_pack"
            ),
            "route_stage_handoff_boundary_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "route_stage_handoff_boundary"
            ),
        },
        "verdict_authority_refs": {
            "fundability_verdict_owner": TARGET_DOMAIN_ID,
            "quality_verdict_owner": TARGET_DOMAIN_ID,
            "export_verdict_owner": TARGET_DOMAIN_ID,
            "submission_ready_gate_ref": "package submission-ready",
        },
        "domain_action_metadata_refs": [
            "/product_entry_manifest/family_action_catalog",
            "/product_entry_manifest/family_stage_control_plane",
            "/product_entry_manifest/grant_transition_oracle",
        ],
        "opl_replacement_expectations": build_opl_replacement_expectations(),
        "forbidden_mag_owned_generic_primitives": [],
        "forbidden_mag_generic_owner_roles": list(FORBIDDEN_MAG_GENERIC_OWNER_ROLES),
        "guarded_by_active_path_scan_ref": (
            "/product_entry_manifest/physical_skeleton_follow_through/"
            "active_path_scan_no_legacy_default_caller"
        ),
        "active_path_scan_state": active_path_scan.get("state", "not_available"),
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "memory_body_owner": TARGET_DOMAIN_ID,
            "grant_truth_owner": TARGET_DOMAIN_ID,
            "grant_memory_body_owner": TARGET_DOMAIN_ID,
            "quality_verdict_owner": TARGET_DOMAIN_ID,
            "export_authority_owner": TARGET_DOMAIN_ID,
            "safe_action_refs_owner": TARGET_DOMAIN_ID,
            "package_authority_owner": TARGET_DOMAIN_ID,
            "owner_receipt_authority": TARGET_DOMAIN_ID,
            "opl_family_scheduler_replacement_owner": "one-person-lab",
            "generic_wrapper_active_caller_owner": "evidence_required_from_one-person-lab",
            "mag_role_for_generated_wrappers": "domain_handler_ref_only_adapter_and_minimal_authority_functions",
            "opl_role": "replacement_owner_and_ref_consumer_only",
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_export_ready": False,
            "opl_can_mutate_grant_artifacts": False,
            "mag_rebuilds_opl_runtime": False,
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
            "mag_implements_generic_artifact_lifecycle": False,
            "mag_long_term_owns_generated_product_status": False,
            "mag_long_term_owns_generated_user_loop": False,
            "mag_long_term_owns_generated_sidecar": False,
            "mag_long_term_owns_generated_grouped_cli_api": False,
            "mag_long_term_owns_generated_projection": False,
            "mag_long_term_owns_generated_lifecycle_wrapper": False,
            "opl_harness_pass_can_declare_grant_ready": False,
            "opl_harness_pass_can_declare_export_ready": False,
        },
}


def _build_route_stage_handoff_boundary() -> dict[str, Any]:
    return {
        "surface_kind": "mag_route_stage_handoff_boundary",
        "version": "mag-route-stage-handoff-boundary.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "route_is_stage": False,
        "route_semantics_owner": TARGET_DOMAIN_ID,
        "domain_truth_owner": TARGET_DOMAIN_ID,
        "stage_graph_owner": "one-person-lab",
        "stage_lifecycle_owner": "one-person-lab",
        "runtime_transition_owner": "one-person-lab",
        "queue_attempt_owner": "one-person-lab",
        "opl_hydrates_route_refs_to_queue_and_stage_attempts": True,
        "mag_owns_inter_route_scheduler": False,
        "stage_graph_ref": "/product_entry_manifest/family_stage_control_plane",
        "route_oracle_ref": "/product_entry_manifest/grant_transition_oracle",
        "route_projection_surface": "stage-route-report",
        "route_semantics": (
            "MAG routes express grant-domain next-owner or route-back recommendations; "
            "OPL transports them as refs into stage attempts."
        ),
        "allowed_handoff_refs": [
            "grant_run_id",
            "route_id",
            "current_stage_ref",
            "recommended_stage_ref",
            "grant_transition_oracle_ref",
            "owner_receipt_ref",
            "typed_blocker_refs",
            "human_gate_schema_ref",
            "no_forbidden_write_ref",
        ],
        "forbidden_payload_classes": [
            "grant_truth_body",
            "grant_artifact_body",
            "memory_body",
            "fundability_verdict_body",
            "quality_verdict_body",
            "export_verdict_body",
            "generic_runtime_state",
            "generic_attempt_ledger_record",
            "generic_runner_decision",
        ],
        "authority_boundary": {
            "mag_owner_receipt_required": True,
            "opl_can_write_grant_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_fundability_verdict": False,
            "opl_can_declare_quality_verdict": False,
            "opl_can_declare_export_verdict": False,
            "opl_can_mutate_grant_artifacts": False,
            "mag_implements_generic_route_scheduler": False,
            "mag_implements_generic_stage_attempt_graph": False,
        },
        "forbidden_claims": [
            "route_is_stage",
            "mag_owned_generic_route_scheduler",
            "mag_owned_generic_stage_attempt_graph",
            "opl_provider_completion_is_grant_ready",
            "opl_stage_attempt_completion_is_export_ready",
        ],
    }


def _build_functional_followthrough_gap_classification() -> dict[str, Any]:
    return {
        "surface_kind": "mag_functional_followthrough_gap_classification",
        "classification_id": "mag.functional_followthrough_gap.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "state": "mag_handler_boundary_ready_external_evidence_gated",
        "standard_agent_source_shape_status": "landed",
        "current_mag_source_role": (
            "declarative_pack_domain_handler_refs_only_adapter_or_minimal_authority"
        ),
        "plan_ref": "docs/active/mag-ideal-state-cross-repo-gap-plan.md",
        "classification_gap_count": 0,
        "mag_functional_structure_gap_count": 0,
        "remaining_mag_functional_structure_gap_ids": [],
        "remaining_mag_functional_structure_gaps": [],
        "closed_classification_surface_ids": list(MAG_FUNCTIONAL_STRUCTURE_GAP_IDS),
        "closed_classification_surfaces": [
            _closed_mag_functional_gap(
                "P1_adapter_thinning_and_pack_input",
                closed_by_refs=[
                    "/product_entry_manifest/mag_consumer_thinning_contract",
                    "/product_entry_manifest/mag_consumer_thinning_contract/"
                    "declarative_grant_pack_compiler_input",
                    "/product_entry_manifest/mag_consumer_thinning_contract/"
                    "generated_surface_handoff",
                    "/product_entry_manifest/mag_consumer_thinning_contract/"
                    "minimal_authority_functions",
                ],
            ),
            _closed_mag_functional_gap(
                "P2_package_export_artifact_lifecycle_handoff",
                closed_by_refs=[
                    "/product_entry_manifest/mag_consumer_thinning_contract/"
                    "opl_replacement_expectations",
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                    "product package-lifecycle-handoff",
                    "product lifecycle-receipt-bundle",
                ],
            ),
            _closed_mag_functional_gap(
                "P3_grant_strategy_memory_locator_writeback_handoff",
                closed_by_refs=[
                    "/product_entry_manifest/domain_memory_descriptor_locator",
                    "/product_entry_manifest/controlled_domain_memory_apply_proof",
                    "product memory-receipt-projection",
                ],
            ),
            _closed_mag_functional_gap(
                "P4_skeleton_generated_surface_and_legacy_retirement",
                closed_by_refs=[
                    "/product_entry_manifest/standard_domain_agent_skeleton",
                    "/product_entry_manifest/physical_skeleton_follow_through/"
                    "active_path_scan_no_legacy_default_caller",
                    "/product_entry_manifest/mag_consumer_thinning_contract/"
                    "generated_surface_handoff",
                    "/product_entry_manifest/mag_consumer_thinning_contract/"
                    "privatized_functional_module_audit",
                ],
            ),
        ],
        "external_owner_gates": [],
        "reclassified_as_testing_evidence_gaps": [
            _testing_evidence_gap(
                "real_workspace_memory_body_migration_and_retrieval_writeback_apply",
                required_evidence=(
                    "accepted and rejected real workspace memory receipts plus body-free "
                    "retrieval/writeback projection"
                ),
                mag_surface_refs=[
                    "/product_entry_manifest/domain_memory_descriptor_locator",
                    "product memory-receipt-projection",
                ],
            ),
            _testing_evidence_gap(
                "real_workspace_package_lifecycle_and_cleanup_restore_retention_receipts",
                required_evidence=(
                    "real workspace package handoff plus cleanup, restore, and retention "
                    "receipt bundle"
                ),
                mag_surface_refs=[
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                    "product package-lifecycle-handoff",
                    "product lifecycle-receipt-bundle",
                ],
            ),
            _testing_evidence_gap(
                "opl_generated_surface_production_consumption_no_regression",
                required_evidence=(
                    "external OPL generated/replacement caller consumes MAG pack input "
                    "without regressing direct MAG surfaces"
                ),
                mag_surface_refs=[
                    "/product_entry_manifest/mag_consumer_thinning_contract/"
                    "declarative_grant_pack_compiler_input",
                    "/product_entry_manifest/mag_consumer_thinning_contract/"
                    "generated_surface_handoff",
                ],
            ),
            _testing_evidence_gap(
                "focused_opl_hosted_receipt_verification",
                required_evidence=(
                    "OPL-hosted attempt evidence reconciles with MAG owner receipt, "
                    "typed blocker, or no-regression refs"
                ),
                mag_surface_refs=[
                    "product hosted-receipt-verification",
                    "/product_entry_manifest/owner_receipt_contract",
                ],
            ),
            _testing_evidence_gap(
                "continuous_live_receipt_reconciliation",
                required_evidence=(
                    "continuous reconciliation snapshot observes repeated receipt refs "
                    "without creating a second truth source"
                ),
                mag_surface_refs=[
                    "product continuous-receipt-reconciliation",
                    "product controlled-soak-receipt-reconciliation-inventory",
                ],
            ),
            _testing_evidence_gap(
                "long_run_live_soak_and_no_forbidden_write_proof",
                required_evidence=(
                    "long-run live soak includes OPL provider receipt, MAG owner receipt "
                    "or typed blocker, and no-forbidden-write proof"
                ),
                mag_surface_refs=[
                    "/product_entry_manifest/controlled_stage_attempt_projection",
                    "/product_entry_manifest/physical_skeleton_follow_through/"
                    "active_path_scan_no_legacy_default_caller",
                ],
            ),
        ],
        "reclassified_testing_evidence_gap_ids": list(MAG_RECLASSIFIED_EVIDENCE_GAP_IDS),
        "authority_boundary": {
            "mag_repo_functional_structure_gaps_zero": True,
            "mag_repo_active_source_shape_landed": True,
            "classification_closed": True,
            "followthrough_gaps_open": False,
            "claims_opl_descriptor_source_available": True,
            "claims_opl_replacement_exists": False,
            "claims_opl_generated_surface_production_consumed": False,
            "claims_real_workspace_memory_migration_complete": False,
            "claims_real_workspace_package_lifecycle_complete": False,
            "claims_focused_hosted_receipt_verification_complete": False,
            "claims_continuous_live_receipt_reconciliation_complete": False,
            "claims_production_long_run_soak_complete": False,
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_export_ready": False,
        },
    }


def _closed_mag_functional_gap(gap_id: str, *, closed_by_refs: list[str]) -> dict[str, Any]:
    return {
        "gap_id": gap_id,
        "previous_bucket": "functional_structure_gap",
        "current_bucket": "standard_agent_source_shape_landed",
        "owner": TARGET_DOMAIN_ID,
        "closed_by_refs": closed_by_refs,
    }


def _testing_evidence_gap(
    gap_id: str,
    *,
    required_evidence: str,
    mag_surface_refs: list[str],
) -> dict[str, Any]:
    return {
        "gap_id": gap_id,
        "previous_bucket": "functional_structure_gap",
        "current_bucket": "production_evidence_tail",
        "owner": "evidence_gate",
        "required_evidence": required_evidence,
        "mag_surface_refs": mag_surface_refs,
    }
