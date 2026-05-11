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


class GrantAutonomyControllerTest(unittest.TestCase):
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

    def _closure_package(
        self,
        *,
        closure_id: str,
        summary: str,
        severity: str = "hard",
        action: str = "continue_mainline",
        target_stage: str | None = None,
        required_input_ids: list[str] | None = None,
        linked_issue_ids: list[str] | None = None,
        blocking_reasons: list[str] | None = None,
        evidence_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        return {
            "closure_id": closure_id,
            "summary": summary,
            "severity": severity,
            "target_stage": target_stage,
            "action": action,
            "required_input_ids": list(required_input_ids or []),
            "evidence_refs": list(evidence_refs or []),
            "linked_issue_ids": list(linked_issue_ids or []),
            "blocking_reasons": list(blocking_reasons or []),
            "evidence_obligations": [],
            "acceptance_signals": [
                {
                    "signal_id": f"signal:{closure_id}",
                    "signal_kind": "controller_action",
                    "summary": summary,
                    "source_surface": "grant_quality",
                    "required_input_ids": list(required_input_ids or []),
                    "evidence_refs": list(evidence_refs or []),
                }
            ],
        }

    def _quality_result(
        self,
        *,
        quality_status: str,
        unresolved_blockers: list[str] | None = None,
        evidence_gaps: list[str] | None = None,
        closure_packages: list[dict[str, Any]] | None = None,
        evidence_supply_queue: list[dict[str, Any]] | None = None,
        workspace_id: str = "ws-001",
        lifecycle_stage: str = "critique",
        draft_id: str | None = "draft-001",
        grant_run_id: str = "grant-001",
        overall_score: int | None = None,
        overall_status: str | None = None,
        summary: str | None = None,
        loop_gate_action: str | None = None,
        loop_gate_stage: str | None = None,
        loop_gate_reason: str | None = None,
    ) -> dict[str, Any]:
        unresolved = list(unresolved_blockers or [])
        gaps = list(evidence_gaps or [])
        packages = [dict(item) for item in (closure_packages or [])]
        supply_queue = [dict(item) for item in (evidence_supply_queue or [])]
        resolved_overall_status = overall_status
        if resolved_overall_status is None:
            resolved_overall_status = quality_status if quality_status != "not_ready" else "blocked"
        resolved_score = overall_score
        if resolved_score is None:
            if quality_status == "submission_grade_candidate":
                resolved_score = 90
            elif quality_status == "near_submission_candidate":
                resolved_score = 78
            else:
                resolved_score = 55
        resolved_summary = summary or f"quality:{resolved_overall_status}"
        resolved_loop_gate_action = loop_gate_action
        if resolved_loop_gate_action is None:
            resolved_loop_gate_action = "continue" if quality_status != "not_ready" else "rollback_required"
        resolved_loop_gate_reason = loop_gate_reason or (unresolved[0] if unresolved else resolved_summary)
        gap_ids = [
            str(item.get("gap_id") or "").strip()
            for item in supply_queue
            if str(item.get("gap_id") or "").strip()
        ]
        status_counts: dict[str, list[str]] = {}
        kind_counts: dict[str, list[str]] = {}
        for item in supply_queue:
            gap_id = str(item.get("gap_id") or "").strip()
            supply_status = str(item.get("supply_status") or "").strip()
            gap_kind = str(item.get("gap_kind") or "").strip()
            if gap_id and supply_status:
                status_counts.setdefault(supply_status, []).append(gap_id)
            if gap_id and gap_kind:
                kind_counts.setdefault(gap_kind, []).append(gap_id)

        return {
            "quality_status": quality_status,
            "blocker_report": {
                "surface_kind": "grant_quality_scorecard",
                "overall_status": resolved_overall_status,
                "overall_score": resolved_score,
            },
            "unresolved_blockers": unresolved,
            "evidence_gaps": gaps,
            "evidence_supply_queue": supply_queue,
            "quality_closure_dossier": {
                "surface_kind": "grant_quality_closure_dossier",
                "dossier_version": 1,
                "workspace_surface_kind": "nsfc_workspace",
                "grant_run_id": grant_run_id,
                "workspace_id": workspace_id,
                "lifecycle_stage": lifecycle_stage,
                "draft_id": draft_id,
                "quality_summary": {
                    "overall_status": resolved_overall_status,
                    "overall_score": resolved_score,
                    "summary": resolved_summary,
                    "loop_gate": {
                        "action": resolved_loop_gate_action,
                        "recommended_stage": loop_gate_stage,
                        "reason": resolved_loop_gate_reason,
                    },
                },
                "unclosed_hard_issues": unresolved,
                "evidence_supply_queue_summary": {
                    "total_gap_count": len(gap_ids),
                    "outstanding_gap_ids": gap_ids,
                    "status_counts": [
                        {
                            "supply_status": status,
                            "count": len(ids),
                            "gap_ids": ids,
                        }
                        for status, ids in status_counts.items()
                    ],
                    "kind_counts": [
                        {
                            "gap_kind": gap_kind,
                            "count": len(ids),
                            "gap_ids": ids,
                        }
                        for gap_kind, ids in kind_counts.items()
                    ],
                },
                "closure_packages": packages,
            },
        }

    def test_report_exposes_tranche_plan_and_final_next_action(self) -> None:
        request = self._workspace_start_request()
        request["controller_plan"] = {
            "current_tranche": "quality_closure",
            "tranche_objective": "关闭质量硬伤并形成 near-submission candidate",
            "tranche_success_gate": {
                "target_status": "near_submission_candidate",
                "requires_zero_blockers": True,
                "requires_zero_evidence_gaps": True,
                "acceptance_criteria": ["质量硬伤清零"],
            },
        }
        quality_calls = {"count": 0}

        def mainline_runner(payload: dict[str, Any]) -> dict[str, Any]:
            self.assertEqual(payload["controller_plan"]["current_tranche"], "quality_closure")
            return {"workspace": {"workspace_id": "ws-001", "lifecycle_stage": "revision"}}

        def quality_evaluator(_workspace: dict[str, Any]) -> dict[str, Any]:
            quality_calls["count"] += 1
            if quality_calls["count"] == 1:
                return self._quality_result(
                    quality_status="not_ready",
                    unresolved_blockers=["科学问题尚未闭合"],
                    evidence_gaps=["申请人适配证据不足"],
                    closure_packages=[
                        self._closure_package(
                            closure_id="scientific-question",
                            summary="科学问题尚未闭合",
                            severity="hard",
                            action="rollback_upstream",
                            target_stage="question_refinement",
                            blocking_reasons=["科学问题尚未闭合"],
                        )
                    ],
                )
            return self._quality_result(
                quality_status="near_submission_candidate",
                unresolved_blockers=[],
                evidence_gaps=[],
                overall_status="near_submission_candidate",
            )

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=mainline_runner,
            quality_evaluator=quality_evaluator,
        )

        self.assertEqual(result["controller_status"], "near_submission_candidate")
        self.assertEqual(result["termination_reason"], "goal_reached")
        self.assertEqual(result["controller_plan"]["current_tranche"], "quality_closure")
        self.assertEqual(
            result["controller_plan"]["tranche_objective"],
            "关闭质量硬伤并形成 near-submission candidate",
        )
        self.assertEqual(result["controller_plan"]["tranche_success_gate"]["target_status"], "near_submission_candidate")
        self.assertEqual(result["controller_plan"]["next_controller_action"], "stop_success")
        self.assertEqual(result["controller_plan"]["decision_basis"]["quality_status"], "near_submission_candidate")
        self.assertEqual(result["tranche_history"][0]["active_closure_package_id"], "scientific-question")
        self.assertEqual(result["tranche_history"][0]["active_closure_package_action"], "rollback_upstream")
        self.assertEqual(result["tranche_history"][0]["closure_package_queue_ids"], ["scientific-question"])
        self.assertEqual(result["tranche_history"][0]["next_controller_action"], "continue_mainline")
        self.assertEqual(result["tranche_history"][0]["gate_status"], "open")
        self.assertEqual(result["tranche_history"][1]["next_controller_action"], "stop_success")
        self.assertEqual(result["tranche_history"][1]["gate_status"], "passed")
        self.assertEqual(result["latest_quality_closure_dossier"]["surface_kind"], "grant_quality_closure_dossier")
        self.assertEqual(result["closure_package_queue"], [])
        self.assertIsNone(result["active_closure_package"])

    def test_fail_closed_report_keeps_latest_active_closure_package(self) -> None:
        request = self._workspace_start_request()
        request["max_rounds_or_cycles"] = 1

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda _payload: (_ for _ in ()).throw(AssertionError("max=1 不应进入 mainline_runner")),
            quality_evaluator=lambda _workspace: self._quality_result(
                quality_status="not_ready",
                unresolved_blockers=["核心科学问题仍未成立"],
                evidence_gaps=["需要补充关键 preliminary evidence"],
                closure_packages=[
                    self._closure_package(
                        closure_id="evidence-gap",
                        summary="需要补充关键 preliminary evidence",
                        severity="gap",
                        action="continue_mainline",
                        target_stage="revision",
                        blocking_reasons=["需要补充关键 preliminary evidence"],
                    ),
                    self._closure_package(
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

        self.assertEqual(result["controller_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "blockers_not_cleared")
        self.assertEqual(result["active_closure_package"]["closure_id"], "scientific-question")
        self.assertEqual(result["active_closure_package"]["action"], "rollback_upstream")
        self.assertEqual(
            [item["closure_id"] for item in result["closure_package_queue"]],
            ["scientific-question", "evidence-gap"],
        )
        self.assertEqual(result["controller_plan"]["active_closure_package_id"], "scientific-question")
        self.assertEqual(result["controller_plan"]["active_closure_package_action"], "rollback_upstream")
        self.assertEqual(result["controller_plan"]["active_closure_package_target_stage"], "question_refinement")

    def test_family_governance_policy_shapes_default_controller_plan(self) -> None:
        request = self._workspace_start_request()
        request["start"]["workspace"] = {
            "workspace_id": "ws-nih-001",
            "lifecycle_stage": "critique",
            "project_profile": {
                "grant_family_grammar": {
                    "family_id": "nih_r21_translational_family_v1",
                    "governance_policy": {
                        "policy_id": "nih_r21_governance_v1",
                        "default_tranche": "quality_closure",
                        "preferred_stop_target": "near_submission_candidate",
                        "quality_bar": {
                            "minimum_score": 78,
                            "blocker_policy": "critical_blockers_must_close",
                            "required_signal_coverage": ["significance", "innovation"],
                        },
                        "rollback_bias": {
                            "default_rollback_stage": "fit_alignment",
                            "trigger_mode": "innovation_gap_sensitive",
                        },
                        "evidence_escalation_policy": {
                            "trigger": "significance_or_innovation_claim_unbounded",
                            "escalation_action": "tighten_aim_scope_and_add_translational_anchor",
                            "required_evidence_types": ["publication", "preliminary_result"],
                        },
                        "controller_defaults": {
                            "target_status": "near_submission_candidate",
                            "require_zero_blockers": True,
                            "require_zero_evidence_gaps": False,
                            "acceptance_criteria": ["significance / innovation 风险关闭"],
                        },
                    },
                }
            },
        }

        def quality_evaluator(_workspace: dict[str, Any]) -> dict[str, Any]:
            return self._quality_result(
                quality_status="near_submission_candidate",
                unresolved_blockers=[],
                evidence_gaps=["仍需补一条次级 supporting evidence"],
                overall_status="near_submission_candidate",
            )

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: payload,
            quality_evaluator=quality_evaluator,
        )

        self.assertEqual(result["controller_status"], "near_submission_candidate")
        self.assertEqual(result["controller_plan"]["current_tranche"], "quality_closure")
        self.assertEqual(result["controller_plan"]["tranche_success_gate"]["target_status"], "near_submission_candidate")
        self.assertFalse(result["controller_plan"]["tranche_success_gate"]["requires_zero_evidence_gaps"])
        self.assertEqual(
            result["controller_plan"]["tranche_success_gate"]["acceptance_criteria"],
            ["significance / innovation 风险关闭"],
        )

    def test_quality_supply_queue_can_trigger_inline_reselection(self) -> None:
        request = self._selection_start_request()
        request["goal"]["target_status"] = "near_submission_candidate"
        request["max_rounds_or_cycles"] = 2
        selector_calls = {"count": 0}
        initializer_calls = {"count": 0}
        quality_calls = {"count": 0}

        def selector(selection_input: dict[str, Any]) -> dict[str, Any]:
            selector_calls["count"] += 1
            return {"selected_profile_id": f"profile-{selector_calls['count']}"}

        def initializer(selection_input: dict[str, Any], selection: dict[str, Any]) -> dict[str, Any]:
            initializer_calls["count"] += 1
            return {
                "workspace": {
                    "workspace_id": f"{selection_input['selection_input_id']}-v{initializer_calls['count']}",
                    "lifecycle_stage": "input_intake",
                    "project_profile": {
                        "grant_family_grammar": {
                            "family_id": "nsfc_general_medical_family_v1",
                        }
                    },
                }
            }

        def quality_evaluator(workspace: dict[str, Any]) -> dict[str, Any]:
            quality_calls["count"] += 1
            if quality_calls["count"] == 1:
                self.assertEqual(workspace["workspace_id"], "sel-001-v1")
                return self._quality_result(
                    quality_status="not_ready",
                    unresolved_blockers=["当前 funding opportunity 与问题不匹配"],
                    evidence_gaps=["需要重选可兼容的 funding family"],
                    evidence_supply_queue=[
                        {
                            "gap_id": "gap-opportunity-fit",
                            "gap_kind": "funding_profile_mismatch",
                            "gap_summary": "当前 funding opportunity 与已选 family 不兼容。",
                            "supply_status": "reselection_required",
                            "controller_action_hint": {
                                "action": "reselect_project_profile",
                                "summary": "重选兼容的 funding / family 组合。",
                                "target_stage": None,
                                "source_surface": "grant_quality",
                            },
                            "required_input_ids": ["sel-001"],
                            "linked_issue_ids": ["unresolved_hard_issues:opportunity-fit"],
                            "linked_issue_summaries": ["当前 funding opportunity 与问题不匹配"],
                            "blocking_reasons": ["当前 funding opportunity 与问题不匹配"],
                            "supply_actions": [],
                            "evidence_refs": [],
                            "source_surfaces": ["grant_quality"],
                        }
                    ],
                    closure_packages=[
                        self._closure_package(
                            closure_id="gap-opportunity-fit",
                            summary="重选兼容的 funding / family 组合。",
                            severity="hard",
                            action="reselect_project_profile",
                            target_stage=None,
                            required_input_ids=["sel-001"],
                            linked_issue_ids=["unresolved_hard_issues:opportunity-fit"],
                            blocking_reasons=["当前 funding opportunity 与问题不匹配"],
                        )
                    ],
                    workspace_id="sel-001-v1",
                    lifecycle_stage="input_intake",
                )
            self.assertEqual(workspace["workspace_id"], "sel-001-v2")
            return self._quality_result(
                quality_status="near_submission_candidate",
                unresolved_blockers=[],
                evidence_gaps=[],
                evidence_supply_queue=[],
                closure_packages=[],
                workspace_id="sel-001-v2",
                lifecycle_stage="input_intake",
                overall_status="near_submission_candidate",
            )

        def mainline_runner(_payload: dict[str, Any]) -> dict[str, Any]:
            raise AssertionError("inline reselection 应在 quality signal 后直接发生，不应先进入 mainline_runner")

        result = run_grant_autonomy_controller(
            request=request,
            selector=selector,
            initializer=initializer,
            mainline_runner=mainline_runner,
            quality_evaluator=quality_evaluator,
        )

        self.assertEqual(result["controller_status"], "near_submission_candidate")
        self.assertEqual(selector_calls["count"], 2)
        self.assertEqual(initializer_calls["count"], 2)
        self.assertEqual(quality_calls["count"], 2)
        self.assertEqual(result["reselection_decisions"][0]["action"], "reselect")
        self.assertTrue(result["reselection_decisions"][0]["accepted"])
        self.assertEqual(result["tranche_history"][0]["next_controller_action"], "reselect_project_profile")

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
                return self._quality_result(
                    quality_status="near_submission_candidate",
                    unresolved_blockers=["关键论证尚未闭环"],
                    evidence_gaps=["机制证据需要补强"],
                    workspace_id="sel-001",
                    lifecycle_stage="input_intake",
                    closure_packages=[
                        self._closure_package(
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
            return self._quality_result(
                quality_status="submission_grade_candidate",
                unresolved_blockers=[],
                evidence_gaps=[],
                workspace_id="sel-001",
                lifecycle_stage="drafting",
                overall_status="submission_grade_candidate",
            )

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
            return self._quality_result(
                quality_status="near_submission_candidate",
                unresolved_blockers=[],
                evidence_gaps=[],
                workspace_id="ws-001",
                lifecycle_stage="critique",
                overall_status="near_submission_candidate",
            )

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
            quality_evaluator=lambda _workspace: self._quality_result(
                quality_status="near_submission_candidate",
                unresolved_blockers=["blocker-a"],
                evidence_gaps=[],
                overall_status="near_submission_candidate",
            ),
        )

        self.assertEqual(result["controller_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "budget_exhausted")

    def test_fail_closed_when_blockers_not_cleared(self) -> None:
        result = run_grant_autonomy_controller(
            request=self._workspace_start_request(),
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": {"selection": selection_input, "meta": selection}},
            mainline_runner=lambda payload: payload,
            quality_evaluator=lambda _workspace: self._quality_result(
                quality_status="submission_grade_candidate",
                unresolved_blockers=["blocker-a"],
                evidence_gaps=[],
                overall_status="submission_grade_candidate",
            ),
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
                return self._quality_result(
                    quality_status="near_submission_candidate",
                    unresolved_blockers=["需要重选 profile"],
                    evidence_gaps=[],
                    workspace_id="sel-001",
                    lifecycle_stage="profile-1",
                    closure_packages=[
                        self._closure_package(
                            closure_id="profile-fit",
                            summary="需要重选 profile",
                            severity="hard",
                            action="continue_mainline",
                            target_stage="revision",
                            required_input_ids=["sel-001"],
                            linked_issue_ids=["profile-fit"],
                            blocking_reasons=["需要重选 profile"],
                        )
                    ],
                    overall_status="near_submission_candidate",
                )
            self.assertEqual(workspace["stage"], "profile-2")
            return self._quality_result(
                quality_status="submission_grade_candidate",
                unresolved_blockers=[],
                evidence_gaps=[],
                workspace_id="sel-001",
                lifecycle_stage="profile-2",
                overall_status="submission_grade_candidate",
            )

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
        self.assertEqual(result["tranche_history"][0]["next_controller_action"], "reselect_project_profile")
        self.assertEqual(result["tranche_history"][0]["decision_reason"], "方向与机会不匹配")

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
            quality_evaluator=lambda _workspace: self._quality_result(
                quality_status="not_ready",
                unresolved_blockers=["需回滚到问题定义"],
                evidence_gaps=[],
                closure_packages=[
                    self._closure_package(
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

        self.assertEqual(result["controller_status"], "failed_closed")
        self.assertEqual(result["termination_reason"], "rollback_policy_disallowed")
        self.assertEqual(len(result["rollback_decisions"]), 1)
        self.assertFalse(result["rollback_decisions"][0]["accepted"])
        self.assertEqual(result["controller_plan"]["next_controller_action"], "fail_closed")
        self.assertEqual(result["tranche_history"][0]["next_controller_action"], "rollback_upstream")
        self.assertEqual(result["tranche_history"][0]["decision_reason"], "证据冲突")

    def test_resume_from_controller_report_continues_cycles_and_preserves_history(self) -> None:
        request = self._workspace_start_request()
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
            return self._quality_result(
                quality_status="not_ready",
                unresolved_blockers=["blocker-a"],
                evidence_gaps=["gap-a"],
                closure_packages=[
                    self._closure_package(
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
        self.assertEqual(quality_calls["count"], 2)
        self.assertEqual(first["completed_cycles"], 2)
        self.assertEqual(first["budget"]["spent_steps"], 3)
        self.assertEqual([entry["cycle"] for entry in first["tranche_history"]], [1, 2])
        self.assertIn("controller_checkpoint", first)

        resume_request = {
            "request_id": "autonomy-resume-001",
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
            return self._quality_result(
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
        self.assertEqual(result["controller_status"], "near_submission_candidate")
        self.assertEqual(result["termination_reason"], "goal_reached")
        self.assertEqual(result["completed_cycles"], 3)
        self.assertEqual(result["max_rounds_or_cycles"], 4)
        self.assertEqual(result["budget"]["max_total_steps"], 5)
        self.assertEqual(result["budget"]["spent_steps"], 4)
        self.assertEqual([entry["cycle"] for entry in result["tranche_history"]], [1, 2, 3])
        self.assertEqual(result["action_trace"][-1]["cycle"], 3)
        self.assertEqual(result["controller_plan"]["current_tranche"], first["controller_plan"]["current_tranche"])
        self.assertEqual(result["controller_checkpoint"]["resume_start_mode"], "controller_report")
        self.assertEqual(result["controller_checkpoint"]["workspace_id"], "ws-001")
        self.assertEqual(result["controller_checkpoint"]["completed_cycles"], 3)
        self.assertEqual(result["controller_checkpoint"]["next_controller_action"], "stop_success")


if __name__ == "__main__":
    unittest.main()
