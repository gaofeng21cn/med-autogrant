from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = "contracts/runtime-program/opl-family-contract-adoption.json"


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _contract() -> dict[str, object]:
    return json.loads(_read(CONTRACT_PATH))


def test_mag_declares_thin_opl_family_contract_adoption() -> None:
    contract = _contract()

    assert contract["contract_kind"] == "mag_opl_family_contract_adoption.v1"
    assert contract["domain_id"] == "med-autogrant"
    assert contract["opl_role"] == "family-level projection consumer only"


def test_mag_runtime_projection_maps_to_grant_runtime_truth_surfaces() -> None:
    contract = _contract()
    attempt = contract["attempt_projection"]

    for surface in (
        "runtime_control",
        "runtime_continuity",
        "grant-autonomy-controller-report",
        "workspace progress",
    ):
        assert surface in attempt["source_surfaces"]
    assert attempt["maps_to_opl_contract"] == "opl_family_runtime_attempt_contract.v1"
    assert "MAG owns grant authoring runtime" in attempt["owner_boundary"]


def test_mag_quality_projection_keeps_grant_quality_owner_and_excludes_other_domain_gates() -> None:
    contract = _contract()
    quality = contract["quality_projection"]

    for surface in (
        "grant_quality_scorecard",
        "grant_quality_closure_dossier",
        "grant review",
        "fundability gate",
        "submission-ready export gate",
    ):
        assert surface in quality["source_surfaces"]
    assert quality["maps_to_opl_contract"] == "opl_family_domain_quality_projection_contract.v1"
    assert quality["claim_only_ready_forbidden"] is True


def test_mag_operator_and_incident_projection_require_source_refs_and_mag_closure() -> None:
    contract = _contract()
    incident = contract["incident_projection"]
    operator = contract["operator_projection"]

    assert incident["maps_to_opl_contract"] == "opl_family_incident_learning_loop.v1"
    assert "MAG-owned closure ref" in incident["closure_rule"]
    for field in ("source_refs", "freshness", "owner_split", "next_surface_ref", "human_gate_reason"):
        assert field in operator["required_fields"]
    for non_goal in (
        "OPL owns grant truth",
        "OPL bypasses submission-ready export gate",
        "OPL owns grant stage truth",
        "medical publication gate",
        "visual render/export proof gate",
    ):
        assert non_goal in contract["non_goals"]


def test_mag_stage_control_projection_is_descriptor_only_and_maps_existing_stage_surfaces() -> None:
    contract = _contract()
    stage_projection = contract["stage_control_projection"]

    assert stage_projection["surface_kind"] == "mag_opl_family_stage_control_projection.v1"
    assert stage_projection["projection_role"] == "descriptor_only_stage_pack"
    assert stage_projection["maps_to_opl_contract"] == "opl_family_stage_control_plane_stage_pack.v1"
    assert stage_projection["maps_existing_surfaces_only"] is True
    assert stage_projection["owner_boundary"] == {
        "domain_truth_owner": "med-autogrant",
        "fundability_judgment_owner": "med-autogrant",
        "submission_ready_export_gate_owner": "med-autogrant",
        "opl_role": "stage descriptor/projection consumer only",
    }

    pack = {entry["opl_stage"]: entry for entry in stage_projection["stage_pack"]}
    assert list(pack) == [
        "call_and_candidate_intake",
        "fundability_strategy",
        "specific_aims_and_structure",
        "proposal_authoring",
        "review_and_rebuttal",
        "package_and_submit_ready",
    ]
    expected_surfaces = {
        "call_and_candidate_intake": {
            "discover-funding-opportunities",
            "select-project-profile",
            "initialize-intake-workspace",
            "input_intake",
        },
        "fundability_strategy": {
            "direction_screening",
            "fit_alignment",
            "grant_quality_scorecard",
            "fundability gate",
        },
        "specific_aims_and_structure": {
            "question_refinement",
            "argument_building",
            "outline",
        },
        "proposal_authoring": {
            "drafting",
            "revision",
            "grant-progress",
            "grant-user-loop",
        },
        "review_and_rebuttal": {
            "critique",
            "review",
            "grant_quality_closure_dossier",
            "quality-diff",
        },
        "package_and_submit_ready": {
            "freeze",
            "frozen",
            "package submission-ready",
            "submission-ready export gate",
        },
    }
    for stage, surfaces in expected_surfaces.items():
        assert set(pack[stage]["mag_surfaces"]) == surfaces
        assert pack[stage]["truth_owner"] == "med-autogrant"
        assert pack[stage]["authority"]


def test_mag_adoption_contract_declares_lifecycle_adapter_mapping() -> None:
    contract = _contract()
    adapter = contract["lifecycle_adapter"]
    operator = contract["operator_projection"]

    assert adapter["surface_kind"] == "opl_family_lifecycle_adapter_contract"
    assert adapter["adapter_id"] == "mag.opl_family.lifecycle_adapter.v1"
    assert adapter["maps_existing_surfaces_only"] is True
    assert adapter["sqlite_migration_required"] is False
    assert adapter["persistence_projection"]["maps_existing_surfaces"] == [
        "session_continuity",
        "runtime_control.restore_point",
        "artifact_inventory",
        "runtime_continuity",
    ]
    assert adapter["persistence_projection"]["write_policy"] == "opl_index_only_no_domain_truth_writes"
    assert adapter["lifecycle_projection"]["maps_to_opl_contract"] == "opl_family_runtime_attempt_contract.v1"
    for field in ("attempt_state", "workspace_boundary", "owner_repo", "last_observed_projection"):
        assert field in adapter["lifecycle_projection"]["required_projection_fields"]
    assert adapter["owner_route_discovery"]["route_truth_owner"] == "med-autogrant"
    assert adapter["owner_route_discovery"]["discovery_surface_ref"] == (
        "/skill_catalog/skills/0/domain_projection/opl_stage_runtime_registration"
    )
    assert adapter["adoption_projection"]["maps_to_opl_contract"] == "opl_family_product_operator_projection.v1"
    assert adapter["adoption_projection"]["required_operator_fields"] == operator["required_fields"]


def test_mag_adoption_contract_declares_domain_memory_locator_without_opl_content_or_verdict_authority() -> None:
    contract = _contract()
    memory = contract["domain_memory_descriptor_locator"]

    assert memory["surface_kind"] == "domain_memory_descriptor_locator"
    assert memory["descriptor_id"] == "mag.domain_memory_descriptor_locator.v1"
    assert memory["manifest_surface_ref"] == "/product_entry_manifest/domain_memory_descriptor_locator"
    assert memory["policy_ref"] == "docs/references/grant_strategy_memory_policy.md"
    assert memory["maps_to_opl_contract"] == "opl_family_domain_memory_locator_contract.v1"
    assert memory["memory_owner"] == "med-autogrant"
    assert memory["memory_content_owner"] == "med-autogrant"
    assert memory["truth_owner"] == "med-autogrant"
    assert memory["fundability_verdict_owner"] == "med-autogrant"
    assert memory["locator_policy"] == "repo_tracked_descriptor_and_locator_refs_only"
    assert memory["stage_memory_refs"] == [
        "call_and_candidate_intake",
        "fundability_strategy",
        "specific_aims_and_structure",
        "proposal_authoring",
        "review_and_rebuttal",
        "package_and_submit_ready",
    ]
    assert set(memory["opl_consumption"]) == {
        "descriptor",
        "policy_ref",
        "stage_descriptor_refs",
        "memory_locator",
        "writeback_receipt_refs",
    }
    for forbidden in (
        "memory_content",
        "fundability_verdict",
        "authoring_quality_verdict",
        "submission_ready_export_verdict",
        "canonical_grant_artifact_content",
    ):
        assert forbidden in memory["opl_non_consumption"]
    assert memory["writeback_policy"] == (
        "opl_may_route_writeback_receipt_refs_but_mag_accepts_or_rejects_memory_content"
    )
    authority = memory["authority_boundary"]
    assert authority["opl_role"] == "memory_locator_ref_and_receipt_ref_consumer_only"
    assert authority["can_hold_memory_content"] is False
    assert authority["can_issue_fundability_verdict"] is False
    assert authority["can_issue_authoring_quality_verdict"] is False
    assert authority["can_issue_export_verdict"] is False
    assert authority["can_mutate_domain_memory_store"] is False
