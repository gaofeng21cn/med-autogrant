from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.consumer_thinning_audit.classification import (
    build_declarative_pack_surfaces,
    build_mag_owned_grant_authority_surfaces,
    build_refs_only_adapter_surfaces,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit.evidence_gates import (
    build_default_caller_deletion_bridge_exit_gate,
    build_legacy_exit_gate,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit.model import (
    build_retired_functional_module_audit_item,
)
from med_autogrant.product_entry_parts.consumer_thinning_audit.retired_surfaces import (
    build_retire_or_tombstone_surfaces,
)
from med_autogrant.product_entry_parts.consumer_thinning_shell import (
    FORBIDDEN_MAG_GENERIC_OWNER_ROLES,
    MAG_THIN_SURFACE_OUTPUT_CLASSES,
    PRIVATE_FUNCTIONAL_STATE_OUTPUT_CLASSES,
    build_consumed_opl_standard_surfaces,
    build_opl_replacement_expectations,
)


def assert_consumer_thinning_contract_for_opl_replacement_handoff(
    testcase: Any,
    manifest: Mapping[str, Any],
) -> None:
    thinning = manifest["mag_consumer_thinning_contract"]
    assert_consumer_thinning_contract_identity(testcase, thinning)
    assert_consumer_thinning_consumed_surfaces(testcase, thinning)
    assert_consumer_thinning_harness_and_route_boundary(testcase, thinning)
    audit = thinning["privatized_functional_module_audit"]
    assert_consumer_thinning_audit_header(testcase, audit)
    assert_consumer_thinning_audit_pack_modules(testcase, audit)
    assert_consumer_thinning_audit_refs_modules(testcase, audit)
    assert_consumer_thinning_audit_mag_authority_modules(testcase, audit)
    assert_consumer_thinning_audit_retired_surfaces(testcase, audit)
    assert_consumer_thinning_followthrough_gaps(testcase, thinning)
    assert_consumer_thinning_output_guard_and_authority(testcase, thinning)
    assert_consumer_thinning_replacement_expectations(testcase, manifest, thinning)


def assert_consumer_thinning_contract_identity(testcase: Any, thinning: Mapping[str, Any]) -> None:
    testcase.assertEqual(thinning["surface_kind"], "mag_consumer_thinning_contract")
    testcase.assertEqual(thinning["contract_id"], "mag.consumer_thinning.contract.v1")
    testcase.assertEqual(thinning["target_domain_id"], "med-autogrant")
    testcase.assertEqual(thinning["owner"], "med-autogrant")
    testcase.assertEqual(thinning["adapter_role"], "domain_authority_pack_with_thin_program_surface")
    testcase.assertEqual(thinning["active_caller_owner"], "med-autogrant")
    testcase.assertEqual(
        thinning["active_caller_surface"],
        "mag_direct_domain_entry_until_opl_caller_evidence",
    )
    testcase.assertEqual(thinning["domain_handler_target"], "med-autogrant")
    testcase.assertEqual(thinning["domain_handler_owner"], "med-autogrant")
    testcase.assertEqual(thinning["state"], "mag_handler_boundary_ready_external_caller_evidence_gated")
    testcase.assertTrue(thinning["claims_opl_replacement_exists"])
    testcase.assertFalse(thinning["claims_domain_repo_physical_delete_authorized"])
    testcase.assertFalse(thinning["claims_production_long_run_soak_complete"])
    testcase.assertEqual(
        thinning["allowed_return_shapes"],
        ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
    )
    testcase.assertEqual(
        thinning["bridge_exit_gate_refs"]["legacy_exit_gate_policy"],
        "delete_or_history_tombstone_after_replacement_proof",
    )
    testcase.assertFalse(thinning["bridge_exit_gate_refs"]["claims_all_bridge_exits_complete"])
    testcase.assertTrue(thinning["bridge_exit_gate_refs"]["mag_handler_boundary_ready"])
    testcase.assertEqual(
        set(thinning["mag_owned_outputs"]),
        set(MAG_THIN_SURFACE_OUTPUT_CLASSES),
    )
    testcase.assertEqual(thinning["forbidden_mag_owned_generic_primitives"], [])
    testcase.assertEqual(
        thinning["forbidden_mag_generic_owner_roles"],
        list(FORBIDDEN_MAG_GENERIC_OWNER_ROLES),
    )

def assert_consumer_thinning_consumed_surfaces(testcase: Any, thinning: Mapping[str, Any]) -> None:
    consumed = thinning["consumed_opl_standard_surfaces"]
    testcase.assertEqual(consumed, build_consumed_opl_standard_surfaces())
    testcase.assertEqual(consumed["surface_kind"], "mag_consumed_opl_standard_surfaces")
    testcase.assertEqual(
        consumed["consumption_policy"],
        "consume_opl_standard_scaffold_and_generic_primitives_no_mag_runtime_rebuild",
    )
    testcase.assertEqual(
        consumed["consumed_generic_primitives"],
        [
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
    )
    testcase.assertEqual(
        consumed["consumed_projection_surfaces"],
        [
            "family_conflict_envelope",
            "stage_attempt_usage_projection",
            "stage_attempt_control_loop_projection",
            "runtime_observability_export",
            "family_product_operator_projection",
        ],
    )
    testcase.assertEqual(
        consumed["functional_harness_consumer_coverage_ref"],
        "/product_entry_manifest/mag_consumer_thinning_contract/"
        "functional_harness_consumer_coverage",
    )
    testcase.assertEqual(
        set(consumed["mag_retained_authority"]),
        {
            "grant_truth",
            "fundability_verdict",
            "quality_verdict",
            "export_verdict",
            "memory_body_accept_reject",
            "package_authority",
            "owner_receipt",
            "grant_helper",
        },
    )
    testcase.assertTrue(consumed["authority_boundary"]["mag_consumes_standard_scaffold"])
    testcase.assertTrue(consumed["authority_boundary"]["mag_consumes_generic_primitives"])
    testcase.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_memory_transport"])
    testcase.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_artifact_gallery"])
    testcase.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_operator_workbench"])
    testcase.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_observability_slo"])
    testcase.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_artifact_lifecycle"])
    testcase.assertFalse(consumed["authority_boundary"]["opl_harness_pass_can_declare_grant_ready"])
    testcase.assertFalse(consumed["authority_boundary"]["opl_harness_pass_can_declare_export_ready"])
    conflict_projection = thinning["opl_family_conflict_blocker_projection"]
    testcase.assertEqual(conflict_projection["envelope_kind"], "opl_conflict_or_blocker.v1")
    testcase.assertEqual(conflict_projection["projection_policy"], "typed_blocker_only_no_fallback_completion")
    testcase.assertIn("receipt_conflict", conflict_projection["allowed_classifications"])
    testcase.assertIn("provider_completion_is_domain_ready", conflict_projection["forbidden_claims"])
    testcase.assertFalse(conflict_projection["authority_boundary"]["provider_completion_is_domain_ready"])
    testcase.assertFalse(conflict_projection["authority_boundary"]["can_fallback_complete"])
    observability = thinning["opl_runtime_observability_consumption"]
    testcase.assertEqual(observability["observability_export_kind"], "opl_runtime_observability_export")
    testcase.assertEqual(observability["consumption_policy"], "read_only_refs_and_counts_no_repair_execution")
    testcase.assertIn("stage_attempt_usage_projection", observability["consumed_opl_surfaces"])
    testcase.assertIn("stage_attempt_control_loop_projection", observability["consumed_opl_surfaces"])
    testcase.assertIn("runtime_observability_export", observability["consumed_opl_surfaces"])
    testcase.assertIn("safe_action_refs", observability["mag_provides_refs"])
    stage_projection = observability["stage_attempt_projection_consumption"]
    testcase.assertFalse(stage_projection["mag_can_schedule_retry_dead_letter"])
    testcase.assertFalse(stage_projection["mag_can_write_opl_stage_attempt_records"])
    testcase.assertFalse(stage_projection["provider_completion_is_grant_ready"])
    testcase.assertFalse(observability["authority_boundary"]["can_execute_repair"])
    testcase.assertFalse(observability["authority_boundary"]["can_authorize_artifact_export"])

def assert_consumer_thinning_harness_and_route_boundary(testcase: Any, thinning: Mapping[str, Any]) -> None:
    coverage = thinning["functional_harness_consumer_coverage"]
    testcase.assertEqual(coverage["surface_kind"], "mag_functional_harness_consumer_coverage")
    testcase.assertEqual(coverage["owner"], "med-autogrant")
    testcase.assertEqual(coverage["harness_owner"], "one-person-lab")
    testcase.assertEqual(coverage["adapter_role"], "domain_authority_pack_consumer_only")
    testcase.assertFalse(coverage["claims_opl_functional_harness_pass"])
    testcase.assertFalse(coverage["claims_grant_ready"])
    testcase.assertFalse(coverage["claims_export_ready"])
    testcase.assertEqual(
        coverage["coverage_chain_ids"],
        [
            "memory_refs_only_writeback_chain",
            "queue_stage_attempt_typed_closeout_chain",
            "generic_transition_runner_chain",
            "restart_dead_letter_repair_human_gate_chain",
        ],
    )
    testcase.assertEqual(
        {chain["chain_id"] for chain in coverage["coverage_chains"]},
        set(coverage["coverage_chain_ids"]),
    )
    testcase.assertEqual(
        set(coverage["mag_retained_authority"]),
        {
            "grant_truth",
            "fundability_verdict",
            "quality_verdict",
            "export_verdict",
            "grant_memory_body_accept_reject",
            "package_authority",
            "owner_receipt",
            "typed_blocker",
            "domain_handler_projection_adapter",
        },
    )
    testcase.assertFalse(coverage["fail_closed_rules"]["opl_harness_pass_is_grant_ready"])
    testcase.assertFalse(coverage["fail_closed_rules"]["opl_harness_pass_is_export_ready"])
    testcase.assertFalse(coverage["fail_closed_rules"]["opl_can_hold_generic_runtime_in_mag"])
    for chain in coverage["coverage_chains"]:
        with testcase.subTest(chain=chain["chain_id"]):
            testcase.assertEqual(chain["mag_role"], "consumer_domain_authority_pack")
            testcase.assertFalse(chain["implemented_in_mag"])
            testcase.assertFalse(chain["mag_claims_generic_runtime_owner"])
            testcase.assertEqual(chain["harness_owner"], "one-person-lab")
            testcase.assertFalse(chain["fail_closed_boundary"]["harness_pass_can_set_grant_ready"])
            testcase.assertFalse(chain["fail_closed_boundary"]["harness_pass_can_set_export_ready"])
            testcase.assertFalse(chain["fail_closed_boundary"]["opl_can_write_grant_truth"])
        testcase.assertFalse(chain["fail_closed_boundary"]["opl_can_write_memory_body"])
        testcase.assertTrue(chain["fail_closed_boundary"]["mag_owner_receipt_required"])
    route_stage_boundary = thinning["route_stage_handoff_boundary"]
    testcase.assertEqual(
        route_stage_boundary["surface_kind"],
        "mag_route_stage_handoff_boundary",
    )
    testcase.assertFalse(route_stage_boundary["route_is_stage"])
    testcase.assertEqual(route_stage_boundary["route_semantics_owner"], "med-autogrant")
    testcase.assertEqual(route_stage_boundary["domain_truth_owner"], "med-autogrant")
    testcase.assertEqual(route_stage_boundary["stage_graph_owner"], "one-person-lab")
    testcase.assertEqual(route_stage_boundary["stage_lifecycle_owner"], "one-person-lab")
    testcase.assertEqual(route_stage_boundary["runtime_transition_owner"], "one-person-lab")
    testcase.assertEqual(route_stage_boundary["queue_attempt_owner"], "one-person-lab")
    testcase.assertTrue(route_stage_boundary["opl_hydrates_route_refs_to_queue_and_stage_attempts"])
    testcase.assertFalse(route_stage_boundary["mag_owns_inter_route_scheduler"])
    testcase.assertEqual(
        route_stage_boundary["stage_graph_ref"],
        "/product_entry_manifest/family_stage_control_plane",
    )
    testcase.assertEqual(
        route_stage_boundary["route_oracle_ref"],
        "/product_entry_manifest/grant_transition_oracle",
    )
    testcase.assertIn("owner_receipt_ref", route_stage_boundary["allowed_handoff_refs"])
    testcase.assertIn("generic_runtime_state", route_stage_boundary["forbidden_payload_classes"])
    testcase.assertFalse(route_stage_boundary["authority_boundary"]["opl_can_write_grant_truth"])
    testcase.assertFalse(
        route_stage_boundary["authority_boundary"]["opl_can_declare_export_verdict"]
    )
    testcase.assertFalse(
        route_stage_boundary["authority_boundary"][
            "mag_implements_generic_route_scheduler"
        ]
    )
    testcase.assertIn("route_is_stage", route_stage_boundary["forbidden_claims"])
    testcase.assertEqual(
        thinning["exposed_domain_handler_return_refs"]["route_stage_handoff_boundary_ref"],
        "/product_entry_manifest/mag_consumer_thinning_contract/"
        "route_stage_handoff_boundary",
    )

def assert_consumer_thinning_audit_header(testcase: Any, audit: Mapping[str, Any]) -> None:
    testcase.assertEqual(audit["surface_kind"], "mag_privatized_functional_module_audit")
    testcase.assertEqual(audit["state"], "manifest_projected_for_opl_unified_audit")
    testcase.assertTrue(audit["opl_unified_audit_read_model"])
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

def assert_consumer_thinning_audit_pack_modules(testcase: Any, audit: Mapping[str, Any]) -> None:
    testcase.assertEqual(audit["declarative_pack_surfaces"], build_declarative_pack_surfaces())
    pack_modules = {
        item["module_id"]: item
        for item in audit["declarative_pack_surfaces"]
    }
    testcase.assertEqual(
        set(pack_modules),
        {
            "runtime_registration",
            "task_lifecycle",
            "source_intake_shell",
        },
    )
    testcase.assertEqual(
        pack_modules["task_lifecycle"]["classification"],
        "declarative_pack_surface",
    )
    testcase.assertEqual(
        pack_modules["task_lifecycle"]["bridge_exit_gate"],
        build_default_caller_deletion_bridge_exit_gate(
            module_id="task_lifecycle",
            classification=pack_modules["task_lifecycle"]["classification"],
            current_surface_refs=pack_modules["task_lifecycle"]["current_surface_refs"],
            mag_retained_authority=pack_modules["task_lifecycle"]["mag_retained_authority"],
        ),
    )
    testcase.assertEqual(
        pack_modules["source_intake_shell"]["active_caller_status"],
        "active_declarative_source_requirements_pack_projection",
    )
    testcase.assertIn("grant_lifecycle_stage", pack_modules["task_lifecycle"]["mag_retained_authority"])

def assert_consumer_thinning_audit_refs_modules(testcase: Any, audit: Mapping[str, Any]) -> None:
    testcase.assertEqual(audit["refs_only_adapter_surfaces"], build_refs_only_adapter_surfaces())
    refs_modules = {
        item["module_id"]: item
        for item in audit["refs_only_adapter_surfaces"]
    }
    testcase.assertEqual(
        set(refs_modules),
        {
            "lifecycle_adapter",
            "observability",
            "domain_handler_product_status_shell",
            "package_lifecycle_shell",
            "human_workbench_scheduler_daemon",
        },
    )
    testcase.assertIn(
        "artifact_package_lifecycle_shell",
        refs_modules["package_lifecycle_shell"]["opl_expected_primitives"],
    )
    testcase.assertEqual(
        refs_modules["domain_handler_product_status_shell"]["active_caller_status"],
        "active_refs_only_domain_domain_handler_adapter",
    )
    testcase.assertIn(
        "src/med_autogrant/product_entry_parts/domain_handler.py",
        refs_modules["domain_handler_product_status_shell"]["code_paths"],
    )

def assert_consumer_thinning_audit_mag_authority_modules(testcase: Any, audit: Mapping[str, Any]) -> None:
    testcase.assertEqual(
        audit["mag_owned_grant_authority_surfaces"],
        build_mag_owned_grant_authority_surfaces(),
    )
    mag_modules = {item["module_id"]: item for item in audit["mag_owned_grant_authority_surfaces"]}
    testcase.assertEqual(
        set(mag_modules),
        {
            "grant_lifecycle_stage",
            "fundability_quality_export_verdicts",
            "package_readiness_submission_ready",
            "grant_transition_oracle",
            "owner_receipt_and_no_regression_evidence",
            "grant_memory_accept_reject",
        },
    )
    testcase.assertEqual(
        mag_modules["package_readiness_submission_ready"]["classification"],
        "minimal_authority_function",
    )
    testcase.assertIn(
        "submission_ready_verdict",
        mag_modules["package_readiness_submission_ready"]["mag_retained_authority"],
    )
    testcase.assertEqual(
        mag_modules["grant_memory_accept_reject"]["active_caller_status"],
        "active_mag_memory_body_decision_keep",
    )
    testcase.assertIn(
        "src/med_autogrant/product_entry_parts/domain_memory_runtime.py",
        mag_modules["grant_memory_accept_reject"]["code_paths"],
    )
    testcase.assertIn(
        "cannot own memory body",
        mag_modules["grant_memory_accept_reject"]["cannot_absorb_reason"],
    )

def assert_consumer_thinning_audit_retired_surfaces(testcase: Any, audit: Mapping[str, Any]) -> None:
    testcase.assertEqual(
        audit["retire_or_tombstone_surfaces"],
        build_retire_or_tombstone_surfaces(),
    )
    retire_modules = {item["module_id"]: item for item in audit["retire_or_tombstone_surfaces"]}
    testcase.assertIn("repo_owned_scheduler_daemon", retire_modules)
    testcase.assertFalse(retire_modules["repo_owned_scheduler_daemon"]["active_caller_allowed"])
    testcase.assertEqual(
        retire_modules["repo_owned_scheduler_daemon"]["active_caller_status"],
        "legacy_scheduler_daemon_absent_runtime_control_is_refs_only_adapter",
    )
    testcase.assertEqual(
        retire_modules["legacy_local_runtime_history_attempt_record"]["active_caller_status"],
        "legacy_local_runtime_history_attempt_record_absent_no_active_caller",
    )
    testcase.assertIn(
        "src/med_autogrant/scheduler_daemon.py:absent",
        retire_modules["repo_owned_scheduler_daemon"]["code_paths"],
    )
    testcase.assertEqual(
        retire_modules["repo_owned_scheduler_daemon"]["exit_gate"],
        build_legacy_exit_gate(
            gate_id="mag.legacy.repo_owned_scheduler_daemon.exit.v1",
            replacement_primitives=[
                "generic_scheduler_daemon",
                "provider_daemon",
                "repair_command_projection",
            ],
            exit_action="delete_or_history_tombstone_repo_owned_scheduler_daemon_surface",
        ),
    )
    testcase.assertEqual(
        retire_modules["domain_runtime_patch_bridge"]["active_caller_status"],
        "retired_physical_facade_removed_no_active_caller",
    )
    testcase.assertEqual(
        retire_modules["domain_runtime_patch_bridge"]["code_paths"],
        ["src/med_autogrant/domain_runtime.py:absent"],
    )
    testcase.assertEqual(
        retire_modules["domain_runtime_patch_bridge"],
        build_retired_functional_module_audit_item(
            "domain_runtime_patch_bridge",
            code_paths=["src/med_autogrant/domain_runtime.py:absent"],
            active_callers=[],
            active_caller_status="retired_physical_facade_removed_no_active_caller",
            migration_action=(
                "Keep only tombstone/provenance; do not add compatibility aliases or "
                "re-export facades."
            ),
            retention_reason="The old domain_runtime facade file is absent from active source.",
            cannot_absorb_reason=(
                "This is retired compatibility glue, not an OPL primitive to absorb."
            ),
            evidence_refs=[
                "docs/decisions.md#2026-05-14：退役-domain-runtime-facade-patch-bridge",
                "tests/test_domain_runtime_split.py::RuntimeSplitStructureTest::test_runtime_patch_target_bridge_is_retired",
                "tests/test_domain_runtime_split.py::RuntimeSplitStructureTest::test_retired_runtime_facade_is_not_present_in_source",
                "tests/test_runtime_cli_structural_helpers.py::test_domain_runtime_parts_do_not_depend_on_facade_patch_bridge",
            ],
        ),
    )
    testcase.assertIn(
        "tests/test_domain_runtime_split.py::RuntimeSplitStructureTest::test_retired_runtime_facade_is_not_present_in_source",
        retire_modules["domain_runtime_patch_bridge"]["evidence_refs"],
    )
    testcase.assertEqual(
        retire_modules["compatibility_only_product_entry_aggregate_test"]["active_caller_status"],
        "legacy_aggregate_test_physically_removed_focused_cases_are_replacement_tests",
    )
    testcase.assertEqual(
        retire_modules["compatibility_only_product_entry_aggregate_test"]["code_paths"],
        ["tests/test_product_entry.py"],
    )
    testcase.assertEqual(
        retire_modules["compatibility_only_product_entry_aggregate_test"]["active_callers"],
        [],
    )
    testcase.assertIn(
        "tests/product_entry_cases/:focused_replacement_tests",
        retire_modules["compatibility_only_product_entry_aggregate_test"]["evidence_refs"],
    )
    testcase.assertEqual(
        audit["mag_thin_adapter_code_surfaces"],
        [
            "product_entry_manifest_builder",
            "domain_handler_guarded_domain_adapter",
            "domain_entry",
            "receipt_schema_and_writer",
            "grant_transition_oracle",
            "refs_only_projection_builders",
            "focused_contract_tests",
        ],
    )
    testcase.assertEqual(
        audit["domain_authority_do_not_retire"],
        [
            "grant_lifecycle_stage",
            "package_readiness_submission_ready",
            "fundability_verdict",
            "authoring_quality_verdict",
            "submission_ready_export_verdict",
            "grant_transition_oracle",
            "owner_receipt",
            "grant_strategy_memory_accept_reject",
        ],
    )
    testcase.assertIn("workspace_source_intake_shell", audit["opl_must_absorb_code_surfaces"])
    testcase.assertIn("generic_scheduler_daemon", audit["opl_must_absorb_code_surfaces"])
    testcase.assertFalse(audit["fail_closed_rules"]["delete_grant_lifecycle_stage_as_generic_lifecycle"])
    testcase.assertFalse(audit["fail_closed_rules"]["delete_package_readiness_as_generic_package_lifecycle"])
    testcase.assertFalse(audit["fail_closed_rules"]["delete_fundability_or_quality_verdict_as_generic_readiness"])

def assert_consumer_thinning_followthrough_gaps(testcase: Any, thinning: Mapping[str, Any]) -> None:
    followthrough = thinning["functional_followthrough_gap_classification"]
    testcase.assertEqual(
        followthrough["surface_kind"],
        "mag_functional_followthrough_gap_classification",
    )
    testcase.assertEqual(
        followthrough["state"],
        "mag_handler_boundary_ready_external_evidence_gated",
    )
    testcase.assertEqual(followthrough["mag_functional_structure_gap_count"], 0)
    testcase.assertEqual(followthrough["remaining_mag_functional_structure_gap_ids"], [])
    testcase.assertEqual(followthrough["remaining_mag_functional_structure_gaps"], [])
    testcase.assertEqual(
        followthrough["closed_classification_surface_ids"],
        [
            "P1_adapter_thinning_and_pack_input",
            "P2_package_export_artifact_lifecycle_handoff",
            "P3_grant_strategy_memory_locator_writeback_handoff",
            "P4_skeleton_generated_surface_and_legacy_retirement",
        ],
    )
    testcase.assertEqual(
        followthrough["reclassified_testing_evidence_gap_ids"],
        [
            "real_workspace_memory_body_migration_and_retrieval_writeback_apply",
            "real_workspace_package_lifecycle_and_cleanup_restore_retention_receipts",
            "opl_generated_surface_production_consumption_no_regression",
            "focused_opl_hosted_receipt_verification",
            "continuous_live_receipt_reconciliation",
            "long_run_live_soak_and_no_forbidden_write_proof",
        ],
    )
    for closed_gap in followthrough["closed_classification_surfaces"]:
        with testcase.subTest(closed_gap=closed_gap["gap_id"]):
            testcase.assertEqual(closed_gap["previous_bucket"], "functional_structure_gap")
            testcase.assertEqual(
                closed_gap["current_bucket"],
                "standard_agent_source_shape_landed",
            )
            testcase.assertEqual(closed_gap["owner"], "med-autogrant")
            testcase.assertTrue(closed_gap["closed_by_refs"])
    testcase.assertEqual(followthrough["external_owner_gates"], [])
    for evidence_gap in followthrough["reclassified_as_testing_evidence_gaps"]:
        with testcase.subTest(evidence_gap=evidence_gap["gap_id"]):
            testcase.assertEqual(evidence_gap["current_bucket"], "production_evidence_tail")
            testcase.assertEqual(evidence_gap["owner"], "evidence_gate")
            testcase.assertTrue(evidence_gap["mag_surface_refs"])
    testcase.assertEqual(followthrough["standard_agent_source_shape_status"], "landed")
    testcase.assertEqual(
        followthrough["current_mag_source_role"],
        "declarative_pack_domain_handler_refs_only_adapter_or_minimal_authority",
    )
    testcase.assertTrue(followthrough["authority_boundary"]["mag_repo_functional_structure_gaps_zero"])
    testcase.assertTrue(followthrough["authority_boundary"]["mag_repo_active_source_shape_landed"])
    testcase.assertTrue(followthrough["authority_boundary"]["classification_closed"])
    testcase.assertFalse(followthrough["authority_boundary"]["followthrough_gaps_open"])
    testcase.assertTrue(followthrough["authority_boundary"]["claims_opl_descriptor_source_available"])
    testcase.assertTrue(followthrough["authority_boundary"]["claims_opl_replacement_exists"])
    testcase.assertFalse(
        followthrough["authority_boundary"]["claims_domain_repo_physical_delete_authorized"]
    )
    testcase.assertFalse(
        followthrough["authority_boundary"]["claims_opl_generated_surface_production_consumed"]
    )
    testcase.assertFalse(followthrough["authority_boundary"]["claims_production_long_run_soak_complete"])

def assert_consumer_thinning_output_guard_and_authority(testcase: Any, thinning: Mapping[str, Any]) -> None:
    output_guard = thinning["thin_surface_output_guard"]
    testcase.assertEqual(output_guard["surface_kind"], "mag_thin_surface_output_guard")
    testcase.assertEqual(
        output_guard["allowed_output_classes"],
        thinning["mag_owned_outputs"],
    )
    testcase.assertEqual(
        output_guard["required_domain_handler_return_refs"],
        thinning["exposed_domain_handler_return_refs"],
    )
    testcase.assertEqual(
        output_guard["private_functional_state_output_classes_forbidden"],
        list(PRIVATE_FUNCTIONAL_STATE_OUTPUT_CLASSES),
    )
    testcase.assertIn("generic_scheduler_state", output_guard["forbidden_output_classes"])
    testcase.assertIn("generic_workbench_state", output_guard["forbidden_output_classes"])
    testcase.assertIn("generic_memory_transport_state", output_guard["forbidden_output_classes"])
    testcase.assertIn("generic_artifact_lifecycle_state", output_guard["forbidden_output_classes"])
    testcase.assertIn("generic_operator_workbench_state", output_guard["forbidden_output_classes"])
    testcase.assertIn("generic_observability_slo_state", output_guard["forbidden_output_classes"])
    for forbidden_state in output_guard["private_functional_state_output_classes_forbidden"]:
        with testcase.subTest(forbidden_state=forbidden_state):
            testcase.assertIn(forbidden_state, output_guard["forbidden_output_classes"])
    testcase.assertIn("family_conflict_envelope_completion_claim", output_guard["forbidden_output_classes"])
    testcase.assertIn("functional_harness_runtime_state", output_guard["forbidden_output_classes"])
    testcase.assertIn("opl_harness_pass_grant_ready", output_guard["forbidden_output_classes"])
    testcase.assertIn("opl_harness_pass_export_ready", output_guard["forbidden_output_classes"])
    testcase.assertIn("grant_artifact_content", output_guard["forbidden_output_classes"])
    testcase.assertIn("memory_body", output_guard["forbidden_output_classes"])
    testcase.assertTrue(output_guard["consumes_opl_replacement_expectations"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_generic_runtime_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_generic_workbench_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_generic_observability_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_private_functional_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_local_attempt_record_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_source_intake_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_package_lifecycle_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_hermes_state_db_runtime_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_family_conflict_completion_claim"])
    testcase.assertFalse(output_guard["authority_boundary"]["mag_can_emit_functional_harness_runtime_state"])
    testcase.assertFalse(output_guard["authority_boundary"]["opl_harness_pass_can_declare_grant_ready"])
    testcase.assertFalse(output_guard["authority_boundary"]["opl_harness_pass_can_declare_export_ready"])
    scaffold_guard = thinning["standard_agent_scaffold_alignment"]
    testcase.assertEqual(
        scaffold_guard["surface_kind"],
        "mag_standard_agent_scaffold_thin_surface_guard",
    )
    testcase.assertFalse(scaffold_guard["knowledge_only_repository"])
    testcase.assertTrue(scaffold_guard["retains_domain_program_surfaces"])
    testcase.assertEqual(scaffold_guard["required_repo_boundaries"], ["agent", "contracts", "runtime", "docs"])
    testcase.assertIn("domain_handler_adapter", scaffold_guard["retained_program_surface_kinds"])
    testcase.assertFalse(scaffold_guard["authority_boundary"]["mag_owns_generic_runtime_framework"])
    testcase.assertFalse(scaffold_guard["authority_boundary"]["mag_is_knowledge_only_repository"])
    authority = thinning["authority_boundary"]
    testcase.assertFalse(authority["opl_can_write_domain_truth"])
    testcase.assertFalse(authority["opl_can_write_memory_body"])
    testcase.assertFalse(authority["opl_can_declare_export_ready"])
    testcase.assertFalse(authority["mag_rebuilds_opl_runtime"])
    testcase.assertFalse(authority["mag_implements_generic_memory_transport"])
    testcase.assertFalse(authority["mag_implements_generic_artifact_gallery"])
    testcase.assertFalse(authority["mag_implements_generic_operator_workbench"])
    testcase.assertFalse(authority["mag_implements_generic_observability_slo"])
    testcase.assertFalse(authority["mag_implements_generic_artifact_lifecycle"])
    testcase.assertFalse(authority["opl_harness_pass_can_declare_grant_ready"])
    testcase.assertFalse(authority["opl_harness_pass_can_declare_export_ready"])

def assert_consumer_thinning_replacement_expectations(testcase: Any, manifest: Mapping[str, Any], thinning: Mapping[str, Any]) -> None:
    testcase.assertEqual(thinning["opl_replacement_expectations"], build_opl_replacement_expectations())
    replacement_ids = {item["primitive_id"] for item in thinning["opl_replacement_expectations"]}
    testcase.assertEqual(
        replacement_ids,
        {
            "workspace_source_intake_shell",
            "memory_locator_writeback_transport",
            "artifact_package_lifecycle_shell",
            "generic_transition_runner",
            "functional_harness_queue_stage_attempt_typed_closeout",
            "functional_harness_restart_dead_letter_repair_human_gate",
            "operator_workbench_drilldown_shell",
            "observability_repair_projection",
            "agent_scaffold_checklist",
        },
    )
    for item in thinning["opl_replacement_expectations"]:
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
