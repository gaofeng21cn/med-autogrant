from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.opl_execution_boundary import require_opl_default_stage_attempt


def run_grant_autonomy_controller(
    *,
    request: Mapping[str, Any],
    opl_stage_attempt: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    request_id = _required_string(request, "request_id")
    start = request.get("start")
    start_mode = str(start.get("mode", "unknown")) if isinstance(start, Mapping) else "unknown"
    goal = dict(request.get("goal")) if isinstance(request.get("goal"), Mapping) else {}
    requested_attempt = opl_stage_attempt or (
        request.get("opl_stage_attempt")
        if isinstance(request.get("opl_stage_attempt"), Mapping)
        else None
    )
    boundary = require_opl_default_stage_attempt(
        dict(requested_attempt) if requested_attempt is not None else None,
        controller_id="autonomy-controller",
    )
    if boundary["ok"]:
        termination_reason = "opl_runtime_controller_required"
        typed_blocker_ref = "typed-blocker:mag/autonomy-controller/opl-runtime-controller-required"
    else:
        termination_reason = "opl_provider_attempt_required"
        typed_blocker_ref = boundary["typed_blocker"]["typed_blocker_ref"]
    return {
        "surface_kind": "grant_autonomy_controller_report",
        "controller_version": 4,
        "request_id": request_id,
        "controller_status": "failed_closed",
        "termination_reason": termination_reason,
        "started_from_mode": start_mode,
        "goal": goal,
        "completed_cycles": 0,
        "unresolved_blockers": [typed_blocker_ref],
        "evidence_gaps": [],
        "final_workspace": {},
        "controller_execution_boundary": {
            "surface_kind": "mag_autonomy_controller_execution_boundary",
            "execution_scope": "thin_direct_handler_no_scheduler",
            "mag_role": "grant_authority_target_and_typed_blocker_emitter",
            "post_start_residency_owner": "one-person-lab",
            "attempt_ledger_owner": "one-person-lab",
            "stage_transition_authority": "one-person-lab",
            "mag_long_running_driver": False,
            "mag_scheduler_daemon_owner": False,
            "mag_owns_attempt_ledger": False,
            "mag_runs_budget_cycle_rollback_or_resume": False,
        },
        "authority_return": {
            "surface_kind": "mag_autonomy_controller_authority_return",
            "result_shape": "typed_blocker",
            "refs": {"typed_blocker_ref": typed_blocker_ref},
            "body_policy": "refs_only_no_runtime_or_grant_body",
        },
    }


def _required_string(payload: Mapping[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"grant autonomy request requires non-empty {field}")
    return value.strip()
