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

REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
DRAFTING_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json"


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


class MagRuntimeQualityGateTest(unittest.TestCase):
    def test_quality_gate_can_force_mainline_route_to_rollback(self) -> None:
        from med_autogrant.domain_runtime_parts.runtime_ops import _apply_quality_gate_to_route

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
        from med_autogrant.domain_runtime_parts.runtime_ops import _apply_quality_gate_to_route

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

    def test_execute_critique_revision_loop_report_embeds_quality_surfaces(self) -> None:
        from med_autogrant.grant_quality import (
            build_grant_quality_closure_dossier as build_closure_dossier_impl,
        )
        from med_autogrant.grant_quality import build_grant_quality_scorecard as build_scorecard_impl
        from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime

        runtime = MagDomainRuntime()
        starting_workspace = _load_json(REVISION_EXAMPLE_PATH)
        critique_workspace = _load_json(CRITIQUE_EXAMPLE_PATH)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch.object(runtime, "_load_workspace", return_value=starting_workspace), patch(
                "med_autogrant.domain_runtime_parts.authoring_surface.run_critique_revision_closed_loop",
                return_value={
                    "rounds": [
                        {
                            "round": 1,
                            "decision": "ready_for_submission",
                            "critique_workspace": critique_workspace,
                            "route": {"recommended_stage": "frozen", "reason": "ready"},
                        }
                    ],
                    "loop_status": "passed",
                    "termination_reason": "ready_for_submission",
                    "final_workspace": critique_workspace,
                    "final_route": {"recommended_stage": "frozen", "reason": "ready"},
                },
            ), patch(
                "med_autogrant.domain_runtime_parts.authoring_surface.build_grant_quality_scorecard",
                wraps=build_scorecard_impl,
            ) as build_scorecard, patch(
                "med_autogrant.domain_runtime_parts.authoring_surface.build_grant_quality_closure_dossier",
                wraps=build_closure_dossier_impl,
            ) as build_dossier:
                payload = runtime.execute_critique_revision_loop(
                    input_path="/tmp/input.json",
                    output_dir=tmp_dir,
                    max_rounds=2,
                )

        loop_report = payload["loop_report"]
        self.assertEqual(loop_report["grant_quality_scorecard"]["surface_kind"], "grant_quality_scorecard")
        self.assertEqual(
            loop_report["grant_quality_closure_dossier"]["surface_kind"],
            "grant_quality_closure_dossier",
        )
        build_scorecard.assert_called_once_with(critique_workspace)
        build_dossier.assert_called_once_with(critique_workspace)

    def test_execute_authoring_mainline_loop_report_embeds_quality_surfaces(self) -> None:
        from med_autogrant.grant_quality import (
            build_grant_quality_closure_dossier as build_closure_dossier_impl,
        )
        from med_autogrant.grant_quality import build_grant_quality_scorecard as build_scorecard_impl
        from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime

        runtime = MagDomainRuntime()
        workspace = _load_json(DRAFTING_EXAMPLE_PATH)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch.object(runtime, "_load_workspace", return_value=workspace), patch(
                "med_autogrant.domain_runtime_parts.authoring_surface.run_authoring_mainline_controller",
                return_value={
                    "cycles": [
                        {
                            "cycle": 1,
                            "decision": "ready_for_submission",
                            "input_workspace": workspace,
                            "route": {"recommended_stage": "frozen", "reason": "ready"},
                        }
                    ],
                    "loop_status": "passed",
                    "termination_reason": "ready_for_submission",
                    "final_workspace": workspace,
                    "final_route": {"recommended_stage": "frozen", "reason": "ready"},
                },
            ), patch(
                "med_autogrant.domain_runtime_parts.authoring_mainline.build_grant_quality_scorecard",
                wraps=build_scorecard_impl,
            ) as build_scorecard, patch(
                "med_autogrant.domain_runtime_parts.authoring_mainline.build_grant_quality_closure_dossier",
                wraps=build_closure_dossier_impl,
            ) as build_dossier:
                payload = runtime.execute_authoring_mainline_loop(
                    input_path="/tmp/input.json",
                    output_dir=tmp_dir,
                    max_cycles=3,
                )

        loop_report = payload["mainline_loop_report"]
        self.assertEqual(loop_report["grant_quality_scorecard"]["surface_kind"], "grant_quality_scorecard")
        self.assertEqual(
            loop_report["grant_quality_closure_dossier"]["surface_kind"],
            "grant_quality_closure_dossier",
        )
        build_scorecard.assert_called_once_with(workspace)
        build_dossier.assert_called_once_with(workspace)
