from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.product_entry_parts.primitives import (
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_PROGRESS_PROJECTION_KIND,
    GRANT_USER_LOOP_KIND,
    TARGET_DOMAIN_ID,
    _read_funding_call_from_summary,
    _optional_mapping,
    _optional_string_from_mapping,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.product_entry_parts.orchestration_companions import (
    _build_managed_runtime_contract,
)
from med_autogrant.product_entry_parts.runtime_contracts import (
    _build_runtime_state_contract,
)
from med_autogrant.domain_runtime_parts.shared import (
    DOMAIN_AUTHORITY_SURFACE_REF,
    GENERATED_SESSION_RESUME_SURFACE_REF,
    GENERATED_SESSION_SURFACE_REF,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.runtime_defaults import build_default_runtime_summary
from med_autogrant.workspace_types import WorkspaceStateError


def _build_default_runtime_continuity_surfaces(
    *,
    resolved_input_path: Path,
    resolved_task_intent: str | None = None,
    progress_projection: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    grant_user_loop_command: str | None = None,
    grant_direct_entry_command: str | None = None,
) -> dict[str, dict[str, Any]]:
    input_path = str(resolved_input_path)
    task_intent = (
        _require_nonempty_string(resolved_task_intent, field_name="resolved_task_intent")
        if grant_user_loop_command is None or grant_direct_entry_command is None
        else None
    )
    command_catalog = _build_product_command_catalog(resolved_input_path)
    current_line = _require_mapping(
        read_mainline_status(),
        "current_line",
        context="mainline_status",
    )
    runtime_summary = build_default_runtime_summary(
        current_owner_line=_require_nonempty_string_from_mapping(
            current_line,
            "current_owner_line",
            context="mainline_status.current_line",
        )
    )
    return _build_runtime_continuity_surfaces(
        progress_projection=progress_projection,
        workspace_summary=workspace_summary,
        runtime_summary=runtime_summary,
        managed_runtime_contract=_build_managed_runtime_contract(),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        input_path=input_path,
        funding_call=_read_funding_call_from_summary(workspace_summary),
        grant_progress_command=command_catalog["grant_progress"],
        summarize_workspace_command=command_catalog["summarize_workspace"],
        stage_route_report_command=command_catalog["stage_route_report"],
        grant_user_loop_command=grant_user_loop_command
        or public_cli_command(
            "grant-user-loop",
            "--input",
            input_path,
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
        grant_direct_entry_command=grant_direct_entry_command
        or public_cli_command(
            "grant-direct-entry",
            "--input",
            input_path,
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
    )


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
            "resume_surface_ref",
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


def _build_session_continuity_surface(
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
    input_path: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "session_continuity",
        "version": 1,
        "summary": "显式锚定 grant session locator，并把通用 session shell 交给 OPL generated surface。",
        "session_locator_field": "grant_run_id",
        "session_handle_kind": "grant_run_id",
        "session_id": grant_run_id,
        "session_owner": "one-person-lab",
        "generated_session_surface_ref": GENERATED_SESSION_SURFACE_REF,
        "generated_resume_surface_ref": GENERATED_SESSION_RESUME_SURFACE_REF,
        "domain_authority_surface_ref": DOMAIN_AUTHORITY_SURFACE_REF,
        "workspace_id": workspace_id,
        "lifecycle_stage": lifecycle_stage,
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
            "OPL generated runtime/session control reference：MAG 只导出 locator、"
            "progress/artifact/approval surface 与 direct-entry authority refs。"
        ),
        "runtime_owner": "one-person-lab",
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
            "session_owner": "one-person-lab",
            "resume_surface_ref": GENERATED_SESSION_RESUME_SURFACE_REF,
            "resume_surface_kind": "opl_generated_session_resume",
            "domain_authority_surface_ref": DOMAIN_AUTHORITY_SURFACE_REF,
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
    surface.pop("user_interaction_contract", None)

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
        "domain_memory_writeback_proposal": public_cli_command(
            "product-domain-memory-proposal",
            "--input",
            str(resolved_input_path),
            "--stage-id",
            "<stage-id>",
            "--source-ref",
            "<workspace-or-runtime-ref>",
            "--lesson-summary",
            "<strategy-lesson-summary>",
            "--format",
            "json",
        ),
        "domain_memory_writeback_decision": public_cli_command(
            "product-domain-memory-decision",
            "--proposal",
            "<proposal-json>",
            "--decision",
            "<accepted|rejected>",
            "--decision-reason",
            "<decision-reason>",
            "--format",
            "json",
        ),
        "domain_memory_receipt_evidence": public_cli_command(
            "product-domain-memory-receipt-evidence",
            "--decision",
            "<decision-json>",
            "--runtime-root",
            "<runtime-state-root>",
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
