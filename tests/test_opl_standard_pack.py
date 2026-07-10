from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from med_autogrant.opl_standard_pack import build_standard_pack
from med_autogrant.opl_standard_pack_constants import GENERATED_SURFACE_OWNER
from med_autogrant.opl_standard_pack_source_policy import REQUIRED_DOMAIN_PACK_PATHS


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
ROOT_CONTRACTS = (
    "domain_descriptor",
    "foundry_agent_series",
    "action_catalog",
    "temporal_stage_run_consumption_policy",
    "stage_control_plane",
    "functional_privatization_audit",
    "private_functional_surface_policy",
    "agent_lab_handoff",
    "oma_handoff_refs",
)


def _opl_bin() -> Path:
    return Path(os.environ.get("OPL_BIN", "/Users/gaofeng/workspace/one-person-lab/bin/opl"))


def test_generated_pack_matches_contract_files_and_authority_sentinels() -> None:
    generated = build_standard_pack()
    for name in ROOT_CONTRACTS:
        assert generated[name] == json.loads(
            (REPO_ROOT / "contracts" / f"{name}.json").read_text(encoding="utf-8")
        )

    policy = generated["temporal_stage_run_consumption_policy"]
    assert policy["runtime_substrate_owner"] == GENERATED_SURFACE_OWNER
    assert policy["runtime_substrate"] == "temporal"
    assert "owner_receipt" in policy["mag_retained_authority_surfaces"]
    assert "typed_blocker_ref" in policy["accepted_domain_closing_ref_fields"]
    assert policy["stage_run_consumption_boundary"]["payload_body_allowed"] is False
    assert all(value is False for value in policy["grant_ready_completion_audit"]["claim_permissions"].values())

    handoff = generated["agent_lab_handoff"]
    assert handoff["payload_policy"] == "refs_only_no_body_material"
    forbidden = ("oma_can_write_grant_truth", "oma_can_write_memory_body", "oma_can_write_artifact_body", "oma_can_issue_owner_receipt", "oma_can_declare_quality_ready", "oma_can_declare_export_ready")
    assert not any(handoff["authority_boundary"][field] for field in forbidden)
    assert generated["oma_handoff_refs"]["standard_contract_ref"] == "contracts/agent_lab_handoff.json"
    assert generated["functional_privatization_audit"]["mag_consumer_thinning_contract"]["active_path_scan_state"] == "passed"


def test_pack_sources_and_stage_semantic_refs_resolve() -> None:
    generated = build_standard_pack()
    compiler_input = generated["pack_compiler_input"]
    assert compiler_input["canonical_semantic_pack_root"] == "agent/"
    assert compiler_input["required_domain_pack_paths"] == REQUIRED_DOMAIN_PACK_PATHS

    refs = [
        ref
        for stage in generated["stage_control_plane"]["stages"]
        for ref in stage["prompt_refs"] + stage["skills"] + stage["knowledge_refs"] + stage["evaluation"]
        if ref["ref_kind"] == "repo_path"
    ]
    for relative_path in [*REQUIRED_DOMAIN_PACK_PATHS, *(ref["ref"] for ref in refs)]:
        path = REPO_ROOT / relative_path
        assert path.exists(), relative_path
        assert path.read_text(encoding="utf-8").strip(), relative_path

    for stage in generated["stage_control_plane"]["stages"]:
        completion = stage["stage_contract"]["stage_completion_policy"]
        assert completion["provider_completion_is_domain_completion"] is False
        assert completion["authority_boundary"]["opl_can_decide_domain_completion"] is False
        assert stage["stage_production_evidence_closeout"]["authority_boundary"]["opl_can_sign_owner_receipt"] is False


def test_opl_consumers_compile_validate_and_do_not_authorize_delete() -> None:
    opl_bin = _opl_bin()
    if not opl_bin.exists():
        pytest.skip(f"OPL bin missing: {opl_bin}")

    commands = (
        (
            [str(opl_bin), "agents", "default-callers", "--agent", f"mag={REPO_ROOT}", "--json"],
            REPO_ROOT,
            "agent_default_caller_readiness",
        ),
        ([str(opl_bin), "agents", "interfaces", "--repo-dir", str(REPO_ROOT), "--json"], opl_bin.parents[1], "generated_agent_interfaces"),
        ([str(opl_bin), "agents", "scaffold", "--validate", str(REPO_ROOT), "--json"], opl_bin.parents[1], "standard_domain_agent_scaffold"),
    )
    payloads = {}
    for command, cwd, key in commands:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
        assert result.returncode == 0, result.stderr or result.stdout
        payloads[key] = json.loads(result.stdout)[key]

    readiness = payloads["agent_default_caller_readiness"]
    assert readiness["reports"][0]["deletion_gate"]["all_deletion_evidence_requirements_observed"] is True
    assert readiness["authority_boundary"]["report_can_authorize_domain_repo_physical_delete"] is False
    assert payloads["generated_agent_interfaces"]["status"] == "ready"
    assert payloads["generated_agent_interfaces"]["domain_repo_can_own_generated_surface"] is False
    validation = payloads["standard_domain_agent_scaffold"]["validation"]
    assert validation["missing_contract_files"] == []
    assert validation["authority_violations"] == []
    assert validation["agent_pack_validation"]["blockers"] == []
