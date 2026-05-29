from __future__ import annotations

from cli_validate_cases import *  # noqa: F401,F403


class CliValidateWorkspaceProductEntryCasesTest(CliValidateWorkspaceTest):
    def test_product_entry_manifest_keeps_domain_handler_contract_for_generated_caller(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "product-entry-manifest")
        manifest = payload["product_entry_manifest"]
        self.assertEqual(manifest["manifest_version"], 2)
        self.assertIn("family_orchestration", manifest)
        self.assertIn("action_graph_ref", manifest["family_orchestration"])
        self.assertIn("human_gates", manifest["family_orchestration"])
        self.assertIn("resume_contract", manifest["family_orchestration"])
        self.assertIn("runtime_inventory", manifest)
        self.assertEqual(manifest["runtime_inventory"]["surface_kind"], "runtime_inventory")
        self.assertIn("runtime_owner", manifest["runtime_inventory"])
        self.assertIn("task_lifecycle", manifest)
        self.assertEqual(manifest["task_lifecycle"]["surface_kind"], "task_lifecycle")
        self.assertIn("checkpoint_summary", manifest["task_lifecycle"])
        self.assertIn("skill_catalog", manifest)
        self.assertEqual(manifest["skill_catalog"]["surface_kind"], "skill_catalog")
        self.assertEqual(len(manifest["skill_catalog"]["skills"]), 1)
        self.assertEqual(manifest["skill_catalog"]["skills"][0]["skill_id"], "med-autogrant")
        self.assertIn("supported_commands", manifest["skill_catalog"])
        self.assertIn("command_contracts", manifest["skill_catalog"])
        self.assertIn("automation", manifest)
        self.assertEqual(manifest["automation"]["surface_kind"], "automation")
        self.assertGreaterEqual(len(manifest["automation"]["automations"]), 1)
        self.assertIn("autonomy_observability", manifest)
        self.assertEqual(
            manifest["autonomy_observability"]["surface_kind"],
            "grant_autonomy_observability",
        )
        self.assertIn("sli_summary", manifest["autonomy_observability"])
        self.assertTrue(manifest["recommended_command"].startswith("opl://generated-surfaces/mag/"))

    def test_skill_catalog_returns_machine_readable_app_skill_surface(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_skill_catalog(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "skill-catalog")
        skill_catalog = payload["skill_catalog"]
        self.assertEqual(skill_catalog["surface_kind"], "skill_catalog")
        self.assertEqual(len(skill_catalog["skills"]), 1)
        skill = skill_catalog["skills"][0]
        self.assertEqual(skill["skill_id"], "med-autogrant")
        self.assertEqual(skill["target_surface_kind"], "product_status")
        self.assertTrue(skill["command"].startswith("opl://generated-surfaces/mag/product-status"))
        domain_projection = skill["domain_projection"]
        self.assertEqual(domain_projection["plugin_name"], "med-autogrant")
        self.assertEqual(domain_projection["skill_entry"], "med-autogrant")
        self.assertEqual(domain_projection["skill_semantics"], "domain_app")
        self.assertEqual(domain_projection["entry_shell_key"], "product_status")
        self.assertEqual(domain_projection["recommended_shell"], "product_status")
        self.assertTrue(domain_projection["entry_command"].startswith("opl://generated-surfaces/mag/product-status"))
        self.assertEqual(
            domain_projection["supporting_shell_keys"],
            [
                "grant_progress",
                "grant_cockpit",
                "grant_direct_entry",
                "grant_user_loop",
                "domain_memory_writeback_proposal",
                "domain_memory_writeback_decision",
                "domain_memory_receipt_evidence",
            ],
        )
        self.assertTrue(domain_projection["shell_commands"]["product_status"].startswith("opl://generated-surfaces/mag/product-status"))
        self.assertTrue(domain_projection["shell_commands"]["grant_user_loop"].startswith("opl://generated-surfaces/mag/open-grant-user-loop"))
        self.assertIn("authority memory-proposal", domain_projection["shell_commands"]["domain_memory_writeback_proposal"])
        self.assertIn("authority memory-receipt-evidence", domain_projection["shell_commands"]["domain_memory_receipt_evidence"])
        self.assertIn("authority memory-decision", domain_projection["shell_commands"]["domain_memory_writeback_decision"])
        self.assertEqual(
            domain_projection["action_catalog_ref"],
            "/product_entry_manifest/family_action_catalog",
        )
        mcp_descriptor = domain_projection["mcp_descriptor"]
        self.assertEqual(mcp_descriptor["name"], "open_grant_user_loop")
        self.assertTrue(mcp_descriptor["command"].startswith("opl://generated-surfaces/mag/open-grant-user-loop"))
        self.assertEqual(mcp_descriptor["surface_kind"], "grant_user_loop")
        self.assertTrue(mcp_descriptor["descriptor_only"])
        self.assertFalse(mcp_descriptor["public_runtime"])
        runtime_continuity = domain_projection["runtime_continuity"]
        self.assertEqual(runtime_continuity["surface_kind"], "skill_runtime_continuity")
        self.assertEqual(runtime_continuity["runtime_owner"], "one-person-lab")
        self.assertEqual(runtime_continuity["domain_owner"], "med-autogrant")
        self.assertEqual(runtime_continuity["executor_owner"], "codex_cli")
        self.assertEqual(runtime_continuity["session_locator_field"], "grant_run_id")
        self.assertEqual(runtime_continuity["session_surface_ref"], "/product_entry_manifest/session_continuity")
        self.assertEqual(runtime_continuity["progress_surface_ref"], "/product_entry_manifest/progress_projection")
        self.assertEqual(runtime_continuity["artifact_surface_ref"], "/product_entry_manifest/artifact_inventory")
        self.assertEqual(
            runtime_continuity["restore_point_surface_ref"],
            "/product_entry_manifest/runtime_control/restore_point",
        )
        self.assertEqual(
            runtime_continuity["recommended_resume_command"],
            "opl://generated-surfaces/mag/product-entry-session#resume",
        )
        self.assertTrue(runtime_continuity["recommended_progress_command"].startswith("opl://generated-surfaces/mag/inspect-progress"))
        self.assertIn("workspace summarize", runtime_continuity["recommended_artifact_command"])
        stage_runtime_registration = domain_projection["opl_stage_runtime_registration"]
        self.assertEqual(
            stage_runtime_registration["surface_kind"],
            "opl_stage_runtime_domain_registration",
        )
        self.assertEqual(stage_runtime_registration["registration_id"], "mag.opl_stage_runtime.registration.v1")
        self.assertEqual(stage_runtime_registration["domain_id"], "medautogrant")
        self.assertEqual(stage_runtime_registration["domain_owner"], "med-autogrant")
        self.assertEqual(stage_runtime_registration["executor_owner"], "codex_cli")
        self.assertEqual(stage_runtime_registration["executor_adapter_owner"], "one-person-lab")
        self.assertEqual(
            stage_runtime_registration["executor_adapter_contract"]["receipt_contract"],
            "AgentExecutionReceipt",
        )
        self.assertTrue(stage_runtime_registration["registration_surface"]["command"].startswith("opl://generated-surfaces/mag/skill-catalog"))
        self.assertIn(
            "/runtime_control/semantic_closure",
            stage_runtime_registration["consumable_projection_refs"],
        )
        self.assertEqual(
            stage_runtime_registration["state_index_inputs"]["attention_queue_index"],
            "/automation/automations/1",
        )
        self.assertEqual(
            stage_runtime_registration["wakeup_boundary"]["policy"],
            "explicit_authoring_loop_continuation",
        )
        native_helper_consumption = stage_runtime_registration["native_helper_consumption"]
        self.assertEqual(native_helper_consumption["protocol_ref"], "contracts/opl-framework/native-helper-contract.json")
        self.assertNotIn("language", native_helper_consumption)
        self.assertEqual(native_helper_consumption["managed_by"], "one-person-lab")
        self.assertEqual(native_helper_consumption["index_consumption_policy"], "opl_index_only_no_domain_truth_writes")
        self.assertEqual(
            native_helper_consumption["indexes"]["artifact_projection_index"],
            {
                "input_ref": "/artifact_inventory",
                "source_surface_kind": "artifact_inventory",
                "write_policy": "opl_index_only",
            },
        )
        self.assertEqual(
            native_helper_consumption["indexes"]["attention_queue_index"],
            {
                "input_ref": "/automation/automations/1",
                "source_surface_kind": "automation_descriptor",
                "write_policy": "opl_index_only",
            },
        )
        for index_ref in native_helper_consumption["indexes"].values():
            self.assertNotIn("backing_helper_id", index_ref)
            self.assertEqual(index_ref["write_policy"], "opl_index_only")
        authority_boundary = native_helper_consumption["authority_boundary"]
        self.assertEqual(authority_boundary["helper_implementation_owner"], "one-person-lab")
        self.assertFalse(authority_boundary["mag_declares_helper_language_or_binary"])
        self.assertFalse(authority_boundary["mag_declares_backing_helper_ids"])
        self.assertFalse(authority_boundary["mag_can_write_domain_truth_from_helper"])
        self.assertEqual(authority_boundary["mag_quality_or_export_verdict_owner"], "med-autogrant")
        self.assertTrue(native_helper_consumption["source_of_truth_rule"].startswith("OPL-owned helpers may index MAG"))
        proof_surface = native_helper_consumption["proof_surface"]
        self.assertEqual(proof_surface["surface_kind"], "opl_native_helper_ref_consumption_proof")
        self.assertEqual(proof_surface["proof_id"], "mag.opl_native_helper.ref_consumption_proof.v1")
        self.assertEqual(
            proof_surface["covered_index_keys"],
            [
                "workspace_registry_index",
                "managed_session_ledger_index",
                "artifact_projection_index",
                "attention_queue_index",
                "runtime_health_snapshot_index",
            ],
        )
        self.assertEqual(
            proof_surface["coverage"]["artifact_projection_index"]["input_ref"],
            "/artifact_inventory",
        )
        self.assertEqual(
            proof_surface["coverage"]["attention_queue_index"]["input_ref"],
            "/automation/automations/1",
        )
        self.assertEqual(
            proof_surface["coverage"]["runtime_health_snapshot_index"]["input_ref"],
            "/runtime_inventory",
        )
        for proof in proof_surface["coverage"].values():
            self.assertNotIn("proof_role", proof)
            self.assertEqual(proof["write_policy"], "opl_index_only")
        self.assertIn("mag_repo_tracked_truth_remains_authoritative", proof_surface["readonly_boundaries"])
        self.assertIn("quality_gate_remains_mag_owned", proof_surface["readonly_boundaries"])
        self.assertIn("submission_ready_gate_remains_mag_owned", proof_surface["readonly_boundaries"])
        self.assertIn("supported_commands", skill_catalog)
        self.assertIn("command_contracts", skill_catalog)

    def test_product_status_projects_domain_handler_surface_for_generated_caller(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_status(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "product-status")
        self.assertEqual(payload["product_status"]["surface_kind"], "product_status")
        self.assertEqual(payload["product_status"]["product_entry_surface"]["shell_key"], "product_status")
        self.assertEqual(payload["product_status"]["operator_loop_surface"]["shell_key"], "grant_user_loop")
        self.assertTrue(
            payload["product_status"]["product_entry_surface"]["command"].startswith(
                "opl://generated-surfaces/mag/product-status"
            )
        )

    def test_product_start_projects_unified_start_surface(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_start(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "product-start")
        self.assertEqual(payload["product_entry_start"]["surface_kind"], "product_entry_start")
        self.assertEqual(payload["product_entry_start"]["recommended_mode_id"], "open_product_entry")
        self.assertEqual(
            [mode["mode_id"] for mode in payload["product_entry_start"]["modes"]],
            ["open_product_entry", "continue_grant_loop", "build_direct_entry"],
        )

    def test_product_group_is_retired_from_public_cli_validation_lane(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            self.run_cli(
                "product",
                "status",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(raised.exception.code, 2)
