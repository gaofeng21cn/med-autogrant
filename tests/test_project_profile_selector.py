from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class ProjectProfileSelectorTest(unittest.TestCase):
    def _base_selection_input(self) -> dict:
        return {
            "selection_input_id": "selection-001",
            "applicant_profile": {"applicant_id": "applicant-001"},
            "track_record": {"track_record_id": "track-001"},
            "active_project_set": {"project_set_id": "projects-001"},
            "preliminary_evidence_pack": {"evidence_pack_id": "prelim-001"},
            "funding_opportunity_pool": [],
        }

    def test_selector_picks_nsfc_profile_when_nsfc_pool_is_compatible(self) -> None:
        from med_autogrant.project_profile_selector import select_project_profile

        selection_input = self._base_selection_input()
        selection_input["funding_opportunity_pool"] = [
            {
                "brief_id": "nsfc-2026-general",
                "funder": "NSFC",
                "program_family": "医学科学部",
                "project_types": ["general"],
            }
        ]

        result = select_project_profile(selection_input)

        self.assertEqual(result["recommended_project_profile"]["preset_id"], "nsfc_general_medical_v1")
        self.assertEqual(result["recommended_funding_opportunity"]["brief_id"], "nsfc-2026-general")
        self.assertEqual(result["selection_summary"]["decision"], "selected")
        self.assertIn("rule.funder", result["selection_summary"]["reason_codes"])

    def test_selector_picks_nih_r21_profile_when_nih_r21_pool_is_compatible(self) -> None:
        from med_autogrant.project_profile_selector import select_project_profile

        selection_input = self._base_selection_input()
        selection_input["funding_opportunity_pool"] = [
            {
                "brief_id": "nih-r21-2026-nhlbi",
                "funder": "NIH",
                "program_family": "NHLBI R21",
                "project_types": ["exploratory_developmental"],
            }
        ]

        result = select_project_profile(selection_input)

        self.assertEqual(result["recommended_project_profile"]["preset_id"], "nih_r21_translational_v1")
        self.assertEqual(result["recommended_funding_opportunity"]["brief_id"], "nih-r21-2026-nhlbi")
        self.assertEqual(result["selection_summary"]["selected_profile_preset_id"], "nih_r21_translational_v1")

    def test_selector_fail_closed_when_no_compatible_preset_exists(self) -> None:
        from med_autogrant.project_profile_selector import select_project_profile

        selection_input = self._base_selection_input()
        selection_input["funding_opportunity_pool"] = [
            {
                "brief_id": "eu-horizon-2026",
                "funder": "EU",
                "program_family": "Horizon",
                "project_types": ["collaborative"],
            }
        ]

        with self.assertRaisesRegex(ValueError, "未找到兼容的 project profile preset"):
            select_project_profile(selection_input)
