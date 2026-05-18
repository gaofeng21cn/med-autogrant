from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID
from med_autogrant.product_entry_parts.consumer_thinning_audit import (
    _build_privatized_functional_module_audit,
)
from med_autogrant.product_entry_parts.consumer_thinning_pack import (
    MAG_MINIMAL_AUTHORITY_FUNCTION_IDS,
    build_declarative_grant_pack_compiler_input,
    build_generated_surface_handoff,
    build_mag_minimal_authority_functions,
)

MAG_THIN_SURFACE_OUTPUT_CLASSES = (
    "grant_owned_refs",
    "owner_receipt",
    "typed_blocker",
    "verdict_refs",
    "domain_action_metadata",
)

FORBIDDEN_MAG_GENERIC_OWNER_ROLES = (
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
)

OPL_FUNCTIONAL_HARNESS_COVERAGE_CHAINS = (
    "memory_refs_only_writeback_chain",
    "queue_stage_attempt_typed_closeout_chain",
    "generic_transition_runner_chain",
    "restart_dead_letter_repair_human_gate_chain",
)

PRIVATE_FUNCTIONAL_STATE_OUTPUT_CLASSES = (
    "local_runtime_journal_state",
    "local_attempt_ledger_state",
    "attention_queue_state",
    "stage_attempt_ledger_state",
    "package_lifecycle_state",
    "source_intake_state",
    "operator_workbench_state",
    "scheduler_daemon_state",
    "hermes_state_db_runtime_state",
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
        "consumes_opl_family_primitive": "family_scheduler_replacement",
        "claims_opl_replacement_exists": False,
        "claims_production_long_run_soak_complete": False,
        "sidecar_contract_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
        "consumed_opl_standard_surfaces": _build_consumed_opl_standard_surfaces(),
        "opl_family_conflict_blocker_projection": _build_opl_family_conflict_blocker_projection(),
        "opl_runtime_observability_consumption": _build_opl_runtime_observability_consumption(),
        "functional_harness_consumer_coverage": _build_functional_harness_consumer_coverage(),
        "privatized_functional_module_audit": _build_privatized_functional_module_audit(),
        "declarative_grant_pack_compiler_input": build_declarative_grant_pack_compiler_input(),
        "generated_surface_handoff": build_generated_surface_handoff(),
        "minimal_authority_functions": build_mag_minimal_authority_functions(),
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
        "thin_surface_output_guard": _build_thin_surface_output_guard(),
        "standard_agent_scaffold_alignment": _build_standard_agent_scaffold_alignment(),
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
            "generated_surface_bridge_exit_gate_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff/bridge_exit_gate"
            ),
            "functional_followthrough_gap_classification_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "functional_followthrough_gap_classification"
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
        "opl_replacement_expectations": _build_opl_replacement_expectations(),
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


def _build_functional_followthrough_gap_classification() -> dict[str, Any]:
    return {
        "surface_kind": "mag_functional_followthrough_gap_classification",
        "classification_id": "mag.functional_followthrough_gap.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "state": "mag_handler_boundary_ready_external_evidence_gated",
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
            "classification_closed": True,
            "followthrough_gaps_open": False,
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
        "current_bucket": "classification_surface_closed_active_bridge_exit_closed",
        "owner": TARGET_DOMAIN_ID,
        "closed_by_refs": closed_by_refs,
    }


def _followthrough_gap(
    gap_id: str,
    *,
    owner: str,
    evidence_required: str,
    mag_role: str,
) -> dict[str, Any]:
    return {
        "gap_id": gap_id,
        "current_bucket": "functional_structure_followthrough_gap",
        "owner": owner,
        "evidence_required": evidence_required,
        "mag_role": mag_role,
        "production_soak_gate": False,
    }


def _external_owner_gate(
    gate_id: str,
    *,
    required_surface_owner: str,
    evidence_gate: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "previous_bucket": "functional_structure_gap",
        "current_bucket": "external_owner_gate",
        "required_surface_owner": required_surface_owner,
        "evidence_gate": evidence_gate,
        "mag_must_not_implement": True,
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
        "current_bucket": "testing_evidence_gap",
        "owner": "evidence_gate",
        "required_evidence": required_evidence,
        "mag_surface_refs": mag_surface_refs,
    }


def _build_opl_replacement_expectations() -> list[dict[str, Any]]:
    return [
        _build_opl_replacement_expectation(
            "workspace_source_intake_shell",
            mag_keeps=["funding_call_profile_task_lock_adapter", "domain_blocker", "owner_receipt"],
            opl_provides=["workspace_locator", "source_receipt", "freshness", "repair_command"],
        ),
        _build_opl_replacement_expectation(
            "memory_locator_writeback_transport",
            mag_keeps=["strategy_memory_policy", "writeback_proposal", "accept_reject", "receipt_writer"],
            opl_provides=["body_free_locator", "index", "freshness", "receipt_ref_projection"],
        ),
        _build_opl_replacement_expectation(
            "artifact_package_lifecycle_shell",
            mag_keeps=["package_refs", "gap_report", "submission_ready_verdict", "manual_portal_boundary"],
            opl_provides=["package_lifecycle_shell", "restore_provenance", "retention", "artifact_index"],
        ),
        _build_opl_replacement_expectation(
            "generic_transition_runner",
            mag_keeps=["grant_transition_oracle", "stage_guard", "typed_blocker", "owner_action_metadata"],
            opl_provides=["matrix_runner", "retry_dead_letter", "dispatch_receipt", "transition_audit"],
        ),
        _build_opl_replacement_expectation(
            "functional_harness_queue_stage_attempt_typed_closeout",
            mag_keeps=["grant_stage_truth", "owner_receipt", "typed_blocker", "no_regression_evidence"],
            opl_provides=["typed_queue", "stage_attempt_ledger", "attempt_dispatch", "typed_closeout_envelope"],
        ),
        _build_opl_replacement_expectation(
            "functional_harness_restart_dead_letter_repair_human_gate",
            mag_keeps=["grant_blocker_meaning", "owner_receipt", "manual_portal_boundary", "safe_action_refs"],
            opl_provides=["restart_token", "dead_letter_record", "repair_command_projection", "human_gate_state"],
        ),
        _build_opl_replacement_expectation(
            "operator_workbench_drilldown_shell",
            mag_keeps=["quality_verdict_refs", "hard_blockers", "safe_action_refs"],
            opl_provides=["workbench_panel", "attention_queue", "repair_command_projection"],
        ),
        _build_opl_replacement_expectation(
            "observability_repair_projection",
            mag_keeps=["owner_receipt_refs", "typed_blocker_refs", "verdict_refs", "safe_action_refs"],
            opl_provides=["runtime_observability_export", "slo_projection", "repair_projection"],
        ),
        _build_opl_replacement_expectation(
            "agent_scaffold_checklist",
            mag_keeps=["grant_domain_authority_pack", "receipt_schema_examples", "docs_taxonomy_example"],
            opl_provides=["new_agent_template", "owner_boundary_checklist", "no_forbidden_write_rule"],
        ),
    ]


def _build_consumed_opl_standard_surfaces() -> dict[str, Any]:
    return {
        "surface_kind": "mag_consumed_opl_standard_surfaces",
        "standard_scaffold_manifest_ref": "/product_entry_manifest/standard_domain_agent_skeleton",
        "generic_primitives_contract_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/opl_replacement_expectations"
        ),
        "sidecar_projection_ref": "/sidecar_export/mag_consumer_thinning_contract",
        "consumption_policy": (
            "consume_opl_standard_scaffold_and_generic_primitives_no_mag_runtime_rebuild"
        ),
        "consumed_generic_primitives": [
            "workspace_source_intake_shell",
            "memory_locator_writeback_transport",
            "artifact_package_lifecycle_shell",
            "generic_transition_runner",
            "functional_harness_queue_stage_attempt_typed_closeout",
            "functional_harness_restart_dead_letter_repair_human_gate",
            "operator_workbench_drilldown_shell",
            "observability_repair_projection",
            "agent_scaffold_checklist",
            "pack_compiler_generated_surface",
        ],
        "consumed_projection_surfaces": [
            "family_conflict_envelope",
            "stage_attempt_usage_projection",
            "stage_attempt_control_loop_projection",
            "runtime_observability_export",
            "family_product_operator_projection",
        ],
        "functional_harness_consumer_coverage_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/"
            "functional_harness_consumer_coverage"
        ),
        "mag_retained_authority": [
            "grant_truth",
            "fundability_verdict",
            "quality_verdict",
            "export_verdict",
            "memory_body_accept_reject",
            "package_authority",
            "owner_receipt",
            "grant_helper",
        ],
        "authority_boundary": {
            "opl_standard_scaffold_owner": "one-person-lab",
            "opl_generic_primitives_owner": "one-person-lab",
            "opl_pack_compiler_owner": "one-person-lab",
            "mag_consumes_standard_scaffold": True,
            "mag_consumes_generic_primitives": True,
            "mag_consumes_generated_surfaces": True,
            "mag_can_own_generic_scheduler": False,
            "mag_can_own_generic_daemon": False,
            "mag_can_own_generic_queue": False,
            "mag_can_own_generic_attempt_ledger": False,
            "mag_can_own_generic_runner": False,
            "mag_can_own_generic_workspace_source_intake": False,
            "mag_can_own_generic_memory_transport": False,
            "mag_can_own_generic_artifact_gallery": False,
            "mag_can_own_generic_operator_workbench": False,
            "mag_can_own_generic_observability_slo": False,
            "mag_can_own_generic_artifact_lifecycle": False,
            "mag_can_long_term_own_generated_wrappers": False,
            "opl_harness_pass_can_declare_grant_ready": False,
            "opl_harness_pass_can_declare_export_ready": False,
        },
    }


def _build_functional_harness_consumer_coverage() -> dict[str, Any]:
    return {
        "surface_kind": "mag_functional_harness_consumer_coverage",
        "version": "v1",
        "coverage_id": "mag.functional_harness.consumer_coverage.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "adapter_role": "domain_authority_pack_consumer_only",
        "state": "consumer_coverage_declared_external_opl_harness_gate",
        "harness_owner": "one-person-lab",
        "claims_opl_functional_harness_pass": False,
        "claims_grant_ready": False,
        "claims_export_ready": False,
        "coverage_chains": [
            _build_functional_harness_chain(
                "memory_refs_only_writeback_chain",
                opl_owned=[
                    "memory_ref_locator",
                    "writeback_proposal_transport",
                    "accepted_rejected_receipt_ref_projection",
                    "freshness_and_grouping",
                ],
                mag_retained=[
                    "grant_memory_body",
                    "writeback_body_accept_reject",
                    "memory_receipt_writer",
                ],
                mag_refs=[
                    "/product_entry_manifest/domain_memory_descriptor_locator",
                    "/product_entry_manifest/controlled_domain_memory_apply_proof",
                ],
            ),
            _build_functional_harness_chain(
                "queue_stage_attempt_typed_closeout_chain",
                opl_owned=[
                    "typed_queue",
                    "stage_attempt_ledger",
                    "attempt_dispatch",
                    "typed_closeout_envelope",
                ],
                mag_retained=[
                    "grant_stage_truth",
                    "owner_receipt",
                    "typed_blocker",
                    "no_regression_evidence",
                ],
                mag_refs=[
                    "/product_entry_manifest/controlled_stage_attempt_projection",
                    "/product_entry_manifest/owner_receipt_contract",
                ],
            ),
            _build_functional_harness_chain(
                "generic_transition_runner_chain",
                opl_owned=[
                    "generic_transition_runner",
                    "matrix_runner",
                    "dispatch_receipt",
                    "transition_execution_audit",
                ],
                mag_retained=[
                    "grant_transition_oracle",
                    "stage_guard",
                    "fundability_quality_export_verdict_refs",
                    "domain_action_metadata",
                ],
                mag_refs=[
                    "/product_entry_manifest/grant_transition_oracle",
                    "/product_entry_manifest/family_stage_control_plane",
                ],
            ),
            _build_functional_harness_chain(
                "restart_dead_letter_repair_human_gate_chain",
                opl_owned=[
                    "restart_token",
                    "dead_letter_record",
                    "repair_command_projection",
                    "human_gate_state",
                ],
                mag_retained=[
                    "grant_blocker_meaning",
                    "owner_receipt",
                    "manual_portal_boundary",
                    "safe_action_refs",
                ],
                mag_refs=[
                    "/product_entry_manifest/task_lifecycle",
                    "/product_entry_manifest/family_orchestration",
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                ],
            ),
        ],
        "coverage_chain_ids": list(OPL_FUNCTIONAL_HARNESS_COVERAGE_CHAINS),
        "mag_retained_authority": [
            "grant_truth",
            "fundability_verdict",
            "quality_verdict",
            "export_verdict",
            "grant_memory_body_accept_reject",
            "package_authority",
            "owner_receipt",
            "typed_blocker",
            "sidecar_projection_adapter",
        ],
        "fail_closed_rules": {
            "opl_harness_pass_is_grant_ready": False,
            "opl_harness_pass_is_export_ready": False,
            "opl_can_hold_generic_runtime_in_mag": False,
            "opl_can_write_memory_body": False,
            "opl_can_write_grant_truth": False,
        },
        "sidecar_projection_policy": "refs_receipts_blockers_verdict_refs_action_metadata_only",
        "output_guard_ref": "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard",
    }


def _build_functional_harness_chain(
    chain_id: str,
    *,
    opl_owned: list[str],
    mag_retained: list[str],
    mag_refs: list[str],
) -> dict[str, Any]:
    return {
        "chain_id": chain_id,
        "harness_owner": "one-person-lab",
        "mag_role": "consumer_domain_authority_pack",
        "implemented_in_mag": False,
        "mag_claims_generic_runtime_owner": False,
        "opl_owned": opl_owned,
        "mag_retained": mag_retained,
        "mag_surface_refs": mag_refs,
        "fail_closed_boundary": {
            "harness_pass_can_set_grant_ready": False,
            "harness_pass_can_set_export_ready": False,
            "opl_can_write_grant_truth": False,
            "opl_can_write_memory_body": False,
            "mag_owner_receipt_required": True,
        },
    }


def _build_opl_family_conflict_blocker_projection() -> dict[str, Any]:
    return {
        "surface_kind": "mag_opl_family_conflict_blocker_projection",
        "envelope_kind": "opl_conflict_or_blocker.v1",
        "schema_ref": "contracts/family-orchestration/family-conflict-envelope.schema.json",
        "projection_policy": "typed_blocker_only_no_fallback_completion",
        "allowed_classifications": [
            "authority_conflict",
            "evidence_blocker",
            "quality_blocker",
            "human_gate",
            "receipt_conflict",
        ],
        "mag_owned_inputs": [
            "owner_receipt",
            "typed_blocker",
            "no_regression_evidence",
            "verdict_refs",
        ],
        "forbidden_claims": [
            "provider_completion_is_domain_ready",
            "fallback_complete",
            "opl_can_write_domain_truth",
            "opl_can_declare_fundability_ready",
            "opl_can_declare_export_ready",
        ],
        "authority_boundary": {
            "opl": "route_project_audit_only",
            "domain": "truth_quality_artifact_gate_owner",
            "provider_completion_is_domain_ready": False,
            "can_write_domain_truth": False,
            "can_fallback_complete": False,
        },
    }


def _build_opl_runtime_observability_consumption() -> dict[str, Any]:
    return {
        "surface_kind": "mag_opl_runtime_observability_consumption",
        "observability_export_kind": "opl_runtime_observability_export",
        "consumption_policy": "read_only_refs_and_counts_no_repair_execution",
        "consumed_opl_surfaces": [
            "runtime_tray_snapshot",
            "stage_attempt_workbench",
            "stage_attempt_usage_projection",
            "stage_attempt_control_loop_projection",
            "runtime_observability_export",
        ],
        "mag_provides_refs": [
            "owner_receipt_refs",
            "typed_blocker_refs",
            "artifact_locator_refs",
            "memory_receipt_refs",
            "grant_transition_oracle_ref",
            "safe_action_refs",
        ],
        "stage_attempt_projection_consumption": {
            "surface_kind": "mag_stage_attempt_projection_consumption",
            "consumption_policy": "OPL_may_count_and_display_MAG_refs_only",
            "mag_can_schedule_retry_dead_letter": False,
            "mag_can_write_opl_stage_attempt_ledger": False,
            "provider_completion_is_grant_ready": False,
        },
        "authority_boundary": {
            "can_execute_repair": False,
            "can_write_domain_truth": False,
            "can_authorize_quality_verdict": False,
            "can_authorize_ready_verdict": False,
            "can_authorize_artifact_export": False,
        },
    }


def _build_thin_surface_output_guard() -> dict[str, Any]:
    return {
        "surface_kind": "mag_thin_surface_output_guard",
        "guard_id": "mag.thin_surface.output_guard.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "output_policy": "grant_refs_and_receipts_only_no_generic_runtime_state",
        "allowed_output_classes": list(MAG_THIN_SURFACE_OUTPUT_CLASSES),
        "private_functional_state_output_classes_forbidden": list(
            PRIVATE_FUNCTIONAL_STATE_OUTPUT_CLASSES
        ),
        "required_sidecar_return_refs": {
            "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
            "controlled_stage_attempt_projection_ref": "/product_entry_manifest/controlled_stage_attempt_projection",
            "controlled_domain_memory_apply_proof_ref": "/product_entry_manifest/controlled_domain_memory_apply_proof",
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
            "generated_surface_bridge_exit_gate_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff/bridge_exit_gate"
            ),
            "functional_followthrough_gap_classification_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "functional_followthrough_gap_classification"
            ),
        },
        "forbidden_output_classes": [
            "generic_scheduler_state",
            "generic_daemon_state",
            "generic_lifecycle_ledger",
            "generic_queue_record",
            "generic_attempt_ledger_record",
            "generic_runner_decision",
            "generic_workbench_state",
            "generic_workspace_source_intake_state",
            "generic_memory_transport_state",
            "generic_artifact_lifecycle_state",
            "generic_artifact_gallery_state",
            "generic_operator_workbench_state",
            "generic_observability_slo_state",
            *PRIVATE_FUNCTIONAL_STATE_OUTPUT_CLASSES,
            "family_conflict_envelope_completion_claim",
            "functional_harness_runtime_state",
            "opl_harness_pass_grant_ready",
            "opl_harness_pass_export_ready",
            "observability_export_execution_result",
            "grant_artifact_content",
            "memory_body",
            "generated_product_status_owner_state",
            "generated_user_loop_owner_state",
            "generated_sidecar_owner_state",
            "generated_grouped_cli_api_owner_state",
            "generated_projection_owner_state",
            "generated_lifecycle_wrapper_owner_state",
        ],
        "consumes_opl_replacement_expectations": True,
        "replacement_expectations_ref": "/product_entry_manifest/mag_consumer_thinning_contract/opl_replacement_expectations",
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "owner_receipt_authority": TARGET_DOMAIN_ID,
            "opl_role": "replacement_owner_and_ref_consumer_only",
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_export_ready": False,
            "mag_can_emit_generic_runtime_state": False,
            "mag_can_emit_generic_workbench_state": False,
            "mag_can_emit_generic_observability_state": False,
            "mag_can_emit_private_functional_state": False,
            "mag_can_emit_local_attempt_ledger_state": False,
            "mag_can_emit_source_intake_state": False,
            "mag_can_emit_package_lifecycle_state": False,
            "mag_can_emit_hermes_state_db_runtime_state": False,
            "mag_can_emit_family_conflict_completion_claim": False,
            "mag_can_emit_functional_harness_runtime_state": False,
            "mag_can_emit_generated_wrapper_owner_state": False,
            "opl_harness_pass_can_declare_grant_ready": False,
            "opl_harness_pass_can_declare_export_ready": False,
        },
    }


def _build_standard_agent_scaffold_alignment() -> dict[str, Any]:
    return {
        "surface_kind": "mag_standard_agent_scaffold_thin_surface_guard",
        "guard_id": "mag.standard_agent_scaffold.thin_surface_guard.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "scaffold_ref": "/product_entry_manifest/standard_domain_agent_skeleton",
        "physical_follow_through_ref": "/product_entry_manifest/physical_skeleton_follow_through",
        "output_guard_ref": "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard",
        "forbidden_owner_roles_ref": "/product_entry_manifest/mag_consumer_thinning_contract/forbidden_mag_generic_owner_roles",
        "knowledge_only_repository": False,
        "retains_domain_program_surfaces": True,
        "required_repo_boundaries": ["agent", "contracts", "runtime", "docs"],
        "retained_program_surface_refs": [
            "src/med_autogrant/domain_entry.py",
            "src/med_autogrant/product_entry.py",
            "src/med_autogrant/product_entry_parts/sidecar.py",
            "schemas/v1/product-entry-manifest.schema.json",
            "tests/product_entry_cases/test_sidecar.py",
            "tests/product_entry_cases/test_functional_closure.py",
        ],
        "retained_program_surface_kinds": [
            "domain_entry",
            "product_entry_manifest_builder",
            "product_sidecar_adapter",
            "schema_contract",
            "focused_product_entry_tests",
            "declarative_grant_pack_compiler_input",
            "minimal_authority_functions",
        ],
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "domain_entry_owner": TARGET_DOMAIN_ID,
            "sidecar_owner": TARGET_DOMAIN_ID,
            "schema_owner": TARGET_DOMAIN_ID,
            "test_owner": TARGET_DOMAIN_ID,
            "opl_scaffold_owner": "one-person-lab",
            "mag_owns_generic_scaffold_template": False,
            "mag_owns_generic_runtime_framework": False,
            "mag_is_knowledge_only_repository": False,
            "mag_owns_generated_product_surface_template": False,
        },
    }


def _build_opl_replacement_expectation(
    primitive_id: str,
    *,
    mag_keeps: list[str],
    opl_provides: list[str],
) -> dict[str, Any]:
    return {
        "primitive_id": primitive_id,
        "owner": "one-person-lab",
        "state": "external_replacement_contract_expected",
        "mag_handoff_policy": "contract_expectation_only",
        "implemented_in_mag": False,
        "mag_keeps": mag_keeps,
        "opl_provides": opl_provides,
        "authority_boundary": {
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_export_ready": False,
            "opl_can_replace_mag_authority_function": False,
        },
    }
