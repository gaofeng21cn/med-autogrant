from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
from support.cli import run_cli  # noqa: E402


DISCOVERY_INPUT = REPO_ROOT / "examples" / "funding_discovery_input_cardiovascular.json"
CRITIQUE_WORKSPACE = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
FROZEN_WORKSPACE = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class PublicCliDispatchTest(unittest.TestCase):
    def test_public_commands_dispatch_domain_requests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            cases = (
                (
                    (
                        "workspace", "refresh-funding-cache", "--input", str(DISCOVERY_INPUT),
                        "--output", f"{tmp_dir}/funding-cache.json", "--format", "json",
                    ),
                    {
                        "command": "refresh-funding-opportunities-cache",
                        "input_path": str(DISCOVERY_INPUT),
                        "output_path": f"{tmp_dir}/funding-cache.json",
                    },
                ),
                (
                    ("workspace", "quality-scorecard", "--input", str(CRITIQUE_WORKSPACE), "--format", "json"),
                    {"command": "grant-quality-scorecard", "input_path": str(CRITIQUE_WORKSPACE)},
                ),
                (
                    (
                        "workspace", "quality-diff", "--input", str(FROZEN_WORKSPACE),
                        "--previous-input", str(CRITIQUE_WORKSPACE), "--format", "json",
                    ),
                    {
                        "command": "grant-quality-diff",
                        "input_path": str(FROZEN_WORKSPACE),
                        "previous_input_path": str(CRITIQUE_WORKSPACE),
                    },
                ),
                (
                    ("workspace", "quality-closure-dossier", "--input", str(CRITIQUE_WORKSPACE), "--format", "json"),
                    {"command": "grant-quality-closure-dossier", "input_path": str(CRITIQUE_WORKSPACE)},
                ),
            )

            for argv, expected_request in cases:
                with self.subTest(command=expected_request["command"]), patch(
                    "med_autogrant.domain_entry.MedAutoGrantDomainEntry"
                ) as entry_class:
                    entry_class.return_value.dispatch.return_value = {
                        "ok": True,
                        "command": expected_request["command"],
                    }
                    exit_code, stdout, stderr = run_cli(*argv, allow_system_exit=False)

                    self.assertEqual((exit_code, stderr), (0, ""))
                    self.assertEqual(json.loads(stdout)["command"], expected_request["command"])
                    entry_class.return_value.dispatch.assert_called_once_with(expected_request)

    def test_discover_funding_public_cli_smoke(self) -> None:
        exit_code, stdout, stderr = run_cli(
            "workspace",
            "discover-funding",
            "--input",
            str(DISCOVERY_INPUT),
            "--format",
            "json",
            allow_system_exit=False,
        )

        payload = json.loads(stdout)
        self.assertEqual((exit_code, stderr), (0, ""))
        self.assertTrue(payload["ok"])
        self.assertGreaterEqual(payload["funding_landscape_discovery"]["candidate_count"], 2)


if __name__ == "__main__":
    unittest.main()
