from __future__ import annotations

from med_autogrant.product_entry_parts.primitives import PRODUCT_STATUS_KIND, TARGET_DOMAIN_ID
from med_autogrant.runtime_defaults import (
    DEFAULT_EXECUTOR_OWNER,
    NON_DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE,
    OPL_AGENT_EXECUTION_RECEIPT_CONTRACT,
    OPL_AGENT_EXECUTION_REQUEST_CONTRACT,
    OPL_EXECUTOR_ADAPTER_CONTRACT_REF,
    OPL_EXECUTOR_ADAPTER_OWNER,
)


_INDEXES = {
    "workspace_registry_index": {
        "input_ref": "/workspace_locator",
        "source_surface_kind": "workspace_locator",
        "write_policy": "opl_index_only",
    },
    "managed_session_ledger_index": {
        "input_ref": "/session_continuity",
        "source_surface_kind": "session_continuity",
        "write_policy": "opl_index_only",
    },
    "artifact_projection_index": {
        "input_ref": "/artifact_inventory",
        "source_surface_kind": "artifact_inventory",
        "write_policy": "opl_index_only",
    },
    "attention_queue_index": {
        "input_ref": "/automation/automations/1",
        "source_surface_kind": "automation_descriptor",
        "write_policy": "opl_index_only",
    },
    "runtime_health_snapshot_index": {
        "input_ref": "/runtime_inventory",
        "source_surface_kind": "runtime_inventory",
        "write_policy": "opl_index_only",
    },
}

MAG_STAGE_RUNTIME_REGISTRATION_PROFILE = {
    "surface_kind": "opl_stage_runtime_domain_registration",
    "version": "v1",
    "registration_id": "mag.opl_stage_runtime.registration.v1",
    "manager_surface_id": "opl_stage_runtime",
    "domain_id": "medautogrant",
    "domain_owner": TARGET_DOMAIN_ID,
    "product_status_kind": PRODUCT_STATUS_KIND,
    "executor_owner": DEFAULT_EXECUTOR_OWNER,
    "executor_adapter_owner": OPL_EXECUTOR_ADAPTER_OWNER,
    "executor_adapter_contract": {
        "contract_ref": OPL_EXECUTOR_ADAPTER_CONTRACT_REF,
        "registry_surface_kind": "opl_agent_executor_registry",
        "request_contract": OPL_AGENT_EXECUTION_REQUEST_CONTRACT,
        "receipt_contract": OPL_AGENT_EXECUTION_RECEIPT_CONTRACT,
        "canonical_executor_backends": ["codex_cli", "hermes_agent", "claude_code"],
        "default_executor": DEFAULT_EXECUTOR_OWNER,
        "non_default_equivalence": NON_DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE,
        "fallback_allowed": False,
    },
    "consumable_projection_refs": [
        "/skill_catalog/skills/0/domain_projection/runtime_continuity",
        "/runtime_control/semantic_closure",
        "/artifact_inventory",
        "/automation/automations/1",
    ],
    "state_index_inputs": {
        key: value["input_ref"] for key, value in _INDEXES.items()
    },
    "native_helper": {
        "protocol_ref": "contracts/opl-framework/native-helper-contract.json",
        "managed_by": "one-person-lab",
        "source_of_truth_rule": (
            "OPL-owned helpers may index MAG workspace, session, artifact, TODO/attention, and "
            "runtime-health refs, but MAG author-side grant truth remains authoritative."
        ),
        "index_consumption_policy": "opl_index_only_no_domain_truth_writes",
        "indexes": _INDEXES,
        "proof": {
            "surface_kind": "opl_native_helper_ref_consumption_proof",
            "version": 1,
            "proof_id": "mag.opl_native_helper.ref_consumption_proof.v1",
            "status": "refs_only_contract_landed",
            "covered_index_keys": list(_INDEXES),
            "readonly_boundaries": [
                "opl_helper_outputs_are_opl_indexes_only",
                "mag_repo_tracked_truth_remains_authoritative",
                "quality_gate_remains_mag_owned",
                "submission_ready_gate_remains_mag_owned",
            ],
            "authoritative_surfaces": [
                "contracts/runtime-program/current-program.json",
                "runtime_control.semantic_closure",
                "skill_catalog.domain_projection.runtime_continuity",
                "package submission-ready",
            ],
        },
    },
    "family_lifecycle": {
        "surface_kind": "opl_family_lifecycle_adapter",
        "version": "v1",
        "adapter_id": "mag.opl_family.lifecycle_adapter.v1",
        "contract_refs": {
            "runtime_attempt": "contracts/opl-framework/family-runtime-attempt-contract.json",
            "product_operator": "contracts/opl-framework/family-product-operator-projection.json",
            "incident_learning": "contracts/opl-framework/family-incident-learning-loop.json",
            "adoption": "contracts/runtime-program/opl-family-contract-adoption.json",
        },
        "persistence_maps_to": "opl_stage_runtime_native_state_projection",
        "persistence_source_refs": [
            "/skill_catalog/skills/0/domain_projection/runtime_continuity",
            "/session_continuity",
            "/artifact_inventory",
            "/runtime_control/restore_point",
        ],
        "identity_fields": ["grant_run_id", "workspace_id", "lifecycle_stage"],
        "runtime_attempt_contract": "opl_family_runtime_attempt_contract.v1",
        "lifecycle_source_refs": [
            "/runtime_control",
            "/task_lifecycle",
            "/progress_projection",
            "/skill_catalog/skills/0/domain_projection/runtime_continuity",
        ],
        "required_projection_fields": [
            "attempt_state",
            "attempt_count",
            "retry_policy",
            "workspace_boundary",
            "owner_repo",
            "failure_reason",
            "reconciliation_status",
            "last_observed_projection",
        ],
        "state_mapping": {
            "running": "task_lifecycle.status",
            "blocked": "task_lifecycle.checkpoint_summary.status",
            "last_observed_projection": "progress_projection",
        },
        "discovery_surface_ref": (
            "/skill_catalog/skills/0/domain_projection/opl_stage_runtime_registration"
        ),
        "route_surfaces": {
            "product_entry": {
                "surface_kind": PRODUCT_STATUS_KIND,
                "command_key": "product_status",
                "ref": "/product_entry_manifest/product_entry_surface",
            },
            "operator_loop": {
                "surface_kind": "grant_user_loop",
                "command_key": "grant_user_loop",
                "ref": "/product_entry_manifest/operator_loop_surface",
            },
            "progress": {
                "surface_kind": "grant_progress",
                "command_key": "recommended_progress_command",
                "ref": "/product_entry_manifest/progress_projection",
            },
            "resume": {
                "surface_kind": "opl_generated_session_resume",
                "command_key": "recommended_resume_command",
                "ref": "/product_entry_manifest/runtime_control/restore_point",
            },
        },
        "adoption_projection": {
            "maps_to_opl_contract": "opl_family_product_operator_projection.v1",
            "source_refs": [
                "/product_entry_manifest/runtime_control",
                "/product_entry_manifest/task_lifecycle",
                "/product_entry_manifest/progress_projection",
                "/product_entry_manifest/artifact_inventory",
                "/product_entry_manifest/operator_loop_surface",
            ],
            "required_operator_fields": [
                "source_refs",
                "freshness",
                "owner_split",
                "next_surface_ref",
                "human_gate_reason",
            ],
            "next_surface_ref": "/product_entry_manifest/operator_loop_surface",
        },
        "adoption_surface": {
            "contract_kind": "mag_opl_family_contract_adoption.v1",
            "contract_ref": "contracts/runtime-program/opl-family-contract-adoption.json",
            "opl_role": "family-level projection consumer only",
        },
        "non_goals": [
            "no_runtime_reshape",
            "no_sqlite_migration",
            "no_opl_grant_truth_ownership",
            "no_submission_ready_gate_bypass",
        ],
    },
    "wakeup_policy": {
        "surface_ref": "/automation/automations/1",
        "policy": "explicit_authoring_loop_continuation",
    },
    "non_goals": [
        "not_a_grant_truth_owner",
        "not_a_quality_gate",
        "not_a_submission_ready_export_gate",
        "not_a_concrete_authoring_executor",
    ],
}


__all__ = ["MAG_STAGE_RUNTIME_REGISTRATION_PROFILE"]
