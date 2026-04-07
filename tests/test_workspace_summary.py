from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.workspace import (  # noqa: E402
    load_workspace_document,
    summarize_workspace_document,
    validate_workspace_document,
)


EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_minimal.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
DIRECTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_direction_screening.json"
QUESTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_question_refinement.json"


class WorkspaceSummaryTest(unittest.TestCase):
    def load_example(self) -> dict[str, object]:
        return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    def test_summary_exposes_selected_objects(self) -> None:
        document = load_workspace_document(EXAMPLE_PATH)
        summary = summarize_workspace_document(document)

        self.assertEqual(summary["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(summary["workspace_id"], "nsfc-demo-001")
        self.assertEqual(summary["mode"], "auto")
        self.assertEqual(summary["lifecycle_stage"], "critique")
        self.assertEqual(summary["selected_direction"]["id"], "dir-inflammatory-remodeling")
        self.assertEqual(summary["selected_question"]["id"], "question-immune-fibrosis")
        self.assertEqual(summary["active_draft"]["id"], "draft-v1")
        self.assertEqual(summary["active_revision_plan"]["id"], "revision-v1")
        self.assertEqual(summary["active_critique"]["id"], "critique-v1")

    def test_validation_accepts_input_intake_without_downstream_objects(self) -> None:
        document = load_workspace_document(INPUT_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_accepts_direction_screening_with_selected_direction_only(self) -> None:
        document = load_workspace_document(DIRECTION_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_rejects_direction_screening_with_only_one_direction_candidate(self) -> None:
        document = load_workspace_document(DIRECTION_EXAMPLE_PATH)
        document["direction_hypotheses"] = [document["direction_hypotheses"][0]]

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("direction_hypotheses", "P2.A 方向阶段必须保留 2 到 5 个 DirectionHypothesis。"),
            messages,
        )

    def test_validation_accepts_question_refinement_with_direction_question_binding_only(self) -> None:
        document = load_workspace_document(QUESTION_EXAMPLE_PATH)

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_summary_exposes_direction_question_binding_for_question_refinement(self) -> None:
        document = load_workspace_document(QUESTION_EXAMPLE_PATH)

        summary = summarize_workspace_document(document)

        self.assertEqual(summary["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(summary["lifecycle_stage"], "question_refinement")
        self.assertEqual(summary["current_selection"]["selected_direction_id"], "dir-inflammatory-remodeling")
        self.assertEqual(summary["current_selection"]["selected_question_id"], "question-immune-fibrosis")
        self.assertEqual(summary["selected_direction"]["id"], "dir-inflammatory-remodeling")
        self.assertEqual(summary["selected_question"]["id"], "question-immune-fibrosis")
        self.assertIsNone(summary["active_argument_chain"])
        self.assertIsNone(summary["active_draft"])
        self.assertIsNone(summary["active_revision_plan"])
        self.assertIsNone(summary["active_critique"])

    def test_validation_rejects_question_refinement_without_selected_question_binding(self) -> None:
        document = load_workspace_document(QUESTION_EXAMPLE_PATH)
        document["current_selection"].pop("selected_question_id")

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("current_selection.selected_question_id", "question_refinement 阶段必须显式绑定当前 ScientificQuestionCard。"),
            messages,
        )

    def test_validation_rejects_missing_selected_question_reference(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["current_selection"]["selected_question_id"] = "question-missing"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("current_selection.selected_question_id", "未找到对应的 ScientificQuestionCard。"),
            messages,
        )

    def test_validation_rejects_empty_revision_plan_during_critique(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["revision_plans"][0]["items"] = []

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("revision_plans", "critique 阶段必须存在非空 RevisionPlan。"),
            messages,
        )

    def test_validation_rejects_frozen_stage_without_ready_for_submission_verdict(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "frozen"
        document["gates"]["presubmission_frozen"] = True

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.verdict", "frozen 阶段的激活批注 verdict 必须为 ready_for_submission。"),
            messages,
        )

    def test_validation_rejects_revision_stage_with_major_reframe_verdict(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["mentor_critiques"][0]["verdict"] = "major_reframe"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.verdict", "revision 阶段的激活批注 verdict 必须为 major_revision 或 minor_revision。"),
            messages,
        )

    def test_validation_rejects_revision_stage_with_ready_for_submission_verdict(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["mentor_critiques"][0]["verdict"] = "ready_for_submission"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("mentor_critiques.verdict", "revision 阶段的激活批注 verdict 必须为 major_revision 或 minor_revision。"),
            messages,
        )

    def test_validation_rejects_revision_stage_with_outline_draft_status(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["application_drafts"][0]["status"] = "outline"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.status", "revision 阶段的激活草稿 status 必须为 draft 或 revised。"),
            messages,
        )

    def test_validation_rejects_critique_stage_with_outline_draft_status(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["application_drafts"][0]["status"] = "outline"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.status", "critique 阶段的激活草稿 status 必须为 draft 或 revised。"),
            messages,
        )

    def test_validation_rejects_frozen_stage_without_frozen_draft_status(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "frozen"
        document["gates"]["presubmission_frozen"] = True
        document["mentor_critiques"][0]["verdict"] = "ready_for_submission"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.status", "frozen 阶段的激活草稿 status 必须为 frozen。"),
            messages,
        )

    def test_validation_accepts_completed_revision_with_explicit_revised_switch(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["application_drafts"][0]["status"] = "revised"
        document["application_drafts"][0]["version_label"] = "v0.4"
        document["revision_plans"][0]["execution_status"] = "completed"
        document["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        document["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        document["revision_plans"][0]["comparison_summary"] = "已根据 major_revision 完成立项依据与机制链条重写。"

        result = validate_workspace_document(document)

        self.assertTrue(result.ok)
        self.assertEqual(result.errors, [])

    def test_validation_rejects_completed_revision_without_revised_status_switch(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["revision_plans"][0]["execution_status"] = "completed"
        document["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        document["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        document["revision_plans"][0]["comparison_summary"] = "已根据 major_revision 完成修订。"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("application_drafts.status", "revision plan 已标记 completed 时，激活草稿 status 必须显式切换为 revised。"),
            messages,
        )

    def test_validation_rejects_revised_status_without_completed_revision_evidence(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["application_drafts"][0]["status"] = "revised"
        document["application_drafts"][0]["version_label"] = "v0.4"

        result = validate_workspace_document(document)

        self.assertFalse(result.ok)
        messages = {(item.path, item.message) for item in result.errors}
        self.assertIn(
            ("revision_plans.execution_status", "激活草稿 status=revised 时，RevisionPlan.execution_status 必须为 completed。"),
            messages,
        )

if __name__ == "__main__":
    unittest.main()
