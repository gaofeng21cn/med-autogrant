from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.domain_handler_contract import (
    DOMAIN_HANDLER_ADAPTER_ID,
    DOMAIN_HANDLER_EXPORT_KIND,
)
from product_entry_cases.support import (
    assert_contains_all,
    assert_false_keys,
    assert_path_values,
    assert_true_keys,
)


def assert_domain_handler_export_maps_runtime_and_attention_surfaces(
    testcase: Any,
    payload: Mapping[str, Any],
    repo_root: Path,
) -> None:
    testcase.assertTrue(payload["ok"])
    testcase.assertEqual(payload["command"], "domain-handler-export")
    export = payload["domain_handler_export"]
    assert_domain_handler_export_identity(testcase, export)
    assert_domain_handler_substrate_and_receipts(testcase, export)
    thinning = export["mag_consumer_thinning_contract"]
    assert_domain_handler_consumer_thinning_contract(testcase, export, thinning)
    assert_domain_handler_consumed_surfaces_and_audit(testcase, export, thinning)
    assert_domain_handler_external_evidence(testcase, export, thinning)
    assert_domain_handler_generated_handoff_and_authority(testcase, export, thinning, repo_root)
    assert_domain_handler_output_guard_and_follow_through(testcase, export, thinning)
    assert_domain_handler_wakeup_autonomy_and_control_plane(testcase, export)


def assert_domain_handler_export_identity(testcase: Any, export: Mapping[str, Any]) -> None:
    assert_path_values(
        testcase,
        export,
        {
            "surface_kind": DOMAIN_HANDLER_EXPORT_KIND,
            "adapter_id": DOMAIN_HANDLER_ADAPTER_ID,
            "caller_owner_contract.active_caller_owner": "med-autogrant",
            "caller_owner_contract.active_caller_surface": (
                "mag_domain_handler_handler_until_opl_caller_evidence"
            ),
            "caller_owner_contract.target_caller_owner": "one-person-lab",
            "caller_owner_contract.target_caller_surface": "opl_generated_or_hosted_domain_handler",
            "caller_owner_contract.domain_handler_target": "med-autogrant",
            "caller_owner_contract.domain_handler_owner": "med-autogrant",
            "caller_owner_contract.claims_fully_cleaned": False,
            "caller_owner_contract.mag_handler_boundary_ready": True,
            "caller_owner_contract.external_opl_generated_or_hosted_caller_evidence_required": True,
            "substrate_boundary.online_substrate_owner": "explicit_opl_provider",
            "substrate_boundary.control_plane_owner": "one-person-lab",
            "substrate_boundary.domain_truth_owner": "med-autogrant",
            "substrate_boundary.hermes_proof_executor_default": False,
            "runtime_control.surface_kind": "runtime_control",
            "runtime_continuity.surface_kind": "skill_runtime_continuity",
            "standard_domain_agent_skeleton.surface_kind": "standard_domain_agent_skeleton",
            "artifact_locator_contract.surface_kind": "domain_artifact_locator_contract",
            "source_provenance.surface_kind": "source_provenance",
            "source_provenance.source_provenance_ref.ref": "docs/source/README.md",
        },
    )
    testcase.assertIn("OPL may explicitly choose", export["substrate_boundary"]["default_executor_note"])
    testcase.assertIn(
        "no_runtime_workbench_ledger_or_scheduler_authority_transferred",
        export["source_provenance"]["authority_boundary"],
    )


def assert_domain_handler_substrate_and_receipts(testcase: Any, export: Mapping[str, Any]) -> None:
    substrate_adapter = export["opl_substrate_adapter_export"]
    assert_path_values(
        testcase,
        substrate_adapter,
        {
            "surface_kind": "mag_opl_substrate_adapter_export",
            "adapter_id": "mag.opl_substrate_adapter.export.v1",
            "workspace_ref_index.body_policy": "locator_only_no_workspace_body",
            "source_ref_index.index_policy": "source_refs_only_no_source_body",
            "artifact_ref_index.body_policy": "locator_and_inventory_refs_only_no_package_body",
            "memory_ref_index.body_policy": "locator_and_receipt_refs_only_no_memory_body",
            "body_exposure_policy.owner_receipt": "receipt_ref_only_no_authority_transfer",
        },
    )
    assert_false_keys(testcase, substrate_adapter["authority_boundary"], ("opl_can_read_package_body", "opl_can_read_memory_body", "opl_can_issue_owner_receipt"))
    hosted_proof = export["controlled_stage_attempt_projection"][
        "opl_hosted_controlled_grant_stage_attempt_proof"
    ]
    assert_path_values(
        testcase,
        export,
        {
            "opl_control_plane.substrate_adapter_export_ref": (
                "/domain_handler_export/opl_substrate_adapter_export"
            ),
            "controlled_stage_attempt_projection.surface_kind": "controlled_stage_attempt_projection",
        },
    )
    assert_path_values(
        testcase,
        hosted_proof,
        {
            "surface_kind": "opl_hosted_controlled_grant_stage_attempt_proof",
            "maps_to_opl_contract": "opl_hosted_controlled_stage_attempt_proof.v1",
            "consumed_memory_proof_ref": (
                "/product_entry_manifest/domain_memory_descriptor_locator/"
                "controlled_consumed_memory_proof"
            ),
            "writeback_receipt_proof_ref": (
                "/product_entry_manifest/domain_memory_descriptor_locator/writeback_receipt_proof"
            ),
            "repo_tracked_real_receipt_instance": False,
            "repo_tracked_real_memory_body": False,
        },
    )
    assert_false_keys(testcase, hosted_proof["authority_boundary"], ("opl_can_hold_fundability_verdict", "opl_can_hold_authoring_quality_verdict", "opl_can_hold_export_verdict"))
    testcase.assertEqual(
        export["receipt_refs"],
        export["controlled_stage_attempt_projection"]["receipt_refs"],
    )
    apply_proof = export["controlled_domain_memory_apply_proof"]
    assert_path_values(
        testcase,
        apply_proof,
        {
            "surface_kind": "controlled_grant_stage_domain_memory_apply_proof",
            "operator_receipt_projection.surface_kind": "mag_domain_memory_operator_receipt_projection",
            "authority_boundary.can_write_fundability_verdict": False,
        },
    )
    testcase.assertEqual(export["memory_receipt_refs"], apply_proof["writeback_receipt_refs"])
    testcase.assertEqual(export["repo_source_layout_audit"], apply_proof["repo_source_layout_audit"])
    assert_path_values(
        testcase,
        export["owner_receipt_contract"],
        {
            "surface_kind": "mag_owner_receipt_contract",
            "allowed_return_shapes": ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
        },
    )


def assert_domain_handler_consumer_thinning_contract(testcase: Any, export: Mapping[str, Any], thinning: Mapping[str, Any]) -> None:
    assert_path_values(
        testcase,
        thinning,
        {
            "surface_kind": "mag_consumer_thinning_contract",
            "active_caller_owner": "med-autogrant",
            "active_caller_surface": "mag_direct_domain_entry_until_opl_caller_evidence",
            "domain_handler_target": "med-autogrant",
            "domain_handler_owner": "med-autogrant",
            "state": "mag_handler_boundary_ready_external_caller_evidence_gated",
            "domain_handler_contract_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
        },
    )
    testcase.assertEqual(
        thinning["exposed_domain_handler_return_refs"],
        {
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
    )
    bridge_refs = thinning["bridge_exit_gate_refs"]
    assert_path_values(
        testcase,
        bridge_refs,
        {
            "generated_surface_bridge_exit_gate_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff/bridge_exit_gate"
            ),
            "legacy_exit_gate_policy": "delete_or_history_tombstone_after_replacement_proof",
            "claims_all_bridge_exits_complete": False,
            "mag_handler_boundary_ready": True,
        },
    )
    testcase.assertEqual(
        export["functional_followthrough_gap_classification"],
        thinning["functional_followthrough_gap_classification"],
    )
    assert_path_values(
        testcase,
        thinning,
        {
            (
                "functional_followthrough_gap_classification",
                "mag_functional_structure_gap_count",
            ): 0,
            (
                "functional_followthrough_gap_classification",
                "authority_boundary",
                "claims_production_long_run_soak_complete",
            ): False,
            "authority_boundary.mag_rebuilds_opl_runtime": False,
            "authority_boundary.generic_wrapper_active_caller_owner": (
                "evidence_required_from_one-person-lab"
            ),
            "authority_boundary.mag_role_for_generated_wrappers": (
                "domain_handler_ref_only_adapter_and_minimal_authority_functions"
            ),
        },
    )
    testcase.assertEqual(thinning["forbidden_mag_owned_generic_primitives"], [])
    assert_contains_all(testcase, thinning["forbidden_mag_generic_owner_roles"], ("generic_operator_workbench_owner", "generic_workspace_source_intake_owner", "generic_memory_transport_owner", "generic_artifact_gallery_owner", "generic_observability_slo_owner"))


def assert_domain_handler_consumed_surfaces_and_audit(testcase: Any, export: Mapping[str, Any], thinning: Mapping[str, Any]) -> None:
    consumed = export["consumed_opl_standard_surfaces"]
    testcase.assertEqual(consumed, thinning["consumed_opl_standard_surfaces"])
    assert_path_values(
        testcase,
        consumed,
        {
            "surface_kind": "mag_consumed_opl_standard_surfaces",
            "domain_handler_projection_ref": "/domain_handler_export/mag_consumer_thinning_contract",
            "authority_boundary.opl_standard_scaffold_owner": "one-person-lab",
        },
    )
    assert_true_keys(testcase, consumed["authority_boundary"], ("mag_consumes_standard_scaffold", "mag_consumes_generic_primitives"))
    assert_false_keys(testcase, consumed["authority_boundary"], ("mag_can_own_generic_memory_transport", "mag_can_own_generic_artifact_gallery", "mag_can_own_generic_operator_workbench", "mag_can_own_generic_observability_slo", "mag_can_own_generic_artifact_lifecycle", "opl_harness_pass_can_declare_grant_ready", "opl_harness_pass_can_declare_export_ready"))
    assert_contains_all(testcase, consumed["consumed_projection_surfaces"], ("family_conflict_envelope", "runtime_observability_export"))
    assert_contains_all(testcase, consumed["mag_retained_authority"], ("grant_truth", "package_authority"))
    conflict_projection = export["opl_family_conflict_blocker_projection"]
    testcase.assertEqual(conflict_projection, thinning["opl_family_conflict_blocker_projection"])
    assert_path_values(
        testcase,
        conflict_projection,
        {
            "projection_policy": "typed_blocker_only_no_fallback_completion",
            "authority_boundary.can_write_domain_truth": False,
            "authority_boundary.can_fallback_complete": False,
        },
    )
    observability = export["opl_runtime_observability_consumption"]
    testcase.assertEqual(observability, thinning["opl_runtime_observability_consumption"])
    assert_path_values(
        testcase,
        observability,
        {
            "observability_export_kind": "opl_runtime_observability_export",
            "consumption_policy": "read_only_refs_and_counts_no_repair_execution",
            "stage_attempt_projection_consumption.provider_completion_is_grant_ready": False,
            "authority_boundary.can_execute_repair": False,
            "authority_boundary.can_authorize_quality_verdict": False,
        },
    )
    testcase.assertIn("stage_attempt_control_loop_projection", observability["consumed_opl_surfaces"])
    coverage = export["functional_harness_consumer_coverage"]
    testcase.assertEqual(coverage, thinning["functional_harness_consumer_coverage"])
    assert_path_values(
        testcase,
        coverage,
        {
            "surface_kind": "mag_functional_harness_consumer_coverage",
            "coverage_chain_ids": [
                "memory_refs_only_writeback_chain",
                "queue_stage_attempt_typed_closeout_chain",
                "generic_transition_runner_chain",
                "restart_dead_letter_repair_human_gate_chain",
            ],
            "claims_opl_functional_harness_pass": False,
            "claims_grant_ready": False,
            "claims_export_ready": False,
            "fail_closed_rules.opl_harness_pass_is_grant_ready": False,
            "fail_closed_rules.opl_harness_pass_is_export_ready": False,
            "fail_closed_rules.opl_can_hold_generic_runtime_in_mag": False,
        },
    )
    audit = export["privatized_functional_module_audit"]
    testcase.assertEqual(audit, thinning["privatized_functional_module_audit"])
    testcase.assertEqual(audit["surface_kind"], "mag_privatized_functional_module_audit")
    testcase.assertEqual(
        {
            item["module_id"]
            for item in audit["declarative_pack_surfaces"]
            if item["classification"] == "declarative_pack_surface"
        },
        {
            "runtime_registration",
            "task_lifecycle",
            "source_intake_shell",
        },
    )
    testcase.assertEqual(
        {
            item["module_id"]
            for item in audit["refs_only_adapter_surfaces"]
            if item["classification"] == "refs_only_adapter"
        },
        {
            "lifecycle_adapter",
            "observability",
            "domain_handler_product_status_shell",
            "package_lifecycle_shell",
            "human_workbench_scheduler_daemon",
        },
    )
    testcase.assertIn("package_readiness_submission_ready", audit["domain_authority_do_not_retire"])
    testcase.assertIn("fundability_verdict", audit["domain_authority_do_not_retire"])
    consumer_modules = {
        item["module_id"]: item
        for item in audit["declarative_pack_surfaces"]
    }
    testcase.assertEqual(
        consumer_modules["source_intake_shell"]["active_caller_status"],
        "active_declarative_source_requirements_pack_projection",
    )
    testcase.assertIn(
        "src/med_autogrant/workspace_validation.py",
        consumer_modules["source_intake_shell"]["code_paths"],
    )
    testcase.assertIn(
        "funding call interpretation",
        consumer_modules["source_intake_shell"]["cannot_absorb_reason"],
    )
    retire_modules = {item["module_id"]: item for item in audit["retire_or_tombstone_surfaces"]}
    assert_path_values(
        testcase,
        retire_modules["closed_default_path_history_index"],
        {"active_caller_status": "closed_default_paths_absent_no_active_caller"},
    )
    no_active_caller_evidence = retire_modules[
        "closed_default_path_history_index"
    ]["no_active_caller_evidence"]
    assert_path_values(
        testcase,
        no_active_caller_evidence,
        {
            "status": "no_active_caller_observed",
            "no_active_caller_observed": True,
            "physical_delete_authorized": False,
        },
    )
    testcase.assertEqual(
        retire_modules["closed_default_path_history_index"]["code_paths"],
        [
            (
                "src/med_autogrant/product_entry_parts/functional_closure_skeleton.py:"
                "closed_default_path_history_summary"
            ),
        ],
    )
    no_active_caller_summary = audit["no_active_caller_evidence_summary"]
    assert_path_values(
        testcase,
        no_active_caller_summary,
        {
            "status": "all_retired_surfaces_no_active_caller_observed",
            "retired_surface_count": 6,
            "no_active_caller_observed_count": 6,
            "physical_delete_authorized": False,
        },
    )
    private_retirement_evidence = audit["private_platform_retirement_owner_evidence"]
    assert_path_values(
        testcase,
        private_retirement_evidence,
        {
            "status": "no_active_caller_evidence_observed_not_delete_authorized",
            "physical_delete_authorized": False,
            "ready_claim_authorized": False,
        },
    )
    assert_false_keys(
        testcase,
        audit["fail_closed_rules"],
        ("provider_completion_is_grant_ready", "mag_can_rebuild_generic_runtime"),
    )
    testcase.assertEqual(
        export["declarative_grant_pack_compiler_input"],
        thinning["declarative_grant_pack_compiler_input"],
    )
    testcase.assertEqual(export["generated_surface_handoff"], thinning["generated_surface_handoff"])
    testcase.assertEqual(
        export["external_evidence_request_pack"],
        thinning["external_evidence_request_pack"],
    )


def assert_domain_handler_external_evidence(testcase: Any, export: Mapping[str, Any], thinning: Mapping[str, Any]) -> None:
    external_pack = export["external_evidence_request_pack"]
    assert_path_values(
        testcase,
        external_pack,
        {
            "surface_kind": "mag_external_evidence_request_pack",
            "state": "request_pack_declared_external_evidence_not_claimed",
            "consumer_thinning_contract_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
            "required_refs_summary.domain_handler_projection_ref": (
                "/domain_handler_export/external_evidence_request_pack"
            ),
        },
    )
    testcase.assertIn("one-person-lab", external_pack["requested_from"])
    testcase.assertIn("codex_app", external_pack["requested_from"])
    testcase.assertIn("production_caller", external_pack["requested_from"])
    assert_false_keys(testcase, external_pack["forbidden_completion_claims"], ("provider_completion_is_fundability_ready", "provider_completion_is_quality_ready", "provider_completion_is_export_ready", "claims_all_bridge_exits_complete", "claims_production_long_run_soak_complete"))
    assert_false_keys(testcase, external_pack["authority_boundary"], ("mag_claims_external_evidence_exists", "mag_claims_direct_hosted_parity_passed", "opl_can_declare_fundability_verdict"))
    testcase.assertEqual(
        export["generated_hosted_default_caller_proof"],
        thinning["generated_hosted_default_caller_proof"],
    )
    default_caller_proof = export["generated_hosted_default_caller_proof"]
    assert_path_values(
        testcase,
        default_caller_proof,
        {
            "default_caller_cutover_state": (
                "mag_handler_boundary_ready_external_default_caller_evidence_gated"
            ),
            "direct_hosted_parity_workorder.parity_owner": "one-person-lab",
            "direct_hosted_parity_workorder.claims_parity_passed": False,
            "no_forbidden_write_boundary.runtime_receipt_write_policy": (
                "runtime_store_only_no_repo_source_receipt_instances"
            ),
        },
    )
    assert_false_keys(testcase, default_caller_proof["authority_boundary"], ("mag_owns_generic_runtime", "opl_generated_caller_can_sign_owner_receipt"))


def assert_domain_handler_generated_handoff_and_authority(testcase: Any, export: Mapping[str, Any], thinning: Mapping[str, Any], repo_root: Path) -> None:
    testcase.assertEqual(export["minimal_authority_functions"], thinning["minimal_authority_functions"])
    bridge_exit = export["generated_surface_handoff"]["bridge_exit_gate"]
    testcase.assertEqual(bridge_exit["surface_kind"], "mag_bridge_exit_gate")
    testcase.assertEqual(bridge_exit["replacement_owner"], "one-person-lab")
    testcase.assertEqual(bridge_exit["domain_handler_owner"], "med-autogrant")
    testcase.assertEqual(
        bridge_exit["exit_action"],
        "delete_or_history_tombstone_mag_handwritten_wrapper_keep_domain_handler",
    )
    testcase.assertFalse(bridge_exit["claims_exit_complete"])
    testcase.assertTrue(bridge_exit["mag_handler_boundary_ready"])
    testcase.assertFalse(bridge_exit["claims_production_long_run_soak_complete"])
    testcase.assertEqual(
        bridge_exit["production_soak_gate_status"],
        "external_live_soak_and_caller_evidence_not_claimed_by_mag_repo",
    )
    testcase.assertIn(
        "no_active_legacy_wrapper_caller_scan",
        bridge_exit["required_evidence"],
    )
    testcase.assertFalse(
        bridge_exit["authority_boundary"]["mag_can_keep_generic_wrapper_after_exit"]
    )
    testcase.assertEqual(
        export["generated_surface_handoff"]["generated_surface_ids"],
        [
            "product_status",
            "product_user_loop",
            "domain_handler",
            "grouped_cli_api",
            "projection_builder",
            "lifecycle_wrapper",
        ],
    )
    testcase.assertFalse(
        export["generated_surface_handoff"]["authority_boundary"][
            "generated_surface_can_declare_verdict"
        ]
    )
    handoff_currentness = export["generated_surface_handoff"]["current_mag_path_status"]
    testcase.assertEqual(handoff_currentness["surface_kind"], "mag_generated_surface_handoff_currentness_proof")
    testcase.assertEqual(handoff_currentness["status"], "current")
    testcase.assertEqual(export["generated_surface_handoff"]["missing_current_mag_path_count"], 0)
    testcase.assertEqual(handoff_currentness["missing_current_mag_path_count"], 0)
    testcase.assertEqual(handoff_currentness["missing_current_mag_paths"], [])
    testcase.assertEqual(
        export["generated_surface_handoff"]["stale_path_policy"],
        "history_or_source_ref_refresh_only",
    )
    testcase.assertTrue(handoff_currentness["claims_opl_replacement_exists"])
    testcase.assertFalse(handoff_currentness["claims_domain_repo_physical_delete_authorized"])
    testcase.assertFalse(handoff_currentness["claims_all_bridge_exits_complete"])
    testcase.assertFalse(handoff_currentness["claims_production_long_run_soak_complete"])
    for surface in export["generated_surface_handoff"]["generated_or_bridge_surfaces"]:
        with testcase.subTest(bridge_surface=surface["surface_id"]):
            testcase.assertEqual(surface["bridge_exit_gate"]["surface_kind"], "mag_bridge_exit_gate")
            testcase.assertEqual(surface["bridge_exit_gate"]["replacement_owner"], "one-person-lab")
            testcase.assertFalse(surface["bridge_exit_gate"]["claims_exit_complete"])
            testcase.assertFalse(surface["bridge_exit_gate"]["claims_production_long_run_soak_complete"])
            testcase.assertEqual(
                surface["bridge_exit_gate"]["exit_action"],
                "delete_or_history_tombstone_this_mag_wrapper_keep_domain_handler",
            )
            testcase.assertEqual(surface["current_mag_path_status"]["status"], "current")
            testcase.assertEqual(surface["missing_current_mag_path_count"], 0)
            testcase.assertEqual(surface["current_mag_path_status"]["missing_count"], 0)
            for path_status in surface["current_mag_path_status"]["paths"]:
                testcase.assertTrue(path_status["exists"])
                testcase.assertTrue((repo_root / path_status["path"]).is_file())
    testcase.assertEqual(
        {
            item["function_id"]
            for item in export["minimal_authority_functions"]
        },
        {
            "fundability_verdict",
            "quality_verdict",
            "export_verdict",
            "package_authority",
            "memory_accept_reject",
            "owner_receipt_signer",
            "grant_helper",
        },
    )
    for authority_function in export["minimal_authority_functions"]:
        with testcase.subTest(domain_handler_authority_function=authority_function["function_id"]):
            testcase.assertEqual(
                authority_function["ai_first_guard_policy"],
                "stage_artifact_or_owner_receipt_required",
            )
            testcase.assertEqual(
                authority_function["output_boundary"]["allowed_return_shapes"],
                authority_function["allowed_return_shapes"],
            )
            testcase.assertIn("typed_blocker", authority_function["allowed_return_shapes"])
            testcase.assertIn(
                "mechanical_ready_verdict",
                authority_function["output_boundary"]["forbidden_outputs"],
            )


def assert_domain_handler_output_guard_and_follow_through(testcase: Any, export: Mapping[str, Any], thinning: Mapping[str, Any]) -> None:
    output_guard = thinning["thin_surface_output_guard"]
    testcase.assertEqual(output_guard["surface_kind"], "mag_thin_surface_output_guard")
    testcase.assertEqual(output_guard["allowed_output_classes"], thinning["mag_owned_outputs"])
    testcase.assertEqual(output_guard["required_domain_handler_return_refs"], thinning["exposed_domain_handler_return_refs"])
    testcase.assertEqual(
        output_guard["private_functional_state_output_classes_forbidden"],
        [
            "local_runtime_journal_state",
            "local_attempt_record_state",
            "attention_queue_state",
            "stage_attempt_records_state",
            "package_lifecycle_state",
            "source_intake_state",
            "operator_workbench_state",
            "scheduler_daemon_state",
            "hermes_state_db_runtime_state",
        ],
    )
    assert_contains_all(testcase, output_guard["forbidden_output_classes"], ("generic_memory_transport_state", "generic_artifact_lifecycle_state", "generic_observability_slo_state", "local_attempt_record_state", "package_lifecycle_state", "source_intake_state", "hermes_state_db_runtime_state", "family_conflict_envelope_completion_claim", "functional_harness_runtime_state", "opl_harness_pass_grant_ready", "opl_harness_pass_export_ready"))
    assert_false_keys(testcase, output_guard["authority_boundary"], ("mag_can_emit_generic_runtime_state", "mag_can_emit_generic_workbench_state", "mag_can_emit_generic_observability_state", "mag_can_emit_private_functional_state", "mag_can_emit_local_attempt_record_state", "mag_can_emit_source_intake_state", "mag_can_emit_package_lifecycle_state", "mag_can_emit_hermes_state_db_runtime_state", "mag_can_emit_family_conflict_completion_claim", "mag_can_emit_functional_harness_runtime_state", "opl_harness_pass_can_declare_grant_ready", "opl_harness_pass_can_declare_export_ready"))
    scaffold_guard = thinning["standard_agent_scaffold_alignment"]
    testcase.assertEqual(
        scaffold_guard["surface_kind"],
        "mag_standard_agent_scaffold_thin_surface_guard",
    )
    testcase.assertFalse(scaffold_guard["knowledge_only_repository"])
    testcase.assertTrue(scaffold_guard["retains_domain_program_surfaces"])
    testcase.assertFalse(export["owner_receipt_contract"]["forbidden_write_proof"]["opl_can_write_grant_truth"])
    testcase.assertEqual(
        export["lifecycle_guarded_apply_proof"]["surface_kind"],
        "mag_lifecycle_guarded_apply_proof",
    )
    testcase.assertEqual(
        [operation["operation"] for operation in export["lifecycle_guarded_apply_proof"]["operations"]],
        ["cleanup", "restore", "retention"],
    )
    testcase.assertEqual(
        export["physical_skeleton_follow_through"]["surface_kind"],
        "mag_physical_skeleton_follow_through",
    )
    physical_follow_through = export["physical_skeleton_follow_through"]
    testcase.assertFalse(physical_follow_through["moves_workspace_artifacts"])
    testcase.assertEqual(
        physical_follow_through["replacement_parity_refs"],
        [
            "/product_entry_manifest/mag_consumer_thinning_contract",
            "/product_entry_manifest/owner_receipt_contract",
            "/product_entry_manifest/grant_transition_oracle",
            "/product_entry_manifest/controlled_soak_no_regression_attempt",
            "/product_entry_manifest/physical_skeleton_follow_through/active_path_current_role_guard",
            "/product_entry_manifest/physical_skeleton_follow_through/current_command_role_guard",
        ],
    )
    testcase.assertEqual(
        physical_follow_through["no_regression_evidence_refs"],
        [
            "tests/product_entry_cases/test_hosted_receipt_verification.py::ProductEntryHostedReceiptVerificationTest::test_hosted_receipt_verification_matches_opl_attempt_to_mag_receipt_refs",
            "tests/product_entry_cases/test_grant_transition_oracle.py::ProductEntryGrantTransitionOracleTest::test_oracle_domain_handler_closeout_writes_no_regression_owner_receipt_refs",
        ],
    )
    testcase.assertEqual(
        physical_follow_through["tombstone_refs"],
        ["docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md"],
    )
    testcase.assertEqual(
        physical_follow_through["history_refs"],
        [
            "docs/decisions.md#2026-05-12-temporal-backed-opl-production-runtime-supersedes-gateway-manager-wording",
            "docs/status.md#旧面退役校准",
        ],
    )
    testcase.assertEqual(physical_follow_through["forbidden_active_path_residue"], [])
    closed_history = physical_follow_through["closed_default_path_history_summary"]
    testcase.assertEqual(closed_history["state"], "closed_history_index_only")
    testcase.assertEqual(closed_history["closed_path_family_count"], 3)
    testcase.assertEqual(closed_history["active_source_residue_count"], 0)
    testcase.assertFalse(closed_history["stores_closed_path_names"])
    testcase.assertEqual(
        export["ideal_state_closure_status"]["surface_kind"],
        "mag_ideal_state_closure_status",
    )
    testcase.assertFalse(export["ideal_state_closure_status"]["claims_production_long_run_soak_complete"])
    testcase.assertFalse(
        export["controlled_stage_attempt_projection"]["opl_consumption_contract"][
            "can_hold_fundability_verdict"
        ]
    )
    testcase.assertFalse(
        export["controlled_stage_attempt_projection"]["opl_consumption_contract"][
            "can_hold_export_verdict"
        ]
    )


def assert_domain_handler_wakeup_autonomy_and_control_plane(testcase: Any, export: Mapping[str, Any]) -> None:
    testcase.assertEqual(export["todo_wakeup"]["surface_kind"], "mag_todo_wakeup_projection")
    testcase.assertEqual(
        export["todo_wakeup"]["authoring_loop_continuation"]["automation_id"],
        "mag.authoring_loop_continuation",
    )
    testcase.assertNotIn("hermes_wakeup_role", export["todo_wakeup"])
    wakeup_contract = export["todo_wakeup"]["opl_wakeup_contract"]
    testcase.assertEqual(wakeup_contract["owner"], "one-person-lab")
    testcase.assertEqual(wakeup_contract["target_action_ref"], "open_grant_user_loop")
    testcase.assertEqual(wakeup_contract["target_surface"], "opl_generated_grant_user_loop")
    testcase.assertTrue(wakeup_contract["target_command"].startswith("opl://generated-surfaces/mag/"))
    testcase.assertEqual(wakeup_contract["target_command"], export["todo_wakeup"]["recommended_wakeup_command"])
    testcase.assertIsNone(wakeup_contract["domain_handler_dispatch_action"])
    testcase.assertEqual(wakeup_contract["queue_write_policy"], "enqueue_wakeup_only_no_grant_truth_writes")
    testcase.assertEqual(wakeup_contract["required_return_shapes"], ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"])
    testcase.assertFalse(any(export["todo_wakeup"]["forbidden_private_runtime_roles"].values()))
    testcase.assertEqual(
        export["autonomy_controller"]["execution_scope"],
        "bounded_single_opl_provider_attempt",
    )
    testcase.assertEqual(
        export["autonomy_controller"]["mag_role"],
        "refs_only_domain_authority_action_target",
    )
    testcase.assertEqual(export["autonomy_controller"]["post_start_residency_owner"], "one-person-lab")
    testcase.assertEqual(export["autonomy_controller"]["attempt_ledger_owner"], "one-person-lab")
    testcase.assertEqual(export["autonomy_controller"]["max_domain_cycles_per_invocation"], 1)
    testcase.assertFalse(export["autonomy_controller"]["mag_long_running_driver"])
    testcase.assertFalse(export["autonomy_controller"]["mag_scheduler_daemon_owner"])
    testcase.assertFalse(export["autonomy_controller"]["mag_attempt_ledger_owner"])
    testcase.assertEqual(
        export["autonomy_controller"]["allowed_return_shapes"],
        ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
    )
    testcase.assertFalse(export["autonomy_controller"]["hermes_proof_executor_default"])
    testcase.assertEqual(export["user_loop_attention_queue"]["queue_owner"], "one-person-lab")
    testcase.assertEqual(
        export["user_loop_attention_queue"]["queue_write_policy"],
        "enqueue_wakeup_only_no_grant_truth_writes",
    )
    testcase.assertEqual(
        export["opl_control_plane"]["write_policy"],
        "opl_index_only_no_grant_truth_writes",
    )
    testcase.assertEqual(
        export["opl_control_plane"]["replacement_expectations_ref"],
        "/domain_handler_export/mag_consumer_thinning_contract/opl_replacement_expectations",
    )
    testcase.assertEqual(
        export["opl_control_plane"]["allowed_dispatch_actions"],
        [
            "closeout/codex-stage-receipts",
            "closeout/executor-first-bundle",
            "closeout/operator-readiness",
            "closeout/physical-morphology-guard",
            "domain-memory/decide",
            "domain-memory/propose",
            "lifecycle/receipt",
            "stage-attempt/closeout",
        ],
    )
    testcase.assertIn("hermes_proof_executor", export["guardrails"]["forbidden_defaults"])
    testcase.assertEqual(
        export["guardrails"]["dispatch_boundary"],
        "OPL-hosted caller may invoke only MAG domain handler guarded actions.",
    )
