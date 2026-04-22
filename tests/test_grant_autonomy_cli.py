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


class GrantAutonomyCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(public_cli_argv(args))
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_execute_grant_autonomy_controller_dispatches_runtime_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "execute-grant-autonomy-controller",
            "grant_autonomy_controller_report": {
                "surface_kind": "grant_autonomy_controller_report",
                "controller_status": "near_submission_candidate",
                "termination_reason": "goal_reached",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload

            with tempfile.TemporaryDirectory() as tmp_dir:
                request_path = Path(tmp_dir) / "autonomy-request.json"
                output_dir = Path(tmp_dir) / "autonomy-output"
                exit_code, stdout, stderr = self.run_cli(
                    "execute-grant-autonomy-controller",
                    "--input",
                    str(request_path),
                    "--output-dir",
                    str(output_dir),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "execute-grant-autonomy-controller",
                "input_path": str(request_path),
                "output_dir": str(output_dir),
            }
        )
