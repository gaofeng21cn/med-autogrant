from __future__ import annotations

import copy
import json
from pathlib import Path
from urllib.parse import urlparse

import pytest

from med_autogrant.opl_standard_pack_source_policy import (
    ACTIVE_PATH_SCAN_POLICY,
    REPO_VERIFICATION_SCRIPT_REFS,
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


def _contract_physical_source_morphology_policy() -> dict[str, object]:
    payload = json.loads((REPO_ROOT / POLICY_REF).read_text(encoding="utf-8"))
    return payload["physical_source_morphology_policy"]


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
    assert policy["state"] == "contract_owned_no_resurrection_scan_policy"
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

    for retired_path in policy["retired_active_paths"]:
        _assert_repo_local_path(retired_path)
        assert not (REPO_ROOT / retired_path).exists(), retired_path

    pattern_ids = set()
    for pattern in policy["forbidden_default_caller_patterns"]:
        pattern_ids.add(pattern["pattern_id"])
        assert pattern["pattern_id"]
        assert pattern["policy"]
        assert pattern["literal_parts"]
        assert all(isinstance(part, str) and part for part in pattern["literal_parts"])

    assert pattern_ids == {
        "domain_runtime_patch_bridge_import",
        "hermes_default_runtime_owner",
        "hermes_default_executor_owner",
        "claude_default_executor_owner",
        "gateway_default_runtime_owner",
        "local_manager_default_runtime_owner",
        "host_agent_default_runtime_owner",
        "json_hermes_default_executor",
    }


def test_repo_shell_wrappers_are_explicitly_classified_as_verification_wrappers() -> None:
    morphology = _contract_physical_source_morphology_policy()
    classifications = {
        surface["surface_id"]: surface
        for surface in morphology["surface_classifications"]
    }
    shell_wrapper_surface = classifications["repo_shell_verification_wrappers"]

    assert shell_wrapper_surface["classification"] == "repo_native_verification_wrapper"
    assert shell_wrapper_surface["allowed_role"] == (
        "repo_native_verification_hygiene_temp_env_bootstrap_quality_and_contract_check_entry"
    )
    assert shell_wrapper_surface["active_caller_status"] == "active_repo_verification_entry"
    assert shell_wrapper_surface["target_owner_after_migration"] == "repo_hygiene_boundary"
    assert shell_wrapper_surface["authority_boundary"] == {
        "can_own_generic_runtime": False,
        "can_own_generated_wrapper": False,
        "can_authorize_physical_delete": False,
        "can_claim_grant_readiness": False,
        "can_claim_production_long_run_soak": False,
    }

    active_repo_scripts = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "scripts").iterdir()
        if path.is_file() and path.suffix in {".py", ".sh"}
    )
    assert active_repo_scripts
    assert REPO_VERIFICATION_SCRIPT_REFS == active_repo_scripts
    assert shell_wrapper_surface["source_refs"] == active_repo_scripts

    active_shell_scripts = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "scripts").iterdir()
        if path.is_file() and path.suffix == ".sh"
    )
    active_python_helpers = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "scripts").iterdir()
        if path.is_file() and path.suffix == ".py"
    )
    assert active_shell_scripts
    assert active_python_helpers

    nested_repo_scripts = sorted(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (REPO_ROOT / "scripts").rglob("*")
        if path.is_file()
        and path.parent != REPO_ROOT / "scripts"
        and path.suffix in {".py", ".sh"}
    )
    assert nested_repo_scripts == []


def test_active_path_scan_uses_policy_and_fails_closed_on_injected_legacy_literal() -> None:
    current_scan = build_physical_skeleton_follow_through()[
        "active_path_scan_no_legacy_default_caller"
    ]
    policy = _contract_active_path_policy()

    assert current_scan["policy_id"] == policy["policy_id"]
    assert current_scan["scanned_scope"]["roots"] == policy["roots"]
    assert current_scan["scanned_scope"]["files"] == policy["files"]
    assert current_scan["scanned_scope"]["suffixes"] == policy["suffixes"]
    assert current_scan["state"] == "passed"
    assert current_scan["forbidden_default_caller_matches"] == []
    assert all(
        status["state"] == "absent"
        for status in current_scan["retired_surface_path_status"]
    )

    injected_policy = copy.deepcopy(policy)
    injected_policy["forbidden_default_caller_patterns"] = [
        *injected_policy["forbidden_default_caller_patterns"],
        {
            "pattern_id": "injected_policy_consumption_probe",
            "literal_parts": ["def ", "_build_active_path_scan_no_legacy_default_caller"],
            "policy": "test proves scanner consumes caller-supplied contract policy",
        },
    ]

    injected_scan = build_physical_skeleton_follow_through(
        active_path_scan_policy=injected_policy,
    )["active_path_scan_no_legacy_default_caller"]

    assert injected_scan["state"] == "failed"
    assert injected_scan["no_legacy_default_caller"] is False
    assert any(
        match["pattern_id"] == "injected_policy_consumption_probe"
        for match in injected_scan["forbidden_default_caller_matches"]
    )


def test_functional_closure_skeleton_does_not_redeclare_retired_policy_literals() -> None:
    source = (
        REPO_ROOT
        / "src"
        / "med_autogrant"
        / "product_entry_parts"
        / "functional_closure_skeleton.py"
    ).read_text(encoding="utf-8")
    policy = _contract_active_path_policy()

    assert POLICY_REF in source
    assert "active_path_scan_policy" in source

    for retired_path in policy["retired_active_paths"]:
        assert retired_path not in source

    for pattern in policy["forbidden_default_caller_patterns"]:
        forbidden_literal = "".join(pattern["literal_parts"])
        assert forbidden_literal not in source
