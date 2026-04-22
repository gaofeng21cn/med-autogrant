from __future__ import annotations

import json
import sys
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


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class GrantQualityCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(public_cli_argv(args))
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_quality_scorecard_dispatches_domain_entry_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-quality-scorecard",
            "grant_quality_scorecard": {
                "surface_kind": "grant_quality_scorecard",
                "overall_status": "blocked",
                "overall_score": 82,
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "workspace",
                "quality-scorecard",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "grant-quality-scorecard",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
            }
        )

    def test_quality_diff_dispatches_domain_entry_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-quality-diff",
            "grant_quality_diff": {
                "surface_kind": "grant_quality_diff",
                "overall_progression": "improved",
                "score_delta": 12,
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "workspace",
                "quality-diff",
                "--input",
                str(FROZEN_EXAMPLE_PATH),
                "--previous-input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "grant-quality-diff",
                "input_path": str(FROZEN_EXAMPLE_PATH),
                "previous_input_path": str(CRITIQUE_EXAMPLE_PATH),
            }
        )

    def test_quality_closure_dossier_dispatches_domain_entry_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-quality-closure-dossier",
            "grant_quality_closure_dossier": {
                "surface_kind": "grant_quality_closure_dossier",
                "quality_summary": {
                    "overall_status": "blocked",
                    "overall_score": 82,
                },
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "workspace",
                "quality-closure-dossier",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "grant-quality-closure-dossier",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
            }
        )
