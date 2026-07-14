from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
from med_autogrant.stage_router import (  # noqa: E402
    _apply_quality_gate_to_route,
    _determine_structural_next_step,
    determine_next_step,
)


EXAMPLES = REPO_ROOT / "examples"


def load(name: str) -> dict[str, object]:
    return json.loads((EXAMPLES / name).read_text(encoding="utf-8"))


class StageRouterTest(unittest.TestCase):
    def test_all_nineteen_stage_routes(self) -> None:
        minimal = load("nsfc_workspace_minimal.json")
        major_reframe = load("nsfc_workspace_p3a_major_reframe.json")
        forced_rollback = load("nsfc_workspace_p3c_forced_rollback_argument.json")

        forced_direction = copy.deepcopy(major_reframe)
        forced_direction["mentor_critiques"][0]["forced_rollback_stage"] = "direction_screening"
        forced_direction["mentor_critiques"][0]["forced_rollback_reason"] = "rebuild direction"
        forced_question = copy.deepcopy(major_reframe)
        forced_question["mentor_critiques"][0]["forced_rollback_stage"] = "question_refinement"
        forced_question["mentor_critiques"][0]["forced_rollback_reason"] = "rebuild question"
        minor_revision = copy.deepcopy(minimal)
        minor_revision["mentor_critiques"][0]["verdict"] = "minor_revision"
        forced_fit = copy.deepcopy(forced_rollback)
        forced_fit["mentor_critiques"][1]["forced_rollback_stage"] = "fit_alignment"
        forced_fit["mentor_critiques"][1]["forced_rollback_reason"] = "rebuild fit"

        cases = (
            (load("nsfc_workspace_p2a_input_intake.json"), "input_intake", "direction_screening", {}),
            (load("nsfc_workspace_p2a_direction_screening.json"), "direction_screening", "question_refinement", {}),
            (load("nsfc_workspace_p2a_question_refinement.json"), "question_refinement", "argument_building", {}),
            (load("nsfc_workspace_p2b_argument_building.json"), "argument_building", "fit_alignment", {}),
            (load("nsfc_workspace_p2b_fit_alignment.json"), "fit_alignment", "outline", {}),
            (load("nsfc_workspace_p2b_outline.json"), "outline", "drafting", {}),
            (load("nsfc_workspace_p2c_drafting.json"), "drafting", "critique", {}),
            (load("nsfc_workspace_p2c_critique.json"), "critique", "revision", {}),
            (minimal, "critique", "revision", {}),
            (major_reframe, "critique", "question_refinement", {}),
            (forced_direction, "critique", "direction_screening", {"forced_rollback_stage": "direction_screening"}),
            (forced_question, "critique", "question_refinement", {"forced_rollback_stage": "question_refinement"}),
            (minor_revision, "critique", "revision", {}),
            (load("nsfc_workspace_p3a_ready_for_submission.json"), "critique", "frozen", {}),
            (load("nsfc_workspace_p2c_revision.json"), "revision", "critique", {}),
            (load("nsfc_workspace_p3b_re_review_major_revision.json"), "critique", "revision", {}),
            (forced_rollback, "critique", "argument_building", {"forced_rollback_stage": "argument_building"}),
            (forced_fit, "critique", "fit_alignment", {"forced_rollback_stage": "fit_alignment"}),
            (load("nsfc_workspace_p3c_presubmission_frozen.json"), "frozen", "frozen", {"presubmission_frozen": True}),
        )

        for document, current_stage, recommended_stage, extra in cases:
            with self.subTest(current=current_stage, recommended=recommended_stage, extra=extra):
                route = determine_next_step(document)
                self.assertEqual(route["current_stage"], current_stage)
                self.assertEqual(route["recommended_stage"], recommended_stage)
                for key, expected in extra.items():
                    self.assertEqual(route[key], expected)

    def test_route_context_is_non_authoritative_codex_input(self) -> None:
        route = determine_next_step(load("nsfc_workspace_p2a_input_intake.json"))

        self.assertEqual(route["surface_kind"], "mag_ai_route_context")
        self.assertEqual(route["semantic_route_owner"], "decisive_codex_attempt")
        self.assertEqual(
            route["authority_boundary"]["semantic_route_owner"],
            "decisive_codex_attempt",
        )
        self.assertEqual(
            route["authority_boundary"]["semantic_route_owner_role"],
            "decisive_attempt_only",
        )
        self.assertEqual(
            route["ai_route_policy"]["semantic_route_owner"],
            "decisive_codex_attempt",
        )
        self.assertFalse(route["authority_boundary"]["mag_writes_stage_current_pointer"])
        self.assertFalse(route["authority_boundary"]["mag_writes_stage_terminal_state"])
        self.assertFalse(route["ai_route_policy"]["program_recommendation_can_block_or_select_route"])
        self.assertFalse(route["authority_boundary"]["framework_can_accept_reject_or_override_codex_route"])

    def test_quality_gate_routes_record_non_blocking_debt(self) -> None:
        for name, recommended_stage, action in (
            ("nsfc_workspace_p2c_critique.json", "revision", "route_back_recommended"),
            ("nsfc_workspace_p3a_ready_for_submission.json", "frozen", "continue"),
            ("nsfc_workspace_p3b_re_review_major_revision.json", "revision", "route_back_recommended"),
            ("nsfc_workspace_p3c_presubmission_frozen.json", "frozen", "continue"),
        ):
            with self.subTest(example=name):
                route = determine_next_step(load(name))
                self.assertEqual(route["recommended_stage"], recommended_stage)
                self.assertEqual(route["quality_gate"]["action"], action)
                self.assertEqual(route["ai_route_policy"]["suggested_target_stage"], recommended_stage)
                self.assertFalse(route["quality_debt"]["blocks_stage_transition"])
                self.assertTrue(route["quality_debt"]["blocks_quality_export_or_ready_claims"])

    def test_early_quality_rollback_is_advisory_debt_not_a_human_gate(self) -> None:
        route = _apply_quality_gate_to_route(
            route=_determine_structural_next_step(load("nsfc_workspace_p2c_critique.json")),
            quality_scorecard={
                "loop_gate": {
                    "action": "route_back_recommended",
                    "recommended_stage": "question_refinement",
                    "reason": "rebuild question",
                }
            },
        )

        self.assertEqual(route["recommended_stage"], "revision")
        self.assertFalse(route["requires_human_confirmation"])
        self.assertEqual(route["ai_route_policy"]["suggested_target_stage"], "revision")
        self.assertFalse(route["ai_route_policy"]["program_recommendation_can_block_or_select_route"])
        self.assertEqual(route["quality_debt"]["recommended_repair_stage"], "question_refinement")
        self.assertFalse(route["quality_debt"]["blocks_stage_transition"])

    def test_ordinary_repair_is_a_nonblocking_codex_route_hint(self) -> None:
        route = determine_next_step(load("nsfc_workspace_p2c_critique.json"))

        self.assertFalse(route["requires_human_confirmation"])
        self.assertTrue(route["ai_route_policy"]["advance_repeat_skip_or_route_back_allowed"])


if __name__ == "__main__":
    unittest.main()
