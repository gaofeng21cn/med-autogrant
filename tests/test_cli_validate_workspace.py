from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402
from med_autogrant.public_cli import public_cli_argv  # noqa: E402


EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_minimal.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
DIRECTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_direction_screening.json"
QUESTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_question_refinement.json"
ARGUMENT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_argument_building.json"
FIT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_fit_alignment.json"
OUTLINE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_outline.json"
DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"
CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
MAJOR_REFRAME_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_major_reframe.json"
READY_FOR_SUBMISSION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FORCED_ROLLBACK_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_forced_rollback_argument.json"
PRESUBMISSION_FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class CliValidateWorkspaceTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(public_cli_argv(args))
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def run_json_cli(self, *args: str) -> dict[str, object]:
        exit_code, stdout, stderr = self.run_cli(*args)
        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        return json.loads(stdout)

    def test_validate_workspace_accepts_p2a_input_intake_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(INPUT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "input_intake")

    def test_validate_workspace_accepts_p2a_direction_screening_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(DIRECTION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "direction_screening")

    def test_validate_workspace_accepts_p2b_argument_building_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(ARGUMENT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "argument_building")

    def test_validate_workspace_accepts_p2b_fit_alignment_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(FIT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "fit_alignment")

    def test_validate_workspace_accepts_p2b_outline_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(OUTLINE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "outline")

    def test_validate_workspace_accepts_p2c_drafting_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(DRAFTING_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "drafting")

    def test_validate_workspace_accepts_p2c_critique_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")

    def test_validate_workspace_accepts_p2c_revision_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(REVISION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "revision")

    def test_validate_workspace_accepts_p3a_major_reframe_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(MAJOR_REFRAME_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")

    def test_validate_workspace_accepts_p3a_ready_for_submission_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(READY_FOR_SUBMISSION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")

    def test_execute_critique_pass_accepts_executor_override(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "execute-critique-pass",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "output_path": "/tmp/critique-output.json",
            "critique_execution": {
                "critique_id": "critique-test",
                "active_revision_plan_id": "revision-plan-test",
                "verdict": "major_revision",
                "executor": {
                    "kind": "hermes_native_full_agent_loop",
                },
            },
            "critique_workspace": {
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "lifecycle_stage": "critique",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload
            exit_code, stdout, stderr = self.run_cli(
                "execute-critique-pass",
                "--input",
                str(DRAFTING_EXAMPLE_PATH),
                "--output",
                "/tmp/critique-output.json",
                "--executor",
                "hermes_native_proof",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "execute-critique-pass",
                "input_path": str(DRAFTING_EXAMPLE_PATH),
                "output_path": "/tmp/critique-output.json",
                "executor_kind": "hermes_native_proof",
            }
        )

    def test_summarize_workspace_exposes_current_selection_for_question_refinement(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(QUESTION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "question_refinement")
        self.assertEqual(payload["current_selection"]["selected_direction_id"], "dir-inflammatory-remodeling")
        self.assertEqual(payload["current_selection"]["selected_question_id"], "question-immune-fibrosis")
        self.assertIsNone(payload["active_argument_chain"])

    def test_grant_progress_projects_user_facing_stage_summary_for_critique_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-progress",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "grant-progress")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["progress_projection"]["projection_kind"], "grant_progress")
        self.assertEqual(payload["progress_projection"]["recommended_next_stage"], "revision")
        self.assertEqual(payload["progress_projection"]["current_blockers"], ["必要性表述仍略偏现象描述。"])
        self.assertEqual(payload["progress_projection"]["needs_author_decision"], False)
        self.assertIn("family_orchestration", payload)
        self.assertIn("action_graph_ref", payload["family_orchestration"])
        self.assertIn("human_gates", payload["family_orchestration"])
        self.assertIn("resume_contract", payload["family_orchestration"])

    def test_grant_cockpit_projects_workspace_alerts_and_commands(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-cockpit",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "grant-cockpit")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["grant_cockpit"]["workspace_status"], "attention_required")
        self.assertIn("必要性表述仍略偏现象描述。", payload["grant_cockpit"]["workspace_alerts"])
        self.assertIn("build_direct_entry", payload["grant_cockpit"]["commands"])
        self.assertIn("family_orchestration", payload)
        self.assertIn("action_graph_ref", payload["family_orchestration"])
        self.assertIn("human_gates", payload["family_orchestration"])
        self.assertIn("resume_contract", payload["family_orchestration"])

    def test_grant_direct_entry_composes_product_surface_for_critique_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-direct-entry",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--task-intent",
            "tighten-grant-mainline",
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "grant-direct-entry")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["grant_direct_entry"]["entry_kind"], "grant_direct_entry")
        self.assertEqual(payload["grant_direct_entry"]["direct_entry"]["entry_mode"], "direct")
        self.assertEqual(payload["grant_direct_entry"]["opl_handoff_entry"]["entry_mode"], "opl-handoff")
        self.assertEqual(
            payload["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "revision",
        )
        self.assertIn("family_orchestration", payload)
        self.assertIn("action_graph_ref", payload["family_orchestration"])
        self.assertIn("human_gates", payload["family_orchestration"])
        self.assertIn("resume_contract", payload["family_orchestration"])

    def test_mainline_status_projects_current_phase_and_tranche(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "mainline-status",
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["program_id"], "med-autogrant-mainline")
        self.assertEqual(payload["current_phase"]["phase_id"], "P4")
        self.assertEqual(
            payload["current_runtime_owner"]["active_tranche"],
            "P4.F local submission-ready package landing",
        )

    def test_mainline_phase_resolves_next_selector(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "mainline-phase",
            "--phase",
            "next",
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["phase"]["phase_id"], "P4")
        self.assertEqual(payload["phase"]["status"], "next")

    def test_grant_user_loop_projects_mainline_snapshot_and_route_action(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-user-loop",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--task-intent",
            "tighten-grant-mainline",
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "grant-user-loop")
        self.assertEqual(payload["grant_user_loop"]["entry_kind"], "grant_user_loop")
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["action_kind"],
            "execute_landed_route",
        )
        self.assertEqual(
            payload["grant_user_loop"]["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "revision",
        )
        self.assertIn("family_orchestration", payload)
        self.assertIn("action_graph_ref", payload["family_orchestration"])
        self.assertIn("human_gates", payload["family_orchestration"])
        self.assertIn("resume_contract", payload["family_orchestration"])

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
        self.assertIn("supported_commands", manifest["skill_catalog"])
        self.assertIn("command_contracts", manifest["skill_catalog"])
        self.assertIn("automation", manifest)
        self.assertEqual(manifest["automation"]["surface_kind"], "automation")
        self.assertGreaterEqual(len(manifest["automation"]["automations"]), 1)

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

    def test_next_step_routes_each_p2a_stage_forward(self) -> None:
        cases = [
            (INPUT_EXAMPLE_PATH, "input_intake", "direction_screening"),
            (DIRECTION_EXAMPLE_PATH, "direction_screening", "question_refinement"),
            (QUESTION_EXAMPLE_PATH, "question_refinement", "argument_building"),
        ]

        for example_path, current_stage, recommended_stage in cases:
            with self.subTest(example=example_path.name):
                exit_code, stdout, stderr = self.run_cli(
                    "next-step",
                    "--input",
                    str(example_path),
                    "--format",
                    "json",
                )

                self.assertEqual(exit_code, 0)
                self.assertEqual(stderr, "")
                payload = json.loads(stdout)
                self.assertEqual(payload["current_stage"], current_stage)
                self.assertEqual(payload["recommended_stage"], recommended_stage)

    def test_summarize_workspace_exposes_active_fit_mapping_for_fit_alignment(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(FIT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "fit_alignment")
        self.assertEqual(payload["current_selection"]["active_fit_mapping_id"], "fit-001")
        self.assertEqual(payload["active_fit_mapping"]["id"], "fit-001")
        self.assertEqual(payload["active_fit_mapping"]["argument_chain_id"], "arg-001")

    def test_next_step_routes_each_p2b_stage_forward(self) -> None:
        cases = [
            (ARGUMENT_EXAMPLE_PATH, "argument_building", "fit_alignment"),
            (FIT_EXAMPLE_PATH, "fit_alignment", "outline"),
            (OUTLINE_EXAMPLE_PATH, "outline", "drafting"),
        ]

        for example_path, current_stage, recommended_stage in cases:
            with self.subTest(example=example_path.name):
                exit_code, stdout, stderr = self.run_cli(
                    "next-step",
                    "--input",
                    str(example_path),
                    "--format",
                    "json",
                )

                self.assertEqual(exit_code, 0)
                self.assertEqual(stderr, "")
                payload = json.loads(stdout)
                self.assertEqual(payload["current_stage"], current_stage)
                self.assertEqual(payload["recommended_stage"], recommended_stage)

    def test_summarize_workspace_exposes_draft_audit_for_p2c_drafting(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(DRAFTING_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        self.assertEqual(payload["active_draft"]["id"], "draft-v1")
        self.assertEqual(payload["active_draft"]["section_count"], 3)
        self.assertIsNone(payload["active_revision_plan"])

    def test_next_step_routes_each_p2c_stage_forward(self) -> None:
        cases = [
            (DRAFTING_EXAMPLE_PATH, "drafting", "critique"),
            (CRITIQUE_EXAMPLE_PATH, "critique", "revision"),
            (REVISION_EXAMPLE_PATH, "revision", "critique"),
        ]

        for example_path, current_stage, recommended_stage in cases:
            with self.subTest(example=example_path.name):
                exit_code, stdout, stderr = self.run_cli(
                    "next-step",
                    "--input",
                    str(example_path),
                    "--format",
                    "json",
                )

                self.assertEqual(exit_code, 0)
                self.assertEqual(stderr, "")
                payload = json.loads(stdout)
                self.assertEqual(payload["current_stage"], current_stage)
                self.assertEqual(payload["recommended_stage"], recommended_stage)

    def test_next_step_routes_major_reframe_back_to_question_refinement(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(MAJOR_REFRAME_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["current_stage"], "critique")
        self.assertEqual(payload["recommended_stage"], "question_refinement")
        self.assertIn("重塑科学问题", payload["reason"])

    def test_next_step_routes_ready_for_submission_to_frozen(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(READY_FOR_SUBMISSION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["current_stage"], "critique")
        self.assertEqual(payload["recommended_stage"], "frozen")
        self.assertIn("ready_for_submission", payload["reason"])

    def test_next_step_routes_forced_rollback_to_argument_building(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(FORCED_ROLLBACK_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["current_stage"], "critique")
        self.assertEqual(payload["recommended_stage"], "argument_building")
        self.assertEqual(payload["forced_rollback_stage"], "argument_building")
        self.assertIn("forced rollback", payload["reason"])

    def test_next_step_keeps_presubmission_frozen_workspace_at_frozen(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["current_stage"], "frozen")
        self.assertEqual(payload["recommended_stage"], "frozen")
        self.assertTrue(payload["presubmission_frozen"])

    def test_stage_route_report_aggregates_p2a_question_refinement_without_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(QUESTION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "question_refinement")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "argument_building")
        self.assertEqual(payload["checkpoint_status"], "forward_progress")
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "forward_progress")
        self.assertEqual(
            payload["verification_checkpoint"]["route_alignment"]["recommended_next_stage"],
            "argument_building",
        )
        self.assertEqual(
            payload["route"]["summarize_workspace"]["current_selection"]["selected_question_id"],
            "question-immune-fibrosis",
        )
        self.assertNotIn("critique_summary", payload["route"])

    def test_stage_route_report_aggregates_p2b_outline_without_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(OUTLINE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "outline")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "drafting")
        self.assertEqual(payload["route"]["summarize_workspace"]["active_fit_mapping"]["id"], "fit-001")
        self.assertEqual(payload["route"]["summarize_workspace"]["active_draft"]["id"], "draft-outline-v1")
        self.assertNotIn("critique_summary", payload["route"])

    def test_stage_route_report_aggregates_p2c_drafting_without_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(DRAFTING_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "critique")
        self.assertEqual(payload["route"]["summarize_workspace"]["active_draft"]["section_count"], 3)
        self.assertNotIn("critique_summary", payload["route"])

    def test_critique_summary_exposes_revision_audit_for_p2c_critique(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["critique_id"], "critique-v1")
        self.assertEqual(payload["revision_plan_id"], "revision-v1")
        self.assertEqual(payload["execution_status"], "planned")
        self.assertEqual(payload["recommended_next_stage"], "revision")

    def test_critique_summary_exposes_completed_revision_evidence_for_p2c_revision(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(REVISION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(payload["execution_status"], "completed")
        self.assertEqual(payload["pre_revision_version_label"], "v0.3")
        self.assertEqual(payload["post_revision_version_label"], "v0.4")
        self.assertIn("比较", payload["comparison_summary"])
        self.assertEqual(payload["recommended_next_stage"], "critique")

    def test_critique_summary_exposes_major_reframe_verdict(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(MAJOR_REFRAME_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["verdict"], "major_reframe")
        self.assertEqual(payload["recommended_next_stage"], "question_refinement")

    def test_critique_summary_exposes_ready_for_submission_verdict(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(READY_FOR_SUBMISSION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["verdict"], "ready_for_submission")
        self.assertEqual(payload["recommended_next_stage"], "frozen")

    def test_stage_route_report_aggregates_p2c_critique_with_critique_summary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "revision")
        self.assertEqual(payload["route"]["critique_summary"]["execution_status"], "planned")

    def test_stage_route_report_aggregates_p2c_revision_with_re_review_boundary(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(REVISION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "critique")
        self.assertEqual(payload["route"]["critique_summary"]["execution_status"], "completed")

    def test_stage_route_report_aggregates_p3a_major_reframe_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(MAJOR_REFRAME_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "question_refinement")
        self.assertEqual(payload["route"]["critique_summary"]["verdict"], "major_reframe")

    def test_stage_route_report_aggregates_p3a_ready_for_submission_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(READY_FOR_SUBMISSION_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "frozen")
        self.assertEqual(payload["route"]["critique_summary"]["verdict"], "ready_for_submission")
        self.assertFalse(payload["route"]["critique_summary"]["presubmission_frozen"])
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "freeze_ready")
        self.assertFalse(payload["verification_checkpoint"]["route_alignment"]["presubmission_frozen"])

    def test_validate_workspace_accepts_re_review_critique_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(RE_REVIEW_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")

    def test_validate_workspace_accepts_forced_rollback_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(FORCED_ROLLBACK_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")

    def test_validate_workspace_accepts_presubmission_frozen_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "frozen")

    def test_generated_revised_workspace_reenters_validator_and_checkpoint_surfaces(self) -> None:
        cases = (
            (CRITIQUE_EXAMPLE_PATH, "v0.4", None),
            (RE_REVIEW_EXAMPLE_PATH, "v0.5", "revision-v1"),
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            for input_path, expected_version_label, expected_reviewed_revision_plan_id in cases:
                with self.subTest(example=input_path.name):
                    revised_path = tmp_path / f"{input_path.stem}-revised.json"
                    revised_payload = self.run_json_cli(
                        "execute-revision-pass",
                        "--input",
                        str(input_path),
                        "--output",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertTrue(revised_payload["ok"])

                    validate_payload = self.run_json_cli(
                        "validate-workspace",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertTrue(validate_payload["ok"])
                    self.assertEqual(validate_payload["lifecycle_stage"], "critique")

                    summary_payload = self.run_json_cli(
                        "summarize-workspace",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertEqual(summary_payload["active_draft"]["status"], "revised")
                    self.assertEqual(summary_payload["active_draft"]["version_label"], expected_version_label)
                    self.assertEqual(summary_payload["active_revision_plan"]["execution_status"], "completed")

                    next_step_payload = self.run_json_cli(
                        "next-step",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertEqual(next_step_payload["current_stage"], "critique")
                    self.assertEqual(next_step_payload["recommended_stage"], "revision")

                    critique_payload = self.run_json_cli(
                        "critique-summary",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertEqual(critique_payload["draft_status"], "revised")
                    self.assertEqual(critique_payload["draft_version_label"], expected_version_label)
                    self.assertEqual(critique_payload["execution_status"], "completed")
                    self.assertEqual(
                        critique_payload["reviewed_revision_plan_id"],
                        expected_reviewed_revision_plan_id,
                    )

                    route_payload = self.run_json_cli(
                        "stage-route-report",
                        "--input",
                        str(revised_path),
                        "--format",
                        "json",
                    )
                    self.assertTrue(route_payload["ok"])
                    self.assertEqual(route_payload["lifecycle_stage"], "critique")
                    self.assertEqual(route_payload["route"]["next_step"]["recommended_stage"], "revision")
                    self.assertEqual(route_payload["route"]["summarize_workspace"]["active_draft"]["status"], "revised")
                    self.assertEqual(
                        route_payload["route"]["summarize_workspace"]["active_draft"]["version_label"],
                        expected_version_label,
                    )
                    self.assertEqual(route_payload["route"]["critique_summary"]["execution_status"], "completed")
                    self.assertEqual(route_payload["verification_checkpoint"]["checkpoint_status"], "forward_progress")
                    self.assertEqual(
                        route_payload["verification_checkpoint"]["route_alignment"]["recommended_next_stage"],
                        "revision",
                    )
                    self.assertEqual(
                        route_payload["verification_checkpoint"]["review_checkpoint"]["reviewed_revision_evidence"],
                        route_payload["route"]["summarize_workspace"]["reviewed_revision_evidence"],
                    )
                    self.assertEqual(
                        route_payload["route"]["critique_summary"]["reviewed_revision_plan_id"],
                        expected_reviewed_revision_plan_id,
                    )

    def test_critique_summary_exposes_re_review_linkage(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(RE_REVIEW_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["critique_id"], "critique-v2")
        self.assertEqual(payload["revision_plan_id"], "revision-v2")
        self.assertEqual(payload["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(payload["reviewed_revision_evidence"]["post_revision_version_label"], "v0.4")

    def test_critique_summary_exposes_forced_rollback_fields(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(FORCED_ROLLBACK_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["critique_id"], "critique-v2")
        self.assertEqual(payload["forced_rollback_stage"], "argument_building")
        self.assertEqual(payload["forced_rollback_reason"], "当前必要性链条已经失真，必须回到 argument chain 重建。")
        self.assertFalse(payload["presubmission_frozen"])
        self.assertEqual(payload["recommended_next_stage"], "argument_building")

    def test_critique_summary_exposes_presubmission_frozen_fields(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertEqual(payload["verdict"], "ready_for_submission")
        self.assertTrue(payload["presubmission_frozen"])
        self.assertEqual(payload["recommended_next_stage"], "frozen")

    def test_summarize_workspace_exposes_re_review_evidence(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(RE_REVIEW_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["active_critique"]["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(payload["reviewed_revision_evidence"]["source_critique_id"], "critique-v1")

    def test_summarize_workspace_exposes_forced_rollback_evidence(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(FORCED_ROLLBACK_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["active_critique"]["forced_rollback_stage"], "argument_building")
        self.assertEqual(payload["active_critique"]["forced_rollback_reason"], "当前必要性链条已经失真，必须回到 argument chain 重建。")
        self.assertFalse(payload["gates"]["presubmission_frozen"])

    def test_summarize_workspace_exposes_presubmission_frozen_gate(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertTrue(payload["gates"]["presubmission_frozen"])
        self.assertEqual(payload["active_draft"]["status"], "frozen")

    def test_stage_route_report_aggregates_p3b_re_review_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(RE_REVIEW_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "revision")
        self.assertEqual(payload["checkpoint_status"], "forward_progress")
        self.assertEqual(payload["route"]["summarize_workspace"]["reviewed_revision_evidence"]["revision_plan_id"], "revision-v1")
        self.assertEqual(payload["route"]["critique_summary"]["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "forward_progress")
        self.assertEqual(
            payload["verification_checkpoint"]["review_checkpoint"]["reviewed_revision_evidence"]["revision_plan_id"],
            "revision-v1",
        )

    def test_stage_route_report_aggregates_p3c_forced_rollback_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(FORCED_ROLLBACK_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "argument_building")
        self.assertEqual(payload["route"]["next_step"]["forced_rollback_stage"], "argument_building")
        self.assertEqual(payload["route"]["critique_summary"]["forced_rollback_stage"], "argument_building")
        self.assertFalse(payload["route"]["critique_summary"]["presubmission_frozen"])
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "rollback_required")
        self.assertEqual(
            payload["verification_checkpoint"]["route_alignment"]["forced_rollback_stage"],
            "argument_building",
        )

    def test_stage_route_report_aggregates_p3c_presubmission_frozen_branch(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "frozen")
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "frozen")
        self.assertTrue(payload["route"]["summarize_workspace"]["gates"]["presubmission_frozen"])
        self.assertTrue(payload["route"]["critique_summary"]["presubmission_frozen"])
        self.assertEqual(payload["verification_checkpoint"]["checkpoint_status"], "submission_frozen")
        self.assertTrue(payload["verification_checkpoint"]["route_alignment"]["presubmission_frozen"])

    def test_validate_workspace_accepts_re_review_revised_output_after_execute_revision_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            revised_output = Path(tmp_dir) / "p3b-revised.json"

            execute_exit, execute_stdout, execute_stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(RE_REVIEW_EXAMPLE_PATH),
                "--output",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(execute_exit, 0)
            self.assertEqual(execute_stderr, "")
            self.assertTrue(json.loads(execute_stdout)["ok"])

            exit_code, stdout, stderr = self.run_cli(
                "validate-workspace",
                "--input",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["error_count"], 0)
            self.assertEqual(payload["errors"], [])

    def test_next_step_keeps_revised_output_on_existing_revision_route(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            revised_output = Path(tmp_dir) / "p2c-revised.json"

            execute_exit, execute_stdout, execute_stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--output",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(execute_exit, 0)
            self.assertEqual(execute_stderr, "")
            self.assertTrue(json.loads(execute_stdout)["ok"])

            exit_code, stdout, stderr = self.run_cli(
                "next-step",
                "--input",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertEqual(payload["current_stage"], "critique")
            self.assertEqual(payload["recommended_stage"], "revision")
            self.assertIn("major_revision", payload["reason"])

    def test_stage_route_report_accepts_re_review_revised_output_and_keeps_reviewed_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            revised_output = Path(tmp_dir) / "p3b-revised.json"

            execute_exit, execute_stdout, execute_stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(RE_REVIEW_EXAMPLE_PATH),
                "--output",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(execute_exit, 0)
            self.assertEqual(execute_stderr, "")
            self.assertTrue(json.loads(execute_stdout)["ok"])

            exit_code, stdout, stderr = self.run_cli(
                "stage-route-report",
                "--input",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["lifecycle_stage"], "critique")
            self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "revision")
            self.assertEqual(
                payload["route"]["summarize_workspace"]["reviewed_revision_evidence"]["revision_plan_id"],
                "revision-v1",
            )
            self.assertEqual(
                payload["route"]["summarize_workspace"]["active_revision_plan"]["execution_status"],
                "completed",
            )
            self.assertEqual(
                payload["verification_checkpoint"]["review_checkpoint"]["reviewed_revision_evidence"]["revision_plan_id"],
                "revision-v1",
            )

    def test_validate_workspace_json_output(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")

        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["error_count"], 0)
        self.assertEqual(payload["errors"], [])

    def test_critique_summary_json_output(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")

        payload = json.loads(stdout)
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["critique_id"], "critique-v1")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["verdict"], "major_revision")
        self.assertEqual(payload["necessity_scientific_value"]["weight"], 60)
        self.assertEqual(payload["applicant_fit"]["weight"], 30)
        self.assertEqual(payload["feasibility"]["weight"], 10)
        self.assertIn("必要性表述仍略偏现象描述。", payload["blocking_issues"])

    def test_module_invocation_outputs_summary(self) -> None:
        env = dict(os.environ)
        env["PYTHONPATH"] = str(SRC_ROOT)

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "med_autogrant.cli",
                "workspace",
                "summarize",
                "--input",
                str(EXAMPLE_PATH),
                "--format",
                "json",
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
            cwd=REPO_ROOT,
        )

        self.assertEqual(completed.returncode, 0)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["selected_question"]["id"], "question-immune-fibrosis")

    def test_stage_route_report_json_output(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")

        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(
            payload["route"]["validate_workspace"]["grant_run_id"],
            "grant-run-nsfc-demo-001-baseline-001",
        )
        self.assertEqual(payload["route"]["validate_workspace"]["ok"], True)
        self.assertEqual(payload["route"]["next_step"]["recommended_stage"], "revision")
        self.assertEqual(payload["route"]["critique_summary"]["verdict"], "major_revision")

    def test_summarize_workspace_returns_structured_json_error_for_invalid_workspace(self) -> None:
        invalid_path = self.write_invalid_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "summarize-workspace")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["errors"][0]["path"], "revision_plans")
        self.assertEqual(payload["errors"][0]["message"], "critique 阶段必须存在非空 RevisionPlan。")
        self.assertIn("critique 阶段必须存在非空 RevisionPlan", payload["error"])

    def test_next_step_returns_structured_json_error_for_invalid_workspace(self) -> None:
        invalid_path = self.write_invalid_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "next-step")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["errors"][0]["path"], "revision_plans")
        self.assertEqual(payload["errors"][0]["message"], "critique 阶段必须存在非空 RevisionPlan。")
        self.assertIn("critique 阶段必须存在非空 RevisionPlan", payload["error"])

    def test_critique_summary_returns_structured_json_error_for_invalid_workspace(self) -> None:
        invalid_path = self.write_invalid_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "critique-summary")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["errors"][0]["path"], "revision_plans")
        self.assertEqual(payload["errors"][0]["message"], "critique 阶段必须存在非空 RevisionPlan。")
        self.assertIn("critique 阶段必须存在非空 RevisionPlan", payload["error"])

    def test_stage_route_report_returns_structured_json_error_for_outline_only_critique_draft(self) -> None:
        invalid_path = self.write_outline_only_critique_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "stage-route-report",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "stage-route-report")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["errors"][0]["path"], "application_drafts.status")
        self.assertEqual(payload["errors"][0]["message"], "critique 阶段的激活草稿 status 必须为 draft 或 revised。")
        self.assertIn("critique 阶段的激活草稿 status 必须为 draft 或 revised", payload["error"])

    def test_next_step_returns_structured_json_error_for_revision_stage_with_outline_draft(self) -> None:
        invalid_path = self.write_revision_outline_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], "next-step")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(payload["errors"][0]["path"], "application_drafts.status")
        self.assertEqual(payload["errors"][0]["message"], "revision 阶段的激活草稿 status 必须为 draft 或 revised。")
        self.assertIn("revision 阶段的激活草稿 status 必须为 draft 或 revised", payload["error"])

    def test_validate_workspace_reports_revision_transition_error_when_completed_plan_does_not_switch_status(self) -> None:
        invalid_path = self.write_revision_completed_without_revised_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(invalid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertGreaterEqual(payload["error_count"], 1)
        messages = {(item["path"], item["message"]) for item in payload["errors"]}
        self.assertIn(
            (
                "application_drafts.status",
                "revision plan 已标记 completed 时，激活草稿 status 必须显式切换为 revised。",
            ),
            messages,
        )

    def test_next_step_routes_completed_revision_back_to_critique(self) -> None:
        valid_path = self.write_completed_revision_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "next-step",
            "--input",
            str(valid_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["current_stage"], "revision")
        self.assertEqual(payload["recommended_stage"], "critique")
        self.assertIn("revised", payload["reason"])

    def write_invalid_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["revision_plans"][0]["items"] = []

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        invalid_path = tmp_dir / "invalid-workspace.json"
        invalid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return invalid_path

    def write_outline_only_critique_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["application_drafts"][0]["status"] = "outline"
        payload["application_drafts"][0]["sections"] = []

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        invalid_path = tmp_dir / "outline-only-critique-workspace.json"
        invalid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return invalid_path

    def write_revision_outline_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["lifecycle_stage"] = "revision"
        payload["application_drafts"][0]["status"] = "outline"

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        invalid_path = tmp_dir / "revision-outline-workspace.json"
        invalid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return invalid_path

    def write_revision_completed_without_revised_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["lifecycle_stage"] = "revision"
        payload["revision_plans"][0]["execution_status"] = "completed"
        payload["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        payload["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        payload["revision_plans"][0]["comparison_summary"] = "已按批注完成修订，但尚未切换草稿状态。"

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        invalid_path = tmp_dir / "revision-completed-without-revised.json"
        invalid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return invalid_path

    def write_completed_revision_workspace(self) -> Path:
        payload = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        payload["lifecycle_stage"] = "revision"
        payload["application_drafts"][0]["status"] = "revised"
        payload["application_drafts"][0]["version_label"] = "v0.4"
        payload["revision_plans"][0]["execution_status"] = "completed"
        payload["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        payload["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        payload["revision_plans"][0]["comparison_summary"] = "已根据 major_revision 完成立项依据与机制链条修订。"

        tmp_dir = Path(tempfile.mkdtemp(prefix="med-autogrant-cli-test-"))
        valid_path = tmp_dir / "revision-completed.json"
        valid_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return valid_path


if __name__ == "__main__":
    unittest.main()
