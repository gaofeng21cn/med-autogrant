from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


TEMPORAL_STAGE_RUN_CONSUMPTION_POLICY_ID = "mag.temporal_stage_run_consumption_policy.v1"
TEMPORAL_STAGE_RUN_CONSUMPTION_POLICY_REF = "/product_entry_manifest/temporal_stage_run_consumption_policy"
TEMPORAL_STAGE_RUN_CONSUMPTION_CONTRACT_REF = "contracts/temporal_stage_run_consumption_policy.json"
TEMPORAL_ATTEMPT_LEDGER_OWNER = "one-person-lab/OPL"
ACCEPTED_DOMAIN_CLOSING_REF_FIELDS = [
    "owner_receipt_ref",
    "typed_blocker_ref",
    "human_gate_ref",
    "route_back_ref",
]
FALSE_COMPLETION_SIGNALS = [
    "provider_completion",
    "schema_completeness",
    "generated_surface_ready",
    "manifest_success",
    "focused_tests_passed",
    "action_catalog_available",
    "runtime_control_projection_present",
    "product_status_projection_present",
    "stage_replay_projection",
    "stage_folder_conformance",
    "package_existence",
    "quality_scorecard_score",
    "grouped_cli_success",
]


def build_temporal_stage_run_consumption_policy() -> dict[str, Any]:
    grant_ready_completion_audit = build_grant_ready_completion_audit()
    return {
        "surface_kind": "temporal_stage_run_consumption_policy",
        "policy_id": TEMPORAL_STAGE_RUN_CONSUMPTION_POLICY_ID,
        "version": 1,
        "owner": TARGET_DOMAIN_ID,
        "contract_ref": TEMPORAL_STAGE_RUN_CONSUMPTION_CONTRACT_REF,
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
        "accepted_domain_closing_ref_fields": ACCEPTED_DOMAIN_CLOSING_REF_FIELDS,
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
        "grant_ready_completion_audit": grant_ready_completion_audit,
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


def build_grant_ready_completion_audit() -> dict[str, Any]:
    return {
        "surface_kind": "grant_ready_completion_audit",
        "audit_id": "mag.grant_ready_completion_audit.v1",
        "version": 1,
        "owner": TARGET_DOMAIN_ID,
        "state": "blocked_without_mag_owner_closing_ref",
        "purpose": (
            "Prevent Temporal/provider/schema/generated-surface/test signals from being "
            "misread as MAG grant-ready, quality-ready, export-ready, or submission-ready completion."
        ),
        "accepted_domain_closing_ref_fields": ACCEPTED_DOMAIN_CLOSING_REF_FIELDS,
        "false_completion_signals": FALSE_COMPLETION_SIGNALS,
        "claim_permissions": {
            "domain_ready": False,
            "grant_ready": False,
            "fundability_ready": False,
            "quality_ready": False,
            "export_ready": False,
            "submission_ready": False,
            "production_ready": False,
        },
        "not_authorized_by": FALSE_COMPLETION_SIGNALS,
        "required_owner_evidence": {
            "domain_closeout": ACCEPTED_DOMAIN_CLOSING_REF_FIELDS,
            "quality_or_export_ready": [
                "mag_owner_receipt_ref",
                "ai_backed_quality_or_export_artifact_ref",
                "mag_owned_typed_blocker_ref",
            ],
            "submission_ready": [
                "submission_ready_human_gate_receipt_ref",
                "mag_owner_receipt_ref",
                "mag_owned_typed_blocker_ref",
            ],
            "temporal_followthrough": [
                "temporal_provider_long_soak_window_evidence_ref",
                "live_receipt_reconciliation_ref",
                "owner_acceptance_or_success_rate_ref",
            ],
        },
        "residual_live_evidence_gaps": [
            "submission_ready_human_gate_receipt",
            "quality_or_export_owner_receipt",
            "temporal_provider_long_soak_window_evidence",
            "app_operator_sustained_consumption",
            "owner_acceptance_or_success_rate_evidence",
        ],
        "source_refs": [
            TEMPORAL_STAGE_RUN_CONSUMPTION_CONTRACT_REF,
            "contracts/live_stage_run_progress_evidence.json",
            "contracts/production_acceptance/mag-production-acceptance.json",
            "docs/status.md",
            "docs/active/mag-ideal-state-cross-repo-gap-plan.md",
        ],
        "authority_boundary": {
            "provider_completion_counts_as_grant_ready": False,
            "schema_completeness_counts_as_grant_ready": False,
            "generated_surface_ready_counts_as_grant_ready": False,
            "focused_tests_count_as_grant_ready": False,
            "stage_replay_counts_as_submission_ready": False,
            "package_existence_counts_as_submission_ready": False,
            "quality_scorecard_counts_as_quality_ready": False,
            "opl_can_write_grant_truth": False,
            "opl_can_sign_mag_owner_receipt": False,
            "mag_can_write_opl_stage_attempts": False,
        },
        "readback_policy": {
            "project_on_temporal_stage_run_consumption_policy": True,
            "project_on_runtime_control": True,
            "project_on_stage_control_plane_closeout": True,
            "project_on_product_status": True,
            "fail_closed_when_owner_closing_ref_missing": True,
        },
    }
