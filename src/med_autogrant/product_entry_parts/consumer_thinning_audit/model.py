from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.consumer_thinning_audit.evidence_gates import (
    build_default_caller_deletion_bridge_exit_gate,
)


def build_functional_module_audit_item(
    module_id: str,
    *,
    classification: str,
    owner: str,
    mag_role: str,
    code_paths: list[str],
    active_callers: list[str],
    active_caller_status: str,
    migration_action: str,
    retention_reason: str,
    cannot_absorb_reason: str,
    current_surface_refs: list[str],
    opl_expected_primitives: list[str],
    mag_retained_authority: list[str],
) -> dict[str, Any]:
    bridge_exit_gate = build_default_caller_deletion_bridge_exit_gate(
        module_id=module_id,
        classification=classification,
        current_surface_refs=current_surface_refs,
        mag_retained_authority=mag_retained_authority,
    )
    return {
        "module_id": module_id,
        "classification": classification,
        "owner": owner,
        "mag_role": mag_role,
        "code_paths": code_paths,
        "active_callers": active_callers,
        "active_caller_status": active_caller_status,
        "migration_action": migration_action,
        "retention_reason": retention_reason,
        "cannot_absorb_reason": cannot_absorb_reason,
        "current_surface_refs": current_surface_refs,
        "opl_expected_primitives": opl_expected_primitives,
        "mag_retained_authority": mag_retained_authority,
        "bridge_exit_gate": bridge_exit_gate,
        "implemented_as_generic_runtime_in_mag": False,
        "opl_can_write_grant_truth": False,
        "opl_can_declare_verdict": False,
    }


def build_retired_functional_module_audit_item(
    module_id: str,
    *,
    code_paths: list[str],
    active_callers: list[str],
    active_caller_status: str,
    migration_action: str,
    retention_reason: str,
    cannot_absorb_reason: str,
    evidence_refs: list[str],
    exit_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "module_id": module_id,
        "classification": "legacy_proof_tombstone",
        "owner": "none_active",
        "state": "retired_or_tombstone_only",
        "code_paths": code_paths,
        "active_callers": active_callers,
        "active_caller_status": active_caller_status,
        "migration_action": migration_action,
        "retention_reason": retention_reason,
        "cannot_absorb_reason": cannot_absorb_reason,
        "evidence_refs": evidence_refs,
        "active_caller_allowed": False,
        "compatibility_alias_allowed": False,
    }
    if exit_gate is not None:
        payload["exit_gate"] = exit_gate
    return payload
