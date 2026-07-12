from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


def build_mag_ai_route_policy(
    *,
    family_stage_control_plane: Mapping[str, Any],
    family_action_catalog: Mapping[str, Any],
) -> dict[str, Any]:
    """Project declared stage scope without selecting or rejecting semantic routes."""

    declared_stage_ids = sorted(
        str(stage["stage_id"])
        for stage in family_stage_control_plane.get("stages", [])
        if isinstance(stage, Mapping) and stage.get("stage_id")
    )
    declared_action_ids = sorted(
        str(action["action_id"])
        for action in family_action_catalog.get("actions", [])
        if isinstance(action, Mapping) and action.get("action_id")
    )
    return {
        "surface_kind": "mag_ai_selected_progress_route_policy",
        "version": "mag-ai-selected-progress-route-policy.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "semantic_route_owner": "codex_cli",
        "route_policy": "ai_selected_progress_route",
        "declared_stage_ids": declared_stage_ids,
        "declared_action_ids": declared_action_ids,
        "route_capabilities": {
            "advance": True,
            "repeat_current_stage": True,
            "skip_declared_stage": True,
            "route_back_to_any_declared_stage": True,
            "carry_raw_partial_or_negative_evidence": True,
        },
        "quality_debt_policy": {
            "blocks_stage_transition": False,
            "blocks_fundability_quality_submission_export_or_ready_claims": True,
        },
        "static_transition_table_present": False,
        "program_validator_can_reject_ai_route": False,
        "authority_boundary": {
            "opl_role": "transport_and_declared_stage_scope_only",
            "mag_role": "grant_truth_and_claim_authority_only",
            "codex_cli_role": "semantic_route_selection",
            "opl_can_select_or_reject_semantic_route": False,
            "mag_static_program_can_select_or_reject_semantic_route": False,
            "opl_can_write_grant_truth": False,
        },
    }


__all__ = ["build_mag_ai_route_policy"]
