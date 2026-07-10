from __future__ import annotations

import json
from pathlib import Path

import pytest

from opl_family_contract_adoption_cases.controlled_soak import (
    test_mag_controlled_soak_deferred_without_descriptor_index_skeleton_regression as _assert_controlled_soak,
)


pytestmark = pytest.mark.meta
REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / "contracts" / "runtime-program" / "opl-family-contract-adoption.json"


def _contract() -> dict[str, object]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_adoption_keeps_mag_truth_receipt_and_export_authority() -> None:
    contract = _contract()
    assert contract["contract_kind"] == "mag_opl_family_contract_adoption.v1"
    assert contract["domain_id"] == "med-autogrant"
    assert contract["opl_role"] == "family-level projection consumer only"
    assert contract["quality_projection"]["claim_only_ready_forbidden"] is True

    memory = contract["domain_memory_descriptor_locator"]
    receipt = contract["owner_receipt_contract"]
    lifecycle = contract["lifecycle_guarded_apply_proof"]
    assert memory["memory_owner"] == "med-autogrant"
    assert memory["authority_boundary"]["can_hold_memory_content"] is False
    assert memory["authority_boundary"]["can_issue_export_verdict"] is False
    assert receipt["allowed_return_shapes"] == ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"]
    assert receipt["receipt_instance_repo_tracked"] is False
    assert lifecycle["domain_mutation_policy"] == "requires_mag_owner_receipt"


def test_stage_projection_is_body_free_and_matches_domain_handler_actions() -> None:
    from med_autogrant.product_entry import MedAutoGrantProductEntry

    contract = _contract()
    plane = json.loads((REPO_ROOT / "contracts" / "stage_control_plane.json").read_text(encoding="utf-8"))
    projection = contract["stage_control_projection"]
    assert projection["projection_role"] == "descriptor_only_stage_pack"
    assert projection["maps_existing_surfaces_only"] is True
    for stage in plane["stages"]:
        boundary = stage["stage_contract"]["user_stage_log_contract"]["authority_boundary"]
        assert all(value is False for value in boundary.values())

    current_program = json.loads(
        (REPO_ROOT / "contracts" / "runtime-program" / "current-program.json").read_text(encoding="utf-8")
    )
    expected_actions = current_program["runtime_owner"]["stage_led_framework_boundary"]["domain_handler_adapter"]["allowed_dispatch_actions"]
    export = MedAutoGrantProductEntry().build_domain_handler_export(
        input_path=REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
    )
    assert export["domain_handler_export"]["opl_control_plane"]["allowed_dispatch_actions"] == expected_actions


def test_source_layout_sentinels_exist_and_controlled_soak_stays_deferred() -> None:
    audit = _contract()["repo_source_layout_audit"]
    assert audit["forbidden_active_path_residue"] == []
    for boundary in audit["boundary_keys"]:
        assert (REPO_ROOT / boundary).is_dir()
        assert audit["source_refs_by_boundary"][boundary]
    _assert_controlled_soak()
