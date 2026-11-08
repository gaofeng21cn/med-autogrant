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
        "lineage": _typed_blocker_lineage(receipt, blocker_kind=blocker_kind),
        "repeat_budget": _typed_blocker_repeat_budget(),
        "next_forced_delta": _typed_blocker_next_forced_delta(receipt, blocker_kind=blocker_kind),
        "escalation_owner": TARGET_DOMAIN_ID,
        "escalation_policy": {
            "route": "mag_owner_surface",
            "owner": TARGET_DOMAIN_ID,
            "trigger": "repeat_budget_exhausted_or_same_blocker_reappears",
        },
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


def _typed_blocker_lineage(receipt: Mapping[str, Any], *, blocker_kind: str) -> dict[str, Any]:
    return {
        "stage_id": receipt.get("stage_id"),
        "blocker_kind": blocker_kind,
        "receipt_ref": receipt.get("receipt_instance_ref"),
        "source_ref": receipt.get("source_ref"),
        "owner": TARGET_DOMAIN_ID,
    }


def _typed_blocker_next_forced_delta(receipt: Mapping[str, Any], *, blocker_kind: str) -> dict[str, Any]:
    stage_id = receipt.get("stage_id")
    return {
        "required_delta_kind": "grant_deliverable_progress_delta_or_domain_owned_typed_blocker",
        "stage_id": stage_id,
        "blocker_kind": blocker_kind,
        "next_owner": TARGET_DOMAIN_ID,
        "escalation_owner": TARGET_DOMAIN_ID,
        "accepted_return_shapes": [
            "domain_owner_receipt_ref",
            "typed_blocker_ref",
            "no_regression_evidence_ref",
        ],
        "can_claim_grant_ready": False,
        "can_claim_submission_ready": False,
    }


def _typed_blocker_repeat_budget() -> dict[str, Any]:
    return {
        "max_repeats_before_escalation": 2,
        "budget_scope": "same_stage_same_blocker_kind",
        "escalation_owner": TARGET_DOMAIN_ID,
    }
