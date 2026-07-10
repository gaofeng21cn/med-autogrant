from __future__ import annotations

from pathlib import Path

import pytest

from med_autogrant.opl_standard_pack import build_standard_pack
from med_autogrant.opl_standard_pack_private_policy import build_private_functional_surface_policy
from med_autogrant.opl_standard_pack_source_policy import (
    ACTIVE_CALLER_STATUS_BY_PHYSICAL_CLASSIFICATION,
    ACTIVE_PATH_SCAN_POLICY,
    PHYSICAL_SOURCE_CLASSIFICATION_BUCKETS,
    PHYSICAL_SOURCE_SURFACE_CLASSIFICATIONS,
    RETIREMENT_EVIDENCE_REFS,
    TARGET_OWNER_BY_PHYSICAL_CLASSIFICATION,
    FORBIDDEN_GENERIC_OWNER_ROLES,
    FORBIDDEN_PHYSICAL_RESIDUE_CLASSES,
)


pytestmark = pytest.mark.meta
REPO_ROOT = Path(__file__).resolve().parents[1]


def test_private_policy_matches_builder_and_source_sentinels() -> None:
    policy = build_standard_pack()["private_functional_surface_policy"]
    assert policy == build_private_functional_surface_policy(
        forbidden_generic_owner_roles=FORBIDDEN_GENERIC_OWNER_ROLES,
        physical_source_classification_buckets=PHYSICAL_SOURCE_CLASSIFICATION_BUCKETS,
        physical_source_surface_classifications=PHYSICAL_SOURCE_SURFACE_CLASSIFICATIONS,
        forbidden_physical_residue_classes=FORBIDDEN_PHYSICAL_RESIDUE_CLASSES,
        active_path_scan_policy=ACTIVE_PATH_SCAN_POLICY,
        retirement_evidence_refs=RETIREMENT_EVIDENCE_REFS,
        target_owner_by_physical_classification=TARGET_OWNER_BY_PHYSICAL_CLASSIFICATION,
        active_caller_status_by_physical_classification=ACTIVE_CALLER_STATUS_BY_PHYSICAL_CLASSIFICATION,
    )

    morphology = policy["physical_source_morphology_policy"]
    classifications = {item["surface_id"]: item for item in morphology["surface_classifications"]}
    assert set(classifications) == set(morphology["required_surface_ids"])
    assert classifications["domain_runtime"]["classification"] == "declarative_grant_handler"
    assert classifications["product_entry"]["classification"] == "refs_only_adapter"
    assert classifications["memory"]["classification"] == "minimal_authority_function"
    assert classifications["package"]["classification"] == "minimal_authority_function"
    assert classifications["legacy_runtime_residue"]["classification"] == "legacy_proof_tombstone"
    for surface in classifications.values():
        for ref in surface["source_refs"]:
            assert not Path(ref).is_absolute()
            assert (REPO_ROOT / ref).exists(), ref


def test_cleanup_and_ready_claims_remain_fail_closed() -> None:
    morphology = build_standard_pack()["private_functional_surface_policy"]["physical_source_morphology_policy"]
    cleanup = morphology["retirement_readback_cleanup_guard"]
    compact = cleanup["compact_cleanup_readiness_summary"]

    assert morphology["retirement_gate"]["state"] == "active_caller_migration_evidence_required"
    assert compact["cleanup_candidate_count"] == 0
    assert compact["can_apply_cleanup"] is False
    assert compact["can_authorize_physical_delete"] is False
    assert morphology["authority_boundary"]["mag_can_own_generic_runtime"] is False
    assert cleanup["authority_boundary"]["guard_can_sign_owner_receipt"] is False
    assert ACTIVE_PATH_SCAN_POLICY["authority_boundary"] == {
        "policy_can_authorize_physical_delete": False,
        "policy_can_claim_production_long_run_soak": False,
        "policy_can_claim_grant_readiness": False,
    }
