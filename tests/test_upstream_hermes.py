from __future__ import annotations

import json
import os
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


REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"


class OptionalHermesProofCliProbeTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_probe_upstream_hermes_dispatches_and_returns_probe_payload(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "probe-upstream-hermes",
            "package_version": "0.8.0",
            "hermes_command": "/tmp/hermes",
            "runtime_root": "/tmp/.hermes",
            "state_db_path": "/tmp/.hermes/state.db",
            "entrypoints": {
                "cli": "hermes",
                "acp": "hermes acp",
                "agent": "run_agent.AIAgent",
                "session_db": "hermes_state.SessionDB",
                "session_manager": "acp_adapter.session.SessionManager",
            },
        }

        with patch("med_autogrant.cli.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload
            exit_code, stdout, stderr = self.run_cli("probe-upstream-hermes", "--format", "json")

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with({"command": "probe-upstream-hermes"})


class MagRuntimeLedgerTest(unittest.TestCase):
    def test_runtime_run_uses_grant_run_ledger_for_attempt_index(self) -> None:
        from med_autogrant.hermes_runtime import MagDomainRuntime

        runtime = MagDomainRuntime()
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "revision-journal.json"
            with patch("med_autogrant.hermes_runtime.MagGrantRunLedger") as ledger_class:
                ledger = ledger_class.return_value
                ledger.record_attempt.return_value = 7

                payload = runtime.run_local(
                    input_path=str(REVISION_EXAMPLE_PATH),
                    journal_path=str(journal_path),
                )

        self.assertEqual(payload["attempt_index"], 7)
        ledger.record_attempt.assert_called_once()
        _, kwargs = ledger.record_attempt.call_args
        self.assertEqual(kwargs["trigger"], "runtime-run")
        self.assertEqual(kwargs["journal_path"], journal_path.resolve())
        self.assertEqual(kwargs["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(kwargs["workspace_id"], "nsfc-demo-001")
        self.assertEqual(kwargs["lifecycle_stage"], "revision")
        self.assertEqual(kwargs["stop_reason"]["code"], "stage_action_required")

    def test_record_attempt_uses_journal_scoped_session_when_grant_run_id_missing(self) -> None:
        from med_autogrant.upstream_hermes import MagGrantRunLedger

        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            journal_path = Path(tmp_dir) / "invalid-journal.json"
            stop_reason = {
                "code": "validation_failed",
                "reason": "missing grant_run_id",
                "current_stage": "revision",
                "recommended_next_stage": "revision",
                "checkpoint_status": None,
                "requires_human_confirmation": False,
                "forced_rollback_stage": None,
                "forced_rollback_reason": None,
            }
            route_report = {
                "ok": False,
                "grant_run_id": None,
                "workspace_id": "nsfc-demo-001",
                "lifecycle_stage": "revision",
                "route": {},
                "checkpoint_status": None,
                "verification_checkpoint": {
                    "checkpoint_status": None,
                    "validation_ok": False,
                },
            }

            with patch.dict(os.environ, {"MED_AUTOGRANT_RUNTIME_STATE_ROOT": str(runtime_root)}, clear=False):
                ledger = MagGrantRunLedger()
                first_attempt = ledger.record_attempt(
                    grant_run_id=None,
                    workspace_id="nsfc-demo-001",
                    trigger="runtime-run",
                    journal_path=journal_path,
                    lifecycle_stage="revision",
                    stop_reason=stop_reason,
                    stage_action_envelope=None,
                    route_report=route_report,
                )
                second_attempt = ledger.record_attempt(
                    grant_run_id=None,
                    workspace_id="nsfc-demo-001",
                    trigger="runtime-resume",
                    journal_path=journal_path,
                    lifecycle_stage="revision",
                    stop_reason=stop_reason,
                    stage_action_envelope=None,
                    route_report=route_report,
                )

        self.assertEqual(first_attempt, 1)
        self.assertEqual(second_attempt, 2)


if __name__ == "__main__":
    unittest.main()
