from __future__ import annotations


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
        self.assertIn("direct grant product status", manifest["product_entry_surface"]["summary"])
        self.assertEqual(
            manifest["managed_runtime_contract"],
            {
                "shared_contract_ref": "contracts/opl-framework/managed-runtime-three-layer-contract.json",
                "runtime_owner": "codex_cli",
                "domain_owner": "med-autogrant",
                "executor_owner": "med-autogrant",
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
        self.assertIn(
            "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/",
            manifest["session_continuity"]["journal_path"],
        )
        self.assertTrue(
            manifest["session_continuity"]["journal_path"].endswith(f"{payload['grant_run_id']}.json")
        )
        self.assertIn(
            "--journal",
            manifest["session_continuity"]["runtime_entries"]["runtime_run"]["command"],
        )
        runtime_control = manifest["runtime_control"]
        self.assertEqual(runtime_control["surface_kind"], "runtime_control")
        self.assertEqual(runtime_control["runtime_owner"], "codex_cli")
        self.assertEqual(runtime_control["domain_owner"], "med-autogrant")
        self.assertEqual(runtime_control["executor_owner"], "med-autogrant")
        self.assertEqual(runtime_control["session_locator"]["locator_field"], "grant_run_id")
        self.assertEqual(runtime_control["session_locator"]["locator_value"], payload["grant_run_id"])
        self.assertEqual(runtime_control["restore_point"]["session_id"], payload["grant_run_id"])
        self.assertEqual(runtime_control["restore_point"]["lifecycle_stage"], payload["lifecycle_stage"])
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
        skeleton = manifest["domain_agent_skeleton_mapping"]
        self.assertEqual(skeleton["surface_kind"], "standard_domain_agent_skeleton_mapping")
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
            skill["domain_projection"]["domain_agent_skeleton_mapping"],
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

    def test_family_orchestration_companion_is_projected_across_product_surfaces(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        progress_payload = entry.read_grant_progress(input_path=str(CRITIQUE_EXAMPLE_PATH))
        cockpit_payload = entry.read_grant_cockpit(input_path=str(CRITIQUE_EXAMPLE_PATH))
        direct_entry_payload = entry.build_grant_direct_entry(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )
        user_loop_payload = entry.build_grant_user_loop(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )
        manifest_payload = entry.build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        _assert_family_orchestration_companion(
            self,
            progress_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            cockpit_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            direct_entry_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            user_loop_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            manifest_payload["product_entry_manifest"].get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )

    def test_family_orchestration_action_graph_uses_shared_product_entry_orchestration(self) -> None:
        from med_autogrant.product_entry_parts import orchestration_companions as module

        captured: dict[str, object] = {}

        def _fake_build_family_product_entry_orchestration(**kwargs: object) -> dict[str, object]:
            captured.update(kwargs)
            return {
                "action_graph_ref": {
                    "ref_kind": "json_pointer",
                    "ref": "/family_orchestration/action_graph",
                    "label": "mag family action graph",
                },
                "action_graph": {
                    "graph_id": str(kwargs["graph_id"]),
                    "target_domain_id": str(kwargs["target_domain_id"]),
                    "graph_kind": str(kwargs["graph_kind"]),
                    "graph_version": str(kwargs["graph_version"]),
                    "nodes": list(kwargs["nodes"]),
                    "edges": list(kwargs["edges"]),
                    "entry_nodes": list(kwargs["entry_nodes"]),
                    "exit_nodes": list(kwargs["exit_nodes"]),
                    "human_gates": list(kwargs["human_gates"]),
                    "checkpoint_policy": {
                        "mode": "explicit_nodes",
                        "checkpoint_nodes": list(kwargs["checkpoint_nodes"]),
                    },
                },
                "human_gates": list(kwargs["human_gate_previews"]),
                "resume_contract": {
                    "surface_kind": str(kwargs["resume_surface_kind"]),
                    "session_locator_field": str(kwargs["session_locator_field"]),
                    "checkpoint_locator_field": str(kwargs["checkpoint_locator_field"]),
                },
            }

        with patch.object(
            module,
            "_build_shared_family_product_entry_orchestration",
            side_effect=_fake_build_family_product_entry_orchestration,
        ):
            payload = module._build_family_orchestration_companion(
                current_route_id="drafting",
                recommended_route_id="critique",
                recommended_route_status="pending",
                needs_author_decision=True,
                review_surface_ref="/review",
                event_envelope_surface_ref="/events",
                checkpoint_lineage_surface_ref="/lineage",
                resume_surface_kind="grant_user_loop",
            )

        self.assertEqual(payload["action_graph"]["graph_id"], "mag_drafting_to_critique_graph")
        self.assertEqual(captured["graph_kind"], "grant_route_orchestration")
        self.assertEqual([node["node_id"] for node in captured["nodes"]], ["route:drafting", "route:critique"])
        self.assertEqual([edge["on"] for edge in captured["edges"]], ["decision"])
        self.assertEqual(captured["entry_nodes"], ["route:drafting"])
        self.assertEqual(captured["exit_nodes"], ["route:critique"])
        self.assertEqual(captured["checkpoint_nodes"], ["route:drafting", "route:critique"])
        self.assertEqual(captured["human_gate_previews"][0]["gate_id"], "mag_route_gate_critique")

    def test_grant_user_loop_projects_landed_critique_route_when_drafting_can_execute_directly(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(DRAFTING_EXAMPLE_PATH),
            task_intent="prepare-critique-handoff",
        )

        self.assertEqual(payload["command"], "grant-user-loop")
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        self.assertEqual(
            payload["grant_user_loop"]["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "critique",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["action_kind"],
            "execute_landed_route",
        )
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_id"], "critique")
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_status"], "landed")
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["command"],
            public_cli_command(
                "execute-critique-pass",
                "--input",
                str(DRAFTING_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id="draft-v1",
                        file_name="critique-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )
        self.assertNotIn("<", payload["grant_user_loop"]["next_action"]["command"])
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["handoff_surfaces"],
            None,
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["run_recommended_route"],
            public_cli_command(
                "execute-critique-pass",
                "--input",
                str(DRAFTING_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id="draft-v1",
                        file_name="critique-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_direct_entry"],
            public_cli_command(
                "grant-direct-entry",
                "--input",
                str(DRAFTING_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "prepare-critique-handoff",
                "--format",
                "json",
            ),
        )
