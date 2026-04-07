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

from med_autogrant.stage_router import determine_next_step  # noqa: E402


EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_minimal.json"
INPUT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_input_intake.json"
DIRECTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_direction_screening.json"
QUESTION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2a_question_refinement.json"
ARGUMENT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_argument_building.json"
FIT_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_fit_alignment.json"
OUTLINE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2b_outline.json"


class StageRouterTest(unittest.TestCase):
    def load_example(self) -> dict[str, object]:
        return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    def test_input_intake_routes_to_direction_screening(self) -> None:
        route = determine_next_step(json.loads(INPUT_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["current_stage"], "input_intake")
        self.assertEqual(route["recommended_stage"], "direction_screening")

    def test_direction_screening_routes_to_question_refinement(self) -> None:
        route = determine_next_step(json.loads(DIRECTION_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["current_stage"], "direction_screening")
        self.assertEqual(route["recommended_stage"], "question_refinement")
        self.assertIn("科学问题尚未冻结", route["reason"])

    def test_question_refinement_routes_to_argument_building(self) -> None:
        route = determine_next_step(json.loads(QUESTION_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["current_stage"], "question_refinement")
        self.assertEqual(route["recommended_stage"], "argument_building")
        self.assertIn("立项依据主链尚未冻结", route["reason"])

    def test_argument_building_routes_to_fit_alignment(self) -> None:
        route = determine_next_step(json.loads(ARGUMENT_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["current_stage"], "argument_building")
        self.assertEqual(route["recommended_stage"], "fit_alignment")
        self.assertIn("申请人适配度映射尚未冻结", route["reason"])

    def test_fit_alignment_routes_to_outline(self) -> None:
        route = determine_next_step(json.loads(FIT_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["current_stage"], "fit_alignment")
        self.assertEqual(route["recommended_stage"], "outline")
        self.assertIn("提纲尚未冻结", route["reason"])

    def test_outline_routes_to_drafting_after_outline_freeze(self) -> None:
        route = determine_next_step(json.loads(OUTLINE_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["current_stage"], "outline")
        self.assertEqual(route["recommended_stage"], "drafting")
        self.assertIn("提纲已冻结", route["reason"])

    def test_major_revision_routes_to_revision(self) -> None:
        route = determine_next_step(self.load_example())

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["workspace_id"], "nsfc-demo-001")
        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "revision")
        self.assertIn("major_revision", route["reason"])
        self.assertIn("执行 revision plan", route["actions"][0])

    def test_major_reframe_routes_back_to_question_refinement(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["mentor_critiques"][0]["verdict"] = "major_reframe"

        route = determine_next_step(document)

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["recommended_stage"], "question_refinement")
        self.assertIn("重塑科学问题", route["reason"])

    def test_completed_revision_routes_back_to_critique(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["lifecycle_stage"] = "revision"
        document["application_drafts"][0]["status"] = "revised"
        document["application_drafts"][0]["version_label"] = "v0.4"
        document["revision_plans"][0]["execution_status"] = "completed"
        document["revision_plans"][0]["pre_revision_version_label"] = "v0.3"
        document["revision_plans"][0]["post_revision_version_label"] = "v0.4"
        document["revision_plans"][0]["comparison_summary"] = "已完成修订并形成前后版本比较。"

        route = determine_next_step(document)

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["current_stage"], "revision")
        self.assertEqual(route["recommended_stage"], "critique")
        self.assertIn("revised", route["reason"])


if __name__ == "__main__":
    unittest.main()
