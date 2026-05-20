from __future__ import annotations

from typing import Any, Mapping

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
    "external_evidence://physical_morphology_hygiene/continuous_no_forbidden_write",
)

_REQUIRED_EXTERNAL_EVIDENCE_REF_MARKERS = (
    ("active_caller_migration", ("active-caller-migration", "active_caller_migration")),
    ("direct_hosted_parity", ("direct-hosted-parity", "direct_hosted_parity")),
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

    claims_physical_cleanup_complete = (
        not blocked_items
        and not item_evidence_gated
        and not missing_external_evidence_refs
    )
    state = _projection_state(
        blocked_count=len(blocked_items),
        evidence_gated_count=len(item_evidence_gated),
        external_evidence_refs_complete=not missing_external_evidence_refs,
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
        "claims": {
            "claims_physical_morphology_cleanup_complete": claims_physical_cleanup_complete,
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
            "can_declare_physical_cleanup_complete": claims_physical_cleanup_complete,
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
) -> str:
    if blocked_count:
        return "blocked_fail_closed"
    if evidence_gated_count or not external_evidence_refs_complete:
        return "allowed_evidence_gated"
    return "allowed_external_evidence_present"


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
