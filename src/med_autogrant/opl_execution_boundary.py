from __future__ import annotations

from typing import Any


_STAGE_TRANSITION_AUTHORITY = "one-person-lab"
_ALLOWED_STAGE_AUTHORITY_RETURN_SHAPES = [
    "transition_intent_ref",
    "domain_owner_receipt",
    "typed_blocker",
    "no_regression_evidence",
]


def build_stage_transition_authority_boundary(
    *,
    surface_id: str,
    mag_role: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_stage_transition_authority_boundary",
        "surface_id": surface_id,
        "stage_transition_authority": _STAGE_TRANSITION_AUTHORITY,
        "stage_transition_authority_role": "sole_stage_current_terminal_next_writer",
        "mag_role": mag_role,
        "mag_writes_stage_current_pointer": False,
        "mag_writes_stage_terminal_state": False,
        "mag_writes_current_owner_delta": False,
        "mag_selects_next_opl_stage": False,
        "provider_completion_is_stage_transition": False,
        "workspace_lifecycle_stage_is_domain_observation": True,
        "recommendation_requires_opl_stage_transition_authority": True,
        "allowed_return_shapes": list(_ALLOWED_STAGE_AUTHORITY_RETURN_SHAPES),
    }


__all__ = ["build_stage_transition_authority_boundary"]
