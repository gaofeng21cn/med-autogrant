from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.owner_receipt_common import (
    RECEIPT_RECONCILIATION_INVENTORY_KIND,
    RECEIPT_SHAPES,
)
from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID
from med_autogrant.workspace_types import WorkspaceStateError
from opl_harness_shared.owner_evidence import (
    build_owner_evidence_observability_summary,
)


RECEIPT_OBSERVABILITY_SUMMARY_KIND = "mag_controlled_soak_receipt_observability_summary"
_RECONCILIATION_STATUSES = (
    "domain_owner_receipt_reconciled",
    "typed_blocker_reconciled",
    "no_regression_evidence_reconciled",
)
_RECEIPT_OBSERVABILITY_PROFILE = {
    "inventory_surface_kind": RECEIPT_RECONCILIATION_INVENTORY_KIND,
    "summary_surface_kind": RECEIPT_OBSERVABILITY_SUMMARY_KIND,
    "domain_id": TARGET_DOMAIN_ID,
    "receipt_shapes": RECEIPT_SHAPES,
    "reconciliation_statuses": _RECONCILIATION_STATUSES,
    "authority_boundary": {
        "opl_ref_consumer_only": True,
        "mag_owner_receipt_authority": True,
        "can_execute_repair": False,
        "can_schedule_retry": False,
        "can_write_opl_stage_attempt_records": False,
        "can_declare_grant_ready": False,
        "can_declare_export_ready": False,
        "can_declare_fundability_ready": False,
        "can_declare_authoring_quality_ready": False,
        "can_declare_production_soak": False,
    },
}


def build_controlled_soak_receipt_observability_summary(
    receipt_reconciliation_inventory: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        return build_owner_evidence_observability_summary(
            receipt_reconciliation_inventory,
            profile=_RECEIPT_OBSERVABILITY_PROFILE,
        )
    except ValueError as exc:
        raise WorkspaceStateError(str(exc)) from exc
