from __future__ import annotations

from typing import Any


_ALLOWED_AI_ROUTE_CONTEXT_RETURN_SHAPES = [
    "ai_route_context",
    "route_back_ref",
    "human_gate_ref",
    "domain_owner_receipt",
    "typed_blocker",
    "no_regression_evidence",
]


def build_ai_route_boundary(
    *,
    surface_id: str,
    mag_role: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_ai_route_boundary",
        "surface_id": surface_id,
        "semantic_route_owner": "codex_cli",
        "semantic_route_owner_role": "single_ai_control_plane",
        "mag_role": mag_role,
        "mag_writes_stage_current_pointer": False,
        "mag_writes_stage_terminal_state": False,
        "mag_writes_current_owner_delta": False,
        "mag_selects_next_opl_stage": False,
        "provider_completion_is_stage_transition": False,
        "workspace_lifecycle_stage_is_domain_observation": True,
        "recommendation_requires_framework_route_approval": False,
        "framework_can_accept_reject_or_override_codex_route": False,
        "program_recommendation_can_block_or_select_route": False,
        "allowed_return_shapes": list(_ALLOWED_AI_ROUTE_CONTEXT_RETURN_SHAPES),
    }


__all__ = ["build_ai_route_boundary"]
