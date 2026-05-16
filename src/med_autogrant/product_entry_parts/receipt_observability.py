from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.owner_receipts import (
    RECEIPT_RECONCILIATION_INVENTORY_KIND,
)
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
)
from med_autogrant.workspace_types import WorkspaceStateError


RECEIPT_OBSERVABILITY_SUMMARY_KIND = "mag_controlled_soak_receipt_observability_summary"

_RECEIPT_SHAPES = ("domain_owner_receipt", "typed_blocker", "no_regression_evidence")
_RECONCILIATION_STATUSES = (
    "domain_owner_receipt_reconciled",
    "typed_blocker_reconciled",
    "no_regression_evidence_reconciled",
)
_FORBIDDEN_WRITE_FIELDS = (
    "repo_receipt_instance_written",
    "grant_truth_written",
    "grant_artifact_written",
    "memory_body_written",
    "fundability_verdict_written",
    "authoring_quality_verdict_written",
    "submission_ready_export_verdict_written",
)


def build_controlled_soak_receipt_observability_summary(
    receipt_reconciliation_inventory: Mapping[str, Any],
) -> dict[str, Any]:
    inventory = _unwrap_inventory(receipt_reconciliation_inventory)
    items = _require_items(inventory)
    summary = _require_mapping(inventory, "summary")
    opl_ledger = _require_mapping(inventory, "opl_ledger")
    forbidden_write_proof = _require_forbidden_write_proof(inventory)
    _require_inventory_identity(inventory)
    _require_summary_consistency(summary, items)

    receipt_refs = [_require_nonempty_item_string(item, "receipt_ref") for item in items]
    typed_blocker_refs = [
        _require_nonempty_item_string(item, "receipt_ref")
        for item in items
        if _require_bool(item, "typed_blocker_present")
    ]
    no_regression_refs = _collect_no_regression_refs(items)
    stage_counts = _count_by(items, "stage_id")
    shape_counts = _count_by(items, "receipt_shape")
    reconciliation_counts = _count_by(items, "reconciliation_status")
    blocker_count = len(typed_blocker_refs)
    no_regression_ref_count = len(no_regression_refs)

    return {
        "surface_kind": RECEIPT_OBSERVABILITY_SUMMARY_KIND,
        "version": "v1",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "state": "read_only_observability_summary_not_live_soak_complete",
        "source_inventory_ref": {
            "surface_kind": inventory["surface_kind"],
            "state": inventory["state"],
            "opl_ledger_ref": _require_nonempty_string(
                opl_ledger.get("ledger_ref"),
                field_name="opl_ledger.ledger_ref",
            ),
            "claims_production_long_run_soak_complete": _require_bool(
                inventory,
                "claims_production_long_run_soak_complete",
            ),
            "mag_writes_opl_ledger": _require_bool(opl_ledger, "mag_writes_opl_ledger"),
            "opl_holds_grant_truth": _require_bool(opl_ledger, "opl_holds_grant_truth"),
        },
        "source_inventory_summary": {
            "item_count": len(items),
            "sidecar_closeout_result_count": _require_int(
                summary,
                "sidecar_closeout_result_count",
            ),
            "by_receipt_shape": shape_counts,
            "by_reconciliation_status": reconciliation_counts,
            "typed_blocker_count": blocker_count,
            "no_regression_evidence_ref_count": no_regression_ref_count,
        },
        "operator_observability": {
            "observability_export_kind": "opl_runtime_observability_export",
            "consumption_policy": "read_only_refs_and_counts_no_repair_execution",
            "status": _operator_status(blocker_count),
            "receipt_ref_count": len(receipt_refs),
            "typed_blocker_ref_count": blocker_count,
            "no_regression_evidence_ref_count": no_regression_ref_count,
            "receipt_refs": receipt_refs,
            "typed_blocker_refs": typed_blocker_refs,
            "no_regression_evidence_refs": no_regression_refs,
            "consumed_inventory_fields": [
                "summary",
                "items.receipt_ref",
                "items.receipt_shape",
                "items.stage_id",
                "items.source_ref",
                "items.reconciliation_status",
                "items.typed_blocker_present",
                "items.no_regression_evidence_refs",
            ],
        },
        "stage_summary": {
            "stage_count": len(stage_counts),
            "by_stage_id": stage_counts,
            "stage_ids": sorted(stage_counts),
        },
        "receipt_shape_summary": {
            "by_receipt_shape": shape_counts,
            "domain_owner_receipt_count": shape_counts.get("domain_owner_receipt", 0),
            "typed_blocker_count": shape_counts.get("typed_blocker", 0),
            "no_regression_evidence_count": shape_counts.get("no_regression_evidence", 0),
        },
        "blocker_summary": {
            "typed_blocker_count": blocker_count,
            "typed_blocker_refs": typed_blocker_refs,
            "has_blockers": bool(blocker_count),
            "blocker_status": "typed_blocker_present" if blocker_count else "no_typed_blocker_present",
        },
        "no_regression_summary": {
            "no_regression_evidence_ref_count": no_regression_ref_count,
            "no_regression_evidence_refs": no_regression_refs,
            "has_no_regression_evidence": bool(no_regression_ref_count),
            "claims_no_regression_only": bool(no_regression_ref_count) and not blocker_count,
        },
        "authority_boundary": _authority_boundary(),
        "forbidden_write_proof": dict(forbidden_write_proof),
    }


def _unwrap_inventory(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError("receipt_reconciliation_inventory 必须是 JSON object。")
    inner = payload.get("receipt_reconciliation_inventory")
    if inner is not None:
        if not isinstance(inner, Mapping):
            raise WorkspaceStateError("receipt_reconciliation_inventory payload 缺少合法 inner inventory。")
        return inner
    return payload


def _require_inventory_identity(inventory: Mapping[str, Any]) -> None:
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
    if _require_bool(inventory, "claims_production_long_run_soak_complete"):
        raise WorkspaceStateError("receipt_reconciliation_inventory 不能声明 production long-run soak 完成。")
    opl_ledger = _require_mapping(inventory, "opl_ledger")
    if _require_bool(opl_ledger, "mag_writes_opl_ledger"):
        raise WorkspaceStateError("receipt_reconciliation_inventory 不能写 OPL ledger。")
    if _require_bool(opl_ledger, "opl_holds_grant_truth"):
        raise WorkspaceStateError("receipt_reconciliation_inventory 不能声明 OPL 持有 grant truth。")


def _require_items(inventory: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    raw_items = inventory.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise WorkspaceStateError("receipt_reconciliation_inventory.items 至少需要一条 refs-only item。")
    items: list[Mapping[str, Any]] = []
    for item in raw_items:
        if not isinstance(item, Mapping):
            raise WorkspaceStateError("receipt_reconciliation_inventory.items 必须只包含 JSON object。")
        receipt_shape = _require_nonempty_item_string(item, "receipt_shape")
        if receipt_shape not in _RECEIPT_SHAPES:
            raise WorkspaceStateError(f"receipt_shape 不支持: {receipt_shape}。")
        reconciliation_status = _require_nonempty_item_string(item, "reconciliation_status")
        if reconciliation_status not in _RECONCILIATION_STATUSES:
            raise WorkspaceStateError(f"reconciliation_status 不支持: {reconciliation_status}。")
        _require_nonempty_item_string(item, "receipt_ref")
        _require_nonempty_item_string(item, "stage_id")
        _require_nonempty_item_string(item, "source_ref")
        _require_bool(item, "typed_blocker_present")
        _require_string_list(item, "no_regression_evidence_refs")
        items.append(item)
    return items


def _require_summary_consistency(summary: Mapping[str, Any], items: list[Mapping[str, Any]]) -> None:
    item_count = _require_int(summary, "item_count")
    if item_count != len(items):
        raise WorkspaceStateError("receipt_reconciliation_inventory.summary.item_count 与 items 不一致。")
    expected_shape_counts = _count_by(items, "receipt_shape")
    if _require_mapping(summary, "by_receipt_shape") != expected_shape_counts:
        raise WorkspaceStateError("receipt_reconciliation_inventory.summary.by_receipt_shape 与 items 不一致。")
    expected_status_counts = _count_by(items, "reconciliation_status")
    if _require_mapping(summary, "by_reconciliation_status") != expected_status_counts:
        raise WorkspaceStateError(
            "receipt_reconciliation_inventory.summary.by_reconciliation_status 与 items 不一致。"
        )
    typed_blocker_count = _require_int(summary, "typed_blocker_count")
    if typed_blocker_count != sum(1 for item in items if _require_bool(item, "typed_blocker_present")):
        raise WorkspaceStateError("receipt_reconciliation_inventory.summary.typed_blocker_count 与 items 不一致。")
    no_regression_count = _require_int(summary, "no_regression_evidence_ref_count")
    if no_regression_count != len(_collect_no_regression_refs(items)):
        raise WorkspaceStateError(
            "receipt_reconciliation_inventory.summary.no_regression_evidence_ref_count 与 items 不一致。"
        )


def _require_forbidden_write_proof(inventory: Mapping[str, Any]) -> Mapping[str, bool]:
    proof = _require_mapping(inventory, "forbidden_write_proof")
    for field_name in _FORBIDDEN_WRITE_FIELDS:
        if proof.get(field_name) is not False:
            raise WorkspaceStateError(
                "receipt_reconciliation_inventory.forbidden_write_proof 必须证明 forbidden writes 全部为 false。"
            )
    return {field_name: False for field_name in _FORBIDDEN_WRITE_FIELDS}


def _authority_boundary() -> dict[str, bool | str]:
    return {
        "opl_ref_consumer_only": True,
        "mag_owner_receipt_authority": True,
        "can_execute_repair": False,
        "can_schedule_retry": False,
        "can_write_opl_stage_attempt_ledger": False,
        "can_declare_grant_ready": False,
        "can_declare_export_ready": False,
        "can_declare_fundability_ready": False,
        "can_declare_authoring_quality_ready": False,
        "can_declare_production_soak": False,
    }


def _collect_no_regression_refs(items: list[Mapping[str, Any]]) -> list[str]:
    refs: list[str] = []
    for item in items:
        for ref in _require_string_list(item, "no_regression_evidence_refs"):
            if ref not in refs:
                refs.append(ref)
    return refs


def _count_by(items: list[Mapping[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = _require_nonempty_item_string(item, key)
        counts[value] = counts.get(value, 0) + 1
    return counts


def _operator_status(blocker_count: int) -> str:
    if blocker_count:
        return "attention_required_typed_blocker_present"
    return "no_regression_evidence_observed"


def _require_mapping(payload: Mapping[str, Any], field_name: str) -> Mapping[str, Any]:
    value = payload.get(field_name)
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"receipt_reconciliation_inventory 缺少合法字段: {field_name}")
    return value


def _require_nonempty_item_string(item: Mapping[str, Any], field_name: str) -> str:
    return _require_nonempty_string(
        item.get(field_name),
        field_name=f"items.{field_name}",
        context="receipt_reconciliation_inventory",
    )


def _require_string_list(item: Mapping[str, Any], field_name: str) -> list[str]:
    value = item.get(field_name)
    if not isinstance(value, list):
        raise WorkspaceStateError(f"receipt_reconciliation_inventory.items.{field_name} 必须是 list。")
    refs: list[str] = []
    for ref in value:
        if not isinstance(ref, str) or not ref.strip():
            raise WorkspaceStateError(
                f"receipt_reconciliation_inventory.items.{field_name} 只能包含非空字符串。"
            )
        refs.append(ref.strip())
    return refs


def _require_bool(payload: Mapping[str, Any], field_name: str) -> bool:
    value = payload.get(field_name)
    if not isinstance(value, bool):
        raise WorkspaceStateError(f"receipt_reconciliation_inventory 缺少合法 bool 字段: {field_name}")
    return value


def _require_int(payload: Mapping[str, Any], field_name: str) -> int:
    value = payload.get(field_name)
    if not isinstance(value, int) or isinstance(value, bool):
        raise WorkspaceStateError(f"receipt_reconciliation_inventory 缺少合法 int 字段: {field_name}")
    return value
