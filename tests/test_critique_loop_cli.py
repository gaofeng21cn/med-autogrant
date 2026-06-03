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


DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"


class CritiqueLoopCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(public_cli_argv(args))
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_execute_critique_revision_loop_dispatches_runtime_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "execute-critique-revision-loop",
            "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
            "workspace_id": "nsfc-demo-001",
            "draft_id": "draft-v1",
            "lifecycle_stage": "drafting",
            "loop_report": {
                "loop_status": "ready_for_submission",
                "completed_rounds": 2,
            },
        }

        with patch("med_autogrant.domain_entry.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload

            with tempfile.TemporaryDirectory() as tmp_dir:
                attempt_path = Path(tmp_dir) / "opl-stage-attempt.json"
                attempt_path.write_text(
                    json.dumps(
                        {
                            "runtime_owner": "one-person-lab",
                            "executor_kind": "codex_cli",
                            "attempt_lease_ref": "lease:opl/stage-attempt/cli",
                        }
                    ),
                    encoding="utf-8",
                )
                exit_code, stdout, stderr = self.run_cli(
                    "pass",
                    "critique-loop",
                    "--input",
                    str(DRAFTING_EXAMPLE_PATH),
                    "--output-dir",
                    tmp_dir,
                    "--max-rounds",
                    "3",
                    "--opl-stage-attempt",
                    str(attempt_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload, expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "execute-critique-revision-loop",
                "input_path": str(DRAFTING_EXAMPLE_PATH),
                "output_dir": unittest.mock.ANY,
                "max_rounds": 3,
                "opl_stage_attempt": {
                    "runtime_owner": "one-person-lab",
                    "executor_kind": "codex_cli",
                    "attempt_lease_ref": "lease:opl/stage-attempt/cli",
                },
            }
        )
