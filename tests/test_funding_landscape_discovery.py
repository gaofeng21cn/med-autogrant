from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class FundingLandscapeDiscoveryTest(unittest.TestCase):
    def _base_discovery_input(self) -> dict:
        return {
            "applicant_profile": {
                "applicant_id": "applicant-001",
                "research_domains": ["心血管医学", "炎症与纤维化"],
                "methods_stack": ["单细胞测序", "动物模型"],
            },
            "track_record": {
                "track_record_id": "track-001",
                "representative_outputs": [
                    {"output_id": "out-1", "output_type": "paper", "title": "心梗后免疫重塑研究"}
                ],
            },
            "rough_direction_hint": "心梗后炎症窗口的可转化干预探索",
        }

    def test_default_discovery_returns_multiple_candidates(self) -> None:
        from med_autogrant.funding_landscape_discovery import discover_funding_landscape

        result = discover_funding_landscape(self._base_discovery_input())

        self.assertGreaterEqual(result["candidate_count"], 2)
        self.assertEqual(len(result["funding_opportunity_pool"]), result["candidate_count"])
        funders = {item["funder"] for item in result["funding_opportunity_pool"]}
        self.assertIn("NSFC", funders)
        self.assertIn("NIH", funders)

    def test_include_funders_filter_shrinks_pool(self) -> None:
        from med_autogrant.funding_landscape_discovery import discover_funding_landscape

        discovery_input = self._base_discovery_input()
        discovery_input["include_funders"] = ["NSFC"]

        result = discover_funding_landscape(discovery_input)

        self.assertGreaterEqual(result["candidate_count"], 1)
        self.assertTrue(all(item["funder"] == "NSFC" for item in result["funding_opportunity_pool"]))
        self.assertIn("include_funders", result["discovery_summary"]["applied_filters"])

    def test_incompatible_hint_fail_closed(self) -> None:
        from med_autogrant.funding_landscape_discovery import discover_funding_landscape

        discovery_input = self._base_discovery_input()
        discovery_input["rough_direction_hint"] = "天体物理黑洞并合引力波信号处理"

        with self.assertRaisesRegex(ValueError, "fail-closed"):
            discover_funding_landscape(discovery_input)
