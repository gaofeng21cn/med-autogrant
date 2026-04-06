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


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402


EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_minimal.json"


class CliValidateWorkspaceTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(list(args))
        return exit_code, stdout.getvalue(), stderr.getvalue()

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
                "summarize-workspace",
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
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "critique")
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
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["lifecycle_stage"], "revision")
        self.assertEqual(payload["errors"][0]["path"], "application_drafts.status")
        self.assertEqual(payload["errors"][0]["message"], "revision 阶段的激活草稿 status 必须为 draft 或 revised。")
        self.assertIn("revision 阶段的激活草稿 status 必须为 draft 或 revised", payload["error"])

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


if __name__ == "__main__":
    unittest.main()
