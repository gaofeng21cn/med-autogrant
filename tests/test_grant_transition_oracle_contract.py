from __future__ import annotations

import json
from pathlib import Path

from med_autogrant.stage_control_plane_parts.transition_oracle import (
    GRANT_TRANSITION_ORACLE_FIXTURES,
    GRANT_TRANSITION_TABLE,
    build_mag_grant_transition_oracle,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_manifest_normal_forward_edges_exist_in_transition_oracle() -> None:
    manifest = _read_json("agent/stages/manifest.json")
    manifest_edges = {
        (stage["stage_id"], next_stage_id)
        for stage in manifest["stages"]
        for next_stage_id in stage["next_stage_refs"]
    }
    oracle_edges = {
        (transition["from_stage_id"], transition["to_stage_id"])
        for transition in GRANT_TRANSITION_TABLE
    }

    assert manifest_edges <= oracle_edges


def test_every_oracle_transition_has_one_matching_fixture() -> None:
    transitions = {
        transition["transition_id"]: transition
        for transition in GRANT_TRANSITION_TABLE
    }
    fixtures_by_transition: dict[str, list[dict[str, object]]] = {}
    for fixture in GRANT_TRANSITION_ORACLE_FIXTURES:
        fixtures_by_transition.setdefault(fixture["expected_transition_id"], []).append(fixture)

    assert set(fixtures_by_transition) == set(transitions)
    assert all(len(fixtures) == 1 for fixtures in fixtures_by_transition.values())
    assert all(
        fixtures[0]["source_stage_id"] == transitions[transition_id]["from_stage_id"]
        for transition_id, fixtures in fixtures_by_transition.items()
    )


def test_fundability_success_and_human_gate_closeouts_are_explicit() -> None:
    manifest = _read_json("agent/stages/manifest.json")
    transitions = {
        transition["transition_id"]: transition
        for transition in GRANT_TRANSITION_TABLE
    }
    fixtures = {
        fixture["fixture_id"]: fixture
        for fixture in GRANT_TRANSITION_ORACLE_FIXTURES
    }

    success = transitions["fundability_strategy_accepted_to_specific_aims"]
    assert success["guard_id"] == "fundability_verdict_and_strategy_accepted"
    assert success["return_shape"] == "owner_receipt_ref"
    assert success["receipt_requirement"] == "fundability_strategy_handoff_receipt"
    assert fixtures["fundability_strategy_ready_to_specific_aims"][
        "expected_transition_id"
    ] == success["transition_id"]

    human_gate_transitions = [
        transition
        for transition in GRANT_TRANSITION_TABLE
        if transition["receipt_requirement"] == "human_gate_receipt"
    ]
    assert human_gate_transitions
    assert all(
        transition["return_shape"] == "human_gate_ref"
        and "blocked_shape" not in transition
        for transition in human_gate_transitions
    )

    oracle = build_mag_grant_transition_oracle(
        family_stage_control_plane=manifest,
        family_action_catalog=_read_json("contracts/action_catalog.json"),
    )
    assert oracle["validation"]["missing_stage_refs"] == []
    assert oracle["validation"]["missing_action_refs"] == []
    assert oracle["validation"]["missing_fixture_transition_refs"] == []
    assert oracle["validation"]["missing_transition_fixture_refs"] == []
    assert oracle["validation"]["duplicate_transition_ids"] == []
    assert oracle["validation"]["duplicate_fixture_ids"] == []
    assert oracle["validation"]["duplicate_fixture_transition_refs"] == []
    assert oracle["validation"]["mismatched_fixture_source_refs"] == []
