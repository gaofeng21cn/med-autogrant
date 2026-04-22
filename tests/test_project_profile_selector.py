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

    def test_selector_attaches_family_grammar_contract_to_nih_profile(self) -> None:
        from med_autogrant.project_profile_selector import build_initialized_intake_workspace, select_project_profile

        selection_input = self._base_selection_input()
        selection_input["selection_input_id"] = "nih-r21-proof-001"
        selection_input["funding_opportunity_pool"] = [
            {
                "brief_id": "nih-r21-2026-nhlbi",
                "funder": "NIH",
                "program_family": "NHLBI R21",
                "project_types": ["exploratory_developmental"],
            }
        ]

        selection = select_project_profile(selection_input)
        profile = selection["recommended_project_profile"]
        grammar = profile["grant_family_grammar"]
        self.assertEqual(grammar["family_id"], "nih_r21_translational_family_v1")
        self.assertEqual(grammar["funder"], "NIH")
        self.assertEqual(
            grammar["template_strategy"]["narrative_style"],
            "significance_innovation_translational",
        )
        self.assertEqual(
            grammar["review_grammar"]["critique_policy"]["policy_id"],
            "nih_r21_significance_innovation_v1",
        )
        self.assertEqual(
            grammar["governance_entry_points"],
            [
                "grant-quality-scorecard",
                "grant-quality-diff",
                "execute-grant-autonomy-controller",
            ],
        )
        workspace, _selection = build_initialized_intake_workspace(selection_input)
        self.assertEqual(
            workspace["project_profile"]["grant_family_grammar"]["family_id"],
            "nih_r21_translational_family_v1",
        )

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

    def test_registry_exposes_common_grammar_and_non_nsfc_placeholder_contract(self) -> None:
        from med_autogrant.grant_family_registry import (
            get_project_profile_preset,
            iter_project_profile_presets,
            list_family_profile_placeholders,
        )

        preset_ids = {preset["preset_id"] for preset in iter_project_profile_presets()}
        self.assertEqual(preset_ids, {"nsfc_general_medical_v1", "nih_r21_translational_v1"})

        nsfc_preset = get_project_profile_preset("nsfc_general_medical_v1")
        nsfc_grammar = nsfc_preset["common_grant_grammar"]
        self.assertEqual(
            nsfc_grammar["template_strategy"]["required_section_strategy"],
            "mirror_funding_brief_mandatory_sections",
        )
        self.assertEqual(
            nsfc_grammar["evidence_policy"]["policy_id"],
            "claim_must_bind_to_track_record_or_preliminary_evidence",
        )
        self.assertEqual(
            nsfc_grammar["review_grammar"]["critique_policy"]["policy_id"],
            "nsfc_mentor_critique_v1",
        )
        self.assertEqual(nsfc_grammar["family_compatibility_hooks"][0]["rule_id"], "rule.funder")

        placeholders = list_family_profile_placeholders()
        self.assertTrue(
            any(
                item["family_id"] == "wellcome_discovery_placeholder_v1"
                and item["funder"] == "Wellcome"
                and item["status"] == "placeholder"
                for item in placeholders
            )
        )

    def test_selector_profile_document_keeps_existing_values_from_common_grammar(self) -> None:
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
        profile = result["recommended_project_profile"]
        self.assertEqual(
            profile["template_profile"]["required_section_strategy"],
            "mirror_funding_brief_mandatory_sections",
        )
        self.assertEqual(
            profile["collaboration_preferences"]["evidence_policy"],
            "significance_and_innovation_claims_require_direct_grounding",
        )
        self.assertEqual(profile["critique_policy"]["policy_id"], "nih_r21_significance_innovation_v1")

    def test_selector_emits_nih_r21_family_grammar_trace_for_portability_proof(self) -> None:
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
        family_trace = result["recommended_project_profile"]["family_grammar_trace"]

        self.assertEqual(family_trace["family_id"], "nih_r21_translational_family_v1")
        self.assertEqual(family_trace["family_label"], "NIH R21 translational family")
        self.assertEqual(family_trace["funder"], "NIH")
        self.assertEqual(family_trace["admission_status"], "admitted")
        self.assertEqual(
            family_trace["template_strategy"]["required_section_strategy"],
            "mirror_funding_brief_mandatory_sections",
        )
        self.assertEqual(
            family_trace["review_grammar"]["review_focus"],
            "significance_and_innovation_weighted_review",
        )
        self.assertEqual(
            family_trace["evidence_policy"]["policy_id"],
            "significance_and_innovation_claims_require_direct_grounding",
        )
        self.assertTrue(
            any(
                item["rule_id"] == "rule.program_family"
                and "NHLBI R21" in item["allowed_values"]
                for item in family_trace["family_compatibility_hooks"]
            )
        )
