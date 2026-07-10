from __future__ import annotations

import pytest

from med_autogrant.grant_autonomy_controller import run_grant_autonomy_controller


REQUEST = {
    "request_id": "autonomy-req-001",
    "start": {
        "mode": "workspace",
        "workspace": {
            "grant_run_id": "grant-run-001",
            "workspace_id": "workspace-001",
            "draft_id": "draft-001",
            "lifecycle_stage": "critique",
            "program_id": "med-autogrant-mainline",
        },
    },
    "goal": {"target_status": "submission_grade_candidate"},
}


def test_missing_request_id_fails_closed_before_runtime_handoff() -> None:
    with pytest.raises(ValueError, match="request_id"):
        run_grant_autonomy_controller(request={"start": {}, "goal": {}})


def test_missing_opl_attempt_returns_lineaged_typed_blocker_and_identity() -> None:
    report = run_grant_autonomy_controller(request=REQUEST)
    blocker = report["authority_return"]["typed_blocker"]

    assert report["controller_status"] == "failed_closed"
    assert report["termination_reason"] == "opl_provider_attempt_required"
    assert report["workspace_identity"] == REQUEST["start"]["workspace"]
    assert blocker["blocker_family"] == "opl_provider_attempt_required"
    assert blocker["repeat_budget"]["mechanism_repair_after_repeat_count"] == 2
    assert blocker["next_forced_delta"] == "supply_valid_opl_stage_attempt_owner_chain"
    assert blocker["escalation_owner"] == "one-person-lab"


def test_valid_opl_attempt_routes_runtime_ownership_without_running_loop() -> None:
    report = run_grant_autonomy_controller(
        request=REQUEST,
        opl_stage_attempt={
            "runtime_owner": "one-person-lab",
            "executor_kind": "codex_cli",
            "stage_run_ref": "stage-run:mag/autonomy-req-001",
            "attempt_lease_ref": "lease:stage-run/mag/autonomy-req-001/owner-chain-default-caller",
            "caller_role": "opl_owner_chain_default_caller",
        },
    )
    blocker = report["authority_return"]["typed_blocker"]

    assert report["termination_reason"] == "opl_runtime_controller_required"
    assert report["completed_cycles"] == 0
    assert report["final_workspace"] == {}
    assert report["controller_execution_boundary"]["mag_runs_budget_cycle_rollback_or_resume"] is False
    assert blocker["next_forced_delta"] == "dispatch_request_through_opl_runtime_controller"
