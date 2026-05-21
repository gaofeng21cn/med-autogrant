from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


def build_private_functional_surface_policy(
    *,
    forbidden_generic_owner_roles: list[str],
    physical_source_classification_buckets: list[str],
    physical_source_surface_classifications: list[dict[str, Any]],
    forbidden_physical_residue_classes: list[str],
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
                "sidecar",
                "runtime_registration",
                "control_plane",
                "lifecycle",
                "memory",
                "package",
                "autonomy_controller",
                "owner_receipt_helper",
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
                    "sidecar",
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
    return {
        "state": "active_caller_migration_required_before_retirement",
        "required_before_delete_or_rename": retirement_evidence_refs,
        "allowed_terminal_actions": ["delete", "rename_to_domain_handler_target", "history_tombstone"],
        "target_owner_after_migration": target_owner,
        "compatibility_alias_allowed": False,
        "no_resurrection_policy": "no_compat_alias_facade_or_generated_surface_owner_in_mag",
    }
