from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID

PACKAGE_SUBMISSION_READY_HUMAN_GATE_ID = "submission_ready_export_gate"


def build_typed_blocker_projection(
    receipt: Mapping[str, Any],
    *,
    blocker_kind: str,
) -> dict[str, Any] | None:
    if receipt.get("receipt_shape") != "typed_blocker":
        return None
    blocker = {
        "blocker_kind": blocker_kind,
        "owner": TARGET_DOMAIN_ID,
        "receipt_ref": receipt.get("receipt_instance_ref"),
        "source_ref": receipt.get("source_ref"),
        "next_action": "Route the blocker back to MAG owner surface before mutating grant truth, memory body, or artifact content.",
    }
    if receipt.get("stage_id") == "package_and_submit_ready":
        blocker.update(_package_submission_ready_human_gate_boundary())
    return blocker


def package_submission_ready_human_gate_authority_boundary(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    if receipt.get("receipt_shape") != "typed_blocker":
        return {}
    if receipt.get("stage_id") != "package_and_submit_ready":
        return {}
    return {
        "human_gate_required": True,
        "human_gate_id": PACKAGE_SUBMISSION_READY_HUMAN_GATE_ID,
        "submission_ready_export_gate_owner": TARGET_DOMAIN_ID,
        "opl_can_bypass_human_gate": False,
        "provider_completion_is_submission_ready": False,
        "can_declare_submission_ready_export": False,
    }


def _package_submission_ready_human_gate_boundary() -> dict[str, Any]:
    return {
        "human_gate_id": PACKAGE_SUBMISSION_READY_HUMAN_GATE_ID,
        "human_gate_required": True,
        "human_gate_owner": TARGET_DOMAIN_ID,
        "receipt_requirement": "human_gate_receipt",
        "can_declare_submission_ready_export": False,
        "opl_can_bypass_human_gate": False,
        "provider_completion_is_submission_ready": False,
        "blocked_claims": [
            "submission_ready",
            "export_ready",
            "production_ready",
        ],
    }
