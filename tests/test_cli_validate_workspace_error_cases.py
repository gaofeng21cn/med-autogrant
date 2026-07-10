from __future__ import annotations

import json

from cli_validate_cases import CliValidateWorkspaceTest


class CliValidateWorkspaceErrorCasesTest(CliValidateWorkspaceTest):
    def assert_workspace_error(
        self,
        command: str,
        input_path: object,
        expected_command: str,
        lifecycle_stage: str,
        error_path: str,
    ) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "workspace", command, "--input", str(input_path), "--format", "json"
        )
        payload = json.loads(stdout)
        self.assertEqual((exit_code, stderr), (1, ""))
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["command"], expected_command)
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], lifecycle_stage)
        self.assertEqual(payload["errors"][0]["path"], error_path)
        self.assertTrue(payload["error"])

    def test_workspace_read_surfaces_fail_closed_for_invalid_revisions(self) -> None:
        empty_revision = self.write_invalid_workspace()
        outline_critique = self.write_outline_only_critique_workspace()
        outline_revision = self.write_revision_outline_workspace()
        cases = (
            ("summarize", empty_revision, "summarize-workspace", "critique", "revision_plans"),
            ("next-step", empty_revision, "next-step", "critique", "revision_plans"),
            ("critique-summary", empty_revision, "critique-summary", "critique", "revision_plans"),
            ("route-report", outline_critique, "stage-route-report", "critique", "application_drafts.status"),
            ("next-step", outline_revision, "next-step", "revision", "application_drafts.status"),
        )
        for case in cases:
            with self.subTest(command=case[0], stage=case[3]):
                self.assert_workspace_error(*case)

    def test_completed_revision_requires_revised_draft_status(self) -> None:
        invalid_path = self.write_revision_completed_without_revised_workspace()
        exit_code, stdout, stderr = self.run_cli(
            "workspace", "validate", "--input", str(invalid_path), "--format", "json"
        )
        payload = json.loads(stdout)
        self.assertEqual((exit_code, stderr), (1, ""))
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertGreaterEqual(payload["error_count"], 1)
        self.assertIn("application_drafts.status", {item["path"] for item in payload["errors"]})

    def test_completed_revision_routes_back_to_critique(self) -> None:
        payload = self.run_workspace_json("next-step", self.write_completed_revision_workspace())
        self.assertEqual(payload["current_stage"], "revision")
        self.assertEqual(payload["recommended_stage"], "critique")
