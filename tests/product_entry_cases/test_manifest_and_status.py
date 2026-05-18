from __future__ import annotations


from product_entry_cases.executor_defaults_assertions import assert_executor_defaults
from product_entry_cases.support import *  # noqa: F401,F403



class ProductEntryManifestStatusTest(unittest.TestCase):
    def test_product_entry_manifest_projects_current_grant_shell_and_shared_handoff(self) -> None:
        from med_autogrant.domain_entry_contract import (
            build_domain_entry_contract,
            build_user_interaction_contract,
        )
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertEqual(payload["command"], "product-entry-manifest")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        manifest = payload["product_entry_manifest"]
        self.assertEqual(manifest["surface_kind"], "product_entry_manifest")
        self.assertEqual(manifest["manifest_version"], 2)
        self.assertEqual(manifest["manifest_kind"], "med_auto_grant_product_entry_manifest")
        self.assertEqual(manifest["target_domain_id"], "med-autogrant")
        self.assertEqual(manifest["formal_entry"]["default"], "CLI")
        self.assertEqual(manifest["formal_entry"]["supported_protocols"], ["MCP"])
        self.assertEqual(manifest["workspace_locator"]["workspace_root"], str(CRITIQUE_EXAMPLE_PATH.resolve()))
        self.assertEqual(manifest["workspace_locator"]["workspace_path"], str(CRITIQUE_EXAMPLE_PATH.resolve()))
        self.assertEqual(manifest["recommended_shell"], "grant_user_loop")
        self.assertEqual(
            manifest["recommended_command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(manifest["product_entry_surface"]["shell_key"], "product_status")
        self.assertEqual(
            manifest["product_entry_surface"]["command"],
            public_cli_command(
                "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(manifest["product_entry_surface"]["surface_kind"], "product_status")
        self.assertIn("OPL generated/hosted status caller", manifest["product_entry_surface"]["summary"])
        self.assertEqual(
            manifest["managed_runtime_contract"],
            {
                "shared_contract_ref": "contracts/opl-framework/managed-runtime-three-layer-contract.json",
                "runtime_owner": "codex_cli",
                "domain_owner": "med-autogrant",
                "executor_owner": "codex_cli",
                "supervision_status_surface": {
                    "surface_kind": "grant_progress",
                    "owner": "med-autogrant",
                },
                "attention_queue_surface": {
                    "surface_kind": "grant_user_loop",
                    "owner": "med-autogrant",
                },
                "recovery_contract_surface": {
                    "surface_kind": "grant_user_loop",
                    "owner": "med-autogrant",
                },
                "fail_closed_rules": [
                    "domain_supervision_cannot_bypass_runtime",
                    "executor_cannot_declare_global_gate_clear",
                    "runtime_cannot_invent_domain_publishability_truth",
                ],
            },
        )
        self.assertEqual(manifest["runtime_inventory"]["surface_kind"], "runtime_inventory")
        self.assertEqual(manifest["runtime_inventory"]["runtime_owner"], "codex_cli")
        self.assertEqual(
            manifest["runtime_inventory"]["domain_owner"],
            manifest["managed_runtime_contract"]["domain_owner"],
        )
        self.assertEqual(manifest["task_lifecycle"]["surface_kind"], "task_lifecycle")
        self.assertEqual(
            manifest["task_lifecycle"]["status"],
            "forward_progress",
        )
        self.assertEqual(
            manifest["task_lifecycle"]["progress_surface"]["surface_kind"],
            "grant_progress",
        )
        self.assertEqual(manifest["persistence_policy"]["surface_kind"], "family_persistence_policy")
        self.assertEqual(manifest["persistence_policy"]["authority_surfaces"][0]["owner"], "med-autogrant")
        self.assertEqual(manifest["lifecycle_ledger"]["surface_kind"], "family_lifecycle_ledger")
        self.assertEqual(manifest["lifecycle_ledger"]["actions"][0]["safety_gate"], "schema_and_shared_family_validator")
        self.assertRegex(manifest["lifecycle_ledger"]["actions"][0]["sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(manifest["owner_route"]["surface_kind"], "family_owner_route")
        self.assertEqual(manifest["owner_route"]["next_owner"], "med-autogrant")
        self.assertIn("open_product_entry", manifest["owner_route"]["allowed_actions"])
        self.assertEqual(manifest["session_continuity"]["surface_kind"], "session_continuity")
        self.assertEqual(manifest["session_continuity"]["session_locator_field"], "grant_run_id")
        self.assertEqual(manifest["session_continuity"]["session_handle_kind"], "grant_run_id")
        self.assertEqual(manifest["session_continuity"]["session_id"], payload["grant_run_id"])
        self.assertEqual(manifest["session_continuity"]["session_owner"], "one-person-lab")
        self.assertEqual(
            manifest["session_continuity"]["generated_session_surface_ref"],
            "opl://generated-surfaces/mag/product-entry-session",
        )
        self.assertEqual(
            manifest["session_continuity"]["generated_resume_surface_ref"],
            "opl://generated-surfaces/mag/product-entry-session#resume",
        )
        self.assertEqual(
            manifest["session_continuity"]["domain_authority_surface_ref"],
            "/product_entry_manifest/owner_receipt_contract",
        )
        runtime_control = manifest["runtime_control"]
        self.assertEqual(runtime_control["surface_kind"], "runtime_control")
        self.assertEqual(runtime_control["runtime_owner"], "one-person-lab")
        self.assertEqual(runtime_control["domain_owner"], "med-autogrant")
        self.assertEqual(runtime_control["executor_owner"], "codex_cli")
        self.assertEqual(runtime_control["session_locator"]["locator_field"], "grant_run_id")
        self.assertEqual(runtime_control["session_locator"]["locator_value"], payload["grant_run_id"])
        self.assertEqual(runtime_control["restore_point"]["session_id"], payload["grant_run_id"])
        self.assertEqual(runtime_control["restore_point"]["lifecycle_stage"], payload["lifecycle_stage"])
        self.assertEqual(runtime_control["restore_point"]["session_owner"], "one-person-lab")
        self.assertEqual(
            runtime_control["restore_point"]["resume_surface_ref"],
            "opl://generated-surfaces/mag/product-entry-session#resume",
        )
        self.assertEqual(
            runtime_control["restore_point"]["domain_authority_surface_ref"],
            "/product_entry_manifest/owner_receipt_contract",
        )
        semantic_closure = runtime_control["semantic_closure"]
        self.assertEqual(semantic_closure["surface_kind"], "runtime_control_semantic_closure")
        self.assertEqual(semantic_closure["authoring_continuity"], "same_funding_call_task")
        self.assertEqual(semantic_closure["funding_call_lock"], "nsfc-2026-general")
        self.assertEqual(semantic_closure["quality_closure_surface"], "grant-quality-closure-dossier")
        self.assertEqual(semantic_closure["submission_ready_gate"], "package_submission_ready_strict_export_gate")
        self.assertEqual(
            semantic_closure["closure_ref"],
            "/product_entry_manifest/grant_authoring_readiness",
        )
        self.assertEqual(
            runtime_control["progress_surface"]["surface_kind"],
            "grant_progress",
        )
        self.assertEqual(
            runtime_control["artifact_pickup_surface"]["surface_kind"],
            "artifact_inventory",
        )
        self.assertEqual(
            runtime_control["approval_control_surface"]["surface_kind"],
            "grant_user_loop",
        )
        self.assertEqual(
            runtime_control["direct_entry"]["surface_kind"],
            "grant_direct_entry",
        )
        self.assertIn(
            "direct-entry",
            runtime_control["direct_entry"]["command"],
        )
        observability = manifest["autonomy_observability"]
        self.assertEqual(observability["surface_kind"], "grant_autonomy_observability")
        self.assertEqual(observability["owner"], "med-autogrant")
        self.assertEqual(observability["sli_summary"]["task_status"], manifest["task_lifecycle"]["status"])
        self.assertEqual(
            observability["sli_summary"]["runtime_health_status"],
            manifest["runtime_inventory"]["health_status"],
        )
        self.assertTrue(observability["sli_summary"]["same_funding_call_locked"])
        self.assertEqual(
            observability["sli_summary"]["remaining_gaps_count"],
            len(manifest["remaining_gaps"]),
        )
        self.assertEqual(manifest["progress_projection"]["surface_kind"], "progress_projection")
        self.assertEqual(
            manifest["progress_projection"]["workspace_path"],
            str(CRITIQUE_EXAMPLE_PATH.resolve()),
        )
        self.assertEqual(
            manifest["progress_projection"]["projection"]["projection_kind"],
            "grant_progress",
        )
        self.assertEqual(manifest["artifact_inventory"]["surface_kind"], "artifact_inventory")
        self.assertEqual(
            manifest["artifact_inventory"]["workspace_path"],
            str(CRITIQUE_EXAMPLE_PATH.resolve()),
        )
        self.assertEqual(
            manifest["artifact_inventory"]["artifacts"][0]["artifact_kind"],
            "workspace_document",
        )
        self.assertEqual(manifest["skill_catalog"]["surface_kind"], "skill_catalog")
        self.assertEqual(len(manifest["skill_catalog"]["skills"]), 1)
        assert_executor_defaults(self, manifest["executor_defaults"])
        skill = manifest["skill_catalog"]["skills"][0]
        self.assertEqual(skill["skill_id"], "med-autogrant")
        self.assertEqual(skill["title"], "Med Auto Grant")
        self.assertEqual(skill["domain_projection"]["plugin_name"], "med-autogrant")
        self.assertEqual(skill["domain_projection"]["skill_entry"], "med-autogrant")
        self.assertEqual(skill["domain_projection"]["recommended_shell"], "product_status")
        self.assertEqual(skill["domain_projection"]["runtime_continuity"]["surface_kind"], "skill_runtime_continuity")
        action_catalog = manifest["family_action_catalog"]
        self.assertEqual(action_catalog["surface_kind"], "family_action_catalog")
        self.assertEqual(action_catalog["catalog_id"], "med_autogrant_action_catalog")
        self.assertEqual(action_catalog["target_domain_id"], "med-autogrant")
        self.assertEqual(action_catalog["authority_boundary"]["domain_truth_owner"], "med-autogrant")
        self.assertIn(
            "MCP projection is descriptor-only",
            action_catalog["notes"],
        )
        user_loop_action = next(
            action for action in action_catalog["actions"] if action["action_id"] == "open_grant_user_loop"
        )
        self.assertEqual(user_loop_action["source_command"]["command"], manifest["recommended_command"])
        self.assertFalse(user_loop_action["supported_surfaces"]["mcp"]["public_runtime"])
        self.assertTrue(user_loop_action["supported_surfaces"]["mcp"]["descriptor_only"])
        self.assertEqual(
            manifest["action_catalog_projections"]["mcp"][0]["name"],
            "open_grant_user_loop",
        )
        self.assertFalse(manifest["action_catalog_projections"]["mcp"][0]["public_runtime"])
        self.assertTrue(manifest["action_catalog_projections"]["mcp"][0]["descriptor_only"])
        self.assertEqual(
            manifest["operator_loop_actions"]["open_loop"]["action_catalog_ref"],
            "open_grant_user_loop",
        )
        self.assertEqual(
            manifest["operator_loop_actions"]["open_loop"]["command"],
            user_loop_action["source_command"]["command"],
        )
        stage_plane = manifest["family_stage_control_plane"]
        self.assertEqual(stage_plane["surface_kind"], "family_stage_control_plane")
        self.assertEqual(stage_plane["version"], "family-stage-control-plane.v1")
        self.assertEqual(stage_plane["plane_id"], "med_autogrant_stage_control_plane")
        self.assertEqual(stage_plane["target_domain_id"], "med-autogrant")
        self.assertEqual(stage_plane["authority_boundary"]["opl_role"], "projection_consumer_only")
        self.assertFalse(stage_plane["authority_boundary"]["can_write_grant_truth"])
        self.assertFalse(stage_plane["authority_boundary"]["can_override_fundability_judgment"])
        self.assertFalse(stage_plane["authority_boundary"]["can_bypass_submission_ready_gate"])
        self.assertEqual(stage_plane["discovery_smoke"]["status"], "ready")
        self.assertEqual(
            stage_plane["discovery_smoke"]["allowed_action_catalog_ref"],
            "/product_entry_manifest/family_action_catalog",
        )
        self.assertEqual(stage_plane["parity"]["status"], "aligned")
        self.assertEqual(
            stage_plane["freshness"]["refresh_policy"],
            "rebuild_product_entry_manifest_before_opl_discovery",
        )
        self.assertIn(
            {"ref_kind": "json_pointer", "ref": "/product_entry_manifest/family_action_catalog", "role": "action_catalog"},
            stage_plane["source_refs"],
        )
        self.assertEqual(
            [stage["stage_id"] for stage in stage_plane["stages"]],
            [
                "call_and_candidate_intake",
                "fundability_strategy",
                "specific_aims_and_structure",
                "proposal_authoring",
                "review_and_rebuttal",
                "package_and_submit_ready",
            ],
        )
        action_ids = {action["action_id"] for action in action_catalog["actions"]}
        required_stage_fields = set(stage_plane["discovery_smoke"]["required_stage_fields"])
        for stage in stage_plane["stages"]:
            with self.subTest(stage=stage["stage_id"]):
                self.assertLessEqual(required_stage_fields, set(stage))
                self.assertEqual(stage["owner"], "med-autogrant")
                self.assertEqual(stage["stage_goal"], stage["goal"])
                self.assertTrue(set(stage["allowed_action_refs"]) <= action_ids)
                self.assertEqual(stage["handoff"]["shared_handoff_ref"], "/shared_handoff")
                self.assertGreaterEqual(len(stage["source_refs"]), 5)
                self.assertEqual(
                    stage["freshness"]["refresh_policy"],
                    "rebuild_product_entry_manifest_before_opl_discovery",
                )
                self.assertFalse(stage["authority_boundary"]["can_write_grant_truth"])
                self.assertFalse(stage["authority_boundary"]["can_override_fundability_judgment"])
                self.assertFalse(stage["authority_boundary"]["can_bypass_submission_ready_gate"])
        proposal_stage = next(stage for stage in stage_plane["stages"] if stage["stage_id"] == "proposal_authoring")
        self.assertEqual(proposal_stage["stage_kind"], "creation")
        self.assertEqual(
            proposal_stage["domain_stage_refs"],
            ["drafting", "revision", "grant-progress", "grant-user-loop"],
        )
        self.assertEqual(
            proposal_stage["authority_boundary"]["submission_ready_export_gate_owner"],
            "med-autogrant",
        )
        thinning = manifest["mag_consumer_thinning_contract"]
        compiler_input = thinning["declarative_grant_pack_compiler_input"]
        self.assertEqual(
            compiler_input["surface_kind"],
            "mag_declarative_grant_pack_compiler_input",
        )
        self.assertEqual(compiler_input["compiler_owner"], "one-person-lab")
        self.assertEqual(compiler_input["pack_owner"], "med-autogrant")
        self.assertEqual(
            compiler_input["input_policy"],
            "declarative_refs_and_authority_manifest_only",
        )
        self.assertEqual(
            compiler_input["source_refs"]["stage_graph_ref"],
            "/product_entry_manifest/family_stage_control_plane",
        )
        self.assertEqual(
            compiler_input["source_refs"]["action_metadata_ref"],
            "/product_entry_manifest/family_action_catalog",
        )
        self.assertEqual(
            compiler_input["source_refs"]["transition_oracle_ref"],
            "/product_entry_manifest/grant_transition_oracle",
        )
        self.assertFalse(compiler_input["authority_boundary"]["opl_can_write_grant_truth"])
        self.assertFalse(compiler_input["authority_boundary"]["opl_can_sign_owner_receipt"])
        self.assertFalse(compiler_input["authority_boundary"]["opl_can_declare_fundability_verdict"])
        generated_handoff = thinning["generated_surface_handoff"]
        self.assertEqual(generated_handoff["surface_kind"], "mag_generated_surface_handoff")
        self.assertEqual(generated_handoff["owner"], "med-autogrant")
        self.assertEqual(generated_handoff["target_generator_owner"], "one-person-lab")
        self.assertEqual(generated_handoff["active_caller_owner"], "med-autogrant")
        self.assertEqual(generated_handoff["domain_handler_target"], "med-autogrant")
        self.assertEqual(generated_handoff["domain_handler_owner"], "med-autogrant")
        self.assertEqual(
            generated_handoff["bridge_exit_gate"]["gate_status"],
            "mag_handler_boundary_ready_external_caller_evidence_required",
        )
        self.assertIn(
            "no_active_legacy_wrapper_caller_scan",
            generated_handoff["bridge_exit_gate"]["required_evidence"],
        )
        self.assertFalse(generated_handoff["bridge_exit_gate"]["claims_exit_complete"])
        self.assertFalse(
            generated_handoff["bridge_exit_gate"]["claims_production_long_run_soak_complete"]
        )
        self.assertEqual(
            generated_handoff["bridge_exit_gate"]["production_soak_gate_status"],
            "external_live_soak_and_caller_evidence_not_claimed_by_mag_repo",
        )
        self.assertEqual(
            generated_handoff["generated_surface_ids"],
            [
                "product_status",
                "product_user_loop",
                "product_sidecar",
                "grouped_cli_api",
                "projection_builder",
                "lifecycle_wrapper",
            ],
        )
        self.assertEqual(
            generated_handoff["current_mag_path_status"]["surface_kind"],
            "mag_generated_surface_handoff_currentness_proof",
        )
        self.assertEqual(generated_handoff["current_mag_path_status"]["status"], "current")
        self.assertEqual(generated_handoff["missing_current_mag_path_count"], 0)
        self.assertEqual(
            generated_handoff["current_mag_path_status"]["missing_current_mag_path_count"],
            0,
        )
        self.assertEqual(
            generated_handoff["stale_path_policy"],
            "history_or_source_ref_refresh_only",
        )
        self.assertFalse(generated_handoff["current_mag_path_status"]["claims_opl_replacement_exists"])
        self.assertFalse(generated_handoff["current_mag_path_status"]["claims_all_bridge_exits_complete"])
        self.assertFalse(
            generated_handoff["current_mag_path_status"]["claims_production_long_run_soak_complete"]
        )
        self.assertEqual(generated_handoff["mag_long_term_owner_surface_ids"], [])
        for surface in generated_handoff["generated_or_bridge_surfaces"]:
            with self.subTest(generated_surface=surface["surface_id"]):
                self.assertEqual(
                    surface["surface_status"],
                    "mag_handler_ref_only_adapter_waiting_for_opl_generated_or_hosted_caller_evidence",
                )
                self.assertEqual(surface["active_caller_owner"], "med-autogrant")
                self.assertEqual(surface["current_owner"], "med-autogrant")
                self.assertEqual(surface["target_owner"], "one-person-lab")
                self.assertEqual(surface["domain_handler_target"], "med-autogrant")
                self.assertEqual(surface["domain_handler_owner"], "med-autogrant")
                self.assertEqual(
                    surface["bridge_exit_gate"]["gate_status"],
                    "mag_handler_boundary_ready_external_caller_evidence_required",
                )
                self.assertFalse(surface["bridge_exit_gate"]["claims_exit_complete"])
                self.assertFalse(surface["bridge_exit_gate"]["claims_production_long_run_soak_complete"])
                self.assertTrue(surface["generated_by_opl_in_target"])
                self.assertFalse(surface["current_mag_long_term_owner"])
                self.assertFalse(surface["keeps_mag_authority_functions"])
                self.assertEqual(surface["current_mag_path_status"]["status"], "current")
                self.assertEqual(surface["missing_current_mag_path_count"], 0)
                self.assertEqual(surface["current_mag_path_status"]["missing_count"], 0)
                self.assertEqual(
                    surface["stale_path_policy"],
                    "history_or_source_ref_refresh_only",
                )
                for path_status in surface["current_mag_path_status"]["paths"]:
                    self.assertTrue(path_status["exists"])
                    self.assertTrue((REPO_ROOT / path_status["path"]).is_file())
        self.assertFalse(generated_handoff["authority_boundary"]["mag_long_term_owner"])
        self.assertFalse(generated_handoff["authority_boundary"]["generated_surface_can_sign_owner_receipt"])
        self.assertFalse(generated_handoff["authority_boundary"]["generated_surface_can_declare_verdict"])
        self.assertEqual(
            thinning["minimal_authority_function_ids"],
            [
                "fundability_verdict",
                "quality_verdict",
                "export_verdict",
                "package_authority",
                "memory_accept_reject",
                "owner_receipt_signer",
                "grant_helper",
            ],
        )
        authority_functions = {
            item["function_id"]: item for item in thinning["minimal_authority_functions"]
        }
        self.assertEqual(set(authority_functions), set(thinning["minimal_authority_function_ids"]))
        for authority_function in authority_functions.values():
            with self.subTest(authority_function=authority_function["function_id"]):
                self.assertEqual(authority_function["owner"], "med-autogrant")
                self.assertEqual(authority_function["retention_class"], "mag_minimal_authority_function")
                self.assertFalse(authority_function["generated_by_opl"])
                self.assertTrue(authority_function["opl_generated_wrapper_allowed"])
                self.assertEqual(
                    authority_function["cannot_absorb_reason"],
                    authority_function["cannot_generate_reason"],
                )
                self.assertEqual(
                    authority_function["ai_first_guard_policy"],
                    "stage_artifact_or_owner_receipt_required",
                )
                self.assertTrue(authority_function["ai_first_guard"])
                self.assertEqual(
                    authority_function["output_boundary"]["allowed_return_shapes"],
                    authority_function["allowed_return_shapes"],
                )
                self.assertIn("typed_blocker", authority_function["allowed_return_shapes"])
                self.assertIn(
                    "mechanical_ready_verdict",
                    authority_function["output_boundary"]["forbidden_outputs"],
                )
        artifact_locator = manifest["artifact_locator_contract"]
        self.assertEqual(artifact_locator["surface_kind"], "domain_artifact_locator_contract")
        self.assertEqual(artifact_locator["locator_id"], "mag.artifact_locator.v1")
        self.assertFalse(artifact_locator["runtime_artifact_root"]["repo_tracked"])
        self.assertIn(
            "$CODEX_HOME/projects/med-autogrant/runtime-state/artifacts/",
            artifact_locator["runtime_artifact_root"]["path_template"],
        )
        self.assertEqual(
            artifact_locator["runtime_artifact_root"]["write_policy"],
            "mag_runtime_or_export_surface_only",
        )
        self.assertEqual(artifact_locator["artifact_inventory_ref"], "/product_entry_manifest/artifact_inventory")
        self.assertFalse(artifact_locator["opl_consumption"]["can_issue_fundability_verdict"])
        self.assertFalse(artifact_locator["opl_consumption"]["can_issue_export_verdict"])
        self.assertTrue(artifact_locator["opl_consumption"]["requires_mag_receipt_for_domain_artifact_mutation"])
        controlled_attempt = manifest["controlled_stage_attempt_projection"]
        self.assertEqual(controlled_attempt["surface_kind"], "controlled_stage_attempt_projection")
        self.assertEqual(controlled_attempt["maps_to_opl_contract"], "opl_family_runtime_attempt_contract.v1")
        self.assertEqual(controlled_attempt["attempt_owner"], "med-autogrant")
        self.assertEqual(controlled_attempt["attempt_state"], manifest["task_lifecycle"]["status"])
        self.assertEqual(controlled_attempt["last_observed_projection"], manifest["progress_projection"])
        self.assertIn(
            "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/",
            controlled_attempt["receipt_refs"]["sidecar_dispatch_receipt_ref"],
        )
        self.assertFalse(controlled_attempt["opl_consumption_contract"]["can_hold_fundability_verdict"])
        self.assertFalse(controlled_attempt["opl_consumption_contract"]["can_hold_export_verdict"])
        self.assertIn(
            "canonical_grant_artifact_content",
            controlled_attempt["opl_consumption_contract"]["does_not_consume"],
        )
        proof = controlled_attempt["proof"]
        self.assertEqual(proof["surface_kind"], "controlled_stage_attempt_fixture_proof")
        self.assertTrue(proof["direct_skill_and_opl_hosted_use_same_descriptor_sidecar_quality_refs"])
        self.assertFalse(proof["opl_verdict_authority"]["fundability"])
        self.assertFalse(proof["opl_verdict_authority"]["submission_ready_export"])
        memory_locator = manifest["domain_memory_descriptor_locator"]
        self.assertEqual(memory_locator["surface_kind"], "domain_memory_descriptor_locator")
        self.assertEqual(memory_locator["descriptor_id"], "mag.domain_memory_descriptor_locator.v1")
        self.assertEqual(memory_locator["memory_owner"], "med-autogrant")
        self.assertEqual(memory_locator["memory_content_owner"], "med-autogrant")
        self.assertEqual(memory_locator["fundability_verdict_owner"], "med-autogrant")
        self.assertEqual(memory_locator["policy_ref"]["ref"], "docs/references/grant_strategy_memory_policy.md")
        self.assertEqual(memory_locator["memory_locator"]["locator_kind"], "domain_memory_locator")
        self.assertFalse(memory_locator["memory_locator"]["repo_tracked"])
        self.assertEqual(
            memory_locator["memory_locator"]["content_policy"],
            "locator_only_no_memory_content_in_repo_manifest",
        )
        self.assertEqual(
            memory_locator["memory_locator"]["retrieval_policy"],
            "stage_specific_small_relevant_sets",
        )
        migration_plan = memory_locator["migration_plan"]
        self.assertEqual(migration_plan["surface_kind"], "domain_memory_migration_plan")
        self.assertEqual(migration_plan["plan_id"], "mag.domain_memory_migration_plan.v1")
        self.assertEqual(migration_plan["migration_state"], "runtime_apply_contract_landed")
        self.assertEqual(
            migration_plan["seed_fixture_ref"]["ref"],
            "contracts/runtime-program/domain-memory-seed-fixture.json",
        )
        self.assertFalse(migration_plan["target_store"]["repo_tracked"])
        self.assertEqual(
            [step["step_id"] for step in migration_plan["migration_steps"]],
            ["discover_candidates", "mag_review", "persist_acceptance"],
        )
        self.assertIn("no_workspace_private_evidence", migration_plan["acceptance_gates"])
        self.assertEqual(migration_plan["pending_runtime_work"], [])
        self.assertEqual(
            migration_plan["runtime_apply_surfaces"],
            [
                "writeback_proposal_generator",
                "accept_reject_command",
                "runtime_receipt_evidence_writer",
                "operator_receipt_projection",
            ],
        )
        proposal_generator = memory_locator["writeback_proposal_generator"]
        self.assertEqual(proposal_generator["surface_kind"], "domain_memory_writeback_proposal_generator")
        self.assertEqual(proposal_generator["output_surface_kind"], "mag_domain_memory_writeback_proposal")
        self.assertEqual(proposal_generator["write_policy"], "runtime_store_only_no_repo_write")
        accept_reject = memory_locator["accept_reject_command"]
        self.assertEqual(accept_reject["surface_kind"], "domain_memory_accept_reject_command")
        self.assertEqual(accept_reject["decision_owner"], "med-autogrant")
        self.assertTrue(accept_reject["requires_mag_decision_before_store_mutation"])
        receipt_writer = memory_locator["runtime_receipt_evidence_writer"]
        self.assertEqual(receipt_writer["surface_kind"], "domain_memory_runtime_receipt_evidence_writer")
        self.assertEqual(receipt_writer["output_surface_kind"], "mag_domain_memory_runtime_receipt_evidence")
        self.assertEqual(receipt_writer["write_policy"], "runtime_receipt_instance_only_no_repo_write")
        operator_receipt = memory_locator["operator_receipt_projection"]
        self.assertEqual(operator_receipt["surface_kind"], "mag_domain_memory_operator_receipt_projection")
        self.assertEqual(
            operator_receipt["receipt_content_policy"],
            "receipt_refs_and_decision_metadata_only_no_memory_body",
        )
        self.assertFalse(operator_receipt["opl_consumption"]["can_hold_memory_content"])
        controlled_fixture = memory_locator["controlled_apply_fixture"]
        self.assertTrue(controlled_fixture["direct_skill_and_opl_hosted_use_same_refs"])
        self.assertFalse(controlled_fixture["opl_verdict_authority"]["fundability"])
        self.assertFalse(controlled_fixture["opl_verdict_authority"]["submission_ready_export"])
        self.assertEqual(
            [ref["stage_id"] for ref in memory_locator["stage_descriptor_refs"]],
            [stage["stage_id"] for stage in stage_plane["stages"]],
        )
        self.assertIn(
            "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/",
            memory_locator["writeback_receipt_refs"]["memory_writeback_receipt_ref"],
        )
        self.assertEqual(
            memory_locator["writeback_receipt_refs"]["receipt_write_policy"],
            "receipt_ref_only_no_domain_memory_content_mutation",
        )
        receipt_locator = memory_locator["receipt_locator"]
        self.assertEqual(receipt_locator["surface_kind"], "domain_memory_receipt_locator")
        self.assertEqual(receipt_locator["locator_id"], "mag.domain_memory_receipt_locator.v1")
        self.assertEqual(
            receipt_locator["receipt_content_policy"],
            "locator_and_decision_metadata_only_no_memory_body",
        )
        self.assertFalse(receipt_locator["repo_tracked"])
        self.assertFalse(memory_locator["opl_consumption_contract"]["can_hold_memory_content"])
        self.assertFalse(memory_locator["opl_consumption_contract"]["can_issue_fundability_verdict"])
        self.assertFalse(memory_locator["opl_consumption_contract"]["can_issue_authoring_quality_verdict"])
        self.assertFalse(memory_locator["opl_consumption_contract"]["can_issue_export_verdict"])
        self.assertFalse(memory_locator["opl_consumption_contract"]["can_mutate_domain_memory_store"])
        for forbidden_memory_role in (
            "memory_content",
            "fundability_verdict",
            "authoring_quality_verdict",
            "submission_ready_export_verdict",
            "canonical_grant_artifact_content",
        ):
            self.assertIn(forbidden_memory_role, memory_locator["opl_consumption_contract"]["does_not_consume"])
        self.assertEqual(
            memory_locator["authority_boundary"]["opl_role"],
            "memory_locator_ref_and_receipt_ref_consumer_only",
        )
        skeleton = manifest["standard_domain_agent_skeleton"]
        self.assertEqual(skeleton["surface_kind"], "standard_domain_agent_skeleton")
        self.assertEqual(skeleton["skeleton_id"], "mag.standard_domain_agent_skeleton.v1")
        self.assertEqual(set(skeleton["repo_source_boundary"]), {"agent", "contracts", "runtime", "docs"})
        self.assertEqual(
            skeleton["runtime_declaration"]["runtime_only_declares"],
            ["sidecar", "projection_builder", "lifecycle_adapter"],
        )
        self.assertEqual(
            skeleton["artifact_locator_ref"],
            "/product_entry_manifest/artifact_locator_contract",
        )
        self.assertEqual(
            skeleton["controlled_stage_attempt_ref"],
            "/product_entry_manifest/controlled_stage_attempt_projection",
        )
        self.assertEqual(
            skeleton["domain_memory_descriptor_locator_ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator",
        )
        self.assertEqual(
            skeleton["domain_memory_descriptor_locator"],
            memory_locator,
        )
        self.assertFalse(skeleton["authority_boundary"]["can_hold_fundability_verdict"])
        self.assertFalse(skeleton["authority_boundary"]["can_hold_export_verdict"])
        self.assertFalse(skeleton["authority_boundary"]["can_write_grant_artifacts"])
        self.assertEqual(
            skill["domain_projection"]["action_catalog_ref"],
            "/product_entry_manifest/family_action_catalog",
        )
        self.assertEqual(
            skill["domain_projection"]["standard_domain_agent_skeleton"],
            skeleton,
        )
        self.assertEqual(
            skill["domain_projection"]["mcp_descriptor"],
            manifest["action_catalog_projections"]["mcp"][0],
        )
        self.assertIn("validate-workspace", manifest["skill_catalog"]["supported_commands"])
        self.assertTrue(manifest["skill_catalog"]["command_contracts"])
        self.assertEqual(manifest["domain_entry_contract"], build_domain_entry_contract())
        self.assertEqual(
            manifest["domain_entry_contract"]["domain_agent_entry_spec"],
            {
                "surface_kind": "domain_agent_entry_spec",
                "agent_id": "mag",
                "title": "Med Auto Grant Domain Agent",
                "description": "Grant authoring domain truth owner surface for Med Auto Grant.",
                "default_engine": "codex",
                "workspace_requirement": "required",
                "locator_schema": {
                    "required_fields": ["input_path"],
                    "optional_fields": ["workspace_id", "grant_run_id", "draft_id"],
                    "workspace_field": "input_path",
                    "workspace_kind": "nsfc_workspace",
                    "workspace_id_field": "workspace_id",
                    "run_id_field": "grant_run_id",
                    "draft_id_field": "draft_id",
                },
                "codex_entry_strategy": "domain_agent_entry",
                "artifact_conventions": "grant_proposal_package",
                "progress_conventions": "grant_workloop_narration",
                "entry_command": "product-status",
                "manifest_command": "product-entry-manifest",
            },
        )
        self.assertEqual(
            manifest["user_interaction_contract"],
            build_user_interaction_contract(),
        )
        self.assertEqual(manifest["automation"]["surface_kind"], "automation")
        self.assertEqual(
            [item["automation_id"] for item in manifest["automation"]["automations"]],
            ["mag.submission_ready_export", "mag.authoring_loop_continuation"],
        )
        self.assertEqual(manifest["operator_loop_surface"]["shell_key"], "grant_user_loop")
        self.assertEqual(manifest["operator_loop_surface"]["command"], manifest["recommended_command"])
        self.assertEqual(manifest["operator_loop_surface"]["surface_kind"], "grant_user_loop")
        self.assertIn("direct grant user inbox shell", manifest["operator_loop_surface"]["summary"])
        self.assertEqual(manifest["operator_loop_actions"]["open_loop"]["command"], manifest["recommended_command"])
        self.assertEqual(manifest["operator_loop_actions"]["open_loop"]["surface_kind"], "grant_user_loop")
        self.assertEqual(manifest["operator_loop_actions"]["inspect_progress"]["requires"], [])
        self.assertEqual(manifest["operator_loop_actions"]["build_direct_entry"]["requires"], ["task_intent"])
        self.assertEqual(manifest["repo_mainline"]["active_phase"], "P4 mature direct grant product entry")
        self.assertEqual(
            manifest["repo_mainline"]["active_tranche"],
            "P4.G authoring-quality-first completion semantics alignment",
        )
        self.assertEqual(manifest["repo_mainline"]["phase_id"], "P4")
        self.assertEqual(
            manifest["repo_mainline"]["phase_summary"],
            "把 direct grant product 面逐步收成当前用户 inbox shell，并以 authoring quality 作为主任务完成语义。",
        )
        self.assertEqual(
            manifest["repo_mainline"]["next_focus"],
            [
                "继续把 `product-entry-manifest` / `product-status` 当作当前 direct grant product entry surface contract，并让 `grant-progress`、`grant-cockpit`、`grant-direct-entry` 与 `grant-user-loop` 继续对齐同一份 product entry surface truth。",
                "继续把 `family_orchestration` companion 从 action graph / human gate preview 深压到 family product-entry manifest v2、event envelope 与 checkpoint lineage contract，并保持 route status 直接读取共享 author-side route truth。",
                "把形式审查/客观补件统一收口到 TODO 与显式唤醒链路，并仅在直接破坏科学论证时升级为 blocker。",
                "对已锁定 funder/family 的任务线保持 continuity，不引入 opportunistic 跨 funder 切换叙事。",
            ],
        )
        self.assertEqual(
            manifest["product_entry_status"]["summary"],
            "把 direct grant product 面逐步收成当前用户 inbox shell，并以 authoring quality 作为主任务完成语义。",
        )
        self.assertEqual(
            manifest["product_entry_status"]["remaining_gaps_count"],
            len(manifest["remaining_gaps"]),
        )
        self.assertEqual(
            manifest["product_entry_status"]["next_focus"],
            manifest["repo_mainline"]["next_focus"],
        )
        self.assertEqual(
            manifest["product_entry_shell"]["grant_progress"]["command"],
            public_cli_command(
                "grant-progress", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            manifest["product_entry_shell"]["grant_user_loop"]["command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            manifest["product_entry_shell"]["product_status"]["command"],
            public_cli_command(
                "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            manifest["shared_handoff"]["direct_entry_builder"]["command"],
            public_cli_command(
                "build-product-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--entry-mode",
                "direct",
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            manifest["shared_handoff"]["opl_handoff_builder"]["command"],
            public_cli_command(
                "build-product-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--entry-mode",
                "opl-handoff",
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        _assert_family_orchestration_companion(
            self,
            manifest.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        self.assertEqual(
            manifest["family_orchestration"]["human_gates"][0]["gate_id"],
            "mag_route_gate_revision",
        )
        self.assertEqual(
            manifest["family_orchestration"]["event_envelope_surface"]["ref"],
            "/product_entry_manifest/recommended_command",
        )
        self.assertEqual(
            manifest["family_orchestration"]["checkpoint_lineage_surface"]["ref"],
            "/product_entry_manifest/repo_mainline/active_phase",
        )
        self.assertEqual(manifest["product_entry_quickstart"]["surface_kind"], "product_entry_quickstart")
        self.assertEqual(manifest["product_entry_quickstart"]["recommended_step_id"], "open_product_entry")
        self.assertEqual(
            [step["step_id"] for step in manifest["product_entry_quickstart"]["steps"]],
            [
                "open_product_entry",
                "continue_grant_loop",
                "inspect_progress",
                "inspect_cockpit",
                "build_submission_ready_package",
            ],
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["steps"][0]["command"],
            public_cli_command(
                "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["steps"][1]["requires"],
            ["task_intent"],
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["steps"][4]["requires"],
            ["output_dir"],
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["resume_contract"],
            manifest["family_orchestration"]["resume_contract"],
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["human_gate_ids"],
            ["mag_route_gate_revision"],
        )
        product_start = manifest["product_entry_start"]
        self.assertEqual(product_start["surface_kind"], "product_entry_start")
        self.assertEqual(product_start["recommended_mode_id"], "open_product_entry")
        self.assertEqual(
            [mode["mode_id"] for mode in product_start["modes"]],
            ["open_product_entry", "continue_grant_loop", "build_direct_entry"],
        )
        self.assertEqual(
            product_start["modes"][0]["command"],
            public_cli_command(
                "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(product_start["modes"][1]["requires"], ["task_intent"])
        self.assertEqual(product_start["modes"][2]["surface_kind"], "grant_direct_entry")
        self.assertEqual(
            product_start["resume_surface"],
            manifest["family_orchestration"]["resume_contract"],
        )
        self.assertEqual(product_start["human_gate_ids"], ["mag_route_gate_revision"])
        self.assertEqual(manifest["product_entry_overview"]["surface_kind"], "product_entry_overview")
        self.assertEqual(
            manifest["product_entry_overview"]["summary"],
            manifest["product_entry_status"]["summary"],
        )
        self.assertEqual(
            manifest["product_entry_overview"]["product_entry_command"],
            public_cli_command(
                "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            manifest["product_entry_overview"]["recommended_command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            manifest["product_entry_overview"]["progress_surface"],
            {
                "surface_kind": "grant_progress",
                "command": public_cli_command(
                    "grant-progress", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "step_id": "inspect_progress",
            },
        )
        self.assertEqual(
            manifest["product_entry_overview"]["resume_surface"],
            {
                "surface_kind": "grant_user_loop",
                "command": public_cli_command(
                    "grant-user-loop",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH.resolve()),
                    "--task-intent",
                    "<describe-task-intent>",
                    "--format",
                    "json",
                ),
                "session_locator_field": "grant_run_id",
                "checkpoint_locator_field": "lifecycle_stage",
            },
        )
        self.assertEqual(manifest["product_entry_overview"]["recommended_step_id"], "open_product_entry")
        self.assertEqual(
            manifest["product_entry_overview"]["next_focus"],
            manifest["product_entry_status"]["next_focus"],
        )
        self.assertEqual(
            manifest["product_entry_overview"]["remaining_gaps_count"],
            manifest["product_entry_status"]["remaining_gaps_count"],
        )
        self.assertEqual(
            manifest["product_entry_overview"]["human_gate_ids"],
            ["mag_route_gate_revision"],
        )
        preflight = manifest["product_entry_preflight"]
        self.assertEqual(preflight["surface_kind"], "product_entry_preflight")
        self.assertEqual(
            preflight["summary"],
            "当前 direct grant product entry surface 的前置检查已通过，可以先复核 workspace 与主线，再进入 product status。",
        )
        self.assertTrue(preflight["ready_to_try_now"])
        self.assertEqual(
            preflight["recommended_check_command"],
            public_cli_command(
                "validate-workspace", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            preflight["recommended_start_command"],
            public_cli_command(
                "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(preflight["blocking_check_ids"], [])
        self.assertEqual(
            [check["check_id"] for check in preflight["checks"]],
            [
                "workspace_document_valid",
                "default_runtime_owner_line",
                "direct_product entry surface_contract_landed",
                "submission_ready_export_gate",
            ],
        )
        self.assertEqual(preflight["checks"][0]["status"], "pass")
        self.assertEqual(preflight["checks"][0]["blocking"], True)
        self.assertEqual(preflight["checks"][1]["status"], "pass")
        self.assertEqual(preflight["checks"][2]["status"], "pass")
        self.assertEqual(preflight["checks"][3]["status"], "warn")
        product_readiness = manifest["product_entry_readiness"]
        self.assertEqual(product_readiness["surface_kind"], "product_entry_readiness")
        self.assertEqual(product_readiness["verdict"], "agent_assisted_ready_not_product_grade")
        self.assertTrue(product_readiness["usable_now"])
        self.assertFalse(product_readiness["good_to_use_now"])
        self.assertFalse(product_readiness["fully_automatic"])
        self.assertEqual(product_readiness["recommended_start_surface"], "product_status")
        self.assertEqual(
            product_readiness["recommended_start_command"],
            public_cli_command(
                "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(product_readiness["recommended_loop_surface"], "grant_user_loop")
        self.assertEqual(
            product_readiness["recommended_loop_command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
        )
        self.assertIn("还不是 mature direct grant Web UI / hosted runtime。", product_readiness["blocking_gaps"])
        readiness = manifest["grant_authoring_readiness"]
        self.assertEqual(readiness["surface_kind"], "grant_authoring_readiness")
        self.assertEqual(readiness["verdict"], "agent_assisted_cli_ready_not_full_autopilot")
        self.assertFalse(readiness["fully_automatic"])
        self.assertTrue(readiness["usable_now"])
        self.assertFalse(readiness["good_to_use_now"])
        self.assertEqual(readiness["recommended_start_surface"], "product_status")
        self.assertEqual(
            readiness["recommended_start_command"],
            public_cli_command(
                "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(readiness["recommended_loop_surface"], "grant_user_loop")
        self.assertEqual(
            [item["step_id"] for item in readiness["workflow_coverage"]],
            [
                "accumulation_direction_screening",
                "hotspot_literature_fit",
                "clinical_question_refinement",
                "innovation_framework",
                "mainline_closure",
                "significance_background_drafting",
                "preliminary_evidence_and_basis",
                "expected_results_timeline",
                "final_review_figures_package",
            ],
        )
        self.assertEqual(readiness["workflow_coverage"][0]["coverage_status"], "landed_route")
        self.assertEqual(readiness["workflow_coverage"][1]["coverage_status"], "partially_supported")
        self.assertIn("还不是 mature direct grant Web UI / hosted runtime。", readiness["blocking_gaps"])
