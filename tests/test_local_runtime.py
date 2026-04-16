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
READY_FOR_SUBMISSION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
FORCED_ROLLBACK_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_forced_rollback_argument.json"
PRESUBMISSION_FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
RE_REVIEW_MAJOR_REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"


class LocalRuntimeCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_run_local_defaults_journal_to_runtime_state_sessions_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            codex_home = Path(tmp_dir) / "codex-home"
            expected_journal_path = (
                codex_home
                / "projects"
                / "med-autogrant"
                / "runtime-state"
                / "sessions"
                / "grant-run-nsfc-demo-001-baseline-001.json"
            )

            with patch.dict(
                os.environ,
                {
                    "CODEX_HOME": str(codex_home),
                    "MED_AUTOGRANT_RUNTIME_STATE_ROOT": "",
                },
                clear=False,
            ):
                exit_code, stdout, stderr = self.run_cli(
                    "run-local",
                    "--input",
                    str(REVISION_EXAMPLE_PATH),
                    "--format",
                    "json",
                )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertEqual(payload["journal_path"], str(expected_journal_path.resolve()))
            self.assertTrue(expected_journal_path.exists())

    def test_run_local_writes_journal_and_stage_action_stop_reason_for_revision_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "revision-journal.json"

            exit_code, stdout, stderr = self.run_cli(
                "run-local",
                "--input",
                str(REVISION_EXAMPLE_PATH),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "run-local")
            self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
            self.assertEqual(payload["draft_id"], "draft-v1")
            self.assertEqual(payload["lifecycle_stage"], "revision")
            self.assertEqual(payload["stop_reason"]["code"], "stage_action_required")
            self.assertEqual(payload["stop_reason"]["recommended_next_stage"], "critique")
            self.assertEqual(payload["stop_reason"]["checkpoint_status"], "forward_progress")
            self.assertEqual(payload["journal_path"], str(journal_path.resolve()))
            self.assertEqual(payload["attempt_index"], 1)
            self.assertTrue(journal_path.exists())

            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            self.assertEqual(journal["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(journal["workspace_id"], "nsfc-demo-001")
            self.assertEqual(journal["latest_stop_reason"]["code"], "stage_action_required")
            self.assertEqual(
                journal["latest_route_report"]["verification_checkpoint"]["checkpoint_status"],
                "forward_progress",
            )
            self.assertEqual(len(journal["attempts"]), 1)
            self.assertEqual(journal["attempts"][0]["trigger"], "run-local")
            self.assertEqual(journal["attempts"][0]["attempt_index"], 1)

    def test_run_local_adds_stage_action_envelope_for_revision_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "revision-envelope-journal.json"

            exit_code, stdout, stderr = self.run_cli(
                "run-local",
                "--input",
                str(REVISION_EXAMPLE_PATH),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            envelope = payload["stage_action_envelope"]
            self.assertIsInstance(envelope, dict)
            self.assertEqual(envelope["envelope_version"], 1)
            self.assertEqual(envelope["status"], "action_required")
            self.assertEqual(envelope["grant_run_id"], payload["grant_run_id"])
            self.assertEqual(envelope["workspace_id"], payload["workspace_id"])
            self.assertEqual(envelope["draft_id"], payload["draft_id"])
            self.assertEqual(envelope["current_stage"], "revision")
            self.assertEqual(envelope["recommended_next_stage"], "critique")
            self.assertEqual(envelope["checkpoint_status"], "forward_progress")
            self.assertFalse(envelope["requires_human_confirmation"])
            self.assertEqual(
                envelope["selection"],
                {
                    "selected_direction_id": "dir-inflammatory-remodeling",
                    "selected_question_id": "question-immune-fibrosis",
                    "active_fit_mapping_id": "fit-001",
                    "active_draft_id": "draft-v1",
                    "active_revision_plan_id": "revision-v1",
                },
            )
            self.assertEqual(
                envelope["action_items"],
                [
                    {
                        "index": 1,
                        "instruction": "提交 revised 草稿进入新一轮导师批注。",
                    },
                    {
                        "index": 2,
                        "instruction": "基于 comparison_summary 核对本轮修订是否覆盖前一轮 blocking issues。",
                    },
                ],
            )
            self.assertIn("revised 草稿", envelope["route_reason"])
            self.assertEqual(
                envelope["resume_decision"],
                {
                    "command": "resume-local",
                    "journal_path": str(journal_path.resolve()),
                    "append_attempt": True,
                    "reuse_grant_run_id": True,
                },
            )

            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            self.assertEqual(journal["latest_stage_action_envelope"], envelope)
            self.assertEqual(journal["attempts"][0]["stage_action_envelope"], envelope)

    def test_run_local_adds_stage_action_envelope_for_critique_major_revision_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "major-revision-envelope-journal.json"

            exit_code, stdout, stderr = self.run_cli(
                "run-local",
                "--input",
                str(RE_REVIEW_MAJOR_REVISION_EXAMPLE_PATH),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            envelope = payload["stage_action_envelope"]
            self.assertIsInstance(envelope, dict)
            self.assertEqual(envelope["current_stage"], "critique")
            self.assertEqual(envelope["recommended_next_stage"], "revision")
            self.assertEqual(envelope["selection"]["active_revision_plan_id"], "revision-v2")
            self.assertEqual(
                envelope["action_items"],
                [
                    {
                        "index": 1,
                        "instruction": "执行 revision plan 中的 P0/P1 项。",
                    },
                    {
                        "index": 2,
                        "instruction": "修订后重新进入导师批注闭环。",
                    },
                ],
            )

    def test_run_local_accepts_re_review_revised_output_after_execute_revision_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            revised_output = Path(tmp_dir) / "p3b-revised.json"
            journal_path = Path(tmp_dir) / "p3b-revised-journal.json"

            execute_exit, execute_stdout, execute_stderr = self.run_cli(
                "execute-revision-pass",
                "--input",
                str(RE_REVIEW_MAJOR_REVISION_EXAMPLE_PATH),
                "--output",
                str(revised_output),
                "--format",
                "json",
            )

            self.assertEqual(execute_exit, 0)
            self.assertEqual(execute_stderr, "")
            self.assertTrue(json.loads(execute_stdout)["ok"])

            exit_code, stdout, stderr = self.run_cli(
                "run-local",
                "--input",
                str(revised_output),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["lifecycle_stage"], "critique")
            self.assertEqual(payload["stop_reason"]["code"], "stage_action_required")
            self.assertEqual(payload["stop_reason"]["recommended_next_stage"], "revision")
            self.assertIsInstance(payload["stage_action_envelope"], dict)
            self.assertEqual(payload["stage_action_envelope"]["current_stage"], "critique")
            self.assertEqual(payload["stage_action_envelope"]["recommended_next_stage"], "revision")
            self.assertEqual(payload["stage_action_envelope"]["selection"]["active_revision_plan_id"], "revision-v2")

            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            self.assertEqual(
                journal["latest_route_report"]["verification_checkpoint"]["review_checkpoint"]["reviewed_revision_evidence"][
                    "revision_plan_id"
                ],
                "revision-v1",
            )
            self.assertEqual(journal["latest_stop_reason"]["code"], "stage_action_required")

    def test_non_stage_action_stop_reasons_do_not_emit_stage_action_envelope(self) -> None:
        cases = (
            (FORCED_ROLLBACK_EXAMPLE_PATH, "rollback.json"),
            (READY_FOR_SUBMISSION_EXAMPLE_PATH, "freeze-ready.json"),
            (PRESUBMISSION_FROZEN_EXAMPLE_PATH, "frozen.json"),
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            for input_path, journal_name in cases:
                with self.subTest(input_path=input_path.name):
                    journal_path = Path(tmp_dir) / journal_name
                    exit_code, stdout, stderr = self.run_cli(
                        "run-local",
                        "--input",
                        str(input_path),
                        "--journal",
                        str(journal_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 0)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertIsNone(payload["stage_action_envelope"])

                    journal = json.loads(journal_path.read_text(encoding="utf-8"))
                    self.assertIsNone(journal["latest_stage_action_envelope"])
                    self.assertIsNone(journal["attempts"][0]["stage_action_envelope"])

    def test_run_local_surfaces_rollback_required_stop_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "rollback-journal.json"

            exit_code, stdout, stderr = self.run_cli(
                "run-local",
                "--input",
                str(FORCED_ROLLBACK_EXAMPLE_PATH),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stop_reason"]["code"], "rollback_required")
            self.assertEqual(payload["stop_reason"]["checkpoint_status"], "rollback_required")
            self.assertEqual(payload["stop_reason"]["forced_rollback_stage"], "argument_building")
            self.assertIn("失真", payload["stop_reason"]["forced_rollback_reason"])

    def test_run_local_surfaces_freeze_ready_stop_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "freeze-ready-journal.json"

            exit_code, stdout, stderr = self.run_cli(
                "run-local",
                "--input",
                str(READY_FOR_SUBMISSION_EXAMPLE_PATH),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stop_reason"]["code"], "freeze_ready")
            self.assertEqual(payload["stop_reason"]["checkpoint_status"], "freeze_ready")
            self.assertTrue(payload["stop_reason"]["requires_human_confirmation"])
            self.assertEqual(payload["stop_reason"]["recommended_next_stage"], "frozen")

    def test_run_local_surfaces_presubmission_frozen_stop_reason(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "frozen-journal.json"

            exit_code, stdout, stderr = self.run_cli(
                "run-local",
                "--input",
                str(PRESUBMISSION_FROZEN_EXAMPLE_PATH),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["stop_reason"]["code"], "presubmission_frozen")
            self.assertEqual(payload["stop_reason"]["checkpoint_status"], "submission_frozen")
            self.assertEqual(payload["stop_reason"]["recommended_next_stage"], "frozen")

    def test_run_local_validation_failed_path_keeps_route_checkpoint_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            invalid_workspace = Path(tmp_dir) / "invalid-workspace.json"
            journal_path = Path(tmp_dir) / "invalid-journal.json"
            document = json.loads(REVISION_EXAMPLE_PATH.read_text(encoding="utf-8"))
            document.pop("grant_run_id")
            invalid_workspace.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")

            exit_code, stdout, stderr = self.run_cli(
                "run-local",
                "--input",
                str(invalid_workspace),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["command"], "run-local")
            self.assertEqual(payload["attempt_index"], 1)
            self.assertEqual(payload["stop_reason"]["code"], "validation_failed")
            self.assertIsNone(payload["stop_reason"]["checkpoint_status"])
            self.assertEqual(payload["stop_reason"]["current_stage"], "revision")
            self.assertEqual(payload["stop_reason"]["recommended_next_stage"], "revision")
            self.assertIsNone(payload["stage_action_envelope"])

            route_report = payload["route_report"]
            self.assertFalse(route_report["ok"])
            self.assertIsNone(route_report["checkpoint_status"])
            self.assertEqual(route_report["lifecycle_stage"], "revision")
            self.assertIsInstance(route_report["route"], dict)
            self.assertFalse(route_report["route"]["validate_workspace"]["ok"])
            self.assertGreater(route_report["route"]["validate_workspace"]["error_count"], 0)
            self.assertIsNone(route_report["route"]["summarize_workspace"])
            self.assertIsNone(route_report["route"]["critique_summary"])
            self.assertEqual(route_report["route"]["next_step"]["current_stage"], "revision")
            self.assertEqual(route_report["route"]["next_step"]["recommended_stage"], "revision")
            self.assertEqual(route_report["route"]["next_step"]["reason"], payload["stop_reason"]["reason"])
            self.assertEqual(route_report["route"]["next_step"]["actions"], [])
            self.assertFalse(route_report["route"]["next_step"]["requires_human_confirmation"])

            verification_checkpoint = route_report["verification_checkpoint"]
            self.assertIsInstance(verification_checkpoint, dict)
            self.assertIsNone(verification_checkpoint["checkpoint_status"])
            self.assertFalse(verification_checkpoint["validation_ok"])

            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            self.assertEqual(journal["latest_stop_reason"]["code"], "validation_failed")
            self.assertIsNone(journal["latest_stage_action_envelope"])
            self.assertIsNone(journal["latest_route_report"]["checkpoint_status"])
            self.assertIsInstance(journal["latest_route_report"]["route"], dict)
            self.assertIsInstance(journal["latest_route_report"]["verification_checkpoint"], dict)
            self.assertFalse(journal["latest_route_report"]["verification_checkpoint"]["validation_ok"])

    def test_resume_local_validation_failed_path_keeps_route_checkpoint_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            invalid_workspace = Path(tmp_dir) / "invalid-workspace.json"
            journal_path = Path(tmp_dir) / "invalid-journal.json"
            document = json.loads(REVISION_EXAMPLE_PATH.read_text(encoding="utf-8"))
            document.pop("grant_run_id")
            invalid_workspace.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")

            first_exit, first_stdout, first_stderr = self.run_cli(
                "run-local",
                "--input",
                str(invalid_workspace),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )
            self.assertEqual(first_exit, 0)
            self.assertEqual(first_stderr, "")
            self.assertFalse(json.loads(first_stdout)["ok"])

            second_exit, second_stdout, second_stderr = self.run_cli(
                "resume-local",
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(second_exit, 0)
            self.assertEqual(second_stderr, "")
            payload = json.loads(second_stdout)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["command"], "resume-local")
            self.assertEqual(payload["attempt_index"], 2)
            self.assertEqual(payload["stop_reason"]["code"], "validation_failed")
            self.assertIsNone(payload["stop_reason"]["checkpoint_status"])
            self.assertIsNone(payload["stage_action_envelope"])
            self.assertIsNone(payload["route_report"]["checkpoint_status"])
            self.assertIsInstance(payload["route_report"]["route"], dict)
            self.assertEqual(payload["route_report"]["route"]["next_step"]["recommended_stage"], "revision")
            self.assertIsInstance(payload["route_report"]["verification_checkpoint"], dict)
            self.assertFalse(payload["route_report"]["verification_checkpoint"]["validation_ok"])

            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            self.assertEqual(len(journal["attempts"]), 2)
            self.assertEqual(journal["attempts"][1]["trigger"], "resume-local")
            self.assertEqual(journal["attempts"][1]["attempt_index"], 2)
            self.assertEqual(journal["latest_stop_reason"]["code"], "validation_failed")
            self.assertIsInstance(journal["latest_route_report"]["verification_checkpoint"], dict)

    def test_resume_local_reuses_journal_input_and_appends_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "resume-journal.json"

            first_exit, first_stdout, first_stderr = self.run_cli(
                "run-local",
                "--input",
                str(REVISION_EXAMPLE_PATH),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )
            self.assertEqual(first_exit, 0)
            self.assertEqual(first_stderr, "")
            first_payload = json.loads(first_stdout)
            self.assertEqual(first_payload["attempt_index"], 1)

            second_exit, second_stdout, second_stderr = self.run_cli(
                "resume-local",
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(second_exit, 0)
            self.assertEqual(second_stderr, "")
            second_payload = json.loads(second_stdout)
            self.assertTrue(second_payload["ok"])
            self.assertEqual(second_payload["command"], "resume-local")
            self.assertEqual(second_payload["grant_run_id"], first_payload["grant_run_id"])
            self.assertEqual(second_payload["workspace_id"], first_payload["workspace_id"])
            self.assertEqual(second_payload["stop_reason"]["code"], "stage_action_required")
            self.assertEqual(second_payload["attempt_index"], 2)
            self.assertEqual(second_payload["stage_action_envelope"]["current_stage"], "revision")
            self.assertEqual(second_payload["stage_action_envelope"]["recommended_next_stage"], "critique")

            journal = json.loads(journal_path.read_text(encoding="utf-8"))
            self.assertEqual(len(journal["attempts"]), 2)
            self.assertEqual(journal["attempts"][0]["trigger"], "run-local")
            self.assertEqual(journal["attempts"][1]["trigger"], "resume-local")
            self.assertEqual(journal["attempts"][1]["attempt_index"], 2)
            self.assertEqual(
                journal["attempts"][1]["stage_action_envelope"]["resume_decision"]["journal_path"],
                str(journal_path.resolve()),
            )
            self.assertEqual(
                journal["latest_stage_action_envelope"]["recommended_next_stage"],
                "critique",
            )

    def test_run_local_rejects_journal_reuse_with_different_input_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "shared-journal.json"

            first_exit, _, first_stderr = self.run_cli(
                "run-local",
                "--input",
                str(REVISION_EXAMPLE_PATH),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )
            self.assertEqual(first_exit, 0)
            self.assertEqual(first_stderr, "")

            second_exit, second_stdout, second_stderr = self.run_cli(
                "run-local",
                "--input",
                str(READY_FOR_SUBMISSION_EXAMPLE_PATH),
                "--journal",
                str(journal_path),
                "--format",
                "json",
            )

            self.assertEqual(second_exit, 1)
            self.assertEqual(second_stderr, "")
            payload = json.loads(second_stdout)
            self.assertFalse(payload["ok"])
            self.assertEqual(payload["command"], "run-local")
            self.assertIn("input_path", payload["error"])


if __name__ == "__main__":
    unittest.main()
