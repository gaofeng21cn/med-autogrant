from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryManifestFrontdeskTest(unittest.TestCase):
    def test_product_entry_manifest_projects_current_grant_shell_and_shared_handoff(self) -> None:
        from med_autogrant.domain_entry_contract import (
            build_domain_entry_contract,
            build_gateway_interaction_contract,
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
        self.assertEqual(manifest["frontdesk_surface"]["shell_key"], "product_frontdesk")
        self.assertEqual(
            manifest["frontdesk_surface"]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(manifest["frontdesk_surface"]["surface_kind"], "product_frontdesk")
        self.assertIn("direct grant product frontdesk", manifest["frontdesk_surface"]["summary"])
        self.assertEqual(
            manifest["managed_runtime_contract"],
            {
                "shared_contract_ref": "contracts/opl-gateway/managed-runtime-three-layer-contract.json",
                "runtime_owner": "upstream_hermes_agent",
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
        self.assertEqual(manifest["runtime_inventory"]["runtime_owner"], "upstream_hermes_agent")
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
        self.assertEqual(runtime_control["runtime_owner"], "upstream_hermes_agent")
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
        self.assertEqual(
            manifest["skill_catalog"]["skills"][0],
            {
                "surface_kind": "skill_descriptor",
                "skill_id": "mag",
                "title": "MAG",
                "owner": "med-autogrant",
                "distribution_mode": "repo_tracked_codex_plugin",
                "target_surface_kind": "product_frontdesk",
                "description": "Canonical Med Auto Grant domain app skill for Codex and OPL callers.",
                "command": public_cli_command(
                    "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                ),
                "readiness": "landed",
                "tags": ["mag", "domain-app", "grant-authoring"],
                "domain_projection": {
                    "plugin_name": "mag",
                    "skill_entry": "mag",
                    "skill_semantics": "domain_app",
                    "entry_shell_key": "product_frontdesk",
                    "entry_command": public_cli_command(
                        "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                    ),
                    "recommended_shell": "product_frontdesk",
                    "supporting_shell_keys": [
                        "grant_progress",
                        "grant_cockpit",
                        "grant_direct_entry",
                        "grant_user_loop",
                    ],
                    "shell_commands": {
                        "product_frontdesk": public_cli_command(
                            "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                        ),
                        "grant_progress": public_cli_command(
                            "grant-progress", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                        ),
                        "grant_cockpit": public_cli_command(
                            "grant-cockpit", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
                        ),
                        "grant_direct_entry": public_cli_command(
                            "grant-direct-entry",
                            "--input",
                            str(CRITIQUE_EXAMPLE_PATH.resolve()),
                            "--task-intent",
                            "<describe-task-intent>",
                            "--format",
                            "json",
                        ),
                        "grant_user_loop": public_cli_command(
                            "grant-user-loop",
                            "--input",
                            str(CRITIQUE_EXAMPLE_PATH.resolve()),
                            "--task-intent",
                            "<describe-task-intent>",
                            "--format",
                            "json",
                        ),
                    },
                        "runtime_continuity": {
                            "surface_kind": "skill_runtime_continuity",
                            "runtime_owner": manifest["runtime_control"]["runtime_owner"],
                            "domain_owner": manifest["runtime_control"]["domain_owner"],
                            "executor_owner": manifest["runtime_control"]["executor_owner"],
                            "authoring_continuity": "same_funding_call_task",
                            "funding_call_lock": "nsfc-2026-general",
                            "quality_closure_surface": "grant-quality-closure-dossier",
                            "submission_ready_gate": "package_submission_ready_strict_export_gate",
                            "session_locator_field": manifest["session_continuity"]["session_locator_field"],
                            "session_surface_ref": "/product_entry_manifest/session_continuity",
                        "progress_surface_ref": manifest["runtime_control"]["progress_surface"]["ref"],
                        "artifact_surface_ref": manifest["runtime_control"]["artifact_pickup_surface"]["ref"],
                        "restore_point_surface_ref": "/product_entry_manifest/runtime_control/restore_point",
                        "recommended_resume_command": manifest["runtime_control"]["restore_point"]["resume_command"],
                        "recommended_progress_command": manifest["runtime_control"]["progress_surface"]["command"],
                        "recommended_artifact_command": (
                            manifest["runtime_control"]["artifact_pickup_surface"]["command"]
                        ),
                    },
                },
            },
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
                "entry_command": "product-frontdesk",
                "manifest_command": "product-entry-manifest",
            },
        )
        self.assertEqual(
            manifest["gateway_interaction_contract"],
            build_gateway_interaction_contract(),
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
                "继续把 `product-entry-manifest` / `product-frontdesk` 当作当前 direct grant frontdoor contract，并让 `grant-progress`、`grant-cockpit`、`grant-direct-entry` 与 `grant-user-loop` 继续对齐同一份 frontdoor truth。",
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
            manifest["product_entry_shell"]["product_frontdesk"]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
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
        self.assertEqual(manifest["product_entry_quickstart"]["recommended_step_id"], "open_frontdesk")
        self.assertEqual(
            [step["step_id"] for step in manifest["product_entry_quickstart"]["steps"]],
            [
                "open_frontdesk",
                "continue_grant_loop",
                "inspect_progress",
                "inspect_cockpit",
                "build_submission_ready_package",
            ],
        )
        self.assertEqual(
            manifest["product_entry_quickstart"]["steps"][0]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
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
        self.assertEqual(product_start["recommended_mode_id"], "open_frontdesk")
        self.assertEqual(
            [mode["mode_id"] for mode in product_start["modes"]],
            ["open_frontdesk", "continue_grant_loop", "build_direct_entry"],
        )
        self.assertEqual(
            product_start["modes"][0]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
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
            manifest["product_entry_overview"]["frontdesk_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
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
        self.assertEqual(manifest["product_entry_overview"]["recommended_step_id"], "open_frontdesk")
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
            "当前 direct grant frontdoor 仍有 blocking preflight check；请先修复 workspace 或 runtime owner line 再进入 product frontdesk。",
        )
        self.assertFalse(preflight["ready_to_try_now"])
        self.assertEqual(
            preflight["recommended_check_command"],
            public_cli_command(
                "validate-workspace", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            preflight["recommended_start_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(preflight["blocking_check_ids"], ["upstream_hermes_owner_line"])
        self.assertEqual(
            [check["check_id"] for check in preflight["checks"]],
            [
                "workspace_document_valid",
                "upstream_hermes_owner_line",
                "direct_frontdoor_contract_landed",
                "submission_ready_export_gate",
            ],
        )
        self.assertEqual(preflight["checks"][0]["status"], "pass")
        self.assertEqual(preflight["checks"][0]["blocking"], True)
        self.assertEqual(preflight["checks"][1]["status"], "fail")
        self.assertEqual(preflight["checks"][2]["status"], "pass")
        self.assertEqual(preflight["checks"][3]["status"], "warn")
        product_readiness = manifest["product_entry_readiness"]
        self.assertEqual(product_readiness["surface_kind"], "product_entry_readiness")
        self.assertEqual(product_readiness["verdict"], "agent_assisted_ready_not_product_grade")
        self.assertTrue(product_readiness["usable_now"])
        self.assertFalse(product_readiness["good_to_use_now"])
        self.assertFalse(product_readiness["fully_automatic"])
        self.assertEqual(product_readiness["recommended_start_surface"], "product_frontdesk")
        self.assertEqual(
            product_readiness["recommended_start_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
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
        self.assertEqual(readiness["recommended_start_surface"], "product_frontdesk")
        self.assertEqual(
            readiness["recommended_start_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
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
        from med_autogrant.product_entry_parts import shared as module

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

    def test_grant_user_loop_projects_landed_question_refinement_route_when_direction_screening_can_execute_directly(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(DIRECTION_EXAMPLE_PATH),
            task_intent="advance-grant-mainline",
        )

        self.assertEqual(payload["command"], "grant-user-loop")
        self.assertEqual(payload["lifecycle_stage"], "direction_screening")
        self.assertEqual(
            payload["grant_user_loop"]["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "question_refinement",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["action_kind"],
            "execute_landed_route",
        )
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_id"], "question_refinement")
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_status"], "landed")
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["command"],
            public_cli_command(
                "execute-question-refinement-pass",
                "--input",
                str(DIRECTION_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id=None,
                        file_name="question-refinement-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )
        self.assertNotIn("<", payload["grant_user_loop"]["next_action"]["command"])
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["run_recommended_route"],
            public_cli_command(
                "execute-question-refinement-pass",
                "--input",
                str(DIRECTION_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id=None,
                        file_name="question-refinement-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )

    def test_product_frontdesk_projects_frontdoor_over_current_grant_loop(self) -> None:
        from med_autogrant.domain_entry_contract import (
            build_domain_entry_contract,
            build_gateway_interaction_contract,
        )
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_frontdesk(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "product-frontdesk")
        frontdesk = payload["product_frontdesk"]
        self.assertEqual(frontdesk["surface_kind"], "product_frontdesk")
        self.assertEqual(frontdesk["recommended_action"], "inspect_or_prepare_grant_loop")
        self.assertEqual(frontdesk["target_domain_id"], "med-autogrant")
        self.assertEqual(frontdesk["frontdesk_surface"]["shell_key"], "product_frontdesk")
        self.assertEqual(
            frontdesk["frontdesk_surface"]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(frontdesk["operator_loop_surface"]["shell_key"], "grant_user_loop")
        self.assertEqual(
            frontdesk["entry_surfaces"]["frontdesk"]["command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            frontdesk["entry_surfaces"]["grant_user_loop"]["command"],
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
            frontdesk["entry_surfaces"]["direct_entry_builder"]["command"],
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
            frontdesk["summary"]["frontdesk_command"],
            public_cli_command(
                "product-frontdesk", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            frontdesk["summary"]["operator_loop_command"],
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
        _assert_family_orchestration_companion(
            self,
            frontdesk.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        self.assertEqual(frontdesk["family_orchestration"]["human_gates"][0]["gate_id"], "mag_route_gate_revision")
        self.assertEqual(
            frontdesk["family_orchestration"]["event_envelope_surface"]["ref"],
            "/product_entry_manifest/recommended_command",
        )
        self.assertEqual(frontdesk["product_entry_overview"]["surface_kind"], "product_entry_overview")
        self.assertEqual(
            frontdesk["product_entry_overview"]["progress_surface"]["surface_kind"],
            "grant_progress",
        )
        self.assertEqual(
            frontdesk["product_entry_overview"]["project_profile_label"],
            "NSFC general medical grant profile",
        )
        self.assertEqual(
            frontdesk["product_entry_overview"]["critique_policy_id"],
            "nsfc_mentor_critique_v1",
        )
        self.assertEqual(
            frontdesk["product_entry_overview"]["resume_surface"]["surface_kind"],
            "grant_user_loop",
        )
        self.assertEqual(
            frontdesk["product_entry_overview"]["resume_surface"]["command"],
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
        self.assertEqual(frontdesk["product_entry_preflight"]["surface_kind"], "product_entry_preflight")
        self.assertFalse(frontdesk["product_entry_preflight"]["ready_to_try_now"])
        self.assertEqual(
            frontdesk["product_entry_preflight"]["recommended_check_command"],
            public_cli_command(
                "validate-workspace", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            frontdesk["product_entry_preflight"],
            frontdesk["product_entry_manifest"]["product_entry_preflight"],
        )
        self.assertEqual(frontdesk["product_entry_start"]["surface_kind"], "product_entry_start")
        self.assertEqual(frontdesk["product_entry_start"]["recommended_mode_id"], "open_frontdesk")
        self.assertEqual(frontdesk["product_entry_start"]["modes"][1]["mode_id"], "continue_grant_loop")
        self.assertEqual(frontdesk["product_entry_start"]["modes"][2]["mode_id"], "build_direct_entry")
        self.assertEqual(frontdesk["product_entry_start"]["resume_surface"]["surface_kind"], "grant_user_loop")
        self.assertEqual(
            frontdesk["product_entry_start"],
            frontdesk["product_entry_manifest"]["product_entry_start"],
        )
        self.assertEqual(frontdesk["product_entry_readiness"]["surface_kind"], "product_entry_readiness")
        self.assertTrue(frontdesk["product_entry_readiness"]["usable_now"])
        self.assertFalse(frontdesk["product_entry_readiness"]["good_to_use_now"])
        self.assertEqual(
            frontdesk["product_entry_readiness"],
            frontdesk["product_entry_manifest"]["product_entry_readiness"],
        )
        self.assertEqual(frontdesk["grant_authoring_readiness"]["surface_kind"], "grant_authoring_readiness")
        self.assertFalse(frontdesk["grant_authoring_readiness"]["fully_automatic"])
        self.assertTrue(frontdesk["grant_authoring_readiness"]["usable_now"])
        self.assertFalse(frontdesk["grant_authoring_readiness"]["good_to_use_now"])
        self.assertEqual(
            frontdesk["grant_authoring_readiness"],
            frontdesk["product_entry_manifest"]["grant_authoring_readiness"],
        )
        self.assertEqual(frontdesk["session_continuity"]["surface_kind"], "session_continuity")
        self.assertEqual(frontdesk["progress_projection"]["surface_kind"], "progress_projection")
        self.assertEqual(frontdesk["artifact_inventory"]["surface_kind"], "artifact_inventory")
        self.assertEqual(frontdesk["runtime_control"]["surface_kind"], "runtime_control")
        self.assertEqual(
            frontdesk["session_continuity"],
            frontdesk["product_entry_manifest"]["session_continuity"],
        )
        self.assertEqual(
            frontdesk["progress_projection"],
            frontdesk["product_entry_manifest"]["progress_projection"],
        )
        self.assertEqual(
            frontdesk["artifact_inventory"],
            frontdesk["product_entry_manifest"]["artifact_inventory"],
        )
        self.assertEqual(
            frontdesk["runtime_control"],
            frontdesk["product_entry_manifest"]["runtime_control"],
        )
        self.assertEqual(frontdesk["product_entry_quickstart"]["recommended_step_id"], "open_frontdesk")
        self.assertEqual(frontdesk["product_entry_quickstart"]["steps"][2]["step_id"], "inspect_progress")
        self.assertEqual(frontdesk["product_entry_quickstart"]["steps"][2]["surface_kind"], "grant_progress")
        self.assertEqual(frontdesk["product_entry_quickstart"]["steps"][4]["step_id"], "build_submission_ready_package")
        self.assertEqual(
            frontdesk["product_entry_quickstart"]["steps"][4]["surface_kind"],
            "submission_ready_package",
        )
        self.assertEqual(frontdesk["product_entry_manifest"]["frontdesk_surface"]["shell_key"], "product_frontdesk")
        self.assertEqual(frontdesk["product_entry_manifest"]["manifest_version"], 2)
        self.assertEqual(frontdesk["domain_entry_contract"], build_domain_entry_contract())
        self.assertEqual(
            frontdesk["domain_entry_contract"]["domain_agent_entry_spec"]["codex_entry_strategy"],
            "domain_agent_entry",
        )
        self.assertEqual(
            frontdesk["domain_entry_contract"]["domain_agent_entry_spec"]["entry_command"],
            "product-frontdesk",
        )
        self.assertEqual(
            frontdesk["domain_entry_contract"]["domain_agent_entry_spec"]["manifest_command"],
            "product-entry-manifest",
        )
        self.assertEqual(
            frontdesk["gateway_interaction_contract"],
            build_gateway_interaction_contract(),
        )
        self.assertEqual(
            frontdesk["domain_entry_contract"],
            frontdesk["product_entry_manifest"]["domain_entry_contract"],
        )
        self.assertEqual(
            frontdesk["gateway_interaction_contract"],
            frontdesk["product_entry_manifest"]["gateway_interaction_contract"],
        )

    def test_product_entry_manifest_fails_closed_on_invalid_mainline_snapshot_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry_parts.entry._build_mainline_snapshot",
            return_value={
                "current_owner_line": "CLI/domain-entry stable capability surface with Codex-default execution and optional hosted runtime carriers",
                "active_phase": "P4 mature direct grant product entry",
                "active_tranche": "P4.G authoring-quality-first completion semantics alignment",
                "phase_map": [{"phase_id": "P4", "phase_name": "mature direct grant product entry", "status": "next"}],
                "next_focus": [1],
                "remaining_gaps": ["mature direct grant Web UI / hosted runtime 仍未 landed。"],
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "product_entry_manifest"):
                MedAutoGrantProductEntry().build_product_entry_manifest(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )

    def test_product_frontdesk_fails_closed_on_invalid_operator_loop_action_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        manifest_payload = deepcopy(
            entry.build_product_entry_manifest(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
            )
        )
        manifest_payload["product_entry_manifest"]["operator_loop_actions"]["open_loop"] = {
            "command": public_cli_command("grant-user-loop", "--format", "json"),
        }

        with patch.object(
            MedAutoGrantProductEntry,
            "build_product_entry_manifest",
            return_value=manifest_payload,
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "product_frontdesk"):
                MedAutoGrantProductEntry().build_product_frontdesk(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )

    def test_grant_progress_family_orchestration_marks_landed_authoring_route_as_approved(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().read_grant_progress(
            input_path=str(DIRECTION_EXAMPLE_PATH),
        )

        family_orchestration = payload["family_orchestration"]
        self.assertEqual(family_orchestration["human_gates"][0]["gate_id"], "mag_route_gate_question_refinement")
        self.assertEqual(family_orchestration["human_gates"][0]["status"], "approved")
        self.assertEqual(family_orchestration["action_graph"]["edges"][0]["on"], "success")

    def test_grant_progress_fails_closed_on_invalid_projection_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry_parts.entry._build_focus_payload",
            return_value={
                "applicant_name": "示例申请人",
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_progress"):
                MedAutoGrantProductEntry().read_grant_progress(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )

    def test_grant_cockpit_fails_closed_on_invalid_command_catalog_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry_parts.entry._build_product_command_catalog",
            return_value={
                "grant_progress": public_cli_command("grant-progress", "--format", "json"),
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_cockpit"):
                MedAutoGrantProductEntry().read_grant_cockpit(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )
