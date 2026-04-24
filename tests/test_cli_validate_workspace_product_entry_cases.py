from __future__ import annotations

from cli_validate_cases import *  # noqa: F401,F403


class CliValidateWorkspaceProductEntryCasesTest(CliValidateWorkspaceTest):
    def test_product_entry_manifest_exposes_family_orchestration_v2(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "product-entry-manifest",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
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

    def test_skill_catalog_returns_machine_readable_app_skill_surface(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "skill-catalog",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "skill-catalog")
        skill_catalog = payload["skill_catalog"]
        self.assertEqual(skill_catalog["surface_kind"], "skill_catalog")
        self.assertEqual(len(skill_catalog["skills"]), 1)
        skill = skill_catalog["skills"][0]
        self.assertEqual(skill["skill_id"], "med-autogrant")
        self.assertEqual(skill["target_surface_kind"], "product_frontdesk")
        self.assertIn("product frontdesk", skill["command"])
        domain_projection = skill["domain_projection"]
        self.assertEqual(domain_projection["plugin_name"], "med-autogrant")
        self.assertEqual(domain_projection["skill_entry"], "med-autogrant")
        self.assertEqual(domain_projection["skill_semantics"], "domain_app")
        self.assertEqual(domain_projection["entry_shell_key"], "product_frontdesk")
        self.assertEqual(domain_projection["recommended_shell"], "product_frontdesk")
        self.assertIn("product frontdesk", domain_projection["entry_command"])
        self.assertEqual(
            domain_projection["supporting_shell_keys"],
            [
                "grant_progress",
                "grant_cockpit",
                "grant_direct_entry",
                "grant_user_loop",
            ],
        )
        self.assertIn("product frontdesk", domain_projection["shell_commands"]["product_frontdesk"])
        self.assertIn("product user-loop", domain_projection["shell_commands"]["grant_user_loop"])
        runtime_continuity = domain_projection["runtime_continuity"]
        self.assertEqual(runtime_continuity["surface_kind"], "skill_runtime_continuity")
        self.assertEqual(runtime_continuity["runtime_owner"], "upstream_hermes_agent")
        self.assertEqual(runtime_continuity["domain_owner"], "med-autogrant")
        self.assertEqual(runtime_continuity["executor_owner"], "med-autogrant")
        self.assertEqual(runtime_continuity["session_locator_field"], "grant_run_id")
        self.assertEqual(runtime_continuity["session_surface_ref"], "/product_entry_manifest/session_continuity")
        self.assertEqual(runtime_continuity["progress_surface_ref"], "/product_entry_manifest/progress_projection")
        self.assertEqual(runtime_continuity["artifact_surface_ref"], "/product_entry_manifest/artifact_inventory")
        self.assertEqual(
            runtime_continuity["restore_point_surface_ref"],
            "/product_entry_manifest/runtime_control/restore_point",
        )
        self.assertIn("runtime resume", runtime_continuity["recommended_resume_command"])
        self.assertIn("workspace progress", runtime_continuity["recommended_progress_command"])
        self.assertIn("workspace summarize", runtime_continuity["recommended_artifact_command"])
        self.assertIn("supported_commands", skill_catalog)
        self.assertIn("command_contracts", skill_catalog)

    def test_product_entry_manifest_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "product-entry-manifest",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前 grant run:", stdout)
        self.assertIn("当前 workspace:", stdout)
        self.assertIn("当前草稿编号:", stdout)
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("manifest 类型:", stdout)
        self.assertIn("维护者参考 phase:", stdout)
        self.assertIn("当前 focus:", stdout)
        self.assertNotIn("manifest_kind:", stdout)
        self.assertNotIn("active_phase:", stdout)
        self.assertNotIn("current_focus:", stdout)

    def test_product_preflight_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "product-preflight",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前 grant run:", stdout)
        self.assertIn("当前 workspace:", stdout)
        self.assertIn("当前草稿编号:", stdout)
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("当前可直接尝试:", stdout)
        self.assertIn("前置检查命令:", stdout)
        self.assertIn("推荐启动命令:", stdout)
        self.assertNotIn("ready_to_try_now:", stdout)
        self.assertNotIn("recommended_check_command:", stdout)
        self.assertNotIn("recommended_start_command:", stdout)

    def test_product_frontdesk_projects_frontdoor_and_current_loop(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "product-frontdesk",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "product-frontdesk")
        self.assertEqual(payload["product_frontdesk"]["surface_kind"], "product_frontdesk")
        self.assertEqual(payload["product_frontdesk"]["frontdesk_surface"]["shell_key"], "product_frontdesk")
        self.assertEqual(payload["product_frontdesk"]["operator_loop_surface"]["shell_key"], "grant_user_loop")

    def test_product_frontdesk_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "product-frontdesk",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("前台入口命令:", stdout)
        self.assertIn("推荐继续命令:", stdout)
        self.assertIn("当前 loop 命令:", stdout)
        self.assertIn("- 可用入口 frontdesk:", stdout)
        self.assertNotIn("frontdesk_command:", stdout)
        self.assertNotIn("recommended_command:", stdout)
        self.assertNotIn("operator_loop_command:", stdout)

    def test_product_start_projects_unified_start_surface(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "product-start",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "product-start")
        self.assertEqual(payload["product_entry_start"]["surface_kind"], "product_entry_start")
        self.assertEqual(payload["product_entry_start"]["recommended_mode_id"], "open_frontdesk")
        self.assertEqual(
            [mode["mode_id"] for mode in payload["product_entry_start"]["modes"]],
            ["open_frontdesk", "continue_grant_loop", "build_direct_entry"],
        )

    def test_build_product_entry_plain_text_prefers_human_facing_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "product-entry.json"
            exit_code, stdout, stderr = self.run_cli(
                "build-product-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--entry-mode",
                "direct",
                "--task-intent",
                "tighten-grant-mainline",
                "--output",
                str(output_path),
                "--format",
                "text",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前 grant run:", stdout)
        self.assertIn("当前 workspace:", stdout)
        self.assertIn("当前草稿编号:", stdout)
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("当前入口模式:", stdout)
        self.assertIn("当前任务意图:", stdout)
        self.assertIn("目标域:", stdout)
        self.assertIn("当前 checkpoint:", stdout)
        self.assertIn("输出位置:", stdout)
        self.assertNotIn("entry_mode:", stdout)
        self.assertNotIn("task_intent:", stdout)
        self.assertNotIn("target_domain_id:", stdout)
        self.assertNotIn("checkpoint_status:", stdout)
        self.assertNotIn("output_path:", stdout)

    def test_product_start_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "product-start",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("建议入口:", stdout)
        self.assertIn("- 可用入口", stdout)
        self.assertNotIn("lifecycle_stage:", stdout)
        self.assertNotIn("recommended_mode_id:", stdout)
        self.assertNotIn("- open_frontdesk:", stdout)
