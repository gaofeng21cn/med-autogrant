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
from med_autogrant.grant_family_registry import (  # noqa: E402
    get_project_profile_preset,
    list_family_profile_placeholders,
)
from med_autogrant.grant_governance_adapter import (  # noqa: E402
    apply_family_governance_to_controller_plan,
    build_family_governance_surface,
    prioritize_closure_package_queue,
)
from med_autogrant.project_profile_selector import _build_grant_family_grammar  # noqa: E402

OPL_STAGE_ATTEMPT = {
    "runtime_owner": "one-person-lab",
    "executor_kind": "codex_cli",
    "attempt_lease_ref": "lease:opl/stage-attempt/test",
}


class GrantGovernanceAdapterTest(unittest.TestCase):
    def _workspace_for_preset(self, preset_id: str) -> dict[str, Any]:
        preset = get_project_profile_preset(preset_id)
        return {
            "workspace_id": f"ws-{preset_id}",
            "lifecycle_stage": "critique",
            "project_profile": {
                "grant_family_grammar": _build_grant_family_grammar(preset),
            },
        }

    def _closure_package(
        self,
        *,
        closure_id: str,
        summary: str,
        action: str,
        target_stage: str | None,
        severity: str = "hard",
    ) -> dict[str, Any]:
        return {
            "closure_id": closure_id,
            "summary": summary,
            "severity": severity,
            "target_stage": target_stage,
            "action": action,
            "required_input_ids": [],
            "evidence_refs": [],
            "linked_issue_ids": [closure_id],
            "blocking_reasons": [summary],
            "evidence_obligations": [],
            "acceptance_signals": [
                {
                    "signal_id": f"signal:{closure_id}",
                    "signal_kind": "controller_action",
                    "summary": summary,
                    "source_surface": "grant_quality",
                    "required_input_ids": [],
                    "evidence_refs": [],
                }
            ],
        }

    def _quality_result(
        self,
        *,
        workspace: dict[str, Any],
        quality_status: str,
        closure_packages: list[dict[str, Any]],
    ) -> dict[str, Any]:
        overall_status = quality_status if quality_status != "not_ready" else "blocked"
        overall_score = 78 if quality_status == "near_submission_candidate" else 55
        return {
            "quality_status": quality_status,
            "blocker_report": {
                "surface_kind": "grant_quality_scorecard",
                "overall_status": overall_status,
                "overall_score": overall_score,
            },
            "unresolved_blockers": [item["summary"] for item in closure_packages if item["severity"] == "hard"],
            "evidence_gaps": [],
            "evidence_supply_queue": [],
            "quality_closure_dossier": {
                "surface_kind": "grant_quality_closure_dossier",
                "dossier_version": 1,
                "workspace_surface_kind": "nsfc_workspace",
                "grant_run_id": "grant-001",
                "workspace_id": workspace["workspace_id"],
                "lifecycle_stage": workspace["lifecycle_stage"],
                "draft_id": None,
                "quality_summary": {
                    "overall_status": overall_status,
                    "overall_score": overall_score,
                    "summary": f"quality:{overall_status}",
                    "loop_gate": {
                        "action": "continue" if quality_status != "not_ready" else "rollback_required",
                        "recommended_stage": None,
                        "reason": "governance adapter test",
                    },
                },
                "unclosed_hard_issues": [item["summary"] for item in closure_packages if item["severity"] == "hard"],
                "evidence_supply_queue_summary": {
                    "total_gap_count": 0,
                    "outstanding_gap_ids": [],
                    "status_counts": [],
                    "kind_counts": [],
                },
                "closure_packages": closure_packages,
            },
        }

    def test_build_family_governance_surface_exposes_family_defaults(self) -> None:
        workspace = self._workspace_for_preset("nih_r21_translational_v1")

        surface = build_family_governance_surface(workspace)

        self.assertEqual(surface["surface_kind"], "grant_family_governance_surface")
        self.assertEqual(surface["family_id"], "nih_r21_translational_family_v1")
        self.assertEqual(surface["preferred_stop_target"], "ready_for_submission_after_significance_innovation_lock")
        self.assertEqual(surface["preferred_rollback_stage"], "fit_alignment")
        self.assertEqual(surface["controller_defaults"]["target_status"], "near_submission_candidate")

    def test_build_family_governance_surface_accepts_placeholder_family(self) -> None:
        placeholder = list_family_profile_placeholders()[0]
        workspace = {
            "workspace_id": "ws-placeholder",
            "lifecycle_stage": "input_intake",
            "project_profile": {
                "grant_family_grammar": {
                    "family_id": placeholder["family_id"],
                    "family_label": placeholder["family_label"],
                    "funder": placeholder["funder"],
                    "admission_status": placeholder["status"],
                    "governance_policy": placeholder["common_grant_grammar"]["governance_policy"],
                    "governance_entry_points": ["execute-grant-autonomy-controller"],
                }
            },
        }

        surface = build_family_governance_surface(workspace)

        self.assertEqual(surface["family_id"], "wellcome_discovery_placeholder_v1")
        self.assertEqual(surface["admission_status"], "placeholder")
        self.assertEqual(surface["preferred_rollback_stage"], "question_refinement")

    def test_apply_family_governance_to_controller_plan_hydrates_defaults(self) -> None:
        workspace = self._workspace_for_preset("wellcome_discovery_v1")
        controller_plan = {
            "current_tranche": "submission_readiness",
            "tranche_objective": "advance_to_submission_grade_candidate",
            "tranche_success_gate": {
                "target_status": "submission_grade_candidate",
                "requires_zero_blockers": True,
                "requires_zero_evidence_gaps": True,
            },
        }

        hydrated = apply_family_governance_to_controller_plan(
            controller_plan,
            workspace=workspace,
            explicit_controller_plan=False,
        )

        self.assertEqual(hydrated["current_tranche"], "discovery_framing_first")
        self.assertEqual(hydrated["tranche_success_gate"]["target_status"], "near_submission_candidate")
        self.assertFalse(hydrated["tranche_success_gate"]["requires_zero_evidence_gaps"])

    def test_prioritize_closure_package_queue_prefers_family_rollback_stage(self) -> None:
        nih_workspace = self._workspace_for_preset("nih_r21_translational_v1")
        wellcome_workspace = self._workspace_for_preset("wellcome_discovery_v1")
        packages = [
            self._closure_package(
                closure_id="pkg-question",
                summary="需要回到问题定义",
                action="rollback_upstream",
                target_stage="question_refinement",
            ),
            self._closure_package(
                closure_id="pkg-fit",
                summary="需要回到 fit alignment",
                action="rollback_upstream",
                target_stage="fit_alignment",
            ),
        ]

        nih_ranked = prioritize_closure_package_queue(packages, workspace=nih_workspace)
        wellcome_ranked = prioritize_closure_package_queue(packages, workspace=wellcome_workspace)

        self.assertEqual(nih_ranked[0]["closure_id"], "pkg-fit")
        self.assertEqual(wellcome_ranked[0]["closure_id"], "pkg-question")

    def test_controller_uses_family_adapter_for_active_closure_package(self) -> None:
        workspace = self._workspace_for_preset("nih_r21_translational_v1")
        packages = [
            self._closure_package(
                closure_id="pkg-question",
                summary="需要回到问题定义",
                action="rollback_upstream",
                target_stage="question_refinement",
            ),
            self._closure_package(
                closure_id="pkg-fit",
                summary="需要回到 fit alignment",
                action="rollback_upstream",
                target_stage="fit_alignment",
            ),
        ]
        request = {
            "request_id": "adapter-controller-001",
            "opl_stage_attempt": dict(OPL_STAGE_ATTEMPT),
            "start": {"mode": "workspace", "workspace": workspace},
            "goal": {
                "target_status": "near_submission_candidate",
                "summary": "adapter should reprioritize active closure package",
            },
            "max_rounds_or_cycles": 1,
            "budget": {"max_total_steps": 4},
            "stop_conditions": {
                "require_zero_blockers": True,
                "require_zero_evidence_gaps": False,
            },
            "blocker_queue": [],
            "evidence_gap_queue": [],
            "reselection_policy": {"enabled": False, "max_reselections": 0},
            "rollback_policy": {"enabled": True, "max_rollbacks": 1},
        }

        result = run_grant_autonomy_controller(
            request=request,
            selector=lambda selection_input: selection_input,
            initializer=lambda selection_input, selection: {"workspace": workspace},
            mainline_runner=lambda _payload: (_ for _ in ()).throw(AssertionError("max=1 should not run mainline")),
            quality_evaluator=lambda _workspace: self._quality_result(
                workspace=workspace,
                quality_status="not_ready",
                closure_packages=packages,
            ),
        )

        self.assertEqual(result["active_closure_package"]["closure_id"], "pkg-fit")
        self.assertEqual(result["controller_plan"]["active_closure_package_target_stage"], "fit_alignment")


if __name__ == "__main__":
    unittest.main()
