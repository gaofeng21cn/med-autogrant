from __future__ import annotations

import json
import os
import subprocess
import sys

from cli_validate_cases import (
    CliValidateWorkspaceTest,
    EXAMPLE_PATH,
    REPO_ROOT,
    SRC_ROOT,
)


class CliValidateWorkspaceErrorCasesTest(CliValidateWorkspaceTest):
    def assert_workspace_json_error(
        self,
        command: str,
        input_path: object,
        *,
        expected_command: str,
        expected_lifecycle_stage: str,
        expected_path: str,
        expected_message: str,
    ) -> dict[str, object]:
        exit_code, stdout, stderr = self.run_cli(
            "workspace",
            command,
            "--input",
            str(input_path),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], expected_command)
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], expected_lifecycle_stage)
        self.assertEqual(payload["errors"][0]["path"], expected_path)
        self.assertEqual(payload["errors"][0]["message"], expected_message)
        self.assertIn(expected_message.split("。", maxsplit=1)[0], payload["error"])
        return payload

    def test_validate_workspace_json_output(self) -> None:
        payload = self.run_workspace_json("validate", EXAMPLE_PATH)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["error_count"], 0)
        self.assertEqual(payload["errors"], [])

    def test_critique_summary_json_output(self) -> None:
        payload = self.run_workspace_json("critique-summary", EXAMPLE_PATH)
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
        payload = self.run_workspace_json("route-report", EXAMPLE_PATH)
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

        self.assert_workspace_json_error(
            "summarize",
            invalid_path,
            expected_command="summarize-workspace",
            expected_lifecycle_stage="critique",
            expected_path="revision_plans",
            expected_message="critique 阶段必须存在非空 RevisionPlan。",
        )

    def test_next_step_returns_structured_json_error_for_invalid_workspace(self) -> None:
        invalid_path = self.write_invalid_workspace()

        self.assert_workspace_json_error(
            "next-step",
            invalid_path,
            expected_command="next-step",
            expected_lifecycle_stage="critique",
            expected_path="revision_plans",
            expected_message="critique 阶段必须存在非空 RevisionPlan。",
        )

    def test_critique_summary_returns_structured_json_error_for_invalid_workspace(self) -> None:
        invalid_path = self.write_invalid_workspace()

        self.assert_workspace_json_error(
            "critique-summary",
            invalid_path,
            expected_command="critique-summary",
            expected_lifecycle_stage="critique",
            expected_path="revision_plans",
            expected_message="critique 阶段必须存在非空 RevisionPlan。",
        )

    def test_stage_route_report_returns_structured_json_error_for_outline_only_critique_draft(self) -> None:
        invalid_path = self.write_outline_only_critique_workspace()

        self.assert_workspace_json_error(
            "route-report",
            invalid_path,
            expected_command="stage-route-report",
            expected_lifecycle_stage="critique",
            expected_path="application_drafts.status",
            expected_message="critique 阶段的激活草稿 status 必须为 draft 或 revised。",
        )

    def test_next_step_returns_structured_json_error_for_revision_stage_with_outline_draft(self) -> None:
        invalid_path = self.write_revision_outline_workspace()

        self.assert_workspace_json_error(
            "next-step",
            invalid_path,
            expected_command="next-step",
            expected_lifecycle_stage="revision",
            expected_path="application_drafts.status",
            expected_message="revision 阶段的激活草稿 status 必须为 draft 或 revised。",
        )

    def test_validate_workspace_reports_revision_transition_error_when_completed_plan_does_not_switch_status(self) -> None:
        invalid_path = self.write_revision_completed_without_revised_workspace()

        exit_code, stdout, stderr = self.run_cli(
            "workspace",
                "validate",
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

        payload = self.run_workspace_json("next-step", valid_path)
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["current_stage"], "revision")
        self.assertEqual(payload["recommended_stage"], "critique")
        self.assertIn("revised", payload["reason"])
