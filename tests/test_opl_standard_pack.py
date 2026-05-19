from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from med_autogrant.opl_standard_pack import build_standard_pack


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_contract(name: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / "contracts" / f"{name}.json").read_text(encoding="utf-8"))


def test_opl_standard_pack_root_contracts_match_mag_canonical_metadata() -> None:
    generated = build_standard_pack()

    assert _read_contract("domain_descriptor") == generated["domain_descriptor"]
    assert _read_contract("action_catalog") == generated["action_catalog"]
    assert _read_contract("stage_control_plane") == generated["stage_control_plane"]
    assert _read_contract("functional_privatization_audit") == generated["functional_privatization_audit"]
    assert (
        _read_contract("private_functional_surface_policy")
        == generated["private_functional_surface_policy"]
    )

    assert generated["action_catalog"]["target_domain_id"] == "med-autogrant"
    assert generated["stage_control_plane"]["target_domain_id"] == "med-autogrant"
    assert generated["pack_compiler_input"]["generated_surface_owner"] == "one-person-lab"
    pack_taxonomy = generated["pack_compiler_input"]["minimal_authority_surface_taxonomy"]
    assert pack_taxonomy["ai_first_judgment_surface_ids"] == [
        "fundability_verdict",
        "quality_verdict",
        "export_verdict",
        "memory_accept_reject",
    ]
    assert pack_taxonomy["programmatic_authority_surface_ids"] == [
        "package_authority",
        "owner_receipt_signer",
        "grant_helper",
    ]
    assert pack_taxonomy["programmatic_verdict_generation_allowed"] is False
    assert generated["pack_compiler_input"]["minimal_authority_surface_contracts"][0][
        "authority_surface_id"
    ] == "fundability_verdict"
    assert all(
        surface["programmatic_verdict_generation_allowed"] is False
        for surface in generated["pack_compiler_input"]["minimal_authority_surface_contracts"]
    )
    assert generated["generated_surface_handoff"]["domain_repo_can_own_generated_surface"] is False
    assert generated["functional_privatization_audit"]["functional_followthrough_gap_classification"][
        "mag_functional_structure_gap_count"
    ] == 0
    assert generated["functional_privatization_audit"]["functional_followthrough_gap_classification"][
        "authority_boundary"
    ]["mag_repo_functional_structure_gaps_zero"] is True
    thinning_contract = generated["functional_privatization_audit"]["mag_consumer_thinning_contract"]
    assert thinning_contract["active_path_scan_state"] == "passed"
    assert thinning_contract["guarded_by_active_path_scan_ref"] == (
        "/product_entry_manifest/physical_skeleton_follow_through/"
        "active_path_scan_no_legacy_default_caller"
    )


def test_private_functional_policy_classifies_physical_source_morphology() -> None:
    generated = build_standard_pack()
    policy = generated["private_functional_surface_policy"]
    morphology = policy["physical_source_morphology_policy"]

    assert morphology["state"] == "classified_no_generic_runtime_reflow"
    assert morphology["classification_buckets"] == [
        "declarative_grant_handler",
        "refs_only_adapter",
        "minimal_authority_function",
        "legacy_proof_tombstone",
    ]
    assert morphology["required_surface_ids"] == [
        "domain_runtime",
        "product_entry",
        "status",
        "user_loop",
        "sidecar",
        "runtime_registration",
        "control_plane",
        "lifecycle",
        "memory",
        "package",
        "autonomy_controller",
        "legacy_runtime_residue",
    ]

    classifications = {
        surface["surface_id"]: surface
        for surface in morphology["surface_classifications"]
    }
    assert set(classifications) == set(morphology["required_surface_ids"])
    assert classifications["domain_runtime"]["classification"] == "declarative_grant_handler"
    assert classifications["runtime_registration"]["classification"] == "declarative_grant_handler"
    assert classifications["product_entry"]["classification"] == "refs_only_adapter"
    assert classifications["status"]["classification"] == "refs_only_adapter"
    assert classifications["user_loop"]["classification"] == "refs_only_adapter"
    assert classifications["sidecar"]["classification"] == "refs_only_adapter"
    assert classifications["control_plane"]["classification"] == "refs_only_adapter"
    assert classifications["lifecycle"]["classification"] == "refs_only_adapter"
    assert classifications["memory"]["classification"] == "minimal_authority_function"
    assert classifications["package"]["classification"] == "minimal_authority_function"
    assert classifications["autonomy_controller"]["classification"] == "minimal_authority_function"
    assert classifications["legacy_runtime_residue"]["classification"] == "legacy_proof_tombstone"

    for forbidden in (
        "local_journal",
        "attempt_ledger",
        "repo_owned_scheduler",
        "hermes_gateway_local_manager_probe",
        "compat_facade_active_alias",
    ):
        assert forbidden in morphology["forbidden_residue_classes"]
        assert forbidden in classifications["legacy_runtime_residue"]["forbidden_roles"]

    assert (
        classifications["autonomy_controller"]["allowed_role"]
        == "grant_route_budget_blocker_policy"
    )
    assert "repo_scheduler_daemon" in classifications["autonomy_controller"]["forbidden_roles"]
    assert "generic_status_workbench_owner" in classifications["status"]["forbidden_roles"]
    assert "generic_scheduler_owner" in classifications["user_loop"]["forbidden_roles"]
    assert "generic_sidecar_owner" in classifications["sidecar"]["forbidden_roles"]
    assert "provider_runtime_owner" in classifications["runtime_registration"]["forbidden_roles"]
    assert "generic_lifecycle_owner" in classifications["lifecycle"]["forbidden_roles"]
    assert "generic_memory_transport_owner" in classifications["memory"]["forbidden_roles"]
    assert "generic_artifact_lifecycle_owner" in classifications["package"]["forbidden_roles"]
    assert (
        morphology["forbidden_reflow_policy"]
        == "do_not_restore_local_journal_attempt_ledger_repo_scheduler_"
        "hermes_gateway_local_manager_probe_or_compat_facade_active_alias"
    )
    assert morphology["authority_boundary"] == {
        "mag_can_own_generic_runtime": False,
        "mag_can_own_generated_wrapper": False,
        "mag_can_restore_compat_facade_active_alias": False,
        "mag_can_emit_local_journal_or_attempt_ledger": False,
        "opl_can_write_grant_truth": False,
        "opl_can_write_memory_body": False,
        "opl_can_declare_export_ready": False,
    }
    assert classifications["legacy_runtime_residue"]["source_refs"] == [
        "docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md"
    ]
    assert classifications["legacy_runtime_residue"]["evidence_refs"] == [
        "/product_entry_manifest/physical_skeleton_follow_through/"
        "active_path_scan_no_legacy_default_caller"
    ]


def test_opl_standard_pack_declares_real_agent_domain_pack_paths() -> None:
    generated = build_standard_pack()
    compiler_input = generated["pack_compiler_input"]
    pack_paths = compiler_input["required_domain_pack_paths"]

    assert compiler_input["canonical_semantic_pack_root"] == "agent/"
    assert compiler_input["canonical_semantic_pack_role"] == "repo_source_declarative_grant_pack"
    assert len(pack_paths) >= 20
    assert not any(path.endswith("/README.md") for path in pack_paths)
    assert any(path.startswith("agent/prompts/") for path in pack_paths)
    assert any(path.startswith("agent/stages/") for path in pack_paths)
    assert any(path.startswith("agent/skills/") for path in pack_paths)
    assert any(path.startswith("agent/quality_gates/") for path in pack_paths)
    assert any(path.startswith("agent/knowledge/") for path in pack_paths)

    forbidden_markers = ("TODO", "TBD")
    for relative_path in pack_paths:
        path = REPO_ROOT / relative_path
        assert path.exists(), relative_path
        text = path.read_text(encoding="utf-8").strip()
        assert text, relative_path
        assert not any(marker in text for marker in forbidden_markers), relative_path


def test_stage_semantic_refs_resolve_to_agent_pack_files() -> None:
    stage_plane = build_standard_pack()["stage_control_plane"]
    forbidden_markers = ("TODO", "TBD")

    required_stage_fields = set(stage_plane["discovery_smoke"]["required_stage_fields"])
    assert {
        "prompt_refs",
        "skills",
        "knowledge_refs",
        "evaluation",
    }.issubset(required_stage_fields)

    for stage in stage_plane["stages"]:
        prompt_refs = stage["prompt_refs"]
        assert prompt_refs == [
            {
                "ref_kind": "repo_path",
                "ref": f"agent/prompts/{stage['stage_id']}.md",
                "role": "stage_prompt",
            }
        ]
        skill_refs = stage["skills"]
        knowledge_refs = stage["knowledge_refs"]
        evaluation_refs = stage["evaluation"]
        stage_contract = stage["stage_contract"]

        assert skill_refs
        assert any(ref["ref_kind"] == "skill_id" and ref["ref"] == "med-autogrant" for ref in skill_refs)
        assert any(
            ref["ref_kind"] == "repo_path" and str(ref["ref"]).startswith("agent/skills/")
            for ref in skill_refs
        )
        assert knowledge_refs
        assert all(
            ref["ref_kind"] == "repo_path" and str(ref["ref"]).startswith("agent/knowledge/")
            for ref in knowledge_refs
        )
        assert evaluation_refs
        assert all(
            ref["ref_kind"] == "repo_path" and str(ref["ref"]).startswith("agent/quality_gates/")
            for ref in evaluation_refs
        )

        semantic_refs = prompt_refs + skill_refs + knowledge_refs + evaluation_refs
        for ref in semantic_refs:
            if ref["ref_kind"] != "repo_path":
                continue
            path = REPO_ROOT / ref["ref"]
            assert path.exists(), ref["ref"]
            text = path.read_text(encoding="utf-8").strip()
            assert text, ref["ref"]
            assert not any(marker in text for marker in forbidden_markers), ref["ref"]
        assert stage_contract["source_scope_refs"]
        assert stage_contract["cohort_query_refs"]
        assert stage_contract["trigger_refs"]
        assert stage_contract["monitor_refs"]
        assert stage_contract["dashboard_metric_refs"]
        assert any(ref["role"] == "opl_provider_stage_launch_trigger" for ref in stage_contract["trigger_refs"])


def test_product_entry_package_keeps_lazy_public_export() -> None:
    from med_autogrant.product_entry_parts import MedAutoGrantProductEntry

    assert MedAutoGrantProductEntry.__name__ == "MedAutoGrantProductEntry"


def test_opl_generated_interfaces_compile_mag_standard_pack() -> None:
    opl_bin = Path(os.environ.get("OPL_BIN", "/Users/gaofeng/workspace/one-person-lab/bin/opl"))
    if not opl_bin.exists():
        pytest.skip(f"OPL binary missing: {opl_bin}")
    opl_root = opl_bin.parents[1]

    result = subprocess.run(
        [str(opl_bin), "agents", "interfaces", "--repo-dir", str(REPO_ROOT), "--json"],
        cwd=opl_root,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)
    bundle = payload["generated_agent_interfaces"]

    assert bundle["source_kind"] == "standard_agent_repo_contracts"
    assert bundle["status"] == "ready"
    assert bundle["owner"] == "one-person-lab"
    assert bundle["domain_repo_can_own_generated_surface"] is False
    assert bundle["blocker_reasons"] == []
    assert bundle["cli"]["status"] == "ready"
    assert bundle["mcp"]["status"] == "ready"
    assert bundle["skill"]["status"] == "ready"
    assert bundle["product_entry"]["status"] == "ready"
    assert bundle["openai_tool"]["status"] == "ready"
    assert bundle["ai_sdk"]["status"] == "ready"
    assert {item["stage_id"] for item in bundle["stage_routes"]} == {
        stage["stage_id"] for stage in build_standard_pack()["stage_control_plane"]["stages"]
    }


def test_opl_standard_scaffold_validates_mag_pack() -> None:
    opl_bin = Path(os.environ.get("OPL_BIN", "/Users/gaofeng/workspace/one-person-lab/bin/opl"))
    if not opl_bin.exists():
        pytest.skip(f"OPL binary missing: {opl_bin}")
    opl_root = opl_bin.parents[1]

    result = subprocess.run(
        [str(opl_bin), "agents", "scaffold", "--validate", str(REPO_ROOT), "--json"],
        cwd=opl_root,
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)
    validation = payload["standard_domain_agent_scaffold"]["validation"]

    assert validation["status"] == "passed"
    assert validation["blockers"] == []
    assert validation["missing_contract_files"] == []
    assert validation["missing_forbidden_role_guards"] == []
