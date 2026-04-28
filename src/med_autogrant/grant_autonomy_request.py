from __future__ import annotations

from copy import deepcopy
from typing import Any

from med_autogrant.grant_autonomy_parts import _fail_closed_report, _normalized_string, _string_list


def validate_grant_autonomy_request(request: Any) -> dict[str, Any]:
    shape = _extract_request_shape(request)
    if not shape["ok"]:
        return shape

    limits = _validate_goal_and_limits(shape)
    if not limits["ok"]:
        return limits

    runtime_inputs = _validate_runtime_inputs(request, shape, limits)
    if not runtime_inputs["ok"]:
        return runtime_inputs

    return {
        "ok": True,
        **{key: shape[key] for key in ("request_id", "start", "start_mode", "goal", "goal_target")},
        "max_rounds_or_cycles": limits["max_rounds_or_cycles"],
        "budget_max": limits["budget_max"],
        "require_zero_blockers": runtime_inputs["require_zero_blockers"],
        "require_zero_evidence_gaps": runtime_inputs["require_zero_evidence_gaps"],
        "controller_plan_input": request.get("controller_plan"),
        "initial_blockers": runtime_inputs["initial_blockers"],
        "initial_evidence_gaps": runtime_inputs["initial_evidence_gaps"],
        "reselection_enabled": runtime_inputs["reselection_enabled"],
        "rollback_enabled": runtime_inputs["rollback_enabled"],
        "max_reselections": runtime_inputs["max_reselections"],
        "max_rollbacks": runtime_inputs["max_rollbacks"],
    }


def _extract_request_shape(request: Any) -> dict[str, Any]:
    if not isinstance(request, dict):
        return _failure(
            request_id="",
            started_from_mode="unknown",
            goal={},
            max_rounds_or_cycles=0,
            budget_max=0,
            termination_reason="invalid_request_object",
        )

    request_id = _normalized_string(request.get("request_id"))
    start = request.get("start")
    goal = request.get("goal")
    budget = request.get("budget")
    if not isinstance(start, dict) or not isinstance(goal, dict) or not isinstance(budget, dict):
        return _failure(
            request_id=request_id,
            started_from_mode="unknown",
            goal=deepcopy(goal) if isinstance(goal, dict) else {},
            max_rounds_or_cycles=0,
            budget_max=0,
            termination_reason="missing_required_input",
        )

    start_mode = _normalized_string(start.get("mode"))
    return {
        "ok": True,
        "request": request,
        "request_id": request_id,
        "start": start,
        "start_mode": start_mode,
        "goal": goal,
        "goal_target": _normalized_string(goal.get("target_status")),
        "budget": budget,
    }


def _validate_goal_and_limits(shape: dict[str, Any]) -> dict[str, Any]:
    goal = shape["goal"]
    request = shape["request"]
    start_mode = shape["start_mode"] or "unknown"
    if shape["goal_target"] not in {"submission_grade_candidate", "near_submission_candidate"}:
        return _failure(
            request_id=shape["request_id"],
            started_from_mode=start_mode,
            goal=deepcopy(goal),
            max_rounds_or_cycles=0,
            budget_max=0,
            termination_reason="invalid_goal_target",
        )

    max_rounds_or_cycles = request.get("max_rounds_or_cycles")
    if not isinstance(max_rounds_or_cycles, int) or max_rounds_or_cycles <= 0:
        return _failure(
            request_id=shape["request_id"],
            started_from_mode=start_mode,
            goal=deepcopy(goal),
            max_rounds_or_cycles=0,
            budget_max=0,
            termination_reason="invalid_max_rounds_or_cycles",
        )

    budget_max = shape["budget"].get("max_total_steps")
    if not isinstance(budget_max, int) or budget_max <= 0:
        return _failure(
            request_id=shape["request_id"],
            started_from_mode=start_mode,
            goal=deepcopy(goal),
            max_rounds_or_cycles=max_rounds_or_cycles,
            budget_max=0,
            termination_reason="invalid_budget",
        )
    return {"ok": True, "max_rounds_or_cycles": max_rounds_or_cycles, "budget_max": budget_max}


def _validate_runtime_inputs(
    request: dict[str, Any],
    shape: dict[str, Any],
    limits: dict[str, Any],
) -> dict[str, Any]:
    stop_conditions = request.get("stop_conditions")
    if not isinstance(stop_conditions, dict):
        return _runtime_failure(shape, limits, blocker_queue=[], evidence_gap_queue=[])

    initial_blockers = _string_list(request.get("blocker_queue"))
    initial_evidence_gaps = _string_list(request.get("evidence_gap_queue"))
    if initial_blockers is None or initial_evidence_gaps is None:
        return _runtime_failure(shape, limits, blocker_queue=[], evidence_gap_queue=[])

    reselection_policy = request.get("reselection_policy")
    rollback_policy = request.get("rollback_policy")
    if not isinstance(reselection_policy, dict) or not isinstance(rollback_policy, dict):
        return _runtime_failure(
            shape,
            limits,
            blocker_queue=initial_blockers,
            evidence_gap_queue=initial_evidence_gaps,
        )

    return {
        "ok": True,
        "require_zero_blockers": bool(stop_conditions.get("require_zero_blockers", True)),
        "require_zero_evidence_gaps": bool(stop_conditions.get("require_zero_evidence_gaps", True)),
        "initial_blockers": initial_blockers,
        "initial_evidence_gaps": initial_evidence_gaps,
        "reselection_enabled": bool(reselection_policy.get("enabled", False)),
        "rollback_enabled": bool(rollback_policy.get("enabled", False)),
        "max_reselections": _nonnegative_int(reselection_policy.get("max_reselections", 0)),
        "max_rollbacks": _nonnegative_int(rollback_policy.get("max_rollbacks", 0)),
    }


def _runtime_failure(
    shape: dict[str, Any],
    limits: dict[str, Any],
    *,
    blocker_queue: list[str],
    evidence_gap_queue: list[str],
) -> dict[str, Any]:
    return _failure(
        request_id=shape["request_id"],
        started_from_mode=shape["start_mode"] or "unknown",
        goal=deepcopy(shape["goal"]),
        max_rounds_or_cycles=limits["max_rounds_or_cycles"],
        budget_max=limits["budget_max"],
        termination_reason="missing_required_input",
        blocker_queue=blocker_queue,
        evidence_gap_queue=evidence_gap_queue,
    )


def _failure(
    *,
    request_id: str,
    started_from_mode: str,
    goal: dict[str, Any],
    max_rounds_or_cycles: int,
    budget_max: int,
    termination_reason: str,
    blocker_queue: list[str] | None = None,
    evidence_gap_queue: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "report": _fail_closed_report(
            request_id=request_id,
            started_from_mode=started_from_mode,
            goal=goal,
            max_rounds_or_cycles=max_rounds_or_cycles,
            budget_max=budget_max,
            spent_steps=0,
            termination_reason=termination_reason,
            blocker_queue=list(blocker_queue or []),
            evidence_gap_queue=list(evidence_gap_queue or []),
        ),
    }


def _nonnegative_int(value: Any) -> int:
    if not isinstance(value, int) or value < 0:
        return 0
    return value
