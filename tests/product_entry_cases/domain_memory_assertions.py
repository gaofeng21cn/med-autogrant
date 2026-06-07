from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def assert_domain_memory_descriptor_locator(
    testcase: Any,
    memory_locator: Mapping[str, Any],
    stage_plane: Mapping[str, Any],
) -> None:
    testcase.assertEqual(memory_locator["surface_kind"], "domain_memory_descriptor_locator")
    testcase.assertEqual(memory_locator["descriptor_id"], "mag.domain_memory_descriptor_locator.v1")
    testcase.assertEqual(memory_locator["memory_owner"], "med-autogrant")
    testcase.assertEqual(memory_locator["memory_content_owner"], "med-autogrant")
    testcase.assertEqual(memory_locator["fundability_verdict_owner"], "med-autogrant")
    testcase.assertEqual(memory_locator["policy_ref"]["ref"], "docs/references/grant_strategy_memory_policy.md")
    testcase.assertEqual(memory_locator["memory_locator"]["locator_kind"], "domain_memory_locator")
    testcase.assertFalse(memory_locator["memory_locator"]["repo_tracked"])
    testcase.assertEqual(
        memory_locator["memory_locator"]["content_policy"],
        "locator_only_no_memory_content_in_repo_manifest",
    )
    testcase.assertEqual(
        memory_locator["memory_locator"]["retrieval_policy"],
        "stage_specific_small_relevant_sets",
    )
    migration_plan = memory_locator["migration_plan"]
    testcase.assertEqual(migration_plan["surface_kind"], "domain_memory_migration_plan")
    testcase.assertEqual(migration_plan["plan_id"], "mag.domain_memory_migration_plan.v1")
    testcase.assertEqual(migration_plan["migration_state"], "runtime_apply_contract_landed")
    testcase.assertEqual(
        migration_plan["source_roots"],
        [
            "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/",
            "opl://generated-surfaces/mag/product-entry-session",
            "workspace_root/.mag-domain-memory/writeback-proposals/",
        ],
    )
    testcase.assertEqual(
        migration_plan["seed_fixture_ref"]["ref"],
        "contracts/runtime-program/domain-memory-seed-fixture.json",
    )
    testcase.assertFalse(migration_plan["target_store"]["repo_tracked"])
    testcase.assertEqual(
        [step["step_id"] for step in migration_plan["migration_steps"]],
        ["discover_candidates", "mag_review", "persist_acceptance"],
    )
    testcase.assertIn("no_workspace_private_evidence", migration_plan["acceptance_gates"])
    testcase.assertEqual(migration_plan["pending_runtime_work"], [])
    testcase.assertEqual(
        migration_plan["runtime_apply_surfaces"],
        [
            "writeback_proposal_generator",
            "accept_reject_command",
            "runtime_receipt_evidence_writer",
            "operator_receipt_projection",
        ],
    )
    proposal_generator = memory_locator["writeback_proposal_generator"]
    testcase.assertEqual(proposal_generator["surface_kind"], "domain_memory_writeback_proposal_generator")
    testcase.assertEqual(proposal_generator["output_surface_kind"], "mag_domain_memory_writeback_proposal")
    testcase.assertEqual(proposal_generator["write_policy"], "runtime_store_only_no_repo_write")
    accept_reject = memory_locator["accept_reject_command"]
    testcase.assertEqual(accept_reject["surface_kind"], "domain_memory_accept_reject_command")
    testcase.assertEqual(accept_reject["decision_owner"], "med-autogrant")
    testcase.assertTrue(accept_reject["requires_mag_decision_before_store_mutation"])
    receipt_writer = memory_locator["runtime_receipt_evidence_writer"]
    testcase.assertEqual(receipt_writer["surface_kind"], "domain_memory_runtime_receipt_evidence_writer")
    testcase.assertEqual(receipt_writer["output_surface_kind"], "mag_domain_memory_runtime_receipt_evidence")
    testcase.assertEqual(receipt_writer["write_policy"], "runtime_receipt_instance_only_no_repo_write")
    operator_receipt = memory_locator["operator_receipt_projection"]
    testcase.assertEqual(operator_receipt["surface_kind"], "mag_domain_memory_operator_receipt_projection")
    testcase.assertEqual(
        operator_receipt["receipt_content_policy"],
        "receipt_refs_and_decision_metadata_only_no_memory_body",
    )
    testcase.assertFalse(operator_receipt["opl_consumption"]["can_hold_memory_content"])
    controlled_fixture = memory_locator["controlled_apply_fixture"]
    testcase.assertTrue(controlled_fixture["direct_skill_and_opl_hosted_use_same_refs"])
    testcase.assertFalse(controlled_fixture["opl_verdict_authority"]["fundability"])
    testcase.assertFalse(controlled_fixture["opl_verdict_authority"]["submission_ready_export"])
    testcase.assertEqual(
        [ref["stage_id"] for ref in memory_locator["stage_descriptor_refs"]],
        [stage["stage_id"] for stage in stage_plane["stages"]],
    )
    testcase.assertIn(
        "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/",
        memory_locator["writeback_receipt_refs"]["memory_writeback_receipt_ref"],
    )
    testcase.assertEqual(
        memory_locator["writeback_receipt_refs"]["receipt_write_policy"],
        "receipt_ref_only_no_domain_memory_content_mutation",
    )
    receipt_locator = memory_locator["receipt_locator"]
    testcase.assertEqual(receipt_locator["surface_kind"], "domain_memory_receipt_locator")
    testcase.assertEqual(receipt_locator["locator_id"], "mag.domain_memory_receipt_locator.v1")
    testcase.assertEqual(
        receipt_locator["receipt_content_policy"],
        "locator_and_decision_metadata_only_no_memory_body",
    )
    testcase.assertFalse(receipt_locator["repo_tracked"])
    testcase.assertFalse(memory_locator["opl_consumption_contract"]["can_hold_memory_content"])
    testcase.assertFalse(memory_locator["opl_consumption_contract"]["can_issue_fundability_verdict"])
    testcase.assertFalse(memory_locator["opl_consumption_contract"]["can_issue_authoring_quality_verdict"])
    testcase.assertFalse(memory_locator["opl_consumption_contract"]["can_issue_export_verdict"])
    testcase.assertFalse(memory_locator["opl_consumption_contract"]["can_mutate_domain_memory_store"])
    for forbidden_memory_role in (
        "memory_content",
        "fundability_verdict",
        "authoring_quality_verdict",
        "submission_ready_export_verdict",
        "canonical_grant_artifact_content",
    ):
        testcase.assertIn(forbidden_memory_role, memory_locator["opl_consumption_contract"]["does_not_consume"])
    testcase.assertEqual(
        memory_locator["authority_boundary"]["opl_role"],
        "memory_locator_ref_and_receipt_ref_consumer_only",
    )


def assert_generated_surface_handoff(
    testcase: Any,
    thinning: Mapping[str, Any],
    repo_root: Path,
) -> None:
    generated_handoff = thinning["generated_surface_handoff"]
    testcase.assertEqual(generated_handoff["surface_kind"], "mag_generated_surface_handoff")
    testcase.assertEqual(generated_handoff["owner"], "med-autogrant")
    testcase.assertEqual(generated_handoff["target_generator_owner"], "one-person-lab")
    testcase.assertEqual(generated_handoff["active_caller_owner"], "med-autogrant")
    testcase.assertEqual(generated_handoff["domain_handler_target"], "med-autogrant")
    testcase.assertEqual(generated_handoff["domain_handler_owner"], "med-autogrant")
    testcase.assertEqual(
        generated_handoff["bridge_exit_gate"]["gate_status"],
        "mag_handler_boundary_ready_external_caller_evidence_required",
    )
    testcase.assertIn(
        "no_active_legacy_wrapper_caller_scan",
        generated_handoff["bridge_exit_gate"]["required_evidence"],
    )
    testcase.assertFalse(generated_handoff["bridge_exit_gate"]["claims_exit_complete"])
    testcase.assertFalse(
        generated_handoff["bridge_exit_gate"]["claims_production_long_run_soak_complete"]
    )
    testcase.assertEqual(
        generated_handoff["bridge_exit_gate"]["production_soak_gate_status"],
        "external_live_soak_and_caller_evidence_not_claimed_by_mag_repo",
    )
    testcase.assertEqual(
        generated_handoff["generated_surface_ids"],
        [
            "product_status",
            "product_user_loop",
            "domain_handler",
            "grouped_cli_api",
            "projection_builder",
            "lifecycle_wrapper",
        ],
    )
    testcase.assertEqual(
        generated_handoff["current_mag_path_status"]["surface_kind"],
        "mag_generated_surface_handoff_currentness_proof",
    )
    testcase.assertEqual(generated_handoff["current_mag_path_status"]["status"], "current")
    testcase.assertEqual(generated_handoff["missing_current_mag_path_count"], 0)
    testcase.assertEqual(
        generated_handoff["current_mag_path_status"]["missing_current_mag_path_count"],
        0,
    )
    testcase.assertEqual(
        generated_handoff["stale_path_policy"],
        "history_or_source_ref_refresh_only",
    )
    testcase.assertTrue(generated_handoff["current_mag_path_status"]["claims_opl_replacement_exists"])
    testcase.assertFalse(
        generated_handoff["current_mag_path_status"][
            "claims_domain_repo_physical_delete_authorized"
        ]
    )
    testcase.assertFalse(generated_handoff["current_mag_path_status"]["claims_all_bridge_exits_complete"])
    testcase.assertFalse(
        generated_handoff["current_mag_path_status"]["claims_production_long_run_soak_complete"]
    )
    testcase.assertEqual(generated_handoff["mag_long_term_owner_surface_ids"], [])
    for surface in generated_handoff["generated_or_bridge_surfaces"]:
        with testcase.subTest(generated_surface=surface["surface_id"]):
            testcase.assertEqual(
                surface["surface_status"],
                "mag_handler_ref_only_adapter_waiting_for_opl_generated_or_hosted_caller_evidence",
            )
            testcase.assertEqual(surface["active_caller_owner"], "med-autogrant")
            testcase.assertEqual(surface["current_owner"], "med-autogrant")
            testcase.assertEqual(surface["target_owner"], "one-person-lab")
            testcase.assertEqual(surface["domain_handler_target"], "med-autogrant")
            testcase.assertEqual(surface["domain_handler_owner"], "med-autogrant")
            testcase.assertEqual(
                surface["bridge_exit_gate"]["gate_status"],
                "mag_handler_boundary_ready_external_caller_evidence_required",
            )
            testcase.assertFalse(surface["bridge_exit_gate"]["claims_exit_complete"])
            testcase.assertFalse(surface["bridge_exit_gate"]["claims_production_long_run_soak_complete"])
            testcase.assertTrue(surface["generated_by_opl_in_target"])
            testcase.assertFalse(surface["current_mag_long_term_owner"])
            testcase.assertFalse(surface["keeps_mag_authority_functions"])
            testcase.assertEqual(surface["current_mag_path_status"]["status"], "current")
            testcase.assertEqual(surface["missing_current_mag_path_count"], 0)
            testcase.assertEqual(surface["current_mag_path_status"]["missing_count"], 0)
            testcase.assertEqual(
                surface["stale_path_policy"],
                "history_or_source_ref_refresh_only",
            )
            for path_status in surface["current_mag_path_status"]["paths"]:
                testcase.assertTrue(path_status["exists"])
                testcase.assertTrue((repo_root / path_status["path"]).is_file())
    testcase.assertFalse(generated_handoff["authority_boundary"]["mag_long_term_owner"])
    testcase.assertFalse(generated_handoff["authority_boundary"]["generated_surface_can_sign_owner_receipt"])
    testcase.assertFalse(generated_handoff["authority_boundary"]["generated_surface_can_declare_verdict"])
