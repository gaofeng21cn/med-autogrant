from __future__ import annotations

import copy
import json
from pathlib import Path
from urllib.parse import urlparse

import pytest

from med_autogrant.opl_standard_pack_source_policy import (
    ACTIVE_PATH_SCAN_POLICY,
)
from med_autogrant.product_entry_parts.functional_closure_skeleton import (
    build_physical_skeleton_follow_through,
)


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_REF = "contracts/private_functional_surface_policy.json"


def _contract_active_path_policy() -> dict[str, object]:
    payload = json.loads((REPO_ROOT / POLICY_REF).read_text(encoding="utf-8"))
    morphology = payload["physical_source_morphology_policy"]
    return morphology["active_path_scan_policy"]


def _assert_repo_local_path(path: str) -> None:
    parsed = urlparse(path)
    assert not parsed.scheme, path
    candidate = Path(path)
    assert not candidate.is_absolute(), path
    assert candidate.parts
    assert ".." not in candidate.parts, path
    assert str(candidate).strip() == path


def test_active_path_scan_policy_is_contract_owned_and_repo_local() -> None:
    policy = _contract_active_path_policy()

    assert policy == ACTIVE_PATH_SCAN_POLICY
    assert policy["state"] == "contract_owned_current_role_guard_policy"
    assert policy["scans_repo_source_only"] is True
    assert policy["excludes_human_docs"] is True
    assert policy["authority_boundary"] == {
        "policy_can_authorize_physical_delete": False,
        "policy_can_claim_production_long_run_soak": False,
        "policy_can_claim_grant_readiness": False,
    }

    for root in policy["roots"]:
        _assert_repo_local_path(root)
        assert (REPO_ROOT / root).is_dir(), root

    existing_explicit_files = []
    for file_path in policy["files"]:
        _assert_repo_local_path(file_path)
        candidate = REPO_ROOT / file_path
        if candidate.exists():
            existing_explicit_files.append(file_path)
            assert candidate.is_file(), file_path
    assert {"Makefile", "pyproject.toml"}.issubset(set(existing_explicit_files))

    for retired_path in policy["forbidden_active_paths"]:
        _assert_repo_local_path(retired_path)
        assert not (REPO_ROOT / retired_path).exists(), retired_path

    pattern_ids = []
    for pattern in policy["forbidden_role_patterns"]:
        pattern_ids.append(pattern["pattern_id"])
        assert pattern["pattern_id"]
        assert pattern["policy"]
        assert pattern["literal_parts"]
        assert all(isinstance(part, str) and part for part in pattern["literal_parts"])

    assert len(pattern_ids) == len(set(pattern_ids))
    assert {
        "domain_runtime_patch_bridge_import",
        "json_generated_surface_owner_in_mag_allowed_true",
        "json_domain_repo_physical_delete_authorized_true",
        "python_single_claims_external_default_caller_consumption_complete_true",
        "toml_physical_delete_authorized_by_refs_true",
    } <= set(pattern_ids)


def test_active_path_scan_uses_policy_and_fails_closed_on_injected_legacy_literal() -> None:
    current_scan = build_physical_skeleton_follow_through()[
        "active_path_current_role_guard"
    ]
    policy = _contract_active_path_policy()

    assert current_scan["policy_id"] == policy["policy_id"]
    assert current_scan["scanned_scope"]["roots"] == policy["roots"]
    assert current_scan["scanned_scope"]["files"] == policy["files"]
    assert current_scan["scanned_scope"]["suffixes"] == policy["suffixes"]
    assert current_scan["state"] == "passed"
    assert current_scan["forbidden_role_matches"] == []
    assert all(
        status["state"] == "absent"
        for status in current_scan["forbidden_path_status"]
    )

    injected_policy = copy.deepcopy(policy)
    injected_policy["forbidden_role_patterns"] = [
        *injected_policy["forbidden_role_patterns"],
        {
            "pattern_id": "injected_policy_consumption_probe",
            "literal_parts": ["def ", "_build_active_path_current_role_guard"],
            "policy": "test proves scanner consumes caller-supplied contract policy",
        },
    ]

    injected_scan = build_physical_skeleton_follow_through(
        active_path_scan_policy=injected_policy,
    )["active_path_current_role_guard"]

    assert injected_scan["state"] == "failed"
    assert injected_scan["current_role_guard_passed"] is False
    assert any(
        match["pattern_id"] == "injected_policy_consumption_probe"
        for match in injected_scan["forbidden_role_matches"]
    )


def test_active_path_scan_fails_closed_on_generated_surface_owner_resurrection() -> None:
    probe_path = REPO_ROOT / "contracts" / "__active_path_scan_generated_owner_probe.json"
    key = "generated_surface_owner" + "_in_mag_allowed"
    probe_path.write_text(
        f'{{"{key}": true}}\n',
        encoding="utf-8",
    )
    try:
        scan = build_physical_skeleton_follow_through()[
            "active_path_current_role_guard"
        ]
    finally:
        probe_path.unlink(missing_ok=True)

    assert scan["state"] == "failed"
    assert scan["current_role_guard_passed"] is False
    assert any(
        match["path"] == "contracts/__active_path_scan_generated_owner_probe.json"
        and match["pattern_id"] == "json_generated_surface_owner_in_mag_allowed_true"
        for match in scan["forbidden_role_matches"]
    )


@pytest.mark.parametrize(
    ("probe_name", "probe_text_parts", "pattern_id"),
    [
        (
            "__active_path_scan_generated_owner_probe.py",
            ["PROBE = {'generated_surface_owner': '", "med-autogrant", "'}\n"],
            "python_generated_surface_owner_points_to_mag",
        ),
        (
            "__active_path_scan_generated_owner_probe.toml",
            ["generated_surface_owner", ' = "', "medautogrant", '"\n'],
            "toml_generated_surface_owner_points_to_mag_domain_id",
        ),
        (
            "__active_path_scan_generated_owner_probe.yaml",
            ["generated_surface_owner: ", "med-autogrant", "\n"],
            "yaml_generated_surface_owner_points_to_mag",
        ),
    ],
)
def test_active_path_scan_fails_closed_on_direct_generated_surface_owner_resurrection(
    probe_name: str,
    probe_text_parts: list[str],
    pattern_id: str,
) -> None:
    probe_path = REPO_ROOT / "contracts" / probe_name
    probe_path.write_text("".join(probe_text_parts), encoding="utf-8")
    try:
        scan = build_physical_skeleton_follow_through()[
            "active_path_current_role_guard"
        ]
    finally:
        probe_path.unlink(missing_ok=True)

    assert scan["state"] == "failed"
    assert scan["current_role_guard_passed"] is False
    assert any(
        match["path"] == f"contracts/{probe_name}"
        and match["pattern_id"] == pattern_id
        for match in scan["forbidden_role_matches"]
    )


@pytest.mark.parametrize(
    ("probe_name", "probe_text_parts", "pattern_id"),
    [
        (
            "__active_path_scan_default_caller_false_ready_probe.json",
            ['{"mag_claims_default_caller_', 'cutover_complete": true}\n'],
            "json_mag_claims_default_caller_cutover_complete_true",
        ),
        (
            "__active_path_scan_default_caller_false_ready_probe.py",
            ['PROBE = {"claims_external_default_caller_', 'consumption_complete": True}\n'],
            "python_claims_external_default_caller_consumption_complete_true",
        ),
        (
            "__active_path_scan_default_caller_false_ready_probe.py",
            ["PROBE = {'mag_claims_default_caller_", "cutover_complete': True}\n"],
            "python_single_mag_claims_default_caller_cutover_complete_true",
        ),
        (
            "__active_path_scan_default_caller_false_ready_probe.toml",
            ["claims_external_default_caller_", "consumption_complete = true\n"],
            "toml_claims_external_default_caller_consumption_complete_true",
        ),
        (
            "__active_path_scan_default_caller_false_ready_probe.yaml",
            ["mag_claims_default_caller_", "cutover_complete: true\n"],
            "yaml_mag_claims_default_caller_cutover_complete_true",
        ),
        (
            "__active_path_scan_default_caller_false_ready_probe.json",
            ['{"claims_opl_generated_hosted_', 'production_caller_complete": true}\n'],
            "json_claims_opl_generated_hosted_production_caller_complete_true",
        ),
        (
            "__active_path_scan_default_caller_false_ready_probe.py",
            ["PROBE = {'claims_opl_generated_hosted_", "production_caller_complete': True}\n"],
            "python_single_claims_opl_generated_hosted_production_caller_complete_true",
        ),
        (
            "__active_path_scan_default_caller_false_ready_probe.toml",
            ["claims_opl_generated_hosted_", "production_caller_complete = true\n"],
            "toml_claims_opl_generated_hosted_production_caller_complete_true",
        ),
        (
            "__active_path_scan_default_caller_false_ready_probe.yaml",
            ["claims_opl_generated_hosted_", "production_caller_complete: true\n"],
            "yaml_claims_opl_generated_hosted_production_caller_complete_true",
        ),
        (
            "__active_path_scan_physical_delete_false_ready_probe.py",
            ['PROBE = {"domain_repo_physical_', 'delete_authorized": True}\n'],
            "python_domain_repo_physical_delete_authorized_true",
        ),
        (
            "__active_path_scan_physical_delete_false_ready_probe.py",
            ["PROBE = {'domain_repo_physical_", "delete_authorized': True}\n"],
            "python_single_domain_repo_physical_delete_authorized_true",
        ),
        (
            "__active_path_scan_physical_delete_false_ready_probe.toml",
            ["domain_repo_physical_", "delete_authorized = true\n"],
            "toml_domain_repo_physical_delete_authorized_true",
        ),
        (
            "__active_path_scan_physical_delete_false_ready_probe.yaml",
            ["domain_repo_physical_", "delete_authorized: true\n"],
            "yaml_domain_repo_physical_delete_authorized_true",
        ),
        (
            "__active_path_scan_physical_delete_false_ready_probe.json",
            ['{"physical_delete_authorized_', 'by_refs": true}\n'],
            "json_physical_delete_authorized_by_refs_true",
        ),
        (
            "__active_path_scan_physical_delete_false_ready_probe.py",
            ["PROBE = {'physical_delete_authorized_", "by_refs': True}\n"],
            "python_single_physical_delete_authorized_by_refs_true",
        ),
        (
            "__active_path_scan_physical_delete_false_ready_probe.toml",
            ["physical_delete_authorized_", "by_refs = true\n"],
            "toml_physical_delete_authorized_by_refs_true",
        ),
        (
            "__active_path_scan_physical_delete_false_ready_probe.yaml",
            ["physical_delete_authorized_", "by_refs: true\n"],
            "yaml_physical_delete_authorized_by_refs_true",
        ),
        (
            "__active_path_scan_domain_readiness_false_ready_probe.json",
            ['{"claims_grant_', 'ready": true}\n'],
            "json_claims_grant_ready_true",
        ),
        (
            "__active_path_scan_domain_readiness_false_ready_probe.py",
            ['PROBE = {"claims_authoring_quality_', 'ready": True}\n'],
            "python_claims_authoring_quality_ready_true",
        ),
        (
            "__active_path_scan_domain_readiness_false_ready_probe.py",
            ["PROBE = {'quality_ready_", "claimed': True}\n"],
            "python_single_quality_ready_claimed_true",
        ),
        (
            "__active_path_scan_domain_readiness_false_ready_probe.toml",
            ["claims_submission_ready_", "export = true\n"],
            "toml_claims_submission_ready_export_true",
        ),
        (
            "__active_path_scan_domain_readiness_false_ready_probe.yaml",
            ["production_ready_", "claimed: true\n"],
            "yaml_production_ready_claimed_true",
        ),
        (
            "__active_path_scan_private_wrapper_retirement_probe.json",
            ['{"private_wrapper_', 'retirement_complete": true}\n'],
            "json_private_wrapper_retirement_complete_true",
        ),
        (
            "__active_path_scan_private_wrapper_retirement_probe.py",
            ['PROBE = {"legacy_wrapper_', 'retirement_complete": True}\n'],
            "python_legacy_wrapper_retirement_complete_true",
        ),
        (
            "__active_path_scan_private_wrapper_retirement_probe.py",
            ["PROBE = {'no_active_private_wrapper_", "caller_complete': True}\n"],
            "python_single_no_active_private_wrapper_caller_complete_true",
        ),
        (
            "__active_path_scan_private_wrapper_retirement_probe.toml",
            ["tombstone_provenance_", "complete = true\n"],
            "toml_tombstone_provenance_complete_true",
        ),
        (
            "__active_path_scan_private_wrapper_retirement_probe.yaml",
            ["claims_private_platform_", "residue_retired: true\n"],
            "yaml_claims_private_platform_residue_retired_true",
        ),
        (
            "__active_path_scan_retirement_readback_probe.json",
            ['{"retirement_readback_', 'cleanup_complete": true}\n'],
            "json_retirement_readback_cleanup_complete_true",
        ),
        (
            "__active_path_scan_retirement_readback_probe.py",
            ['PROBE = {"cleanup_readback_physical_', 'delete_authorized": True}\n'],
            "python_cleanup_readback_physical_delete_authorized_true",
        ),
        (
            "__active_path_scan_retirement_readback_probe.py",
            ["PROBE = {'claims_cleanup_readback_", "authorizes_delete': True}\n"],
            "python_single_claims_cleanup_readback_authorizes_delete_true",
        ),
        (
            "__active_path_scan_retirement_readback_probe.toml",
            ["retirement_readback_guard_", "satisfied = true\n"],
            "toml_retirement_readback_guard_satisfied_true",
        ),
        (
            "__active_path_scan_retirement_readback_probe.yaml",
            ["claims_retirement_cleanup_", "applied: true\n"],
            "yaml_claims_retirement_cleanup_applied_true",
        ),
        (
            "__active_path_scan_generated_hosted_surface_probe.json",
            ['{"app_workbench_live_', 'rendering_complete": true}\n'],
            "json_app_workbench_live_rendering_complete_true",
        ),
        (
            "__active_path_scan_generated_hosted_surface_probe.py",
            ['PROBE = {"claims_registry_discovery_', 'live_complete": True}\n'],
            "python_claims_registry_discovery_live_complete_true",
        ),
        (
            "__active_path_scan_generated_hosted_surface_probe.py",
            ["PROBE = {'claims_default_caller_", "cutover_complete': True}\n"],
            "python_single_claims_default_caller_cutover_complete_true",
        ),
        (
            "__active_path_scan_generated_hosted_surface_probe.toml",
            ["generated_hosted_surface_", "live_ready = true\n"],
            "toml_generated_hosted_surface_live_ready_true",
        ),
        (
            "__active_path_scan_generated_hosted_surface_probe.yaml",
            ["claims_app_operator_sustained_", "consumption_complete: true\n"],
            "yaml_claims_app_operator_sustained_consumption_complete_true",
        ),
        (
            "__active_path_scan_strict_source_purity_probe.json",
            ['{"strict_source_', 'purity_complete": true}\n'],
            "json_strict_source_purity_complete_true",
        ),
        (
            "__active_path_scan_strict_source_purity_probe.py",
            ['PROBE = {"source_ref_integrity_', 'guard_satisfied": True}\n'],
            "python_source_ref_integrity_guard_satisfied_true",
        ),
        (
            "__active_path_scan_strict_source_purity_probe.py",
            ["PROBE = {'source_ref_integrity_can_", "authorize_delete': True}\n"],
            "python_single_source_ref_integrity_can_authorize_delete_true",
        ),
        (
            "__active_path_scan_strict_source_purity_probe.toml",
            ["active_path_current_role_guard_", "complete = true\n"],
            "toml_active_path_current_role_guard_complete_true",
        ),
        (
            "__active_path_scan_strict_source_purity_probe.yaml",
            ["machine_source_guard_can_claim_", "domain_ready: true\n"],
            "yaml_machine_source_guard_can_claim_domain_ready_true",
        ),
    ],
)
def test_active_path_scan_fails_closed_on_default_caller_false_ready_resurrection(
    probe_name: str,
    probe_text_parts: list[str],
    pattern_id: str,
) -> None:
    probe_path = REPO_ROOT / "contracts" / probe_name
    probe_path.write_text("".join(probe_text_parts), encoding="utf-8")
    try:
        scan = build_physical_skeleton_follow_through()[
            "active_path_current_role_guard"
        ]
    finally:
        probe_path.unlink(missing_ok=True)

    assert scan["state"] == "failed"
    assert scan["current_role_guard_passed"] is False
    assert any(
        match["path"] == f"contracts/{probe_name}"
        and match["pattern_id"] == pattern_id
        for match in scan["forbidden_role_matches"]
    )
