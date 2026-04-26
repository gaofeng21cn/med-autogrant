from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap

_editable_shared_bootstrap.ensure_editable_dependency_paths()

from med_autogrant.control_plane import read_program_id, resolve_runtime_state_root
from med_autogrant.domain_entry_contract import (
    build_domain_entry_contract,
    build_gateway_interaction_contract,
    build_shared_handoff,
)
from med_autogrant.domain_entry import MedAutoGrantDomainEntry
from med_autogrant.hermes_runtime import (
    _build_author_side_route_contract,
    GRANT_COCKPIT_SCHEMA_FILE,
    GRANT_DIRECT_ENTRY_SCHEMA_FILE,
    GRANT_PROGRESS_SCHEMA_FILE,
    GRANT_USER_LOOP_SCHEMA_FILE,
    PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
    PRODUCT_ENTRY_SCHEMA_FILE,
    PRODUCT_FRONTDESK_SCHEMA_FILE,
    _build_executor_routing_contract,
    _build_operator_contract,
    _build_runtime_state_contract,
    _build_runtime_substrate_contract,
    _read_current_program_contract,
    _validate_contract_schema,
    _validate_executor_routing_contract,
)
from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.public_cli import public_cli_command, public_command_label
from med_autogrant.workspace import (
    WorkspaceFileError,
    WorkspaceStateError,
    load_workspace_document,
    validate_workspace_document,
)


def _require_nonempty_string_from_mapping(payload: Mapping[str, Any], field_name: str, *, context: str) -> str:
    value = payload.get(field_name)
    if isinstance(value, str) and value.strip():
        return value.strip()
    raise WorkspaceStateError(f"{context}.{field_name} 必须是非空字符串。")


def _require_mapping(payload: Mapping[str, Any], field_name: str, *, context: str) -> Mapping[str, Any]:
    value = payload.get(field_name)
    if isinstance(value, Mapping):
        return value
    raise WorkspaceStateError(f"{context}.{field_name} 必须是 object。")


def _require_nonempty_string(value: Any, *, field_name: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    raise WorkspaceStateError(f"{field_name} 必须是非空字符串。")


def _optional_mapping(payload: Mapping[str, Any], field_name: str) -> Mapping[str, Any] | None:
    value = payload.get(field_name)
    return value if isinstance(value, Mapping) else None


def _optional_string_from_mapping(payload: Mapping[str, Any] | None, field_name: str) -> str | None:
    if payload is None:
        return None
    value = payload.get(field_name)
    return value.strip() if isinstance(value, str) and value.strip() else None

from opl_harness_shared.managed_runtime import build_managed_runtime_contract as _build_shared_managed_runtime_contract
from opl_harness_shared.family_orchestration import (
    buildFamilyIntakeEvidenceCompanion as _build_shared_family_intake_evidence_companion,
    build_family_product_entry_orchestration as _build_shared_family_product_entry_orchestration,
)
from opl_harness_shared.automation_companions import (
    build_automation_catalog as _build_shared_automation_catalog,
    build_automation_descriptor as _build_shared_automation_descriptor,
)
from opl_harness_shared.product_entry_companions import (
    build_family_product_frontdesk_from_manifest as _build_shared_family_product_frontdesk_from_manifest,
    build_family_product_entry_manifest as _build_shared_family_product_entry_manifest,
    build_operator_loop_action_catalog as _build_shared_operator_loop_action_catalog,
    build_product_entry_start as _build_shared_product_entry_start,
    build_product_entry_overview as _build_shared_product_entry_overview,
    build_product_entry_quickstart as _build_shared_product_entry_quickstart,
    build_product_entry_readiness as _build_shared_product_entry_readiness,
    build_product_entry_resume_surface as _build_shared_product_entry_resume_surface,
    build_product_entry_shell_catalog as _build_shared_product_entry_shell_catalog,
    build_product_entry_shell_linked_surface as _build_shared_product_entry_shell_linked_surface,
    collect_family_human_gate_ids as _collect_family_human_gate_ids,
    validate_family_product_frontdesk as _validate_shared_family_product_frontdesk,
    validate_family_product_entry_manifest as _validate_shared_family_product_entry_manifest,
)
from opl_harness_shared.product_entry_program_companions import (
    build_detailed_readiness as _build_shared_detailed_readiness,
    build_product_entry_preflight as _build_shared_product_entry_preflight,
    build_workflow_coverage_item as _build_shared_workflow_coverage_item,
)
from opl_harness_shared.runtime_task_companions import (
    build_runtime_inventory as _build_shared_runtime_inventory,
    build_task_lifecycle as _build_shared_task_lifecycle,
)
from opl_harness_shared.status_narration import (
    PROGRESS_ANSWER_CHECKLIST,
    build_status_narration_contract,
)
from opl_harness_shared.skill_catalog import (
    build_skill_catalog as _build_shared_skill_catalog,
    build_skill_descriptor as _build_shared_skill_descriptor,
)


PRODUCT_ENTRY_VERSION = 1
PRODUCT_ENTRY_KIND = "med_auto_grant_product_entry"
PRODUCT_ENTRY_MANIFEST_KIND = "med_auto_grant_product_entry_manifest"
PRODUCT_FRONTDESK_KIND = "product_frontdesk"
TARGET_DOMAIN_ID = "med-autogrant"
SUPPORTED_ENTRY_MODES = ("direct", "opl-handoff")
GRANT_PROGRESS_PROJECTION_VERSION = 1
GRANT_PROGRESS_PROJECTION_KIND = "grant_progress"
GRANT_COCKPIT_KIND = "grant_cockpit"
GRANT_DIRECT_ENTRY_VERSION = 1
GRANT_DIRECT_ENTRY_KIND = "grant_direct_entry"
GRANT_USER_LOOP_VERSION = 1
GRANT_USER_LOOP_KIND = "grant_user_loop"
REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}



def _build_runtime_continuity_surfaces(
    *,
    progress_projection: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
    runtime_summary: Mapping[str, Any],
    managed_runtime_contract: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
    funding_call: str,
    grant_progress_command: str,
    summarize_workspace_command: str,
    stage_route_report_command: str,
    grant_user_loop_command: str,
    grant_direct_entry_command: str,
) -> dict[str, dict[str, Any]]:
    session_continuity = _build_session_continuity_surface(
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
    )
    progress_surface = _build_progress_projection_surface(
        projection=dict(progress_projection),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
        inspect_progress_command=grant_progress_command,
        summarize_workspace_command=summarize_workspace_command,
        stage_route_report_command=stage_route_report_command,
    )
    artifact_inventory = _build_artifact_inventory_surface(
        workspace_summary=workspace_summary,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
    )
    runtime_control = _build_runtime_control_surface(
        runtime_summary=runtime_summary,
        managed_runtime_contract=managed_runtime_contract,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        journal_path=_require_nonempty_string_from_mapping(
            session_continuity,
            "journal_path",
            context="session_continuity",
        ),
        runtime_resume_command=_require_nonempty_string_from_mapping(
            _require_mapping(
                _require_mapping(
                    session_continuity,
                    "runtime_entries",
                    context="session_continuity",
                ),
                "runtime_resume",
                context="session_continuity.runtime_entries",
            ),
            "command",
            context="session_continuity.runtime_entries.runtime_resume",
        ),
        funding_call=funding_call,
        grant_progress_command=grant_progress_command,
        summarize_workspace_command=summarize_workspace_command,
        grant_user_loop_command=grant_user_loop_command,
        grant_direct_entry_command=grant_direct_entry_command,
    )
    return {
        "session_continuity": session_continuity,
        "progress_projection": progress_surface,
        "artifact_inventory": artifact_inventory,
        "runtime_control": runtime_control,
    }

def _build_skill_runtime_continuity_envelope(
    *,
    session_continuity: Mapping[str, Any],
    progress_surface: Mapping[str, Any],
    artifact_inventory: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
) -> dict[str, Any]:
    if (
        _require_nonempty_string_from_mapping(
            progress_surface,
            "surface_kind",
            context="progress_surface",
        )
        != "progress_projection"
    ):
        raise WorkspaceStateError("progress_surface 必须是 progress_projection。")
    if (
        _require_nonempty_string_from_mapping(
            artifact_inventory,
            "surface_kind",
            context="artifact_inventory",
        )
        != "artifact_inventory"
    ):
        raise WorkspaceStateError("artifact_inventory 必须是 artifact_inventory。")
    runtime_control_restore_point = _require_mapping(
        runtime_control,
        "restore_point",
        context="runtime_control",
    )
    runtime_control_progress_surface = _require_mapping(
        runtime_control,
        "progress_surface",
        context="runtime_control",
    )
    runtime_control_artifact_surface = _require_mapping(
        runtime_control,
        "artifact_pickup_surface",
        context="runtime_control",
    )
    progress_surface_ref = _require_nonempty_string_from_mapping(
        runtime_control_progress_surface,
        "ref",
        context="runtime_control.progress_surface",
    )
    artifact_surface_ref = _require_nonempty_string_from_mapping(
        runtime_control_artifact_surface,
        "ref",
        context="runtime_control.artifact_pickup_surface",
    )
    semantic_closure = _require_mapping(
        runtime_control,
        "semantic_closure",
        context="runtime_control",
    )
    return {
        "surface_kind": "skill_runtime_continuity",
        "runtime_owner": _require_nonempty_string_from_mapping(
            runtime_control,
            "runtime_owner",
            context="runtime_control",
        ),
        "domain_owner": _require_nonempty_string_from_mapping(
            runtime_control,
            "domain_owner",
            context="runtime_control",
        ),
        "executor_owner": _require_nonempty_string_from_mapping(
            runtime_control,
            "executor_owner",
            context="runtime_control",
        ),
        "authoring_continuity": _require_nonempty_string_from_mapping(
            semantic_closure,
            "authoring_continuity",
            context="runtime_control.semantic_closure",
        ),
        "funding_call_lock": _require_nonempty_string_from_mapping(
            semantic_closure,
            "funding_call_lock",
            context="runtime_control.semantic_closure",
        ),
        "quality_closure_surface": _require_nonempty_string_from_mapping(
            semantic_closure,
            "quality_closure_surface",
            context="runtime_control.semantic_closure",
        ),
        "submission_ready_gate": _require_nonempty_string_from_mapping(
            semantic_closure,
            "submission_ready_gate",
            context="runtime_control.semantic_closure",
        ),
        "session_locator_field": _require_nonempty_string_from_mapping(
            session_continuity,
            "session_locator_field",
            context="session_continuity",
        ),
        "session_surface_ref": "/product_entry_manifest/session_continuity",
        "progress_surface_ref": progress_surface_ref,
        "artifact_surface_ref": artifact_surface_ref,
        "restore_point_surface_ref": "/product_entry_manifest/runtime_control/restore_point",
        "recommended_resume_command": _require_nonempty_string_from_mapping(
            runtime_control_restore_point,
            "resume_command",
            context="runtime_control.restore_point",
        ),
        "recommended_progress_command": _require_nonempty_string_from_mapping(
            runtime_control_progress_surface,
            "command",
            context="runtime_control.progress_surface",
        ),
        "recommended_artifact_command": _require_nonempty_string_from_mapping(
            runtime_control_artifact_surface,
            "command",
            context="runtime_control.artifact_pickup_surface",
        ),
    }


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
            "surface_kind": PRODUCT_FRONTDESK_KIND,
            "command": shell_commands["product_frontdesk"],
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


def _build_session_continuity_surface(
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
) -> dict[str, Any]:
    runtime_state_contract = _build_runtime_state_contract()
    session_journal_root = _require_nonempty_string_from_mapping(
        runtime_state_contract,
        "session_journal_root",
        context="runtime_state_contract",
    )
    journal_path = f"{session_journal_root}{grant_run_id}.json"
    runtime_run_command = public_cli_command(
        "runtime-run",
        "--input",
        input_path,
        "--journal",
        journal_path,
        "--format",
        "json",
    )
    runtime_resume_command = public_cli_command(
        "runtime-resume",
        "--journal",
        journal_path,
        "--format",
        "json",
    )
    return {
        "surface_kind": "session_continuity",
        "version": 1,
        "summary": "显式锚定 session locator 与 journal durable anchor，避免依赖默认 journal 推断。",
        "session_locator_field": "grant_run_id",
        "session_handle_kind": "grant_run_id",
        "session_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "runtime_state_contract": dict(runtime_state_contract),
        "journal_path": journal_path,
        "runtime_entries": {
            "runtime_run": {
                "command": runtime_run_command,
                "surface_kind": "runtime_run",
                "summary": "用显式 --journal 启动或继续当前 workspace 的 runtime run。",
            },
            "runtime_resume": {
                "command": runtime_resume_command,
                "surface_kind": "runtime_resume",
                "summary": "用显式 --journal 恢复当前 session。",
            },
        },
        "repo_owned_truth": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": input_path,
            "truth_owner": TARGET_DOMAIN_ID,
        },
    }

def _build_runtime_control_surface(
    *,
    runtime_summary: Mapping[str, Any],
    managed_runtime_contract: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    journal_path: str,
    runtime_resume_command: str,
    funding_call: str,
    grant_progress_command: str,
    summarize_workspace_command: str,
    grant_user_loop_command: str,
    grant_direct_entry_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "runtime_control",
        "version": 2,
        "summary": (
            "repo-owned runtime control reference：显式导出 owner 语义、restore point、"
            "progress/artifact/approval surface 与 direct-entry locator。"
        ),
        "runtime_owner": _require_nonempty_string_from_mapping(
            runtime_summary,
            "runtime_owner",
            context="runtime_summary",
        ),
        "domain_owner": _require_nonempty_string_from_mapping(
            managed_runtime_contract,
            "domain_owner",
            context="managed_runtime_contract",
        ),
        "executor_owner": _require_nonempty_string_from_mapping(
            managed_runtime_contract,
            "executor_owner",
            context="managed_runtime_contract",
        ),
        "session_locator": {
            "locator_field": "grant_run_id",
            "locator_value": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
        },
        "restore_point": {
            "session_id": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
            "journal_path": journal_path,
            "resume_command": runtime_resume_command,
            "resume_surface_kind": "runtime_resume",
        },
        "semantic_closure": {
            "surface_kind": "runtime_control_semantic_closure",
            "authoring_continuity": "same_funding_call_task",
            "funding_call_lock": _require_nonempty_string(funding_call, field_name="funding_call"),
            "quality_closure_surface": "grant-quality-closure-dossier",
            "submission_ready_gate": "package_submission_ready_strict_export_gate",
            "closure_ref": "/product_entry_manifest/grant_authoring_readiness",
        },
        "progress_surface": {
            "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
            "command": grant_progress_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/progress_projection",
            "summary": "当前 grant progress projection surface。",
        },
        "artifact_pickup_surface": {
            "surface_kind": "artifact_inventory",
            "command": summarize_workspace_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/artifact_inventory",
            "summary": "当前 workspace artifact pickup index surface。",
        },
        "approval_control_surface": {
            "surface_kind": GRANT_USER_LOOP_KIND,
            "command": grant_user_loop_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/operator_loop_surface",
            "summary": "当前人工 gate / control action 入口。",
        },
        "direct_entry": {
            "surface_kind": GRANT_DIRECT_ENTRY_KIND,
            "command": grant_direct_entry_command,
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/product_entry_shell/grant_direct_entry",
            "summary": "直接导出当前 grant direct-entry command 与 locator。",
        },
    }

def _build_progress_projection_surface(
    *,
    projection: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
    inspect_progress_command: str,
    summarize_workspace_command: str,
    stage_route_report_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "progress_projection",
        "version": 1,
        "summary": "repo-owned workspace truth 上的 grant progress projection。",
        "workspace_surface_kind": "nsfc_workspace",
        "workspace_path": input_path,
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "projection_kind": _require_nonempty_string_from_mapping(
            projection,
            "projection_kind",
            context="grant-progress.progress_projection",
        ),
        "projection": dict(projection),
        "truth_anchors": {
            "workspace_document": {
                "ref_kind": "path",
                "ref": input_path,
                "label": "workspace JSON (repo-owned truth)",
            },
            "stage_route_report": {
                "ref_kind": "command",
                "ref": stage_route_report_command,
                "label": "stage-route-report (derives from workspace truth)",
            },
            "summarize_workspace": {
                "ref_kind": "command",
                "ref": summarize_workspace_command,
                "label": "summarize-workspace (derives from workspace truth)",
            },
            "inspect_progress": {
                "ref_kind": "command",
                "ref": inspect_progress_command,
                "label": "grant-progress (projection surface)",
            },
        },
    }

def _build_artifact_inventory_surface(
    *,
    workspace_summary: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
) -> dict[str, Any]:
    artifacts: list[dict[str, Any]] = [
        {
            "artifact_kind": "workspace_document",
            "label": "workspace JSON (repo-owned truth)",
            "ref": {
                "ref_kind": "path",
                "ref": input_path,
            },
        }
    ]

    def _append_workspace_ref(*, artifact_kind: str, label: str, ref: str) -> None:
        artifacts.append(
            {
                "artifact_kind": artifact_kind,
                "label": label,
                "ref": {
                    "ref_kind": "workspace_locator",
                    "ref": ref,
                },
            }
        )

    active_draft = _optional_mapping(workspace_summary, "active_draft")
    if isinstance(active_draft, Mapping):
        draft_id = _optional_string_from_mapping(active_draft, "id")
        if draft_id is not None:
            _append_workspace_ref(
                artifact_kind="active_draft",
                label=f"active draft: {draft_id}",
                ref=f"grant_workspace::{workspace_id}::application_drafts::{draft_id}",
            )

    active_revision_plan = _optional_mapping(workspace_summary, "active_revision_plan")
    if isinstance(active_revision_plan, Mapping):
        revision_plan_id = _optional_string_from_mapping(active_revision_plan, "id")
        if revision_plan_id is not None:
            _append_workspace_ref(
                artifact_kind="active_revision_plan",
                label=f"active revision plan: {revision_plan_id}",
                ref=f"grant_workspace::{workspace_id}::revision_plans::{revision_plan_id}",
            )

    active_critique = _optional_mapping(workspace_summary, "active_critique")
    if isinstance(active_critique, Mapping):
        critique_id = _optional_string_from_mapping(active_critique, "id")
        if critique_id is not None:
            _append_workspace_ref(
                artifact_kind="active_critique",
                label=f"active critique: {critique_id}",
                ref=f"grant_workspace::{workspace_id}::mentor_critiques::{critique_id}",
            )

    selected_direction = _optional_mapping(workspace_summary, "selected_direction")
    if isinstance(selected_direction, Mapping):
        direction_id = _optional_string_from_mapping(selected_direction, "id")
        if direction_id is not None:
            _append_workspace_ref(
                artifact_kind="selected_direction",
                label=f"selected direction: {direction_id}",
                ref=f"grant_workspace::{workspace_id}::direction_hypotheses::{direction_id}",
            )

    selected_question = _optional_mapping(workspace_summary, "selected_question")
    if isinstance(selected_question, Mapping):
        question_id = _optional_string_from_mapping(selected_question, "id")
        if question_id is not None:
            _append_workspace_ref(
                artifact_kind="selected_question",
                label=f"selected question: {question_id}",
                ref=f"grant_workspace::{workspace_id}::scientific_question_cards::{question_id}",
            )

    return {
        "surface_kind": "artifact_inventory",
        "version": 1,
        "summary": "汇总 workspace 内当前被选中的主要对象与 draft 工件，作为 repo-owned continuity truth 的索引。",
        "workspace_surface_kind": "nsfc_workspace",
        "workspace_path": input_path,
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
        "artifacts": artifacts,
    }

def _strip_contract_bundle_fields(surface: dict[str, Any]) -> None:
    surface.pop("schema_ref", None)
    surface.pop("domain_entry_contract", None)
    surface.pop("gateway_interaction_contract", None)

def _build_product_command_catalog(input_path: Path) -> dict[str, str]:
    resolved_input_path = input_path.expanduser().resolve()
    return {
        "grant_progress": public_cli_command(
            "grant-progress", "--input", str(resolved_input_path), "--format", "json"
        ),
        "grant_intake_audit": public_cli_command(
            "grant-intake-audit", "--input", str(resolved_input_path), "--format", "json"
        ),
        "grant_evidence_grounding": public_cli_command(
            "grant-evidence-grounding", "--input", str(resolved_input_path), "--format", "json"
        ),
        "summarize_workspace": public_cli_command(
            "summarize-workspace", "--input", str(resolved_input_path), "--format", "json"
        ),
        "stage_route_report": public_cli_command(
            "stage-route-report", "--input", str(resolved_input_path), "--format", "json"
        ),
        "critique_summary": public_cli_command(
            "critique-summary", "--input", str(resolved_input_path), "--format", "json"
        ),
        "build_direct_entry": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "direct",
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
        "build_opl_handoff": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "opl-handoff",
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
        "build_submission_ready_package": public_cli_command(
            "build-submission-ready-package",
            "--input",
            str(resolved_input_path),
            "--output-dir",
            "<submission-ready-output-dir>",
            "--format",
            "json",
        ),
    }

def _validate_runtime_continuity_alignment(
    *,
    session_continuity: Mapping[str, Any],
    progress_surface: Mapping[str, Any],
    artifact_inventory: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
    projection_truth: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    context_prefix: str,
) -> None:
    if progress_surface.get("projection") != projection_truth:
        raise WorkspaceStateError(
            f"{context_prefix}.progress_projection 与 continuity progress surface 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            session_continuity,
            "session_id",
            context=f"{context_prefix}.session_continuity",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.session_continuity.session_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            progress_surface,
            "grant_run_id",
            context=f"{context_prefix}.progress_projection",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.progress_projection.grant_run_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            artifact_inventory,
            "grant_run_id",
            context=f"{context_prefix}.artifact_inventory",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.artifact_inventory.grant_run_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    runtime_control_session_locator = _require_mapping(
        runtime_control,
        "session_locator",
        context=f"{context_prefix}.runtime_control",
    )
    if (
        _require_nonempty_string_from_mapping(
            runtime_control_session_locator,
            "locator_value",
            context=f"{context_prefix}.runtime_control.session_locator",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.runtime_control.session_locator.locator_value 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    runtime_control_restore_point = _require_mapping(
        runtime_control,
        "restore_point",
        context=f"{context_prefix}.runtime_control",
    )
    if (
        _require_nonempty_string_from_mapping(
            runtime_control_restore_point,
            "session_id",
            context=f"{context_prefix}.runtime_control.restore_point",
        )
        != grant_run_id
    ):
        raise WorkspaceStateError(
            f"{context_prefix}.runtime_control.restore_point.session_id 与 grant_run_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

def _schema_payload_without_contract_bundle(
    payload: Mapping[str, Any],
    *,
    surface_key: str,
) -> dict[str, Any]:
    normalized_payload = dict(payload)
    surface = dict(
        _require_mapping(
            payload,
            surface_key,
            context=f"{surface_key}_schema_validation",
        )
    )
    _strip_contract_bundle_fields(surface)
    nested_manifest = surface.get("product_entry_manifest")
    if isinstance(nested_manifest, Mapping):
        normalized_manifest = dict(nested_manifest)
        _strip_contract_bundle_fields(normalized_manifest)
        surface["product_entry_manifest"] = normalized_manifest
    normalized_payload[surface_key] = surface
    return normalized_payload

__all__ = [name for name in globals() if name.startswith("_") and not name.startswith("__")]
