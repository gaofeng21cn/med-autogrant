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
NON_NSFC_INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nih_r21_workspace_p2a_input_intake.json"



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

    def test_validate_workspace_accepts_non_nsfc_profiled_workspace(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(NON_NSFC_INPUT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["workspace_id"], "nih-r21-demo-001")

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

    def test_grant_intake_audit_dispatches_workspace_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-intake-audit",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": None,
            "lifecycle_stage": "input_intake",
            "input_path": str(INPUT_EXAMPLE_PATH),
            "grant_intake_audit": {
                "audit_kind": "grant_intake_audit",
                "intake_status": "ready",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload
            exit_code, stdout, stderr = self.run_cli(
                "grant-intake-audit",
                "--input",
                str(INPUT_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "grant-intake-audit",
                "input_path": str(INPUT_EXAMPLE_PATH),
            }
        )

    def test_grant_evidence_grounding_dispatches_workspace_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-evidence-grounding",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": None,
            "lifecycle_stage": "input_intake",
            "input_path": str(INPUT_EXAMPLE_PATH),
            "grant_evidence_grounding": {
                "grounding_kind": "grant_evidence_grounding",
                "grounding_status": "intake_grounded",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload
            exit_code, stdout, stderr = self.run_cli(
                "grant-evidence-grounding",
                "--input",
                str(INPUT_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "grant-evidence-grounding",
                "input_path": str(INPUT_EXAMPLE_PATH),
            }
        )

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

    def test_summarize_workspace_exposes_intake_and_evidence_surfaces_for_input_intake(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(INPUT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["grant_intake_audit"]["audit_kind"], "grant_intake_audit")
        self.assertTrue(payload["grant_intake_audit"]["readiness"]["ready_for_direction_screening"])
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "intake_grounded")

    def test_grant_intake_audit_projects_machine_readable_intake_surface(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-intake-audit",
            "--input",
            str(INPUT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "grant-intake-audit")
        self.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
        self.assertEqual(payload["grant_intake_audit"]["applicant_profile_id"], "applicant-gaofeng")

    def test_grant_evidence_grounding_projects_machine_readable_grounding_surface(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-evidence-grounding",
            "--input",
            str(INPUT_EXAMPLE_PATH),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "grant-evidence-grounding")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "intake_grounded")
        self.assertEqual(
            payload["grant_evidence_grounding"]["evidence_inventory"]["primary_evidence_ids"],
            ["evi-output-1", "evi-prelim-1", "evi-project-1"],
        )

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
        self.assertEqual(payload["grant_intake_audit"]["audit_kind"], "grant_intake_audit")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_kind"], "grant_evidence_grounding")
        self.assertIn("family_orchestration", payload)
        self.assertIn("action_graph_ref", payload["family_orchestration"])
        self.assertIn("human_gates", payload["family_orchestration"])
        self.assertIn("resume_contract", payload["family_orchestration"])

    def test_grant_progress_plain_text_prefers_shared_human_status_narration(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-progress",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("当前判断: 当前状态：批注审阅；下一阶段：修订落实；当前卡点：必要性表述仍略偏现象描述。", stdout)
        self.assertIn("下一步建议: 执行 revision plan 中的 P0/P1 项。", stdout)
        self.assertNotIn("current_stage_summary:", stdout)
        self.assertNotIn("next_system_action:", stdout)

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
        self.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "selection_grounded")
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
        self.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
        self.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "selection_grounded")
        self.assertIn("family_orchestration", payload)
        self.assertIn("action_graph_ref", payload["family_orchestration"])
        self.assertIn("human_gates", payload["family_orchestration"])
        self.assertIn("resume_contract", payload["family_orchestration"])

    def test_mainline_status_projects_current_line_focus_and_maintainer_references(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "mainline-status",
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["program_id"], "med-autogrant-mainline")
        self.assertEqual(
            payload["current_line"]["current_owner_line"],
            "CLI/domain-entry stable capability surface with Codex-default execution and optional hosted runtime carriers",
        )
        self.assertTrue(payload["current_focus"]["summary"])
        self.assertEqual(
            payload["maintainer_references"]["runtime_owner"]["active_tranche"],
            "P4.G authoring-quality-first completion semantics alignment",
        )

    def test_mainline_status_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "mainline-status",
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前 program:", stdout)
        self.assertIn("当前 line:", stdout)
        self.assertIn("当前 focus:", stdout)
        self.assertIn("- 当前 focus 项:", stdout)
        self.assertIn("- 已完成 record P4.F:", stdout)
        self.assertIn("- 剩余 gap:", stdout)
        self.assertNotIn("program_id:", stdout)
        self.assertNotIn("active_phase:", stdout)
        self.assertNotIn("active_tranche:", stdout)

    def test_validate_workspace_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "validate-workspace",
            "--input",
            str(EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前 grant run:", stdout)
        self.assertIn("当前 workspace:", stdout)
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("校验结果: True", stdout)
        self.assertIn("错误数量: 0", stdout)
        self.assertNotIn("grant_run_id:", stdout)
        self.assertNotIn("workspace_id:", stdout)
        self.assertNotIn("lifecycle_stage:", stdout)
        self.assertNotIn("error_count:", stdout)

    def test_summarize_workspace_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "summarize-workspace",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前 grant run:", stdout)
        self.assertIn("当前 workspace:", stdout)
        self.assertIn("当前模式:", stdout)
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("当前方向:", stdout)
        self.assertIn("当前问题:", stdout)
        self.assertIn("当前 fit 映射:", stdout)
        self.assertIn("当前草稿:", stdout)
        self.assertIn("当前批注结论:", stdout)
        self.assertNotIn("selected_direction:", stdout)
        self.assertNotIn("selected_question:", stdout)
        self.assertNotIn("active_fit_mapping:", stdout)
        self.assertNotIn("active_draft:", stdout)
        self.assertNotIn("active_critique_verdict:", stdout)

    def test_critique_summary_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "critique-summary",
            "--input",
            str(EXAMPLE_PATH),
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前 grant run:", stdout)
        self.assertIn("当前 workspace:", stdout)
        self.assertIn("当前批注编号:", stdout)
        self.assertIn("当前草稿编号:", stdout)
        self.assertIn("当前结论:", stdout)
        self.assertIn("整体诊断:", stdout)
        self.assertIn("建议下一阶段:", stdout)
        self.assertNotIn("critique_id:", stdout)
        self.assertNotIn("draft_id:", stdout)
        self.assertNotIn("verdict:", stdout)
        self.assertNotIn("overall_diagnosis:", stdout)
        self.assertNotIn("recommended_next_stage:", stdout)

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
        self.assertEqual(payload["maintainer_reference"]["record_detail"]["phase_id"], "P4")
        self.assertEqual(payload["maintainer_reference"]["record_detail"]["status"], "next")

    def test_mainline_phase_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "mainline-phase",
            "--phase",
            "next",
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前 line:", stdout)
        self.assertIn("维护参考 selector:", stdout)
        self.assertIn("维护参考记录: P4", stdout)
        self.assertIn("记录名称:", stdout)
        self.assertIn("记录状态:", stdout)
        self.assertIn("- 可用入口", stdout)
        self.assertNotRegex(stdout, r"(?m)^phase_id:")
        self.assertNotRegex(stdout, r"(?m)^phase_name:")
        self.assertNotRegex(stdout, r"(?m)^status:")

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

    def test_grant_user_loop_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "grant-user-loop",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--task-intent",
            "tighten-grant-mainline",
            "--format",
            "text",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("当前 grant run:", stdout)
        self.assertIn("当前 workspace:", stdout)
        self.assertIn("当前草稿编号:", stdout)
        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("当前 focus:", stdout)
        self.assertIn("当前动作:", stdout)
        self.assertIn("推荐执行命令:", stdout)
        self.assertNotIn("current_focus:", stdout)
        self.assertNotIn("next_action:", stdout)
        self.assertNotIn("run_recommended_route:", stdout)

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
