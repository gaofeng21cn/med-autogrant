from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_json(relative_path: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_state_index_kernel_adoption_is_opl_owned_refs_only_sidecar() -> None:
    adoption = _read_json("contracts/stage_artifact_kernel_adoption.json")
    state_index = adoption["state_index_kernel_adoption"]

    assert state_index["surface_kind"] == "opl_state_index_kernel_sidecar_adoption"
    assert state_index["state_index_kernel_owner"] == "one-person-lab"
    assert state_index["sqlite_sidecar_owner"] == "one-person-lab"
    assert state_index["sqlite_migration_required"] is False
    assert state_index["mag_consumption_role"] == "opaque_refs_only_sidecar_index_consumer"
    assert state_index["source_of_truth"] == "physical_stage_folder_files_and_mag_owned_artifact_files"
    assert state_index["index_authority"] == "derived_refs_only_no_domain_body_authority"
    assert state_index["derived_index_rebuildable"] is True
    assert set(state_index["consumed_index_refs"]) == {
        "stage_folder_ref_index",
        "manifest_ref_index",
        "receipt_ref_index",
        "current_pointer_ref_index",
        "canonical_artifact_ref_index",
        "export_ref_index",
        "lineage_ref_index",
        "retention_ref_index",
        "conformance_ref_index",
    }

    forbidden_payloads = set(state_index["forbidden_sqlite_payloads"])
    assert {
        "grant_body",
        "grant_strategy_memory_body",
        "fundability_verdict_body",
        "authoring_quality_verdict_body",
        "submission_ready_export_verdict_body",
        "package_body",
        "artifact_body",
    } <= forbidden_payloads

    assert {
        "generic_sqlite_owner",
        "generic_state_index_kernel_owner",
        "generic_runtime_owner",
        "generic_lifecycle_owner",
        "generic_queue_owner",
        "generic_read_model_owner",
    } <= set(state_index["forbidden_mag_owner_roles"])

    authority = state_index["authority_boundary"]
    assert authority == {
        "mag_can_write_sqlite_sidecar_index": False,
        "mag_can_store_grant_body_in_sqlite": False,
        "mag_can_store_memory_body_in_sqlite": False,
        "mag_can_store_verdict_body_in_sqlite": False,
        "mag_can_store_package_body_in_sqlite": False,
        "opl_can_read_grant_body_from_index": False,
        "opl_can_read_memory_body_from_index": False,
        "opl_can_read_verdict_body_from_index": False,
        "opl_can_read_package_body_from_index": False,
    }


def test_opl_family_lifecycle_adapter_points_to_same_state_index_adoption() -> None:
    stage_adoption = _read_json("contracts/stage_artifact_kernel_adoption.json")
    family_adoption = _read_json("contracts/runtime-program/opl-family-contract-adoption.json")
    state_index = stage_adoption["state_index_kernel_adoption"]
    lifecycle_adapter = family_adoption["lifecycle_adapter"]
    sidecar = lifecycle_adapter["state_index_sidecar_consumption"]

    assert lifecycle_adapter["sqlite_migration_required"] is False
    assert (
        lifecycle_adapter["state_index_kernel_adoption_ref"]
        == "contracts/stage_artifact_kernel_adoption.json#/state_index_kernel_adoption"
    )
    assert sidecar["maps_to"] == "opl_state_index_kernel_sidecar"
    assert sidecar["state_index_kernel_owner"] == state_index["state_index_kernel_owner"]
    assert sidecar["sqlite_sidecar_owner"] == state_index["sqlite_sidecar_owner"]
    assert sidecar["mag_consumption_role"] == state_index["mag_consumption_role"]
    assert sidecar["sqlite_migration_required"] is False
    assert sidecar["source_of_truth"] == state_index["source_of_truth"]
    assert sidecar["write_policy"] == "opl_refs_only_index_no_domain_truth_writes"
    assert sidecar["forbidden_sqlite_payloads"] == state_index["forbidden_sqlite_payloads"]
    assert sidecar["forbidden_mag_owner_roles"] == state_index["forbidden_mag_owner_roles"]


def test_foundry_series_forbids_mag_specific_sqlite_or_state_index_owner_drift() -> None:
    series = _read_json("contracts/foundry_agent_series.json")
    profile = series["domain_specific_profile"]

    assert "mag_specific_sqlite_or_state_index_kernel_owner" in profile["forbidden_series_drift"]
    assert profile["opl_scope"] == "refs_projection_runtime_only"
    assert profile["series_variation_policy"] == (
        "MAG differs from MAS/RCA/OMA by grant and fund-material inputs plus grant proposal and package "
        "outputs, not by lifecycle ownership."
    )
