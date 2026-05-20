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
        "required_coordination_refs": [
            "opl_agent_lab_suite_result",
            "opl_meta_agent_external_suite_self_evolution_result",
        ],
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "opl_agent_lab_ref_consumer_only": True,
            "meta_agent_work_order_consumer_only": True,
            "can_declare_fundability_ready": False,
            "can_declare_submission_ready_export": False,
        },
    }
