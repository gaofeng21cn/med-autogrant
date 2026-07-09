from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.grant_autonomy_controller import run_grant_autonomy_controller  # noqa: E402
from med_autogrant.grant_autonomy_trace import spend_budget_step  # noqa: E402
from tests.support.grant_autonomy_controller import (  # noqa: E402
    OPL_STAGE_ATTEMPT,
    closure_package,
    quality_result,
    selection_start_request,
    workspace_start_request,
)


class GrantAutonomyControllerTest(unittest.TestCase):
    def assert_status(self, result: dict[str, Any], status: str, reason: str) -> None:
        self.assertEqual(result["controller_status"], status)
        self.assertEqual(result["termination_reason"], reason)

    def assert_typed_blocker_return(self, result: dict[str, Any], ref: str | None = None) -> None:
        self.assertEqual(result["authority_return"]["result_shape"], "typed_blocker")
        if ref is not None:
            self.assertEqual(result["authority_return"]["refs"]["typed_blocker_ref"], ref)

    def assert_mag_does_not_own_attempt_ledger(self, boundary: dict[str, Any]) -> None:
        self.assertFalse(boundary["mag_long_running_driver"])
        self.assertFalse(boundary["mag_owns_attempt_ledger"])

    def test_spend_budget_step_records_action_trace_without_overrun(self) -> None:
        action_trace: list[dict[str, Any]] = []

        ok, spent_steps = spend_budget_step(
            spent_steps=0,
            budget_max=1,
            action_trace=action_trace,
            step_action="quality_evaluator",
            cycle=3,
        )

        self.assertTrue(ok)
        self.assertEqual(spent_steps, 1)
        self.assertEqual(
            action_trace,
            [
                {
                    "step_action": "quality_evaluator",
                    "cycle": 3,
                    "step_index": 1,
                    "result": "executed",
                }
            ],
        )

        ok, spent_steps = spend_budget_step(
            spent_steps=spent_steps,
            budget_max=1,
            action_trace=action_trace,
            step_action="mainline_runner",
            cycle=3,
        )

        self.assertFalse(ok)
        self.assertEqual(spent_steps, 1)
        self.assertEqual(len(action_trace), 1)

    def test_runtime_quality_evaluator_keeps_projection_only_scorecard_not_ready(self) -> None:
        from med_autogrant.domain_runtime_parts.runtime_ops import build_autonomy_quality_evaluator_output

        workspace = json.loads((REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json").read_text(encoding="utf-8"))
        for critique in workspace["mentor_critiques"]:
            critique.get("metadata", {}).pop("owner", None)

        quality_output = build_autonomy_quality_evaluator_output(workspace)

        self.assertEqual(quality_output["quality_status"], "not_ready")
        self.assertIn("AI reviewer-backed critique", quality_output["unresolved_blockers"][0])
        self.assertTrue(quality_output["blocker_report"]["ai_reviewer_required"])
        self.assertEqual(quality_output["blocker_report"]["assessment_owner"], "projection_only")

    def test_fail_closed_report_keeps_latest_active_closure_package(self) -> None:
        request = workspace_start_request()
        request["max_rounds_or_cycles"] = 1

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda _payload: (_ for _ in ()).throw(AssertionError("max=1 不应进入 mainline_runner")),
            quality_evaluator=lambda _workspace: quality_result(
                quality_status="not_ready",
                unresolved_blockers=["核心科学问题仍未成立"],
                evidence_gaps=["需要补充关键 preliminary evidence"],
                closure_packages=[
                    closure_package(
                        closure_id="evidence-gap",
                        summary="需要补充关键 preliminary evidence",
                        severity="gap",
                        action="continue_mainline",
                        target_stage="revision",
                        blocking_reasons=["需要补充关键 preliminary evidence"],
                    ),
                    closure_package(
                        closure_id="scientific-question",
                        summary="核心科学问题仍未成立",
                        severity="hard",
                        action="rollback_upstream",
                        target_stage="question_refinement",
                        blocking_reasons=["核心科学问题仍未成立"],
                    ),
                ],
            ),
        )

        self.assert_status(result, "failed_closed", "blockers_not_cleared")
        self.assertEqual(result["active_closure_package"]["closure_id"], "scientific-question")
        self.assertEqual(result["active_closure_package"]["action"], "rollback_upstream")
        self.assertEqual(
            [item["closure_id"] for item in result["closure_package_queue"]],
            ["scientific-question", "evidence-gap"],
        )
        self.assertEqual(result["controller_plan"]["active_closure_package_id"], "scientific-question")
        self.assertEqual(result["controller_plan"]["active_closure_package_action"], "rollback_upstream")
        self.assertEqual(result["controller_plan"]["active_closure_package_target_stage"], "question_refinement")
        self.assert_typed_blocker_return(result)
        self.assertIn("typed_blocker_ref", result["authority_return"]["refs"])

    def test_selection_input_path_yields_after_one_domain_attempt_for_opl_provider_residency(self) -> None:
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
                return quality_result(
                    quality_status="near_submission_candidate",
                    unresolved_blockers=["关键论证尚未闭环"],
                    evidence_gaps=["机制证据需要补强"],
                    workspace_id="sel-001",
                    lifecycle_stage="input_intake",
                    closure_packages=[
                        closure_package(
                            closure_id="argument-closure",
                            summary="关键论证尚未闭环",
                            severity="hard",
                            action="continue_mainline",
                            target_stage="argument_building",
                            blocking_reasons=["关键论证尚未闭环"],
                        )
                    ],
                    overall_status="near_submission_candidate",
                )
            self.assertEqual(workspace["stage"], "drafting")
            return quality_result(
                quality_status="submission_grade_candidate",
                unresolved_blockers=[],
                evidence_gaps=[],
                workspace_id="sel-001",
                lifecycle_stage="drafting",
                overall_status="submission_grade_candidate",
            )

        result = run_grant_autonomy_controller(
            request=selection_start_request(),
            selector=selector,
            initializer=initializer,
            mainline_runner=mainline_runner,
            quality_evaluator=quality_evaluator,
        )

        self.assert_status(result, "failed_closed", "opl_provider_attempt_required")
        self.assertEqual(result["completed_cycles"], 1)
        self.assertEqual(
            call_order,
            ["selector", "initializer", "quality_evaluator", "mainline_runner"],
        )
        self.assertEqual(result["controller_plan"]["next_controller_action"], "continue_mainline")
        self.assert_typed_blocker_return(result, "typed-blocker:mag/autonomy-controller/opl-provider-attempt-required")
        self.assertEqual(
            result["controller_execution_boundary"]["max_domain_cycles_per_invocation"],
            1,
        )
        self.assertEqual(
            result["controller_execution_boundary"]["attempt_ledger_owner"],
            "one-person-lab",
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
            return quality_result(
                quality_status="near_submission_candidate",
                unresolved_blockers=[],
                evidence_gaps=[],
                workspace_id="ws-001",
                lifecycle_stage="critique",
                overall_status="near_submission_candidate",
            )

        result = run_grant_autonomy_controller(
            request=workspace_start_request(),
            selector=selector,
            initializer=initializer,
            mainline_runner=mainline_runner,
            quality_evaluator=quality_evaluator,
        )

        self.assert_status(result, "near_submission_candidate", "goal_reached")
        self.assertEqual(result["completed_cycles"], 1)
        self.assertEqual(selector_calls, [])
        self.assertEqual(
            result["controller_execution_boundary"]["execution_scope"],
            "bounded_single_opl_provider_attempt",
        )
        self.assert_mag_does_not_own_attempt_ledger(result["controller_execution_boundary"])
        self.assertEqual(result["authority_return"]["result_shape"], "no_regression_evidence")

    def test_fail_closed_when_missing_required_input(self) -> None:
        request = selection_start_request()
        request["start"] = {"mode": "selection_input"}

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: payload,
            quality_evaluator=lambda workspace: workspace,
        )

        self.assert_status(result, "failed_closed", "missing_required_input")
        self.assertEqual(result["action_trace"], [])

    def test_fail_closed_when_quality_result_is_unstructured(self) -> None:
        result = run_grant_autonomy_controller(
            request=workspace_start_request(),
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: payload,
            quality_evaluator=lambda _workspace: ["bad-payload"],
        )

        self.assert_status(result, "failed_closed", "quality_evaluator_unstructured_result")

    def test_fail_closed_when_budget_exhausted(self) -> None:
        request = selection_start_request()
        request["budget"] = {"max_total_steps": 2}

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda _selection_input: {"selected_profile_id": "profile-nsfc"},
            initializer=lambda selection_input, _selection: {"workspace": {"workspace_id": selection_input["selection_input_id"]}},
            mainline_runner=lambda payload: {"workspace": payload["workspace"]},
            quality_evaluator=lambda _workspace: quality_result(
                quality_status="near_submission_candidate",
                unresolved_blockers=["blocker-a"],
                evidence_gaps=[],
                overall_status="near_submission_candidate",
            ),
        )

        self.assert_status(result, "failed_closed", "budget_exhausted")

    def test_fail_closed_when_blockers_not_cleared(self) -> None:
        result = run_grant_autonomy_controller(
            request=workspace_start_request(),
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: payload,
            quality_evaluator=lambda _workspace: quality_result(
                quality_status="submission_grade_candidate",
                unresolved_blockers=["blocker-a"],
                evidence_gaps=[],
                overall_status="submission_grade_candidate",
            ),
        )

        self.assert_status(result, "failed_closed", "blockers_not_cleared")

    def test_fail_closed_when_rollback_policy_disallows_request(self) -> None:
        request = workspace_start_request()

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: {
                "workspace": payload["workspace"],
                "rollback_decision": {"action": "rollback", "reason": "证据冲突"},
            },
            quality_evaluator=lambda _workspace: quality_result(
                quality_status="not_ready",
                unresolved_blockers=["需回滚到问题定义"],
                evidence_gaps=[],
                closure_packages=[
                    closure_package(
                        closure_id="question-definition",
                        summary="需回滚到问题定义",
                        severity="hard",
                        action="rollback_upstream",
                        target_stage="question_refinement",
                        blocking_reasons=["需回滚到问题定义"],
                    )
                ],
            ),
        )

        self.assert_status(result, "failed_closed", "rollback_policy_disallowed")
        self.assertEqual(len(result["rollback_decisions"]), 1)
        self.assertFalse(result["rollback_decisions"][0]["accepted"])
        self.assertEqual(result["controller_plan"]["next_controller_action"], "fail_closed")
        self.assertEqual(result["tranche_history"][0]["next_controller_action"], "rollback_upstream")
        self.assertEqual(result["tranche_history"][0]["decision_reason"], "证据冲突")

    def test_resume_from_controller_report_continues_cycles_and_preserves_history(self) -> None:
        request = workspace_start_request()
        request["goal"]["target_status"] = "near_submission_candidate"
        request["max_rounds_or_cycles"] = 2
        request["budget"] = {"max_total_steps": 10}
        request["blocker_queue"] = ["seed blocker"]
        request["evidence_gap_queue"] = ["seed gap"]
        request["controller_plan"] = {
            "current_tranche": "quality_closure",
            "tranche_objective": "close blockers then resume",
            "tranche_success_gate": {
                "target_status": "near_submission_candidate",
                "requires_zero_blockers": True,
                "requires_zero_evidence_gaps": True,
            },
        }
        mainline_calls = {"count": 0}
        quality_calls = {"count": 0}

        def mainline_runner(payload: dict[str, Any]) -> dict[str, Any]:
            mainline_calls["count"] += 1
            workspace = payload["workspace"]
            self.assertEqual(workspace["workspace_id"], "ws-001")
            return {"workspace": {"workspace_id": "ws-001", "lifecycle_stage": "revision"}}

        def quality_evaluator(_workspace: dict[str, Any]) -> dict[str, Any]:
            quality_calls["count"] += 1
            return quality_result(
                quality_status="not_ready",
                unresolved_blockers=["blocker-a"],
                evidence_gaps=["gap-a"],
                closure_packages=[
                        closure_package(
                        closure_id="blocker-a",
                        summary="blocker-a",
                        severity="hard",
                        action="continue_mainline",
                        target_stage="revision",
                        blocking_reasons=["blocker-a"],
                    )
                ],
            )

        first = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=mainline_runner,
            quality_evaluator=quality_evaluator,
        )

        self.assertEqual(mainline_calls["count"], 1)
        self.assertEqual(quality_calls["count"], 1)
        self.assertEqual(first["completed_cycles"], 1)
        self.assertEqual(first["budget"]["spent_steps"], 2)
        self.assertEqual([entry["cycle"] for entry in first["tranche_history"]], [1])
        self.assertIn("controller_checkpoint", first)

        resume_request = {
            "request_id": "autonomy-resume-001",
            "opl_stage_attempt": dict(OPL_STAGE_ATTEMPT),
            "start": {"mode": "controller_report", "controller_report": first},
            "goal": request["goal"],
            "max_rounds_or_cycles": 2,
            "budget": {"max_total_steps": 2},
            "stop_conditions": request["stop_conditions"],
            "blocker_queue": [],
            "evidence_gap_queue": [],
            "reselection_policy": request["reselection_policy"],
            "rollback_policy": request["rollback_policy"],
        }

        def quality_evaluator_resume(workspace: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(workspace["lifecycle_stage"], "revision")
            return quality_result(
                quality_status="near_submission_candidate",
                unresolved_blockers=[],
                evidence_gaps=[],
                workspace_id="ws-001",
                lifecycle_stage="revision",
                overall_status="near_submission_candidate",
            )

        result = run_grant_autonomy_controller(
            request=resume_request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda _payload: (_ for _ in ()).throw(AssertionError("resume success 不应再进入 mainline_runner")),
            quality_evaluator=quality_evaluator_resume,
        )

        self.assertEqual(result["started_from_mode"], "controller_report")
        self.assert_status(result, "near_submission_candidate", "goal_reached")
        self.assertEqual(result["completed_cycles"], 2)
        self.assertEqual(result["max_rounds_or_cycles"], 3)
        self.assertEqual(result["budget"]["max_total_steps"], 4)
        self.assertEqual(result["budget"]["spent_steps"], 3)
        self.assertEqual([entry["cycle"] for entry in result["tranche_history"]], [1, 2])
        self.assertEqual(result["action_trace"][-1]["cycle"], 2)
        self.assertEqual(result["controller_plan"]["current_tranche"], first["controller_plan"]["current_tranche"])
        self.assertEqual(result["controller_checkpoint"]["resume_start_mode"], "controller_report")
        self.assertEqual(result["controller_checkpoint"]["workspace_id"], "ws-001")
        self.assertEqual(result["controller_checkpoint"]["completed_cycles"], 2)
        self.assertEqual(result["controller_checkpoint"]["next_controller_action"], "stop_success")


if __name__ == "__main__":
    unittest.main()
