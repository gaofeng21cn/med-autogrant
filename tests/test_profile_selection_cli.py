from __future__ import annotations

import json
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


if "hermes_cli.config" not in sys.modules:
    hermes_cli = types.ModuleType("hermes_cli")
    hermes_cli_config = types.ModuleType("hermes_cli.config")

    def _load_config() -> dict:
        return {}

    hermes_cli_config.load_config = _load_config
    hermes_cli.config = hermes_cli_config
    sys.modules["hermes_cli"] = hermes_cli
    sys.modules["hermes_cli.config"] = hermes_cli_config

if "hermes_constants" not in sys.modules:
    hermes_constants = types.ModuleType("hermes_constants")

    def _parse_reasoning_effort(_value: str) -> dict:
        return {}

    hermes_constants.parse_reasoning_effort = _parse_reasoning_effort
    sys.modules["hermes_constants"] = hermes_constants

if "run_agent" not in sys.modules:
    run_agent = types.ModuleType("run_agent")

    class _AIAgentStub:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        def run_conversation(self, _prompt: str) -> dict:
            return {"completed": True, "api_calls": 0, "final_response": "{}"}

    run_agent.AIAgent = _AIAgentStub
    sys.modules["run_agent"] = run_agent

from med_autogrant.cli import main  # noqa: E402
from med_autogrant.public_cli import public_cli_argv  # noqa: E402


NSFC_SELECTION_INPUT = REPO_ROOT / "examples" / "profile_selection_input_nsfc_general.json"
NIH_SELECTION_INPUT = REPO_ROOT / "examples" / "profile_selection_input_nih_r21.json"


class ProjectProfileSelectionCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(public_cli_argv(args))
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_select_project_profile_returns_nsfc_recommendation(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "select-project-profile",
            "--input",
            str(NSFC_SELECTION_INPUT),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["project_profile_selection"]["recommended_project_profile"]["preset_id"], "nsfc_general_medical_v1")
        self.assertEqual(payload["project_profile_selection"]["recommended_funding_opportunity"]["brief_id"], "nsfc-2026-general")
        self.assertEqual(
            payload["project_profile_selection"]["recommended_project_profile"]["grant_family_grammar"]["governance_policy"]["default_tranche"],
            "direction_screening_to_argument_closure",
        )
        self.assertEqual(
            payload["project_profile_selection"]["selection_summary"]["evaluated_profile_preset_count"],
            2,
        )

    def test_select_project_profile_returns_nih_r21_recommendation(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "select-project-profile",
            "--input",
            str(NIH_SELECTION_INPUT),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["project_profile_selection"]["recommended_project_profile"]["preset_id"], "nih_r21_translational_v1")
        self.assertEqual(payload["project_profile_selection"]["recommended_funding_opportunity"]["brief_id"], "nih-r21-2026-nhlbi")
        self.assertEqual(
            payload["project_profile_selection"]["recommended_project_profile"]["grant_family_grammar"]["family_id"],
            "nih_r21_translational_family_v1",
        )
        self.assertEqual(
            payload["project_profile_selection"]["recommended_project_profile"]["grant_family_grammar"]["governance_policy"]["preferred_stop_target"],
            "ready_for_submission_after_significance_innovation_lock",
        )
        self.assertEqual(
            payload["project_profile_selection"]["selection_summary"]["evaluated_profile_preset_count"],
            2,
        )

    def test_initialize_intake_workspace_materializes_input_intake_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "initialized-workspace.json"

            exit_code, stdout, stderr = self.run_cli(
                "initialize-intake-workspace",
                "--input",
                str(NSFC_SELECTION_INPUT),
                "--output",
                str(output_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["initialized_workspace"]["lifecycle_stage"], "input_intake")
            self.assertEqual(
                payload["initialized_workspace"]["project_profile"]["preset_id"],
                "nsfc_general_medical_v1",
            )
            self.assertTrue(output_path.exists())
