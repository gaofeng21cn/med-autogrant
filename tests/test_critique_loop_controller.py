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
from med_autogrant.opl_execution_boundary import (  # noqa: E402
    build_stage_transition_authority_boundary,
    require_opl_default_stage_attempt,
)

OPL_STAGE_ATTEMPT = {
    "runtime_owner": "one-person-lab",
    "executor_kind": "codex_cli",
    "attempt_lease_ref": "lease:opl/stage-attempt/test",
}


class CritiqueLoopControllerTest(unittest.TestCase):
    def test_opl_execution_boundary_helpers_require_provider_owned_stage_attempt(self) -> None:
        missing = require_opl_default_stage_attempt(
            None,
            controller_id="critique-loop",
        )
        self.assertFalse(missing["ok"])
        self.assertEqual(missing["typed_blocker"]["blocker_kind"], "missing_opl_stage_attempt")
        self.assertFalse(missing["typed_blocker"]["mag_owns_attempt_ledger"])
        self.assertEqual(missing["typed_blocker"]["stage_transition_authority"], "one-person-lab")

        allowed = require_opl_default_stage_attempt(
            OPL_STAGE_ATTEMPT,
            controller_id="critique-loop",
        )
        self.assertTrue(allowed["ok"])
        boundary = allowed["execution_boundary"]
        self.assertEqual(boundary["runtime_owner"], "one-person-lab")
        self.assertFalse(boundary["mag_writes_stage_current_pointer"])
        self.assertFalse(boundary["mag_writes_stage_terminal_state"])
        self.assertFalse(boundary["provider_completion_is_stage_transition"])

        authority = build_stage_transition_authority_boundary(
            surface_id="critique-loop",
            mag_role="domain_controller_result_not_stage_writer",
        )
        self.assertEqual(authority["surface_kind"], "mag_stage_transition_authority_boundary")
        self.assertEqual(authority["stage_transition_authority"], "one-person-lab")
        self.assertFalse(authority["mag_selects_next_opl_stage"])
        self.assertFalse(authority["provider_completion_is_stage_transition"])
        self.assertIn("transition_intent_ref", authority["allowed_return_shapes"])

    def test_missing_opl_stage_attempt_returns_typed_blocker_without_running(self) -> None:
        def critique_runner(_document: dict[str, Any]) -> dict[str, Any]:
            raise AssertionError("缺少 OPL attempt 时不应运行 critique_runner")

        result = run_critique_revision_closed_loop(
            current_document={"doc": "initial"},
            max_rounds=3,
            critique_runner=critique_runner,
            revision_runner=critique_runner,
            route_resolver=critique_runner,
        )

        self.assertEqual(result["loop_status"], "failed_closed")
        self.assertEqual(result["loop_status_role"], "mag_domain_controller_result_not_opl_stage_terminal")
        self.assertEqual(result["stage_transition_authority"], "one-person-lab")
        self.assertFalse(result["authority_boundary"]["mag_writes_stage_current_pointer"])
        self.assertFalse(result["authority_boundary"]["mag_writes_stage_terminal_state"])
        self.assertTrue(
            result["authority_boundary"]["recommendation_requires_opl_stage_transition_authority"]
        )
        self.assertEqual(result["termination_reason"], "opl_provider_attempt_required")
        self.assertEqual(
            result["typed_blocker"]["typed_blocker_ref"],
            "typed-blocker:mag/critique-loop/opl-default-stage-attempt-required",
        )

    def test_empty_attempt_lease_object_does_not_authorize_loop(self) -> None:
        def critique_runner(_document: dict[str, Any]) -> dict[str, Any]:
            raise AssertionError("缺少 OPL lease/receipt ref 时不应运行 critique_runner")

        result = run_critique_revision_closed_loop(
            current_document={"doc": "initial"},
            max_rounds=3,
            critique_runner=critique_runner,
            revision_runner=critique_runner,
            route_resolver=critique_runner,
            opl_stage_attempt={
                "runtime_owner": "one-person-lab",
                "executor_kind": "codex_cli",
                "attempt_lease": {},
            },
        )

        self.assertEqual(result["loop_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "opl_provider_attempt_required")
        self.assertEqual(
            result["typed_blocker"]["blocker_kind"],
            "opl_attempt_lease_or_receipt_required",
        )

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
            opl_stage_attempt=OPL_STAGE_ATTEMPT,
        )

        self.assertEqual(result["loop_status"], "passed")
        self.assertEqual(result["loop_status_role"], "mag_domain_controller_result_not_opl_stage_terminal")
        self.assertEqual(result["authority_return"]["result_shape"], "no_regression_evidence")
        self.assertTrue(result["authority_return"]["requires_opl_stage_transition_authority"])
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
            opl_stage_attempt=OPL_STAGE_ATTEMPT,
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
            opl_stage_attempt=OPL_STAGE_ATTEMPT,
        )

        self.assertEqual(result["loop_status"], "rollback_required")
        self.assertEqual(result["termination_reason"], "forced_rollback")
        self.assertEqual(result["authority_return"]["result_shape"], "typed_blocker")
        self.assertEqual(result["typed_blocker"]["blocker_kind"], "forced_rollback")

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
            opl_stage_attempt=OPL_STAGE_ATTEMPT,
        )

        self.assertEqual(result["loop_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "max_rounds_exhausted")
        self.assertEqual(result["typed_blocker"]["blocker_kind"], "max_rounds_exhausted")
