from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.grant_autonomy_controller import run_grant_autonomy_controller  # noqa: E402


class GrantAutonomyControllerTest(unittest.TestCase):
    def _selection_start_request(self) -> dict[str, Any]:
        return {
            "request_id": "autonomy-req-001",
            "start": {
                "mode": "selection_input",
                "selection_input": {
                    "selection_input_id": "sel-001",
                    "funding_opportunity_pool": [{"brief_id": "nsfc-2026-general"}],
                },
            },
            "goal": {
                "target_status": "submission_grade_candidate",
                "summary": "进入可提交态",
            },
            "max_rounds_or_cycles": 3,
            "budget": {"max_total_steps": 20},
            "stop_conditions": {
                "require_zero_blockers": True,
                "require_zero_evidence_gaps": True,
            },
            "blocker_queue": ["初始 blocker"],
            "evidence_gap_queue": ["初始证据缺口"],
            "reselection_policy": {
                "enabled": True,
                "max_reselections": 1,
            },
            "rollback_policy": {
                "enabled": True,
                "max_rollbacks": 1,
            },
        }

    def _workspace_start_request(self) -> dict[str, Any]:
        return {
            "request_id": "autonomy-req-002",
            "start": {
                "mode": "workspace",
                "workspace": {
                    "workspace_id": "ws-001",
                    "lifecycle_stage": "critique",
                },
            },
            "goal": {
                "target_status": "near_submission_candidate",
                "summary": "先达到 near submission",
            },
            "max_rounds_or_cycles": 2,
            "budget": {"max_total_steps": 10},
            "stop_conditions": {
                "require_zero_blockers": True,
                "require_zero_evidence_gaps": True,
            },
            "blocker_queue": [],
            "evidence_gap_queue": [],
            "reselection_policy": {
                "enabled": False,
                "max_reselections": 0,
            },
            "rollback_policy": {
                "enabled": False,
                "max_rollbacks": 0,
            },
        }

    def test_selection_input_path_runs_selector_initializer_mainline_quality(self) -> None:
        call_order: list[str] = []
        quality_calls = {"count": 0}

        def selector(selection_input: dict[str, Any]) -> dict[str, Any]:
            call_order.append("selector")
            self.assertEqual(selection_input["selection_input_id"], "sel-001")
            return {"selected_profile_id": "profile-nsfc"}

        def initializer(selection_input: dict[str, Any], selection: dict[str, Any]) -> dict[str, Any]:
            call_order.append("initializer")
            self.assertEqual(selection["selected_profile_id"], "profile-nsfc")
            return {"workspace": {"workspace_id": selection_input["selection_input_id"], "stage": "input_intake"}}

        def mainline_runner(payload: dict[str, Any]) -> dict[str, Any]:
            call_order.append("mainline_runner")
            self.assertEqual(payload["workspace"]["stage"], "input_intake")
            return {"workspace": {"workspace_id": "sel-001", "stage": "drafting"}}

        def quality_evaluator(workspace: dict[str, Any]) -> dict[str, Any]:
            quality_calls["count"] += 1
            call_order.append("quality_evaluator")
            if quality_calls["count"] == 1:
                self.assertEqual(workspace["stage"], "input_intake")
                return {
                    "quality_status": "near_submission_candidate",
                    "blocker_report": {"report_kind": "quality_snapshot"},
                    "unresolved_blockers": ["关键论证尚未闭环"],
                    "evidence_gaps": ["机制证据需要补强"],
                }
            self.assertEqual(workspace["stage"], "drafting")
            return {
                "quality_status": "submission_grade_candidate",
                "blocker_report": {"report_kind": "quality_snapshot"},
                "unresolved_blockers": [],
                "evidence_gaps": [],
            }

        result = run_grant_autonomy_controller(
            request=self._selection_start_request(),
            selector=selector,
            initializer=initializer,
            mainline_runner=mainline_runner,
            quality_evaluator=quality_evaluator,
        )

        self.assertEqual(result["controller_status"], "submission_grade_candidate")
        self.assertEqual(result["termination_reason"], "goal_reached")
        self.assertEqual(result["completed_cycles"], 2)
        self.assertEqual(
            call_order,
            ["selector", "initializer", "quality_evaluator", "mainline_runner", "quality_evaluator"],
        )

    def test_workspace_path_can_finish_without_selector_initializer(self) -> None:
        selector_calls: list[str] = []

        def selector(_selection_input: dict[str, Any]) -> dict[str, Any]:
            selector_calls.append("selector")
            return {"selected_profile_id": "unused"}

        def initializer(_selection_input: dict[str, Any], _selection: dict[str, Any]) -> dict[str, Any]:
            raise AssertionError("workspace 起步不应进入 initializer")

        def mainline_runner(_payload: dict[str, Any]) -> dict[str, Any]:
            raise AssertionError("near_submission 且无 blocker 时不应进入 mainline_runner")

        def quality_evaluator(workspace: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(workspace["workspace_id"], "ws-001")
            return {
                "quality_status": "near_submission_candidate",
                "blocker_report": {"report_kind": "quality_snapshot"},
                "unresolved_blockers": [],
                "evidence_gaps": [],
            }

        result = run_grant_autonomy_controller(
            request=self._workspace_start_request(),
            selector=selector,
            initializer=initializer,
            mainline_runner=mainline_runner,
            quality_evaluator=quality_evaluator,
        )

        self.assertEqual(result["controller_status"], "near_submission_candidate")
        self.assertEqual(result["termination_reason"], "goal_reached")
        self.assertEqual(result["completed_cycles"], 1)
        self.assertEqual(selector_calls, [])

    def test_fail_closed_when_missing_required_input(self) -> None:
        request = self._selection_start_request()
        request["start"] = {"mode": "selection_input"}

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: payload,
            quality_evaluator=lambda workspace: workspace,
        )

        self.assertEqual(result["controller_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "missing_required_input")
        self.assertEqual(result["action_trace"], [])

    def test_fail_closed_when_quality_result_is_unstructured(self) -> None:
        result = run_grant_autonomy_controller(
            request=self._workspace_start_request(),
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: payload,
            quality_evaluator=lambda _workspace: ["bad-payload"],
        )

        self.assertEqual(result["controller_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "quality_evaluator_unstructured_result")

    def test_fail_closed_when_budget_exhausted(self) -> None:
        request = self._selection_start_request()
        request["budget"] = {"max_total_steps": 2}

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda _selection_input: {"selected_profile_id": "profile-nsfc"},
            initializer=lambda selection_input, _selection: {"workspace": {"workspace_id": selection_input["selection_input_id"]}},
            mainline_runner=lambda payload: {"workspace": payload["workspace"]},
            quality_evaluator=lambda _workspace: {
                "quality_status": "near_submission_candidate",
                "blocker_report": {"report_kind": "quality_snapshot"},
                "unresolved_blockers": ["blocker-a"],
                "evidence_gaps": [],
            },
        )

        self.assertEqual(result["controller_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "budget_exhausted")

    def test_fail_closed_when_blockers_not_cleared(self) -> None:
        result = run_grant_autonomy_controller(
            request=self._workspace_start_request(),
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: payload,
            quality_evaluator=lambda _workspace: {
                "quality_status": "submission_grade_candidate",
                "blocker_report": {"report_kind": "quality_snapshot"},
                "unresolved_blockers": ["blocker-a"],
                "evidence_gaps": [],
            },
        )

        self.assertEqual(result["controller_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "blockers_not_cleared")

    def test_reselection_decision_respected_when_policy_enabled(self) -> None:
        request = self._selection_start_request()
        quality_calls = {"count": 0}
        selection_calls = {"count": 0}

        def selector(_selection_input: dict[str, Any]) -> dict[str, Any]:
            selection_calls["count"] += 1
            return {"selected_profile_id": f"profile-{selection_calls['count']}"}

        def initializer(selection_input: dict[str, Any], selection: dict[str, Any]) -> dict[str, Any]:
            return {"workspace": {"workspace_id": selection_input["selection_input_id"], "stage": selection["selected_profile_id"]}}

        def quality_evaluator(workspace: dict[str, Any]) -> dict[str, Any]:
            quality_calls["count"] += 1
            if quality_calls["count"] == 1:
                self.assertEqual(workspace["stage"], "profile-1")
                return {
                    "quality_status": "near_submission_candidate",
                    "blocker_report": {"report_kind": "quality_snapshot"},
                    "unresolved_blockers": ["需要重选 profile"],
                    "evidence_gaps": [],
                }
            self.assertEqual(workspace["stage"], "profile-2")
            return {
                "quality_status": "submission_grade_candidate",
                "blocker_report": {"report_kind": "quality_snapshot"},
                "unresolved_blockers": [],
                "evidence_gaps": [],
            }

        def mainline_runner(_payload: dict[str, Any]) -> dict[str, Any]:
            return {
                "workspace": {"workspace_id": "sel-001", "stage": "drafting"},
                "reselection_decision": {"action": "reselect", "reason": "方向与机会不匹配"},
            }

        result = run_grant_autonomy_controller(
            request=request,
            selector=selector,
            initializer=initializer,
            mainline_runner=mainline_runner,
            quality_evaluator=quality_evaluator,
        )

        self.assertEqual(result["controller_status"], "submission_grade_candidate")
        self.assertEqual(result["termination_reason"], "goal_reached")
        self.assertEqual(selection_calls["count"], 2)
        self.assertEqual(len(result["reselection_decisions"]), 1)
        self.assertTrue(result["reselection_decisions"][0]["accepted"])

    def test_fail_closed_when_rollback_policy_disallows_request(self) -> None:
        request = self._workspace_start_request()

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: {
                "workspace": payload["workspace"],
                "rollback_decision": {"action": "rollback", "reason": "证据冲突"},
            },
            quality_evaluator=lambda _workspace: {
                "quality_status": "not_ready",
                "blocker_report": {"report_kind": "quality_snapshot"},
                "unresolved_blockers": ["需回滚到问题定义"],
                "evidence_gaps": [],
            },
        )

        self.assertEqual(result["controller_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "rollback_policy_disallowed")
        self.assertEqual(len(result["rollback_decisions"]), 1)
        self.assertFalse(result["rollback_decisions"][0]["accepted"])


if __name__ == "__main__":
    unittest.main()
