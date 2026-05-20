from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID
from med_autogrant.public_cli import public_cli_command


def build_production_live_acceptance_receipt_surface() -> dict[str, Any]:
    return {
        "surface_kind": "mag_production_live_acceptance_receipt_surface",
        "state": "mag_owner_receipt_projection_available",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "command": public_cli_command(
            "production-live-acceptance-receipt",
            "--owner-receipt-evidence",
            "<owner-receipt-evidence.json>",
            "--agent-lab-suite-result",
            "<agent-lab-suite-result.json>",
            "--meta-agent-coordination-result",
            "<meta-agent-coordination-result.json>",
            "--format",
            "json",
        ),
        "accepted_owner_receipt_shape": "domain_owner_receipt",
        "accepted_closeout_shapes": [
            "domain_owner_receipt",
            "typed_blocker",
        ],
        "required_coordination_refs": [
            "opl_agent_lab_suite_result",
            "opl_meta_agent_external_suite_self_evolution_result",
        ],
        "required_patch_loop_refs": [
            "blocked_suite_result_ref",
            "developer_patch_work_order_ref",
            "patch_traceability_matrix_ref",
            "target_repo_verification_refs",
            "target_runtime_read_model_consumption_ref",
            "workspace_environment_proof_ref",
            "no_forbidden_write_proof_ref",
            "target_owner_receipt_or_typed_blocker_ref",
            "patch_absorption_ref",
            "worktree_cleanup_ref",
            "agent_lab_re_evaluation_ref",
        ],
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "opl_agent_lab_ref_consumer_only": True,
            "meta_agent_work_order_consumer_only": True,
            "can_declare_fundability_ready": False,
            "can_declare_submission_ready_export": False,
        },
    }
