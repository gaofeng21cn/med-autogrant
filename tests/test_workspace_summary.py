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


class WorkspaceSummaryTest(unittest.TestCase):
    def load_example(self) -> dict[str, object]:
        return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    def test_summary_exposes_selected_objects(self) -> None:
        document = load_workspace_document(EXAMPLE_PATH)
        summary = summarize_workspace_document(document)

        self.assertEqual(summary["workspace_id"], "nsfc-demo-001")
        self.assertEqual(summary["mode"], "auto")
        self.assertEqual(summary["lifecycle_stage"], "critique")
        self.assertEqual(summary["selected_direction"]["id"], "dir-inflammatory-remodeling")
        self.assertEqual(summary["selected_question"]["id"], "question-immune-fibrosis")
        self.assertEqual(summary["active_draft"]["id"], "draft-v1")
        self.assertEqual(summary["active_revision_plan"]["id"], "revision-v1")
        self.assertEqual(summary["active_critique"]["id"], "critique-v1")

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

if __name__ == "__main__":
    unittest.main()
