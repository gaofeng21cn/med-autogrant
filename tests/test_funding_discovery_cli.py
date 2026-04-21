from __future__ import annotations

import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402
from med_autogrant.public_cli import public_cli_argv  # noqa: E402


DISCOVERY_INPUT = REPO_ROOT / "examples" / "funding_discovery_input_cardiovascular.json"


class FundingDiscoveryCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(public_cli_argv(args))
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_discover_funding_opportunities_returns_candidate_pool(self) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "discover-funding-opportunities",
            "--input",
            str(DISCOVERY_INPUT),
            "--format",
            "json",
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        self.assertGreaterEqual(payload["funding_landscape_discovery"]["candidate_count"], 2)
        brief_ids = [item["brief_id"] for item in payload["funding_landscape_discovery"]["funding_opportunity_pool"]]
        self.assertIn("nsfc-2026-general", brief_ids)
        self.assertIn("nih-r21-2026-nhlbi", brief_ids)

