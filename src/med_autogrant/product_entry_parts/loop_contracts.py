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
from med_autogrant.product_entry_parts.runtime_contracts import (
    GRANT_COCKPIT_SCHEMA_FILE,
    GRANT_DIRECT_ENTRY_SCHEMA_FILE,
    GRANT_PROGRESS_SCHEMA_FILE,
    GRANT_USER_LOOP_SCHEMA_FILE,
    PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
    PRODUCT_ENTRY_SCHEMA_FILE,
    PRODUCT_FRONTDESK_SCHEMA_FILE,
    _build_author_side_route_contract,
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
    load_workspace_document,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError
from med_autogrant.workspace_validation import validate_workspace_document


def _read_nonempty_string_list(value: Any, *, context: str) -> list[str]:
    if not isinstance(value, list):
        raise WorkspaceStateError(f"{context} 必须为 list。")
    strings = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if len(strings) != len(value):
        raise WorkspaceStateError(f"{context} 必须只包含非空字符串。")
    return strings

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


from med_autogrant.product_entry_parts.runtime_surfaces import (
    _schema_payload_without_contract_bundle,
    _validate_runtime_continuity_alignment,
)
from med_autogrant.product_entry_parts.primitives import (
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)

def _validate_grant_direct_entry_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_contract_schema(
        payload,
        schema_file=GRANT_DIRECT_ENTRY_SCHEMA_FILE,
        context="grant_direct_entry",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    grant_direct_entry = _require_mapping(
        payload,
        "grant_direct_entry",
        context="grant_direct_entry",
    )
    direct_entry = _require_mapping(
        grant_direct_entry,
        "direct_entry",
        context="grant_direct_entry.direct_entry",
    )
    opl_handoff_entry = _require_mapping(
        grant_direct_entry,
        "opl_handoff_entry",
        context="grant_direct_entry.opl_handoff_entry",
    )
    if (
        _require_nonempty_string_from_mapping(
            direct_entry,
            "entry_mode",
            context="grant_direct_entry.direct_entry",
        )
        != "direct"
    ):
        raise WorkspaceStateError(
            "grant_direct_entry.direct_entry.entry_mode 必须为 direct。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if (
        _require_nonempty_string_from_mapping(
            opl_handoff_entry,
            "entry_mode",
            context="grant_direct_entry.opl_handoff_entry",
        )
        != "opl-handoff"
    ):
        raise WorkspaceStateError(
            "grant_direct_entry.opl_handoff_entry.entry_mode 必须为 opl-handoff。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    direct_task_intent = _require_nonempty_string_from_mapping(
        direct_entry,
        "task_intent",
        context="grant_direct_entry.direct_entry",
    )
    opl_handoff_task_intent = _require_nonempty_string_from_mapping(
        opl_handoff_entry,
        "task_intent",
        context="grant_direct_entry.opl_handoff_entry",
    )
    task_intent = _require_nonempty_string_from_mapping(
        grant_direct_entry,
        "task_intent",
        context="grant_direct_entry",
    )
    if direct_task_intent != task_intent:
        raise WorkspaceStateError(
            "grant_direct_entry.direct_entry.task_intent 与顶层 direct entry contract 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if opl_handoff_task_intent != task_intent:
        raise WorkspaceStateError(
            "grant_direct_entry.opl_handoff_entry.task_intent 与顶层 direct entry contract 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    current_stage_route = _require_mapping(
        grant_direct_entry,
        "current_stage_route",
        context="grant_direct_entry",
    )
    recommended_executor_route = _require_mapping(
        grant_direct_entry,
        "recommended_executor_route",
        context="grant_direct_entry",
    )
    direct_executor_routing_contract = _require_mapping(
        direct_entry,
        "executor_routing_contract",
        context="grant_direct_entry.direct_entry",
    )
    opl_executor_routing_contract = _require_mapping(
        opl_handoff_entry,
        "executor_routing_contract",
        context="grant_direct_entry.opl_handoff_entry",
    )
    if direct_executor_routing_contract.get("current_stage_route") != current_stage_route:
        raise WorkspaceStateError(
            "grant_direct_entry.current_stage_route 与 direct entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if direct_executor_routing_contract.get("recommended_executor_route") != recommended_executor_route:
        raise WorkspaceStateError(
            "grant_direct_entry.recommended_executor_route 与 direct entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if opl_executor_routing_contract.get("current_stage_route") != current_stage_route:
        raise WorkspaceStateError(
            "grant_direct_entry.current_stage_route 与 opl_handoff entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if opl_executor_routing_contract.get("recommended_executor_route") != recommended_executor_route:
        raise WorkspaceStateError(
            "grant_direct_entry.recommended_executor_route 与 opl_handoff entry route truth 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    _validate_runtime_continuity_alignment(
        session_continuity=_require_mapping(
            payload,
            "session_continuity",
            context="grant_direct_entry",
        ),
        progress_surface=_require_mapping(
            payload,
            "progress_projection",
            context="grant_direct_entry",
        ),
        artifact_inventory=_require_mapping(
            payload,
            "artifact_inventory",
            context="grant_direct_entry",
        ),
        runtime_control=_require_mapping(
            payload,
            "runtime_control",
            context="grant_direct_entry",
        ),
        projection_truth=_require_mapping(
            grant_direct_entry,
            "progress_projection",
            context="grant_direct_entry",
        ),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        context_prefix="grant_direct_entry",
    )

def _build_mainline_snapshot(mainline_status: Mapping[str, Any]) -> dict[str, Any]:
    current_line = _require_mapping(
        mainline_status,
        "current_line",
        context="mainline_status",
    )
    current_focus = _require_mapping(
        mainline_status,
        "current_focus",
        context="mainline_status",
    )
    maintainer_references = _require_mapping(
        mainline_status,
        "maintainer_references",
        context="mainline_status",
    )
    current_runtime_owner = _require_mapping(
        maintainer_references,
        "runtime_owner",
        context="mainline_status.maintainer_references",
    )
    phase_ladder = maintainer_references.get("phase_ladder")
    if not isinstance(phase_ladder, list):
        raise WorkspaceStateError("mainline_status.maintainer_references.phase_ladder 必须为 list。")
    return {
        "current_owner_line": _require_nonempty_string_from_mapping(
            current_line,
            "current_owner_line",
            context="mainline_status.current_line",
        ),
        "active_phase": _require_nonempty_string_from_mapping(
            current_runtime_owner,
            "active_phase",
            context="mainline_status.maintainer_references.runtime_owner",
        ),
        "active_tranche": _require_nonempty_string_from_mapping(
            current_runtime_owner,
            "active_tranche",
            context="mainline_status.maintainer_references.runtime_owner",
        ),
        "phase_map": [
            {
                "phase_id": _require_nonempty_string_from_mapping(item, "phase_id", context="mainline_status.phase_ladder"),
                "phase_name": _require_nonempty_string_from_mapping(item, "phase_name", context="mainline_status.phase_ladder"),
                "status": _require_nonempty_string_from_mapping(item, "status", context="mainline_status.phase_ladder"),
            }
            for item in phase_ladder
            if isinstance(item, Mapping)
        ],
        "next_focus": _read_nonempty_string_list(
            current_focus.get("focus_items"),
            context="mainline_status.current_focus.focus_items",
        ),
        "remaining_gaps": _read_nonempty_string_list(
            mainline_status.get("remaining_gaps"),
            context="mainline_status.remaining_gaps",
        ),
    }

def _build_next_action_payload(
    *,
    recommended_executor_route: Mapping[str, Any],
    input_path: Path,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> dict[str, Any]:
    route_id = _require_nonempty_string_from_mapping(
        recommended_executor_route,
        "route_id",
        context="grant_user_loop.recommended_executor_route",
    )
    route_status = _require_nonempty_string_from_mapping(
        recommended_executor_route,
        "route_status",
        context="grant_user_loop.recommended_executor_route",
    )
    if route_status == "landed":
        return {
            "action_kind": "execute_landed_route",
            "route_id": route_id,
            "route_status": route_status,
            "summary": f"当前推荐 route {route_id} 已 landed，可直接调用现有 author-side executor surface。",
            "command": _build_route_execution_command(
                route_id=route_id,
                input_path=input_path,
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                draft_id=draft_id,
            ),
            "handoff_surfaces": None,
        }

    raise WorkspaceStateError(
        f"grant_user_loop 只接受已 landed 的 route contract，收到 {route_id}({route_status})。",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=route_id,
    )

def _build_route_execution_command(
    *,
    route_id: str,
    input_path: Path,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> str:
    resolved_input_path = input_path.expanduser().resolve()
    output_path = _build_runtime_route_output_path(
        route_id=route_id,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        draft_id=draft_id,
    )
    if route_id == "direction_screening":
        return public_cli_command(
            "execute-direction-screening-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "question_refinement":
        return public_cli_command(
            "execute-question-refinement-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "argument_building":
        return public_cli_command(
            "execute-argument-building-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "fit_alignment":
        return public_cli_command(
            "execute-fit-alignment-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "outline":
        return public_cli_command(
            "execute-outline-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "drafting":
        return public_cli_command(
            "execute-drafting-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "critique":
        return public_cli_command(
            "execute-critique-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "revision":
        return public_cli_command(
            "execute-revision-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "frozen":
        return public_cli_command(
            "execute-freeze-pass",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "artifact_bundle":
        return public_cli_command(
            "build-artifact-bundle",
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "final_package":
        artifact_bundle_path = _build_runtime_route_output_path(
            route_id="artifact_bundle",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            draft_id=draft_id,
        )
        return public_cli_command(
            "build-final-package",
            "--input",
            str(resolved_input_path),
            "--artifact-bundle",
            str(artifact_bundle_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "hosted_contract_bundle":
        final_package_path = _build_runtime_route_output_path(
            route_id="final_package",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            draft_id=draft_id,
        )
        return public_cli_command(
            "build-hosted-contract-bundle",
            "--final-package",
            str(final_package_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    raise WorkspaceStateError(f"grant_user_loop 不支持 landed route command: {route_id}")

def _build_runtime_route_output_path(
    *,
    route_id: str,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> Path:
    output_file = {
        "direction_screening": "direction-screening-workspace.json",
        "question_refinement": "question-refinement-workspace.json",
        "argument_building": "argument-building-workspace.json",
        "fit_alignment": "fit-alignment-workspace.json",
        "outline": "outline-workspace.json",
        "drafting": "drafting-workspace.json",
        "critique": "critique-workspace.json",
        "revision": "revision-workspace.json",
        "frozen": "frozen-workspace.json",
        "artifact_bundle": "artifact-bundle.json",
        "final_package": "final-package.json",
        "hosted_contract_bundle": "hosted-contract-bundle.json",
    }.get(route_id)
    if output_file is None:
        raise WorkspaceStateError(f"grant_user_loop 不支持 runtime output path route: {route_id}")

    program_id = _require_runtime_path_segment(read_program_id(), field_name="program_id")
    return (
        resolve_runtime_state_root()
        / "reports"
        / program_id
        / _require_runtime_path_segment(grant_run_id, field_name="grant_run_id")
        / _require_runtime_path_segment(workspace_id, field_name="workspace_id")
        / _require_runtime_path_segment(draft_id or "no-draft", field_name="draft_id")
        / output_file
    ).resolve()

def _require_runtime_path_segment(value: str, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"grant_user_loop runtime output path 缺少合法字段: {field_name}")
    resolved_value = value.strip()
    if resolved_value in {".", ".."} or "/" in resolved_value or "\\" in resolved_value:
        raise WorkspaceStateError(f"grant_user_loop runtime output path 字段不能包含路径分隔符: {field_name}")
    return resolved_value

def _build_grant_user_loop_commands(
    *,
    input_path: Path,
    task_intent: str,
    run_recommended_route: Any,
) -> dict[str, Any]:
    resolved_input_path = input_path.expanduser().resolve()
    return {
        "mainline_status": public_cli_command("mainline-status", "--format", "json"),
        "phase_status_current": public_cli_command("mainline-phase", "--phase", "current", "--format", "json"),
        "phase_status_next": public_cli_command("mainline-phase", "--phase", "next", "--format", "json"),
        "open_grant_cockpit": public_cli_command(
            "grant-cockpit", "--input", str(resolved_input_path), "--format", "json"
        ),
        "open_grant_direct_entry": public_cli_command(
            "grant-direct-entry",
            "--input",
            str(resolved_input_path),
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
        "run_recommended_route": (
            _require_nonempty_string(run_recommended_route, field_name="run_recommended_route")
            if run_recommended_route is not None
            else None
        ),
        "build_direct_entry": public_cli_command(
            "build-product-entry",
            "--input",
            str(resolved_input_path),
            "--entry-mode",
            "direct",
            "--task-intent",
            task_intent,
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
            task_intent,
            "--format",
            "json",
        ),
    }

def _validate_grant_user_loop_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_contract_schema(
        payload,
        schema_file=GRANT_USER_LOOP_SCHEMA_FILE,
        context="grant_user_loop",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    grant_user_loop = _require_mapping(
        payload,
        "grant_user_loop",
        context="grant_user_loop",
    )
    grant_direct_entry = _require_mapping(
        grant_user_loop,
        "grant_direct_entry",
        context="grant_user_loop.grant_direct_entry",
    )
    if (
        _require_nonempty_string_from_mapping(
            grant_user_loop,
            "task_intent",
            context="grant_user_loop",
        )
        != _require_nonempty_string_from_mapping(
            grant_direct_entry,
            "task_intent",
            context="grant_user_loop.grant_direct_entry",
        )
    ):
        raise WorkspaceStateError(
            "grant_user_loop.task_intent 与 grant_direct_entry.task_intent 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    next_action = _require_mapping(
        grant_user_loop,
        "next_action",
        context="grant_user_loop.next_action",
    )
    recommended_executor_route = _require_mapping(
        grant_direct_entry,
        "recommended_executor_route",
        context="grant_user_loop.grant_direct_entry",
    )
    _validate_runtime_continuity_alignment(
        session_continuity=_require_mapping(
            grant_user_loop,
            "session_continuity",
            context="grant_user_loop.session_continuity",
        ),
        progress_surface=_require_mapping(
            grant_user_loop,
            "progress_projection",
            context="grant_user_loop.progress_projection",
        ),
        artifact_inventory=_require_mapping(
            grant_user_loop,
            "artifact_inventory",
            context="grant_user_loop.artifact_inventory",
        ),
        runtime_control=_require_mapping(
            grant_user_loop,
            "runtime_control",
            context="grant_user_loop.runtime_control",
        ),
        projection_truth=_require_mapping(
            grant_direct_entry,
            "progress_projection",
            context="grant_user_loop.grant_direct_entry",
        ),
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        context_prefix="grant_user_loop",
    )
    if next_action.get("route_id") != recommended_executor_route.get("route_id"):
        raise WorkspaceStateError(
            "grant_user_loop.next_action.route_id 与 grant_direct_entry.recommended_executor_route.route_id 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if next_action.get("route_status") != recommended_executor_route.get("route_status"):
        raise WorkspaceStateError(
            "grant_user_loop.next_action.route_status 与 grant_direct_entry.recommended_executor_route.route_status 不一致。",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    action_kind = _require_nonempty_string_from_mapping(
        next_action,
        "action_kind",
        context="grant_user_loop.next_action",
    )
    command = next_action.get("command")
    handoff_surfaces = next_action.get("handoff_surfaces")
    if action_kind == "execute_landed_route":
        if not isinstance(command, str) or not command.strip():
            raise WorkspaceStateError(
                "grant_user_loop.next_action.command 必须在 landed route 时非空。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )
        if handoff_surfaces is not None:
            raise WorkspaceStateError(
                "grant_user_loop.next_action.handoff_surfaces 必须在 landed route 时为空。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )
    elif action_kind != "execute_landed_route":
        raise WorkspaceStateError(
            f"grant_user_loop.next_action.action_kind 非法: {action_kind}",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

def _validate_product_entry_manifest_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_shared_family_product_entry_manifest(
        payload["product_entry_manifest"],
        require_contract_bundle=True,
        require_runtime_companions=True,
    )
    _validate_contract_schema(
        _schema_payload_without_contract_bundle(payload, surface_key="product_entry_manifest"),
        schema_file=PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE,
        context="product_entry_manifest",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )

def _validate_product_frontdesk_contract(
    payload: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    _validate_shared_family_product_frontdesk(
        payload["product_frontdesk"],
        require_contract_bundle=True,
        require_runtime_companions=True,
    )
    _validate_contract_schema(
        _schema_payload_without_contract_bundle(payload, surface_key="product_frontdesk"),
        schema_file=PRODUCT_FRONTDESK_SCHEMA_FILE,
        context="product_frontdesk",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    product_frontdesk = _require_mapping(
        payload,
        "product_frontdesk",
        context="product_frontdesk",
    )
    manifest = _require_mapping(
        product_frontdesk,
        "product_entry_manifest",
        context="product_frontdesk.product_entry_manifest",
    )
    for surface_key in ("session_continuity", "progress_projection", "artifact_inventory", "runtime_control"):
        if product_frontdesk.get(surface_key) != manifest.get(surface_key):
            raise WorkspaceStateError(
                f"product_frontdesk.{surface_key} 与 product_entry_manifest.{surface_key} 不一致。",
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )

__all__ = [name for name in globals() if name.startswith("_") and not name.startswith("__")]
