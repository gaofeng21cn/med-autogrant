from __future__ import annotations

import json
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


INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"


class AuthoringMainlineCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(public_cli_argv(args))
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_execute_authoring_mainline_loop_dispatches_runtime_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "execute-authoring-mainline-loop",
            "grant_run_id": "grant-run-demo",
            "workspace_id": "workspace-demo",
            "draft_id": "draft-demo",
            "lifecycle_stage": "drafting",
            "mainline_loop_report": {
                "loop_status": "passed",
                "completed_cycles": 4
            }
        }

        with patch("med_autogrant.domain_entry.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload

            with tempfile.TemporaryDirectory() as tmp_dir:
                exit_code, stdout, stderr = self.run_cli(
                    "execute-authoring-mainline-loop",
                    "--input",
                    str(INPUT_EXAMPLE_PATH),
                    "--output-dir",
                    tmp_dir,
                    "--max-cycles",
                    "6",
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload, expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "execute-authoring-mainline-loop",
                "input_path": str(INPUT_EXAMPLE_PATH),
                "output_dir": unittest.mock.ANY,
                "max_cycles": 6,
            }
        )
