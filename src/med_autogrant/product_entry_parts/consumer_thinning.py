from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID

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
        "state": "handoff_ready_external_opl_replacement_gated",
        "consumes_opl_family_primitive": "family_scheduler_replacement",
        "claims_opl_replacement_exists": False,
        "claims_production_long_run_soak_complete": False,
        "sidecar_contract_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
        "consumed_opl_standard_surfaces": _build_consumed_opl_standard_surfaces(),
        "opl_family_conflict_blocker_projection": _build_opl_family_conflict_blocker_projection(),
        "opl_runtime_observability_consumption": _build_opl_runtime_observability_consumption(),
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
        },
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
            "operator_workbench_drilldown_shell",
            "observability_repair_projection",
            "agent_scaffold_checklist",
        ],
        "consumed_projection_surfaces": [
            "family_conflict_envelope",
            "stage_attempt_usage_projection",
            "stage_attempt_control_loop_projection",
            "runtime_observability_export",
            "family_product_operator_projection",
        ],
        "mag_retained_authority": [
            "grant_truth",
            "fundability_verdict",
            "quality_verdict",
            "export_verdict",
            "memory_body_accept_reject",
            "package_authority",
            "owner_receipt",
        ],
        "authority_boundary": {
            "opl_standard_scaffold_owner": "one-person-lab",
            "opl_generic_primitives_owner": "one-person-lab",
            "mag_consumes_standard_scaffold": True,
            "mag_consumes_generic_primitives": True,
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
        "required_sidecar_return_refs": {
            "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
            "controlled_stage_attempt_projection_ref": "/product_entry_manifest/controlled_stage_attempt_projection",
            "controlled_domain_memory_apply_proof_ref": "/product_entry_manifest/controlled_domain_memory_apply_proof",
            "lifecycle_guarded_apply_proof_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
            "grant_transition_oracle_ref": "/product_entry_manifest/grant_transition_oracle",
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
            "family_conflict_envelope_completion_claim",
            "observability_export_execution_result",
            "grant_artifact_content",
            "memory_body",
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
            "mag_can_emit_family_conflict_completion_claim": False,
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
        },
    }
