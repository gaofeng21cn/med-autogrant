from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    PRODUCT_STATUS_KIND,
    TARGET_DOMAIN_ID,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.runtime_defaults import DEFAULT_RUNTIME_OWNER


def _build_opl_runtime_manager_registration(
    *,
    runtime_summary: Mapping[str, Any],
    runtime_continuity: Mapping[str, Any],
    shell_commands: Mapping[str, str],
    skill_catalog_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "opl_runtime_manager_domain_registration",
        "version": "v1",
        "registration_id": "mag.opl_runtime_manager.registration.v1",
        "manager_surface_id": "opl_runtime_manager",
        "domain_id": "medautogrant",
        "domain_owner": TARGET_DOMAIN_ID,
        "runtime_owner": _require_nonempty_string_from_mapping(
            runtime_summary,
            "runtime_owner",
            context="runtime_summary",
        ),
        "executor_owner": "med-autogrant",
        "domain_entry_surface": {
            "surface_kind": PRODUCT_STATUS_KIND,
            "command": shell_commands["product_status"],
            "manifest_command": skill_catalog_command,
        },
        "registration_surface": {
            "surface_kind": "skill_catalog",
            "ref": "/skill_catalog/skills/0/domain_projection/opl_runtime_manager_registration",
            "command": skill_catalog_command,
        },
        "consumable_projection_refs": [
            "/skill_catalog/skills/0/domain_projection/runtime_continuity",
            "/runtime_control/semantic_closure",
            "/artifact_inventory",
            "/automation/automations/1",
        ],
        "state_index_inputs": {
            "workspace_registry_index": "/workspace_locator",
            "managed_session_ledger_index": "/session_continuity",
            "artifact_projection_index": "/artifact_inventory",
            "attention_queue_index": "/automation/automations/1",
            "runtime_health_snapshot_index": "/runtime_inventory",
        },
        "native_helper_consumption": {
            "protocol_ref": "contracts/opl-gateway/native-helper-contract.json",
            "language": "rust",
            "managed_by": "one-person-lab",
            "source_of_truth_rule": (
                "Rust helpers may index MAG workspace, session, artifact, TODO/attention, and runtime-health "
                "surfaces, but MAG author-side grant truth remains authoritative."
            ),
            "proof_surface": _build_opl_native_helper_indexing_proof(),
            "indexes": {
                "workspace_registry_index": {
                    "input_ref": "/workspace_locator",
                    "backing_helper_id": "opl-state-indexer",
                },
                "managed_session_ledger_index": {
                    "input_ref": "/session_continuity",
                    "backing_helper_id": "opl-state-indexer",
                },
                "artifact_projection_index": {
                    "input_ref": "/artifact_inventory",
                    "backing_helper_id": "opl-artifact-indexer",
                },
                "attention_queue_index": {
                    "input_ref": "/automation/automations/1",
                    "backing_helper_id": "opl-state-indexer",
                },
                "runtime_health_snapshot_index": {
                    "input_ref": "/runtime_inventory",
                    "backing_helper_id": "opl-runtime-watch",
                },
            },
        },
        "family_lifecycle_adapter": _build_opl_family_lifecycle_adapter(
            runtime_continuity=runtime_continuity,
            shell_commands=shell_commands,
        ),
        "resume_contract": {
            "session_locator_field": _require_nonempty_string_from_mapping(
                runtime_continuity,
                "session_locator_field",
                context="runtime_continuity",
            ),
            "recommended_resume_command": _require_nonempty_string_from_mapping(
                runtime_continuity,
                "recommended_resume_command",
                context="runtime_continuity",
            ),
            "recommended_progress_command": _require_nonempty_string_from_mapping(
                runtime_continuity,
                "recommended_progress_command",
                context="runtime_continuity",
            ),
        },
        "wakeup_boundary": {
            "owner": TARGET_DOMAIN_ID,
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


def _build_opl_family_lifecycle_adapter(
    *,
    runtime_continuity: Mapping[str, Any],
    shell_commands: Mapping[str, str],
) -> dict[str, Any]:
    recommended_resume_command = _require_nonempty_string_from_mapping(
        runtime_continuity,
        "recommended_resume_command",
        context="runtime_continuity",
    )
    recommended_progress_command = _require_nonempty_string_from_mapping(
        runtime_continuity,
        "recommended_progress_command",
        context="runtime_continuity",
    )
    return {
        "surface_kind": "opl_family_lifecycle_adapter",
        "version": "v1",
        "adapter_id": "mag.opl_family.lifecycle_adapter.v1",
        "contract_refs": {
            "runtime_attempt": "contracts/opl-gateway/family-runtime-attempt-contract.json",
            "product_operator": "contracts/opl-gateway/family-product-operator-projection.json",
            "incident_learning": "contracts/opl-gateway/family-incident-learning-loop.json",
            "adoption": "contracts/runtime-program/opl-family-contract-adoption.json",
        },
        "persistence_projection": {
            "maps_to": "opl_runtime_manager_native_state_projection",
            "source_surface_refs": [
                "/skill_catalog/skills/0/domain_projection/runtime_continuity",
                "/session_continuity",
                "/artifact_inventory",
                "/runtime_control/restore_point",
            ],
            "identity_fields": ["grant_run_id", "workspace_id", "lifecycle_stage"],
            "write_policy": "opl_index_only_no_domain_truth_writes",
            "sqlite_migration_required": False,
        },
        "lifecycle_projection": {
            "maps_to_opl_contract": "opl_family_runtime_attempt_contract.v1",
            "source_surface_refs": [
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
        },
        "owner_route_discovery": {
            "discovery_surface_ref": "/skill_catalog/skills/0/domain_projection/opl_runtime_manager_registration",
            "owner_split": {
                "runtime_manager_owner": "one-person-lab",
                "runtime_kernel_owner": DEFAULT_RUNTIME_OWNER,
                "domain_truth_owner": TARGET_DOMAIN_ID,
                "executor_owner": TARGET_DOMAIN_ID,
            },
            "route_surface_refs": {
                "product_entry": {
                    "surface_kind": PRODUCT_STATUS_KIND,
                    "command": shell_commands["product_status"],
                    "ref": "/product_entry_manifest/product_entry_surface",
                },
                "operator_loop": {
                    "surface_kind": "grant_user_loop",
                    "command": shell_commands["grant_user_loop"],
                    "ref": "/product_entry_manifest/operator_loop_surface",
                },
                "progress": {
                    "surface_kind": "grant_progress",
                    "command": recommended_progress_command,
                    "ref": "/product_entry_manifest/progress_projection",
                },
                "resume": {
                    "surface_kind": "runtime_resume",
                    "command": recommended_resume_command,
                    "ref": "/product_entry_manifest/runtime_control/restore_point",
                },
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
    }


def _build_opl_native_helper_indexing_proof() -> dict[str, Any]:
    return {
        "surface_kind": "opl_native_helper_indexing_proof",
        "version": 1,
        "proof_id": "mag.opl_rust_native_helper.indexing_proof.v1",
        "status": "proof_surface_landed",
        "covered_index_keys": [
            "workspace_registry_index",
            "managed_session_ledger_index",
            "artifact_projection_index",
            "attention_queue_index",
            "runtime_health_snapshot_index",
        ],
        "coverage": {
            "workspace_registry_index": {
                "input_ref": "/workspace_locator",
                "source_surface_kind": "workspace_locator",
                "proof_role": "workspace_registry_indexing",
                "write_policy": "opl_index_only",
            },
            "managed_session_ledger_index": {
                "input_ref": "/session_continuity",
                "source_surface_kind": "session_continuity",
                "proof_role": "session_ledger_indexing",
                "write_policy": "opl_index_only",
            },
            "artifact_projection_index": {
                "input_ref": "/artifact_inventory",
                "source_surface_kind": "artifact_inventory",
                "proof_role": "artifact_projection_indexing",
                "write_policy": "opl_index_only",
            },
            "attention_queue_index": {
                "input_ref": "/automation/automations/1",
                "source_surface_kind": "automation_descriptor",
                "proof_role": "todo_wakeup_indexing",
                "write_policy": "opl_index_only",
            },
            "runtime_health_snapshot_index": {
                "input_ref": "/runtime_inventory",
                "source_surface_kind": "runtime_inventory",
                "proof_role": "runtime_health_indexing",
                "write_policy": "opl_index_only",
            },
        },
        "readonly_boundaries": [
            "rust_helper_outputs_are_opl_indexes_only",
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
    }
