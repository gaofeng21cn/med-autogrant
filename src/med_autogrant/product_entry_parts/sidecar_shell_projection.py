from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_mapping
from med_autogrant.product_entry_parts.sidecar_contract import ALLOWED_ACTIONS
from med_autogrant.product_entry_parts.sidecar_projection import (
    build_attention_queue_projection,
    build_autonomy_controller_projection,
    build_todo_wakeup_projection,
    default_executor_owner,
)


def build_sidecar_caller_owner_contract() -> dict[str, Any]:
    return {
        "active_caller_owner": TARGET_DOMAIN_ID,
        "active_caller_surface": "mag_product_sidecar_handler_until_opl_caller_evidence",
        "target_caller_owner": "one-person-lab",
        "target_caller_surface": "opl_generated_or_hosted_sidecar",
        "domain_handler_target": TARGET_DOMAIN_ID,
        "domain_handler_owner": TARGET_DOMAIN_ID,
        "mag_role": "guarded_domain_handler_target_and_authority_refs_only",
        "claims_fully_cleaned": False,
        "mag_handler_boundary_ready": True,
        "external_opl_generated_or_hosted_caller_evidence_required": True,
    }


def build_sidecar_substrate_boundary(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "online_substrate_owner": "explicit_opl_provider",
        "control_plane_owner": "one-person-lab",
        "domain_truth_owner": TARGET_DOMAIN_ID,
        "quality_gate_owner": TARGET_DOMAIN_ID,
        "artifact_owner": TARGET_DOMAIN_ID,
        "default_executor_owner": default_executor_owner(manifest),
        "default_executor_note": (
            "Default executor remains Codex/domain-selected; OPL may explicitly choose "
            "a stage-led runtime provider for wakeup/control-plane carrier duties."
        ),
        "hermes_proof_executor_default": False,
    }


def build_sidecar_shell_payload(
    *,
    manifest: Mapping[str, Any],
    runtime_registration: Mapping[str, Any],
    automation: Mapping[str, Any],
    autonomy_observability: Mapping[str, Any],
    user_loop_command: str,
) -> dict[str, Any]:
    return {
        "caller_owner_contract": build_sidecar_caller_owner_contract(),
        "substrate_boundary": build_sidecar_substrate_boundary(manifest),
        "todo_wakeup": build_todo_wakeup_projection(
            automation=automation,
            manifest=manifest,
            user_loop_command=user_loop_command,
        ),
        "autonomy_controller": build_autonomy_controller_projection(
            manifest=manifest,
            autonomy_observability=autonomy_observability,
        ),
        "user_loop_attention_queue": build_attention_queue_projection(
            manifest=manifest,
            autonomy_observability=autonomy_observability,
            user_loop_command=user_loop_command,
        ),
        "opl_control_plane": {
            "registration": dict(runtime_registration),
            "family_lifecycle_adapter": dict(
                _require_mapping(
                    runtime_registration,
                    "family_lifecycle_adapter",
                    context="sidecar_export.runtime_registration",
                )
            ),
            "write_policy": "opl_index_only_no_grant_truth_writes",
            "substrate_adapter_export_ref": "/sidecar_export/opl_substrate_adapter_export",
            "allowed_dispatch_actions": sorted(ALLOWED_ACTIONS),
            "replacement_expectations_ref": (
                "/sidecar_export/mag_consumer_thinning_contract/opl_replacement_expectations"
            ),
        },
        "guardrails": {
            "dispatch_boundary": "OPL-hosted caller may invoke only MAG domain handler guarded actions.",
            "forbidden_defaults": [
                "hermes_proof_executor",
                "grant_truth_mutation_by_opl",
                "quality_gate_override_by_opl",
                "submission_ready_gate_bypass",
            ],
        },
    }
