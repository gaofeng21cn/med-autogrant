from __future__ import annotations

from typing import Any, Mapping, Sequence

from med_autogrant.product_entry_parts.owner_receipt_common import read_forbidden_write_proof
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.workspace_types import WorkspaceStateError


STAGE_ATTEMPT_OBSERVABILITY_KIND = "mag_stage_attempt_observability_projection"


def build_stage_attempt_observability_projection(
    *,
    controlled_stage_attempt_projection: Mapping[str, Any],
    receipt_reconciliation_inventory: Mapping[str, Any],
    opl_usage_projection_ref: str,
    opl_control_loop_projection_ref: str,
) -> dict[str, Any]:
    stage_attempt = _coerce_stage_attempt_projection(controlled_stage_attempt_projection)
    inventory = _coerce_receipt_reconciliation_inventory(receipt_reconciliation_inventory)
    _validate_stage_attempt(stage_attempt)
    _validate_inventory(inventory)
    usage_ref = _require_nonempty_string(
        opl_usage_projection_ref,
        field_name="opl_usage_projection_ref",
    )
    control_loop_ref = _require_nonempty_string(
        opl_control_loop_projection_ref,
        field_name="opl_control_loop_projection_ref",
    )
    items = _inventory_items(inventory)
    payload = {
        "surface_kind": STAGE_ATTEMPT_OBSERVABILITY_KIND,
        "version": "v1",
        "state": "refs_only_projection_ready_for_opl_consumption",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "consumes_opl_surfaces": {
            "stage_attempt_usage_projection_ref": usage_ref,
            "stage_attempt_control_loop_projection_ref": control_loop_ref,
            "role": "external_projection_refs_only",
            "mag_writes_opl_stage_attempt_records": False,
            "mag_dispatches_opl_retries": False,
            "mag_owns_generic_control_loop": False,
        },
        "stage_attempt": {
            "attempt_ref": "/product_entry_manifest/controlled_stage_attempt_projection",
            "attempt_id": _require_nonempty_string_from_mapping(
                stage_attempt,
                "attempt_id",
                context="controlled_stage_attempt_projection",
            ),
            "attempt_state": _require_nonempty_string_from_mapping(
                stage_attempt,
                "attempt_state",
                context="controlled_stage_attempt_projection",
            ),
            "attempt_owner": _require_nonempty_string_from_mapping(
                stage_attempt,
                "attempt_owner",
                context="controlled_stage_attempt_projection",
            ),
            "maps_to_opl_contract": _require_nonempty_string_from_mapping(
                stage_attempt,
                "maps_to_opl_contract",
                context="controlled_stage_attempt_projection",
            ),
            "receipt_refs": dict(
                _require_mapping(
                    stage_attempt,
                    "receipt_refs",
                    context="controlled_stage_attempt_projection",
                )
            ),
        },
        "receipt_inventory_summary": _receipt_inventory_summary(inventory, items),
        "blocked_receipt_refs": [
            _require_nonempty_string_from_mapping(item, "receipt_ref", context="receipt_inventory_item")
            for item in items
            if bool(item.get("typed_blocker_present"))
        ],
        "no_regression_evidence_refs": _no_regression_evidence_refs(items),
        "control_loop_handoff": {
            "handoff_state": _control_loop_handoff_state(items),
            "typed_blocker_count": sum(1 for item in items if bool(item.get("typed_blocker_present"))),
            "next_owner": "one-person-lab",
            "required_opl_surface": "stage_attempt_control_loop_projection",
            "mag_returns_only": [
                "domain_owner_receipt_ref",
                "typed_blocker",
                "no_regression_evidence_ref",
            ],
        },
        "claims": {
            "claims_opl_provider_completion": False,
            "claims_production_long_run_soak_complete": False,
            "claims_grant_fundability_ready": False,
            "claims_authoring_quality_ready": False,
            "claims_submission_ready_export": False,
        },
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "mag_stage_truth_authority": True,
            "opl_usage_projection_owner": "one-person-lab",
            "opl_control_loop_projection_owner": "one-person-lab",
            "opl_can_write_grant_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_export_ready": False,
            "mag_implements_generic_attempt_ledger": False,
            "mag_implements_generic_runner": False,
            "mag_implements_generic_scheduler": False,
        },
        "forbidden_write_proof": read_forbidden_write_proof(
            inventory,
            context="receipt_reconciliation_inventory",
        ),
    }
    return {
        "ok": True,
        "command": "stage-attempt-observability-projection",
        "stage_attempt_observability_projection": payload,
    }


def _coerce_stage_attempt_projection(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("surface_kind") == "controlled_stage_attempt_projection":
        return payload
    return _require_mapping(
        payload,
        "controlled_stage_attempt_projection",
        context="stage_attempt_observability",
    )


def _coerce_receipt_reconciliation_inventory(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if payload.get("surface_kind") == "mag_controlled_soak_receipt_reconciliation_inventory":
        return payload
    return _require_mapping(
        payload,
        "receipt_reconciliation_inventory",
        context="stage_attempt_observability",
    )


def _validate_stage_attempt(stage_attempt: Mapping[str, Any]) -> None:
    if stage_attempt.get("surface_kind") != "controlled_stage_attempt_projection":
        raise WorkspaceStateError(
            "controlled_stage_attempt_projection.surface_kind 必须是 controlled_stage_attempt_projection。"
        )
    if stage_attempt.get("attempt_owner") != TARGET_DOMAIN_ID:
        raise WorkspaceStateError("controlled_stage_attempt_projection.attempt_owner 必须是 med-autogrant。")
    if stage_attempt.get("maps_to_opl_contract") != "opl_family_runtime_attempt_contract.v1":
        raise WorkspaceStateError(
            "controlled_stage_attempt_projection.maps_to_opl_contract 必须是 opl_family_runtime_attempt_contract.v1。"
        )


def _validate_inventory(inventory: Mapping[str, Any]) -> None:
    if inventory.get("surface_kind") != "mag_controlled_soak_receipt_reconciliation_inventory":
        raise WorkspaceStateError(
            "receipt_reconciliation_inventory.surface_kind 必须是 "
            "mag_controlled_soak_receipt_reconciliation_inventory。"
        )
    if bool(inventory.get("claims_production_long_run_soak_complete")):
        raise WorkspaceStateError("receipt_reconciliation_inventory 不能声明 production long-run soak complete。")
    authority = _require_mapping(
        inventory,
        "authority_boundary",
        context="receipt_reconciliation_inventory",
    )
    forbidden_ready_keys = (
        "can_declare_fundability_ready",
        "can_declare_authoring_quality_ready",
        "can_declare_submission_ready_export",
    )
    if any(bool(authority.get(key)) for key in forbidden_ready_keys):
        raise WorkspaceStateError("receipt_reconciliation_inventory 不能声明 grant readiness/export readiness。")


def _receipt_inventory_summary(
    inventory: Mapping[str, Any],
    items: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    summary = _require_mapping(inventory, "summary", context="receipt_reconciliation_inventory")
    return {
        "inventory_ref": "receipt_reconciliation_inventory",
        "state": _require_nonempty_string_from_mapping(
            inventory,
            "state",
            context="receipt_reconciliation_inventory",
        ),
        "item_count": len(items),
        "by_receipt_shape": dict(
            _require_mapping(
                summary,
                "by_receipt_shape",
                context="receipt_reconciliation_inventory.summary",
            )
        ),
        "by_reconciliation_status": dict(
            _require_mapping(
                summary,
                "by_reconciliation_status",
                context="receipt_reconciliation_inventory.summary",
            )
        ),
        "typed_blocker_count": int(summary.get("typed_blocker_count", 0)),
        "no_regression_evidence_ref_count": int(summary.get("no_regression_evidence_ref_count", 0)),
    }


def _inventory_items(inventory: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    raw_items = inventory.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise WorkspaceStateError("receipt_reconciliation_inventory.items 必须是非空列表。")
    items: list[Mapping[str, Any]] = []
    for item in raw_items:
        if not isinstance(item, Mapping):
            raise WorkspaceStateError("receipt_reconciliation_inventory.items 每一项都必须是对象。")
        items.append(item)
    return items


def _no_regression_evidence_refs(items: Sequence[Mapping[str, Any]]) -> list[str]:
    refs: list[str] = []
    for item in items:
        raw_refs = item.get("no_regression_evidence_refs")
        if not isinstance(raw_refs, list):
            raise WorkspaceStateError("receipt_inventory_item.no_regression_evidence_refs 必须是列表。")
        for ref in raw_refs:
            resolved = _require_nonempty_string(ref, field_name="no_regression_evidence_ref")
            if resolved not in refs:
                refs.append(resolved)
    return refs


def _control_loop_handoff_state(items: Sequence[Mapping[str, Any]]) -> str:
    if any(bool(item.get("typed_blocker_present")) for item in items):
        return "typed_blocker_refs_ready_for_opl_control_loop"
    return "no_regression_refs_ready_for_opl_usage_projection"
