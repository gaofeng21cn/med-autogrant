from __future__ import annotations

from typing import Any, Mapping

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
            "forbidden_reflow_policy": (
                "do_not_restore_legacy_local_persistence_attempt_records_repo_cadence_"
                "executor_probe_or_compat_alias"
            ),
            "no_resurrection_policy": {
                "policy": "do_not_restore_retired_runtime_wrapper_or_compatibility_surfaces",
                "compatibility_alias_allowed": False,
                "facade_reexport_allowed": False,
                "local_journal_or_attempt_ledger_allowed": False,
                "repo_owned_scheduler_or_daemon_allowed": False,
                "generic_runtime_owner_allowed": False,
                "generated_surface_owner_in_mag_allowed": False,
                "applies_to_surface_ids": [
                    "grouped_cli_wrapper",
                    "product_entry",
                    "domain_handler",
                    "runtime_registration",
                    "control_plane",
                    "legacy_runtime_residue",
                ],
                "forbidden_after_retirement": [
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
        "retired_active_paths": [str(item) for item in policy["retired_active_paths"]],
        "forbidden_default_caller_patterns": [
            {
                "pattern_id": str(pattern["pattern_id"]),
                "literal_parts": [str(item) for item in pattern["literal_parts"]],
                "policy": str(pattern["policy"]),
            }
            for pattern in policy["forbidden_default_caller_patterns"]
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
    return {
        "guard_id": "mag.physical_morphology.retirement_readback_cleanup_guard.v1",
        "state": "readback_guard_available_physical_delete_not_authorized",
        "readback_surface_ref": "product physical-morphology-guard",
        "allowed_readback_outputs": [
            "source_role_classification",
            "missing_evidence_worklist",
            "owner_delta_route",
            "typed_blocker_ref_shape",
            "no_resurrection_policy",
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
            "no_resurrection_policy": "no_runtime_compat_alias_or_facade_reexport",
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
            "no_resurrection_policy": "no_mechanical_verdict_or_generic_runtime_wrapper",
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
            "no_resurrection_policy": "no_runtime_session_queue_workbench_or_generated_surface_owner",
        }
    return {
        "state": "active_caller_migration_required_before_retirement",
        "required_before_delete_or_rename": retirement_evidence_refs,
        "allowed_terminal_actions": ["delete", "rename_to_domain_handler_target", "history_tombstone"],
        "target_owner_after_migration": target_owner,
        "compatibility_alias_allowed": False,
        "no_resurrection_policy": "no_compat_alias_facade_or_generated_surface_owner_in_mag",
    }
