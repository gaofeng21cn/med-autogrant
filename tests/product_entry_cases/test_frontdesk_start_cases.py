from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryFrontdeskStartCaseTest(unittest.TestCase):
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
            "med_autogrant.product_entry_parts.manifest_builder._build_mainline_snapshot",
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
            "med_autogrant.product_entry_parts.progress._build_focus_payload",
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
            "med_autogrant.product_entry_parts.progress._build_product_command_catalog",
            return_value={
                "grant_progress": public_cli_command("grant-progress", "--format", "json"),
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_cockpit"):
                MedAutoGrantProductEntry().read_grant_cockpit(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )
