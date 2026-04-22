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


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


class HermesRuntimeAutonomyControllerTest(unittest.TestCase):
    def test_execute_grant_autonomy_controller_validates_and_writes_report(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        workspace = _load_json(FROZEN_EXAMPLE_PATH)
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
            "controller_version": 1,
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
            "controller_plan": {
                "current_tranche": "submission_readiness",
                "tranche_objective": "advance_to_submission_grade_candidate",
                "tranche_success_gate": {
                    "target_status": "submission_grade_candidate",
                    "requires_zero_blockers": True,
                    "requires_zero_evidence_gaps": True,
                },
                "next_controller_action": "stop_success",
                "decision_basis": {
                    "cycle": 1,
                    "gate_status": "passed",
                    "quality_status": "submission_grade_candidate",
                    "unresolved_blockers": [],
                    "evidence_gaps": [],
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
