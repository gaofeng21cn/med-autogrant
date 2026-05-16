from __future__ import annotations

from typing import Any, Mapping, Sequence

from med_autogrant.product_entry_parts.hosted_receipt_verification import (
    HOSTED_RECEIPT_VERIFICATION_KIND,
)
from med_autogrant.product_entry_parts.owner_receipts import (
    RECEIPT_RECONCILIATION_INVENTORY_KIND,
)
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.product_entry_parts.receipt_observability import (
    RECEIPT_OBSERVABILITY_SUMMARY_KIND,
)
from med_autogrant.product_entry_parts.stage_attempt_observability import (
    STAGE_ATTEMPT_OBSERVABILITY_KIND,
)
from med_autogrant.workspace_types import WorkspaceStateError


CONTINUOUS_RECEIPT_RECONCILIATION_SNAPSHOT_KIND = (
    "mag_continuous_receipt_reconciliation_snapshot"
)

_RECEIPT_SHAPES = (
    "domain_owner_receipt",
    "typed_blocker",
    "no_regression_evidence",
)
_RECONCILIATION_STATUSES = (
    "domain_owner_receipt_reconciled",
    "typed_blocker_reconciled",
    "no_regression_evidence_reconciled",
)
_READY_CLAIM_KEYS = (
    "grant_ready",
    "quality_ready",
    "export_ready",
    "fundability_ready",
    "submission_ready",
    "submission_ready_export",
    "production_soak_complete",
    "production_long_run_soak_complete",
    "claims_grant_ready",
    "claims_quality_ready",
    "claims_export_ready",
    "claims_fundability_ready",
    "claims_authoring_quality_ready",
    "claims_submission_ready",
    "claims_submission_ready_export",
    "claims_production_soak_complete",
    "claims_production_long_run_soak_complete",
    "provider_completion_consumed_as_readiness",
    "provider_completion_can_declare_grant_ready",
    "provider_completion_can_declare_export_ready",
    "can_declare_grant_ready",
    "can_declare_export_ready",
    "can_declare_fundability_ready",
    "can_declare_authoring_quality_ready",
    "can_declare_submission_ready_export",
    "can_declare_production_soak",
)
def build_continuous_receipt_reconciliation_snapshot(
    *,
    focused_hosted_receipt_verification_items: Sequence[Mapping[str, Any]],
    receipt_reconciliation_inventory: Mapping[str, Any],
    receipt_observability_summary: Mapping[str, Any] | None = None,
    stage_attempt_observability_projection: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    inventory = _coerce_inventory(receipt_reconciliation_inventory)
    _reject_ready_claims(
        inventory,
        context="receipt_reconciliation_inventory",
        allow_provider_completion_claim=True,
    )
    _validate_inventory_identity(inventory)
    inventory_items = _inventory_items(inventory)
    verification_items = _verification_items(focused_hosted_receipt_verification_items)
    resolved_receipt_observability_summary = None
    if receipt_observability_summary is not None:
        resolved_receipt_observability_summary = _coerce_receipt_observability_summary(
            receipt_observability_summary
        )
        _validate_receipt_observability_summary(resolved_receipt_observability_summary)
    resolved_stage_attempt_observability_projection = None
    if stage_attempt_observability_projection is not None:
        resolved_stage_attempt_observability_projection = _coerce_stage_attempt_observability_projection(
            stage_attempt_observability_projection
        )
        _validate_stage_attempt_observability_projection(resolved_stage_attempt_observability_projection)

    inventory_refs = [_receipt_ref_from_inventory_item(item) for item in inventory_items]
    verified_refs = [_receipt_ref_from_verification(item) for item in verification_items]
    unmatched_refs = [ref for ref in inventory_refs if ref not in verified_refs]
    shape_counts = _count_inventory_shapes(inventory_items)

    return {
        "surface_kind": CONTINUOUS_RECEIPT_RECONCILIATION_SNAPSHOT_KIND,
        "version": "v1",
        "state": "read_only_snapshot_not_live_soak_complete",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "summary": {
            "verified_count": len(verification_items),
            "typed_blocker_count": shape_counts.get("typed_blocker", 0),
            "no_regression_evidence_count": shape_counts.get("no_regression_evidence", 0),
            "domain_owner_receipt_count": shape_counts.get("domain_owner_receipt", 0),
            "unmatched_count": len(unmatched_refs),
        },
        "receipt_refs": {
            "all_inventory_refs": inventory_refs,
            "verified_refs": verified_refs,
            "typed_blocker_refs": _typed_blocker_refs(inventory_items),
            "no_regression_evidence_refs": _no_regression_evidence_refs(inventory_items),
            "domain_owner_receipt_refs": _domain_owner_receipt_refs(inventory_items),
            "unmatched_refs": unmatched_refs,
        },
        "source_surfaces": {
            "focused_hosted_receipt_verification_count": len(verification_items),
            "receipt_reconciliation_inventory": {
                "surface_kind": inventory["surface_kind"],
                "state": _require_nonempty_string_from_mapping(
                    inventory,
                    "state",
                    context="receipt_reconciliation_inventory",
                ),
            },
            "receipt_observability_summary": _optional_source_surface(
                resolved_receipt_observability_summary,
                expected_kind=RECEIPT_OBSERVABILITY_SUMMARY_KIND,
            ),
            "stage_attempt_observability_projection": _optional_source_surface(
                resolved_stage_attempt_observability_projection,
                expected_kind=STAGE_ATTEMPT_OBSERVABILITY_KIND,
            ),
        },
        "claims": {
            "claims_production_long_run_soak_complete": False,
            "claims_grant_ready": False,
            "claims_quality_ready": False,
            "claims_export_ready": False,
        },
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "mag_writes_opl_ledger": False,
            "mag_implements_opl_provider": False,
            "mag_declares_live_soak_complete": False,
            "mag_declares_grant_ready": False,
            "mag_declares_quality_ready": False,
            "mag_declares_export_ready": False,
            "opl_ledger_role": "external_read_only_ref",
            "snapshot_scope": "refs_and_counts_only",
        },
    }


def _coerce_inventory(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError("receipt_reconciliation_inventory 必须是 JSON object。")
    if payload.get("surface_kind") == RECEIPT_RECONCILIATION_INVENTORY_KIND:
        return payload
    return _require_mapping(
        payload,
        "receipt_reconciliation_inventory",
        context="continuous_receipt_reconciliation_snapshot",
    )


def _validate_inventory_identity(inventory: Mapping[str, Any]) -> None:
    if inventory.get("surface_kind") != RECEIPT_RECONCILIATION_INVENTORY_KIND:
        raise WorkspaceStateError(
            "receipt_reconciliation_inventory.surface_kind 必须是 "
            f"{RECEIPT_RECONCILIATION_INVENTORY_KIND}。"
        )
    if inventory.get("owner") != TARGET_DOMAIN_ID:
        raise WorkspaceStateError("receipt_reconciliation_inventory.owner 必须是 med-autogrant。")
    if inventory.get("target_domain_id") != TARGET_DOMAIN_ID:
        raise WorkspaceStateError(
            "receipt_reconciliation_inventory.target_domain_id 必须是 med-autogrant。"
        )
    opl_ledger = _require_mapping(inventory, "opl_ledger", context="receipt_reconciliation_inventory")
    if bool(opl_ledger.get("mag_writes_opl_ledger")):
        raise WorkspaceStateError("continuous receipt snapshot 不能写 OPL ledger。")
    if bool(opl_ledger.get("opl_holds_grant_truth")):
        raise WorkspaceStateError("continuous receipt snapshot 不能声明 OPL 持有 grant truth。")
    authority = _require_mapping(
        inventory,
        "authority_boundary",
        context="receipt_reconciliation_inventory",
    )
    _reject_ready_claims(authority, context="receipt_reconciliation_inventory.authority_boundary")


def _inventory_items(inventory: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    raw_items = inventory.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise WorkspaceStateError("receipt_reconciliation_inventory.items 至少需要一条 item。")
    items: list[Mapping[str, Any]] = []
    for item in raw_items:
        if not isinstance(item, Mapping):
            raise WorkspaceStateError("receipt_reconciliation_inventory.items 必须只包含 JSON object。")
        _reject_ready_claims(item, context="receipt_reconciliation_inventory.items")
        receipt_shape = _require_nonempty_string_from_mapping(
            item,
            "receipt_shape",
            context="receipt_reconciliation_inventory.items",
        )
        if receipt_shape not in _RECEIPT_SHAPES:
            raise WorkspaceStateError(f"receipt_shape 不支持: {receipt_shape}。")
        reconciliation_status = _require_nonempty_string_from_mapping(
            item,
            "reconciliation_status",
            context="receipt_reconciliation_inventory.items",
        )
        if reconciliation_status not in _RECONCILIATION_STATUSES:
            raise WorkspaceStateError(f"reconciliation_status 不支持: {reconciliation_status}。")
        _receipt_ref_from_inventory_item(item)
        _require_nonempty_string_from_mapping(
            item,
            "stage_id",
            context="receipt_reconciliation_inventory.items",
        )
        _require_nonempty_string_from_mapping(
            item,
            "source_ref",
            context="receipt_reconciliation_inventory.items",
        )
        _require_bool(item, "typed_blocker_present", context="receipt_reconciliation_inventory.items")
        _require_string_list(
            item,
            "no_regression_evidence_refs",
            context="receipt_reconciliation_inventory.items",
        )
        item_authority = item.get("authority_boundary")
        if isinstance(item_authority, Mapping):
            _reject_ready_claims(
                item_authority,
                context="receipt_reconciliation_inventory.items.authority_boundary",
            )
        items.append(item)
    return items


def _verification_items(payloads: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    if not isinstance(payloads, Sequence) or isinstance(payloads, (str, bytes)):
        raise WorkspaceStateError("focused_hosted_receipt_verification_items 必须是 list。")
    if not payloads:
        raise WorkspaceStateError("focused_hosted_receipt_verification_items 至少需要一条 item。")
    items: list[Mapping[str, Any]] = []
    for payload in payloads:
        verification = _coerce_verification(payload)
        _reject_ready_claims(
            verification,
            context="focused_hosted_receipt_verification",
            allow_provider_completion_claim=True,
        )
        _validate_verification_identity(verification)
        items.append(verification)
    return items


def _coerce_verification(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError("focused_hosted_receipt_verification item 必须是 JSON object。")
    if payload.get("surface_kind") == HOSTED_RECEIPT_VERIFICATION_KIND:
        return payload
    return _require_mapping(
        payload,
        "focused_hosted_receipt_verification",
        context="continuous_receipt_reconciliation_snapshot",
    )


def _coerce_receipt_observability_summary(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError("receipt_observability_summary 必须是 JSON object。")
    if payload.get("surface_kind") == RECEIPT_OBSERVABILITY_SUMMARY_KIND:
        return payload
    return _require_mapping(
        payload,
        "receipt_observability_summary",
        context="continuous_receipt_reconciliation_snapshot",
    )


def _coerce_stage_attempt_observability_projection(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError("stage_attempt_observability_projection 必须是 JSON object。")
    if payload.get("surface_kind") == STAGE_ATTEMPT_OBSERVABILITY_KIND:
        return payload
    return _require_mapping(
        payload,
        "stage_attempt_observability_projection",
        context="continuous_receipt_reconciliation_snapshot",
    )


def _validate_verification_identity(verification: Mapping[str, Any]) -> None:
    if verification.get("surface_kind") != HOSTED_RECEIPT_VERIFICATION_KIND:
        raise WorkspaceStateError(
            "focused_hosted_receipt_verification.surface_kind 必须是 "
            f"{HOSTED_RECEIPT_VERIFICATION_KIND}。"
        )
    if verification.get("owner") != TARGET_DOMAIN_ID:
        raise WorkspaceStateError("focused_hosted_receipt_verification.owner 必须是 med-autogrant。")
    if verification.get("target_domain_id") != TARGET_DOMAIN_ID:
        raise WorkspaceStateError(
            "focused_hosted_receipt_verification.target_domain_id 必须是 med-autogrant。"
        )
    if verification.get("state") != "focused_hosted_receipt_refs_verified_not_live_soak":
        raise WorkspaceStateError(
            "focused_hosted_receipt_verification.state 必须是 "
            "focused_hosted_receipt_refs_verified_not_live_soak。"
        )
    owner_receipt = _require_mapping(
        verification,
        "mag_owner_receipt",
        context="focused_hosted_receipt_verification",
    )
    receipt_shape = _require_nonempty_string_from_mapping(
        owner_receipt,
        "receipt_shape",
        context="focused_hosted_receipt_verification.mag_owner_receipt",
    )
    if receipt_shape not in _RECEIPT_SHAPES:
        raise WorkspaceStateError(f"focused_hosted_receipt_verification receipt_shape 不支持: {receipt_shape}。")
    _receipt_ref_from_verification(verification)
    _reject_ready_claims(
        _require_mapping(
            verification,
            "claims",
            context="focused_hosted_receipt_verification",
        ),
        context="focused_hosted_receipt_verification.claims",
        allow_provider_completion_claim=True,
    )
    _reject_ready_claims(
        _require_mapping(
            verification,
            "authority_boundary",
            context="focused_hosted_receipt_verification",
        ),
        context="focused_hosted_receipt_verification.authority_boundary",
    )
    _reject_ready_claims(
        _require_mapping(
            verification,
            "opl_attempt",
            context="focused_hosted_receipt_verification",
        ),
        context="focused_hosted_receipt_verification.opl_attempt",
    )


def _validate_receipt_observability_summary(summary: Mapping[str, Any]) -> None:
    if not isinstance(summary, Mapping):
        raise WorkspaceStateError("receipt_observability_summary 必须是 JSON object。")
    _reject_ready_claims(
        summary,
        context="receipt_observability_summary",
        allow_provider_completion_claim=True,
    )
    if summary.get("surface_kind") != RECEIPT_OBSERVABILITY_SUMMARY_KIND:
        raise WorkspaceStateError(
            "receipt_observability_summary.surface_kind 必须是 "
            f"{RECEIPT_OBSERVABILITY_SUMMARY_KIND}。"
        )
    _reject_ready_claims(
        _require_mapping(summary, "authority_boundary", context="receipt_observability_summary"),
        context="receipt_observability_summary.authority_boundary",
    )
    source_ref = _require_mapping(
        summary,
        "source_inventory_ref",
        context="receipt_observability_summary",
    )
    _reject_ready_claims(source_ref, context="receipt_observability_summary.source_inventory_ref")


def _validate_stage_attempt_observability_projection(projection: Mapping[str, Any]) -> None:
    if not isinstance(projection, Mapping):
        raise WorkspaceStateError("stage_attempt_observability_projection 必须是 JSON object。")
    _reject_ready_claims(
        projection,
        context="stage_attempt_observability_projection",
        allow_provider_completion_claim=True,
    )
    if projection.get("surface_kind") != STAGE_ATTEMPT_OBSERVABILITY_KIND:
        raise WorkspaceStateError(
            "stage_attempt_observability_projection.surface_kind 必须是 "
            f"{STAGE_ATTEMPT_OBSERVABILITY_KIND}。"
        )
    _reject_ready_claims(
        _require_mapping(projection, "claims", context="stage_attempt_observability_projection"),
        context="stage_attempt_observability_projection.claims",
        allow_provider_completion_claim=True,
    )
    _reject_ready_claims(
        _require_mapping(
            projection,
            "authority_boundary",
            context="stage_attempt_observability_projection",
        ),
        context="stage_attempt_observability_projection.authority_boundary",
    )


def _reject_ready_claims(
    payload: Any,
    *,
    context: str,
    allow_provider_completion_claim: bool = False,
) -> None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            if allow_provider_completion_claim and key == "claims_opl_provider_completion":
                continue
            if key in _READY_CLAIM_KEYS and bool(value):
                raise WorkspaceStateError(
                    f"{context} 不能声明 production soak 或 grant/quality/export ready。"
                )
            _reject_ready_claims(
                value,
                context=f"{context}.{key}",
                allow_provider_completion_claim=allow_provider_completion_claim,
            )
        return
    if isinstance(payload, list):
        for index, item in enumerate(payload):
            _reject_ready_claims(
                item,
                context=f"{context}[{index}]",
                allow_provider_completion_claim=allow_provider_completion_claim,
            )


def _receipt_ref_from_inventory_item(item: Mapping[str, Any]) -> str:
    return _require_nonempty_string_from_mapping(
        item,
        "receipt_ref",
        context="receipt_reconciliation_inventory.items",
    )


def _receipt_ref_from_verification(verification: Mapping[str, Any]) -> str:
    owner_receipt = _require_mapping(
        verification,
        "mag_owner_receipt",
        context="focused_hosted_receipt_verification",
    )
    return _require_nonempty_string_from_mapping(
        owner_receipt,
        "receipt_ref",
        context="focused_hosted_receipt_verification.mag_owner_receipt",
    )


def _count_inventory_shapes(items: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        shape = _require_nonempty_string_from_mapping(
            item,
            "receipt_shape",
            context="receipt_reconciliation_inventory.items",
        )
        counts[shape] = counts.get(shape, 0) + 1
    return counts


def _typed_blocker_refs(items: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        _receipt_ref_from_inventory_item(item)
        for item in items
        if _require_bool(
            item,
            "typed_blocker_present",
            context="receipt_reconciliation_inventory.items",
        )
    ]


def _no_regression_evidence_refs(items: Sequence[Mapping[str, Any]]) -> list[str]:
    refs: list[str] = []
    for item in items:
        for ref in _require_string_list(
            item,
            "no_regression_evidence_refs",
            context="receipt_reconciliation_inventory.items",
        ):
            if ref not in refs:
                refs.append(ref)
    return refs


def _domain_owner_receipt_refs(items: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        _receipt_ref_from_inventory_item(item)
        for item in items
        if item.get("receipt_shape") == "domain_owner_receipt"
    ]


def _optional_source_surface(
    payload: Mapping[str, Any] | None,
    *,
    expected_kind: str,
) -> dict[str, str] | None:
    if payload is None:
        return None
    return {
        "surface_kind": expected_kind,
        "state": _require_nonempty_string_from_mapping(payload, "state", context=expected_kind),
    }


def _require_bool(payload: Mapping[str, Any], field_name: str, *, context: str) -> bool:
    value = payload.get(field_name)
    if not isinstance(value, bool):
        raise WorkspaceStateError(f"{context}.{field_name} 必须是 bool。")
    return value


def _require_string_list(
    payload: Mapping[str, Any],
    field_name: str,
    *,
    context: str,
) -> list[str]:
    value = payload.get(field_name)
    if not isinstance(value, list):
        raise WorkspaceStateError(f"{context}.{field_name} 必须是 list。")
    return [
        _require_nonempty_string(item, field_name=field_name, context=context)
        for item in value
    ]
