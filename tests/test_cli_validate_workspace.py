from __future__ import annotations

import json
import os
import subprocess
import sys
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


if __name__ == "__main__":
    unittest.main()
