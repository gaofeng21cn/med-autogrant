from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from med_autogrant.opl_execution_boundary import (
    build_stage_transition_authority_boundary,
    require_opl_default_stage_attempt,
)


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
    opl_stage_attempt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(max_cycles, int) or max_cycles <= 0:
        raise ValueError("max_cycles 必须是正整数。")
    if not isinstance(stage_runners, dict):
        raise TypeError("stage_runners 必须是 stage -> runner 的映射。")

    boundary = require_opl_default_stage_attempt(
        opl_stage_attempt,
        controller_id="authoring-mainline-loop",
    )
    if not boundary["ok"]:
        return _with_controller_receipt_boundary(
            {
            "cycles": [],
            "loop_status": "failed_closed",
            "final_workspace": deepcopy(current_workspace),
            "final_route": {},
            "termination_reason": "opl_provider_attempt_required",
            "typed_blocker": boundary["typed_blocker"],
            },
            controller_id="authoring-mainline-loop",
        )

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
            return _with_controller_receipt_boundary(
                {
                "cycles": cycles,
                "loop_status": "passed",
                "final_workspace": workspace,
                "final_route": route,
                "termination_reason": "ready_for_submission",
                },
                controller_id="authoring-mainline-loop",
            )

        runner = stage_runners.get(recommended_stage)
        if runner is None:
            cycle_entry["decision"] = "fail_closed"
            cycles.append(cycle_entry)
            return _with_controller_receipt_boundary(
                {
                "cycles": cycles,
                "loop_status": "failed_closed",
                "final_workspace": workspace,
                "final_route": route,
                "termination_reason": "unknown_recommended_stage",
                "typed_blocker": _build_controller_typed_blocker(
                    controller_id="authoring-mainline-loop",
                    reason="unknown_recommended_stage",
                ),
                },
                controller_id="authoring-mainline-loop",
            )

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

    return _with_controller_receipt_boundary(
        {
        "cycles": cycles,
        "loop_status": "failed_closed",
        "final_workspace": workspace,
        "final_route": final_route or {},
        "termination_reason": "max_cycles_exhausted",
        "typed_blocker": _build_controller_typed_blocker(
            controller_id="authoring-mainline-loop",
            reason="max_cycles_exhausted",
        ),
        },
        controller_id="authoring-mainline-loop",
    )


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


def _with_controller_receipt_boundary(payload: dict[str, Any], *, controller_id: str) -> dict[str, Any]:
    termination_reason = str(payload.get("termination_reason") or "unknown")
    result_shape = "no_regression_evidence" if termination_reason == "ready_for_submission" else "typed_blocker"
    refs = (
        {"no_regression_evidence_ref": f"no-regression:mag/{controller_id}/ready-for-submission"}
        if result_shape == "no_regression_evidence"
        else {"typed_blocker_ref": f"typed-blocker:mag/{controller_id}/{termination_reason}"}
    )
    final_route = payload.get("final_route")
    final_recommended_stage = (
        str(final_route.get("recommended_stage") or "").strip()
        if isinstance(final_route, dict)
        else ""
    )
    return {
        "surface_kind": "mag_domain_controller_receipt",
        **payload,
        "loop_status_role": "mag_domain_controller_result_not_opl_stage_terminal",
        "stage_transition_authority": "one-person-lab",
        "authority_boundary": build_stage_transition_authority_boundary(
            surface_id=f"mag.{controller_id}",
            mag_role="bounded_domain_controller_receipt_only",
        ),
        "stage_transition_intent": {
            "surface_kind": "mag_stage_transition_intent_recommendation",
            "intent_kind": "domain_controller_closeout_recommendation",
            "target_stage": final_recommended_stage or None,
            "requires_opl_stage_transition_authority": True,
            "return_shape": result_shape,
        },
        "authority_return": {
            "surface_kind": "mag_stage_authority_return",
            "result_shape": result_shape,
            "allowed_return_shapes": [
                "domain_owner_receipt",
                "typed_blocker",
                "no_regression_evidence",
            ],
            "refs": refs,
            "requires_opl_stage_transition_authority": True,
            "body_policy": "refs_only_no_stage_current_or_terminal_write",
        },
    }


def _build_controller_typed_blocker(*, controller_id: str, reason: str) -> dict[str, Any]:
    return {
        "surface_kind": "mag_domain_controller_typed_blocker",
        "controller_id": controller_id,
        "blocker_kind": reason,
        "typed_blocker_ref": f"typed-blocker:mag/{controller_id}/{reason}",
        "stage_transition_authority": "one-person-lab",
        "mag_writes_stage_current_pointer": False,
        "mag_writes_stage_terminal_state": False,
    }
