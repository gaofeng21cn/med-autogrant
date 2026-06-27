from __future__ import annotations

from pathlib import Path

import pytest

from med_autogrant.opl_standard_pack import build_standard_pack
from med_autogrant.opl_standard_pack_constants import GENERATED_SURFACE_OWNER
from med_autogrant.opl_standard_pack_private_policy import (
    build_private_functional_surface_policy,
)
from med_autogrant.opl_standard_pack_source_policy import (
    ACTIVE_PATH_SCAN_POLICY,
    ACTIVE_CALLER_STATUS_BY_PHYSICAL_CLASSIFICATION,
    DOMAIN_READINESS_FALSE_READY_PATTERN_IDS,
    FORBIDDEN_GENERIC_OWNER_ROLES,
    FORBIDDEN_PHYSICAL_RESIDUE_CLASSES,
    GENERATED_HOSTED_SURFACE_FALSE_READY_PATTERN_IDS,
    PHYSICAL_SOURCE_CLASSIFICATION_BUCKETS,
    PHYSICAL_SOURCE_SURFACE_CLASSIFICATIONS,
    PRIVATE_WRAPPER_RETIREMENT_FALSE_READY_PATTERN_IDS,
    REPO_VERIFICATION_SCRIPT_REFS,
    RETIREMENT_EVIDENCE_REFS,
    STRICT_SOURCE_PURITY_FALSE_READY_PATTERN_IDS,
    TARGET_OWNER_BY_PHYSICAL_CLASSIFICATION,
)


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_private_functional_policy_classifies_physical_source_morphology() -> None:
    generated = build_standard_pack()
    policy = generated["private_functional_surface_policy"]
    direct_policy = build_private_functional_surface_policy(
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
    assert policy == direct_policy
    morphology = policy["physical_source_morphology_policy"]

    assert morphology["state"] == "classified_no_generic_runtime_reflow"
    assert morphology["classification_buckets"] == PHYSICAL_SOURCE_CLASSIFICATION_BUCKETS
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
        "repo_shell_verification_wrappers",
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
    assert (
        classifications["repo_shell_verification_wrappers"]["classification"]
        == "repo_native_verification_wrapper"
    )
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
    assert (
        classifications["repo_shell_verification_wrappers"]["source_refs"]
        == sorted(
            path.relative_to(REPO_ROOT).as_posix()
            for path in (REPO_ROOT / "scripts").iterdir()
            if path.is_file() and path.suffix in {".py", ".sh"}
        )
    )
    assert classifications["repo_shell_verification_wrappers"]["source_refs"] == (
        REPO_VERIFICATION_SCRIPT_REFS
    )
    assert (
        classifications["repo_shell_verification_wrappers"]["allowed_role"]
        == "repo_native_verification_hygiene_temp_env_bootstrap_quality_and_contract_check_entry"
    )
    assert (
        classifications["repo_shell_verification_wrappers"]["active_caller_status"]
        == "active_repo_verification_entry"
    )
    assert (
        classifications["repo_shell_verification_wrappers"]["target_owner_after_migration"]
        == "repo_hygiene_boundary"
    )
    assert classifications["repo_shell_verification_wrappers"]["authority_boundary"] == {
        "can_own_generic_runtime": False,
        "can_own_generated_wrapper": False,
        "can_authorize_physical_delete": False,
        "can_claim_grant_readiness": False,
        "can_claim_production_long_run_soak": False,
    }
    assert "generic_state_machine_runner_owner" in classifications[
        "repo_shell_verification_wrappers"
    ]["forbidden_roles"]
    assert classifications["repo_shell_verification_wrappers"]["retirement_gate"]["state"] == (
        "retained_repo_native_verification_entry_do_not_promote_to_runtime_owner"
    )
    assert classifications["grouped_cli_wrapper"]["active_caller_status"] == (
        "active_refs_only_adapter_until_opl_generated_caller_migration"
    )
    assert (
        classifications["grouped_cli_wrapper"]["target_owner_after_migration"]
        == GENERATED_SURFACE_OWNER
    )
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
        "required_evidence_refs": RETIREMENT_EVIDENCE_REFS,
        "delete_or_tombstone_only_after_gate": True,
        "compatibility_alias_allowed": False,
        "claims_physical_cleanup_complete": False,
    }
    readback_guard = morphology["retirement_readback_cleanup_guard"]
    assert readback_guard["guard_id"] == (
        "mag.physical_morphology.retirement_readback_cleanup_guard.v1"
    )
    assert readback_guard["state"] == (
        "readback_guard_available_physical_delete_not_authorized"
    )
    assert readback_guard["readback_surface_ref"] == "authority morphology-guard"
    assert readback_guard["required_before_cleanup_apply"] == [
        *RETIREMENT_EVIDENCE_REFS,
        "owner_receipt://mag/physical_delete_or_tombstone_authorization",
    ]
    assert "missing_evidence_worklist" in readback_guard["allowed_readback_outputs"]
    assert "owner_delta_work_order_pack" in readback_guard["allowed_readback_outputs"]
    assert "physical_delete_operation" in readback_guard["forbidden_readback_outputs"]
    assert "owner_receipt_signature" in readback_guard["forbidden_readback_outputs"]
    assert "typed_blocker_instance_creation" in readback_guard["forbidden_readback_outputs"]
    assert readback_guard["claims"] == {
        "claims_retirement_cleanup_complete": False,
        "claims_physical_delete_authorized": False,
        "claims_owner_receipt_signed": False,
        "claims_typed_blocker_created": False,
        "claims_domain_ready": False,
        "claims_production_ready": False,
    }
    compact_cleanup_summary = readback_guard["compact_cleanup_readiness_summary"]
    assert compact_cleanup_summary["summary_id"] == (
        "mag.physical_morphology.compact_cleanup_readiness_summary.v1"
    )
    assert compact_cleanup_summary["state"] == (
        "compact_cleanup_worklist_empty_current_thin_surfaces_retained"
    )
    assert compact_cleanup_summary["cleanup_candidate_count"] == 0
    assert compact_cleanup_summary["cleanup_candidate_surface_ids"] == []
    assert compact_cleanup_summary["owner_delta_required"] is False
    assert compact_cleanup_summary["migrated_surface_ids"] == ["grouped_cli_wrapper"]
    assert compact_cleanup_summary["retained_current_thin_surface_ids"] == [
        "product_entry",
        "status",
        "user_loop",
        "domain_handler",
        "control_plane",
        "lifecycle",
    ]
    assert compact_cleanup_summary["non_candidate_surface_ids"] == [
        "grouped_cli_wrapper",
        "product_entry",
        "status",
        "user_loop",
        "domain_handler",
        "control_plane",
        "lifecycle",
    ]
    non_candidate_statuses = compact_cleanup_summary["non_candidate_surface_statuses"]
    assert non_candidate_statuses["grouped_cli_wrapper"]["state"] == (
        "migrated_no_active_compat_alias_or_facade"
    )
    assert non_candidate_statuses["grouped_cli_wrapper"]["delete_path"] == []
    assert (
        non_candidate_statuses["grouped_cli_wrapper"]["retention_policy"]
        == "keep_no_resurrection_guard_do_not_recreate_wrapper_alias"
    )
    for surface_id in compact_cleanup_summary["retained_current_thin_surface_ids"]:
        assert non_candidate_statuses[surface_id]["state"] == "retained_current_thin_surface"
        assert non_candidate_statuses[surface_id]["cleanup_candidate"] is False
        assert non_candidate_statuses[surface_id]["delete_path"]
        assert non_candidate_statuses[surface_id]["retirement_guard"] == (
            "owner_receipt_or_domain_typed_blocker_required_before_delete"
        )
        assert non_candidate_statuses[surface_id]["no_resurrection_policy"] == (
            "no_generic_wrapper_alias_facade_or_owner_claim"
        )
    assert compact_cleanup_summary["can_apply_cleanup"] is False
    assert compact_cleanup_summary["can_authorize_physical_delete"] is False
    assert compact_cleanup_summary["can_claim_domain_ready"] is False
    assert compact_cleanup_summary["can_claim_production_ready"] is False
    owner_delta_work_order = compact_cleanup_summary["owner_delta_work_order_pack"]
    assert owner_delta_work_order["surface_kind"] == "mag_cleanup_owner_delta_work_order_pack"
    assert owner_delta_work_order["state"] == (
        "no_cleanup_candidates_current_thin_surfaces_retained"
    )
    assert owner_delta_work_order["cleanup_candidate_count"] == 0
    assert owner_delta_work_order["owner_delta_route_count"] == 0
    assert owner_delta_work_order["owner_delta_routes"] == []
    assert all(
        route["typed_blocker_ref_shape"].startswith(
            "typed_blocker://mag/physical_morphology_cleanup/"
        )
        for route in owner_delta_work_order["owner_delta_routes"]
    )
    assert owner_delta_work_order["authority_boundary"] == {
        "work_order_can_write_grant_truth": False,
        "work_order_can_sign_owner_receipt": False,
        "work_order_can_create_typed_blocker_instance": False,
        "work_order_can_authorize_physical_delete": False,
        "work_order_can_claim_default_caller_cutover": False,
        "work_order_can_claim_app_operator_consumption": False,
        "work_order_can_claim_grant_ready": False,
        "work_order_can_claim_submission_ready": False,
        "work_order_can_claim_domain_ready": False,
        "work_order_can_claim_production_ready": False,
    }
    assert readback_guard["authority_boundary"] == {
        "guard_can_identify_cleanup_candidates": True,
        "guard_can_route_owner_delta": True,
        "guard_can_authorize_physical_delete": False,
        "guard_can_sign_owner_receipt": False,
        "guard_can_create_typed_blocker": False,
        "guard_can_claim_default_caller_cutover": False,
        "guard_can_claim_app_or_live_readiness": False,
    }
    assert morphology["no_resurrection_policy"]["compatibility_alias_allowed"] is False
    assert "grouped_cli_wrapper" in morphology["no_resurrection_policy"]["applies_to_surface_ids"]
    assert (
        morphology["forbidden_reflow_policy"]
        == "do_not_restore_legacy_local_persistence_attempt_records_repo_cadence_"
        "executor_probe_or_compat_alias"
    )
    assert morphology["active_path_scan_policy"] == ACTIVE_PATH_SCAN_POLICY
    source_ref_integrity = morphology["source_ref_integrity_gate"]
    assert source_ref_integrity["gate_id"] == (
        "mag.physical_morphology.source_ref_integrity_gate.v1"
    )
    assert source_ref_integrity["state"] == "repo_local_source_refs_declared_no_second_truth"
    checked_refs = source_ref_integrity["checked_source_refs"]
    assert source_ref_integrity["checked_source_ref_count"] == len(checked_refs)
    assert checked_refs == sorted(
        {
            ref
            for surface in morphology["surface_classifications"]
            for ref in surface["source_refs"]
        }
    )
    for ref in checked_refs:
        assert not ref.startswith("human_doc:"), ref
        assert not Path(ref).is_absolute(), ref
        assert ".." not in Path(ref).parts, ref
        assert "://" not in ref, ref
        assert (REPO_ROOT / ref).exists(), ref
    assert source_ref_integrity["validation_policy"] == {
        "all_refs_must_be_repo_local": True,
        "all_refs_must_exist_in_repo_checkout": True,
        "human_doc_refs_do_not_count_as_machine_source_refs": True,
        "docs_history_refs_allowed_only_for_tombstone_or_provenance": True,
        "path_existence_can_claim_runtime_ready": False,
        "path_existence_can_authorize_physical_delete": False,
    }
    assert source_ref_integrity["authority_boundary"] == {
        "gate_can_fix_missing_refs": False,
        "gate_can_create_alias_files": False,
        "gate_can_authorize_physical_delete": False,
        "gate_can_claim_default_caller_cutover": False,
        "gate_can_claim_app_or_live_readiness": False,
        "gate_can_claim_grant_readiness": False,
        "gate_can_claim_production_ready": False,
    }
    strict_source_guard = morphology["strict_source_purity_no_second_truth_guard"]
    assert strict_source_guard["guard_id"] == (
        "mag.physical_morphology.strict_source_purity_no_second_truth_guard.v1"
    )
    assert strict_source_guard["state"] == (
        "source_purity_guard_available_not_readiness_or_delete_authority"
    )
    assert strict_source_guard["machine_roots_guarded"] == [
        "src",
        "tests",
        "schemas",
        "contracts",
        "scripts",
        "plugins",
        "Makefile",
        "pyproject.toml",
        ".agents/plugins/marketplace.json",
    ]
    assert "repo_local_source_ref_integrity_status" in strict_source_guard["allowed_outputs"]
    assert "physical_delete_operation" in strict_source_guard["forbidden_outputs"]
    assert strict_source_guard["authority_boundary"] == {
        "guard_can_write_grant_truth": False,
        "guard_can_create_alias_files": False,
        "guard_can_sign_owner_receipt": False,
        "guard_can_create_typed_blocker": False,
        "guard_can_authorize_physical_delete": False,
        "guard_can_claim_default_caller_cutover": False,
        "guard_can_claim_generated_hosted_live_consumption": False,
        "guard_can_claim_grant_readiness": False,
        "guard_can_claim_submission_ready": False,
        "guard_can_claim_production_ready": False,
    }
    active_path_scan_policy = morphology["active_path_scan_policy"]
    assert set(readback_guard["false_ready_claim_guard_pattern_ids"]).issubset(
        {
            pattern["pattern_id"]
            for pattern in active_path_scan_policy["forbidden_default_caller_patterns"]
        }
    )
    assert active_path_scan_policy["policy_id"] == (
        "mag.active_path_scan.no_legacy_default_caller.policy.v1"
    )
    assert active_path_scan_policy["roots"] == [
        "src",
        "tests",
        "schemas",
        "contracts",
        "scripts",
        "plugins",
    ]
    assert active_path_scan_policy["files"] == [
        "Makefile",
        "pyproject.toml",
        ".agents/plugins/marketplace.json",
    ]
    assert active_path_scan_policy["suffixes"] == [
        ".json",
        ".py",
        ".sh",
        ".toml",
        ".yaml",
        ".yml",
    ]
    assert {
        pattern["pattern_id"]
        for pattern in active_path_scan_policy["forbidden_default_caller_patterns"]
    } == {
        "domain_runtime_patch_bridge_import",
        "hermes_default_runtime_owner",
        "hermes_default_executor_owner",
        "claude_default_executor_owner",
        "gateway_default_runtime_owner",
        "local_manager_default_runtime_owner",
        "host_agent_default_runtime_owner",
        "json_hermes_default_executor",
        "json_generated_surface_owner_points_to_mag",
        "json_generated_surface_owner_points_to_mag_domain_id",
        "python_generated_surface_owner_points_to_mag",
        "python_generated_surface_owner_points_to_mag_domain_id",
        "toml_generated_surface_owner_points_to_mag",
        "toml_generated_surface_owner_points_to_mag_domain_id",
        "yaml_generated_surface_owner_points_to_mag",
        "yaml_generated_surface_owner_points_to_mag_domain_id",
        "json_generated_surface_owner_in_mag_allowed_true",
        "python_generated_surface_owner_in_mag_allowed_true",
        "toml_generated_surface_owner_in_mag_allowed_true",
        "json_domain_can_claim_generated_surface_owner_true",
        "python_domain_can_claim_generated_surface_owner_true",
        "toml_domain_can_claim_generated_surface_owner_true",
        "json_mag_can_own_generated_wrapper_true",
        "python_mag_can_own_generated_wrapper_true",
        "json_mag_claims_default_caller_cutover_complete_true",
        "python_mag_claims_default_caller_cutover_complete_true",
        "python_single_mag_claims_default_caller_cutover_complete_true",
        "toml_mag_claims_default_caller_cutover_complete_true",
        "yaml_mag_claims_default_caller_cutover_complete_true",
        "json_claims_external_default_caller_consumption_complete_true",
        "python_claims_external_default_caller_consumption_complete_true",
        "python_single_claims_external_default_caller_consumption_complete_true",
        "toml_claims_external_default_caller_consumption_complete_true",
        "yaml_claims_external_default_caller_consumption_complete_true",
        "json_claims_opl_generated_hosted_production_caller_complete_true",
        "python_claims_opl_generated_hosted_production_caller_complete_true",
        "python_single_claims_opl_generated_hosted_production_caller_complete_true",
        "toml_claims_opl_generated_hosted_production_caller_complete_true",
        "yaml_claims_opl_generated_hosted_production_caller_complete_true",
        "json_domain_repo_physical_delete_authorized_true",
        "python_domain_repo_physical_delete_authorized_true",
        "python_single_domain_repo_physical_delete_authorized_true",
        "toml_domain_repo_physical_delete_authorized_true",
        "yaml_domain_repo_physical_delete_authorized_true",
        "json_physical_delete_authorized_by_refs_true",
        "python_physical_delete_authorized_by_refs_true",
        "python_single_physical_delete_authorized_by_refs_true",
        "toml_physical_delete_authorized_by_refs_true",
        "yaml_physical_delete_authorized_by_refs_true",
        *PRIVATE_WRAPPER_RETIREMENT_FALSE_READY_PATTERN_IDS,
        *GENERATED_HOSTED_SURFACE_FALSE_READY_PATTERN_IDS,
        *DOMAIN_READINESS_FALSE_READY_PATTERN_IDS,
        *STRICT_SOURCE_PURITY_FALSE_READY_PATTERN_IDS,
    }
    assert active_path_scan_policy["authority_boundary"] == {
        "policy_can_authorize_physical_delete": False,
        "policy_can_claim_production_long_run_soak": False,
        "policy_can_claim_grant_readiness": False,
    }
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
