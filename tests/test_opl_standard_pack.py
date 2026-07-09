from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from med_autogrant.opl_standard_pack import build_standard_pack
from med_autogrant.opl_standard_pack_constants import DOMAIN_LABEL, GENERATED_SURFACE_OWNER
from med_autogrant.opl_standard_pack_source_policy import (
    GENERATED_SURFACES,
    REQUIRED_DOMAIN_PACK_PATHS,
)


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


def _read_contract(name: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / "contracts" / f"{name}.json").read_text(encoding="utf-8"))


def _opl_bin() -> Path:
    return Path(os.environ.get("OPL_BIN", "/Users/gaofeng/workspace/one-person-lab/bin/opl"))


def test_opl_standard_pack_root_contracts_match_mag_canonical_metadata() -> None:
    generated = build_standard_pack()

    for name in ROOT_CONTRACTS:
        assert _read_contract(name) == generated[name]

    assert generated["domain_descriptor"]["domain_label"] == DOMAIN_LABEL
    assert generated["domain_descriptor"]["generated_surface_owner"] == GENERATED_SURFACE_OWNER
    assert generated["action_catalog"]["target_domain_id"] == "med-autogrant"
    assert generated["stage_control_plane"]["target_domain_id"] == "med-autogrant"

    policy = generated["temporal_stage_run_consumption_policy"]
    assert policy == generated["action_catalog"]["temporal_stage_run_consumption_policy"]
    assert policy["runtime_substrate_owner"] == GENERATED_SURFACE_OWNER
    assert policy["runtime_substrate"] == "temporal"
    assert policy["domain_role"] == "refs_only_consumer_and_grant_authority"
    assert "owner_receipt" in policy["mag_retained_authority_surfaces"]
    assert "typed_blocker_ref" in policy["accepted_domain_closing_ref_fields"]
    assert policy["stage_run_consumption_boundary"]["payload_body_allowed"] is False
    ready_audit = policy["grant_ready_completion_audit"]
    assert all(
        ready_audit["claim_permissions"][field] is False
        for field in (
            "grant_ready",
            "fundability_ready",
            "quality_ready",
            "export_ready",
            "submission_ready",
        )
    )
    assert "focused_tests_passed" in ready_audit["false_completion_signals"]

    audit = generated["functional_privatization_audit"]
    assert audit["functional_followthrough_gap_classification"]["mag_functional_structure_gap_count"] == 0
    assert audit["mag_consumer_thinning_contract"]["active_path_scan_state"] == "passed"


def test_opl_default_callers_see_mag_deletion_evidence_without_delete_authority() -> None:
    opl_bin = _opl_bin()
    if not opl_bin.exists():
        pytest.skip(f"OPL bin not found: {opl_bin}")

    result = subprocess.run(
        [
            str(opl_bin),
            "agents",
            "default-callers",
            "--agent",
            f"mag={REPO_ROOT}",
            "--json",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    readiness = json.loads(result.stdout)["agent_default_caller_readiness"]
    assert readiness["status"] == "ready_domain_evidence_required"
    assert readiness["migration_gate_policy"]["physical_delete_authorized_by_this_report"] is False
    assert readiness["authority_boundary"]["report_can_authorize_domain_repo_physical_delete"] is False
    assert readiness["reports"][0]["deletion_gate"]["all_deletion_evidence_requirements_observed"] is True


def test_agent_lab_handoff_is_standard_body_free_consumer_refs_only() -> None:
    handoff = build_standard_pack()["agent_lab_handoff"]

    assert handoff["surface_kind"] == "agent_lab_handoff.v1"
    assert handoff["payload_policy"] == "refs_only_no_body_material"
    assert handoff["handoff_refs"]["production_acceptance"]["state_ref"] == (
        "contracts/production_acceptance/mag-production-acceptance.json"
    )
    assert handoff["handoff_refs"]["real_target_patch_loop_closeout"]["read_model_consumption_ref"] == (
        "/product_entry_manifest/production_live_acceptance_receipt"
    )
    assert all(
        handoff["authority_boundary"][field] is False
        for field in (
            "oma_can_write_grant_truth",
            "oma_can_write_memory_body",
            "oma_can_issue_owner_receipt",
            "oma_can_declare_quality_ready",
        )
    )
    assert "grant_truth_body" in handoff["forbidden_payload_classes"]


def test_oma_handoff_refs_points_to_standard_agent_lab_handoff() -> None:
    generated = build_standard_pack()
    wrapper = generated["oma_handoff_refs"]

    assert wrapper["surface_kind"] == "mag_oma_handoff_refs.v1"
    assert wrapper["standard_contract_ref"] == "contracts/agent_lab_handoff.json"
    assert wrapper["authority_boundary"] == generated["agent_lab_handoff"]["authority_boundary"]


def test_opl_standard_pack_declares_real_agent_domain_pack_paths() -> None:
    compiler_input = build_standard_pack()["pack_compiler_input"]
    pack_paths = compiler_input["required_domain_pack_paths"]

    assert compiler_input["canonical_semantic_pack_root"] == "agent/"
    assert pack_paths == REQUIRED_DOMAIN_PACK_PATHS
    assert len(pack_paths) >= 20
    assert any(path.startswith("agent/prompts/") for path in pack_paths)
    assert any(path.startswith("agent/quality_gates/") for path in pack_paths)
    for relative_path in pack_paths:
        path = REPO_ROOT / relative_path
        assert path.exists(), relative_path
        assert path.read_text(encoding="utf-8").strip(), relative_path


def test_stage_semantic_refs_resolve_to_agent_pack_files() -> None:
    stage_plane = build_standard_pack()["stage_control_plane"]

    for stage in stage_plane["stages"]:
        semantic_refs = stage["prompt_refs"] + stage["skills"] + stage["knowledge_refs"] + stage["evaluation"]
        repo_refs = [ref for ref in semantic_refs if ref["ref_kind"] == "repo_path"]
        assert repo_refs
        for ref in repo_refs:
            path = REPO_ROOT / ref["ref"]
            assert path.exists(), ref["ref"]
            assert path.read_text(encoding="utf-8").strip(), ref["ref"]

        completion_policy = stage["stage_contract"]["stage_completion_policy"]
        assert completion_policy["provider_completion_is_domain_completion"] is False
        assert completion_policy["opl_content_judgment_allowed"] is False
        assert "owner_receipt_ref" in completion_policy["accepted_closeout_ref_fields"]
        assert completion_policy["authority_boundary"]["opl_can_decide_domain_completion"] is False
        assert stage["stage_production_evidence_closeout"]["authority_boundary"]["opl_can_sign_owner_receipt"] is False


def test_opl_generated_interfaces_compile_mag_standard_pack() -> None:
    opl_bin = _opl_bin()
    if not opl_bin.exists():
        pytest.skip(f"OPL binary missing: {opl_bin}")

    result = subprocess.run(
        [str(opl_bin), "agents", "interfaces", "--repo-dir", str(REPO_ROOT), "--json"],
        cwd=opl_bin.parents[1],
        check=True,
        text=True,
        capture_output=True,
    )
    bundle = json.loads(result.stdout)["generated_agent_interfaces"]

    assert bundle["source_kind"] == "standard_agent_repo_contracts"
    assert bundle["status"] == "ready"
    assert bundle["domain_repo_can_own_generated_surface"] is False
    assert {item["stage_id"] for item in bundle["stage_routes"]} == {
        stage["stage_id"] for stage in build_standard_pack()["stage_control_plane"]["stages"]
    }


def test_opl_standard_scaffold_validates_mag_pack() -> None:
    opl_bin = _opl_bin()
    if not opl_bin.exists():
        pytest.skip(f"OPL binary missing: {opl_bin}")

    result = subprocess.run(
        [str(opl_bin), "agents", "scaffold", "--validate", str(REPO_ROOT), "--json"],
        cwd=opl_bin.parents[1],
        check=True,
        text=True,
        capture_output=True,
    )
    validation = json.loads(result.stdout)["standard_domain_agent_scaffold"]["validation"]

    assert validation["missing_contract_files"] == []
    assert validation["missing_forbidden_role_guards"] == []
    assert validation["authority_violations"] == []
    assert validation["agent_pack_validation"]["blockers"] == []
    assert validation["stage_ref_validation"]["blockers"] == []
