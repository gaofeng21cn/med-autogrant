from __future__ import annotations

import json
from pathlib import Path

from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime


def test_runtime_autonomy_adapter_writes_failed_closed_report(tmp_path: Path) -> None:
    request = {
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
    request_path = tmp_path / "autonomy-request.json"
    output_dir = tmp_path / "autonomy-output"
    request_path.write_text(json.dumps(request), encoding="utf-8")

    payload = MagDomainRuntime().execute_grant_autonomy_controller(
        input_path=request_path,
        output_dir=output_dir,
        opl_stage_attempt={
            "runtime_owner": "one-person-lab",
            "executor_kind": "codex_cli",
            "stage_run_ref": "stage-run:mag/autonomy-req-001",
            "attempt_lease_ref": "lease:stage-run/mag/autonomy-req-001/owner-chain-default-caller",
            "caller_role": "opl_owner_chain_default_caller",
        },
    )

    report = payload["grant_autonomy_controller_report"]
    report_path = Path(payload["grant_autonomy_controller_report_path"])
    assert payload["ok"] is True
    assert payload["workspace_id"] == "workspace-001"
    assert payload["final_workspace_path"] is None
    assert report["controller_version"] == 4
    assert report["controller_status"] == "failed_closed"
    assert report["termination_reason"] == "opl_runtime_controller_required"
    assert report["workspace_identity"] == request["start"]["workspace"]
    assert report["controller_execution_boundary"]["mag_runs_budget_cycle_rollback_or_resume"] is False
    authority_return = report["authority_return"]
    typed_blocker = authority_return["typed_blocker"]
    assert authority_return["result_shape"] == "typed_blocker"
    assert typed_blocker["typed_blocker_ref"] == authority_return["refs"]["typed_blocker_ref"]
    assert typed_blocker["blocker_family"] == "opl_runtime_controller_required"
    assert typed_blocker["next_forced_delta"] == "dispatch_request_through_opl_runtime_controller"
    assert typed_blocker["escalation_owner"] == "one-person-lab"
    assert json.loads(report_path.read_text(encoding="utf-8")) == report
