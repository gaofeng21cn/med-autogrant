from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from support.cli import run_cli  # noqa: E402


FREEZE_READY_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
FORWARD_PROGRESS_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"


class FinalPackageCliCase(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        return run_cli(*args)

    def _build_bundle(self, input_path: Path, output_path: Path) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "package",
            "artifact-bundle",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
