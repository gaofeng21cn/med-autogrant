from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
from med_autogrant.grant_quality import build_grant_quality_diff, build_grant_quality_scorecard  # noqa: E402


EXAMPLES = REPO_ROOT / "examples"
CRITIQUE_PATH = EXAMPLES / "nsfc_workspace_p2c_critique.json"
RE_REVIEW_PATH = EXAMPLES / "nsfc_workspace_p3b_re_review_major_revision.json"
FROZEN_PATH = EXAMPLES / "nsfc_workspace_p3c_presubmission_frozen.json"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def active_critique(document: dict[str, object]) -> dict[str, object]:
    plan_id = document["current_selection"]["active_revision_plan_id"]
    plan = next(item for item in document["revision_plans"] if item["revision_plan_id"] == plan_id)
    return next(item for item in document["mentor_critiques"] if item["critique_id"] == plan["critique_id"])


def set_owner(document: dict[str, object], owner: str | None, *, independent: bool = False) -> None:
    critique = active_critique(document)
    metadata = critique.setdefault("metadata", {})
    if owner is None:
        metadata.pop("owner", None)
        metadata.pop("independent_review_evidence", None)
        return
    metadata["owner"] = owner
    if independent:
        critique_id = critique["critique_id"]
        metadata["independent_review_evidence"] = {
            "execution_attempt_ref": f"codex_cli::grant-run::{critique_id}",
            "review_attempt_ref": f"mentor_critiques::{critique_id}",
            "review_receipt_ref": f"mentor_critiques::{critique_id}::metadata.independent_review_evidence",
            "no_shared_context_verified": True,
            "reviewer_owner": owner,
            "reviewer_agent_ref": "codex_cli::critique_executor",
        }


class GrantQualityScorecardTest(unittest.TestCase):
    def test_scorecard_surfaces_blockers_and_route_recommendation_for_critique_workspace(self) -> None:
        document = load(CRITIQUE_PATH)
        set_owner(document, "Codex CLI critique executor", independent=True)
        scorecard = build_grant_quality_scorecard(document)

        self.assertEqual(scorecard["overall_status"], "blocked")
        self.assertEqual(scorecard["loop_gate"]["action"], "rollback_required")
        self.assertEqual(scorecard["loop_gate"]["recommended_stage"], "argument_building")
        self.assertGreater(scorecard["overall_score"], 0)
        self.assertLessEqual(scorecard["overall_score"], 85)
        self.assertEqual(len(scorecard["dimensions"]), 7)
        self.assertTrue(scorecard["unresolved_hard_issues"])
        self.assertTrue(any(item["dimension_id"] == "necessity_value_closure" for item in scorecard["tracked_issues"]))

    def test_scorecard_requires_ai_backed_critique_before_candidate_status(self) -> None:
        document = load(FROZEN_PATH)
        set_owner(document, None)
        scorecard = build_grant_quality_scorecard(document)

        self.assertEqual(scorecard["assessment_owner"], "projection_only")
        self.assertTrue(scorecard["ai_reviewer_required"])
        self.assertEqual(scorecard["loop_gate"]["recommended_stage"], "critique")
        self.assertIsNone(scorecard["independent_review_evidence"])
        self.assertTrue(scorecard["ai_reviewer_blocker_reason"])

    def test_scorecard_rejects_known_ai_owner_without_independent_review_evidence(self) -> None:
        document = load(FROZEN_PATH)
        set_owner(document, "Codex CLI critique executor")
        scorecard = build_grant_quality_scorecard(document)

        self.assertEqual(scorecard["assessment_owner"], "projection_only")
        self.assertTrue(scorecard["ai_reviewer_required"])
        self.assertIsNone(scorecard["review_artifact_ref"])
        self.assertIsNone(scorecard["independent_review_evidence"])

    def test_scorecard_marks_ai_backed_frozen_workspace_as_submission_grade_candidate(self) -> None:
        document = load(FROZEN_PATH)
        set_owner(document, "Codex CLI critique executor", independent=True)
        scorecard = build_grant_quality_scorecard(document)

        self.assertEqual(scorecard["assessment_owner"], "ai_reviewer_backed")
        self.assertEqual(scorecard["overall_status"], "submission_grade_candidate")
        self.assertEqual(scorecard["loop_gate"]["action"], "ready_for_submission")
        self.assertIsNone(scorecard["loop_gate"]["recommended_stage"])
        self.assertEqual(scorecard["unresolved_hard_issues"], [])
        self.assertGreaterEqual(scorecard["overall_score"], 85)
        self.assertEqual(scorecard["review_artifact_ref"], "mentor_critiques::critique-v1")

    def test_scorecard_rejects_imprecise_critique_owner_as_projection_only(self) -> None:
        document = load(FROZEN_PATH)
        set_owner(document, "not a Codex reviewer")
        scorecard = build_grant_quality_scorecard(document)

        self.assertEqual(scorecard["assessment_owner"], "projection_only")
        self.assertEqual(scorecard["overall_status"], "blocked")


class GrantQualityDiffTest(unittest.TestCase):
    def test_quality_diff_reports_closed_and_remaining_issues(self) -> None:
        diff = build_grant_quality_diff(current_document=load(FROZEN_PATH), previous_document=load(CRITIQUE_PATH))
        closed = next(item for item in diff["issue_progress"]["issue_closure_progress"] if item["transition"] == "closed")

        self.assertEqual(diff["overall_progression"], "improved")
        self.assertGreater(diff["score_delta"], 0)
        self.assertEqual(diff["issue_progress"]["remaining_open_issues"], [])
        self.assertTrue(diff["issue_progress"]["closed_issues"])
        self.assertEqual(closed["closure_delta"], "issue_closed")
        self.assertEqual(closed["previous_closure_status"], "blocked")
        self.assertIsNone(closed["current_closure_status"])

    def test_quality_diff_preserves_newly_opened_issue_when_re_review_adds_new_round(self) -> None:
        diff = build_grant_quality_diff(current_document=load(RE_REVIEW_PATH), previous_document=load(CRITIQUE_PATH))
        opened = next(item for item in diff["issue_progress"]["issue_closure_progress"] if item["transition"] == "newly_opened")

        self.assertEqual(diff["overall_progression"], "mixed")
        self.assertTrue(diff["issue_progress"]["newly_opened_issues"])
        self.assertTrue(diff["issue_progress"]["closed_issues"])
        self.assertEqual(opened["closure_delta"], "new_blocker_opened")
        self.assertIsNone(opened["previous_closure_status"])
        self.assertEqual(opened["current_closure_status"], "blocked")

    def test_quality_diff_tracks_same_lineage_when_issue_summary_is_rephrased(self) -> None:
        previous = load(CRITIQUE_PATH)
        current = load(CRITIQUE_PATH)
        active_critique(current)["necessity_scientific_value"]["blocking_issues"][0] = "rephrased issue"
        diff = build_grant_quality_diff(current_document=current, previous_document=previous)
        lineage = next(
            item for item in diff["issue_progress"]["issue_closure_progress"]
            if item["lineage_basis"]["anchor_ref"] == "necessity_value_closure:rev-item-1"
        )

        self.assertEqual(diff["overall_progression"], "stable")
        self.assertEqual(lineage["transition"], "still_open")
        self.assertNotEqual(lineage["previous_issue_id"], lineage["current_issue_id"])
        self.assertEqual(lineage["previous_issue_id"].split(":")[0], lineage["current_issue_id"].split(":")[0])
        self.assertEqual(lineage["current_summary"], "rephrased issue")

    def test_quality_diff_reports_evidence_supply_progress(self) -> None:
        diff = build_grant_quality_diff(current_document=load(FROZEN_PATH), previous_document=load(CRITIQUE_PATH))
        supply = diff["evidence_supply_progress"]
        progress = next(item for item in supply["gap_progress"] if item["transition"] == "closed")

        self.assertEqual(supply["remaining_open_gaps"], [])
        self.assertEqual(progress["previous_gap_kind"], "hard_blocker")
        self.assertIsNone(progress["current_gap_kind"])
        self.assertEqual(progress["current_required_input_ids"], [])
        self.assertEqual(progress["supply_delta"], "supply_closed")
        self.assertEqual(progress["previous_controller_action_hint"]["action"], "rollback_upstream")
