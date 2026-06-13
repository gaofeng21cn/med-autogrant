from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.grant_autonomy_controller_plan import _normalize_controller_plan  # noqa: E402
from med_autogrant.grant_autonomy_loop_shell import run_grant_autonomy_loop  # noqa: E402


def _quality_result(
    *,
    workspace_id: str,
    lifecycle_stage: str,
    quality_status: str = "near_submission_candidate",
) -> dict[str, Any]:
    return {
        "quality_status": quality_status,
        "blocker_report": {
            "surface_kind": "grant_quality_scorecard",
            "overall_status": quality_status,
            "overall_score": 78,
        },
        "unresolved_blockers": [],
        "evidence_gaps": [],
        "evidence_supply_queue": [],
        "quality_closure_dossier": {
            "surface_kind": "grant_quality_closure_dossier",
            "dossier_version": 1,
            "workspace_surface_kind": "nsfc_workspace",
            "grant_run_id": "grant-loop-shell",
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
            "draft_id": "draft-loop-shell",
            "quality_summary": {
                "overall_status": quality_status,
                "overall_score": 78,
                "summary": f"quality:{quality_status}",
                "loop_gate": {
                    "action": "continue",
                    "recommended_stage": None,
                    "reason": f"quality:{quality_status}",
                },
            },
            "unclosed_hard_issues": [],
            "evidence_supply_queue_summary": {
                "total_gap_count": 0,
                "outstanding_gap_ids": [],
                "status_counts": [],
                "kind_counts": [],
            },
            "closure_packages": [],
        },
    }


def _unexpected_callback(name: str) -> Any:
    def fail(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        raise AssertionError(f"{name} should not run when the quality goal is already met")

    return fail


def test_loop_shell_can_finish_workspace_start_when_quality_goal_is_met() -> None:
    goal = {
        "target_status": "near_submission_candidate",
        "summary": "先达到 near submission",
    }
    result = run_grant_autonomy_loop(
        request_id="autonomy-req-loop-shell",
        start_mode="workspace",
        goal=goal,
        goal_target="near_submission_candidate",
        max_rounds_or_cycles=1,
        budget_max=4,
        spent_steps=0,
        initial_blockers=[],
        initial_evidence_gaps=[],
        action_trace=[],
        reselection_decisions=[],
        rollback_decisions=[],
        tranche_history=[],
        completed_cycles=0,
        latest_blocker_report={},
        unresolved_blockers=[],
        evidence_gaps=[],
        latest_quality_closure_dossier=None,
        closure_package_queue=[],
        active_closure_package=None,
        controller_plan=_normalize_controller_plan(
            None,
            goal=goal,
            require_zero_blockers=True,
            require_zero_evidence_gaps=True,
        ),
        selection_input=None,
        workspace={"workspace_id": "ws-loop-shell", "lifecycle_stage": "critique"},
        explicit_controller_plan=False,
        reselection_enabled=False,
        rollback_enabled=False,
        max_reselections=0,
        max_rollbacks=0,
        reselection_count=0,
        rollback_count=0,
        selector=_unexpected_callback("selector"),
        initializer=_unexpected_callback("initializer"),
        mainline_runner=_unexpected_callback("mainline_runner"),
        quality_evaluator=lambda workspace: _quality_result(
            workspace_id=str(workspace["workspace_id"]),
            lifecycle_stage=str(workspace["lifecycle_stage"]),
        ),
    )

    assert result["controller_status"] == "near_submission_candidate"
    assert result["termination_reason"] == "goal_reached"
    assert result["completed_cycles"] == 1
    assert result["action_trace"][0]["step_action"] == "quality_evaluator"
    assert result["tranche_history"][0]["gate_status"] == "passed"
    assert result["authority_return"]["result_shape"] == "no_regression_evidence"
