from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = "contracts/runtime-program/opl-family-contract-adoption.json"


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _contract() -> dict[str, object]:
    return json.loads(_read(CONTRACT_PATH))


def test_mag_controlled_soak_deferred_without_descriptor_index_skeleton_regression() -> None:
    contract = _contract()
    skeleton = contract["standard_domain_agent_skeleton"]
    controlled_soak = skeleton["controlled_soak"]

    assert controlled_soak["state"] == "deferred"
    assert controlled_soak["required_opl_substrate"] == "Temporal production online runtime"
    assert controlled_soak["no_regression_surfaces"] == [
        "family_action_catalog",
        "family_stage_control_plane",
        "standard_domain_agent_skeleton",
        "artifact_locator_contract",
        "controlled_stage_attempt_projection",
        "controlled_domain_memory_apply_proof",
        "owner_receipt_contract",
        "lifecycle_guarded_apply_proof",
        "physical_skeleton_follow_through",
        "domain_memory_descriptor_locator",
        "repo_source_layout_audit",
    ]
    assert "provider_hosted_controlled_grant_stage_soak_completed" in controlled_soak["forbidden_deferred_claims"]
    assert "accepted_or_rejected_receipt_instance_repo_tracked" in controlled_soak["forbidden_deferred_claims"]
    assert "OPL_holds_fundability_or_submission_ready_export_verdict" in controlled_soak["forbidden_deferred_claims"]
