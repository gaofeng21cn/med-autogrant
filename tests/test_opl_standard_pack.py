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
    assert pack_taxonomy["retired_legacy_function_id_compatibility"] is False
    assert pack_taxonomy["compatibility_alias_allowed"] is False
    assert "legacy_function_id_compatibility" not in pack_taxonomy
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
    assert all(
        surface["retired_legacy_function_id_compatibility"] is False
        and surface["compatibility_alias_allowed"] is False
        and "legacy_function_id_compatibility" not in surface
        for surface in generated["pack_compiler_input"]["minimal_authority_surface_contracts"]
    )
    assert generated["generated_surface_handoff"]["domain_repo_can_own_generated_surface"] is False
    assert _read_contract("agent_lab_handoff") == generated["agent_lab_handoff"]
    assert generated["domain_descriptor"]["standard_contract_refs"]["agent_lab_handoff"] == (
        "contracts/agent_lab_handoff.json"
    )
    assert _read_contract("oma_handoff_refs") == generated["oma_handoff_refs"]
    assert generated["domain_descriptor"]["standard_contract_refs"]["oma_handoff_refs"] == (
        "contracts/oma_handoff_refs.json"
    )
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


def test_opl_default_callers_see_mag_deletion_evidence_without_delete_authority() -> None:
    opl_bin = Path(os.environ.get("OPL_BIN", "/Users/gaofeng/workspace/one-person-lab/bin/opl"))
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
    assert readiness["summary"]["generated_default_caller_surface_count"] == 8
    assert readiness["summary"]["missing_domain_owner_receipt_or_typed_blocker_count"] == 0
    assert readiness["summary"]["missing_no_forbidden_write_proof_count"] == 0
    assert readiness["summary"]["missing_tombstone_or_provenance_ref_count"] == 0
    assert readiness["migration_gate_policy"]["physical_delete_authorized_by_this_report"] is False
    assert readiness["authority_boundary"]["report_can_authorize_domain_repo_physical_delete"] is False

    report = readiness["reports"][0]
    assert report["deletion_gate"]["physical_delete_authorized"] is False
    by_surface = {gate["surface_id"]: gate for gate in report["surface_gates"]}
    assert by_surface["mcp"]["active_caller_module_id"] == "human_workbench_scheduler_daemon"
    assert by_surface["product_status"]["active_caller_module_id"] == "domain_handler_product_status_shell"
    assert by_surface["domain_handler"]["active_caller_module_id"] == "runtime_registration"
    for gate in report["surface_gates"]:
        worklist = gate["deletion_evidence_worklist"]
        assert worklist["domain_owner_receipt_or_typed_blocker"]["status"] == "observed"
        assert worklist["no_forbidden_write_proof"]["status"] == "observed"
        assert worklist["tombstone_or_provenance_ref"]["status"] == "observed"
        assert worklist["physical_delete_authorized"] is False


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
        "grouped_cli_wrapper",
        "status",
        "user_loop",
        "domain_handler",
        "runtime_registration",
        "control_plane",
        "lifecycle",
        "memory",
        "package",
        "autonomy_controller",
        "owner_receipt_helper",
        "legacy_runtime_residue",
    ]

    classifications = {
        surface["surface_id"]: surface
        for surface in morphology["surface_classifications"]
    }
    assert set(classifications) == set(morphology["required_surface_ids"])
    assert classifications["domain_runtime"]["classification"] == "declarative_grant_handler"
    assert classifications["domain_runtime"]["source_refs"] == [
        "src/med_autogrant/domain_runtime_parts/substrate.py",
        "src/med_autogrant/domain_entry.py",
    ]
    assert classifications["domain_runtime"]["allowed_role"] == (
        "route_authority_adapter_without_facade_reexport"
    )
    assert classifications["runtime_registration"]["classification"] == "declarative_grant_handler"
    assert classifications["product_entry"]["classification"] == "refs_only_adapter"
    assert classifications["grouped_cli_wrapper"]["classification"] == "refs_only_adapter"
    assert classifications["status"]["classification"] == "refs_only_adapter"
    assert classifications["user_loop"]["classification"] == "refs_only_adapter"
    assert classifications["domain_handler"]["classification"] == "refs_only_adapter"
    assert classifications["control_plane"]["classification"] == "refs_only_adapter"
    assert classifications["lifecycle"]["classification"] == "refs_only_adapter"
    assert classifications["memory"]["classification"] == "minimal_authority_function"
    assert classifications["package"]["classification"] == "minimal_authority_function"
    assert classifications["autonomy_controller"]["classification"] == "minimal_authority_function"
    assert classifications["owner_receipt_helper"]["classification"] == "minimal_authority_function"
    assert classifications["legacy_runtime_residue"]["classification"] == "legacy_proof_tombstone"

    for forbidden in (
        "legacy_local_persistence_surface",
        "legacy_attempt_record_surface",
        "legacy_repo_cadence_owner",
        "legacy_executor_runtime_probe",
        "legacy_compat_alias_surface",
    ):
        assert forbidden in morphology["forbidden_residue_classes"]
        assert forbidden in classifications["legacy_runtime_residue"]["forbidden_roles"]

    assert (
        classifications["autonomy_controller"]["allowed_role"]
        == "grant_route_budget_blocker_policy"
    )
    assert "repo_scheduler_daemon" in classifications["autonomy_controller"]["forbidden_roles"]
    assert "generic_status_workbench_owner" in classifications["status"]["forbidden_roles"]
    assert "generic_cli_mcp_product_wrapper_owner" in classifications["grouped_cli_wrapper"]["forbidden_roles"]
    assert "generic_scheduler_owner" in classifications["user_loop"]["forbidden_roles"]
    assert "generic_domain_handler_owner" in classifications["domain_handler"]["forbidden_roles"]
    assert "generic_sidecar_owner" in classifications["domain_handler"]["forbidden_roles"]
    assert "provider_runtime_owner" in classifications["runtime_registration"]["forbidden_roles"]
    assert "generic_lifecycle_owner" in classifications["lifecycle"]["forbidden_roles"]
    assert "generic_memory_transport_owner" in classifications["memory"]["forbidden_roles"]
    assert "generic_artifact_lifecycle_owner" in classifications["package"]["forbidden_roles"]
    assert "generic_attempt_ledger_owner" in classifications["owner_receipt_helper"]["forbidden_roles"]
    assert classifications["grouped_cli_wrapper"]["active_caller_status"] == (
        "active_refs_only_adapter_until_opl_generated_caller_migration"
    )
    assert classifications["grouped_cli_wrapper"]["target_owner_after_migration"] == "one-person-lab"
    assert classifications["grouped_cli_wrapper"]["retirement_gate"]["state"] == (
        "active_caller_migration_required_before_retirement"
    )
    assert classifications["grouped_cli_wrapper"]["retirement_gate"][
        "compatibility_alias_allowed"
    ] is False
    assert classifications["owner_receipt_helper"]["active_caller_status"] == (
        "retained_mag_authority_function"
    )
    assert classifications["owner_receipt_helper"]["target_owner_after_migration"] == "med-autogrant"
    assert classifications["owner_receipt_helper"]["retirement_gate"]["state"] == (
        "retained_mag_authority_do_not_delete_without_replacement_receipt"
    )
    assert classifications["legacy_runtime_residue"]["retirement_gate"]["state"] == (
        "already_tombstone_no_active_caller"
    )
    assert morphology["retirement_gate"] == {
        "gate_id": "mag.physical_morphology.retirement_gate.v1",
        "state": "active_caller_migration_evidence_required",
        "required_evidence_refs": [
            "external_evidence://physical_morphology_hygiene/active_caller_migration_receipt",
            "external_evidence://physical_morphology_hygiene/direct_hosted_parity_no_regression",
            "external_evidence://physical_morphology_hygiene/owner_receipt_or_typed_blocker_roundtrip",
            "external_evidence://physical_morphology_hygiene/continuous_no_forbidden_write",
            "physical_morphology://no_active_compat_alias_or_facade_scan",
        ],
        "delete_or_tombstone_only_after_gate": True,
        "compatibility_alias_allowed": False,
        "claims_physical_cleanup_complete": False,
    }
    assert morphology["no_resurrection_policy"]["compatibility_alias_allowed"] is False
    assert "grouped_cli_wrapper" in morphology["no_resurrection_policy"]["applies_to_surface_ids"]
    assert (
        morphology["forbidden_reflow_policy"]
        == "do_not_restore_legacy_local_persistence_attempt_records_repo_cadence_"
        "executor_probe_or_compat_alias"
    )
    assert morphology["authority_boundary"] == {
        "mag_can_own_generic_runtime": False,
        "mag_can_own_generated_wrapper": False,
        "mag_can_restore_legacy_compat_alias": False,
        "mag_can_emit_local_persistence_or_attempt_records": False,
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


def test_agent_lab_handoff_is_standard_body_free_consumer_refs_only() -> None:
    generated = build_standard_pack()
    handoff = generated["agent_lab_handoff"]

    assert handoff["surface_kind"] == "agent_lab_handoff.v1"
    assert handoff["consumer"] == "opl-meta-agent"
    assert handoff["consumer_contract"] == "agent:evidence"
    assert handoff["payload_policy"] == "refs_only_no_body_material"
    assert handoff["authority_boundary"] == {
        "oma_can_write_grant_truth": False,
        "oma_can_write_memory_body": False,
        "oma_can_write_artifact_body": False,
        "oma_can_issue_owner_receipt": False,
        "oma_can_declare_fundability_ready": False,
        "oma_can_declare_quality_ready": False,
        "oma_can_declare_export_ready": False,
        "oma_consumes_mag_refs_only": True,
        "owner_receipt_authority_owner": "med-autogrant",
        "quality_verdict_owner": "med-autogrant",
        "artifact_authority_owner": "med-autogrant",
        "memory_authority_owner": "med-autogrant",
    }

    for forbidden in (
        "grant_truth_body",
        "grant_artifact_body",
        "memory_body",
        "proposal_text_body",
        "fundability_verdict_body",
        "authoring_quality_verdict_body",
        "submission_ready_export_verdict_body",
    ):
        assert forbidden in handoff["forbidden_payload_classes"]

    refs = handoff["handoff_refs"]
    assert set(refs) == {
        "production_acceptance",
        "agent_lab_handoff",
        "owner_route",
        "owner_receipt",
        "typed_blocker",
        "generated_surface_handoff",
        "editable_surface_hints",
        "no_forbidden_write_proof",
        "real_target_patch_loop_closeout",
    }
    assert refs["production_acceptance"]["state_ref"] == (
        "contracts/production_acceptance/mag-production-acceptance.json"
    )
    assert refs["production_acceptance"]["external_evidence_ledger_ref"] == (
        "contracts/external_evidence/mag-evidence-receipt-ledger.json"
    )
    assert refs["agent_lab_handoff"]["suite_result_shape"] == "opl_agent_lab_suite_result"
    assert refs["owner_route"]["manifest_ref"] == "/product_entry_manifest/owner_route"
    assert refs["owner_route"]["route_truth_owner"] == "med-autogrant"
    assert refs["owner_receipt"]["contract_ref"] == "contracts/owner_receipt_contract.json"
    assert refs["owner_receipt"]["authority"] == "mag_issues_owner_receipts_oma_consumes_refs_only"
    assert refs["typed_blocker"]["ledger_ref"] == "contracts/external_evidence/mag-evidence-receipt-ledger.json"
    assert "typed_blocker_ref" in refs["typed_blocker"]["accepted_return_shapes"]
    assert refs["generated_surface_handoff"]["contract_ref"] == "contracts/generated_surface_handoff.json"
    assert refs["generated_surface_handoff"]["generator_owner"] == "one-person-lab"
    assert refs["editable_surface_hints"]["editable_shared_bootstrap_ref"] == (
        "src/med_autogrant/editable_shared_bootstrap.py"
    )
    assert refs["editable_surface_hints"]["boundary"] == (
        "editable_hints_are_dependency_path_hints_not_runtime_or_artifact_authority"
    )
    assert refs["no_forbidden_write_proof"]["external_evidence_ledger_ref"] == (
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/request_closures/4"
    )
    assert refs["no_forbidden_write_proof"]["boundary"] == "proof_refs_do_not_grant_oma_write_authority"
    closeout = refs["real_target_patch_loop_closeout"]
    assert closeout["state"] == "refs_only_closeout_smoke_ready"
    assert closeout["closeout_kind"] == "ahe_real_target_scaleout_smoke"
    assert closeout["production_acceptance_ref"] == (
        "contracts/production_acceptance/mag-production-acceptance.json#/patch_loop_refs"
    )
    assert closeout["read_model_consumption_ref"] == (
        "/product_entry_manifest/production_live_acceptance_receipt"
    )
    assert set(closeout["required_closeout_ref_keys"]) == {
        "blocked_suite_result_ref",
        "developer_patch_work_order_ref",
        "patch_traceability_matrix_ref",
        "target_repo_verification_refs",
        "target_runtime_read_model_consumption_ref",
        "workspace_environment_proof_ref",
        "no_forbidden_write_proof_ref",
        "target_owner_receipt_or_typed_blocker_ref",
        "patch_absorption_ref",
        "worktree_cleanup_ref",
        "agent_lab_re_evaluation_ref",
    }
    assert set(closeout["closeout_refs"]) == set(closeout["required_closeout_ref_keys"])
    assert closeout["closeout_refs"]["developer_patch_work_order_ref"] == (
        "developer-work-order:oma/mag/ai-first-mag-patch-smoke"
    )
    assert closeout["closeout_refs"]["target_runtime_read_model_consumption_ref"] == (
        "/product_entry_manifest/production_live_acceptance_receipt"
    )
    assert closeout["closeout_refs"]["target_owner_receipt_or_typed_blocker_ref"] == (
        "receipt:mag/production-live-acceptance/2026-05-20"
    )


def test_oma_handoff_refs_points_to_standard_agent_lab_handoff() -> None:
    generated = build_standard_pack()
    wrapper = generated["oma_handoff_refs"]

    assert wrapper["surface_kind"] == "mag_oma_handoff_refs.v1"
    assert wrapper["consumer_contract"] == "agent:evidence"
    assert wrapper["standard_contract_ref"] == "contracts/agent_lab_handoff.json"
    assert wrapper["handoff_refs"] == {
        "standard_agent_lab_handoff": "contracts/agent_lab_handoff.json",
        "real_target_patch_loop_closeout": (
            "contracts/agent_lab_handoff.json#/handoff_refs/"
            "real_target_patch_loop_closeout"
        ),
    }
    assert wrapper["authority_boundary"] == generated["agent_lab_handoff"]["authority_boundary"]


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
        assert stage_contract["expected_receipt_refs"]
        assert stage_contract["monitor_freshness_refs"]
        assert stage_contract["replay_evidence_refs"]
        assert stage_contract["stage_production_evidence_refs"]
        assert any(ref["role"] == "opl_provider_stage_launch_trigger" for ref in stage_contract["trigger_refs"])
        expected_receipt = stage_contract["expected_receipt_refs"][0]
        assert expected_receipt["owner"] == "med-autogrant"
        assert expected_receipt["required_return_shapes"] == [
            "domain_owner_receipt_ref",
            "typed_blocker_ref",
            "no_regression_evidence_ref",
        ]
        assert expected_receipt["body_free_payload_required"] is True
        replay_refs_by_role = {
            ref["role"]: ref
            for ref in stage_contract["replay_evidence_refs"]
        }
        assert replay_refs_by_role["recorded_runtime_event_ref"]["ref"] == (
            expected_receipt["runtime_event_refs"][0]
        )
        assert replay_refs_by_role["stage_closeout_receipt_ref"]["ref"] == expected_receipt["ref"]
        monitor_roles = {ref["role"] for ref in stage_contract["monitor_refs"]}
        assert "stage_replay_monitor" in monitor_roles
        assert "stage_owner_receipt_handoff_monitor" in monitor_roles
        assert "live_stage_attempt_monitor" in monitor_roles
        assert "no_forbidden_write_guard_monitor" in monitor_roles
        assert "direct_hosted_parity_no_regression_monitor" in monitor_roles
        closeout = stage["stage_production_evidence_closeout"]
        assert closeout["surface_kind"] == "mag_stage_production_evidence_closeout_refs"
        assert closeout["state"] == "body_free_refs_ready_for_opl_record_preflight"
        assert closeout["expected_receipt_refs"] == stage_contract["expected_receipt_refs"]
        assert closeout["monitor_freshness_refs"] == stage_contract["monitor_freshness_refs"]
        assert closeout["authority_boundary"]["opl_can_sign_owner_receipt"] is False
        assert closeout["authority_boundary"]["opl_can_write_grant_truth"] is False
        assert closeout["authority_boundary"]["opl_can_declare_export_ready"] is False


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
