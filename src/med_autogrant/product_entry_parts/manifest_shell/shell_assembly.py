from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.action_catalog import (
    annotate_operator_loop_actions_with_catalog_refs,
    build_mag_family_action_catalog,
    project_mag_family_action_catalog,
)
from med_autogrant.product_entry_parts.orchestration_companions import (
    _build_family_orchestration_companion,
    _build_product_entry_start,
    _route_status_from_route_id,
)
from med_autogrant.product_entry_parts.primitives import (
    GRANT_COCKPIT_KIND,
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_PROGRESS_PROJECTION_KIND,
    GRANT_USER_LOOP_KIND,
    PRODUCT_STATUS_KIND,
    _optional_mapping,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.stage_control_plane import (
    build_mag_family_stage_control_plane,
    build_mag_grant_transition_oracle,
)
from opl_harness_shared.product_entry_companions import (
    build_operator_loop_action_catalog as _build_shared_operator_loop_action_catalog,
    build_product_entry_overview as _build_shared_product_entry_overview,
    build_product_entry_quickstart as _build_shared_product_entry_quickstart,
    build_product_entry_resume_surface as _build_shared_product_entry_resume_surface,
    build_product_entry_shell_catalog as _build_shared_product_entry_shell_catalog,
    build_product_entry_shell_linked_surface as _build_shared_product_entry_shell_linked_surface,
    collect_family_human_gate_ids as _collect_family_human_gate_ids,
)


def build_manifest_shell_assembly(
    *,
    resolved_input_path: Path,
    command_catalog: Mapping[str, str],
    progress_payload: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
    current_focus: Mapping[str, Any],
    mainline_snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    task_intent_placeholder = "<describe-task-intent>"
    grant_user_loop_command = public_cli_command(
        "grant-user-loop",
        "--input",
        str(resolved_input_path),
        "--task-intent",
        task_intent_placeholder,
        "--format",
        "json",
    )
    product_status_command = public_cli_command(
        "product-status", "--input", str(resolved_input_path), "--format", "json"
    )
    grant_cockpit_command = public_cli_command(
        "grant-cockpit", "--input", str(resolved_input_path), "--format", "json"
    )
    grant_direct_entry_command = public_cli_command(
        "grant-direct-entry",
        "--input",
        str(resolved_input_path),
        "--task-intent",
        task_intent_placeholder,
        "--format",
        "json",
    )
    base_operator_loop_actions = _build_base_operator_loop_actions(
        command_catalog=command_catalog,
        grant_user_loop_command=grant_user_loop_command,
        grant_cockpit_command=grant_cockpit_command,
        grant_direct_entry_command=grant_direct_entry_command,
    )
    family_action_catalog = build_mag_family_action_catalog(
        action_commands=base_operator_loop_actions,
    )
    family_stage_control_plane = build_mag_family_stage_control_plane(
        family_action_catalog=family_action_catalog,
    )
    grant_transition_oracle = build_mag_grant_transition_oracle(
        family_stage_control_plane=family_stage_control_plane,
        family_action_catalog=family_action_catalog,
    )
    action_catalog_projections = project_mag_family_action_catalog(family_action_catalog)
    operator_loop_actions = annotate_operator_loop_actions_with_catalog_refs(
        operator_loop_actions=base_operator_loop_actions,
        action_catalog=family_action_catalog,
    )
    family_orchestration = _build_manifest_family_orchestration(
        progress_payload=progress_payload,
        progress_projection=progress_projection,
    )
    product_entry_start = _build_product_entry_start(
        product_status_command=product_status_command,
        grant_user_loop_command=grant_user_loop_command,
        grant_direct_entry_command=grant_direct_entry_command,
        operator_loop_actions=operator_loop_actions,
        family_orchestration=family_orchestration,
    )
    product_entry_quickstart = _build_product_entry_quickstart(
        command_catalog=command_catalog,
        product_status_command=product_status_command,
        grant_user_loop_command=grant_user_loop_command,
        grant_cockpit_command=grant_cockpit_command,
        grant_direct_entry_command=grant_direct_entry_command,
        operator_loop_actions=operator_loop_actions,
        family_orchestration=family_orchestration,
    )
    product_entry_shell = _build_product_entry_shell(
        command_catalog=command_catalog,
        product_status_command=product_status_command,
        grant_user_loop_command=grant_user_loop_command,
        grant_cockpit_command=grant_cockpit_command,
        grant_direct_entry_command=grant_direct_entry_command,
    )
    return {
        "product_status_command": product_status_command,
        "grant_user_loop_command": grant_user_loop_command,
        "grant_cockpit_command": grant_cockpit_command,
        "grant_direct_entry_command": grant_direct_entry_command,
        "base_operator_loop_actions": base_operator_loop_actions,
        "family_action_catalog": family_action_catalog,
        "family_stage_control_plane": family_stage_control_plane,
        "grant_transition_oracle": grant_transition_oracle,
        "action_catalog_projections": action_catalog_projections,
        "operator_loop_actions": operator_loop_actions,
        "family_orchestration": family_orchestration,
        "product_entry_start": product_entry_start,
        "product_entry_quickstart": product_entry_quickstart,
        "product_entry_overview": _build_product_entry_overview(
            command_catalog=command_catalog,
            product_status_command=product_status_command,
            grant_user_loop_command=grant_user_loop_command,
            operator_loop_actions=operator_loop_actions,
            family_orchestration=family_orchestration,
            product_entry_quickstart=product_entry_quickstart,
            current_focus=current_focus,
            mainline_snapshot=mainline_snapshot,
            workspace_summary=workspace_summary,
        ),
        "product_entry_shell": product_entry_shell,
        "product_entry_surface": _build_shared_product_entry_shell_linked_surface(
            shell_key="product_status",
            shell_surface=product_entry_shell["product_status"],
            summary=(
                "OPL generated/hosted status caller 只读消费 MAG handler refs、user loop、projection 与 handoff。"
            ),
        ),
        "operator_loop_surface": _build_shared_product_entry_shell_linked_surface(
            shell_key="grant_user_loop",
            shell_surface=product_entry_shell["grant_user_loop"],
            summary=(
                "当前 operator loop 以 grant-user-loop 作为 direct grant user inbox shell，"
                "在同一入口下汇总 progress、route action 与 mainline snapshot。"
            ),
        ),
        "human_gate_ids": _collect_family_human_gate_ids(family_orchestration),
        "shell_commands": _build_shell_commands(
            product_entry_shell=product_entry_shell,
            command_catalog=command_catalog,
        ),
    }


def _build_base_operator_loop_actions(
    *,
    command_catalog: Mapping[str, str],
    grant_user_loop_command: str,
    grant_cockpit_command: str,
    grant_direct_entry_command: str,
) -> dict[str, Any]:
    return _build_shared_operator_loop_action_catalog(
        {
            "open_loop": {
                "command": grant_user_loop_command,
                "surface_kind": GRANT_USER_LOOP_KIND,
                "summary": "进入当前 direct grant user inbox shell。",
                "requires": [],
            },
            "inspect_progress": {
                "command": command_catalog["grant_progress"],
                "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
                "summary": "读取当前 workspace 的阶段摘要、checkpoint 与下一步。",
                "requires": [],
            },
            "inspect_cockpit": {
                "command": grant_cockpit_command,
                "surface_kind": GRANT_COCKPIT_KIND,
                "summary": "查看主线 snapshot、对象面和当前 route action 汇总。",
                "requires": [],
            },
            "build_direct_entry": {
                "command": grant_direct_entry_command,
                "surface_kind": GRANT_DIRECT_ENTRY_KIND,
                "summary": "把用户意图组合成当前 grant direct-entry contract。",
                "requires": ["task_intent"],
            },
            "build_submission_ready_package": {
                "command": command_catalog["build_submission_ready_package"],
                "surface_kind": "submission_ready_package",
                "summary": "检查 submission-ready gate，并在通过时一次性导出本地交付目录。",
                "requires": ["output_dir"],
            },
        }
    )


def _build_manifest_family_orchestration(
    *,
    progress_payload: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
) -> dict[str, Any]:
    current_route_id = _require_nonempty_string_from_mapping(
        progress_projection,
        "current_stage",
        context="grant-progress.progress_projection",
    )
    recommended_route_id = _require_nonempty_string_from_mapping(
        progress_projection,
        "recommended_next_stage",
        context="grant-progress.progress_projection",
    )
    orchestration_projection = _require_mapping(
        progress_payload,
        "family_orchestration",
        context="grant-progress",
    )
    return _build_family_orchestration_companion(
        current_route_id=current_route_id,
        recommended_route_id=recommended_route_id,
        recommended_route_status=_route_status_from_route_id(recommended_route_id),
        needs_author_decision=bool(progress_projection.get("needs_author_decision")),
        intake_evidence_companion=_optional_mapping(
            orchestration_projection,
            "intake_evidence_companion",
        ),
        project_profile_companion=_optional_mapping(
            orchestration_projection,
            "project_profile_companion",
        ),
        review_surface_ref="/product_entry_manifest/operator_loop_surface",
        event_envelope_surface_ref="/product_entry_manifest/recommended_command",
        checkpoint_lineage_surface_ref="/product_entry_manifest/repo_mainline/active_phase",
        resume_surface_kind=GRANT_USER_LOOP_KIND,
    )


def _build_product_entry_quickstart(
    *,
    command_catalog: Mapping[str, str],
    product_status_command: str,
    grant_user_loop_command: str,
    grant_cockpit_command: str,
    grant_direct_entry_command: str,
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    family_orchestration: Mapping[str, Any],
) -> dict[str, Any]:
    return _build_shared_product_entry_quickstart(
        summary=(
            "先从 OPL-hosted grant status caller 进入 MAG domain handler target，"
            "再回到 grant-user-loop，必要时读取 progress 或 cockpit projection。"
        ),
        recommended_step_id="open_product_entry",
        steps=[
            {
                "step_id": "open_product_entry",
                "title": "Open grant status",
                "command": product_status_command,
                "surface_kind": PRODUCT_STATUS_KIND,
                "summary": "打开当前 direct grant product entry surface。",
                "requires": [],
            },
            {
                "step_id": "continue_grant_loop",
                "title": "Continue current grant loop",
                "command": grant_user_loop_command,
                "surface_kind": GRANT_USER_LOOP_KIND,
                "summary": operator_loop_actions["open_loop"]["summary"],
                "requires": ["task_intent"],
            },
            {
                "step_id": "inspect_progress",
                "title": "Inspect current progress",
                "command": command_catalog["grant_progress"],
                "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
                "summary": operator_loop_actions["inspect_progress"]["summary"],
                "requires": list(operator_loop_actions["inspect_progress"]["requires"]),
            },
            {
                "step_id": "inspect_cockpit",
                "title": "Inspect current cockpit",
                "command": grant_cockpit_command,
                "surface_kind": GRANT_COCKPIT_KIND,
                "summary": operator_loop_actions["inspect_cockpit"]["summary"],
                "requires": list(operator_loop_actions["inspect_cockpit"]["requires"]),
            },
            {
                "step_id": "build_submission_ready_package",
                "title": "Build submission-ready package",
                "command": command_catalog["build_submission_ready_package"],
                "surface_kind": "submission_ready_package",
                "summary": operator_loop_actions["build_submission_ready_package"]["summary"],
                "requires": list(operator_loop_actions["build_submission_ready_package"]["requires"]),
            },
        ],
        resume_contract=dict(family_orchestration["resume_contract"]),
        human_gate_ids=_collect_family_human_gate_ids(family_orchestration),
    )


def _build_product_entry_overview(
    *,
    command_catalog: Mapping[str, str],
    product_status_command: str,
    grant_user_loop_command: str,
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    family_orchestration: Mapping[str, Any],
    product_entry_quickstart: Mapping[str, Any],
    current_focus: Mapping[str, Any],
    mainline_snapshot: Mapping[str, Any],
    workspace_summary: Mapping[str, Any],
) -> dict[str, Any]:
    product_entry_overview = _build_shared_product_entry_overview(
        summary=_require_nonempty_string_from_mapping(
            current_focus,
            "summary",
            context="mainline_status.current_focus",
        ),
        product_entry_command=product_status_command,
        recommended_command=grant_user_loop_command,
        operator_loop_command=grant_user_loop_command,
        progress_surface={
            "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
            "command": command_catalog["grant_progress"],
            "step_id": "inspect_progress",
        },
        resume_surface=_build_shared_product_entry_resume_surface(
            command=grant_user_loop_command,
            resume_contract=family_orchestration["resume_contract"],
        ),
        recommended_step_id=product_entry_quickstart["recommended_step_id"],
        next_focus=list(mainline_snapshot["next_focus"]),
        remaining_gaps_count=len(mainline_snapshot["remaining_gaps"]),
        human_gate_ids=list(product_entry_quickstart["human_gate_ids"]),
    )
    project_profile = _require_mapping(
        workspace_summary,
        "project_profile",
        context="summarize-workspace",
    )
    product_entry_overview.update(
        {
            "project_profile_label": _require_nonempty_string_from_mapping(
                project_profile,
                "profile_label",
                context="summarize-workspace.project_profile",
            ),
            "template_label": _require_nonempty_string_from_mapping(
                project_profile,
                "template_label",
                context="summarize-workspace.project_profile",
            ),
            "critique_policy_id": _require_nonempty_string_from_mapping(
                project_profile,
                "critique_policy_id",
                context="summarize-workspace.project_profile",
            ),
        }
    )
    return product_entry_overview


def _build_product_entry_shell(
    *,
    command_catalog: Mapping[str, str],
    product_status_command: str,
    grant_user_loop_command: str,
    grant_cockpit_command: str,
    grant_direct_entry_command: str,
) -> dict[str, Any]:
    return _build_shared_product_entry_shell_catalog(
        {
            "product_status": {
                "command": product_status_command,
                "surface_kind": PRODUCT_STATUS_KIND,
            },
            "grant_progress": {
                "command": command_catalog["grant_progress"],
                "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
            },
            "grant_cockpit": {
                "command": grant_cockpit_command,
                "surface_kind": GRANT_COCKPIT_KIND,
            },
            "grant_direct_entry": {
                "command": grant_direct_entry_command,
                "surface_kind": GRANT_DIRECT_ENTRY_KIND,
            },
            "grant_user_loop": {
                "command": grant_user_loop_command,
                "surface_kind": GRANT_USER_LOOP_KIND,
            },
        }
    )


def _build_shell_commands(
    *,
    product_entry_shell: Mapping[str, Mapping[str, Any]],
    command_catalog: Mapping[str, str],
) -> dict[str, str]:
    return {
        "product_status": _require_nonempty_string_from_mapping(
            product_entry_shell["product_status"],
            "command",
            context="product_entry_shell.product_status",
        ),
        "grant_progress": _require_nonempty_string_from_mapping(
            product_entry_shell["grant_progress"],
            "command",
            context="product_entry_shell.grant_progress",
        ),
        "grant_cockpit": _require_nonempty_string_from_mapping(
            product_entry_shell["grant_cockpit"],
            "command",
            context="product_entry_shell.grant_cockpit",
        ),
        "grant_direct_entry": _require_nonempty_string_from_mapping(
            product_entry_shell["grant_direct_entry"],
            "command",
            context="product_entry_shell.grant_direct_entry",
        ),
        "grant_user_loop": _require_nonempty_string_from_mapping(
            product_entry_shell["grant_user_loop"],
            "command",
            context="product_entry_shell.grant_user_loop",
        ),
        "domain_memory_writeback_proposal": command_catalog["domain_memory_writeback_proposal"],
        "domain_memory_writeback_decision": command_catalog["domain_memory_writeback_decision"],
        "domain_memory_receipt_evidence": command_catalog["domain_memory_receipt_evidence"],
    }
