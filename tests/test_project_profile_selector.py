from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.grant_family_registry import (  # noqa: E402
    get_project_profile_preset,
    iter_project_profile_presets,
    list_family_profile_placeholders,
)
from med_autogrant.project_profile_selector import (  # noqa: E402
    build_initialized_intake_workspace,
    select_project_profile,
)


NSFC_BRIEF = {"brief_id": "nsfc-2026-general", "funder": "NSFC", "program_family": "医学科学部", "project_types": ["general"]}
NIH_R21_BRIEF = {
    "brief_id": "nih-r21-2026-nhlbi",
    "funder": "NIH",
    "program_family": "NHLBI R21",
    "project_types": ["exploratory_developmental"],
}
WELLCOME_BRIEF = {"brief_id": "wellcome-discovery-2026", "funder": "Wellcome", "program_family": "Discovery Award", "project_types": ["discovery"]}
EU_HORIZON_BRIEF = {"brief_id": "eu-horizon-2026", "funder": "EU", "program_family": "Horizon", "project_types": ["collaborative"]}


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

    def _selection_input_with_brief(self, brief: dict[str, object], *, selection_input_id: str = "selection-001") -> dict:
        selection_input = self._base_selection_input()
        selection_input["selection_input_id"] = selection_input_id
        selection_input["funding_opportunity_pool"] = [dict(brief)]
        return selection_input

    def test_selector_picks_nsfc_profile_when_nsfc_pool_is_compatible(self) -> None:
        selection_input = self._selection_input_with_brief(NSFC_BRIEF)
        result = select_project_profile(selection_input)

        self.assertEqual(result["recommended_project_profile"]["preset_id"], "nsfc_general_medical_v1")
        self.assertEqual(result["recommended_funding_opportunity"]["brief_id"], "nsfc-2026-general")
        self.assertEqual(result["selection_summary"]["decision"], "selected")
        self.assertIn("rule.funder", result["selection_summary"]["reason_codes"])

    def test_selector_picks_nih_r21_profile_when_nih_r21_pool_is_compatible(self) -> None:
        selection_input = self._selection_input_with_brief(NIH_R21_BRIEF)
        result = select_project_profile(selection_input)

        self.assertEqual(result["recommended_project_profile"]["preset_id"], "nih_r21_translational_v1")
        self.assertEqual(result["recommended_funding_opportunity"]["brief_id"], "nih-r21-2026-nhlbi")
        self.assertEqual(result["selection_summary"]["selected_profile_preset_id"], "nih_r21_translational_v1")

    def test_selector_picks_wellcome_profile_when_wellcome_pool_is_compatible(self) -> None:
        selection_input = self._selection_input_with_brief(WELLCOME_BRIEF, selection_input_id="wellcome-proof-001")
        result = select_project_profile(selection_input)

        self.assertEqual(result["recommended_project_profile"]["preset_id"], "wellcome_discovery_v1")
        self.assertEqual(result["recommended_funding_opportunity"]["brief_id"], "wellcome-discovery-2026")
        self.assertEqual(result["selection_summary"]["selected_profile_preset_id"], "wellcome_discovery_v1")
        grammar = result["recommended_project_profile"]["grant_family_grammar"]
        self.assertEqual(grammar["family_id"], "wellcome_discovery_family_v1")
        self.assertEqual(grammar["review_grammar"]["review_focus"], "transformative_potential_and_execution_readiness")
        self.assertEqual(grammar["governance_policy"]["controller_defaults"]["target_status"], "near_submission_candidate")
        workspace, _selection = build_initialized_intake_workspace(selection_input)
        self.assertEqual(
            workspace["project_profile"]["grant_family_grammar"]["family_id"],
            "wellcome_discovery_family_v1",
        )

    def test_selector_attaches_family_grammar_contract_to_nih_profile(self) -> None:
        selection_input = self._selection_input_with_brief(NIH_R21_BRIEF, selection_input_id="nih-r21-proof-001")
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
            ],
        )
        self.assertEqual(
            grammar["governance_policy"]["default_tranche"],
            "aims_significance_innovation_loop",
        )
        self.assertEqual(
            grammar["governance_policy"]["preferred_stop_target"],
            "ready_for_submission_after_significance_innovation_lock",
        )
        self.assertEqual(
            grammar["governance_policy"]["quality_bar"]["minimum_score"],
            78,
        )
        self.assertEqual(
            grammar["governance_policy"]["controller_defaults"]["target_status"],
            "near_submission_candidate",
        )
        workspace, _selection = build_initialized_intake_workspace(selection_input)
        self.assertEqual(
            workspace["project_profile"]["grant_family_grammar"]["family_id"],
            "nih_r21_translational_family_v1",
        )

    def test_selector_fail_closed_when_no_compatible_preset_exists(self) -> None:
        selection_input = self._selection_input_with_brief(EU_HORIZON_BRIEF)
        with self.assertRaisesRegex(ValueError, "未找到兼容的 project profile preset"):
            select_project_profile(selection_input)

    def test_registry_exposes_common_grammar_and_non_nsfc_placeholder_contract(self) -> None:
        preset_ids = {preset["preset_id"] for preset in iter_project_profile_presets()}
        self.assertEqual(
            preset_ids,
            {"nsfc_general_medical_v1", "nih_r21_translational_v1", "wellcome_discovery_v1"},
        )

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
        wellcome_preset = get_project_profile_preset("wellcome_discovery_v1")
        self.assertEqual(
            wellcome_preset["common_grant_grammar"]["review_grammar"]["critique_policy"]["policy_id"],
            "wellcome_discovery_transformative_value_v1",
        )

    def test_nih_profile_document_keeps_common_values_and_family_trace(self) -> None:
        result = select_project_profile(self._selection_input_with_brief(NIH_R21_BRIEF))
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
        self.assertEqual(
            family_trace["governance_policy"]["rollback_bias"]["default_rollback_stage"],
            "fit_alignment",
        )
        self.assertEqual(
            family_trace["governance_policy"]["evidence_escalation_policy"]["trigger"],
            "significance_or_innovation_claim_unbounded",
        )
        self.assertTrue(
            any(
                item["rule_id"] == "rule.program_family"
                and "NHLBI R21" in item["allowed_values"]
                for item in family_trace["family_compatibility_hooks"]
            )
        )

    def test_selector_emits_distinct_family_governance_policy_for_nsfc_and_nih_r21(self) -> None:
        nsfc_input = self._selection_input_with_brief(NSFC_BRIEF, selection_input_id="nsfc-governance-001")
        nih_input = self._selection_input_with_brief(NIH_R21_BRIEF, selection_input_id="nih-governance-001")
        nsfc_profile = select_project_profile(nsfc_input)["recommended_project_profile"]
        nih_profile = select_project_profile(nih_input)["recommended_project_profile"]
        nsfc_policy = nsfc_profile["grant_family_grammar"]["governance_policy"]
        nih_policy = nih_profile["grant_family_grammar"]["governance_policy"]

        self.assertEqual(nsfc_policy["default_tranche"], "direction_screening_to_argument_closure")
        self.assertEqual(nih_policy["default_tranche"], "aims_significance_innovation_loop")
        self.assertEqual(nsfc_policy["preferred_stop_target"], "fit_alignment_locked_before_outline")
        self.assertEqual(
            nih_policy["preferred_stop_target"],
            "ready_for_submission_after_significance_innovation_lock",
        )
        self.assertEqual(nsfc_policy["rollback_bias"]["default_rollback_stage"], "argument_building")
        self.assertEqual(nih_policy["rollback_bias"]["default_rollback_stage"], "fit_alignment")
        self.assertEqual(nsfc_policy["controller_defaults"]["target_status"], "submission_grade_candidate")
        self.assertEqual(nih_policy["controller_defaults"]["target_status"], "near_submission_candidate")
        self.assertGreater(
            nsfc_policy["quality_bar"]["minimum_score"],
            nih_policy["quality_bar"]["minimum_score"],
        )
