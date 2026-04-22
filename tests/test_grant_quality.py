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
