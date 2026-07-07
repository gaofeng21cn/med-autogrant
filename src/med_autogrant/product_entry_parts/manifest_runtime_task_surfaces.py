from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    GRANT_PROGRESS_PROJECTION_KIND,
    GRANT_USER_LOOP_KIND,
    TARGET_DOMAIN_ID,
    _optional_string_from_mapping,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)
from opl_harness_shared.automation_companions import (
    build_automation_catalog as _build_shared_automation_catalog,
    build_automation_descriptor as _build_shared_automation_descriptor,
)
from opl_harness_shared.runtime_task_companions import (
    build_runtime_inventory as _build_shared_runtime_inventory,
    build_task_lifecycle as _build_shared_task_lifecycle,
)


def _build_runtime_inventory(
    *,
    resolved_input_path: Path,
    progress_payload: Mapping[str, Any],
    product_entry_preflight: Mapping[str, Any],
    runtime_summary: Mapping[str, Any],
    opl_provider_runtime_contract: Mapping[str, Any],
    checkpoint_status: str,
    repo_mainline: Mapping[str, Any],
) -> dict[str, Any]:
    return _build_shared_runtime_inventory(
        summary=(
            "当前 runtime inventory 由 mainline runtime owner、OPL provider runtime contract 与 grant projection "
            "surface 共同构成。"
        ),
        runtime_owner=_require_nonempty_string_from_mapping(
            runtime_summary,
            "runtime_owner",
            context="product_entry_manifest.runtime",
        ),
        domain_owner=_require_nonempty_string_from_mapping(
            opl_provider_runtime_contract,
            "domain_owner",
            context="product_entry_manifest.opl_provider_runtime_contract",
        ),
        executor_owner=_require_nonempty_string_from_mapping(
            opl_provider_runtime_contract,
            "executor_owner",
            context="product_entry_manifest.opl_provider_runtime_contract",
        ),
        substrate=_require_nonempty_string_from_mapping(
            runtime_summary,
            "default_runtime_substrate",
            context="product_entry_manifest.runtime",
        ),
        availability=(
            "ready_to_try_now"
            if bool(product_entry_preflight.get("ready_to_try_now"))
            else "preflight_blocked"
        ),
        health_status="attention_required" if checkpoint_status == "blocked" else "healthy",
        status_surface={
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/product_entry_shell/grant_progress",
            "role": "runtime_status",
            "label": "grant progress projection surface",
        },
        attention_surface={
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/operator_loop_surface",
            "role": "attention_queue",
            "label": "grant user loop attention surface",
        },
        recovery_surface={
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/family_orchestration/resume_contract",
            "role": "recovery_contract",
            "label": "family resume contract surface",
        },
        workspace_binding={
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": str(resolved_input_path),
            "grant_run_id": progress_payload["grant_run_id"],
            "workspace_id": progress_payload["workspace_id"],
            "draft_id": progress_payload["draft_id"],
            "lifecycle_stage": progress_payload["lifecycle_stage"],
        },
        domain_projection={
            "runtime": dict(runtime_summary),
            "opl_provider_runtime_contract": dict(opl_provider_runtime_contract),
            "checkpoint_status": checkpoint_status,
            "repo_mainline": dict(repo_mainline),
        },
    )


def _build_task_lifecycle(
    *,
    progress_payload: Mapping[str, Any],
    checkpoint_status: str,
    grant_user_loop_command: str,
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    family_orchestration: Mapping[str, Any],
    human_gate_ids: list[str],
    continuation_route_id: str,
    continuation_route_status: str,
    continuation_next_action: Mapping[str, Any],
    continuation_action_kind: str,
    verification_checkpoint: Mapping[str, Any],
    verification_identity: Mapping[str, Any],
    repo_mainline: Mapping[str, Any],
) -> dict[str, Any]:
    draft_id = _optional_string_from_mapping(verification_identity, "draft_id")
    return _build_shared_task_lifecycle(
        task_kind="grant_authoring_mainline",
        task_id=f"{progress_payload['workspace_id']}:{draft_id or 'no-draft'}",
        status=checkpoint_status,
        summary=(
            f"当前 checkpoint_status={checkpoint_status}，"
            f"continuation 指向 {continuation_route_id}({continuation_route_status})。"
        ),
        session_id=progress_payload["grant_run_id"],
        run_id=progress_payload["grant_run_id"],
        progress_surface={
            "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
            "summary": operator_loop_actions["inspect_progress"]["summary"],
            "command": operator_loop_actions["inspect_progress"]["command"],
            "step_id": "inspect_progress",
            "locator_fields": ["grant_run_id", "workspace_id", "lifecycle_stage"],
        },
        resume_surface={
            "surface_kind": GRANT_USER_LOOP_KIND,
            "summary": operator_loop_actions["open_loop"]["summary"],
            "command": grant_user_loop_command,
            "step_id": "continue_grant_loop",
            "locator_fields": ["grant_run_id", "lifecycle_stage"],
        },
        checkpoint_summary={
            "status": checkpoint_status,
            "summary": (
                f"verification checkpoint 对齐 {continuation_route_id} route，"
                f"route_status={continuation_route_status}。"
            ),
            "checkpoint_id": (
                f"{progress_payload['workspace_id']}:{draft_id or 'no-draft'}:"
                f"{progress_payload['lifecycle_stage']}"
            ),
            "lineage_ref": dict(
                _require_mapping(
                    family_orchestration,
                    "checkpoint_lineage_surface",
                    context="family_orchestration",
                )
            ),
            "verification_ref": {
                "ref_kind": "json_pointer",
                "ref": "/product_entry_manifest/task_lifecycle/domain_projection/verification_checkpoint",
                "label": "stage route verification checkpoint",
            },
        },
        human_gate_ids=list(human_gate_ids),
        domain_projection={
            "verification_checkpoint": dict(verification_checkpoint),
            "verification_identity": dict(verification_identity),
            "repo_mainline": dict(repo_mainline),
            "family_orchestration": dict(family_orchestration),
            "continuation_next_action": dict(continuation_next_action),
            "continuation_action_kind": continuation_action_kind,
        },
    )


def _build_automation_catalog(
    *,
    grant_authoring_readiness: Mapping[str, Any],
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    command_catalog: Mapping[str, str],
    grant_user_loop_command: str,
    family_orchestration: Mapping[str, Any],
    continuation_route_id: str,
    continuation_route_status: str,
    continuation_next_action: Mapping[str, Any],
    human_gate_ids: list[str],
) -> dict[str, Any]:
    return _build_shared_automation_catalog(
        summary="automation companion 聚合 submission-ready 导出 gate 与 authoring loop continuation 提示。",
        readiness_summary=(
            f"submission_ready={grant_authoring_readiness['fully_automatic']}; "
            f"good_to_use_now={grant_authoring_readiness['good_to_use_now']}"
        ),
        automations=[
            _build_shared_automation_descriptor(
                automation_id="mag.submission_ready_export",
                title="Submission-ready export",
                owner=TARGET_DOMAIN_ID,
                trigger_kind="manual_submission_gate",
                target_surface_kind="submission_ready_package",
                summary=operator_loop_actions["build_submission_ready_package"]["summary"],
                readiness_status=(
                    "agent_assisted"
                    if grant_authoring_readiness["fully_automatic"] is False
                    else "fully_automatic"
                ),
                gate_policy="fail_closed_submission_ready_gate",
                output_expectation=[
                    "输出 submission-ready-package.json",
                    "输出 fail-closed audit summary",
                    "保持 external_submission_performed=false",
                ],
                target_command=command_catalog["build_submission_ready_package"],
                domain_projection={
                    "automation_scope": "local_submission_package",
                    "readiness_verdict": (
                        "submission_ready"
                        if grant_authoring_readiness["fully_automatic"]
                        else "agent_assisted_ready_not_product_grade"
                    ),
                    "requires": ["output_dir", "submission_ready_export_gate"],
                },
            ),
            _build_shared_automation_descriptor(
                automation_id="mag.authoring_loop_continuation",
                title="Authoring loop continuation",
                owner=TARGET_DOMAIN_ID,
                trigger_kind="manual_authoring_resume",
                target_surface_kind=GRANT_USER_LOOP_KIND,
                summary=(
                    f"继续 grant user loop 并推进 {continuation_route_id} route "
                    f"({continuation_route_status})。"
                ),
                readiness_status="landed",
                gate_policy="family_human_gate_resume_contract",
                output_expectation=[
                    "返回 next_action command 或 handoff_surfaces",
                    "保持 route_status 与 checkpoint_status 对齐",
                    "在 human gate 请求时保留人工决策位",
                ],
                target_command=grant_user_loop_command,
                domain_projection={
                    "next_action": dict(continuation_next_action),
                    "human_gate_ids": human_gate_ids,
                    "resume_contract": dict(
                        _require_mapping(
                            family_orchestration,
                            "resume_contract",
                            context="family_orchestration",
                        )
                    ),
                },
            ),
        ],
    )
