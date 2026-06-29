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
OPL_OWNED_SUBSTRATE_SURFACES = [
    "generated_shell",
    "product_status_shell",
    "user_loop_shell",
    "direct_entry_shell",
    "domain_handler_shell",
    "operator_workbench_shell",
    "temporal_stage_run_substrate",
    "typed_queue",
    "stage_run_attempt_provenance",
    "provider_scheduler",
]
MAG_RETAINED_AUTHORITY_SURFACES = [
    "grant_native_domain_entry",
    "schema_backed_authoring_contract",
    "fundability_quality_export_verdict",
    "submission_package_authority",
    "memory_accept_reject",
    "owner_receipt",
    "typed_blocker",
]
FORBIDDEN_MAG_SUBSTRATE_ROLES = [
    "private_runner",
    "private_queue",
    "temporal_wrapper",
    "status_shell_owner",
    "user_loop_shell_owner",
    "direct_entry_shell_owner",
    "domain_handler_shell_owner",
    "workbench_owner",
    "stage_run_attempt_provenance_owner",
    "provider_scheduler_owner",
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
        "stage_run_substrate_owner": "one-person-lab",
        "stage_run_owner_surface": "opl_temporal_stage_run_kernel",
        "domain_role": "refs_only_consumer_and_grant_authority",
        "domain_truth_owner": TARGET_DOMAIN_ID,
        "temporal_attempt_ledger_owner": TEMPORAL_ATTEMPT_LEDGER_OWNER,
        "opl_owned_substrate_surfaces": OPL_OWNED_SUBSTRATE_SURFACES,
        "mag_retained_authority_surfaces": MAG_RETAINED_AUTHORITY_SURFACES,
        "forbidden_mag_substrate_roles": FORBIDDEN_MAG_SUBSTRATE_ROLES,
        "provider_completion_is_domain_completion": False,
        "domain_repo_can_own_temporal_runtime": False,
        "domain_repo_can_write_opl_stage_attempts": False,
        "domain_repo_can_own_stage_run_substrate": False,
        "mag_can_own_status_user_loop_direct_entry_domain_handler_or_workbench_shell": False,
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
        "stage_run_consumption_boundary": {
            "surface_kind": "mag_stage_run_consumption_boundary",
            "owner": TARGET_DOMAIN_ID,
            "consumer_role": "consume_opl_stage_run_refs_only",
            "opl_substrate_owner": "one-person-lab",
            "stage_run_owner_surface": "opl_temporal_stage_run_kernel",
            "payload_body_allowed": False,
            "mag_runtime_state_write_allowed": False,
            "accepted_consumed_ref_fields": [
                "temporal_stage_run_ref",
                "provider_attempt_ref",
                "provider_completion_ref",
                "stage_attempt_ref",
            ],
            "accepted_domain_closing_ref_fields": ACCEPTED_DOMAIN_CLOSING_REF_FIELDS,
            "authority_boundary": {
                "mag_can_start_temporal_worker": False,
                "mag_can_schedule_stage_run": False,
                "mag_can_write_attempt_ledger": False,
                "mag_can_own_generated_shell": False,
                "opl_can_write_grant_truth": False,
                "opl_can_sign_mag_owner_receipt": False,
                "provider_completion_counts_as_domain_completion": False,
            },
        },
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
            "project_on_stage_run_substrate_boundary": True,
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
            "stage_run_domain_closeout": ACCEPTED_DOMAIN_CLOSING_REF_FIELDS,
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
