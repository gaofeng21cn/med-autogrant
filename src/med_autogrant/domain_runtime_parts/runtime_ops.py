from __future__ import annotations

from typing import Any

from med_autogrant.stage_router import _build_forced_rollback_actions


def _apply_quality_gate_to_route(
    *,
    route: dict[str, Any],
    quality_scorecard: dict[str, Any] | None,
) -> dict[str, Any]:
    resolved_route = dict(route)
    quality_payload = quality_scorecard if isinstance(quality_scorecard, dict) else {}
    quality_gate = quality_payload.get("loop_gate")
    if not isinstance(quality_gate, dict):
        return resolved_route

    resolved_route["quality_gate"] = dict(quality_gate)
    gate_action = str(quality_gate.get("action") or "").strip()
    gate_reason = str(quality_gate.get("reason") or "").strip()
    gate_stage = str(quality_gate.get("recommended_stage") or "").strip()
    route_stage = str(resolved_route.get("recommended_stage") or "").strip()

    if gate_action == "rollback_required" and gate_stage and gate_stage != route_stage:
        resolved_route["recommended_stage"] = gate_stage
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} 质量 gate 要求回退：{gate_reason}".strip()
        resolved_route["actions"] = _build_forced_rollback_actions(gate_stage)
        resolved_route["requires_human_confirmation"] = gate_stage in {
            "direction_screening",
            "question_refinement",
        }
        return resolved_route

    if gate_action == "continue" and route_stage in {"frozen", "ready_for_submission"} and gate_stage:
        resolved_route["recommended_stage"] = gate_stage
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} 质量 gate 暂不允许停止：{gate_reason}".strip()
        return resolved_route

    if gate_action == "ready_for_submission" and gate_reason:
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} {gate_reason}".strip()
    return resolved_route


def _looks_like_workspace(payload: dict[str, Any]) -> bool:
    return all(isinstance(payload.get(field), str) and payload[field] for field in (
        "grant_run_id",
        "workspace_id",
        "lifecycle_stage",
    ))
