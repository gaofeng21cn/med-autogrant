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
        "medical publication gate",
        "visual render/export proof gate",
    ):
        assert non_goal in contract["non_goals"]


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
        "/skill_catalog/skills/0/domain_projection/opl_runtime_manager_registration"
    )
    assert adapter["adoption_projection"]["maps_to_opl_contract"] == "opl_family_product_operator_projection.v1"
    assert adapter["adoption_projection"]["required_operator_fields"] == operator["required_fields"]
