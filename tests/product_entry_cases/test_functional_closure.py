from __future__ import annotations

import tempfile
from pathlib import Path

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryFunctionalClosureTest(unittest.TestCase):
    def test_manifest_exposes_mag_owner_receipt_contract_for_opl_ref_only_consumption(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]

        contract = manifest["owner_receipt_contract"]
        self.assertEqual(contract["surface_kind"], "mag_owner_receipt_contract")
        self.assertEqual(contract["contract_id"], "mag.owner_receipt.contract.v1")
        self.assertEqual(contract["target_domain_id"], "med-autogrant")
        self.assertEqual(contract["receipt_owner"], "med-autogrant")
        self.assertEqual(contract["maps_to_opl_contract"], "opl_domain_owner_receipt_envelope.v1")
        self.assertEqual(
            contract["allowed_return_shapes"],
            ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
        )
        self.assertEqual(
            contract["receipt_ref_templates"]["stage_attempt_receipt_ref"],
            manifest["controlled_stage_attempt_projection"]["receipt_refs"]["stage_attempt_receipt_ref"],
        )
        self.assertFalse(contract["forbidden_write_proof"]["opl_can_write_grant_truth"])
        self.assertFalse(contract["forbidden_write_proof"]["opl_can_write_grant_artifacts"])
        self.assertFalse(contract["forbidden_write_proof"]["opl_can_hold_fundability_verdict"])
        self.assertIn(
            "/product_entry_manifest/owner_receipt_contract",
            manifest["controlled_stage_attempt_projection"]["owner_receipt_contract_ref"],
        )
        self.assertEqual(
            manifest["controlled_soak_no_regression_attempt"]["owner_receipt_contract_ref"],
            "/product_entry_manifest/owner_receipt_contract",
        )

    def test_manifest_exposes_accept_reject_domain_memory_receipt_fixtures_without_memory_body(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        proof = payload["product_entry_manifest"]["controlled_domain_memory_apply_proof"]

        fixtures = proof["controlled_receipt_instances"]
        self.assertEqual(fixtures["surface_kind"], "mag_domain_memory_controlled_receipt_instances")
        self.assertEqual(fixtures["state"], "runtime_receipt_evidence_path_verified")
        self.assertFalse(fixtures["repo_tracked_real_receipt_instance"])
        self.assertTrue(fixtures["runtime_receipt_instance_writable"])
        self.assertFalse(fixtures["contains_memory_body"])
        self.assertFalse(fixtures["contains_quality_or_export_verdict"])
        self.assertEqual(fixtures["accepted_receipt"]["decision"], "accepted")
        self.assertEqual(fixtures["rejected_receipt"]["decision"], "rejected")
        self.assertIsNotNone(fixtures["accepted_receipt"]["accepted_memory_ref"])
        self.assertIn("domain-memory/accepted-strategy-context-fixture.json", fixtures["accepted_receipt_instance_ref"])
        self.assertIsNone(fixtures["accepted_receipt"]["rejected_memory_ref"])
        self.assertIsNone(fixtures["rejected_receipt"]["accepted_memory_ref"])
        self.assertIsNotNone(fixtures["rejected_receipt"]["rejected_memory_ref"])
        self.assertIn("domain-memory/rejected-strategy-context-fixture.json", fixtures["rejected_receipt_instance_ref"])
        self.assertEqual(
            fixtures["missing_receipt_blocker"]["blocker_kind"],
            "domain_memory_owner_receipt_required",
        )
        self.assertEqual(fixtures["missing_receipt_blocker"]["owner"], "med-autogrant")
        self.assertFalse(fixtures["missing_receipt_blocker"]["opl_can_synthesize_receipt"])

    def test_manifest_exposes_lifecycle_guarded_apply_proof_for_cleanup_restore_retention(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]
        proof = manifest["lifecycle_guarded_apply_proof"]

        self.assertEqual(proof["surface_kind"], "mag_lifecycle_guarded_apply_proof")
        self.assertEqual(proof["proof_id"], "mag.lifecycle.guarded_apply.proof.v1")
        self.assertEqual(proof["target_domain_id"], "med-autogrant")
        self.assertEqual(proof["owner_receipt_contract_ref"], "/product_entry_manifest/owner_receipt_contract")
        self.assertEqual(
            [operation["operation"] for operation in proof["operations"]],
            ["cleanup", "restore", "retention"],
        )
        for operation in proof["operations"]:
            with self.subTest(operation=operation["operation"]):
                self.assertEqual(operation["opl_apply_scope"], "opl_owned_ledger_and_locator_only")
                self.assertEqual(operation["domain_mutation_policy"], "requires_mag_owner_receipt")
                self.assertEqual(operation["artifact_mutation_authority"], "med-autogrant")
                self.assertEqual(
                    operation["typed_blocker"]["blocker_kind"],
                    "mag_domain_artifact_owner_receipt_required",
                )
                self.assertFalse(operation["typed_blocker"]["opl_can_execute_domain_artifact_mutation"])
        self.assertFalse(proof["authority_boundary"]["opl_can_delete_grant_artifacts"])
        self.assertFalse(proof["authority_boundary"]["opl_can_restore_grant_artifacts"])
        self.assertFalse(proof["authority_boundary"]["opl_can_set_retention_for_grant_truth"])

    def test_owner_receipt_evidence_writer_persists_no_regression_receipt_without_domain_writes(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            payload = MedAutoGrantProductEntry().write_owner_receipt_evidence(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-stage-attempt://attempt-1",
                closeout_summary="Controlled OPL-hosted attempt reused MAG refs without mutating grant truth.",
                runtime_root=tmp_dir,
                receipt_id="attempt-1",
            )
            receipt = payload["owner_receipt_evidence"]
            receipt_path = Path(receipt["receipt_instance_ref"])
            receipt_exists = receipt_path.exists()

        self.assertEqual(payload["command"], "owner-receipt-evidence")
        self.assertEqual(receipt["surface_kind"], "mag_owner_receipt_evidence")
        self.assertEqual(receipt["state"], "runtime_receipt_instance_written")
        self.assertEqual(receipt["receipt_shape"], "no_regression_evidence")
        self.assertEqual(receipt["stage_id"], "review_and_rebuttal")
        self.assertTrue(receipt_exists)
        self.assertFalse(receipt["repo_tracked"])
        self.assertFalse(receipt["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(receipt["forbidden_write_proof"]["memory_body_written"])
        self.assertFalse(receipt["forbidden_write_proof"]["submission_ready_export_verdict_written"])
        self.assertTrue(receipt["opl_consumption"]["consumes_receipt_ref_only"])
        self.assertIn(
            "/product_entry_manifest/controlled_stage_attempt_projection",
            receipt["source_refs"],
        )

    def test_lifecycle_receipt_evidence_writer_persists_guarded_apply_receipt_without_artifact_mutation(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            payload = MedAutoGrantProductEntry().write_lifecycle_receipt_evidence(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                operation="cleanup",
                receipt_shape="typed_blocker",
                source_ref="opl-lifecycle://cleanup/attempt-1",
                closeout_summary="Cleanup request requires MAG owner receipt before artifact mutation.",
                runtime_root=tmp_dir,
                receipt_id="cleanup-blocker-1",
            )
            receipt = payload["lifecycle_receipt_evidence"]
            receipt_path = Path(receipt["receipt_instance_ref"])
            receipt_exists = receipt_path.exists()

        self.assertEqual(payload["command"], "lifecycle-receipt-evidence")
        self.assertEqual(receipt["surface_kind"], "mag_lifecycle_receipt_evidence")
        self.assertEqual(receipt["state"], "runtime_receipt_instance_written")
        self.assertEqual(receipt["operation"], "cleanup")
        self.assertEqual(receipt["receipt_shape"], "typed_blocker")
        self.assertTrue(receipt_exists)
        self.assertFalse(receipt["repo_tracked"])
        self.assertEqual(receipt["artifact_mutation"], "none")
        self.assertEqual(receipt["lifecycle_mutation"], "receipt_metadata_only")
        self.assertFalse(receipt["forbidden_write_proof"]["grant_artifact_written"])
        self.assertFalse(receipt["forbidden_write_proof"]["memory_body_written"])
        self.assertTrue(receipt["opl_consumption"]["consumes_receipt_ref_only"])

    def test_manifest_exposes_physical_skeleton_follow_through_with_repo_source_anchors(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]
        follow_through = manifest["physical_skeleton_follow_through"]
        audit = manifest["controlled_domain_memory_apply_proof"]["repo_source_layout_audit"]

        self.assertEqual(follow_through["surface_kind"], "mag_physical_skeleton_follow_through")
        self.assertEqual(follow_through["state"], "declarative_grant_pack_landed")
        self.assertEqual(audit["layout_state"], "declarative_grant_pack_follow_through_landed")
        agent_root = follow_through["roots"]["agent"]
        self.assertEqual(agent_root["state"], "declarative_grant_pack_present")
        self.assertEqual(agent_root["anchor_ref"], "agent/prompts/call_and_candidate_intake.md")
        self.assertEqual(agent_root["canonical_semantic_pack_root"], "agent/")
        self.assertEqual(agent_root["canonical_semantic_pack_role"], "repo_source_declarative_grant_pack")
        self.assertIn("agent/prompts/fundability_strategy.md", agent_root["required_pack_refs"])
        self.assertIn("agent/README.md", agent_root["human_readable_provenance_refs"])
        self.assertTrue(
            next(entry for entry in follow_through["root_status"] if entry["root"] == "agent")[
                "required_pack_refs_exist"
            ]
        )
        self.assertIn("agent/README.md", follow_through["human_readable_provenance_refs"])
        self.assertIn("current machine anchors", follow_through["human_readable_provenance_policy"])
        self.assertFalse(follow_through["moves_workspace_artifacts"])
        self.assertFalse(follow_through["moves_runtime_receipt_instances"])
        self.assertEqual(follow_through["legacy_active_path_policy"], "physically_removed_or_history_tombstone_only")
        self.assertEqual(
            follow_through["active_path_scan_no_legacy_default_caller_ref"],
            "/product_entry_manifest/physical_skeleton_follow_through/"
            "active_path_scan_no_legacy_default_caller",
        )
        active_path_scan = follow_through["active_path_scan_no_legacy_default_caller"]
        self.assertEqual(active_path_scan["surface_kind"], "mag_active_path_scan_no_legacy_default_caller")
        self.assertEqual(active_path_scan["state"], "passed")
        self.assertTrue(active_path_scan["no_legacy_default_caller"])
        self.assertGreater(active_path_scan["scanned_file_count"], 0)
        self.assertEqual(active_path_scan["forbidden_default_caller_matches"], [])
        self.assertFalse(active_path_scan["claims_production_long_run_soak_complete"])
        self.assertTrue(active_path_scan["authority_boundary"]["proves_repo_local_active_machine_surface_only"])
        self.assertFalse(active_path_scan["authority_boundary"]["proves_opl_hosted_production_soak"])
        self.assertFalse(active_path_scan["authority_boundary"]["proves_grant_quality_or_export_readiness"])
        self.assertFalse(active_path_scan["authority_boundary"]["opl_can_write_domain_truth"])
        self.assertFalse(active_path_scan["authority_boundary"]["opl_can_declare_export_ready"])
        self.assertEqual(
            {entry["path"]: entry["state"] for entry in active_path_scan["retired_surface_path_status"]},
            {
                "tests/test_product_entry.py": "absent",
                "src/med_autogrant/domain_runtime_parts/patch_targets.py": "absent",
                "src/med_autogrant/gateway.py": "absent",
                "src/med_autogrant/local_manager.py": "absent",
                "src/med_autogrant/" + "host" + "_agent.py": "absent",
            },
        )
        self.assertEqual(audit["retired_active_path_policy"], "physically_removed_or_history_tombstone_only")
        self.assertEqual(audit["forbidden_active_path_residue"], [])
        residue_states = {entry["path_family"]: entry["state"] for entry in audit["legacy_active_path_residue"]}
        self.assertEqual(residue_states["default Hermes active path"], "tombstone_only")
        self.assertEqual(residue_states["default Gateway active path"], "physically_removed_from_active_source")
        self.assertEqual(residue_states["default local-manager active path"], "physically_removed_from_active_source")
        for root_key, root in follow_through["roots"].items():
            with self.subTest(root=root_key):
                self.assertTrue((REPO_ROOT / root["anchor_ref"]).exists())
                self.assertEqual(root["owner"], "med-autogrant")
        for ref_status in audit["source_ref_status"]:
            with self.subTest(source_ref=ref_status["path"]):
                self.assertFalse(ref_status["path"].endswith("/README.md"))
                self.assertTrue(ref_status["exists"])
                self.assertTrue((REPO_ROOT / ref_status["path"]).exists())

    def test_manifest_exposes_ideal_state_closure_status_without_claiming_live_soak(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]

        closure_status = manifest["ideal_state_closure_status"]
        self.assertEqual(closure_status["surface_kind"], "mag_ideal_state_closure_status")
        self.assertEqual(closure_status["state"], "repo_closure_landed_external_evidence_gated")
        self.assertEqual(closure_status["plan_ref"], "docs/active/mag-ideal-state-cross-repo-gap-plan.md")
        self.assertEqual(closure_status["owner"], "med-autogrant")
        self.assertFalse(closure_status["claims_production_long_run_soak_complete"])
        self.assertFalse(closure_status["authority_boundary"]["opl_can_write_domain_truth"])
        self.assertFalse(closure_status["authority_boundary"]["opl_can_write_memory_body"])
        self.assertFalse(closure_status["authority_boundary"]["opl_can_declare_export_ready"])
        transition_oracle = closure_status["mag_owned_transition_oracle"]
        self.assertEqual(
            transition_oracle["surface_kind"],
            "mag_grant_transition_oracle",
        )
        self.assertEqual(transition_oracle["state"], "domain_spec_landed_external_runner_gate")
        self.assertEqual(transition_oracle["runner_owner"], "one-person-lab")
        self.assertEqual(transition_oracle["oracle_fixture_status"], "landed")
        self.assertEqual(transition_oracle["transition_table_status"], "landed")
        self.assertEqual(transition_oracle["validation"]["status"], "ready_for_opl_runner_ingestion")
        self.assertGreaterEqual(transition_oracle["validation"]["transition_count"], 6)
        self.assertGreaterEqual(transition_oracle["validation"]["oracle_fixture_count"], 6)
        self.assertFalse(transition_oracle["authority_boundary"]["opl_can_infer_submission_ready_export_ready"])
        self.assertIn(
            "review_closed_to_package_and_submit_ready",
            {transition["transition_id"] for transition in transition_oracle["transition_table"]},
        )
        direct_retirement = closure_status["direct_retirement_posture"]
        self.assertEqual(direct_retirement["state"], "active")
        self.assertEqual(
            direct_retirement["policy"],
            "migrate_active_callers_then_delete_or_history_tombstone",
        )
        self.assertIn("facade patch bridge", direct_retirement["forbidden_compatibility_surfaces"])
        self.assertEqual(
            direct_retirement["active_path_scan_no_legacy_default_caller_ref"],
            "/product_entry_manifest/physical_skeleton_follow_through/"
            "active_path_scan_no_legacy_default_caller",
        )
        phase_states = {phase["phase_id"]: phase["state"] for phase in closure_status["phases"]}
        self.assertEqual(
            phase_states,
            {
                "P0": "landed",
                "P1": "mag_adapter_thinning_contract_landed_external_opl_replacement_gate",
                "P2": "external_opl_package_lifecycle_shell_gate",
                "P3": "runtime_workspace_evidence_gate",
                "P4": "landed_with_external_scaffold_template_handoff_gate",
                "P5": "external_evidence_gate",
                "P6": "production_soak_gate",
            },
        )
        p1 = next(phase for phase in closure_status["phases"] if phase["phase_id"] == "P1")
        self.assertEqual(
            p1["required_evidence_refs"],
            [
                "mag_consumer_thinning_contract_ref",
                "sidecar_refs_only_projection_ref",
                "opl_generic_primitive_replacement_contract_ref",
            ],
        )
        self.assertIn(
            "/product_entry_manifest/mag_consumer_thinning_contract",
            p1["mag_surface_refs"],
        )
        p3 = next(phase for phase in closure_status["phases"] if phase["phase_id"] == "P3")
        self.assertIn(
            "mag_runtime_memory_body_migration_ref",
            p3["required_evidence_refs"],
        )
        p6 = next(phase for phase in closure_status["phases"] if phase["phase_id"] == "P6")
        self.assertIn("long_run_soak_no_forbidden_write_proof_ref", p6["required_evidence_refs"])
        self.assertTrue(closure_status["repo_source_exclusions"]["memory_body"])
        self.assertTrue(closure_status["repo_source_exclusions"]["runtime_receipt_instances"])

    def test_manifest_exposes_consumer_thinning_contract_for_opl_replacement_handoff(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]

        thinning = manifest["mag_consumer_thinning_contract"]
        self.assertEqual(thinning["surface_kind"], "mag_consumer_thinning_contract")
        self.assertEqual(thinning["contract_id"], "mag.consumer_thinning.contract.v1")
        self.assertEqual(thinning["target_domain_id"], "med-autogrant")
        self.assertEqual(thinning["owner"], "med-autogrant")
        self.assertEqual(thinning["adapter_role"], "domain_authority_pack_with_thin_program_surface")
        self.assertEqual(thinning["active_caller_owner"], "med-autogrant")
        self.assertEqual(
            thinning["active_caller_surface"],
            "mag_direct_domain_entry_until_opl_caller_evidence",
        )
        self.assertEqual(thinning["domain_handler_target"], "med-autogrant")
        self.assertEqual(thinning["domain_handler_owner"], "med-autogrant")
        self.assertEqual(thinning["state"], "mag_handler_boundary_ready_external_caller_evidence_gated")
        self.assertFalse(thinning["claims_opl_replacement_exists"])
        self.assertFalse(thinning["claims_production_long_run_soak_complete"])
        self.assertEqual(
            thinning["allowed_return_shapes"],
            ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
        )
        self.assertEqual(
            thinning["bridge_exit_gate_refs"]["legacy_exit_gate_policy"],
            "delete_or_history_tombstone_after_replacement_proof",
        )
        self.assertFalse(thinning["bridge_exit_gate_refs"]["claims_all_bridge_exits_complete"])
        self.assertTrue(thinning["bridge_exit_gate_refs"]["mag_handler_boundary_ready"])
        self.assertEqual(
            set(thinning["mag_owned_outputs"]),
            {
                "grant_owned_refs",
                "owner_receipt",
                "typed_blocker",
                "verdict_refs",
                "domain_action_metadata",
            },
        )
        self.assertEqual(thinning["forbidden_mag_owned_generic_primitives"], [])
        self.assertEqual(
            thinning["forbidden_mag_generic_owner_roles"],
            [
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
            ],
        )
        consumed = thinning["consumed_opl_standard_surfaces"]
        self.assertEqual(consumed["surface_kind"], "mag_consumed_opl_standard_surfaces")
        self.assertEqual(
            consumed["consumption_policy"],
            "consume_opl_standard_scaffold_and_generic_primitives_no_mag_runtime_rebuild",
        )
        self.assertEqual(
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
        self.assertEqual(
            consumed["consumed_projection_surfaces"],
            [
                "family_conflict_envelope",
                "stage_attempt_usage_projection",
                "stage_attempt_control_loop_projection",
                "runtime_observability_export",
                "family_product_operator_projection",
            ],
        )
        self.assertEqual(
            consumed["functional_harness_consumer_coverage_ref"],
            "/product_entry_manifest/mag_consumer_thinning_contract/"
            "functional_harness_consumer_coverage",
        )
        self.assertEqual(
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
        self.assertTrue(consumed["authority_boundary"]["mag_consumes_standard_scaffold"])
        self.assertTrue(consumed["authority_boundary"]["mag_consumes_generic_primitives"])
        self.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_memory_transport"])
        self.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_artifact_gallery"])
        self.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_operator_workbench"])
        self.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_observability_slo"])
        self.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_artifact_lifecycle"])
        self.assertFalse(consumed["authority_boundary"]["opl_harness_pass_can_declare_grant_ready"])
        self.assertFalse(consumed["authority_boundary"]["opl_harness_pass_can_declare_export_ready"])
        conflict_projection = thinning["opl_family_conflict_blocker_projection"]
        self.assertEqual(conflict_projection["envelope_kind"], "opl_conflict_or_blocker.v1")
        self.assertEqual(conflict_projection["projection_policy"], "typed_blocker_only_no_fallback_completion")
        self.assertIn("receipt_conflict", conflict_projection["allowed_classifications"])
        self.assertIn("provider_completion_is_domain_ready", conflict_projection["forbidden_claims"])
        self.assertFalse(conflict_projection["authority_boundary"]["provider_completion_is_domain_ready"])
        self.assertFalse(conflict_projection["authority_boundary"]["can_fallback_complete"])
        observability = thinning["opl_runtime_observability_consumption"]
        self.assertEqual(observability["observability_export_kind"], "opl_runtime_observability_export")
        self.assertEqual(observability["consumption_policy"], "read_only_refs_and_counts_no_repair_execution")
        self.assertIn("stage_attempt_usage_projection", observability["consumed_opl_surfaces"])
        self.assertIn("stage_attempt_control_loop_projection", observability["consumed_opl_surfaces"])
        self.assertIn("runtime_observability_export", observability["consumed_opl_surfaces"])
        self.assertIn("safe_action_refs", observability["mag_provides_refs"])
        stage_projection = observability["stage_attempt_projection_consumption"]
        self.assertFalse(stage_projection["mag_can_schedule_retry_dead_letter"])
        self.assertFalse(stage_projection["mag_can_write_opl_stage_attempt_ledger"])
        self.assertFalse(stage_projection["provider_completion_is_grant_ready"])
        self.assertFalse(observability["authority_boundary"]["can_execute_repair"])
        self.assertFalse(observability["authority_boundary"]["can_authorize_artifact_export"])
        coverage = thinning["functional_harness_consumer_coverage"]
        self.assertEqual(coverage["surface_kind"], "mag_functional_harness_consumer_coverage")
        self.assertEqual(coverage["owner"], "med-autogrant")
        self.assertEqual(coverage["harness_owner"], "one-person-lab")
        self.assertEqual(coverage["adapter_role"], "domain_authority_pack_consumer_only")
        self.assertFalse(coverage["claims_opl_functional_harness_pass"])
        self.assertFalse(coverage["claims_grant_ready"])
        self.assertFalse(coverage["claims_export_ready"])
        self.assertEqual(
            coverage["coverage_chain_ids"],
            [
                "memory_refs_only_writeback_chain",
                "queue_stage_attempt_typed_closeout_chain",
                "generic_transition_runner_chain",
                "restart_dead_letter_repair_human_gate_chain",
            ],
        )
        self.assertEqual(
            {chain["chain_id"] for chain in coverage["coverage_chains"]},
            set(coverage["coverage_chain_ids"]),
        )
        self.assertEqual(
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
                "sidecar_projection_adapter",
            },
        )
        self.assertFalse(coverage["fail_closed_rules"]["opl_harness_pass_is_grant_ready"])
        self.assertFalse(coverage["fail_closed_rules"]["opl_harness_pass_is_export_ready"])
        self.assertFalse(coverage["fail_closed_rules"]["opl_can_hold_generic_runtime_in_mag"])
        for chain in coverage["coverage_chains"]:
            with self.subTest(chain=chain["chain_id"]):
                self.assertEqual(chain["mag_role"], "consumer_domain_authority_pack")
                self.assertFalse(chain["implemented_in_mag"])
                self.assertFalse(chain["mag_claims_generic_runtime_owner"])
                self.assertEqual(chain["harness_owner"], "one-person-lab")
                self.assertFalse(chain["fail_closed_boundary"]["harness_pass_can_set_grant_ready"])
                self.assertFalse(chain["fail_closed_boundary"]["harness_pass_can_set_export_ready"])
                self.assertFalse(chain["fail_closed_boundary"]["opl_can_write_grant_truth"])
            self.assertFalse(chain["fail_closed_boundary"]["opl_can_write_memory_body"])
            self.assertTrue(chain["fail_closed_boundary"]["mag_owner_receipt_required"])
        route_stage_boundary = thinning["route_stage_handoff_boundary"]
        self.assertEqual(
            route_stage_boundary["surface_kind"],
            "mag_route_stage_handoff_boundary",
        )
        self.assertFalse(route_stage_boundary["route_is_stage"])
        self.assertEqual(route_stage_boundary["route_semantics_owner"], "med-autogrant")
        self.assertEqual(route_stage_boundary["domain_truth_owner"], "med-autogrant")
        self.assertEqual(route_stage_boundary["stage_graph_owner"], "one-person-lab")
        self.assertEqual(route_stage_boundary["stage_lifecycle_owner"], "one-person-lab")
        self.assertEqual(route_stage_boundary["runtime_transition_owner"], "one-person-lab")
        self.assertEqual(route_stage_boundary["queue_attempt_owner"], "one-person-lab")
        self.assertTrue(route_stage_boundary["opl_hydrates_route_refs_to_queue_and_stage_attempts"])
        self.assertFalse(route_stage_boundary["mag_owns_inter_route_scheduler"])
        self.assertEqual(
            route_stage_boundary["stage_graph_ref"],
            "/product_entry_manifest/family_stage_control_plane",
        )
        self.assertEqual(
            route_stage_boundary["route_oracle_ref"],
            "/product_entry_manifest/grant_transition_oracle",
        )
        self.assertIn("owner_receipt_ref", route_stage_boundary["allowed_handoff_refs"])
        self.assertIn("generic_runtime_state", route_stage_boundary["forbidden_payload_classes"])
        self.assertFalse(route_stage_boundary["authority_boundary"]["opl_can_write_grant_truth"])
        self.assertFalse(
            route_stage_boundary["authority_boundary"]["opl_can_declare_export_verdict"]
        )
        self.assertFalse(
            route_stage_boundary["authority_boundary"][
                "mag_implements_generic_route_scheduler"
            ]
        )
        self.assertIn("route_is_stage", route_stage_boundary["forbidden_claims"])
        self.assertEqual(
            thinning["exposed_sidecar_return_refs"]["route_stage_handoff_boundary_ref"],
            "/product_entry_manifest/mag_consumer_thinning_contract/"
            "route_stage_handoff_boundary",
        )
        audit = thinning["privatized_functional_module_audit"]
        self.assertEqual(audit["surface_kind"], "mag_privatized_functional_module_audit")
        self.assertEqual(audit["state"], "manifest_projected_for_opl_unified_audit")
        self.assertTrue(audit["opl_unified_audit_read_model"])
        self.assertFalse(audit["claims_generic_runtime_removed_from_mag"])
        self.assertFalse(audit["claims_opl_replacement_exists"])
        self.assertFalse(audit["claims_production_long_run_soak_complete"])
        self.assertEqual(
            audit["classification_buckets"],
            [
                "declarative_pack_surface",
                "refs_only_adapter",
                "minimal_authority_function",
                "legacy_proof_tombstone",
            ],
        )
        pack_modules = {
            item["module_id"]: item
            for item in audit["declarative_pack_surfaces"]
        }
        self.assertEqual(
            set(pack_modules),
            {
                "runtime_registration",
                "task_lifecycle",
                "source_intake_shell",
            },
        )
        self.assertEqual(
            pack_modules["task_lifecycle"]["classification"],
            "declarative_pack_surface",
        )
        self.assertEqual(
            pack_modules["source_intake_shell"]["active_caller_status"],
            "active_declarative_source_requirements_pack_projection",
        )
        refs_modules = {
            item["module_id"]: item
            for item in audit["refs_only_adapter_surfaces"]
        }
        self.assertEqual(
            set(refs_modules),
            {
                "lifecycle_adapter",
                "observability",
                "sidecar_product_status_shell",
                "package_lifecycle_shell",
                "human_workbench_scheduler_daemon",
            },
        )
        self.assertIn("grant_lifecycle_stage", pack_modules["task_lifecycle"]["mag_retained_authority"])
        self.assertIn(
            "artifact_package_lifecycle_shell",
            refs_modules["package_lifecycle_shell"]["opl_expected_primitives"],
        )
        self.assertEqual(
            refs_modules["sidecar_product_status_shell"]["active_caller_status"],
            "active_refs_only_domain_sidecar_adapter",
        )
        self.assertIn(
            "src/med_autogrant/product_entry_parts/sidecar.py",
            refs_modules["sidecar_product_status_shell"]["code_paths"],
        )
        mag_modules = {item["module_id"]: item for item in audit["mag_owned_grant_authority_surfaces"]}
        self.assertEqual(
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
        self.assertEqual(
            mag_modules["package_readiness_submission_ready"]["classification"],
            "minimal_authority_function",
        )
        self.assertIn(
            "submission_ready_verdict",
            mag_modules["package_readiness_submission_ready"]["mag_retained_authority"],
        )
        self.assertEqual(
            mag_modules["grant_memory_accept_reject"]["active_caller_status"],
            "active_mag_memory_body_decision_keep",
        )
        self.assertIn(
            "src/med_autogrant/product_entry_parts/domain_memory_runtime.py",
            mag_modules["grant_memory_accept_reject"]["code_paths"],
        )
        self.assertIn(
            "cannot own memory body",
            mag_modules["grant_memory_accept_reject"]["cannot_absorb_reason"],
        )
        retire_modules = {item["module_id"]: item for item in audit["retire_or_tombstone_surfaces"]}
        self.assertIn("repo_owned_scheduler_daemon", retire_modules)
        self.assertFalse(retire_modules["repo_owned_scheduler_daemon"]["active_caller_allowed"])
        self.assertEqual(
            retire_modules["repo_owned_scheduler_daemon"]["active_caller_status"],
            "legacy_scheduler_daemon_physically_removed_refs_only_runtime_control",
        )
        self.assertEqual(
            retire_modules["local_runtime_journal_attempt_ledger"]["active_caller_status"],
            "legacy_local_journal_attempt_ledger_physically_removed",
        )
        self.assertIn(
            "src/med_autogrant/runtime_defaults.py",
            retire_modules["repo_owned_scheduler_daemon"]["code_paths"],
        )
        self.assertEqual(
            retire_modules["domain_runtime_patch_bridge"]["active_caller_status"],
            "retired_physical_facade_removed_no_active_caller",
        )
        self.assertEqual(
            retire_modules["domain_runtime_patch_bridge"]["code_paths"],
            ["src/med_autogrant/domain_runtime.py:absent"],
        )
        self.assertIn(
            "tests/test_domain_runtime_split.py::RuntimeSplitStructureTest::test_retired_runtime_facade_is_not_present_in_source",
            retire_modules["domain_runtime_patch_bridge"]["evidence_refs"],
        )
        self.assertEqual(
            retire_modules["compatibility_only_product_entry_aggregate_test"]["active_caller_status"],
            "legacy_aggregate_test_physically_removed_focused_cases_are_replacement_tests",
        )
        self.assertEqual(
            retire_modules["compatibility_only_product_entry_aggregate_test"]["code_paths"],
            ["tests/test_product_entry.py"],
        )
        self.assertEqual(
            retire_modules["compatibility_only_product_entry_aggregate_test"]["active_callers"],
            [],
        )
        self.assertIn(
            "tests/product_entry_cases/:focused_replacement_tests",
            retire_modules["compatibility_only_product_entry_aggregate_test"]["evidence_refs"],
        )
        self.assertEqual(
            audit["mag_thin_adapter_code_surfaces"],
            [
                "product_entry_manifest_builder",
                "product_sidecar_guarded_domain_adapter",
                "domain_entry",
                "receipt_schema_and_writer",
                "grant_transition_oracle",
                "refs_only_projection_builders",
                "focused_contract_tests",
            ],
        )
        self.assertEqual(
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
        self.assertIn("workspace_source_intake_shell", audit["opl_must_absorb_code_surfaces"])
        self.assertIn("generic_scheduler_daemon", audit["opl_must_absorb_code_surfaces"])
        self.assertFalse(audit["fail_closed_rules"]["delete_grant_lifecycle_stage_as_generic_lifecycle"])
        self.assertFalse(audit["fail_closed_rules"]["delete_package_readiness_as_generic_package_lifecycle"])
        self.assertFalse(audit["fail_closed_rules"]["delete_fundability_or_quality_verdict_as_generic_readiness"])
        followthrough = thinning["functional_followthrough_gap_classification"]
        self.assertEqual(
            followthrough["surface_kind"],
            "mag_functional_followthrough_gap_classification",
        )
        self.assertEqual(
            followthrough["state"],
            "mag_handler_boundary_ready_external_evidence_gated",
        )
        self.assertEqual(followthrough["mag_functional_structure_gap_count"], 0)
        self.assertEqual(followthrough["remaining_mag_functional_structure_gap_ids"], [])
        self.assertEqual(followthrough["remaining_mag_functional_structure_gaps"], [])
        self.assertEqual(
            followthrough["closed_classification_surface_ids"],
            [
                "P1_adapter_thinning_and_pack_input",
                "P2_package_export_artifact_lifecycle_handoff",
                "P3_grant_strategy_memory_locator_writeback_handoff",
                "P4_skeleton_generated_surface_and_legacy_retirement",
            ],
        )
        self.assertEqual(
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
            with self.subTest(closed_gap=closed_gap["gap_id"]):
                self.assertEqual(closed_gap["previous_bucket"], "functional_structure_gap")
                self.assertEqual(
                    closed_gap["current_bucket"],
                    "classification_surface_closed_active_bridge_exit_closed",
                )
                self.assertEqual(closed_gap["owner"], "med-autogrant")
                self.assertTrue(closed_gap["closed_by_refs"])
        self.assertEqual(followthrough["external_owner_gates"], [])
        for evidence_gap in followthrough["reclassified_as_testing_evidence_gaps"]:
            with self.subTest(evidence_gap=evidence_gap["gap_id"]):
                self.assertEqual(evidence_gap["current_bucket"], "testing_evidence_gap")
                self.assertEqual(evidence_gap["owner"], "evidence_gate")
                self.assertTrue(evidence_gap["mag_surface_refs"])
        self.assertTrue(followthrough["authority_boundary"]["mag_repo_functional_structure_gaps_zero"])
        self.assertTrue(followthrough["authority_boundary"]["classification_closed"])
        self.assertFalse(followthrough["authority_boundary"]["followthrough_gaps_open"])
        self.assertFalse(followthrough["authority_boundary"]["claims_opl_replacement_exists"])
        self.assertFalse(
            followthrough["authority_boundary"]["claims_opl_generated_surface_production_consumed"]
        )
        self.assertFalse(followthrough["authority_boundary"]["claims_production_long_run_soak_complete"])
        output_guard = thinning["thin_surface_output_guard"]
        self.assertEqual(output_guard["surface_kind"], "mag_thin_surface_output_guard")
        self.assertEqual(
            output_guard["allowed_output_classes"],
            thinning["mag_owned_outputs"],
        )
        self.assertEqual(
            output_guard["required_sidecar_return_refs"],
            thinning["exposed_sidecar_return_refs"],
        )
        self.assertEqual(
            output_guard["private_functional_state_output_classes_forbidden"],
            [
                "local_runtime_journal_state",
                "local_attempt_ledger_state",
                "attention_queue_state",
                "stage_attempt_ledger_state",
                "package_lifecycle_state",
                "source_intake_state",
                "operator_workbench_state",
                "scheduler_daemon_state",
                "hermes_state_db_runtime_state",
            ],
        )
        self.assertIn("generic_scheduler_state", output_guard["forbidden_output_classes"])
        self.assertIn("generic_workbench_state", output_guard["forbidden_output_classes"])
        self.assertIn("generic_memory_transport_state", output_guard["forbidden_output_classes"])
        self.assertIn("generic_artifact_lifecycle_state", output_guard["forbidden_output_classes"])
        self.assertIn("generic_operator_workbench_state", output_guard["forbidden_output_classes"])
        self.assertIn("generic_observability_slo_state", output_guard["forbidden_output_classes"])
        for forbidden_state in output_guard["private_functional_state_output_classes_forbidden"]:
            with self.subTest(forbidden_state=forbidden_state):
                self.assertIn(forbidden_state, output_guard["forbidden_output_classes"])
        self.assertIn("family_conflict_envelope_completion_claim", output_guard["forbidden_output_classes"])
        self.assertIn("functional_harness_runtime_state", output_guard["forbidden_output_classes"])
        self.assertIn("opl_harness_pass_grant_ready", output_guard["forbidden_output_classes"])
        self.assertIn("opl_harness_pass_export_ready", output_guard["forbidden_output_classes"])
        self.assertIn("grant_artifact_content", output_guard["forbidden_output_classes"])
        self.assertIn("memory_body", output_guard["forbidden_output_classes"])
        self.assertTrue(output_guard["consumes_opl_replacement_expectations"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_generic_runtime_state"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_generic_workbench_state"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_generic_observability_state"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_private_functional_state"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_local_attempt_ledger_state"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_source_intake_state"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_package_lifecycle_state"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_hermes_state_db_runtime_state"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_family_conflict_completion_claim"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_functional_harness_runtime_state"])
        self.assertFalse(output_guard["authority_boundary"]["opl_harness_pass_can_declare_grant_ready"])
        self.assertFalse(output_guard["authority_boundary"]["opl_harness_pass_can_declare_export_ready"])
        scaffold_guard = thinning["standard_agent_scaffold_alignment"]
        self.assertEqual(
            scaffold_guard["surface_kind"],
            "mag_standard_agent_scaffold_thin_surface_guard",
        )
        self.assertFalse(scaffold_guard["knowledge_only_repository"])
        self.assertTrue(scaffold_guard["retains_domain_program_surfaces"])
        self.assertEqual(scaffold_guard["required_repo_boundaries"], ["agent", "contracts", "runtime", "docs"])
        self.assertIn("product_sidecar_adapter", scaffold_guard["retained_program_surface_kinds"])
        self.assertFalse(scaffold_guard["authority_boundary"]["mag_owns_generic_runtime_framework"])
        self.assertFalse(scaffold_guard["authority_boundary"]["mag_is_knowledge_only_repository"])
        authority = thinning["authority_boundary"]
        self.assertFalse(authority["opl_can_write_domain_truth"])
        self.assertFalse(authority["opl_can_write_memory_body"])
        self.assertFalse(authority["opl_can_declare_export_ready"])
        self.assertFalse(authority["mag_rebuilds_opl_runtime"])
        self.assertFalse(authority["mag_implements_generic_memory_transport"])
        self.assertFalse(authority["mag_implements_generic_artifact_gallery"])
        self.assertFalse(authority["mag_implements_generic_operator_workbench"])
        self.assertFalse(authority["mag_implements_generic_observability_slo"])
        self.assertFalse(authority["mag_implements_generic_artifact_lifecycle"])
        self.assertFalse(authority["opl_harness_pass_can_declare_grant_ready"])
        self.assertFalse(authority["opl_harness_pass_can_declare_export_ready"])
        replacement_ids = {item["primitive_id"] for item in thinning["opl_replacement_expectations"]}
        self.assertEqual(
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
            with self.subTest(primitive_id=item["primitive_id"]):
                self.assertEqual(item["owner"], "one-person-lab")
                self.assertEqual(item["mag_handoff_policy"], "contract_expectation_only")
                self.assertFalse(item["implemented_in_mag"])
        self.assertEqual(
            thinning["sidecar_contract_ref"],
            "/product_entry_manifest/mag_consumer_thinning_contract",
        )
        self.assertEqual(
            manifest["ideal_state_closure_status"]["consumer_thinning_contract_ref"],
            "/product_entry_manifest/mag_consumer_thinning_contract",
        )
