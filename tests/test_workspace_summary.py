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


if __name__ == "__main__":
    unittest.main()
