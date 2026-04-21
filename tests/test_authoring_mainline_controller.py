from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.authoring_mainline_controller import run_authoring_mainline_controller  # noqa: E402


class AuthoringMainlineControllerTest(unittest.TestCase):
    def test_drafting_to_critique_revision_then_passed(self) -> None:
        calls: list[str] = []

        def route_resolver(workspace: dict[str, Any]) -> dict[str, Any]:
            stage = workspace["stage"]
            if stage == "drafting":
                return {"recommended_stage": "critique"}
            if stage == "after_critique":
                return {"recommended_stage": "revision"}
            if stage == "after_revision":
                return {"recommended_stage": "frozen"}
            raise AssertionError(f"unexpected stage: {stage}")

        def critique_runner(workspace: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(workspace["stage"], "drafting")
            calls.append("critique")
            return {"workspace": {"stage": "after_critique", "version": 2}}

        def revision_runner(workspace: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(workspace["stage"], "after_critique")
            calls.append("revision")
            return {"workspace": {"stage": "after_revision", "version": 3}}

        result = run_authoring_mainline_controller(
            current_workspace={"stage": "drafting", "version": 1},
            max_cycles=5,
            route_resolver=route_resolver,
            stage_runners={
                "critique": critique_runner,
                "revision": revision_runner,
            },
        )

        self.assertEqual(result["loop_status"], "passed")
        self.assertEqual(result["termination_reason"], "ready_for_submission")
        self.assertEqual(result["final_workspace"]["stage"], "after_revision")
        self.assertEqual(calls, ["critique", "revision"])

    def test_question_refinement_rollback_rebuild_then_passed(self) -> None:
        calls: list[str] = []

        def route_resolver(workspace: dict[str, Any]) -> dict[str, Any]:
            stage = workspace["stage"]
            if stage == "critique":
                return {"recommended_stage": "question_refinement"}
            if stage == "question_refined":
                return {"recommended_stage": "critique"}
            if stage == "re_critique_done":
                return {"recommended_stage": "frozen"}
            raise AssertionError(f"unexpected stage: {stage}")

        def question_refinement_runner(workspace: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(workspace["stage"], "critique")
            calls.append("question_refinement")
            return {"workspace": {"stage": "question_refined"}}

        def critique_runner(workspace: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(workspace["stage"], "question_refined")
            calls.append("critique")
            return {"workspace": {"stage": "re_critique_done"}}

        result = run_authoring_mainline_controller(
            current_workspace={"stage": "critique"},
            max_cycles=5,
            route_resolver=route_resolver,
            stage_runners={
                "question_refinement": question_refinement_runner,
                "critique": critique_runner,
            },
        )

        self.assertEqual(result["loop_status"], "passed")
        self.assertEqual(result["termination_reason"], "ready_for_submission")
        self.assertEqual(result["final_workspace"]["stage"], "re_critique_done")
        self.assertEqual(calls, ["question_refinement", "critique"])
        self.assertEqual(result["cycles"][0]["decision"], "rollback_rebuild")

    def test_fit_alignment_rollback_rebuild_then_passed(self) -> None:
        calls: list[str] = []

        def route_resolver(workspace: dict[str, Any]) -> dict[str, Any]:
            stage = workspace["stage"]
            if stage == "critique":
                return {"recommended_stage": "fit_alignment"}
            if stage == "fit_aligned":
                return {"recommended_stage": "revision"}
            if stage == "revised":
                return {"recommended_stage": "ready_for_submission"}
            raise AssertionError(f"unexpected stage: {stage}")

        def fit_alignment_runner(workspace: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(workspace["stage"], "critique")
            calls.append("fit_alignment")
            return {"fit_alignment_workspace": {"stage": "fit_aligned"}}

        def revision_runner(workspace: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(workspace["stage"], "fit_aligned")
            calls.append("revision")
            return {"workspace": {"stage": "revised"}}

        result = run_authoring_mainline_controller(
            current_workspace={"stage": "critique"},
            max_cycles=5,
            route_resolver=route_resolver,
            stage_runners={
                "fit_alignment": fit_alignment_runner,
                "revision": revision_runner,
            },
        )

        self.assertEqual(result["loop_status"], "passed")
        self.assertEqual(result["final_workspace"]["stage"], "revised")
        self.assertEqual(calls, ["fit_alignment", "revision"])
        self.assertEqual(result["cycles"][0]["decision"], "rollback_rebuild")

    def test_unknown_route_fail_closed(self) -> None:
        def route_resolver(_workspace: dict[str, Any]) -> dict[str, Any]:
            return {"recommended_stage": "impossible_stage"}

        result = run_authoring_mainline_controller(
            current_workspace={"stage": "drafting"},
            max_cycles=3,
            route_resolver=route_resolver,
            stage_runners={},
        )

        self.assertEqual(result["loop_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "unknown_recommended_stage")
        self.assertEqual(result["final_route"]["recommended_stage"], "impossible_stage")

    def test_max_cycles_exhausted_fail_closed(self) -> None:
        def route_resolver(_workspace: dict[str, Any]) -> dict[str, Any]:
            return {"recommended_stage": "critique"}

        def critique_runner(_workspace: dict[str, Any]) -> dict[str, Any]:
            return {"workspace": {"stage": "drafting"}}

        result = run_authoring_mainline_controller(
            current_workspace={"stage": "drafting"},
            max_cycles=2,
            route_resolver=route_resolver,
            stage_runners={"critique": critique_runner},
        )

        self.assertEqual(result["loop_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "max_cycles_exhausted")
        self.assertEqual(len(result["cycles"]), 2)
