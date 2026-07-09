from __future__ import annotations

from pathlib import Path

import pytest

from med_autogrant.opl_standard_pack import build_standard_pack
from med_autogrant.opl_standard_pack_constants import GENERATED_SURFACE_OWNER
from med_autogrant.opl_standard_pack_private_policy import (
    build_private_functional_surface_policy,
)
from med_autogrant.opl_standard_pack_source_policy import (
    ACTIVE_CALLER_STATUS_BY_PHYSICAL_CLASSIFICATION,
    ACTIVE_PATH_SCAN_POLICY,
    PHYSICAL_SOURCE_CLASSIFICATION_BUCKETS,
    PHYSICAL_SOURCE_SURFACE_CLASSIFICATIONS,
    PRIVATE_WRAPPER_RETIREMENT_FALSE_READY_PATTERN_IDS,
    RETIREMENT_EVIDENCE_REFS,
    STRICT_SOURCE_PURITY_FALSE_READY_PATTERN_IDS,
    TARGET_OWNER_BY_PHYSICAL_CLASSIFICATION,
    DOMAIN_READINESS_FALSE_READY_PATTERN_IDS,
    FORBIDDEN_GENERIC_OWNER_ROLES,
    FORBIDDEN_PHYSICAL_RESIDUE_CLASSES,
    GENERATED_HOSTED_SURFACE_FALSE_READY_PATTERN_IDS,
)


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_private_functional_policy_classifies_current_source_morphology() -> None:
    policy = build_standard_pack()["private_functional_surface_policy"]
    assert policy == build_private_functional_surface_policy(
        forbidden_generic_owner_roles=FORBIDDEN_GENERIC_OWNER_ROLES,
        physical_source_classification_buckets=PHYSICAL_SOURCE_CLASSIFICATION_BUCKETS,
        physical_source_surface_classifications=PHYSICAL_SOURCE_SURFACE_CLASSIFICATIONS,
        forbidden_physical_residue_classes=FORBIDDEN_PHYSICAL_RESIDUE_CLASSES,
        active_path_scan_policy=ACTIVE_PATH_SCAN_POLICY,
        retirement_evidence_refs=RETIREMENT_EVIDENCE_REFS,
        target_owner_by_physical_classification=TARGET_OWNER_BY_PHYSICAL_CLASSIFICATION,
        active_caller_status_by_physical_classification=(
            ACTIVE_CALLER_STATUS_BY_PHYSICAL_CLASSIFICATION
        ),
    )

    morphology = policy["physical_source_morphology_policy"]
    classifications = {
        surface["surface_id"]: surface
        for surface in morphology["surface_classifications"]
    }
    assert set(classifications) == set(morphology["required_surface_ids"])
    assert classifications["domain_runtime"]["classification"] == "declarative_grant_handler"
    assert classifications["product_entry"]["classification"] == "refs_only_adapter"
    assert classifications["grouped_cli_wrapper"]["target_owner_after_migration"] == (
        GENERATED_SURFACE_OWNER
    )
    assert classifications["memory"]["classification"] == "minimal_authority_function"
    assert classifications["package"]["classification"] == "minimal_authority_function"
    assert classifications["autonomy_controller"]["classification"] == (
        "minimal_authority_function"
    )
    assert classifications["repo_shell_verification_wrappers"]["classification"] == (
        "repo_native_verification_wrapper"
    )
    assert classifications["legacy_runtime_residue"]["classification"] == (
        "legacy_proof_tombstone"
    )

    for surface in classifications.values():
        for ref in surface["source_refs"]:
            path = Path(ref)
            assert not path.is_absolute(), ref
            assert ".." not in path.parts, ref
            assert "://" not in ref, ref
            assert (REPO_ROOT / ref).exists(), ref


def test_private_functional_policy_keeps_cleanup_and_ready_claims_fail_closed() -> None:
    morphology = build_standard_pack()["private_functional_surface_policy"][
        "physical_source_morphology_policy"
    ]
    cleanup = morphology["retirement_readback_cleanup_guard"]
    compact = cleanup["compact_cleanup_readiness_summary"]

    assert morphology["retirement_gate"]["state"] == (
        "active_caller_migration_evidence_required"
    )
    assert cleanup["state"] == "readback_guard_available_physical_delete_not_authorized"
    assert compact["cleanup_candidate_count"] == 0
    assert compact["owner_delta_required"] is False
    assert compact["can_apply_cleanup"] is False
    assert compact["can_authorize_physical_delete"] is False
    assert set(compact["retained_current_thin_surface_ids"]) == {
        "product_entry",
        "status",
        "user_loop",
        "domain_handler",
        "control_plane",
        "lifecycle",
    }
    assert compact["remaining_authority_gap"]["physical_delete_authorized"] is False
    assert compact["retained_surface_owner_decision"]["decision"] == (
        "retain_as_current_thin_domain_target"
    )
    assert morphology["authority_boundary"]["mag_can_own_generic_runtime"] is False
    assert morphology["authority_boundary"]["mag_can_own_generated_wrapper"] is False
    assert cleanup["authority_boundary"]["guard_can_authorize_physical_delete"] is False
    assert cleanup["authority_boundary"]["guard_can_sign_owner_receipt"] is False
    assert compact["owner_delta_work_order_pack"]["authority_boundary"][
        "work_order_can_authorize_physical_delete"
    ] is False
    assert compact["owner_delta_work_order_pack"]["authority_boundary"][
        "work_order_can_claim_production_ready"
    ] is False


def test_private_functional_policy_keeps_active_path_false_ready_patterns() -> None:
    morphology = build_standard_pack()["private_functional_surface_policy"][
        "physical_source_morphology_policy"
    ]
    policy = morphology["active_path_scan_policy"]
    pattern_ids = {pattern["pattern_id"] for pattern in policy["forbidden_role_patterns"]}

    assert policy == ACTIVE_PATH_SCAN_POLICY
    assert {
        "domain_runtime_patch_bridge_import",
        "json_generated_surface_owner_in_mag_allowed_true",
        "json_domain_repo_physical_delete_authorized_true",
        "python_single_claims_external_default_caller_consumption_complete_true",
        "yaml_machine_source_guard_can_claim_domain_ready_true",
        *PRIVATE_WRAPPER_RETIREMENT_FALSE_READY_PATTERN_IDS,
        *GENERATED_HOSTED_SURFACE_FALSE_READY_PATTERN_IDS,
        *DOMAIN_READINESS_FALSE_READY_PATTERN_IDS,
        *STRICT_SOURCE_PURITY_FALSE_READY_PATTERN_IDS,
    } <= pattern_ids
    assert policy["authority_boundary"] == {
        "policy_can_authorize_physical_delete": False,
        "policy_can_claim_production_long_run_soak": False,
        "policy_can_claim_grant_readiness": False,
    }
