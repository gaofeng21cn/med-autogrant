from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.consumer_thinning_shell import (
    PRIVATE_FUNCTIONAL_STATE_OUTPUT_CLASSES,
)


def assert_consumer_thinning_contract_for_opl_replacement_handoff(
    testcase: Any,
    manifest: Mapping[str, Any],
) -> None:
    thinning = manifest["mag_consumer_thinning_contract"]
    audit = thinning["privatized_functional_module_audit"]

    assert_consumer_thinning_contract_identity(testcase, thinning)
    assert_consumer_thinning_consumed_surfaces(testcase, thinning)
    assert_consumer_thinning_harness_and_route_boundary(testcase, thinning)
    assert_consumer_thinning_audit_boundary(testcase, audit)
    assert_consumer_thinning_followthrough_gaps(testcase, thinning)
    assert_consumer_thinning_output_guard_and_authority(testcase, thinning)
    assert_consumer_thinning_replacement_expectations(testcase, manifest, thinning)


def assert_consumer_thinning_contract_identity(testcase: Any, thinning: Mapping[str, Any]) -> None:
    testcase.assertEqual(thinning["surface_kind"], "mag_consumer_thinning_contract")
    testcase.assertEqual(thinning["contract_id"], "mag.consumer_thinning.contract.v1")
    testcase.assertEqual(thinning["target_domain_id"], "med-autogrant")
    testcase.assertEqual(thinning["owner"], "med-autogrant")
    testcase.assertEqual(thinning["adapter_role"], "domain_authority_pack_with_thin_program_surface")
    testcase.assertEqual(thinning["state"], "mag_handler_boundary_ready_external_caller_evidence_gated")
    testcase.assertTrue(thinning["claims_opl_replacement_exists"])
    testcase.assertFalse(thinning["claims_domain_repo_physical_delete_authorized"])
    testcase.assertFalse(thinning["claims_production_long_run_soak_complete"])
    testcase.assertEqual(
        thinning["allowed_return_shapes"],
        ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
    )
    testcase.assertFalse(thinning["bridge_exit_gate_refs"]["claims_all_bridge_exits_complete"])
    testcase.assertTrue(thinning["bridge_exit_gate_refs"]["mag_handler_boundary_ready"])
    testcase.assertEqual(thinning["forbidden_mag_owned_generic_primitives"], [])
    testcase.assertIn("generic_scheduler_owner", thinning["forbidden_mag_generic_owner_roles"])
    testcase.assertIn("generic_memory_transport_owner", thinning["forbidden_mag_generic_owner_roles"])


def assert_consumer_thinning_consumed_surfaces(testcase: Any, thinning: Mapping[str, Any]) -> None:
    consumed = thinning["consumed_opl_standard_surfaces"]
    testcase.assertEqual(consumed["surface_kind"], "mag_consumed_opl_standard_surfaces")
    testcase.assertEqual(
        consumed["consumption_policy"],
        "consume_opl_standard_scaffold_and_generic_primitives_no_mag_runtime_rebuild",
    )
    testcase.assertIn("generic_transition_runner", consumed["consumed_generic_primitives"])
    testcase.assertIn("stage_attempt_control_loop_projection", consumed["consumed_projection_surfaces"])
    testcase.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_memory_transport"])
    testcase.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_artifact_lifecycle"])
    testcase.assertFalse(consumed["authority_boundary"]["opl_harness_pass_can_declare_grant_ready"])

    conflict_projection = thinning["opl_family_conflict_blocker_projection"]
    testcase.assertEqual(conflict_projection["envelope_kind"], "opl_conflict_or_blocker.v1")
    testcase.assertIn("provider_completion_is_domain_ready", conflict_projection["forbidden_claims"])
    testcase.assertFalse(conflict_projection["authority_boundary"]["provider_completion_is_domain_ready"])
    testcase.assertFalse(conflict_projection["authority_boundary"]["can_fallback_complete"])

    observability = thinning["opl_runtime_observability_consumption"]
    testcase.assertEqual(observability["consumption_policy"], "read_only_refs_and_counts_no_repair_execution")
    testcase.assertIn("safe_action_refs", observability["mag_provides_refs"])
    testcase.assertFalse(observability["authority_boundary"]["can_execute_repair"])
    testcase.assertFalse(observability["authority_boundary"]["can_authorize_artifact_export"])


def assert_consumer_thinning_harness_and_route_boundary(testcase: Any, thinning: Mapping[str, Any]) -> None:
    coverage = thinning["functional_harness_consumer_coverage"]
    testcase.assertEqual(coverage["surface_kind"], "mag_functional_harness_consumer_coverage")
    testcase.assertEqual(coverage["harness_owner"], "one-person-lab")
    testcase.assertFalse(coverage["claims_opl_functional_harness_pass"])
    testcase.assertFalse(coverage["claims_grant_ready"])
    testcase.assertFalse(coverage["claims_export_ready"])
    testcase.assertTrue(coverage["coverage_chains"])
    for chain in coverage["coverage_chains"]:
        with testcase.subTest(chain=chain["chain_id"]):
            testcase.assertEqual(chain["mag_role"], "consumer_domain_authority_pack")
            testcase.assertFalse(chain["implemented_in_mag"])
            testcase.assertFalse(chain["mag_claims_generic_runtime_owner"])
            testcase.assertFalse(chain["fail_closed_boundary"]["opl_can_write_grant_truth"])
            testcase.assertTrue(chain["fail_closed_boundary"]["mag_owner_receipt_required"])

    route_stage_boundary = thinning["route_stage_handoff_boundary"]
    testcase.assertEqual(route_stage_boundary["surface_kind"], "mag_route_stage_handoff_boundary")
    testcase.assertFalse(route_stage_boundary["route_is_stage"])
    testcase.assertEqual(route_stage_boundary["route_semantics_owner"], "med-autogrant")
    testcase.assertEqual(route_stage_boundary["stage_graph_owner"], "one-person-lab")
    testcase.assertFalse(route_stage_boundary["mag_owns_inter_route_scheduler"])
    testcase.assertIn("generic_runtime_state", route_stage_boundary["forbidden_payload_classes"])
    testcase.assertFalse(route_stage_boundary["authority_boundary"]["opl_can_write_grant_truth"])
    testcase.assertFalse(route_stage_boundary["authority_boundary"]["mag_implements_generic_route_scheduler"])


def assert_consumer_thinning_audit_boundary(testcase: Any, audit: Mapping[str, Any]) -> None:
    testcase.assertEqual(audit["surface_kind"], "mag_privatized_functional_module_audit")
    testcase.assertEqual(audit["state"], "manifest_projected_for_opl_unified_audit")
    testcase.assertFalse(audit["claims_generic_runtime_removed_from_mag"])
    testcase.assertTrue(audit["claims_opl_replacement_exists"])
    testcase.assertFalse(audit["claims_domain_repo_physical_delete_authorized"])
    testcase.assertFalse(audit["claims_production_long_run_soak_complete"])
    testcase.assertEqual(
        audit["classification_buckets"],
        [
            "declarative_pack_surface",
            "refs_only_adapter",
            "minimal_authority_function",
            "legacy_proof_tombstone",
        ],
    )

    pack_modules = {item["module_id"]: item for item in audit["declarative_pack_surfaces"]}
    refs_modules = {item["module_id"]: item for item in audit["refs_only_adapter_surfaces"]}
    mag_modules = {item["module_id"]: item for item in audit["mag_owned_grant_authority_surfaces"]}
    retire_modules = {item["module_id"]: item for item in audit["retire_or_tombstone_surfaces"]}

    testcase.assertEqual(pack_modules["task_lifecycle"]["classification"], "declarative_pack_surface")
    testcase.assertIn("grant_lifecycle_stage", pack_modules["task_lifecycle"]["mag_retained_authority"])
    testcase.assertIn(
        "artifact_package_lifecycle_shell",
        refs_modules["package_lifecycle_shell"]["opl_expected_primitives"],
    )
    testcase.assertEqual(
        mag_modules["package_readiness_submission_ready"]["classification"],
        "minimal_authority_function",
    )
    testcase.assertIn(
        "submission_ready_verdict",
        mag_modules["package_readiness_submission_ready"]["mag_retained_authority"],
    )
    testcase.assertFalse(retire_modules["repo_owned_scheduler_daemon"]["active_caller_allowed"])
    testcase.assertEqual(
        retire_modules["domain_runtime_patch_bridge"]["active_caller_status"],
        "retired_physical_facade_removed_no_active_caller",
    )
    testcase.assertEqual(
        retire_modules["domain_runtime_patch_bridge"]["code_paths"],
        ["src/med_autogrant/domain_runtime.py:absent"],
    )
    testcase.assertEqual(
        retire_modules["compatibility_only_product_entry_aggregate_test"]["active_callers"],
        [],
    )


def assert_consumer_thinning_followthrough_gaps(testcase: Any, thinning: Mapping[str, Any]) -> None:
    followthrough = thinning["functional_followthrough_gap_classification"]
    testcase.assertEqual(followthrough["surface_kind"], "mag_functional_followthrough_gap_classification")
    testcase.assertEqual(followthrough["state"], "mag_handler_boundary_ready_external_evidence_gated")
    testcase.assertEqual(followthrough["mag_functional_structure_gap_count"], 0)
    testcase.assertEqual(followthrough["remaining_mag_functional_structure_gap_ids"], [])
    testcase.assertEqual(followthrough["standard_agent_source_shape_status"], "landed")
    testcase.assertEqual(
        followthrough["current_mag_source_role"],
        "declarative_pack_domain_handler_refs_only_adapter_or_minimal_authority",
    )
    testcase.assertTrue(followthrough["authority_boundary"]["mag_repo_functional_structure_gaps_zero"])
    testcase.assertTrue(followthrough["authority_boundary"]["mag_repo_active_source_shape_landed"])
    testcase.assertFalse(followthrough["authority_boundary"]["followthrough_gaps_open"])
    testcase.assertFalse(
        followthrough["authority_boundary"]["claims_domain_repo_physical_delete_authorized"]
    )
    testcase.assertFalse(
        followthrough["authority_boundary"]["claims_opl_generated_surface_production_consumed"]
    )
    testcase.assertFalse(followthrough["authority_boundary"]["claims_production_long_run_soak_complete"])

    for evidence_gap in followthrough["reclassified_as_testing_evidence_gaps"]:
        with testcase.subTest(evidence_gap=evidence_gap["gap_id"]):
            testcase.assertEqual(evidence_gap["current_bucket"], "production_evidence_tail")
            testcase.assertEqual(evidence_gap["owner"], "evidence_gate")
            testcase.assertTrue(evidence_gap["mag_surface_refs"])


def assert_consumer_thinning_output_guard_and_authority(testcase: Any, thinning: Mapping[str, Any]) -> None:
    output_guard = thinning["thin_surface_output_guard"]
    testcase.assertEqual(output_guard["surface_kind"], "mag_thin_surface_output_guard")
    for forbidden_state in PRIVATE_FUNCTIONAL_STATE_OUTPUT_CLASSES:
        with testcase.subTest(forbidden_state=forbidden_state):
            testcase.assertIn(forbidden_state, output_guard["forbidden_output_classes"])
    for forbidden_output in {
        "generic_scheduler_state",
        "generic_artifact_lifecycle_state",
        "generic_observability_slo_state",
        "grant_artifact_content",
        "memory_body",
    }:
        testcase.assertIn(forbidden_output, output_guard["forbidden_output_classes"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_generic_runtime_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_private_functional_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_source_intake_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_package_lifecycle_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["opl_harness_pass_can_declare_grant_ready"])

    scaffold_guard = thinning["standard_agent_scaffold_alignment"]
    testcase.assertFalse(scaffold_guard["knowledge_only_repository"])
    testcase.assertTrue(scaffold_guard["retains_domain_program_surfaces"])
    testcase.assertFalse(scaffold_guard["authority_boundary"]["mag_owns_generic_runtime_framework"])

    authority = thinning["authority_boundary"]
    testcase.assertFalse(authority["opl_can_write_domain_truth"])
    testcase.assertFalse(authority["opl_can_write_memory_body"])
    testcase.assertFalse(authority["opl_can_declare_export_ready"])
    testcase.assertFalse(authority["mag_rebuilds_opl_runtime"])
    testcase.assertFalse(authority["mag_implements_generic_artifact_lifecycle"])


def assert_consumer_thinning_replacement_expectations(
    testcase: Any,
    manifest: Mapping[str, Any],
    thinning: Mapping[str, Any],
) -> None:
    expectations = thinning["opl_replacement_expectations"]
    expectation_ids = {item["primitive_id"] for item in expectations}
    testcase.assertIn("workspace_source_intake_shell", expectation_ids)
    testcase.assertIn("generic_transition_runner", expectation_ids)
    testcase.assertIn("artifact_package_lifecycle_shell", expectation_ids)
    for item in expectations:
        with testcase.subTest(primitive_id=item["primitive_id"]):
            testcase.assertEqual(item["owner"], "one-person-lab")
            testcase.assertEqual(item["mag_handoff_policy"], "contract_expectation_only")
            testcase.assertFalse(item["implemented_in_mag"])
    testcase.assertEqual(
        thinning["domain_handler_contract_ref"],
        "/product_entry_manifest/mag_consumer_thinning_contract",
    )
    testcase.assertEqual(
        manifest["ideal_state_closure_status"]["consumer_thinning_contract_ref"],
        "/product_entry_manifest/mag_consumer_thinning_contract",
    )
