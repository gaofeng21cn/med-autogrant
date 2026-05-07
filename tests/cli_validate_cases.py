from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from support.cli import run_cli as run_cli_helper  # noqa: E402
from support.cli import run_json_cli as run_json_cli_helper  # noqa: E402
from support.workspaces import (  # noqa: E402
    write_completed_revision_workspace,
    write_empty_revision_items_workspace,
    write_outline_only_critique_workspace,
    write_revision_completed_without_revised_workspace,
    write_revision_outline_workspace,
)


EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_minimal.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
DIRECTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_direction_screening.json"
QUESTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_question_refinement.json"
ARGUMENT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_argument_building.json"
FIT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_fit_alignment.json"
OUTLINE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_outline.json"
DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"
CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
MAJOR_REFRAME_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_major_reframe.json"
READY_FOR_SUBMISSION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FORCED_ROLLBACK_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_forced_rollback_argument.json"
PRESUBMISSION_FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
NON_NSFC_INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nih_r21_workspace_p2a_input_intake.json"



class CliValidateWorkspaceTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        return run_cli_helper(*args, allow_system_exit=False)

    def run_json_cli(self, *args: str) -> dict[str, object]:
        payload = run_json_cli_helper(*args, allow_system_exit=False)
        self.assertIsInstance(payload, dict)
        return payload

    def write_invalid_workspace(self) -> Path:
        return write_empty_revision_items_workspace(EXAMPLE_PATH)

    def write_outline_only_critique_workspace(self) -> Path:
        return write_outline_only_critique_workspace(EXAMPLE_PATH)

    def write_revision_outline_workspace(self) -> Path:
        return write_revision_outline_workspace(EXAMPLE_PATH)

    def write_revision_completed_without_revised_workspace(self) -> Path:
        return write_revision_completed_without_revised_workspace(EXAMPLE_PATH)

    def write_completed_revision_workspace(self) -> Path:
        return write_completed_revision_workspace(EXAMPLE_PATH)
