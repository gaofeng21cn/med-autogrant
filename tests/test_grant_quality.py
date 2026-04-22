from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


class GrantQualityScorecardTest(unittest.TestCase):
    def test_scorecard_surfaces_blockers_and_route_recommendation_for_critique_workspace(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        critique_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        scorecard = build_grant_quality_scorecard(critique_workspace)

        self.assertEqual(scorecard["surface_kind"], "grant_quality_scorecard")
        self.assertEqual(scorecard["workspace_id"], "nsfc-demo-001")
        self.assertEqual(scorecard["overall_status"], "blocked")
        self.assertEqual(scorecard["loop_gate"]["action"], "rollback_required")
        self.assertEqual(scorecard["loop_gate"]["recommended_stage"], "argument_building")
        self.assertGreater(scorecard["overall_score"], 0)
        self.assertLessEqual(scorecard["overall_score"], 85)
        dimension_ids = {item["dimension_id"] for item in scorecard["dimensions"]}
        self.assertEqual(
            dimension_ids,
            {
                "scientific_question_validity",
                "necessity_value_closure",
                "applicant_fit",
                "technical_feasibility",
                "claim_evidence_coverage",
                "unresolved_hard_issues",
                "version_issue_closure",
            },
        )
        self.assertIn("必要性表述仍略偏现象描述。", scorecard["unresolved_hard_issues"])
        self.assertTrue(
            any(item["dimension_id"] == "necessity_value_closure" for item in scorecard["tracked_issues"])
        )

    def test_scorecard_marks_frozen_workspace_as_submission_grade_candidate(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        frozen_workspace = _load_json(FROZEN_EXAMPLE_PATH)
        scorecard = build_grant_quality_scorecard(frozen_workspace)

        self.assertEqual(scorecard["overall_status"], "submission_grade_candidate")
        self.assertEqual(scorecard["loop_gate"]["action"], "ready_for_submission")
        self.assertIsNone(scorecard["loop_gate"]["recommended_stage"])
        self.assertEqual(scorecard["unresolved_hard_issues"], [])
        self.assertGreaterEqual(scorecard["overall_score"], 85)

    def test_scorecard_attaches_closure_governance_to_open_hard_issues(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        critique_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        scorecard = build_grant_quality_scorecard(critique_workspace)

        hard_issues = [
            item
            for item in scorecard["tracked_issues"]
            if item["status"] == "open" and item["severity"] == "hard"
        ]
        self.assertTrue(hard_issues)
        for issue in hard_issues:
            with self.subTest(issue=issue["issue_id"]):
                self.assertEqual(issue["closure_status"], "blocked")
                self.assertEqual(issue["blocking_reason"], issue["summary"])
                self.assertIn("summary", issue["recommended_closure_action"])
                self.assertIn("target_stage", issue["recommended_closure_action"])
                self.assertIsInstance(issue["evidence_obligations"], list)

        necessity_issue = next(
            item
            for item in hard_issues
            if item["summary"] == "尚未充分说明为什么现有现象学研究不能回答该机制问题。"
        )
        self.assertIn(
            "从现象相关到未知机制",
            necessity_issue["recommended_closure_action"]["summary"],
        )
        self.assertTrue(
            any(
                "arg-001" in obligation["required_input_ids"]
                for obligation in necessity_issue["evidence_obligations"]
            )
        )
        self.assertIn("lineage_id", necessity_issue)
        self.assertEqual(necessity_issue["lineage_basis"]["anchor_kind"], "revision_item")
        self.assertEqual(
            necessity_issue["lineage_basis"]["anchor_ref"],
            "necessity_value_closure:rev-item-1",
        )

    def test_scorecard_exposes_formal_evidence_supply_queue(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        critique_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        scorecard = build_grant_quality_scorecard(critique_workspace)

        supply_queue = scorecard["evidence_supply_queue"]
        self.assertTrue(supply_queue)
        necessity_gap = next(
            item
            for item in supply_queue
            if item["gap_id"] == "revision_item:necessity_value_closure:rev-item-1"
        )
        self.assertEqual(necessity_gap["gap_kind"], "hard_blocker")
        self.assertIn("arg-001", necessity_gap["required_input_ids"])
        self.assertIn("question-immune-fibrosis", necessity_gap["required_input_ids"])
        self.assertTrue(
            any(issue_id.startswith("necessity_value_closure:") for issue_id in necessity_gap["linked_issue_ids"])
        )
        self.assertEqual(
            necessity_gap["controller_action_hint"]["target_stage"],
            "argument_building",
        )
        self.assertEqual(
            necessity_gap["controller_action_hint"]["action"],
            "rollback_upstream",
        )
        self.assertEqual(necessity_gap["supply_status"], "blocked")
        self.assertTrue(necessity_gap["supply_actions"])

    def test_scorecard_emits_reselection_supply_item_when_family_and_funding_brief_mismatch(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        critique_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        critique_workspace["project_profile"]["grant_family_grammar"] = {
            "family_id": "nih_r21_translational_family_v1",
            "family_label": "NIH R21 translational family",
            "funder": "NIH",
            "admission_status": "admitted",
            "template_strategy": {
                "required_section_strategy": "mirror_funding_brief_mandatory_sections",
                "narrative_style": "significance_innovation_translational",
            },
            "review_grammar": {
                "review_focus": "significance_and_innovation_weighted_review",
                "critique_policy": {
                    "preset_id": "nih_r21_significance_innovation_v1",
                    "policy_id": "nih_r21_significance_innovation_v1",
                },
            },
            "evidence_policy": {
                "policy_id": "significance_and_innovation_claims_require_direct_grounding",
            },
            "governance_policy": {
                "default_tranche": "aims_significance_innovation_loop",
                "preferred_stop_target": "ready_for_submission_after_significance_innovation_lock",
                "quality_bar": {
                    "minimum_score": 78,
                    "blocker_policy": "critical_blockers_must_close",
                    "required_signal_coverage": ["significance", "innovation", "approach_feasibility"],
                },
                "rollback_bias": {
                    "default_rollback_stage": "fit_alignment",
                    "trigger_mode": "innovation_gap_sensitive",
                },
                "evidence_escalation_policy": {
                    "trigger": "significance_or_innovation_claim_unbounded",
                    "escalation_action": "tighten_aim_scope_and_add_translational_anchor",
                    "required_evidence_types": ["publication", "preliminary_result"],
                },
                "controller_defaults": {
                    "target_status": "near_submission_candidate",
                    "require_zero_blockers": True,
                    "require_zero_evidence_gaps": False,
                },
            },
            "family_compatibility_hooks": [
                {
                    "rule_id": "rule.funder",
                    "opportunity_field": "funder",
                    "allowed_values": ["NIH"],
                }
            ],
            "governance_entry_points": [
                "grant-quality-scorecard",
                "grant-quality-diff",
                "execute-grant-autonomy-controller",
            ],
        }

        scorecard = build_grant_quality_scorecard(critique_workspace)

        mismatch_gap = next(
            item
            for item in scorecard["evidence_supply_queue"]
            if item["gap_kind"] == "funding_profile_mismatch"
        )
        self.assertEqual(mismatch_gap["supply_status"], "reselection_required")
        self.assertEqual(
            mismatch_gap["controller_action_hint"]["action"],
            "reselect_project_profile",
        )
        self.assertIn("profile-nsfc-general-medical", mismatch_gap["required_input_ids"])

    def test_closure_dossier_turns_open_issue_lineages_into_closure_packages(self) -> None:
        from med_autogrant.grant_quality import (
            build_grant_quality_closure_dossier,
            build_grant_quality_scorecard,
        )

        critique_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        scorecard = build_grant_quality_scorecard(critique_workspace)
        dossier = build_grant_quality_closure_dossier(critique_workspace)

        self.assertEqual(dossier["surface_kind"], "grant_quality_closure_dossier")
        self.assertEqual(dossier["workspace_id"], scorecard["workspace_id"])
        self.assertEqual(dossier["quality_summary"]["overall_status"], scorecard["overall_status"])
        self.assertEqual(dossier["quality_summary"]["overall_score"], scorecard["overall_score"])
        self.assertEqual(dossier["quality_summary"]["loop_gate"], scorecard["loop_gate"])
        self.assertEqual(
            dossier["evidence_supply_queue_summary"]["total_gap_count"],
            len(scorecard["evidence_supply_queue"]),
        )

        necessity_issue = next(
            item
            for item in scorecard["tracked_issues"]
            if item["summary"] == "尚未充分说明为什么现有现象学研究不能回答该机制问题。"
        )
        necessity_package = next(
            item
            for item in dossier["closure_packages"]
            if item["closure_id"] == necessity_issue["lineage_id"]
        )
        self.assertEqual(
            necessity_package["action"],
            necessity_issue["recommended_closure_action"]["action"],
        )
        self.assertEqual(
            necessity_package["target_stage"],
            necessity_issue["recommended_closure_action"]["target_stage"],
        )
        self.assertEqual(
            necessity_package["linked_issue_ids"],
            [necessity_issue["issue_id"]],
        )
        self.assertTrue(necessity_package["blocking_reasons"])
        self.assertTrue(necessity_package["evidence_obligations"])
        self.assertTrue(necessity_package["acceptance_signals"])

    def test_closure_dossier_keeps_queue_only_reselection_gap_as_package(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_closure_dossier

        critique_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        critique_workspace["project_profile"]["grant_family_grammar"] = {
            "family_id": "nih_r21_translational_family_v1",
            "family_label": "NIH R21 translational family",
            "funder": "NIH",
            "admission_status": "admitted",
            "template_strategy": {
                "required_section_strategy": "mirror_funding_brief_mandatory_sections",
                "narrative_style": "significance_innovation_translational",
            },
            "review_grammar": {
                "review_focus": "significance_and_innovation_weighted_review",
                "critique_policy": {
                    "preset_id": "nih_r21_significance_innovation_v1",
                    "policy_id": "nih_r21_significance_innovation_v1",
                },
            },
            "evidence_policy": {
                "policy_id": "significance_and_innovation_claims_require_direct_grounding",
            },
            "governance_policy": {
                "default_tranche": "aims_significance_innovation_loop",
                "preferred_stop_target": "ready_for_submission_after_significance_innovation_lock",
                "quality_bar": {
                    "minimum_score": 78,
                    "blocker_policy": "critical_blockers_must_close",
                    "required_signal_coverage": ["significance", "innovation", "approach_feasibility"],
                },
                "rollback_bias": {
                    "default_rollback_stage": "fit_alignment",
                    "trigger_mode": "innovation_gap_sensitive",
                },
                "evidence_escalation_policy": {
                    "trigger": "significance_or_innovation_claim_unbounded",
                    "escalation_action": "tighten_aim_scope_and_add_translational_anchor",
                    "required_evidence_types": ["publication", "preliminary_result"],
                },
                "controller_defaults": {
                    "target_status": "near_submission_candidate",
                    "require_zero_blockers": True,
                    "require_zero_evidence_gaps": False,
                },
            },
            "family_compatibility_hooks": [
                {
                    "rule_id": "rule.funder",
                    "opportunity_field": "funder",
                    "allowed_values": ["NIH"],
                }
            ],
            "governance_entry_points": [
                "grant-quality-scorecard",
                "grant-quality-diff",
                "execute-grant-autonomy-controller",
            ],
        }

        dossier = build_grant_quality_closure_dossier(critique_workspace)

        mismatch_package = next(
            item
            for item in dossier["closure_packages"]
            if item["closure_id"] == "funding_profile_mismatch:nsfc-demo-001:nih_r21_translational_family_v1"
        )
        self.assertEqual(mismatch_package["action"], "reselect_project_profile")
        self.assertIsNone(mismatch_package["target_stage"])
        self.assertEqual(mismatch_package["evidence_obligations"], [])
        self.assertIn("funding_profile_mismatch:rule.funder", mismatch_package["linked_issue_ids"])
        self.assertTrue(mismatch_package["acceptance_signals"])


class GrantQualityDiffTest(unittest.TestCase):
    def test_quality_diff_reports_closed_and_remaining_issues(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_diff

        current_workspace = _load_json(FROZEN_EXAMPLE_PATH)
        previous_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        diff = build_grant_quality_diff(
            current_document=current_workspace,
            previous_document=previous_workspace,
        )

        self.assertEqual(diff["surface_kind"], "grant_quality_diff")
        self.assertEqual(diff["overall_progression"], "improved")
        self.assertGreater(diff["score_delta"], 0)
        self.assertIn("必要性表述仍略偏现象描述。", diff["issue_progress"]["closed_issues"])
        self.assertEqual(diff["issue_progress"]["remaining_open_issues"], [])
        closure_progress = diff["issue_progress"]["issue_closure_progress"]
        closed_necessity = next(
            item
            for item in closure_progress
            if item["summary"] == "必要性表述仍略偏现象描述。"
        )
        self.assertEqual(closed_necessity["transition"], "closed")
        self.assertEqual(closed_necessity["previous_closure_status"], "blocked")
        self.assertIsNone(closed_necessity["current_closure_status"])
        self.assertEqual(closed_necessity["closure_delta"], "issue_closed")

    def test_quality_diff_preserves_newly_opened_issue_when_re_review_adds_new_round(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_diff

        current_workspace = _load_json(RE_REVIEW_EXAMPLE_PATH)
        previous_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        diff = build_grant_quality_diff(
            current_document=current_workspace,
            previous_document=previous_workspace,
        )

        self.assertEqual(diff["overall_progression"], "mixed")
        self.assertIn(
            "修订后的研究基础是否与关键实验闭环直接对应",
            diff["issue_progress"]["newly_opened_issues"],
        )
        self.assertIn(
            "必要性表述仍略偏现象描述。",
            diff["issue_progress"]["closed_issues"],
        )
        new_issue_progress = next(
            item
            for item in diff["issue_progress"]["issue_closure_progress"]
            if item["summary"] == "修订后的研究基础是否与关键实验闭环直接对应"
        )
        self.assertEqual(new_issue_progress["transition"], "newly_opened")
        self.assertIsNone(new_issue_progress["previous_closure_status"])
        self.assertEqual(new_issue_progress["current_closure_status"], "blocked")
        self.assertEqual(new_issue_progress["closure_delta"], "new_blocker_opened")

    def test_quality_diff_tracks_same_lineage_when_issue_summary_is_rephrased(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_diff

        previous_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        current_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        current_workspace["mentor_critiques"][0]["necessity_scientific_value"]["blocking_issues"][0] = (
            "现有现象学证据仍未解释该机制缺口。"
        )

        diff = build_grant_quality_diff(
            current_document=current_workspace,
            previous_document=previous_workspace,
        )

        self.assertEqual(diff["overall_progression"], "stable")
        self.assertEqual(diff["issue_progress"]["closed_issues"], [])
        self.assertEqual(diff["issue_progress"]["newly_opened_issues"], [])
        self.assertIn(
            "现有现象学证据仍未解释该机制缺口。",
            diff["issue_progress"]["remaining_open_issues"],
        )
        lineage_progress = next(
            item
            for item in diff["issue_progress"]["issue_closure_progress"]
            if item["lineage_basis"]["anchor_ref"] == "necessity_value_closure:rev-item-1"
        )
        self.assertEqual(lineage_progress["transition"], "still_open")
        self.assertEqual(
            lineage_progress["previous_summary"],
            "尚未充分说明为什么现有现象学研究不能回答该机制问题。",
        )
        self.assertEqual(
            lineage_progress["current_summary"],
            "现有现象学证据仍未解释该机制缺口。",
        )
        self.assertNotEqual(
            lineage_progress["previous_issue_id"],
            lineage_progress["current_issue_id"],
        )
        self.assertEqual(
            lineage_progress["previous_issue_id"].split(":")[0],
            lineage_progress["current_issue_id"].split(":")[0],
        )

    def test_quality_diff_reports_evidence_supply_progress(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_diff

        current_workspace = _load_json(FROZEN_EXAMPLE_PATH)
        previous_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        diff = build_grant_quality_diff(
            current_document=current_workspace,
            previous_document=previous_workspace,
        )

        supply_progress = diff["evidence_supply_progress"]
        self.assertIn(
            "revision_item:necessity_value_closure:rev-item-1",
            supply_progress["closed_gaps"],
        )
        self.assertEqual(supply_progress["remaining_open_gaps"], [])
        progress_entry = next(
            item
            for item in supply_progress["gap_progress"]
            if item["gap_id"] == "revision_item:necessity_value_closure:rev-item-1"
        )
        self.assertEqual(progress_entry["transition"], "closed")
        self.assertEqual(progress_entry["previous_gap_kind"], "hard_blocker")
        self.assertIsNone(progress_entry["current_gap_kind"])
        self.assertIn("arg-001", progress_entry["previous_required_input_ids"])
        self.assertEqual(progress_entry["current_required_input_ids"], [])
        self.assertEqual(progress_entry["supply_delta"], "supply_closed")
        self.assertEqual(
            progress_entry["previous_controller_action_hint"]["action"],
            "rollback_upstream",
        )
