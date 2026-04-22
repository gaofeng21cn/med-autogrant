from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
NIH_SELECTION_INPUT_PATH = REPO_ROOT / "examples" / "profile_selection_input_nih_r21.json"


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


class HermesRuntimeAutonomyControllerTest(unittest.TestCase):
    def _quality_summary(
        self,
        *,
        overall_status: str,
        overall_score: int,
        recommended_stage: str | None,
        reason: str,
    ) -> dict[str, object]:
        return {
            "overall_status": overall_status,
            "overall_score": overall_score,
            "summary": f"quality:{overall_status}",
            "loop_gate": {
                "action": "ready_for_submission" if overall_status == "submission_grade_candidate" else "continue",
                "recommended_stage": recommended_stage,
                "reason": reason,
            },
        }

    def _quality_dossier(
        self,
        *,
        workspace: dict[str, object],
        overall_status: str,
        overall_score: int,
        recommended_stage: str | None,
        reason: str,
    ) -> dict[str, object]:
        summary = self._quality_summary(
            overall_status=overall_status,
            overall_score=overall_score,
            recommended_stage=recommended_stage,
            reason=reason,
        )
        current_selection = workspace.get("current_selection") if isinstance(workspace, dict) else {}
        draft_id = current_selection.get("active_draft_id") if isinstance(current_selection, dict) else None
        return {
            "surface_kind": "grant_quality_closure_dossier",
            "dossier_version": 1,
            "workspace_surface_kind": "nsfc_workspace",
            "grant_run_id": workspace["grant_run_id"],
            "workspace_id": workspace["workspace_id"],
            "lifecycle_stage": workspace["lifecycle_stage"],
            "draft_id": draft_id,
            "quality_summary": summary,
            "unclosed_hard_issues": [],
            "evidence_supply_queue_summary": {
                "total_gap_count": 0,
                "outstanding_gap_ids": [],
                "status_counts": [],
                "kind_counts": [],
            },
            "closure_packages": [],
        }

    def _controller_plan_quality_fields(
        self,
        *,
        quality_summary: dict[str, object],
    ) -> dict[str, object]:
        return {
            "quality_summary": quality_summary,
            "closure_package_queue_ids": [],
            "active_closure_package_id": None,
            "active_closure_package_action": None,
            "active_closure_package_target_stage": None,
        }

    def test_execute_grant_autonomy_controller_validates_and_writes_report(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        workspace = _load_json(FROZEN_EXAMPLE_PATH)
        quality_summary = self._quality_summary(
            overall_status="submission_grade_candidate",
            overall_score=90,
            recommended_stage="frozen",
            reason="ready",
        )
        quality_dossier = self._quality_dossier(
            workspace=workspace,
            overall_status="submission_grade_candidate",
            overall_score=90,
            recommended_stage="frozen",
            reason="ready",
        )
        request = {
            "request_id": "autonomy-req-001",
            "start": {
                "mode": "workspace",
                "workspace": workspace,
            },
            "goal": {
                "target_status": "submission_grade_candidate",
                "summary": "produce submission-grade candidate",
            },
            "max_rounds_or_cycles": 1,
            "budget": {
                "max_total_steps": 4,
            },
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
        report = {
            "surface_kind": "grant_autonomy_controller_report",
            "controller_version": 3,
            "controller_checkpoint": {
                "checkpoint_id": "checkpoint-001",
                "resume_start_mode": "controller_report",
                "workspace_id": workspace["workspace_id"],
                "completed_cycles": 1,
                "next_controller_action": "stop_success",
            },
            "request_id": "autonomy-req-001",
            "controller_status": "submission_grade_candidate",
            "termination_reason": "goal_reached",
            "started_from_mode": "workspace",
            "goal": request["goal"],
            "completed_cycles": 1,
            "max_rounds_or_cycles": 1,
            "budget": {
                "max_total_steps": 4,
                "spent_steps": 1,
                "remaining_steps": 3,
                "exhausted": False,
            },
            "blocker_report": {
                "initial_blocker_queue": [],
                "initial_evidence_gap_queue": [],
                "latest_quality_blocker_report": {"surface_kind": "grant_quality_scorecard"},
                "unresolved_blocker_count": 0,
                "evidence_gap_count": 0,
            },
            "unresolved_blockers": [],
            "evidence_gaps": [],
            "action_trace": [
                {
                    "step_action": "quality_evaluator",
                    "cycle": 1,
                    "step_index": 1,
                    "result": "executed",
                }
            ],
            "reselection_decisions": [],
            "rollback_decisions": [],
            "latest_quality_closure_dossier": quality_dossier,
            "closure_package_queue": [],
            "active_closure_package": None,
            "controller_plan": {
                "current_tranche": "submission_readiness",
                "tranche_objective": "advance_to_submission_grade_candidate",
                "tranche_success_gate": {
                    "target_status": "submission_grade_candidate",
                    "requires_zero_blockers": True,
                    "requires_zero_evidence_gaps": True,
                },
                **self._controller_plan_quality_fields(quality_summary=quality_summary),
                "next_controller_action": "stop_success",
                "decision_basis": {
                    "cycle": 1,
                    "gate_status": "passed",
                    "quality_status": "submission_grade_candidate",
                    "unresolved_blockers": [],
                    "evidence_gaps": [],
                    **self._controller_plan_quality_fields(quality_summary=quality_summary),
                    "decision_reason": "tranche_success_gate_satisfied",
                    "termination_reason": "goal_reached",
                },
            },
            "tranche_history": [
                {
                    "cycle": 1,
                    "current_tranche": "submission_readiness",
                    "tranche_objective": "advance_to_submission_grade_candidate",
                    "tranche_success_gate": {
                        "target_status": "submission_grade_candidate",
                        "requires_zero_blockers": True,
                        "requires_zero_evidence_gaps": True,
                    },
                    "gate_status": "passed",
                    "next_controller_action": "stop_success",
                    "decision_reason": "tranche_success_gate_satisfied",
                    "quality_status": "submission_grade_candidate",
                    "unresolved_blockers": [],
                    "evidence_gaps": [],
                    **self._controller_plan_quality_fields(quality_summary=quality_summary),
                    "termination_reason": "goal_reached",
                }
            ],
            "final_workspace": workspace,
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            request_path = Path(tmp_dir) / "autonomy-request.json"
            output_dir = Path(tmp_dir) / "autonomy-output"
            request_path.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")

            with patch("med_autogrant.hermes_runtime.run_grant_autonomy_controller") as run_controller:
                run_controller.return_value = report
                payload = HermesRuntimeSubstrate().execute_grant_autonomy_controller(
                    input_path=request_path,
                    output_dir=output_dir,
                )

                self.assertTrue(payload["ok"])
                self.assertEqual(payload["command"], "execute-grant-autonomy-controller")
                self.assertEqual(payload["controller_status"], "submission_grade_candidate")
                self.assertTrue(Path(payload["grant_autonomy_controller_report_path"]).exists())
                self.assertTrue(Path(payload["final_workspace_path"]).exists())
                self.assertEqual(payload["grant_autonomy_controller_report"], report)
                run_controller.assert_called_once()

    def test_execute_grant_autonomy_controller_preserves_nih_family_grammar_from_selection_start(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        selection_input = _load_json(NIH_SELECTION_INPUT_PATH)
        final_workspace = _load_json(FROZEN_EXAMPLE_PATH)
        quality_summary = self._quality_summary(
            overall_status="near_submission_candidate",
            overall_score=78,
            recommended_stage="revision",
            reason="keep improving",
        )
        quality_dossier = self._quality_dossier(
            workspace=final_workspace,
            overall_status="near_submission_candidate",
            overall_score=78,
            recommended_stage="revision",
            reason="keep improving",
        )
        request = {
            "request_id": "autonomy-req-nih-001",
            "start": {
                "mode": "selection_input",
                "selection_input": selection_input,
            },
            "goal": {
                "target_status": "near_submission_candidate",
                "summary": "prove NIH R21 can enter the same autonomy controller lane",
            },
            "max_rounds_or_cycles": 1,
            "budget": {
                "max_total_steps": 4,
            },
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
        report = {
            "surface_kind": "grant_autonomy_controller_report",
            "controller_version": 3,
            "controller_checkpoint": {
                "checkpoint_id": "checkpoint-nih-001",
                "resume_start_mode": "controller_report",
                "workspace_id": "nsfc-demo-001",
                "completed_cycles": 1,
                "next_controller_action": "stop_success",
            },
            "request_id": "autonomy-req-nih-001",
            "controller_status": "near_submission_candidate",
            "termination_reason": "goal_reached",
            "started_from_mode": "selection_input",
            "goal": request["goal"],
            "completed_cycles": 1,
            "max_rounds_or_cycles": 1,
            "budget": {
                "max_total_steps": 4,
                "spent_steps": 3,
                "remaining_steps": 1,
                "exhausted": False,
            },
            "blocker_report": {
                "initial_blocker_queue": [],
                "initial_evidence_gap_queue": [],
                "latest_quality_blocker_report": {"surface_kind": "grant_quality_scorecard"},
                "unresolved_blocker_count": 0,
                "evidence_gap_count": 0,
            },
            "unresolved_blockers": [],
            "evidence_gaps": [],
            "action_trace": [],
            "reselection_decisions": [],
            "rollback_decisions": [],
            "latest_quality_closure_dossier": quality_dossier,
            "closure_package_queue": [],
            "active_closure_package": None,
            "controller_plan": {
                "current_tranche": "quality_closure",
                "tranche_objective": "advance_to_near_submission_candidate",
                "tranche_success_gate": {
                    "target_status": "near_submission_candidate",
                    "requires_zero_blockers": True,
                    "requires_zero_evidence_gaps": True,
                },
                **self._controller_plan_quality_fields(quality_summary=quality_summary),
                "next_controller_action": "stop_success",
                "decision_basis": {
                    "cycle": 1,
                    "gate_status": "passed",
                    "quality_status": "near_submission_candidate",
                    "unresolved_blockers": [],
                    "evidence_gaps": [],
                    **self._controller_plan_quality_fields(quality_summary=quality_summary),
                    "decision_reason": "tranche_success_gate_satisfied",
                    "termination_reason": "goal_reached",
                },
            },
            "tranche_history": [
                {
                    "cycle": 1,
                    "current_tranche": "quality_closure",
                    "tranche_objective": "advance_to_near_submission_candidate",
                    "tranche_success_gate": {
                        "target_status": "near_submission_candidate",
                        "requires_zero_blockers": True,
                        "requires_zero_evidence_gaps": True,
                    },
                    "gate_status": "passed",
                    "next_controller_action": "stop_success",
                    "decision_reason": "tranche_success_gate_satisfied",
                    "quality_status": "near_submission_candidate",
                    "unresolved_blockers": [],
                    "evidence_gaps": [],
                    **self._controller_plan_quality_fields(quality_summary=quality_summary),
                    "termination_reason": "goal_reached",
                }
            ],
            "final_workspace": final_workspace,
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            request_path = Path(tmp_dir) / "autonomy-nih-request.json"
            output_dir = Path(tmp_dir) / "autonomy-nih-output"
            request_path.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")

            def _run_controller_side_effect(**kwargs: object) -> dict[str, object]:
                selector = kwargs["selector"]
                initializer = kwargs["initializer"]
                request_payload = kwargs["request"]
                self.assertIsInstance(request_payload, dict)
                self.assertIsInstance(selector, object)
                self.assertIsInstance(initializer, object)
                selection = selector(request["start"]["selection_input"])
                initialized = initializer(request["start"]["selection_input"], selection)
                grammar = initialized["workspace"]["project_profile"]["grant_family_grammar"]
                self.assertEqual(grammar["family_id"], "nih_r21_translational_family_v1")
                self.assertEqual(grammar["funder"], "NIH")
                self.assertIn("execute-grant-autonomy-controller", grammar["governance_entry_points"])
                return report

            with patch("med_autogrant.hermes_runtime.run_grant_autonomy_controller") as run_controller:
                run_controller.side_effect = _run_controller_side_effect
                payload = HermesRuntimeSubstrate().execute_grant_autonomy_controller(
                    input_path=request_path,
                    output_dir=output_dir,
                )

                self.assertTrue(payload["ok"])
                self.assertEqual(payload["controller_status"], "near_submission_candidate")
                run_controller.assert_called_once()

    def test_execute_grant_autonomy_controller_keeps_nih_family_trace_from_selection_input(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        selection_input = _load_json(NIH_SELECTION_INPUT_PATH)
        request = {
            "request_id": "autonomy-nih-r21-proof-001",
            "start": {
                "mode": "selection_input",
                "selection_input": selection_input,
            },
            "goal": {
                "target_status": "near_submission_candidate",
                "summary": "prove NIH R21 can stay inside the shared autonomy contract",
            },
            "max_rounds_or_cycles": 1,
            "budget": {
                "max_total_steps": 4,
            },
            "stop_conditions": {
                "require_zero_blockers": False,
                "require_zero_evidence_gaps": False,
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

        with tempfile.TemporaryDirectory() as tmp_dir:
            request_path = Path(tmp_dir) / "autonomy-request.json"
            output_dir = Path(tmp_dir) / "autonomy-output"
            request_path.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")

            payload = HermesRuntimeSubstrate().execute_grant_autonomy_controller(
                input_path=request_path,
                output_dir=output_dir,
            )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["workspace_id"], "profile-select-nih-demo")
        self.assertEqual(payload["termination_reason"], "blockers_not_cleared")
        self.assertEqual(
            payload["grant_autonomy_controller_report"]["started_from_mode"],
            "selection_input",
        )
        family_trace = payload["final_workspace"]["project_profile"]["family_grammar_trace"]
        self.assertEqual(family_trace["family_id"], "nih_r21_translational_family_v1")
        self.assertEqual(family_trace["funder"], "NIH")
        self.assertEqual(
            family_trace["review_grammar"]["critique_policy"]["policy_id"],
            "nih_r21_significance_innovation_v1",
        )
        self.assertTrue(
            any(
                item["rule_id"] == "rule.program_family"
                and "NIH R21 Parent" in item["allowed_values"]
                for item in family_trace["family_compatibility_hooks"]
            )
        )

    def test_autonomy_quality_evaluator_output_includes_closure_dossier(self) -> None:
        from med_autogrant.hermes_runtime import _build_autonomy_quality_evaluator_output

        workspace = _load_json(FROZEN_EXAMPLE_PATH)
        payload = _build_autonomy_quality_evaluator_output(workspace)

        self.assertIn("quality_closure_dossier", payload)
        dossier = payload["quality_closure_dossier"]
        self.assertEqual(dossier["surface_kind"], "grant_quality_closure_dossier")
        self.assertEqual(dossier["workspace_id"], workspace["workspace_id"])
        self.assertIsInstance(dossier["closure_packages"], list)
        self.assertEqual(
            dossier["quality_summary"]["overall_status"],
            payload["blocker_report"]["overall_status"],
        )
