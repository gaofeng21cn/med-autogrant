from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class FundingLandscapeDiscoveryTest(unittest.TestCase):
    NIH_R21_PARENT_HTML = """
    <html>
      <body>
        NIH Exploratory/Developmental Research Project Grant (Parent R21 Clinical Trial Not Allowed)
        <a href="https://simpler.grants.gov/opportunity/357807" target="_blank">PA-25-304</a>
      </body>
    </html>
    """
    NSFC_GUIDE_LIST_HTML = """
    <html>
      <body>
        <a href="/p1/2931/3971/3972/qy2026.html">2026年度国家自然科学基金项目指南</a>
        <a href="/p1/3381/2824/99667.html">关于2026年度国家自然科学基金项目申请与结题等有关事项的通告</a>
      </body>
    </html>
    """
    NSFC_MEDICAL_HTML = """
    <html>
      <body>
        <title>医学科学部</title>
        <div>医学科学部</div>
      </body>
    </html>
    """

    def _base_discovery_input(self) -> dict:
        return {
            "discovery_input_id": "discovery-001",
            "mode": "auto",
            "metadata": {
                "schema_version": "v1",
                "created_at": "2026-04-21T12:00:00Z",
                "updated_at": "2026-04-21T12:00:00Z",
                "source_mode": "auto",
            },
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

    def test_official_live_discovery_returns_official_candidates(self) -> None:
        from med_autogrant.funding_landscape_discovery import (
            OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL,
            OFFICIAL_NSFC_GUIDE_LIST_URL,
            OFFICIAL_NSFC_MEDICAL_GUIDE_URL,
            discover_funding_landscape,
        )

        discovery_input = self._base_discovery_input()
        discovery_input["discovery_source"] = "official_live"

        fixtures = {
            OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL: self.NIH_R21_PARENT_HTML,
            OFFICIAL_NSFC_GUIDE_LIST_URL: self.NSFC_GUIDE_LIST_HTML,
            OFFICIAL_NSFC_MEDICAL_GUIDE_URL: self.NSFC_MEDICAL_HTML,
        }

        result = discover_funding_landscape(
            discovery_input,
            fetch_text=lambda url: fixtures[url],
        )

        self.assertEqual(result["discovery_summary"]["discovery_source"], "official_live")
        self.assertGreaterEqual(result["candidate_count"], 2)
        self.assertEqual(result["discovery_summary"]["source_receipt_count"], 3)
        brief_ids = {item["brief_id"] for item in result["funding_opportunity_pool"]}
        self.assertIn("nsfc-2026-general-medical-live", brief_ids)
        self.assertIn("nih-r21-pa-25-304", brief_ids)
