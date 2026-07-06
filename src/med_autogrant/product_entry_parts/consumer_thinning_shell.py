from __future__ import annotations

from typing import Any

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

OPL_FUNCTIONAL_HARNESS_COVERAGE_CHAINS = (
    "memory_refs_only_writeback_chain",
    "queue_stage_attempt_typed_closeout_chain",
    "generic_transition_runner_chain",
    "restart_dead_letter_repair_human_gate_chain",
)

OPL_REPLACEMENT_PRIMITIVE_IDS = (
    "workspace_source_intake_shell",
    "memory_locator_writeback_transport",
    "artifact_package_lifecycle_shell",
    "generic_transition_runner",
    "functional_harness_queue_stage_attempt_typed_closeout",
    "functional_harness_restart_dead_letter_repair_human_gate",
    "operator_workbench_drilldown_shell",
    "observability_repair_projection",
    "agent_scaffold_checklist",
)

OPL_CONSUMED_GENERIC_PRIMITIVES = (
    *OPL_REPLACEMENT_PRIMITIVE_IDS,
    "pack_compiler_generated_surface",
)

OPL_CONSUMED_PROJECTION_SURFACES = (
    "family_conflict_envelope",
    "stage_attempt_usage_projection",
    "stage_attempt_control_loop_projection",
    "runtime_observability_export",
    "family_product_operator_projection",
)

MAG_CONSUMED_RETAINED_AUTHORITY = (
    "grant_truth",
    "fundability_verdict",
    "quality_verdict",
    "export_verdict",
    "memory_body_accept_reject",
    "package_authority",
    "owner_receipt",
    "grant_helper",
)

MAG_FUNCTIONAL_HARNESS_RETAINED_AUTHORITY = (
    "grant_truth",
    "fundability_verdict",
    "quality_verdict",
    "export_verdict",
    "grant_memory_body_accept_reject",
    "package_authority",
    "owner_receipt",
    "typed_blocker",
    "domain_handler_projection_adapter",
)

PRIVATE_FUNCTIONAL_STATE_OUTPUT_CLASSES = (
    "local_runtime_journal_state",
    "local_attempt_record_state",
    "attention_queue_state",
    "stage_attempt_records_state",
    "package_lifecycle_state",
    "source_intake_state",
    "operator_workbench_state",
    "scheduler_daemon_state",
    "hermes_state_db_runtime_state",
)


def build_opl_replacement_expectations() -> list[dict[str, Any]]:
    replacement_rows = [
        (
            OPL_REPLACEMENT_PRIMITIVE_IDS[0],
            ["funding_call_profile_task_lock_adapter", "domain_blocker", "owner_receipt"],
            ["workspace_locator", "source_receipt", "freshness", "repair_command"],
        ),
        (
            OPL_REPLACEMENT_PRIMITIVE_IDS[1],
            ["strategy_memory_policy", "writeback_proposal", "accept_reject", "receipt_writer"],
            ["body_free_locator", "index", "freshness", "receipt_ref_projection"],
        ),
        (
            OPL_REPLACEMENT_PRIMITIVE_IDS[2],
            ["package_refs", "gap_report", "submission_ready_verdict", "manual_portal_boundary"],
            ["package_lifecycle_shell", "restore_provenance", "retention", "artifact_index"],
        ),
        (
            OPL_REPLACEMENT_PRIMITIVE_IDS[3],
            ["grant_transition_oracle", "stage_guard", "typed_blocker", "owner_action_metadata"],
            ["matrix_runner", "retry_dead_letter", "dispatch_receipt", "transition_audit"],
        ),
        (
            OPL_REPLACEMENT_PRIMITIVE_IDS[4],
            ["grant_stage_truth", "owner_receipt", "typed_blocker", "no_regression_evidence"],
            ["typed_queue", "stage_attempt_records", "attempt_dispatch", "typed_closeout_envelope"],
        ),
        (
            OPL_REPLACEMENT_PRIMITIVE_IDS[5],
            ["grant_blocker_meaning", "owner_receipt", "manual_portal_boundary", "safe_action_refs"],
            ["restart_token", "dead_letter_record", "repair_command_projection", "human_gate_state"],
        ),
        (
            OPL_REPLACEMENT_PRIMITIVE_IDS[6],
            ["quality_verdict_refs", "hard_blockers", "safe_action_refs"],
            ["workbench_panel", "attention_queue", "repair_command_projection"],
        ),
        (
            OPL_REPLACEMENT_PRIMITIVE_IDS[7],
            ["owner_receipt_refs", "typed_blocker_refs", "verdict_refs", "safe_action_refs"],
            ["runtime_observability_export", "slo_projection", "repair_projection"],
        ),
        (
            OPL_REPLACEMENT_PRIMITIVE_IDS[8],
            ["grant_domain_authority_pack", "receipt_schema_examples", "docs_taxonomy_example"],
            ["new_agent_template", "owner_boundary_checklist", "no_forbidden_write_rule"],
        ),
    ]
    return [
        _build_opl_replacement_expectation(
            primitive_id,
            mag_keeps=mag_keeps,
            opl_provides=opl_provides,
        )
        for primitive_id, mag_keeps, opl_provides in replacement_rows
    ]


def build_consumed_opl_standard_surfaces() -> dict[str, Any]:
    return {
        "surface_kind": "mag_consumed_opl_standard_surfaces",
        "standard_scaffold_manifest_ref": "/product_entry_manifest/standard_domain_agent_skeleton",
        "generic_primitives_contract_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/opl_replacement_expectations"
        ),
        "domain_handler_projection_ref": "/domain_handler_export/mag_consumer_thinning_contract",
        "consumption_policy": (
            "consume_opl_standard_scaffold_and_generic_primitives_no_mag_runtime_rebuild"
        ),
        "consumed_generic_primitives": list(OPL_CONSUMED_GENERIC_PRIMITIVES),
        "consumed_projection_surfaces": list(OPL_CONSUMED_PROJECTION_SURFACES),
        "functional_harness_consumer_coverage_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/"
            "functional_harness_consumer_coverage"
        ),
        "mag_retained_authority": list(MAG_CONSUMED_RETAINED_AUTHORITY),
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


def build_functional_harness_consumer_coverage() -> dict[str, Any]:
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
                    "stage_attempt_records",
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
        "mag_retained_authority": list(MAG_FUNCTIONAL_HARNESS_RETAINED_AUTHORITY),
        "fail_closed_rules": {
            "opl_harness_pass_is_grant_ready": False,
            "opl_harness_pass_is_export_ready": False,
            "opl_can_hold_generic_runtime_in_mag": False,
            "opl_can_write_memory_body": False,
            "opl_can_write_grant_truth": False,
        },
        "domain_handler_projection_policy": "refs_receipts_blockers_verdict_refs_action_metadata_only",
        "output_guard_ref": "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard",
    }


def build_opl_family_conflict_blocker_projection() -> dict[str, Any]:
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


def build_opl_runtime_observability_consumption() -> dict[str, Any]:
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
            "mag_can_write_opl_stage_attempt_records": False,
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


def build_thin_surface_output_guard() -> dict[str, Any]:
    return {
        "surface_kind": "mag_thin_surface_output_guard",
        "guard_id": "mag.thin_surface.output_guard.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "output_policy": "grant_refs_and_receipts_only_no_generic_runtime_state",
        "allowed_output_classes": list(MAG_THIN_SURFACE_OUTPUT_CLASSES),
        "private_functional_state_output_classes_forbidden": list(
            PRIVATE_FUNCTIONAL_STATE_OUTPUT_CLASSES
        ),
        "required_domain_handler_return_refs": {
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
            "generated_domain_handler_owner_state",
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
            "mag_can_emit_local_attempt_record_state": False,
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


def build_standard_agent_scaffold_alignment() -> dict[str, Any]:
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
            "src/med_autogrant/product_entry_parts/domain_handler.py",
            "schemas/v1/product-entry-manifest.schema.json",
            "tests/product_entry_cases/test_domain_handler.py",
            "tests/product_entry_cases/test_functional_closure.py",
        ],
        "retained_program_surface_kinds": [
            "domain_entry",
            "product_entry_manifest_builder",
            "domain_handler_adapter",
            "schema_contract",
            "focused_product_entry_tests",
            "declarative_grant_pack_compiler_input",
            "minimal_authority_functions",
        ],
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "domain_entry_owner": TARGET_DOMAIN_ID,
            "domain_handler_owner": TARGET_DOMAIN_ID,
            "schema_owner": TARGET_DOMAIN_ID,
            "test_owner": TARGET_DOMAIN_ID,
            "opl_scaffold_owner": "one-person-lab",
            "mag_owns_generic_scaffold_template": False,
            "mag_owns_generic_runtime_framework": False,
            "mag_is_knowledge_only_repository": False,
            "mag_owns_generated_product_surface_template": False,
        },
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
