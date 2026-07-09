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
)


def assert_domain_handler_export_maps_runtime_and_attention_surfaces(
    testcase: Any,
    payload: Mapping[str, Any],
    repo_root: Path,
) -> None:
    testcase.assertTrue(payload["ok"])
    testcase.assertEqual(payload["command"], "domain-handler-export")
    export = payload["domain_handler_export"]
    thinning = export["mag_consumer_thinning_contract"]

    assert_path_values(
        testcase,
        export,
        {
            "surface_kind": DOMAIN_HANDLER_EXPORT_KIND,
            "adapter_id": DOMAIN_HANDLER_ADAPTER_ID,
            "caller_owner_contract.active_caller_owner": "med-autogrant",
            "caller_owner_contract.target_caller_owner": "one-person-lab",
            "caller_owner_contract.domain_handler_owner": "med-autogrant",
            "caller_owner_contract.claims_fully_cleaned": False,
            "caller_owner_contract.mag_handler_boundary_ready": True,
            "substrate_boundary.control_plane_owner": "one-person-lab",
            "substrate_boundary.domain_truth_owner": "med-autogrant",
            "runtime_control.surface_kind": "runtime_control",
            "runtime_continuity.surface_kind": "skill_runtime_continuity",
            "standard_domain_agent_skeleton.surface_kind": "standard_domain_agent_skeleton",
            "artifact_locator_contract.surface_kind": "domain_artifact_locator_contract",
            "source_provenance.surface_kind": "source_provenance",
        },
    )
    testcase.assertIn(
        "no_runtime_workbench_ledger_or_scheduler_authority_transferred",
        export["source_provenance"]["authority_boundary"],
    )

    _assert_refs_only_runtime_boundary(testcase, export)
    _assert_consumer_thinning_contract(testcase, export, thinning)
    _assert_generated_handoff_boundary(testcase, export, repo_root)
    _assert_output_and_control_plane_guards(testcase, export, thinning)


def _assert_refs_only_runtime_boundary(testcase: Any, export: Mapping[str, Any]) -> None:
    substrate_adapter = export["opl_substrate_adapter_export"]
    assert_path_values(
        testcase,
        substrate_adapter,
        {
            "surface_kind": "mag_opl_substrate_adapter_export",
            "workspace_ref_index.body_policy": "locator_only_no_workspace_body",
            "source_ref_index.index_policy": "source_refs_only_no_source_body",
            "artifact_ref_index.body_policy": "locator_and_inventory_refs_only_no_package_body",
            "memory_ref_index.body_policy": "locator_and_receipt_refs_only_no_memory_body",
        },
    )
    assert_false_keys(
        testcase,
        substrate_adapter["authority_boundary"],
        ("opl_can_read_package_body", "opl_can_read_memory_body", "opl_can_issue_owner_receipt"),
    )

    hosted_proof = export["controlled_stage_attempt_projection"][
        "opl_hosted_controlled_grant_stage_attempt_proof"
    ]
    assert_path_values(
        testcase,
        hosted_proof,
        {
            "maps_to_opl_contract": "opl_hosted_controlled_stage_attempt_proof.v1",
            "repo_tracked_real_receipt_instance": False,
            "repo_tracked_real_memory_body": False,
        },
    )
    assert_false_keys(
        testcase,
        hosted_proof["authority_boundary"],
        ("opl_can_hold_fundability_verdict", "opl_can_hold_authoring_quality_verdict", "opl_can_hold_export_verdict"),
    )
    testcase.assertEqual(
        export["receipt_refs"],
        export["controlled_stage_attempt_projection"]["receipt_refs"],
    )
    testcase.assertEqual(
        export["memory_receipt_refs"],
        export["controlled_domain_memory_apply_proof"]["writeback_receipt_refs"],
    )
    assert_path_values(
        testcase,
        export["owner_receipt_contract"],
        {
            "surface_kind": "mag_owner_receipt_contract",
            "allowed_return_shapes": ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
        },
    )


def _assert_consumer_thinning_contract(
    testcase: Any,
    export: Mapping[str, Any],
    thinning: Mapping[str, Any],
) -> None:
    assert_path_values(
        testcase,
        thinning,
        {
            "surface_kind": "mag_consumer_thinning_contract",
            "domain_handler_owner": "med-autogrant",
            "state": "mag_handler_boundary_ready_external_caller_evidence_gated",
            "bridge_exit_gate_refs.claims_all_bridge_exits_complete": False,
            "authority_boundary.mag_rebuilds_opl_runtime": False,
        },
    )
    testcase.assertEqual(thinning["forbidden_mag_owned_generic_primitives"], [])
    assert_contains_all(
        testcase,
        thinning["forbidden_mag_generic_owner_roles"],
        (
            "generic_operator_workbench_owner",
            "generic_workspace_source_intake_owner",
            "generic_memory_transport_owner",
            "generic_artifact_gallery_owner",
            "generic_observability_slo_owner",
        ),
    )

    consumed = export["consumed_opl_standard_surfaces"]
    testcase.assertEqual(consumed, thinning["consumed_opl_standard_surfaces"])
    assert_false_keys(
        testcase,
        consumed["authority_boundary"],
        (
            "mag_can_own_generic_memory_transport",
            "mag_can_own_generic_artifact_gallery",
            "mag_can_own_generic_operator_workbench",
            "mag_can_own_generic_observability_slo",
            "opl_harness_pass_can_declare_grant_ready",
            "opl_harness_pass_can_declare_export_ready",
        ),
    )
    assert_contains_all(testcase, consumed["mag_retained_authority"], ("grant_truth", "package_authority"))

    observability = export["opl_runtime_observability_consumption"]
    testcase.assertEqual(observability, thinning["opl_runtime_observability_consumption"])
    assert_path_values(
        testcase,
        observability,
        {
            "consumption_policy": "read_only_refs_and_counts_no_repair_execution",
            "stage_attempt_projection_consumption.provider_completion_is_grant_ready": False,
            "authority_boundary.can_execute_repair": False,
            "authority_boundary.can_authorize_quality_verdict": False,
        },
    )

    coverage = export["functional_harness_consumer_coverage"]
    testcase.assertEqual(coverage, thinning["functional_harness_consumer_coverage"])
    assert_false_keys(
        testcase,
        coverage["fail_closed_rules"],
        (
            "opl_harness_pass_is_grant_ready",
            "opl_harness_pass_is_export_ready",
            "opl_can_hold_generic_runtime_in_mag",
        ),
    )


def _assert_generated_handoff_boundary(
    testcase: Any,
    export: Mapping[str, Any],
    repo_root: Path,
) -> None:
    handoff = export["generated_surface_handoff"]
    bridge_exit = handoff["bridge_exit_gate"]
    assert_path_values(
        testcase,
        bridge_exit,
        {
            "surface_kind": "mag_bridge_exit_gate",
            "replacement_owner": "one-person-lab",
            "domain_handler_owner": "med-autogrant",
            "claims_exit_complete": False,
            "claims_production_long_run_soak_complete": False,
        },
    )
    testcase.assertEqual(
        set(handoff["generated_surface_ids"]),
        {
            "product_status",
            "product_user_loop",
            "domain_handler",
            "grouped_cli_api",
            "projection_builder",
            "lifecycle_wrapper",
        },
    )
    testcase.assertFalse(handoff["authority_boundary"]["generated_surface_can_declare_verdict"])
    testcase.assertEqual(handoff["missing_current_mag_path_count"], 0)
    for surface in handoff["generated_or_bridge_surfaces"]:
        with testcase.subTest(bridge_surface=surface["surface_id"]):
            testcase.assertFalse(surface["bridge_exit_gate"]["claims_exit_complete"])
            testcase.assertEqual(surface["current_mag_path_status"]["status"], "current")
            for path_status in surface["current_mag_path_status"]["paths"]:
                testcase.assertTrue((repo_root / path_status["path"]).is_file())

    testcase.assertEqual(
        {item["function_id"] for item in export["minimal_authority_functions"]},
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
        testcase.assertIn("typed_blocker", authority_function["allowed_return_shapes"])
        testcase.assertIn(
            "mechanical_ready_verdict",
            authority_function["output_boundary"]["forbidden_outputs"],
        )


def _assert_output_and_control_plane_guards(
    testcase: Any,
    export: Mapping[str, Any],
    thinning: Mapping[str, Any],
) -> None:
    output_guard = thinning["thin_surface_output_guard"]
    testcase.assertEqual(output_guard["allowed_output_classes"], thinning["mag_owned_outputs"])
    assert_contains_all(
        testcase,
        output_guard["forbidden_output_classes"],
        (
            "generic_memory_transport_state",
            "generic_artifact_lifecycle_state",
            "generic_observability_slo_state",
            "functional_harness_runtime_state",
            "opl_harness_pass_grant_ready",
            "opl_harness_pass_export_ready",
        ),
    )
    assert_false_keys(
        testcase,
        output_guard["authority_boundary"],
        (
            "mag_can_emit_generic_runtime_state",
            "mag_can_emit_generic_workbench_state",
            "mag_can_emit_generic_observability_state",
            "mag_can_emit_private_functional_state",
            "opl_harness_pass_can_declare_grant_ready",
            "opl_harness_pass_can_declare_export_ready",
        ),
    )

    physical_follow_through = export["physical_skeleton_follow_through"]
    assert_path_values(
        testcase,
        physical_follow_through,
        {
            "surface_kind": "mag_physical_skeleton_follow_through",
            "moves_workspace_artifacts": False,
            "closed_default_path_history_summary.state": "closed_history_index_only",
            "closed_default_path_history_summary.active_source_residue_count": 0,
        },
    )
    testcase.assertEqual(physical_follow_through["forbidden_active_path_residue"], [])
    testcase.assertFalse(export["ideal_state_closure_status"]["claims_production_long_run_soak_complete"])

    wakeup = export["todo_wakeup"]
    testcase.assertEqual(wakeup["opl_wakeup_contract"]["owner"], "one-person-lab")
    testcase.assertEqual(wakeup["opl_wakeup_contract"]["queue_write_policy"], "enqueue_wakeup_only_no_grant_truth_writes")
    testcase.assertNotIn("hermes_wakeup_role", wakeup)
    assert_false_keys(
        testcase,
        export["autonomy_controller"],
        ("mag_long_running_driver", "mag_scheduler_daemon_owner", "mag_attempt_ledger_owner", "hermes_proof_executor_default"),
    )
    testcase.assertEqual(export["opl_control_plane"]["write_policy"], "opl_index_only_no_grant_truth_writes")
