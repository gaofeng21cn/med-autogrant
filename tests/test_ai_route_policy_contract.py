from __future__ import annotations

import json
from pathlib import Path

from med_autogrant.stage_control_plane_parts.ai_route_policy import build_mag_ai_route_policy


REPO_ROOT = Path(__file__).resolve().parents[1]


def _assert_progress_first_route_policy(policy: dict[str, object]) -> None:
    assert policy["route_selection_owner"] == "codex_cli"
    assert policy["codex_may_advance_skip_repeat_reverse_or_route_back"] is True
    assert policy["any_declared_stage_may_start_from_any_prior_stage_result"] is True
    assert policy["declared_requires_are_quality_context_not_launch_gates"] is True
    assert policy["next_stage_refs_are_recommendations_not_constraints"] is True


def test_stage_manifest_gives_codex_unrestricted_declared_stage_routing() -> None:
    manifest = json.loads((REPO_ROOT / "agent/stages/manifest.json").read_text(encoding="utf-8"))
    policy = manifest["progress_first_policy"]
    _assert_progress_first_route_policy(policy)
    assert policy["no_output_or_failure_diagnostic_advances_stage"] is True


def test_stage_operating_principles_match_progress_first_route_policy() -> None:
    principles = json.loads(
        (REPO_ROOT / "contracts/stage_operating_principles.json").read_text(encoding="utf-8")
    )
    _assert_progress_first_route_policy(principles["speed_policy"])


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
