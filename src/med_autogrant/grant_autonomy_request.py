from __future__ import annotations

from copy import deepcopy
from typing import Any

from med_autogrant.grant_autonomy_parts import _fail_closed_report, _normalized_string, _string_list


def validate_grant_autonomy_request(request: Any) -> dict[str, Any]:
    if not isinstance(request, dict):
        return {
            "ok": False,
            "report": _fail_closed_report(
                request_id="",
                started_from_mode="unknown",
                goal={},
                max_rounds_or_cycles=0,
                budget_max=0,
                spent_steps=0,
                termination_reason="invalid_request_object",
                blocker_queue=[],
                evidence_gap_queue=[],
            ),
        }

    request_id = _normalized_string(request.get("request_id"))
    start = request.get("start")
    goal = request.get("goal")
    max_rounds_or_cycles = request.get("max_rounds_or_cycles")
    budget = request.get("budget")

    if not isinstance(start, dict) or not isinstance(goal, dict) or not isinstance(budget, dict):
        return {
            "ok": False,
            "report": _fail_closed_report(
                request_id=request_id,
                started_from_mode="unknown",
                goal=deepcopy(goal) if isinstance(goal, dict) else {},
                max_rounds_or_cycles=0,
                budget_max=0,
                spent_steps=0,
                termination_reason="missing_required_input",
                blocker_queue=[],
                evidence_gap_queue=[],
            ),
        }

    start_mode = _normalized_string(start.get("mode"))
    goal_target = _normalized_string(goal.get("target_status"))
    if goal_target not in {"submission_grade_candidate", "near_submission_candidate"}:
        return {
            "ok": False,
            "report": _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode or "unknown",
                goal=deepcopy(goal),
                max_rounds_or_cycles=0,
                budget_max=0,
                spent_steps=0,
                termination_reason="invalid_goal_target",
                blocker_queue=[],
                evidence_gap_queue=[],
            ),
        }
    if not isinstance(max_rounds_or_cycles, int) or max_rounds_or_cycles <= 0:
        return {
            "ok": False,
            "report": _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode or "unknown",
                goal=deepcopy(goal),
                max_rounds_or_cycles=0,
                budget_max=0,
                spent_steps=0,
                termination_reason="invalid_max_rounds_or_cycles",
                blocker_queue=[],
                evidence_gap_queue=[],
            ),
        }

    budget_max = budget.get("max_total_steps")
    if not isinstance(budget_max, int) or budget_max <= 0:
        return {
            "ok": False,
            "report": _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode or "unknown",
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=0,
                spent_steps=0,
                termination_reason="invalid_budget",
                blocker_queue=[],
                evidence_gap_queue=[],
            ),
        }

    stop_conditions = request.get("stop_conditions")
    if not isinstance(stop_conditions, dict):
        return {
            "ok": False,
            "report": _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode or "unknown",
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=0,
                termination_reason="missing_required_input",
                blocker_queue=[],
                evidence_gap_queue=[],
            ),
        }

    initial_blockers = _string_list(request.get("blocker_queue"))
    initial_evidence_gaps = _string_list(request.get("evidence_gap_queue"))
    if initial_blockers is None or initial_evidence_gaps is None:
        return {
            "ok": False,
            "report": _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode or "unknown",
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=0,
                termination_reason="missing_required_input",
                blocker_queue=[],
                evidence_gap_queue=[],
            ),
        }

    reselection_policy = request.get("reselection_policy")
    rollback_policy = request.get("rollback_policy")
    if not isinstance(reselection_policy, dict) or not isinstance(rollback_policy, dict):
        return {
            "ok": False,
            "report": _fail_closed_report(
                request_id=request_id,
                started_from_mode=start_mode or "unknown",
                goal=deepcopy(goal),
                max_rounds_or_cycles=max_rounds_or_cycles,
                budget_max=budget_max,
                spent_steps=0,
                termination_reason="missing_required_input",
                blocker_queue=initial_blockers,
                evidence_gap_queue=initial_evidence_gaps,
            ),
        }

    max_reselections = reselection_policy.get("max_reselections", 0)
    max_rollbacks = rollback_policy.get("max_rollbacks", 0)
    if not isinstance(max_reselections, int) or max_reselections < 0:
        max_reselections = 0
    if not isinstance(max_rollbacks, int) or max_rollbacks < 0:
        max_rollbacks = 0

    return {
        "ok": True,
        "request_id": request_id,
        "start": start,
        "start_mode": start_mode,
        "goal": goal,
        "goal_target": goal_target,
        "max_rounds_or_cycles": max_rounds_or_cycles,
        "budget_max": budget_max,
        "require_zero_blockers": bool(stop_conditions.get("require_zero_blockers", True)),
        "require_zero_evidence_gaps": bool(stop_conditions.get("require_zero_evidence_gaps", True)),
        "controller_plan_input": request.get("controller_plan"),
        "initial_blockers": initial_blockers,
        "initial_evidence_gaps": initial_evidence_gaps,
        "reselection_enabled": bool(reselection_policy.get("enabled", False)),
        "rollback_enabled": bool(rollback_policy.get("enabled", False)),
        "max_reselections": max_reselections,
        "max_rollbacks": max_rollbacks,
    }
