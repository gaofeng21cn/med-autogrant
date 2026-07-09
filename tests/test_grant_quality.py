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


def _mark_active_critique_ai_backed(document: dict[str, object]) -> None:
    active_revision_plan_id = document["current_selection"]["active_revision_plan_id"]  # type: ignore[index]
    active_revision_plan = next(
        item
        for item in document["revision_plans"]  # type: ignore[index]
        if item["revision_plan_id"] == active_revision_plan_id
    )
    critique = next(
        item
        for item in document["mentor_critiques"]  # type: ignore[index]
        if item["critique_id"] == active_revision_plan["critique_id"]
    )
    metadata = critique.setdefault("metadata", {})
    metadata["owner"] = "Codex CLI critique executor"
    critique_id = critique["critique_id"]
    metadata["independent_review_evidence"] = {
        "execution_attempt_ref": f"codex_cli::grant-run::{critique_id}",
        "review_attempt_ref": f"mentor_critiques::{critique_id}",
        "review_receipt_ref": f"mentor_critiques::{critique_id}::metadata.independent_review_evidence",
        "no_shared_context_verified": True,
        "reviewer_owner": "Codex CLI critique executor",
        "reviewer_agent_ref": "codex_cli::critique_executor",
    }


def _remove_active_critique_ai_owner(document: dict[str, object]) -> None:
    active_revision_plan_id = document["current_selection"]["active_revision_plan_id"]  # type: ignore[index]
    active_revision_plan = next(
        item
        for item in document["revision_plans"]  # type: ignore[index]
        if item["revision_plan_id"] == active_revision_plan_id
    )
    critique = next(
        item
        for item in document["mentor_critiques"]  # type: ignore[index]
        if item["critique_id"] == active_revision_plan["critique_id"]
    )
    critique.get("metadata", {}).pop("owner", None)


def _set_active_critique_owner(document: dict[str, object], owner: str) -> None:
    active_revision_plan_id = document["current_selection"]["active_revision_plan_id"]  # type: ignore[index]
    active_revision_plan = next(
        item
        for item in document["revision_plans"]  # type: ignore[index]
        if item["revision_plan_id"] == active_revision_plan_id
    )
    critique = next(
        item
        for item in document["mentor_critiques"]  # type: ignore[index]
        if item["critique_id"] == active_revision_plan["critique_id"]
    )
    critique.setdefault("metadata", {})["owner"] = owner


class GrantQualityScorecardTest(unittest.TestCase):
    def test_scorecard_surfaces_blockers_and_route_recommendation_for_critique_workspace(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        critique_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)
        _mark_active_critique_ai_backed(critique_workspace)
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

    def test_scorecard_requires_ai_backed_critique_before_candidate_status(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        frozen_workspace = _load_json(FROZEN_EXAMPLE_PATH)
        _remove_active_critique_ai_owner(frozen_workspace)
        scorecard = build_grant_quality_scorecard(frozen_workspace)

        self.assertEqual(scorecard["assessment_owner"], "projection_only")
        self.assertTrue(scorecard["ai_reviewer_required"])
        self.assertEqual(scorecard["overall_status"], "blocked")
        self.assertEqual(scorecard["loop_gate"]["action"], "continue")
        self.assertEqual(scorecard["loop_gate"]["recommended_stage"], "critique")
        self.assertIsNone(scorecard["independent_review_evidence"])
        self.assertIn("independent execution/review receipt refs", scorecard["ai_reviewer_blocker_reason"])

    def test_scorecard_rejects_known_ai_owner_without_independent_review_evidence(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        frozen_workspace = _load_json(FROZEN_EXAMPLE_PATH)
        _set_active_critique_owner(frozen_workspace, "Codex CLI critique executor")
        scorecard = build_grant_quality_scorecard(frozen_workspace)

        self.assertEqual(scorecard["assessment_owner"], "projection_only")
        self.assertTrue(scorecard["ai_reviewer_required"])
        self.assertIsNone(scorecard["review_artifact_ref"])
        self.assertIsNone(scorecard["independent_review_evidence"])
        self.assertEqual(scorecard["overall_status"], "blocked")

    def test_scorecard_marks_ai_backed_frozen_workspace_as_submission_grade_candidate(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        frozen_workspace = _load_json(FROZEN_EXAMPLE_PATH)
        _mark_active_critique_ai_backed(frozen_workspace)
        scorecard = build_grant_quality_scorecard(frozen_workspace)

        self.assertEqual(scorecard["assessment_owner"], "ai_reviewer_backed")
        self.assertFalse(scorecard["ai_reviewer_required"])
        self.assertEqual(scorecard["review_artifact_ref"], "mentor_critiques::critique-v1")
        self.assertEqual(
            scorecard["independent_review_evidence"]["review_attempt_ref"],
            "mentor_critiques::critique-v1",
        )
        self.assertIsNone(scorecard["ai_reviewer_blocker_reason"])
        self.assertEqual(scorecard["overall_status"], "submission_grade_candidate")
        self.assertEqual(scorecard["loop_gate"]["action"], "ready_for_submission")
        self.assertIsNone(scorecard["loop_gate"]["recommended_stage"])
        self.assertEqual(scorecard["unresolved_hard_issues"], [])
        self.assertGreaterEqual(scorecard["overall_score"], 85)

    def test_scorecard_rejects_imprecise_critique_owner_as_projection_only(self) -> None:
        from med_autogrant.grant_quality import build_grant_quality_scorecard

        frozen_workspace = _load_json(FROZEN_EXAMPLE_PATH)
        _set_active_critique_owner(frozen_workspace, "not a Codex reviewer")
        scorecard = build_grant_quality_scorecard(frozen_workspace)

        self.assertEqual(scorecard["assessment_owner"], "projection_only")
        self.assertTrue(scorecard["ai_reviewer_required"])
        self.assertEqual(scorecard["overall_status"], "blocked")

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
