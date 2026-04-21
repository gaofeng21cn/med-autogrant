from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.critique_loop_controller import run_critique_revision_closed_loop  # noqa: E402


class CritiqueLoopControllerTest(unittest.TestCase):
    def test_ready_for_submission_stops_in_first_round(self) -> None:
        current_document = {"stage": "drafting"}

        def critique_runner(document: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(document, current_document)
            return {"critique_workspace": {"stage": "critique", "round": 1}}

        def revision_runner(_document: dict[str, Any]) -> dict[str, Any]:
            raise AssertionError("ready_for_submission 场景不应进入 revision_runner")

        def route_resolver(document: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(document["round"], 1)
            return {"recommended_stage": "frozen", "reason": "ready_for_submission"}

        result = run_critique_revision_closed_loop(
            current_document=current_document,
            max_rounds=3,
            critique_runner=critique_runner,
            revision_runner=revision_runner,
            route_resolver=route_resolver,
        )

        self.assertEqual(result["loop_status"], "passed")
        self.assertEqual(result["termination_reason"], "ready_for_submission")
        self.assertEqual(len(result["rounds"]), 1)

    def test_major_revision_then_second_round_passes(self) -> None:
        def critique_runner(document: dict[str, Any]) -> dict[str, Any]:
            if document["doc"] == "initial":
                return {"critique_workspace": {"doc": "after-critique-1"}}
            if document["doc"] == "after-revision-1":
                return {"critique_workspace": {"doc": "after-critique-2"}}
            raise AssertionError(f"unexpected critique input: {document}")

        def revision_runner(document: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(document["doc"], "after-critique-1")
            return {"revised_workspace": {"doc": "after-revision-1"}}

        def route_resolver(document: dict[str, Any]) -> dict[str, Any]:
            if document["doc"] == "after-critique-1":
                return {"recommended_stage": "revision", "reason": "major_revision"}
            if document["doc"] == "after-critique-2":
                return {"recommended_stage": "frozen", "reason": "ready_for_submission"}
            raise AssertionError(f"unexpected route input: {document}")

        result = run_critique_revision_closed_loop(
            current_document={"doc": "initial"},
            max_rounds=3,
            critique_runner=critique_runner,
            revision_runner=revision_runner,
            route_resolver=route_resolver,
        )

        self.assertEqual(result["loop_status"], "passed")
        self.assertEqual(len(result["rounds"]), 2)
        self.assertEqual(result["rounds"][0]["decision"], "revision_required")
        self.assertEqual(result["rounds"][1]["decision"], "ready_for_submission")

    def test_forced_rollback_stops_with_rollback_required(self) -> None:
        def critique_runner(_document: dict[str, Any]) -> dict[str, Any]:
            return {"critique_workspace": {"doc": "after-critique-1"}}

        def revision_runner(_document: dict[str, Any]) -> dict[str, Any]:
            raise AssertionError("forced rollback 场景不应进入 revision_runner")

        def route_resolver(_document: dict[str, Any]) -> dict[str, Any]:
            return {
                "recommended_stage": "argument_building",
                "forced_rollback_stage": "argument_building",
                "reason": "forced rollback",
            }

        result = run_critique_revision_closed_loop(
            current_document={"doc": "initial"},
            max_rounds=2,
            critique_runner=critique_runner,
            revision_runner=revision_runner,
            route_resolver=route_resolver,
        )

        self.assertEqual(result["loop_status"], "rollback_required")
        self.assertEqual(result["termination_reason"], "forced_rollback")

    def test_max_rounds_stops_fail_closed(self) -> None:
        def critique_runner(document: dict[str, Any]) -> dict[str, Any]:
            if document["doc"] == "initial":
                return {"critique_workspace": {"doc": "after-critique-1"}}
            if document["doc"] == "after-revision-1":
                return {"critique_workspace": {"doc": "after-critique-2"}}
            raise AssertionError(f"unexpected critique input: {document}")

        def revision_runner(document: dict[str, Any]) -> dict[str, Any]:
            if document["doc"] == "after-critique-1":
                return {"revised_workspace": {"doc": "after-revision-1"}}
            if document["doc"] == "after-critique-2":
                return {"revised_workspace": {"doc": "after-revision-2"}}
            raise AssertionError(f"unexpected revision input: {document}")

        def route_resolver(_document: dict[str, Any]) -> dict[str, Any]:
            return {"recommended_stage": "revision", "reason": "major_revision"}

        result = run_critique_revision_closed_loop(
            current_document={"doc": "initial"},
            max_rounds=2,
            critique_runner=critique_runner,
            revision_runner=revision_runner,
            route_resolver=route_resolver,
        )

        self.assertEqual(result["loop_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "max_rounds_exhausted")
