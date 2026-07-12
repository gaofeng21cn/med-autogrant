from __future__ import annotations

from med_autogrant.stage_control_plane_parts.ai_route_policy import build_mag_ai_route_policy


def test_ai_route_policy_projects_declared_scope_without_program_route_authority() -> None:
    policy = build_mag_ai_route_policy(
        family_stage_control_plane={"stages": [{"stage_id": "intake"}, {"stage_id": "draft"}]},
        family_action_catalog={"actions": [{"action_id": "author"}]},
    )

    assert policy["semantic_route_owner"] == "codex_cli"
    assert policy["declared_stage_ids"] == ["draft", "intake"]
    assert policy["route_capabilities"]["route_back_to_any_declared_stage"] is True
    assert policy["quality_debt_policy"]["blocks_stage_transition"] is False
    assert policy["static_transition_table_present"] is False
    assert policy["program_validator_can_reject_ai_route"] is False
