from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class HermesRuntimeQualityGateTest(unittest.TestCase):
    def test_quality_gate_can_force_mainline_route_to_rollback(self) -> None:
        from med_autogrant.hermes_runtime import _apply_quality_gate_to_route

        route = {
            "current_stage": "critique",
            "recommended_stage": "revision",
            "reason": "导师建议进入 revision",
        }
        scorecard = {
            "loop_gate": {
                "action": "rollback_required",
                "recommended_stage": "argument_building",
                "reason": "必要性链条未闭合。",
            }
        }

        resolved = _apply_quality_gate_to_route(route=route, quality_scorecard=scorecard)

        self.assertEqual(resolved["recommended_stage"], "argument_building")
        self.assertEqual(resolved["quality_gate"]["action"], "rollback_required")
        self.assertIn("必要性链条未闭合", resolved["reason"])

    def test_quality_gate_can_veto_submission_stop(self) -> None:
        from med_autogrant.hermes_runtime import _apply_quality_gate_to_route

        route = {
            "current_stage": "critique",
            "recommended_stage": "frozen",
            "reason": "批注建议可以进入 frozen",
        }
        scorecard = {
            "loop_gate": {
                "action": "continue",
                "recommended_stage": "revision",
                "reason": "仍有未关闭问题。",
            }
        }

        resolved = _apply_quality_gate_to_route(route=route, quality_scorecard=scorecard)

        self.assertEqual(resolved["recommended_stage"], "revision")
        self.assertEqual(resolved["quality_gate"]["action"], "continue")
        self.assertIn("仍有未关闭问题", resolved["reason"])
