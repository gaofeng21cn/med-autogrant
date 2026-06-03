from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from med_autogrant.opl_execution_boundary import require_opl_default_stage_attempt


CritiqueRunner = Callable[[dict[str, Any]], dict[str, Any]]
RevisionRunner = Callable[[dict[str, Any]], dict[str, Any]]
RouteResolver = Callable[[dict[str, Any]], dict[str, Any]]

_PASS_RECOMMENDED_STAGE = "frozen"
_REVISION_RECOMMENDED_STAGE = "revision"
_ROLLBACK_RECOMMENDED_STAGES = {
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
}


def run_critique_revision_closed_loop(
    *,
    current_document: dict[str, Any],
    max_rounds: int,
    critique_runner: CritiqueRunner,
    revision_runner: RevisionRunner,
    route_resolver: RouteResolver,
    opl_stage_attempt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not isinstance(max_rounds, int) or max_rounds <= 0:
        raise ValueError("max_rounds 必须是正整数。")

    boundary = require_opl_default_stage_attempt(
        opl_stage_attempt,
        controller_id="critique-loop",
    )
    if not boundary["ok"]:
        return {
            "rounds": [],
            "loop_status": "failed_closed",
            "final_workspace": deepcopy(current_document),
            "final_route": {},
            "termination_reason": "opl_provider_attempt_required",
            "typed_blocker": boundary["typed_blocker"],
        }

    workspace = deepcopy(current_document)
    rounds: list[dict[str, Any]] = []
    final_route: dict[str, Any] | None = None

    for round_index in range(1, max_rounds + 1):
        critique_output = _require_mapping(critique_runner(workspace), scope="critique_runner output")
        critique_workspace = _extract_workspace(
            critique_output,
            preferred_key="critique_workspace",
            scope="critique_runner output",
        )

        route = _require_mapping(route_resolver(critique_workspace), scope="route_resolver output")
        recommended_stage = str(route.get("recommended_stage") or "").strip()
        final_route = route

        round_entry: dict[str, Any] = {
            "round": round_index,
            "critique_workspace": critique_workspace,
            "route": route,
        }

        if _is_rollback_route(route=route, recommended_stage=recommended_stage):
            round_entry["decision"] = "rollback_required"
            rounds.append(round_entry)
            return {
                "rounds": rounds,
                "loop_status": "rollback_required",
                "final_workspace": critique_workspace,
                "final_route": route,
                "termination_reason": _resolve_rollback_reason(route=route, recommended_stage=recommended_stage),
            }

        if recommended_stage == _PASS_RECOMMENDED_STAGE:
            round_entry["decision"] = "ready_for_submission"
            rounds.append(round_entry)
            return {
                "rounds": rounds,
                "loop_status": "passed",
                "final_workspace": critique_workspace,
                "final_route": route,
                "termination_reason": "ready_for_submission",
            }

        if recommended_stage != _REVISION_RECOMMENDED_STAGE:
            round_entry["decision"] = "rollback_required"
            rounds.append(round_entry)
            return {
                "rounds": rounds,
                "loop_status": "rollback_required",
                "final_workspace": critique_workspace,
                "final_route": route,
                "termination_reason": "unsupported_route",
            }

        revision_output = _require_mapping(revision_runner(critique_workspace), scope="revision_runner output")
        revised_workspace = _extract_workspace(
            revision_output,
            preferred_key="revised_workspace",
            scope="revision_runner output",
        )
        round_entry["decision"] = "revision_required"
        round_entry["revision_workspace"] = revised_workspace
        rounds.append(round_entry)
        workspace = revised_workspace

    return {
        "rounds": rounds,
        "loop_status": "failed_closed",
        "final_workspace": workspace,
        "final_route": final_route or {},
        "termination_reason": "max_rounds_exhausted",
    }


def _require_mapping(value: Any, *, scope: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{scope} 必须返回 object。")
    return value


def _extract_workspace(payload: dict[str, Any], *, preferred_key: str, scope: str) -> dict[str, Any]:
    workspace = payload.get(preferred_key, payload)
    if not isinstance(workspace, dict):
        raise TypeError(f"{scope}.{preferred_key} 必须是 object。")
    return workspace


def _is_rollback_route(*, route: dict[str, Any], recommended_stage: str) -> bool:
    if route.get("forced_rollback_stage"):
        return True
    return recommended_stage in _ROLLBACK_RECOMMENDED_STAGES


def _resolve_rollback_reason(*, route: dict[str, Any], recommended_stage: str) -> str:
    if route.get("forced_rollback_stage"):
        return "forced_rollback"
    if recommended_stage in {"direction_screening", "question_refinement"}:
        return "major_reframe"
    return "rollback_required"
