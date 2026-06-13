from __future__ import annotations

from med_autogrant.grant_autonomy_loop_parts import (
    GrantAutonomyLoopContext,
    append_tranche_history,
)


def test_loop_context_reports_keep_controller_and_quality_state() -> None:
    context = GrantAutonomyLoopContext(
        request_id="autonomy-loop-context-001",
        start_mode="workspace",
        goal={
            "target_status": "near_submission_candidate",
            "summary": "Reach a near submission candidate.",
        },
        max_rounds_or_cycles=2,
        budget_max=5,
        initial_blockers=["initial blocker"],
        initial_evidence_gaps=["initial evidence gap"],
        action_trace=[
            {
                "step_action": "quality_evaluator",
                "cycle": 1,
                "step_index": 1,
                "result": "executed",
            }
        ],
        reselection_decisions=[],
        rollback_decisions=[],
    )
    controller_plan = {
        "current_tranche": "quality_closure",
        "tranche_objective": "Close hard quality issues.",
        "tranche_success_gate": {
            "target_status": "near_submission_candidate",
            "requires_zero_blockers": True,
            "requires_zero_evidence_gaps": True,
        },
    }
    quality_dossier = {
        "surface_kind": "grant_quality_closure_dossier",
        "quality_summary": {
            "overall_status": "blocked",
            "overall_score": 55,
            "summary": "hard blocker remains",
        },
        "closure_packages": [],
    }
    active_closure_package = {
        "closure_id": "hard-blocker",
        "summary": "Hard blocker remains.",
        "action": "rollback_upstream",
        "target_stage": "question_refinement",
    }
    tranche_history = [
        {
            "cycle": 1,
            "gate_status": "blocked",
            "quality_status": "not_ready",
            "next_controller_action": "rollback_upstream",
            "decision_reason": "Hard blocker remains.",
            "termination_reason": "blockers_not_cleared",
        }
    ]

    failed = context.fail_closed_report(
        spent_steps=1,
        termination_reason="blockers_not_cleared",
        completed_cycles=1,
        workspace={"workspace_id": "ws-001"},
        latest_blocker_report={"overall_status": "blocked"},
        unresolved_blockers=["hard blocker"],
        evidence_gaps=["missing evidence"],
        controller_plan=controller_plan,
        tranche_history=tranche_history,
        latest_quality_closure_dossier=quality_dossier,
        closure_package_queue=[active_closure_package],
        active_closure_package=active_closure_package,
    )

    assert failed["controller_status"] == "failed_closed"
    assert failed["termination_reason"] == "blockers_not_cleared"
    assert failed["request_id"] == "autonomy-loop-context-001"
    assert failed["blocker_report"]["initial_blocker_queue"] == ["initial blocker"]
    assert failed["controller_plan"]["active_closure_package_id"] == "hard-blocker"
    assert failed["controller_plan"]["next_controller_action"] == "fail_closed"
    assert failed["authority_return"]["result_shape"] == "typed_blocker"

    success = context.success_report(
        spent_steps=2,
        controller_status="near_submission_candidate",
        termination_reason="goal_reached",
        completed_cycles=2,
        workspace={"workspace_id": "ws-001"},
        latest_blocker_report={"overall_status": "near_submission_candidate"},
        unresolved_blockers=[],
        evidence_gaps=[],
        controller_plan=controller_plan,
        tranche_history=[],
        latest_quality_closure_dossier=quality_dossier,
        closure_package_queue=[],
        active_closure_package=None,
    )

    assert success["controller_status"] == "near_submission_candidate"
    assert success["termination_reason"] == "goal_reached"
    assert success["authority_return"]["result_shape"] == "no_regression_evidence"
    assert success["budget"]["remaining_steps"] == 3


def test_append_tranche_history_projects_active_closure_package() -> None:
    tranche_history: list[dict[str, object]] = []

    append_tranche_history(
        tranche_history,
        cycle=3,
        controller_plan={
            "current_tranche": "quality_closure",
            "tranche_objective": "Close the active closure package.",
            "tranche_success_gate": {
                "target_status": "near_submission_candidate",
                "requires_zero_blockers": True,
                "requires_zero_evidence_gaps": False,
            },
        },
        quality_status="not_ready",
        unresolved_blockers=["hard blocker"],
        evidence_gaps=["secondary evidence gap"],
        next_controller_action="rollback_upstream",
        gate_status="blocked",
        decision_reason="Hard blocker remains.",
        termination_reason="blockers_not_cleared",
        latest_quality_closure_dossier={
            "quality_summary": {
                "overall_status": "blocked",
                "summary": "hard blocker remains",
            }
        },
        closure_package_queue=[
            {
                "closure_id": "hard-blocker",
                "action": "rollback_upstream",
                "target_stage": "question_refinement",
            }
        ],
        active_closure_package={
            "closure_id": "hard-blocker",
            "action": "rollback_upstream",
            "target_stage": "question_refinement",
        },
    )

    assert len(tranche_history) == 1
    entry = tranche_history[0]
    assert entry["cycle"] == 3
    assert entry["current_tranche"] == "quality_closure"
    assert entry["gate_status"] == "blocked"
    assert entry["next_controller_action"] == "rollback_upstream"
    assert entry["closure_package_queue_ids"] == ["hard-blocker"]
    assert entry["active_closure_package_id"] == "hard-blocker"
    assert entry["active_closure_package_action"] == "rollback_upstream"
    assert entry["active_closure_package_target_stage"] == "question_refinement"
