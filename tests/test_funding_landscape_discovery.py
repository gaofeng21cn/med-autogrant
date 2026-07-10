from __future__ import annotations

import copy
import unittest

from med_autogrant.funding_landscape_discovery import (  # noqa: E402
    OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL,
    OFFICIAL_NSFC_GUIDE_LIST_URL,
    OFFICIAL_NSFC_MEDICAL_GUIDE_URL,
    build_funding_landscape_cache,
    build_funding_landscape_diff_report,
    discover_funding_landscape,
)


class FundingLandscapeDiscoveryTest(unittest.TestCase):
    def base_input(self) -> dict[str, object]:
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

    def cache_snapshot(self) -> dict[str, object]:
        item = {
            "metadata": {
                "schema_version": "v1",
                "created_at": "2026-04-22T08:00:00Z",
                "updated_at": "2026-04-22T08:00:00Z",
                "source_mode": "auto",
            },
            "brief_id": "nih-r21-pa-25-304",
            "funder": "NIH",
            "program_family": "NIH R21 Parent",
            "project_types": ["exploratory_developmental"],
            "application_year": 2025,
            "mandatory_sections": ["Significance"],
            "formal_constraints": ["official opportunity"],
            "evaluation_notes": ["significance and innovation"],
        }
        return {
            "cache_version": 1,
            "cache_kind": "funding_landscape_cache",
            "discovery_input_id": "discovery-001",
            "refreshed_at": "2026-04-22T08:00:00Z",
            "sources": [
                {
                    "source_id": "nih_parent_announcements",
                    "source_kind": "official_html",
                    "source_url": OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL,
                    "fetched_at": "2026-04-22T08:00:00Z",
                    "item_count": 1,
                    "funding_opportunity_pool": [item],
                }
            ],
            "funding_opportunity_pool": [item],
        }

    def test_filter_and_incompatible_hint_fail_closed(self) -> None:
        filtered_input = self.base_input()
        filtered_input["include_funders"] = ["NSFC"]
        filtered = discover_funding_landscape(filtered_input)

        self.assertGreaterEqual(filtered["candidate_count"], 1)
        self.assertTrue(all(item["funder"] == "NSFC" for item in filtered["funding_opportunity_pool"]))
        self.assertIn("include_funders", filtered["discovery_summary"]["applied_filters"])

        incompatible = self.base_input()
        incompatible["rough_direction_hint"] = "天体物理黑洞并合引力波信号处理"
        with self.assertRaisesRegex(ValueError, "fail-closed"):
            discover_funding_landscape(incompatible)

    def test_default_discovery_keeps_multiple_funders_and_provenance(self) -> None:
        result = discover_funding_landscape(self.base_input())

        self.assertGreaterEqual(result["candidate_count"], 2)
        self.assertEqual(len(result["funding_opportunity_pool"]), result["candidate_count"])
        self.assertTrue({"NSFC", "NIH"} <= {item["funder"] for item in result["funding_opportunity_pool"]})
        provenance = {item["brief_id"]: item for item in result["funding_opportunity_provenance"]}
        self.assertEqual(provenance["nsfc-2026-general"]["provenance_status"], "repo_catalog_static")
        self.assertEqual(provenance["nsfc-2026-general"]["provenance_score"], 50)

    def test_fake_fetch_and_cached_discovery_modes(self) -> None:
        live_input = self.base_input()
        live_input["discovery_source"] = "official_live"
        fixtures = {
            OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL: (
                "NIH Exploratory/Developmental Research Project Grant "
                '(Parent R21 Clinical Trial Not Allowed) <a href="https://simpler.grants.gov/'
                'opportunity/357807">PA-25-304</a>'
            ),
            OFFICIAL_NSFC_GUIDE_LIST_URL: '<a href="/p1/2931/3971/3972/qy2026.html">2026年度国家自然科学基金项目指南</a>',
            OFFICIAL_NSFC_MEDICAL_GUIDE_URL: "<title>医学科学部</title>",
        }
        live = discover_funding_landscape(live_input, fetch_text=fixtures.__getitem__)
        self.assertEqual(live["discovery_summary"]["source_receipt_count"], 3)
        self.assertIn("nih-r21-pa-25-304", {item["brief_id"] for item in live["funding_opportunity_pool"]})

        cached_input = self.base_input()
        cached_input["discovery_source"] = "official_cached"
        cached = discover_funding_landscape(cached_input, cached_snapshot=self.cache_snapshot())
        self.assertEqual(cached["candidate_count"], 1)
        self.assertEqual(cached["funding_opportunity_pool"][0]["brief_id"], "nih-r21-pa-25-304")
        self.assertEqual(cached["discovery_summary"]["source_receipt_count"], 1)

    def test_cache_refresh_reports_added_official_entries(self) -> None:
        fixtures = {
            OFFICIAL_NIH_PARENT_ANNOUNCEMENTS_URL: (
                "NIH Exploratory/Developmental Research Project Grant "
                '(Parent R21 Clinical Trial Not Allowed) <a href="https://simpler.grants.gov/'
                'opportunity/357807">PA-25-304</a>'
            ),
            OFFICIAL_NSFC_GUIDE_LIST_URL: '<a href="/p1/2931/3971/3972/qy2026.html">2026年度国家自然科学基金项目指南</a>',
            OFFICIAL_NSFC_MEDICAL_GUIDE_URL: "<title>医学科学部</title>",
        }
        previous = self.cache_snapshot()
        current = build_funding_landscape_cache(
            self.base_input(),
            fetch_text=fixtures.__getitem__,
            existing_snapshot=previous,
        )
        diff = build_funding_landscape_diff_report(previous_snapshot=previous, current_snapshot=current)

        self.assertEqual(diff["report_kind"], "funding_landscape_diff_report")
        self.assertGreaterEqual(diff["added_count"], 1)
        self.assertIn("added", {item["change_status"] for item in diff["changes"]})

    def test_cache_diff_marks_withdrawn_entries(self) -> None:
        current = self.cache_snapshot()
        previous = copy.deepcopy(current)
        withdrawn = copy.deepcopy(previous["funding_opportunity_pool"][0])
        withdrawn["brief_id"] = "nih-r21-pa-24-001"
        previous["sources"][0]["funding_opportunity_pool"].append(withdrawn)
        previous["sources"][0]["item_count"] = 2
        previous["funding_opportunity_pool"].append(withdrawn)

        diff = build_funding_landscape_diff_report(previous_snapshot=previous, current_snapshot=current)

        self.assertEqual(diff["withdrawn_count"], 1)
        self.assertEqual(
            next(item["brief_id"] for item in diff["changes"] if item["change_status"] == "withdrawn_or_not_listed"),
            "nih-r21-pa-24-001",
        )
