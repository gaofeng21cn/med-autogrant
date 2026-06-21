from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any, Mapping
from urllib.parse import urlparse

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
)
from med_autogrant.workspace_types import WorkspaceStateError


PHYSICAL_MORPHOLOGY_GUARD_PROJECTION_KIND = "mag_physical_morphology_guard_projection"

ALLOWED_PHYSICAL_MORPHOLOGY_ROLES = (
    "declarative_pack_surface",
    "domain_handler_target",
    "refs_only_adapter",
    "minimal_authority_function",
    "native_helper",
    "diagnostic",
    "legacy_proof_tombstone",
)

_MISSING_EXTERNAL_EVIDENCE_REFS = (
    "external_evidence://physical_morphology_hygiene/active_caller_migration_receipt",
    "external_evidence://physical_morphology_hygiene/direct_hosted_parity_no_regression",
    "external_evidence://physical_morphology_hygiene/owner_receipt_or_typed_blocker_roundtrip",
    "external_evidence://physical_morphology_hygiene/continuous_no_forbidden_write",
)
_PHYSICAL_DELETE_OWNER_RECEIPT_REF = (
    "owner_receipt://mag/physical_delete_or_tombstone_authorization"
)

_REQUIRED_EXTERNAL_EVIDENCE_REF_MARKERS = (
    ("active_caller_migration", ("active-caller-migration", "active_caller_migration")),
    ("direct_hosted_parity", ("direct-hosted-parity", "direct_hosted_parity")),
    ("owner_receipt_roundtrip", ("owner-receipt", "owner_receipt", "typed-blocker", "typed_blocker")),
    ("continuous_no_forbidden_write", ("no-forbidden-write", "no_forbidden_write")),
)


def build_physical_morphology_guard_projection(
    *,
    source_items: list[Mapping[str, Any]],
    external_evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    items = _project_source_items(source_items)
    explicit_external_refs = _read_ref_list(
        external_evidence_refs or [],
        context="external_evidence_refs",
    )
    allowed_items = [item for item in items if item["allowed"]]
    blocked_items = [item for item in items if not item["allowed"]]
    item_evidence_gated = [
        item for item in items if not item["evidence_refs"]
    ]
    source_ref_integrity = _source_ref_integrity_guard(items)
    required_next_evidence_refs = _dedupe(
        [
            ref
            for item in items
            for ref in item["required_next_evidence_refs"]
        ]
    )
    missing_external_evidence_refs = _missing_external_evidence_refs(explicit_external_refs)
    required_next_evidence_refs = _dedupe(
        required_next_evidence_refs + missing_external_evidence_refs
    )

    claims_ready_for_owner_receipted_cleanup = (
        not blocked_items
        and not item_evidence_gated
        and not missing_external_evidence_refs
        and source_ref_integrity["state"] == "passed"
    )
    state = _projection_state(
        blocked_count=len(blocked_items),
        evidence_gated_count=len(item_evidence_gated),
        external_evidence_refs_complete=not missing_external_evidence_refs,
        source_ref_integrity_passed=source_ref_integrity["state"] == "passed",
    )

    return {
        "surface_kind": PHYSICAL_MORPHOLOGY_GUARD_PROJECTION_KIND,
        "version": "v1",
        "state": state,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "projection_role": "repo_local_physical_morphology_refs_role_guard",
        "allowed_roles": list(ALLOWED_PHYSICAL_MORPHOLOGY_ROLES),
        "summary": {
            "source_item_count": len(items),
            "allowed_count": len(allowed_items),
            "blocked_count": len(blocked_items),
            "evidence_gated_item_count": len(item_evidence_gated),
            "external_evidence_ref_count": len(explicit_external_refs),
        },
        "allowed_count": len(allowed_items),
        "blocked_count": len(blocked_items),
        "allowed_items": allowed_items,
        "blocked_items": blocked_items,
        "external_evidence_refs": explicit_external_refs,
        "missing_external_evidence_refs": missing_external_evidence_refs,
        "required_next_evidence_refs": required_next_evidence_refs,
        "source_ref_integrity_guard": source_ref_integrity,
        "claims": {
            "claims_physical_morphology_cleanup_complete": False,
            "claims_ready_for_owner_receipted_cleanup": claims_ready_for_owner_receipted_cleanup,
            "claims_generic_runtime_owner": False,
            "claims_app_workbench_owner": False,
            "claims_scheduler_daemon_owner": False,
            "claims_attempt_ledger_owner": False,
            "claims_local_journal_owner": False,
            "claims_compatibility_alias_owner": False,
        },
        "authority_boundary": {
            "mag_role": "physical_morphology_read_guard_projection",
            "projection_scope": "source_path_module_role_evidence_refs_only",
            "mag_implements_opl_runtime": False,
            "mag_implements_app_workbench": False,
            "mag_implements_scheduler_daemon": False,
            "mag_implements_attempt_ledger": False,
            "mag_implements_local_journal": False,
            "mag_restores_compatibility_alias": False,
            "can_declare_physical_cleanup_complete": False,
            "can_declare_ready_for_owner_receipted_cleanup": claims_ready_for_owner_receipted_cleanup,
            "source_ref_integrity_can_claim_runtime_ready": False,
            "source_ref_integrity_can_authorize_physical_delete": False,
        },
        "retirement_gate": {
            "gate_id": "mag.physical_morphology.retirement_gate.v1",
            "state": _retirement_gate_state(
                blocked_count=len(blocked_items),
                evidence_gated_count=len(item_evidence_gated),
                missing_external_evidence_refs=missing_external_evidence_refs,
            ),
            "required_evidence_refs": required_next_evidence_refs,
            "delete_or_tombstone_only_after_gate": True,
            "compatibility_alias_allowed": False,
            "owner_receipt_or_typed_blocker_roundtrip_required": True,
            "no_resurrection_policy": (
                "no_compat_alias_facade_local_journal_attempt_ledger_scheduler_"
                "or_generated_surface_owner_in_mag"
            ),
        },
        "retirement_readback_cleanup_guard": _retirement_readback_cleanup_guard(
            required_next_evidence_refs=required_next_evidence_refs,
        ),
        "no_resurrection_policy": {
            "compatibility_alias_allowed": False,
            "facade_reexport_allowed": False,
            "local_journal_or_attempt_ledger_allowed": False,
            "repo_owned_scheduler_or_daemon_allowed": False,
            "generic_runtime_owner_allowed": False,
            "generated_surface_owner_in_mag_allowed": False,
        },
        "projection_policy": (
            "refs_and_role_projection_only_no_runtime_no_workbench_no_scheduler_"
            "no_lifecycle_owner_no_compat_alias"
        ),
    }


def _project_source_items(source_items: Any) -> list[dict[str, Any]]:
    if not isinstance(source_items, list):
        raise WorkspaceStateError("source_items 必须是 list of object。")
    if not source_items:
        raise WorkspaceStateError("source_items 至少需要一条 source item。")

    projected: list[dict[str, Any]] = []
    for index, item in enumerate(source_items):
        if not isinstance(item, Mapping):
            raise WorkspaceStateError(f"source_items[{index}] 必须是 object。")
        projected.append(_project_source_item(item, index=index))
    return projected


def _project_source_item(item: Mapping[str, Any], *, index: int) -> dict[str, Any]:
    context = f"source_items[{index}]"
    path = _require_nonempty_string(item.get("path"), field_name="path", context=context)
    module_id = _require_nonempty_string(
        item.get("module_id"),
        field_name="module_id",
        context=context,
    )
    declared_role = _require_nonempty_string(
        item.get("declared_role"),
        field_name="declared_role",
        context=context,
    )
    evidence_refs = _read_ref_list(item.get("evidence_refs"), context=f"{context}.evidence_refs")
    forbidden_role_flags = _read_forbidden_role_flags(
        item.get("forbidden_role_flags"),
        context=f"{context}.forbidden_role_flags",
    )
    true_forbidden_flags = [
        flag for flag, enabled in forbidden_role_flags.items() if enabled
    ]

    blocker_reasons: list[dict[str, Any]] = []
    required_next_evidence_refs: list[str] = []
    if declared_role not in ALLOWED_PHYSICAL_MORPHOLOGY_ROLES:
        blocker_reasons.append(
            {
                "reason": "declared_role_not_allowed",
                "declared_role": declared_role,
                "allowed_roles": list(ALLOWED_PHYSICAL_MORPHOLOGY_ROLES),
            }
        )
        required_next_evidence_refs.append(
            f"physical_morphology://items/{module_id}/role_classification_receipt"
        )
    if true_forbidden_flags:
        blocker_reasons.append(
            {
                "reason": "forbidden_role_flag_true",
                "forbidden_true_flags": true_forbidden_flags,
            }
        )
        required_next_evidence_refs.append(
            f"physical_morphology://items/{module_id}/no_forbidden_role_write_proof"
        )
    if not evidence_refs:
        required_next_evidence_refs.append(
            f"physical_morphology://items/{module_id}/role_evidence_ref"
        )

    allowed = not blocker_reasons
    deletion_readiness = _deletion_readiness(
        module_id=module_id,
        blocked_by_surface_gate=not allowed,
        item_required_refs=required_next_evidence_refs,
    )
    return {
        "path": path,
        "module_id": module_id,
        "declared_role": declared_role,
        "allowed": allowed,
        "evidence_refs": evidence_refs,
        "forbidden_role_flags": forbidden_role_flags,
        "true_forbidden_flags": true_forbidden_flags,
        "blocker_reasons": blocker_reasons,
        "required_next_evidence_refs": _dedupe(required_next_evidence_refs),
        "deletion_readiness": deletion_readiness,
    }


def _source_ref_integrity_guard(items: list[dict[str, Any]]) -> dict[str, Any]:
    invalid_refs = [
        {
            "path": item["path"],
            "module_id": item["module_id"],
            "reason": reason,
        }
        for item in items
        for reason in _source_ref_integrity_violations(item["path"])
    ]
    state = "failed" if invalid_refs else "passed"
    return {
        "guard_id": "mag.physical_morphology.source_ref_integrity_guard.v1",
        "state": state,
        "checked_source_ref_count": len(items),
        "invalid_source_refs": invalid_refs,
        "required_ref_shape": "repo_local_relative_path",
        "forbidden_ref_shapes": [
            "absolute_path",
            "parent_directory_traversal",
            "uri_or_url",
            "empty_ref",
            "human_doc_ref_as_machine_source_ref",
        ],
        "authority_boundary": {
            "guard_can_create_missing_refs": False,
            "guard_can_create_alias_files": False,
            "guard_can_authorize_physical_delete": False,
            "guard_can_claim_default_caller_cutover": False,
            "guard_can_claim_app_or_live_readiness": False,
            "guard_can_claim_grant_readiness": False,
            "guard_can_claim_production_ready": False,
        },
    }


def _source_ref_integrity_violations(path: str) -> list[str]:
    violations: list[str] = []
    parsed = urlparse(path)
    if parsed.scheme:
        violations.append("uri_or_url")
    candidate = PurePosixPath(path)
    if candidate.is_absolute():
        violations.append("absolute_path")
    if not candidate.parts:
        violations.append("empty_ref")
    if ".." in candidate.parts:
        violations.append("parent_directory_traversal")
    if path.startswith("human_doc:"):
        violations.append("human_doc_ref_as_machine_source_ref")
    return violations


def _deletion_readiness(
    *,
    module_id: str,
    blocked_by_surface_gate: bool,
    item_required_refs: list[str],
) -> dict[str, Any]:
    missing_retirement_evidence_refs = _dedupe(
        list(item_required_refs)
        + list(_MISSING_EXTERNAL_EVIDENCE_REFS)
        + [_PHYSICAL_DELETE_OWNER_RECEIPT_REF]
    )
    return {
        "surface_id": module_id,
        "state": "blocked_by_surface_evidence_or_owner_receipt",
        "physical_delete_authorized": False,
        "owner_receipt_required_ref": _PHYSICAL_DELETE_OWNER_RECEIPT_REF,
        "typed_blocker_allowed_ref": (
            f"typed_blocker://mag/physical_delete_or_tombstone/{module_id}"
        ),
        "missing_retirement_evidence_refs": missing_retirement_evidence_refs,
        "next_owner_delta_required": (
            "mag_owner_physical_delete_receipt_or_domain_owned_typed_blocker_required"
        ),
        "delete_or_tombstone_only_after_gate": True,
        "blocked_by_surface_gate": blocked_by_surface_gate,
        "claims_grant_ready": False,
        "claims_submission_ready": False,
        "claims_production_ready": False,
    }


def _retirement_readback_cleanup_guard(
    *,
    required_next_evidence_refs: list[str],
) -> dict[str, Any]:
    return {
        "guard_id": "mag.physical_morphology.retirement_readback_cleanup_guard.v1",
        "state": "readback_guard_available_physical_delete_not_authorized",
        "readback_can_identify_cleanup_candidates": True,
        "readback_can_route_owner_delta": True,
        "readback_can_authorize_physical_delete": False,
        "readback_can_sign_owner_receipt": False,
        "readback_can_create_typed_blocker": False,
        "allowed_outputs": [
            "source_role_classification",
            "missing_evidence_worklist",
            "owner_delta_route",
            "typed_blocker_ref_shape",
            "no_resurrection_policy",
        ],
        "forbidden_outputs": [
            "physical_delete_operation",
            "owner_receipt_signature",
            "typed_blocker_instance_creation",
            "grant_ready_or_submission_ready_claim",
            "production_ready_claim",
            "app_or_default_caller_cutover_claim",
        ],
        "required_next_evidence_refs": list(required_next_evidence_refs),
        "claims": {
            "claims_retirement_cleanup_complete": False,
            "claims_physical_delete_authorized": False,
            "claims_owner_receipt_signed": False,
            "claims_typed_blocker_created": False,
            "claims_domain_ready": False,
            "claims_production_ready": False,
        },
    }


def _read_forbidden_role_flags(value: Any, *, context: str) -> dict[str, bool]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 object。")
    flags: dict[str, bool] = {}
    for raw_key, raw_value in value.items():
        key = _normalize_key(
            _require_nonempty_string(raw_key, field_name="key", context=context)
        )
        if not isinstance(raw_value, bool):
            raise WorkspaceStateError(f"{context}.{key} 必须是 bool。")
        flags[key] = raw_value
    return flags


def _read_ref_list(value: Any, *, context: str) -> list[str]:
    if not isinstance(value, list):
        raise WorkspaceStateError(f"{context} 必须是 ref string list。")
    refs: list[str] = []
    for index, item in enumerate(value):
        ref = _require_nonempty_string(item, field_name="ref", context=f"{context}[{index}]")
        if ref not in refs:
            refs.append(ref)
    return refs


def _projection_state(
    *,
    blocked_count: int,
    evidence_gated_count: int,
    external_evidence_refs_complete: bool,
    source_ref_integrity_passed: bool,
) -> str:
    if not source_ref_integrity_passed:
        return "blocked_by_source_ref_integrity"
    if blocked_count:
        return "blocked_fail_closed"
    if evidence_gated_count or not external_evidence_refs_complete:
        return "allowed_evidence_gated"
    return "allowed_external_evidence_present"


def _retirement_gate_state(
    *,
    blocked_count: int,
    evidence_gated_count: int,
    missing_external_evidence_refs: list[str],
) -> str:
    if blocked_count:
        return "blocked_by_forbidden_role_flags"
    if evidence_gated_count:
        return "blocked_by_missing_role_evidence_refs"
    if missing_external_evidence_refs:
        return "active_caller_migration_evidence_required"
    return "eligible_for_owner_receipted_cleanup"


def _missing_external_evidence_refs(external_evidence_refs: list[str]) -> list[str]:
    normalized_refs = [_normalize_key(ref) for ref in external_evidence_refs]
    missing_refs: list[str] = []
    for index, (_category, markers) in enumerate(_REQUIRED_EXTERNAL_EVIDENCE_REF_MARKERS):
        if not any(
            any(marker in normalized_ref for marker in markers)
            for normalized_ref in normalized_refs
        ):
            missing_refs.append(_MISSING_EXTERNAL_EVIDENCE_REFS[index])
    return missing_refs


def _normalize_key(value: str) -> str:
    return value.strip().lower().replace(" ", "_")


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped


__all__ = [
    "ALLOWED_PHYSICAL_MORPHOLOGY_ROLES",
    "PHYSICAL_MORPHOLOGY_GUARD_PROJECTION_KIND",
    "build_physical_morphology_guard_projection",
]
