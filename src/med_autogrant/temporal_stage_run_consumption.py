from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


TEMPORAL_STAGE_RUN_CONSUMPTION_POLICY_ID = "mag.temporal_stage_run_consumption_policy.v1"
TEMPORAL_STAGE_RUN_CONSUMPTION_POLICY_REF = "/product_entry_manifest/temporal_stage_run_consumption_policy"
TEMPORAL_ATTEMPT_LEDGER_OWNER = "one-person-lab/OPL"


def build_temporal_stage_run_consumption_policy() -> dict[str, Any]:
    return {
        "surface_kind": "temporal_stage_run_consumption_policy",
        "policy_id": TEMPORAL_STAGE_RUN_CONSUMPTION_POLICY_ID,
        "version": 1,
        "owner": TARGET_DOMAIN_ID,
        "runtime_substrate_owner": "one-person-lab",
        "runtime_substrate": "temporal",
        "domain_role": "refs_only_consumer_and_grant_authority",
        "domain_truth_owner": TARGET_DOMAIN_ID,
        "temporal_attempt_ledger_owner": TEMPORAL_ATTEMPT_LEDGER_OWNER,
        "provider_completion_is_domain_completion": False,
        "domain_repo_can_own_temporal_runtime": False,
        "domain_repo_can_write_opl_stage_attempts": False,
        "generated_surface_ready_can_claim_domain_ready": False,
        "mag_writes_opl_stage_attempt_records": False,
        "mag_can_create_temporal_attempt_ledger": False,
        "mag_can_run_temporal_worker_or_scheduler": False,
        "accepted_domain_closing_ref_fields": [
            "owner_receipt_ref",
            "typed_blocker_ref",
            "human_gate_ref",
            "route_back_ref",
        ],
        "accepted_consumed_ref_fields": [
            "temporal_stage_run_ref",
            "provider_attempt_ref",
            "provider_completion_ref",
            "stage_attempt_ref",
        ],
        "domain_completion_policy": (
            "Only MAG owner receipt, typed blocker, human gate, or route-back refs can close "
            "domain completion; OPL provider completion and generated-surface readiness remain "
            "runtime/projection signals."
        ),
        "authority_boundary": {
            "opl_can_write_grant_truth": False,
            "opl_can_authorize_quality_or_export": False,
            "opl_can_sign_mag_owner_receipt": False,
            "mag_can_write_opl_stage_attempts": False,
            "mag_can_own_temporal_runtime": False,
            "provider_completion_counts_as_domain_completion": False,
            "generated_surface_ready_counts_as_domain_ready": False,
        },
        "readback_policy": {
            "project_on_product_status": True,
            "project_on_runtime_control": True,
            "project_on_action_catalog": True,
            "project_on_generated_surface_handoff": True,
            "second_runtime_forbidden": True,
        },
    }
