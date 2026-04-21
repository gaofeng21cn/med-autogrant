from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable


RouteResolver = Callable[[dict[str, Any]], dict[str, Any]]
StageRunner = Callable[[dict[str, Any]], dict[str, Any]]

_PASS_RECOMMENDED_STAGES = {"ready_for_submission", "frozen"}
_ROLLBACK_STAGES = {
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
}


def run_authoring_mainline_controller(
    *,
    current_workspace: dict[str, Any],
    max_cycles: int,
    route_resolver: RouteResolver,
    stage_runners: dict[str, StageRunner],
) -> dict[str, Any]:
    if not isinstance(max_cycles, int) or max_cycles <= 0:
        raise ValueError("max_cycles 必须是正整数。")
    if not isinstance(stage_runners, dict):
        raise TypeError("stage_runners 必须是 stage -> runner 的映射。")

    workspace = deepcopy(current_workspace)
    cycles: list[dict[str, Any]] = []
    final_route: dict[str, Any] | None = None

    for cycle_index in range(1, max_cycles + 1):
        route = _require_mapping(route_resolver(workspace), scope="route_resolver output")
        final_route = route
        recommended_stage = str(route.get("recommended_stage") or "").strip()
        cycle_entry: dict[str, Any] = {
            "cycle": cycle_index,
            "route": route,
            "input_workspace": workspace,
        }

        if recommended_stage in _PASS_RECOMMENDED_STAGES:
            cycle_entry["decision"] = "ready_for_submission"
            cycles.append(cycle_entry)
            return {
                "cycles": cycles,
                "loop_status": "passed",
                "final_workspace": workspace,
                "final_route": route,
                "termination_reason": "ready_for_submission",
            }

        runner = stage_runners.get(recommended_stage)
        if runner is None:
            cycle_entry["decision"] = "fail_closed"
            cycles.append(cycle_entry)
            return {
                "cycles": cycles,
                "loop_status": "failed_closed",
                "final_workspace": workspace,
                "final_route": route,
                "termination_reason": "unknown_recommended_stage",
            }

        runner_output = _require_mapping(runner(workspace), scope=f"{recommended_stage}_runner output")
        rebuilt_workspace = _extract_workspace(
            runner_output,
            preferred_keys=("workspace", f"{recommended_stage}_workspace"),
            scope=f"{recommended_stage}_runner output",
        )

        cycle_entry["decision"] = "rollback_rebuild" if recommended_stage in _ROLLBACK_STAGES else "progressed"
        cycle_entry["output_workspace"] = rebuilt_workspace
        cycles.append(cycle_entry)
        workspace = rebuilt_workspace

    return {
        "cycles": cycles,
        "loop_status": "failed_closed",
        "final_workspace": workspace,
        "final_route": final_route or {},
        "termination_reason": "max_cycles_exhausted",
    }


def _require_mapping(value: Any, *, scope: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{scope} 必须返回 object。")
    return value


def _extract_workspace(
    payload: dict[str, Any],
    *,
    preferred_keys: tuple[str, ...],
    scope: str,
) -> dict[str, Any]:
    for key in preferred_keys:
        if key in payload:
            workspace = payload[key]
            if not isinstance(workspace, dict):
                raise TypeError(f"{scope}.{key} 必须是 object。")
            return workspace
    return payload
