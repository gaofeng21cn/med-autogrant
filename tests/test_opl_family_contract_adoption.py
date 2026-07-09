from __future__ import annotations

import json
from pathlib import Path

import pytest

from opl_family_contract_adoption_cases.controlled_soak import (
    test_mag_controlled_soak_deferred_without_descriptor_index_skeleton_regression as _assert_controlled_soak,
)


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = "contracts/runtime-program/opl-family-contract-adoption.json"
STAGE_CONTROL_PLANE_PATH = "contracts/stage_control_plane.json"
USER_STAGE_LOG_REQUIRED_FIELDS = {
    "stage_name",
    "problem_summary",
    "stage_goal",
    "stage_work_done",
    "changed_stage_surfaces",
    "outcome",
    "remaining_blockers",
    "evidence_refs",
}


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _contract() -> dict[str, object]:
    return json.loads(_read(CONTRACT_PATH))


def test_mag_adoption_contract_keeps_domain_owner_boundary() -> None:
    contract = _contract()

    assert contract["contract_kind"] == "mag_opl_family_contract_adoption.v1"
    assert contract["domain_id"] == "med-autogrant"
    assert contract["opl_role"] == "family-level projection consumer only"
    assert contract["attempt_projection"]["maps_to_opl_contract"] == (
        "opl_family_runtime_attempt_contract.v1"
    )
    assert contract["quality_projection"]["claim_only_ready_forbidden"] is True
    assert "OPL owns grant truth" in contract["non_goals"]
    assert "OPL bypasses submission-ready export gate" in contract["non_goals"]


def test_current_program_domain_handler_actions_match_product_entry_export() -> None:
    from med_autogrant.product_entry import MedAutoGrantProductEntry

    current_program = json.loads(_read("contracts/runtime-program/current-program.json"))
    adapter = current_program["runtime_owner"]["stage_led_framework_boundary"][
        "domain_handler_adapter"
    ]
    export = MedAutoGrantProductEntry().build_domain_handler_export(
        input_path=REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
    )

    assert adapter["allowed_dispatch_actions"] == export["domain_handler_export"][
        "opl_control_plane"
    ]["allowed_dispatch_actions"]


def test_mag_stage_control_projection_and_user_stage_log_remain_body_free() -> None:
    contract = _contract()
    stage_projection = contract["stage_control_projection"]
    plane = json.loads(_read(STAGE_CONTROL_PLANE_PATH))

    assert stage_projection["projection_role"] == "descriptor_only_stage_pack"
    assert stage_projection["maps_existing_surfaces_only"] is True
    assert stage_projection["owner_boundary"] == {
        "domain_truth_owner": "med-autogrant",
        "fundability_judgment_owner": "med-autogrant",
        "submission_ready_export_gate_owner": "med-autogrant",
        "opl_role": "stage descriptor/projection consumer only",
    }
    assert {stage["opl_stage"] for stage in stage_projection["stage_pack"]} == {
        "call_and_candidate_intake",
        "fundability_strategy",
        "specific_aims_and_structure",
        "proposal_authoring",
        "review_and_rebuttal",
        "package_and_submit_ready",
    }

    for stage in plane["stages"]:
        user_stage_log = stage["stage_contract"]["user_stage_log_contract"]
        assert user_stage_log["surface_kind"] == "opl_standard_agent_user_stage_log_contract"
        assert set(user_stage_log["required_domain_semantic_fields"]) == (
            USER_STAGE_LOG_REQUIRED_FIELDS
        )
        assert user_stage_log["authority_boundary"] == {
            "opl_can_infer_domain_semantics": False,
            "opl_can_read_artifact_body": False,
            "opl_can_write_domain_truth": False,
            "opl_can_authorize_quality_or_export": False,
            "provider_completion_can_claim_stage_semantics_complete": False,
        }


def test_mag_adoption_contract_keeps_memory_and_receipt_authority_in_mag() -> None:
    contract = _contract()
    memory = contract["domain_memory_descriptor_locator"]
    descriptor = contract["domain_memory_descriptor"]
    owner_receipt = contract["owner_receipt_contract"]
    lifecycle = contract["lifecycle_guarded_apply_proof"]

    assert memory["memory_owner"] == "med-autogrant"
    assert memory["memory_content_owner"] == "med-autogrant"
    assert memory["writeback_policy"] == (
        "opl_may_route_writeback_receipt_refs_but_mag_accepts_or_rejects_memory_content"
    )
    assert memory["migration_plan"]["migration_state"] == "runtime_apply_contract_landed"
    assert memory["authority_boundary"]["can_hold_memory_content"] is False
    assert memory["authority_boundary"]["can_issue_export_verdict"] is False
    assert descriptor["authority_boundary"]["domain_memory_owner"] == "med-autogrant"
    assert "memory_store_owner" in descriptor["authority_boundary"]["forbidden_opl_authority"]

    assert owner_receipt["allowed_return_shapes"] == [
        "domain_owner_receipt",
        "typed_blocker",
        "no_regression_evidence",
    ]
    assert owner_receipt["receipt_instance_repo_tracked"] is False
    assert lifecycle["operations"] == ["cleanup", "restore", "retention"]
    assert lifecycle["domain_mutation_policy"] == "requires_mag_owner_receipt"


def test_mag_adoption_contract_keeps_source_layout_and_controlled_soak_deferred() -> None:
    contract = _contract()
    audit = contract["repo_source_layout_audit"]
    follow_through = contract["physical_skeleton_follow_through"]

    assert audit["layout_state"] == "declarative_grant_pack_follow_through_landed"
    assert audit["boundary_keys"] == ["agent", "contracts", "runtime", "docs"]
    assert audit["forbidden_active_path_residue"] == []
    assert follow_through["state"] == "declarative_grant_pack_landed"
    assert follow_through["moves_workspace_artifacts"] is False
    assert follow_through["moves_runtime_receipt_instances"] is False
    assert follow_through["moves_memory_body"] is False
    for boundary in audit["boundary_keys"]:
        assert (REPO_ROOT / boundary).is_dir()
        assert audit["source_refs_by_boundary"][boundary]
    for anchor_ref in (
        "agent/prompts/call_and_candidate_intake.md",
        "agent/quality_gates/fundability.md",
        "agent/knowledge/grant_strategy_memory.md",
        "contracts/runtime-program/current-program.json",
        "src/med_autogrant/product_entry_parts/domain_handler.py",
    ):
        assert (REPO_ROOT / anchor_ref).exists()
    _assert_controlled_soak()
