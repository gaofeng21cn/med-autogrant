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
DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"
CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
MAJOR_REFRAME_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_major_reframe.json"
READY_FOR_SUBMISSION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FORCED_ROLLBACK_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_forced_rollback_argument.json"
PRESUBMISSION_FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class StageRouterTest(unittest.TestCase):
    def load_example(self) -> dict[str, object]:
        return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    def build_re_review_workspace(self) -> dict[str, object]:
        return json.loads(RE_REVIEW_EXAMPLE_PATH.read_text(encoding="utf-8"))

    def build_major_reframe_workspace(self) -> dict[str, object]:
        return json.loads(MAJOR_REFRAME_EXAMPLE_PATH.read_text(encoding="utf-8"))

    def build_forced_rollback_workspace(self) -> dict[str, object]:
        return json.loads(FORCED_ROLLBACK_EXAMPLE_PATH.read_text(encoding="utf-8"))

    def test_input_intake_routes_to_direction_screening(self) -> None:
        route = determine_next_step(json.loads(INPUT_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["surface_kind"], "mag_stage_transition_oracle_recommendation")
        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["current_stage"], "input_intake")
        self.assertEqual(route["recommended_stage"], "direction_screening")
        self.assertEqual(route["current_stage_role"], "workspace_lifecycle_observation")
        self.assertEqual(route["recommended_stage_role"], "transition_intent_recommendation")
        self.assertEqual(route["stage_transition_authority"], "one-person-lab")
        self.assertFalse(route["authority_boundary"]["mag_writes_stage_current_pointer"])
        self.assertFalse(route["authority_boundary"]["mag_writes_stage_terminal_state"])
        self.assertTrue(
            route["authority_boundary"]["recommendation_requires_opl_stage_transition_authority"]
        )
        self.assertEqual(
            route["transition_intent"]["surface_kind"],
            "mag_stage_transition_intent_recommendation",
        )
        self.assertTrue(route["transition_intent"]["requires_opl_stage_transition_authority"])

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

    def test_drafting_routes_to_critique(self) -> None:
        route = determine_next_step(json.loads(DRAFTING_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["current_stage"], "drafting")
        self.assertEqual(route["recommended_stage"], "critique")
        self.assertIn("当前草稿已形成", route["reason"])

    def test_critique_routes_to_revision(self) -> None:
        route = determine_next_step(json.loads(CRITIQUE_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "revision")
        self.assertIn("major_revision", route["reason"])

    def test_major_revision_routes_to_revision(self) -> None:
        route = determine_next_step(self.load_example())

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["workspace_id"], "nsfc-demo-001")
        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "revision")
        self.assertIn("major_revision", route["reason"])
        self.assertIn("执行 revision plan", route["actions"][0])

    def test_major_reframe_routes_back_to_question_refinement(self) -> None:
        route = determine_next_step(json.loads(MAJOR_REFRAME_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["recommended_stage"], "question_refinement")
        self.assertIn("重塑科学问题", route["reason"])

    def test_major_reframe_can_force_rollback_to_direction_screening(self) -> None:
        document = self.build_major_reframe_workspace()
        document["mentor_critiques"][0]["forced_rollback_stage"] = "direction_screening"
        document["mentor_critiques"][0]["forced_rollback_reason"] = "当前方向无法稳定承载机制级科学问题。"

        route = determine_next_step(document)

        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "direction_screening")
        self.assertEqual(route["forced_rollback_stage"], "direction_screening")
        self.assertIn("forced rollback", route["reason"])

    def test_major_reframe_can_force_rollback_to_question_refinement(self) -> None:
        document = self.build_major_reframe_workspace()
        document["mentor_critiques"][0]["forced_rollback_stage"] = "question_refinement"
        document["mentor_critiques"][0]["forced_rollback_reason"] = "当前问题表述无法稳定锚定知识边界。"

        route = determine_next_step(document)

        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "question_refinement")
        self.assertEqual(route["forced_rollback_stage"], "question_refinement")
        self.assertIn("forced rollback", route["reason"])

    def test_minor_revision_routes_to_revision(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["mentor_critiques"][0]["verdict"] = "minor_revision"

        route = determine_next_step(document)

        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "revision")
        self.assertIn("minor_revision", route["reason"])

    def test_ready_for_submission_routes_to_frozen(self) -> None:
        route = determine_next_step(json.loads(READY_FOR_SUBMISSION_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "frozen")
        self.assertIn("ready_for_submission", route["reason"])

    def test_completed_revision_routes_back_to_critique(self) -> None:
        route = determine_next_step(json.loads(REVISION_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["current_stage"], "revision")
        self.assertEqual(route["recommended_stage"], "critique")
        self.assertIn("revised", route["reason"])

    def test_re_review_critique_routes_back_to_revision_using_new_active_plan(self) -> None:
        route = determine_next_step(self.build_re_review_workspace())

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "revision")
        self.assertIn("major_revision", route["reason"])

    def test_major_revision_can_force_rollback_to_argument_building(self) -> None:
        route = determine_next_step(self.build_forced_rollback_workspace())

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "argument_building")
        self.assertEqual(route["forced_rollback_stage"], "argument_building")
        self.assertIn("forced rollback", route["reason"])

    def test_major_revision_can_force_rollback_to_fit_alignment(self) -> None:
        document = self.build_forced_rollback_workspace()
        document["mentor_critiques"][1]["forced_rollback_stage"] = "fit_alignment"
        document["mentor_critiques"][1]["forced_rollback_reason"] = "申请人适配度证据链需要回退重建。"

        route = determine_next_step(document)

        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "fit_alignment")
        self.assertEqual(route["forced_rollback_stage"], "fit_alignment")
        self.assertIn("forced rollback", route["reason"])

    def test_presubmission_frozen_stage_stays_frozen(self) -> None:
        route = determine_next_step(json.loads(PRESUBMISSION_FROZEN_EXAMPLE_PATH.read_text(encoding="utf-8")))

        self.assertEqual(route["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(route["current_stage"], "frozen")
        self.assertEqual(route["recommended_stage"], "frozen")
        self.assertTrue(route["presubmission_frozen"])


if __name__ == "__main__":
    unittest.main()
