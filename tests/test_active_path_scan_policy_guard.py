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

    pattern_ids = [
        pattern["pattern_id"] for pattern in policy["forbidden_role_patterns"]
    ]
    assert pattern_ids
    assert len(pattern_ids) == len(set(pattern_ids))
    assert {
        "domain_runtime_patch_bridge_import",
        "json_generated_surface_owner_in_mag_allowed_true",
        "python_single_claims_external_default_caller_consumption_complete_true",
        "toml_physical_delete_authorized_by_refs_true",
    } <= set(pattern_ids)
    for pattern in policy["forbidden_role_patterns"]:
        assert pattern["policy"]
        assert pattern["literal_parts"]
        assert all(isinstance(part, str) and part for part in pattern["literal_parts"])


def test_active_path_scan_passes_current_repo_scope() -> None:
    policy = _contract_active_path_policy()
    current_scan = build_physical_skeleton_follow_through()[
        "active_path_current_role_guard"
    ]

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


def test_active_path_scan_uses_policy_and_fails_closed_on_injected_literal() -> None:
    policy = _contract_active_path_policy()
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
