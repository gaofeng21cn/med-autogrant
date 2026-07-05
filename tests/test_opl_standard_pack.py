from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from med_autogrant.opl_standard_pack import build_standard_pack
from med_autogrant.opl_standard_pack_constants import DOMAIN_LABEL, GENERATED_SURFACE_OWNER
from med_autogrant.opl_standard_pack_handoff_refs import (
    AHE_PATCH_LOOP_CLOSEOUT_REFS,
    AHE_PATCH_LOOP_REF_KEYS,
)
from med_autogrant.opl_standard_pack_profiles import (
    AGENT_MEMBERSHIP_PROJECTION_POLICY,
    DOMAIN_SPECIFIC_PROFILE,
    SERIES_DESIGN_PROFILE,
    SHARED_POLICY_RELEASE,
    STANDARD_FEEDBACK_SELF_EVOLUTION_TRIGGER_POLICY,
    STANDARD_PUBLIC_PROJECTION_POLICY,
    WORKSPACE_TOPOLOGY_PROFILE,
)
from med_autogrant.opl_standard_pack_source_policy import (
    GENERATED_SURFACES,
    REQUIRED_DOMAIN_PACK_PATHS,
)


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def _read_contract(name: str) -> dict[str, object]:
    return json.loads((REPO_ROOT / "contracts" / f"{name}.json").read_text(encoding="utf-8"))


def test_opl_standard_pack_root_contracts_match_mag_canonical_metadata() -> None:
    generated = build_standard_pack()

    _assert_root_contracts_match(generated)
    _assert_action_and_stage_domains(generated)
    _assert_foundry_agent_series_contract(generated["foundry_agent_series"])
    _assert_workspace_topology_profile(generated["foundry_agent_series"])
    _assert_adapter_thinning_policy(generated)
    _assert_pack_compiler_input(generated)
    _assert_standard_handoff_refs(generated)
    _assert_functional_privatization_audit(generated)


def _assert_root_contracts_match(generated: dict[str, object]) -> None:
    assert _read_contract("domain_descriptor") == generated["domain_descriptor"]
    assert _read_contract("foundry_agent_series") == generated["foundry_agent_series"]
    assert _read_contract("action_catalog") == generated["action_catalog"]
    assert (
        _read_contract("temporal_stage_run_consumption_policy")
        == generated["temporal_stage_run_consumption_policy"]
    )
    assert _read_contract("stage_control_plane") == generated["stage_control_plane"]
    assert _read_contract("functional_privatization_audit") == generated["functional_privatization_audit"]
    assert (
        _read_contract("private_functional_surface_policy")
        == generated["private_functional_surface_policy"]
    )


def _assert_action_and_stage_domains(generated: dict[str, object]) -> None:
    assert generated["action_catalog"]["target_domain_id"] == "med-autogrant"
    assert generated["stage_control_plane"]["target_domain_id"] == "med-autogrant"
    assert generated["domain_descriptor"]["domain_label"] == DOMAIN_LABEL
    assert generated["domain_descriptor"]["generated_surface_owner"] == GENERATED_SURFACE_OWNER
    policy = generated["action_catalog"]["temporal_stage_run_consumption_policy"]
    assert policy == generated["temporal_stage_run_consumption_policy"]
    assert policy["surface_kind"] == "temporal_stage_run_consumption_policy"
    assert policy["contract_ref"] == "contracts/temporal_stage_run_consumption_policy.json"
    assert policy["runtime_substrate_owner"] == GENERATED_SURFACE_OWNER
    assert policy["runtime_substrate"] == "temporal"
    assert policy["stage_run_substrate_owner"] == GENERATED_SURFACE_OWNER
    assert policy["stage_run_owner_surface"] == "opl_temporal_stage_run_kernel"
    assert policy["temporal_attempt_ledger_owner"] == "one-person-lab/OPL"
    assert policy["domain_role"] == "refs_only_consumer_and_grant_authority"
    assert set(policy["opl_owned_substrate_surfaces"]) >= {
        "generated_shell",
        "product_status_shell",
        "user_loop_shell",
        "direct_entry_shell",
        "domain_handler_shell",
        "operator_workbench_shell",
        "temporal_stage_run_substrate",
        "typed_queue",
        "stage_run_attempt_provenance",
        "provider_scheduler",
    }
    assert policy["mag_retained_authority_surfaces"] == [
        "grant_native_domain_entry",
        "schema_backed_authoring_contract",
        "fundability_quality_export_verdict",
        "submission_package_authority",
        "memory_accept_reject",
        "owner_receipt",
        "typed_blocker",
    ]
    assert set(policy["forbidden_mag_substrate_roles"]) >= {
        "private_runner",
        "private_queue",
        "temporal_wrapper",
        "status_shell_owner",
        "user_loop_shell_owner",
        "direct_entry_shell_owner",
        "domain_handler_shell_owner",
        "workbench_owner",
        "stage_run_attempt_provenance_owner",
        "provider_scheduler_owner",
    }
    assert policy["provider_completion_is_domain_completion"] is False
    assert policy["domain_repo_can_own_temporal_runtime"] is False
    assert policy["domain_repo_can_write_opl_stage_attempts"] is False
    assert policy["domain_repo_can_own_stage_run_substrate"] is False
    assert policy["mag_can_own_status_user_loop_direct_entry_domain_handler_or_workbench_shell"] is False
    assert policy["generated_surface_ready_can_claim_domain_ready"] is False
    assert policy["mag_writes_opl_stage_attempt_records"] is False
    assert policy["accepted_domain_closing_ref_fields"] == [
        "owner_receipt_ref",
        "typed_blocker_ref",
        "human_gate_ref",
        "route_back_ref",
    ]
    assert policy["authority_boundary"]["provider_completion_counts_as_domain_completion"] is False
    assert policy["authority_boundary"]["generated_surface_ready_counts_as_domain_ready"] is False
    assert policy["authority_boundary"]["mag_can_write_opl_stage_attempts"] is False
    assert policy["authority_boundary"]["mag_can_own_temporal_runtime"] is False
    substrate_boundary = policy["stage_run_consumption_boundary"]
    assert substrate_boundary["surface_kind"] == "mag_stage_run_consumption_boundary"
    assert substrate_boundary["consumer_role"] == "consume_opl_stage_run_refs_only"
    assert substrate_boundary["opl_substrate_owner"] == GENERATED_SURFACE_OWNER
    assert substrate_boundary["stage_run_owner_surface"] == "opl_temporal_stage_run_kernel"
    assert substrate_boundary["payload_body_allowed"] is False
    assert substrate_boundary["mag_runtime_state_write_allowed"] is False
    assert substrate_boundary["accepted_domain_closing_ref_fields"] == policy["accepted_domain_closing_ref_fields"]
    assert set(substrate_boundary["accepted_consumed_ref_fields"]) >= {
        "temporal_stage_run_ref",
        "provider_attempt_ref",
        "provider_completion_ref",
        "stage_attempt_ref",
    }
    assert substrate_boundary["authority_boundary"] == {
        "mag_can_start_temporal_worker": False,
        "mag_can_schedule_stage_run": False,
        "mag_can_write_attempt_ledger": False,
        "mag_can_own_generated_shell": False,
        "opl_can_write_grant_truth": False,
        "opl_can_sign_mag_owner_receipt": False,
        "provider_completion_counts_as_domain_completion": False,
    }
    audit = policy["grant_ready_completion_audit"]
    assert audit["surface_kind"] == "grant_ready_completion_audit"
    assert audit["state"] == "blocked_without_mag_owner_closing_ref"
    assert audit["accepted_domain_closing_ref_fields"] == policy["accepted_domain_closing_ref_fields"]
    assert audit["required_owner_evidence"]["stage_run_domain_closeout"] == (
        policy["accepted_domain_closing_ref_fields"]
    )
    assert audit["claim_permissions"] == {
        "domain_ready": False,
        "grant_ready": False,
        "fundability_ready": False,
        "quality_ready": False,
        "export_ready": False,
        "submission_ready": False,
        "production_ready": False,
    }
    assert {
        "provider_completion",
        "schema_completeness",
        "generated_surface_ready",
        "focused_tests_passed",
        "stage_replay_projection",
        "package_existence",
        "quality_scorecard_score",
    } <= set(audit["false_completion_signals"])
    assert audit["authority_boundary"]["provider_completion_counts_as_grant_ready"] is False
    assert audit["authority_boundary"]["schema_completeness_counts_as_grant_ready"] is False
    assert audit["authority_boundary"]["generated_surface_ready_counts_as_grant_ready"] is False
    assert audit["authority_boundary"]["focused_tests_count_as_grant_ready"] is False
    assert "submission_ready_human_gate_receipt" in audit["residual_live_evidence_gaps"]
    assert "temporal_provider_long_soak_window_evidence" in audit["residual_live_evidence_gaps"]


def _assert_foundry_agent_series_contract(series: dict[str, object]) -> None:
    assert series["surface_kind"] == "opl_foundry_agent_series_contract"
    assert series["version"] == "foundry-agent-series.v1"
    assert series["product_layer"] == "foundry_agent"
    assert series["domain_id"] == "medautogrant"
    assert series["stage_control_plane_target_domain_id"] == "med-autogrant"
    assert series["contract_version_policy"] == {
        "current_version": "foundry-agent-series.v1",
        "domain_contract_ref": "contracts/foundry_agent_series.json",
        "exact_version_pin_required": True,
        "compatible_version_range": ["foundry-agent-series.v1"],
        "breaking_change_requires_new_version": True,
        "domain_descriptor_must_reference_domain_contract": True,
    }
    assert series["shared_release_pin_strategy"] == {
        "owner_release_contract_ref": "contracts/family-release/shared-owner-release.json",
        "owner_commit_pin_required": True,
        "domain_dependency_pin_required": True,
        "supported_pin_sources": [
            "pyproject.toml",
            "uv.lock",
            "package.json",
            "package-lock.json",
        ],
        "consumer_alignment_check": "family:shared-release",
        "domain_contract_version_pin_does_not_authorize_domain_truth": True,
    }
    assert series["shared_policy_release"] == SHARED_POLICY_RELEASE
    assert series["agent_membership_projection_policy"] == AGENT_MEMBERSHIP_PROJECTION_POLICY
    assert series["standard_public_projection_policy"] == STANDARD_PUBLIC_PROJECTION_POLICY
    assert (
        series["standard_feedback_self_evolution_trigger_policy"]
        == STANDARD_FEEDBACK_SELF_EVOLUTION_TRIGGER_POLICY
    )
    assert series["series_design_profile"] == SERIES_DESIGN_PROFILE
    assert series["domain_specific_profile"] == DOMAIN_SPECIFIC_PROFILE
    assert "stage_completion_policy" in series["required_stage_packets"]
    assert "stage_completion_policy" in series["series_design_profile"]["stage_pack_sections"]


def _assert_workspace_topology_profile(series: dict[str, object]) -> None:
    workspace_topology = series["workspace_topology_profile"]
    assert workspace_topology == WORKSPACE_TOPOLOGY_PROFILE
    assert workspace_topology["surface_kind"] == "opl_workspace_topology_profile"
    assert workspace_topology["profile_id"] == "opl.workspace_topology_profile.v1"
    assert workspace_topology["default_profiles"]["one_off"][
        "project_collection_path"
    ] == "projects"
    assert workspace_topology["default_profiles"]["rca_series"][
        "project_collection_path"
    ] == "projects"
    assert workspace_topology["default_profiles"]["mas_portfolio"][
        "project_collection_path"
    ] == "projects"
    assert workspace_topology["workspace_initialization_policy"][
        "default_project_collection_path"
    ] == "projects"
    assert workspace_topology["workspace_initialization_policy"][
        "legacy_project_collection_aliases"
    ] == ["deliverables", "studies"]
    assert "one_off_still_uses_project_collection_path" not in workspace_topology[
        "workspace_initialization_policy"
    ]


def _assert_adapter_thinning_policy(generated: dict[str, object]) -> None:
    assert generated["domain_descriptor"]["standard_contract_refs"][
        "foundry_agent_series_policy_release"
    ] == "contracts/opl-framework/foundry-agent-series-policy-release.json"
    assert generated["foundry_agent_series"]["domain_adapter_policy"]["no_parallel_progress_schema"] is True
    thinning = generated["foundry_agent_series"]["purpose_first_adapter_thinning_policy"]
    assert thinning["default_retained_surface_roles"] == [
        "refs_only_adapter",
        "domain_handler_target",
        "minimal_authority_function",
        "migration_input",
        "history_or_tombstone_provenance",
    ]
    assert thinning["default_operator_delta_shape"] == (
        "grant_deliverable_progress_delta_or_mag_owned_typed_blocker"
    )
    assert thinning["physical_delete_required_gates"] == [
        "replacement_parity",
        "no_active_caller",
        "owner_receipt_or_typed_blocker",
        "no_forbidden_write",
        "tombstone_or_provenance",
    ]
    assert (
        thinning["evidence_tail_boundary"][
            "submission_ready_export_gate_closeout_requires"
        ]
        == "human_gate_receipt_or_mag_owned_typed_blocker"
    )
    assert thinning["evidence_tail_boundary"]["provider_completion_is_submission_ready"] is False
    assert (
        generated["foundry_agent_series"]["app_projection_policy"][
            "app_consumes_shared_progress_projection_only"
        ]
        is True
    )


def _assert_pack_compiler_input(generated: dict[str, object]) -> None:
    assert generated["pack_compiler_input"]["generated_surface_owner"] == GENERATED_SURFACE_OWNER
    pack_taxonomy = generated["pack_compiler_input"]["minimal_authority_surface_taxonomy"]
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
        surface["compatibility_alias_allowed"] is False
        and "legacy_function_id_compatibility" not in surface
        for surface in generated["pack_compiler_input"]["minimal_authority_surface_contracts"]
    )


def _assert_standard_handoff_refs(generated: dict[str, object]) -> None:
    assert generated["generated_surface_handoff"]["domain_repo_can_own_generated_surface"] is False
    handoff_policy = generated["generated_surface_handoff"]["temporal_stage_run_consumption_policy"]
    assert handoff_policy == generated["action_catalog"]["temporal_stage_run_consumption_policy"]
    assert handoff_policy == generated["temporal_stage_run_consumption_policy"]
    do_not_write = generated["generated_surface_handoff"]["consumption_boundary"][
        "opl_generated_surfaces_do_not_write"
    ]
    assert "opl_stage_attempt_records" in do_not_write
    assert "temporal_attempt_ledger" in do_not_write
    assert [
        surface["surface_id"] for surface in generated["generated_surface_handoff"]["generated_surfaces"]
    ] == GENERATED_SURFACES
    assert _read_contract("agent_lab_handoff") == generated["agent_lab_handoff"]
    assert generated["domain_descriptor"]["standard_contract_refs"]["agent_lab_handoff"] == (
        "contracts/agent_lab_handoff.json"
    )
    assert _read_contract("oma_handoff_refs") == generated["oma_handoff_refs"]
    assert generated["domain_descriptor"]["standard_contract_refs"]["oma_handoff_refs"] == (
        "contracts/oma_handoff_refs.json"
    )


def _assert_functional_privatization_audit(generated: dict[str, object]) -> None:
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
        "active_path_current_role_guard"
    )
    audit = generated["functional_privatization_audit"]["privatized_functional_module_audit"]
    assert audit["no_active_caller_evidence_summary"][
        "status"
    ] == "all_retired_surfaces_no_active_caller_observed"
    assert audit["no_active_caller_evidence_summary"][
        "no_active_caller_observed_count"
    ] == 6
    assert audit["private_platform_retirement_owner_evidence"][
        "physical_delete_authorized"
    ] is False


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
    assert report["closed_surface_detail_policy"] == (
        "closed_retirement_gate_details_omitted_from_default_payload"
    )
    assert report["summary"]["surface_retirement_gate_count"] == 8
    assert report["summary"]["closed_surface_retirement_gate_count"] == 8
    deletion_gate = report["deletion_gate"]
    assert deletion_gate["all_deletion_evidence_requirements_observed"] is True
    assert deletion_gate["generated_default_caller_readiness_can_authorize_physical_delete"] is False
    assert deletion_gate["evidence_worklist_count"] == 0
    assert deletion_gate["missing_domain_owner_receipt_or_typed_blocker_count"] == 0
    assert deletion_gate["missing_no_forbidden_write_proof_count"] == 0
    assert deletion_gate["missing_tombstone_or_provenance_ref_count"] == 0
    assert "domain_ready" in deletion_gate["not_authorized_claims"]


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
    assert refs["generated_surface_handoff"]["generator_owner"] == GENERATED_SURFACE_OWNER
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
    trigger = handoff["feedback_self_evolution_trigger"]
    assert trigger["surface_kind"] == "opl_foundry_agent_feedback_self_evolution_trigger"
    assert trigger["policy_ref"] == (
        "contracts/foundry_agent_series.json#/standard_feedback_self_evolution_trigger_policy"
    )
    assert trigger["policy_id"] == "standard_agent_feedback_self_evolution_trigger.v1"
    assert trigger["target_agent_id"] == "medautogrant"
    assert trigger["adapter_kind"] == "domain_thin_feedback_adapter"
    assert trigger["feedbackops_event_kind"] == "target_agent_feedback_external_suite"
    assert trigger["external_suite_ref"] == (
        "contracts/agent_lab_handoff.json#/handoff_refs/agent_lab_handoff"
    )
    assert trigger["developer_mode_execution_gate_refs"] == [
        "opl-developer-mode:repo-fix-execution",
        "opl-developer-mode:direct-fix-or-fork-pr-route",
    ]
    assert trigger["owner_closeout_readback_refs"] == [
        "contracts/production_acceptance/mag-production-acceptance.json#/closure_evidence",
        "contracts/owner_receipt_contract.json",
        "contracts/external_evidence/mag-evidence-receipt-ledger.json",
    ]
    assert trigger["authority_boundary"] == {
        "refs_only": True,
        "can_write_domain_truth": False,
        "can_mutate_artifact_body": False,
        "can_authorize_quality_or_export": False,
        "can_create_owner_receipt": False,
        "can_create_typed_blocker": False,
        "can_execute_repo_patch_without_developer_mode": False,
    }
    assert closeout["read_model_consumption_ref"] == (
        "/product_entry_manifest/production_live_acceptance_receipt"
    )
    assert closeout["required_closeout_ref_keys"] == AHE_PATCH_LOOP_REF_KEYS
    assert set(closeout["closeout_refs"]) == set(closeout["required_closeout_ref_keys"])
    assert closeout["closeout_refs"]["developer_patch_work_order_ref"] == (
        AHE_PATCH_LOOP_CLOSEOUT_REFS["developer_patch_work_order_ref"]
    )
    assert closeout["closeout_refs"]["target_runtime_read_model_consumption_ref"] == (
        AHE_PATCH_LOOP_CLOSEOUT_REFS["target_runtime_read_model_consumption_ref"]
    )
    assert closeout["closeout_refs"]["target_owner_receipt_or_typed_blocker_ref"] == (
        AHE_PATCH_LOOP_CLOSEOUT_REFS["target_owner_receipt_or_typed_blocker_ref"]
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
    assert pack_paths == REQUIRED_DOMAIN_PACK_PATHS
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
        completion_policy = stage_contract["stage_completion_policy"]
        assert completion_policy["surface_kind"] == "domain_stage_completion_policy"
        assert completion_policy["version"] == "domain-stage-completion-policy.v1"
        assert completion_policy["completion_judgment_owner"] == "domain_stage"
        assert completion_policy["closeout_packet_required"] is True
        assert completion_policy["provider_completion_is_domain_completion"] is False
        assert completion_policy["opl_content_judgment_allowed"] is False
        assert completion_policy["next_stage_transition_owner"] == "opl_runtime"
        assert set(completion_policy["required_closeout_outcomes"]) >= {
            "completed_and_continue",
            "completed_and_wait_owner",
            "route_back",
            "blocked",
            "rejected",
        }
        assert set(completion_policy["accepted_closeout_ref_fields"]) >= {
            "owner_receipt_ref",
            "typed_blocker_ref",
            "human_gate_ref",
            "route_back_ref",
        }
        assert completion_policy["authority_boundary"] == {
            "opl_can_decide_domain_completion": False,
            "provider_completion_counts_as_stage_complete": False,
            "file_presence_counts_as_stage_complete": False,
            "suite_pass_counts_as_stage_complete": False,
            "conformance_pass_counts_as_stage_complete": False,
        }
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


def test_product_entry_canonical_module_keeps_public_export() -> None:
    from med_autogrant.product_entry import MedAutoGrantProductEntry

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

    assert validation["missing_contract_files"] == []
    assert validation["missing_forbidden_role_guards"] == []
    assert validation["authority_violations"] == []
    assert validation["agent_pack_validation"]["blockers"] == []
    assert validation["stage_ref_validation"]["blockers"] == []

    stage_completion_blockers = [
        blocker
        for blocker in validation["blockers"]
        if "stage_completion_policy" in blocker
    ]
    assert stage_completion_blockers == []
