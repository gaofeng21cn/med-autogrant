from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.physical_morphology_guard import (
    PHYSICAL_MORPHOLOGY_GUARD_PUBLIC_READBACK_REF,
    PHYSICAL_MORPHOLOGY_SOURCE_REF_INTEGRITY_READBACK_REF,
)

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


def build_private_functional_surface_policy(
    *,
    forbidden_generic_owner_roles: list[str],
    physical_source_classification_buckets: list[str],
    physical_source_surface_classifications: list[dict[str, Any]],
    forbidden_physical_residue_classes: list[str],
    active_path_scan_policy: Mapping[str, Any],
    retirement_evidence_refs: list[str],
    target_owner_by_physical_classification: Mapping[str, str],
    active_caller_status_by_physical_classification: Mapping[str, str],
) -> dict[str, Any]:
    return {
        "surface_kind": "opl_domain_private_functional_surface_admission_policy",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "default_posture": "forbidden_until_classified_and_receipted",
        "forbidden_private_surface_classes": [
            "generic_scheduler",
            "generic_queue_or_attempt_ledger",
            "generic_cli_mcp_product_wrapper",
            "generic_workbench_shell",
            "generic_observability_runtime",
        ],
        "allowed_private_surface_classes": [
            "minimal_authority_function",
            "grant_native_helper_implementation",
            "ai_first_verdict_ref_materializer",
        ],
        "forbidden_generic_owner_roles": forbidden_generic_owner_roles,
        "purpose_first_owner_delta_domain_thinning_gate": {
            "contract_id": "mag.purpose_first_owner_delta_domain_thinning_gate.v1",
            "applies_to_surface_ids": [
                "product_entry",
                "grouped_cli_wrapper",
                "status",
                "user_loop",
                "domain_handler",
                "runtime_registration",
                "control_plane",
                "lifecycle",
            ],
            "default_operator_delta": "grant_deliverable_progress_delta_or_domain_owned_typed_blocker",
            "domain_thinning_required_before_physical_delete": [
                "external_evidence://purpose_first_domain_thinning/opl_generated_default_caller_consumes_same_refs",
                "external_evidence://purpose_first_domain_thinning/sustained_app_or_default_caller_consumption",
                "external_evidence://purpose_first_domain_thinning/direct_hosted_parity_no_regression",
                "external_evidence://purpose_first_domain_thinning/owner_receipt_or_typed_blocker_roundtrip",
                "external_evidence://purpose_first_domain_thinning/no_active_domain_repo_generic_shell_caller",
                "external_evidence://purpose_first_domain_thinning/continuous_no_forbidden_write",
                "owner_receipt://mag/physical_delete_or_tombstone_authorization",
            ],
            "forbidden_grant_readiness_substitutes": [
                "package_existence",
                "schema_completeness",
                "stage_replay_projection",
                "opl_ledger_verification",
                "provider_completion",
                "grouped_cli_success",
                "product_entry_manifest_success",
                "refs_only_accounting_closeout",
            ],
            "human_gate_blocker": {
                "blocker_id": "submission_ready_export_gate",
                "claims_export_ready": False,
                "claims_submission_ready": False,
                "owner": TARGET_DOMAIN_ID,
                "required_closeout": "human_gate_receipt_or_domain_owned_typed_blocker_update",
                "state": "blocking_human_gate",
            },
            "source_human_doc_refs": [
                "human_doc:one-person-lab/docs/active/opl-family-purpose-first-design-audit.md",
                "human_doc:med-autogrant/docs/status.md",
                "human_doc:med-autogrant/docs/active/mag-ideal-state-cross-repo-gap-plan.md",
            ],
            "valid_owner_delta_return_shapes": [
                "domain_owner_receipt_ref",
                "domain_owned_typed_blocker_ref",
                "no_regression_evidence_ref",
            ],
        },
        "physical_source_morphology_policy": {
            "surface_kind": "mag_physical_source_morphology_policy",
            "policy_id": "mag.physical_source_morphology.v1",
            "target_domain_id": TARGET_DOMAIN_ID,
            "state": "classified_no_generic_runtime_reflow",
            "classification_buckets": physical_source_classification_buckets,
            "required_surface_ids": [
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
            ],
            "surface_classifications": _physical_source_surface_classifications(
                physical_source_surface_classifications=physical_source_surface_classifications,
                target_owner_by_physical_classification=target_owner_by_physical_classification,
                active_caller_status_by_physical_classification=(
                    active_caller_status_by_physical_classification
                ),
                retirement_evidence_refs=retirement_evidence_refs,
            ),
            "forbidden_residue_classes": forbidden_physical_residue_classes,
            "active_path_scan_policy": _active_path_scan_policy(active_path_scan_policy),
            "source_ref_integrity_gate": _source_ref_integrity_gate(
                physical_source_surface_classifications
            ),
            "strict_source_purity_no_second_truth_guard": (
                _strict_source_purity_no_second_truth_guard()
            ),
            "forbidden_reflow_policy": (
                "forbid_generic_runtime_scheduler_attempt_records_executor_probe_"
                "or_compat_alias_owner_roles"
            ),
            "current_role_guard": {
                "guard_id": "mag.physical_morphology.current_role_guard.v1",
                "policy": "allow_current_roles_and_forbid_generic_owner_roles",
                "compatibility_alias_allowed": False,
                "facade_reexport_allowed": False,
                "local_journal_or_attempt_ledger_allowed": False,
                "repo_owned_scheduler_or_daemon_allowed": False,
                "generic_runtime_owner_allowed": False,
                "generated_surface_owner_in_mag_allowed": False,
                "allowed_roles": [
                    "domain_handler_target",
                    "refs_only_adapter",
                    "minimal_authority_function",
                    "repo_native_verification_wrapper",
                ],
                "forbidden_roles": [
                    "compatibility_alias",
                    "facade_reexport",
                    "repo_owned_scheduler_or_daemon",
                    "local_journal_or_attempt_ledger",
                    "generic_runtime_or_workbench_owner_claim",
                ],
            },
            "retirement_gate": {
                "gate_id": "mag.physical_morphology.retirement_gate.v1",
                "state": "active_caller_migration_evidence_required",
                "required_evidence_refs": retirement_evidence_refs,
                "delete_or_tombstone_only_after_gate": True,
                "compatibility_alias_allowed": False,
                "claims_physical_cleanup_complete": False,
            },
            "retirement_readback_cleanup_guard": _retirement_readback_cleanup_guard(
                retirement_evidence_refs
            ),
            "authority_boundary": {
                "mag_can_own_generic_runtime": False,
                "mag_can_own_generated_wrapper": False,
                "mag_can_restore_legacy_compat_alias": False,
                "mag_can_emit_local_persistence_or_attempt_records": False,
                "opl_can_write_grant_truth": False,
                "opl_can_write_memory_body": False,
                "opl_can_declare_export_ready": False,
            },
        },
    }


def _source_ref_integrity_gate(
    physical_source_surface_classifications: list[dict[str, Any]],
) -> dict[str, Any]:
    checked_refs = sorted(
        {
            str(ref)
            for surface in physical_source_surface_classifications
            for ref in surface.get("source_refs", [])
        }
    )
    return {
        "gate_id": "mag.physical_morphology.source_ref_integrity_gate.v1",
        "state": "repo_local_source_refs_declared_no_second_truth",
        "checked_source_ref_count": len(checked_refs),
        "checked_source_refs": checked_refs,
        "required_ref_shape": "repo_local_path_or_repo_local_contract_path",
        "forbidden_ref_shapes": [
            "absolute_path",
            "parent_directory_traversal",
            "uri_or_url",
            "empty_ref",
            "human_doc_ref_as_machine_source_ref",
            "legacy_alias_ref_without_contract_owner",
        ],
        "validation_policy": {
            "all_refs_must_be_repo_local": True,
            "all_refs_must_exist_in_repo_checkout": True,
            "human_doc_refs_do_not_count_as_machine_source_refs": True,
            "docs_history_refs_allowed_only_for_tombstone_or_provenance": True,
            "path_existence_can_claim_runtime_ready": False,
            "path_existence_can_authorize_physical_delete": False,
        },
        "authority_boundary": {
            "gate_can_fix_missing_refs": False,
            "gate_can_create_alias_files": False,
            "gate_can_authorize_physical_delete": False,
            "gate_can_claim_default_caller_cutover": False,
            "gate_can_claim_app_or_live_readiness": False,
            "gate_can_claim_grant_readiness": False,
            "gate_can_claim_production_ready": False,
        },
    }


def _strict_source_purity_no_second_truth_guard() -> dict[str, Any]:
    return {
        "guard_id": "mag.physical_morphology.strict_source_purity_no_second_truth_guard.v1",
        "state": "source_purity_guard_available_not_readiness_or_delete_authority",
        "guard_role": (
            "active_path_scan_and_source_ref_integrity_are_repo_machine_source_guards_"
            "not_grant_truth_or_physical_delete_authority"
        ),
        "readback_surface_refs": [
            (
                "contracts/private_functional_surface_policy.json#/"
                "physical_source_morphology_policy/active_path_scan_policy"
            ),
            (
                "contracts/private_functional_surface_policy.json#/"
                "physical_source_morphology_policy/source_ref_integrity_gate"
            ),
            PHYSICAL_MORPHOLOGY_SOURCE_REF_INTEGRITY_READBACK_REF,
        ],
        "machine_roots_guarded": [
            "src",
            "tests",
            "schemas",
            "contracts",
            "scripts",
            "plugins",
            "Makefile",
            "pyproject.toml",
            ".agents/plugins/marketplace.json",
        ],
        "allowed_outputs": [
            "forbidden_literal_match_list",
            "forbidden_path_status",
            "repo_local_source_ref_integrity_status",
            "missing_evidence_worklist",
            "owner_delta_route",
            "typed_blocker_ref_shape",
            "current_role_guard",
        ],
        "forbidden_outputs": [
            "grant_truth_write",
            "owner_receipt_signature",
            "typed_blocker_instance_creation",
            "physical_delete_operation",
            "default_caller_cutover_claim",
            "generated_hosted_live_consumption_claim",
            "grant_ready_or_submission_ready_claim",
            "production_ready_claim",
        ],
        "fail_closed_conditions": [
            "retired_active_path_exists",
            "forbidden_default_caller_literal_match",
            "source_ref_missing_or_external",
            "human_doc_ref_used_as_machine_source_ref",
            "source_purity_or_source_ref_true_flag_claims_ready_or_delete_authority",
        ],
        "authority_boundary": {
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
        },
    }


def _active_path_scan_policy(policy: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "surface_kind": str(policy["surface_kind"]),
        "policy_id": str(policy["policy_id"]),
        "target_domain_id": str(policy["target_domain_id"]),
        "state": str(policy["state"]),
        "roots": [str(item) for item in policy["roots"]],
        "files": [str(item) for item in policy["files"]],
        "suffixes": sorted(str(item) for item in policy["suffixes"]),
        "excludes_human_docs": bool(policy["excludes_human_docs"]),
        "human_doc_policy": str(policy["human_doc_policy"]),
        "scans_repo_source_only": bool(policy["scans_repo_source_only"]),
        "forbidden_active_paths": [str(item) for item in policy["forbidden_active_paths"]],
        "forbidden_role_patterns": [
            {
                "pattern_id": str(pattern["pattern_id"]),
                "literal_parts": [str(item) for item in pattern["literal_parts"]],
                "policy": str(pattern["policy"]),
            }
            for pattern in policy["forbidden_role_patterns"]
        ],
        "authority_boundary": {
            "policy_can_authorize_physical_delete": False,
            "policy_can_claim_production_long_run_soak": False,
            "policy_can_claim_grant_readiness": False,
        },
    }


def _physical_source_surface_classifications(
    *,
    physical_source_surface_classifications: list[dict[str, Any]],
    target_owner_by_physical_classification: Mapping[str, str],
    active_caller_status_by_physical_classification: Mapping[str, str],
    retirement_evidence_refs: list[str],
) -> list[dict[str, Any]]:
    return [
        _with_physical_surface_lifecycle_fields(
            surface,
            target_owner_by_physical_classification=target_owner_by_physical_classification,
            active_caller_status_by_physical_classification=(
                active_caller_status_by_physical_classification
            ),
            retirement_evidence_refs=retirement_evidence_refs,
        )
        for surface in physical_source_surface_classifications
    ]


def _retirement_readback_cleanup_guard(retirement_evidence_refs: list[str]) -> dict[str, Any]:
    compact_summary = _compact_cleanup_readiness_summary(retirement_evidence_refs)
    return {
        "guard_id": "mag.physical_morphology.retirement_readback_cleanup_guard.v1",
        "state": "readback_guard_available_physical_delete_not_authorized",
        "readback_surface_ref": PHYSICAL_MORPHOLOGY_GUARD_PUBLIC_READBACK_REF,
        "allowed_readback_outputs": [
            "source_role_classification",
            "missing_evidence_worklist",
            "owner_delta_route",
            "owner_delta_work_order_pack",
            "typed_blocker_ref_shape",
            "current_role_guard",
        ],
        "forbidden_readback_outputs": [
            "physical_delete_operation",
            "owner_receipt_signature",
            "typed_blocker_instance_creation",
            "grant_ready_or_submission_ready_claim",
            "production_ready_claim",
            "app_or_default_caller_cutover_claim",
        ],
        "required_before_cleanup_apply": [
            *retirement_evidence_refs,
            "owner_receipt://mag/physical_delete_or_tombstone_authorization",
        ],
        "compact_cleanup_readiness_summary": compact_summary,
        "false_ready_claim_guard_pattern_ids": [
            "json_retirement_readback_cleanup_complete_true",
            "python_retirement_readback_cleanup_complete_true",
            "python_single_retirement_readback_cleanup_complete_true",
            "toml_retirement_readback_cleanup_complete_true",
            "yaml_retirement_readback_cleanup_complete_true",
            "json_cleanup_readback_physical_delete_authorized_true",
            "python_cleanup_readback_physical_delete_authorized_true",
            "python_single_cleanup_readback_physical_delete_authorized_true",
            "toml_cleanup_readback_physical_delete_authorized_true",
            "yaml_cleanup_readback_physical_delete_authorized_true",
            "json_claims_cleanup_readback_authorizes_delete_true",
            "python_claims_cleanup_readback_authorizes_delete_true",
            "python_single_claims_cleanup_readback_authorizes_delete_true",
            "toml_claims_cleanup_readback_authorizes_delete_true",
            "yaml_claims_cleanup_readback_authorizes_delete_true",
        ],
        "claims": {
            "claims_retirement_cleanup_complete": False,
            "claims_physical_delete_authorized": False,
            "claims_owner_receipt_signed": False,
            "claims_typed_blocker_created": False,
            "claims_domain_ready": False,
            "claims_production_ready": False,
        },
        "authority_boundary": {
            "guard_can_identify_cleanup_candidates": True,
            "guard_can_route_owner_delta": True,
            "guard_can_authorize_physical_delete": False,
            "guard_can_sign_owner_receipt": False,
            "guard_can_create_typed_blocker": False,
            "guard_can_claim_default_caller_cutover": False,
            "guard_can_claim_app_or_live_readiness": False,
        },
    }


def _compact_cleanup_readiness_summary(retirement_evidence_refs: list[str]) -> dict[str, Any]:
    missing_evidence_refs = [
        *retirement_evidence_refs,
        "owner_receipt://mag/physical_delete_or_tombstone_authorization",
    ]
    cleanup_candidate_surface_ids: list[str] = []
    migrated_surface_ids = ["grouped_cli_wrapper"]
    retained_current_thin_surface_ids = [
        "product_entry",
        "status",
        "user_loop",
        "domain_handler",
        "control_plane",
        "lifecycle",
    ]
    non_candidate_surface_ids = [
        *migrated_surface_ids,
        *retained_current_thin_surface_ids,
    ]
    return {
        "summary_id": "mag.physical_morphology.compact_cleanup_readiness_summary.v1",
        "state": "compact_cleanup_worklist_empty_current_thin_surfaces_retained",
        "source_ref": (
            "contracts/private_functional_surface_policy.json#/"
            "physical_source_morphology_policy/retirement_readback_cleanup_guard"
        ),
        "cleanup_candidate_count": len(cleanup_candidate_surface_ids),
        "cleanup_candidate_surface_ids": cleanup_candidate_surface_ids,
        "owner_delta_required": False,
        "non_candidate_surface_ids": non_candidate_surface_ids,
        "migrated_surface_ids": migrated_surface_ids,
        "retained_current_thin_surface_ids": retained_current_thin_surface_ids,
        "non_candidate_surface_statuses": {
            "grouped_cli_wrapper": {
                "state": "migrated_no_active_compat_alias_or_facade",
                "evidence_refs": [
                    "git_commit:ef1cbd64b51f26e7cb8352035cc44bd61205b3f0",
                    "tests/product_entry_cases/test_cli_dispatch.py::"
                    "test_public_groups_are_registered_directly_without_flat_grouped_wrapper",
                    "tests/product_entry_cases/test_cli_dispatch.py::"
                    "test_flat_product_status_alias_has_no_special_compatibility_branch",
                ],
                "delete_path": [],
                "retention_policy": "covered_by_current_role_guard",
            },
            "product_entry": _retained_current_thin_surface_status(
                allowed_role="grant_handler_target_receipt_refs_and_typed_blockers",
                retention_reason=(
                    "current MAG product entry is a thin target/readback assembly surface, not "
                    "a generic product shell cleanup candidate"
                ),
                patchable_delete_path=[
                    "replace remaining active domain calls with OPL generated product entry readback",
                    "prove direct hosted parity and no forbidden writes",
                    "remove source refs only after owner receipt or typed blocker roundtrip",
                ],
            ),
            "status": _retained_current_thin_surface_status(
                allowed_role="grant_status_refs_and_typed_blocker_projection",
                retention_reason=(
                    "current status files project grant refs and typed blockers without owning a "
                    "generic status workbench"
                ),
                patchable_delete_path=[
                    "move status read-model default caller to generated surface",
                    "prove same refs and no grant readiness substitution",
                    "delete or tombstone repo status refs only after owner receipt",
                ],
            ),
            "user_loop": _retained_current_thin_surface_status(
                allowed_role="grant_user_loop_domain_action_target_and_receipt_refs",
                retention_reason=(
                    "current loop surface is an action target/ref adapter, not a scheduler or daemon"
                ),
                patchable_delete_path=[
                    "route action catalog and loop contracts through OPL generated caller",
                    "prove no repo scheduler daemon or attempt loop is introduced",
                    "remove repo-local loop adapter after owner receipt or typed blocker",
                ],
            ),
            "domain_handler": _retained_current_thin_surface_status(
                allowed_role="guarded_domain_dispatch_and_refs_projection",
                retention_reason=(
                    "current domain handler remains the MAG grant-native dispatch target and refs "
                    "projection boundary"
                ),
                patchable_delete_path=[
                    "migrate default dispatch caller to generated domain handler surface",
                    "prove guarded dispatch parity and no sidecar/workbench ownership",
                    "delete repo-local wrapper code only after owner receipt or typed blocker",
                ],
            ),
            "control_plane": _retained_current_thin_surface_status(
                allowed_role="body_free_runtime_control_refs_projection",
                retention_reason=(
                    "current control plane stores body-free refs/projections and does not own a "
                    "provider repair executor or attempt ledger"
                ),
                patchable_delete_path=[
                    "move runtime control default caller to OPL control-plane owner",
                    "prove body-free refs parity and no attempt-ledger ownership",
                    "delete repo-local adapter only after owner receipt or typed blocker",
                ],
            ),
            "lifecycle": _retained_current_thin_surface_status(
                allowed_role="cleanup_restore_retention_receipt_refs_adapter",
                retention_reason=(
                    "current lifecycle surface is an owner-receipt refs adapter, not a generic "
                    "artifact lifecycle shell"
                ),
                patchable_delete_path=[
                    "move lifecycle readback to generated delivery/lifecycle surface",
                    "prove receipt refs parity and no artifact lifecycle ownership",
                    "remove repo-local lifecycle adapter after owner receipt or typed blocker",
                ],
            ),
        },
        "required_before_cleanup_apply": missing_evidence_refs,
        "missing_evidence_refs": missing_evidence_refs,
        "owner_delta_work_order_pack": _cleanup_owner_delta_work_order_pack(
            cleanup_candidate_surface_ids=cleanup_candidate_surface_ids,
            missing_evidence_refs=missing_evidence_refs,
        ),
        "can_apply_cleanup": False,
        "can_authorize_physical_delete": False,
        "can_claim_default_caller_cutover_complete": False,
        "can_claim_app_operator_consumption": False,
        "can_claim_grant_ready": False,
        "can_claim_submission_ready": False,
        "can_claim_domain_ready": False,
        "can_claim_production_ready": False,
    }


def _retained_current_thin_surface_status(
    *,
    allowed_role: str,
    retention_reason: str,
    patchable_delete_path: list[str],
) -> dict[str, Any]:
    return {
        "state": "retained_current_thin_surface",
        "allowed_role": allowed_role,
        "retention_reason": retention_reason,
        "cleanup_candidate": False,
        "delete_path": patchable_delete_path,
        "retirement_guard": "owner_receipt_or_domain_typed_blocker_required_before_delete",
        "current_role_guard": "forbid_generic_wrapper_alias_facade_or_owner_claim",
    }


def _cleanup_owner_delta_work_order_pack(
    *,
    cleanup_candidate_surface_ids: list[str],
    missing_evidence_refs: list[str],
) -> dict[str, Any]:
    state = (
        "no_cleanup_candidates_current_thin_surfaces_retained"
        if not cleanup_candidate_surface_ids
        else "owner_delta_required_cleanup_not_authorized"
    )
    return {
        "surface_kind": "mag_cleanup_owner_delta_work_order_pack",
        "pack_id": "mag.physical_morphology.cleanup_owner_delta_work_order_pack.v1",
        "state": state,
        "target_domain_id": TARGET_DOMAIN_ID,
        "source_summary_ref": (
            "contracts/private_functional_surface_policy.json#/"
            "physical_source_morphology_policy/retirement_readback_cleanup_guard/"
            "compact_cleanup_readiness_summary"
        ),
        "cleanup_candidate_count": len(cleanup_candidate_surface_ids),
        "owner_delta_route_count": len(cleanup_candidate_surface_ids),
        "owner_delta_routes": [
            {
                "surface_id": surface_id,
                "next_owner": "med-autogrant_owner_receipt_or_typed_blocker_surface",
                "required_delta": (
                    "provide_active_caller_migration_direct_hosted_parity_no_forbidden_write_"
                    "and_physical_delete_owner_receipt_or_domain_typed_blocker_refs"
                ),
                "required_evidence_refs": list(missing_evidence_refs),
                "owner_receipt_ref_shape": (
                    f"owner_receipt://mag/{surface_id}/physical_delete_or_tombstone_authorization"
                ),
                "typed_blocker_ref_shape": (
                    f"typed_blocker://mag/physical_morphology_cleanup/{surface_id}/"
                    "requires-owner-receipt-or-evidence"
                ),
            }
            for surface_id in cleanup_candidate_surface_ids
        ],
        "authority_boundary": {
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
        },
    }


def _with_physical_surface_lifecycle_fields(
    surface: Mapping[str, Any],
    *,
    target_owner_by_physical_classification: Mapping[str, str],
    active_caller_status_by_physical_classification: Mapping[str, str],
    retirement_evidence_refs: list[str],
) -> dict[str, Any]:
    classification = str(surface["classification"])
    target_owner = target_owner_by_physical_classification[classification]
    active_caller_status = active_caller_status_by_physical_classification[classification]
    enriched = dict(surface)
    enriched["active_caller_status"] = active_caller_status
    enriched["target_owner_after_migration"] = target_owner
    enriched["retirement_gate"] = _surface_retirement_gate(
        surface_id=str(surface["surface_id"]),
        classification=classification,
        target_owner=target_owner,
        retirement_evidence_refs=retirement_evidence_refs,
    )
    return enriched


def _surface_retirement_gate(
    *,
    surface_id: str,
    classification: str,
    target_owner: str,
    retirement_evidence_refs: list[str],
) -> dict[str, Any]:
    if classification == "legacy_proof_tombstone":
        return {
            "state": "already_tombstone_no_active_caller",
            "required_before_delete_or_rename": [],
            "allowed_terminal_actions": ["keep_history_tombstone", "delete_if_no_source_ref_required"],
            "compatibility_alias_allowed": False,
            "current_role_guard": "forbid_runtime_compat_alias_or_facade_reexport",
        }
    if classification == "minimal_authority_function":
        return {
            "state": "retained_mag_authority_do_not_delete_without_replacement_receipt",
            "required_before_delete_or_rename": [
                f"owner_receipt://mag/{surface_id}/authority_replacement_or_retirement_decision",
                "direct_hosted_parity_no_regression",
                "no_forbidden_write_proof",
            ],
            "allowed_terminal_actions": [
                "retain_as_minimal_authority_function",
                "rename_only_with_owner_receipt_and_no_regression",
            ],
            "target_owner_after_migration": target_owner,
            "compatibility_alias_allowed": False,
            "current_role_guard": "forbid_mechanical_verdict_or_generic_runtime_wrapper",
        }
    if classification == "repo_native_verification_wrapper":
        return {
            "state": "retained_repo_native_verification_entry_do_not_promote_to_runtime_owner",
            "required_before_delete_or_rename": [
                "repo_hygiene_replacement_command",
                "verification_entry_no_regression",
            ],
            "allowed_terminal_actions": [
                "retain_as_repo_native_verification_wrapper",
                "delete_or_rename_only_with_repo_verification_replacement",
            ],
            "target_owner_after_migration": target_owner,
            "compatibility_alias_allowed": False,
            "current_role_guard": "forbid_runtime_session_queue_workbench_or_generated_surface_owner",
        }
    return {
        "state": "active_caller_migration_required_before_retirement",
        "required_before_delete_or_rename": retirement_evidence_refs,
        "allowed_terminal_actions": ["delete", "rename_to_domain_handler_target", "history_tombstone"],
        "target_owner_after_migration": target_owner,
        "compatibility_alias_allowed": False,
        "current_role_guard": "forbid_compat_alias_facade_or_generated_surface_owner_in_mag",
    }
