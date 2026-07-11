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


def test_foundry_consumer_does_not_copy_state_index_policy() -> None:
    series = _read_json("contracts/foundry_agent_series.json")
    adoption = _read_json("contracts/stage_artifact_kernel_adoption.json")

    assert "state_index_kernel_adoption" not in series
    assert adoption["state_index_kernel_adoption"]["state_index_kernel_owner"] == "one-person-lab"
