from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from support.cli import run_cli  # noqa: E402
from med_autogrant.product_entry import MedAutoGrantProductEntry  # noqa: E402


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
FORCED_ROLLBACK_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_forced_rollback_argument.json"
PRESUBMISSION_FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
NON_NSFC_INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nih_r21_workspace_p2a_input_intake.json"



class CliValidateWorkspaceTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        return run_cli(*args, allow_system_exit=False)

    def run_json_cli(self, *args: str) -> dict[str, object]:
        exit_code, stdout, stderr = self.run_cli(*args)
        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        return json.loads(stdout)

    def run_workspace_json(self, command: str, input_path: Path) -> dict[str, object]:
        return self.run_json_cli(
            "workspace",
            command,
            "--input",
            str(input_path),
            "--format",
            "json",
        )

    def assert_next_step_case(
        self,
        example_path: Path,
        current_stage: str,
        recommended_stage: str,
    ) -> dict[str, object]:
        payload = self.run_workspace_json("next-step", example_path)
        self.assertEqual(payload["current_stage"], current_stage)
        self.assertEqual(payload["recommended_stage"], recommended_stage)
        return payload

    def test_validate_workspace_accepts_supported_workspace_profiles(self) -> None:
        cases = [
            (INPUT_EXAMPLE_PATH, "lifecycle_stage", "input_intake"),
            (DIRECTION_EXAMPLE_PATH, "lifecycle_stage", "direction_screening"),
            (ARGUMENT_EXAMPLE_PATH, "lifecycle_stage", "argument_building"),
            (FIT_EXAMPLE_PATH, "lifecycle_stage", "fit_alignment"),
            (OUTLINE_EXAMPLE_PATH, "lifecycle_stage", "outline"),
            (DRAFTING_EXAMPLE_PATH, "lifecycle_stage", "drafting"),
            (CRITIQUE_EXAMPLE_PATH, "lifecycle_stage", "critique"),
            (REVISION_EXAMPLE_PATH, "lifecycle_stage", "revision"),
            (MAJOR_REFRAME_EXAMPLE_PATH, "lifecycle_stage", "critique"),
            (READY_FOR_SUBMISSION_EXAMPLE_PATH, "lifecycle_stage", "critique"),
            (NON_NSFC_INPUT_EXAMPLE_PATH, "workspace_id", "nih-r21-demo-001"),
        ]

        for example_path, field, expected in cases:
            with self.subTest(example=example_path.name):
                payload = self.run_workspace_json("validate", example_path)
                self.assertTrue(payload["ok"])
                self.assertEqual(payload[field], expected)

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

        with patch("med_autogrant.domain_entry.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload
            exit_code, stdout, stderr = self.run_cli(
                "workspace",
                "intake-audit",
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

        with patch("med_autogrant.domain_entry.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload
            exit_code, stdout, stderr = self.run_cli(
                "workspace",
                "evidence-grounding",
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
                    "kind": "hermes_agent",
                },
            },
            "critique_workspace": {
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "lifecycle_stage": "critique",
            },
        }

        with patch("med_autogrant.domain_entry.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload
            exit_code, stdout, stderr = self.run_cli(
                "pass",
                "critique",
                "--input",
                str(DRAFTING_EXAMPLE_PATH),
                "--output",
                "/tmp/critique-output.json",
                "--executor",
                "hermes_agent",
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
                "executor_kind": "hermes_agent",
            }
        )

    def test_grant_progress_plain_text_prefers_shared_human_status_narration(self) -> None:
        from med_autogrant.cli_rendering_parts import _render_text

        payload = MedAutoGrantProductEntry().read_grant_progress(
            input_path=str(CRITIQUE_EXAMPLE_PATH)
        )
        stdout = _render_text("grant-progress", payload)

        self.assertIn("当前阶段: 批注审阅", stdout)
        self.assertIn("当前判断: 当前状态：批注审阅；下一阶段：修订落实；当前卡点：必要性表述仍略偏现象描述。", stdout)
        self.assertIn("下一步建议: 执行 revision plan 中的 P0/P1 项。", stdout)
        self.assertNotIn("current_stage_summary:", stdout)
        self.assertNotIn("next_system_action:", stdout)

    def test_validate_workspace_plain_text_prefers_human_facing_labels(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "workspace",
                "validate",
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
            "workspace",
                "summarize",
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
            "workspace",
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
            "mainline",
            "phase",
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

    def test_grant_user_loop_plain_text_prefers_human_facing_labels(self) -> None:
        from med_autogrant.cli_rendering_parts import _render_text

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )
        stdout = _render_text("grant-user-loop", payload)

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

    def test_next_step_routes_stage_sequence_forward(self) -> None:
        cases = [
            (INPUT_EXAMPLE_PATH, "input_intake", "direction_screening"),
            (DIRECTION_EXAMPLE_PATH, "direction_screening", "question_refinement"),
            (QUESTION_EXAMPLE_PATH, "question_refinement", "argument_building"),
            (ARGUMENT_EXAMPLE_PATH, "argument_building", "fit_alignment"),
            (FIT_EXAMPLE_PATH, "fit_alignment", "outline"),
            (OUTLINE_EXAMPLE_PATH, "outline", "drafting"),
            (DRAFTING_EXAMPLE_PATH, "drafting", "critique"),
            (CRITIQUE_EXAMPLE_PATH, "critique", "revision"),
            (REVISION_EXAMPLE_PATH, "revision", "critique"),
        ]

        for example_path, current_stage, recommended_stage in cases:
            with self.subTest(example=example_path.name):
                self.assert_next_step_case(example_path, current_stage, recommended_stage)

    def test_next_step_routes_major_reframe_back_to_question_refinement(self) -> None:
        payload = self.assert_next_step_case(
            MAJOR_REFRAME_EXAMPLE_PATH,
            "critique",
            "question_refinement",
        )
        self.assertIn("重塑科学问题", payload["reason"])

    def test_next_step_routes_ready_for_submission_to_frozen(self) -> None:
        payload = self.assert_next_step_case(
            READY_FOR_SUBMISSION_EXAMPLE_PATH,
            "critique",
            "frozen",
        )
        self.assertIn("ready_for_submission", payload["reason"])

    def test_next_step_routes_forced_rollback_to_argument_building(self) -> None:
        payload = self.assert_next_step_case(
            FORCED_ROLLBACK_EXAMPLE_PATH,
            "critique",
            "argument_building",
        )
        self.assertEqual(payload["forced_rollback_stage"], "argument_building")
        self.assertIn("forced rollback", payload["reason"])

    def test_next_step_keeps_presubmission_frozen_workspace_at_frozen(self) -> None:
        payload = self.assert_next_step_case(
            PRESUBMISSION_FROZEN_EXAMPLE_PATH,
            "frozen",
            "frozen",
        )
        self.assertTrue(payload["presubmission_frozen"])


if __name__ == "__main__":
    unittest.main()
