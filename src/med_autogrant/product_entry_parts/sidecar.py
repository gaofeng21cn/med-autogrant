from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


SIDECAR_EXPORT_KIND = "mag_product_sidecar_export"
SIDECAR_DISPATCH_KIND = "mag_product_sidecar_dispatch"
SIDECAR_ADAPTER_ID = "mag.opl_stage_led.product_sidecar.v1"
SIDECAR_VERSION = 1

_ALLOWED_ACTIONS = {
    "status/read",
    "user-loop/wakeup",
    "autonomy-controller/dry-run",
    "autonomy-controller/guarded-run",
    "notification/receipt",
}


def build_sidecar_export(
    product_entry: Any,
    *,
    input_path: str | Path,
) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    manifest_payload = product_entry.build_product_entry_manifest(input_path=resolved_input_path)
    manifest = _require_mapping(
        manifest_payload,
        "product_entry_manifest",
        context="sidecar_export",
    )
    skill_catalog = _require_mapping(manifest, "skill_catalog", context="sidecar_export.product_entry_manifest")
    skill = _first_skill(skill_catalog)
    domain_projection = _require_mapping(skill, "domain_projection", context="sidecar_export.skill_catalog.skill")
    runtime_control = _require_mapping(manifest, "runtime_control", context="sidecar_export.product_entry_manifest")
    runtime_continuity = _require_mapping(
        domain_projection,
        "runtime_continuity",
        context="sidecar_export.skill_catalog.domain_projection",
    )
    runtime_registration = _require_mapping(
        domain_projection,
        "opl_runtime_manager_registration",
        context="sidecar_export.skill_catalog.domain_projection",
    )
    domain_agent_skeleton = _require_mapping(
        domain_projection,
        "domain_agent_skeleton_mapping",
        context="sidecar_export.skill_catalog.domain_projection",
    )
    controlled_stage_attempt = _require_mapping(
        manifest,
        "controlled_stage_attempt_projection",
        context="sidecar_export.product_entry_manifest",
    )
    automation = _require_mapping(manifest, "automation", context="sidecar_export.product_entry_manifest")
    autonomy_observability = _require_mapping(
        manifest,
        "autonomy_observability",
        context="sidecar_export.product_entry_manifest",
    )
    user_loop_command = _require_nonempty_string_from_mapping(
        _require_mapping(manifest, "operator_loop_surface", context="sidecar_export.product_entry_manifest"),
        "command",
        context="sidecar_export.operator_loop_surface",
    )
    export_payload = {
        "surface_kind": SIDECAR_EXPORT_KIND,
        "schema_version": SIDECAR_VERSION,
        "adapter_id": SIDECAR_ADAPTER_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "substrate_boundary": {
            "online_substrate_owner": "explicit_opl_provider",
            "control_plane_owner": "one-person-lab",
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "quality_gate_owner": TARGET_DOMAIN_ID,
            "artifact_owner": TARGET_DOMAIN_ID,
            "default_executor_owner": _default_executor_owner(manifest),
            "default_executor_note": (
                "Default executor remains Codex/domain-selected; OPL may explicitly choose "
                "a stage-led runtime provider for wakeup/control-plane carrier duties."
            ),
            "hermes_proof_executor_default": False,
        },
        "workspace_locator": dict(
            _require_mapping(manifest, "workspace_locator", context="sidecar_export.product_entry_manifest")
        ),
        "identity": {
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
        },
        "runtime_control": dict(runtime_control),
        "runtime_continuity": dict(runtime_continuity),
        "domain_agent_skeleton_mapping": dict(domain_agent_skeleton),
        "artifact_locator_contract": dict(
            _require_mapping(manifest, "artifact_locator_contract", context="sidecar_export.product_entry_manifest")
        ),
        "controlled_stage_attempt_projection": dict(controlled_stage_attempt),
        "receipt_refs": dict(
            _require_mapping(
                controlled_stage_attempt,
                "receipt_refs",
                context="sidecar_export.controlled_stage_attempt_projection",
            )
        ),
        "todo_wakeup": _build_todo_wakeup_projection(
            automation=automation,
            manifest=manifest,
            user_loop_command=user_loop_command,
        ),
        "autonomy_controller": _build_autonomy_controller_projection(
            manifest=manifest,
            autonomy_observability=autonomy_observability,
        ),
        "user_loop_attention_queue": _build_attention_queue_projection(
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
            "allowed_dispatch_actions": sorted(_ALLOWED_ACTIONS),
        },
        "guardrails": {
            "dispatch_boundary": "MAG-owned guarded product actions only.",
            "forbidden_defaults": [
                "hermes_proof_executor",
                "grant_truth_mutation_by_opl",
                "quality_gate_override_by_opl",
                "submission_ready_gate_bypass",
            ],
        },
    }
    return {
        "ok": True,
        "command": "product-sidecar-export",
        "grant_run_id": manifest_payload["grant_run_id"],
        "workspace_id": manifest_payload["workspace_id"],
        "draft_id": manifest_payload["draft_id"],
        "lifecycle_stage": manifest_payload["lifecycle_stage"],
        "input_path": manifest_payload["input_path"],
        "sidecar_export": export_payload,
    }


def dispatch_sidecar_task(
    product_entry: Any,
    *,
    task_path: str | Path,
) -> dict[str, Any]:
    resolved_task_path = Path(task_path).expanduser().resolve()
    task = _read_json_mapping(resolved_task_path, context="sidecar_task")
    action = _require_nonempty_string_from_mapping(task, "action", context="sidecar_task")
    if action not in _ALLOWED_ACTIONS:
        raise WorkspaceStateError(f"sidecar task action 不允许: {action}")
    input_path = _require_nonempty_string_from_mapping(task, "input_path", context="sidecar_task")
    if action == "status/read":
        return _dispatch_status_read(product_entry, task=task, input_path=input_path, task_path=resolved_task_path)
    if action == "user-loop/wakeup":
        return _dispatch_user_loop_wakeup(product_entry, task=task, input_path=input_path, task_path=resolved_task_path)
    if action in {"autonomy-controller/dry-run", "autonomy-controller/guarded-run"}:
        return _dispatch_autonomy_controller(task=task, input_path=input_path, task_path=resolved_task_path)
    return _dispatch_notification_receipt(task=task, input_path=input_path, task_path=resolved_task_path)


def _dispatch_status_read(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
) -> dict[str, Any]:
    status = product_entry.build_product_status(input_path=input_path)
    return _dispatch_payload(
        action="status/read",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "sidecar_status_read_result",
            "product_status": status["product_status"],
        },
        executed_command=None,
    )


def _dispatch_user_loop_wakeup(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
) -> dict[str, Any]:
    task_intent = _require_nonempty_string_from_mapping(task, "task_intent", context="sidecar_task")
    user_loop = product_entry.build_grant_user_loop(input_path=input_path, task_intent=task_intent)
    return _dispatch_payload(
        action="user-loop/wakeup",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "sidecar_user_loop_wakeup_result",
            "grant_user_loop": {
                "surface_kind": "grant_user_loop",
                "payload": user_loop["grant_user_loop"],
            },
        },
        executed_command=None,
    )


def _dispatch_autonomy_controller(
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
) -> dict[str, Any]:
    output_dir = _require_nonempty_string_from_mapping(task, "output_dir", context="sidecar_task")
    mode = "dry_run" if task["action"] == "autonomy-controller/dry-run" else "guarded_run"
    command = public_cli_command(
        "execute-grant-autonomy-controller",
        "--input",
        input_path,
        "--output-dir",
        output_dir,
        "--format",
        "json",
    )
    return _dispatch_payload(
        action=str(task["action"]),
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="accepted",
        result={
            "surface_kind": "sidecar_autonomy_controller_guarded_action",
            "mode": mode,
            "command": command,
            "execution_policy": "caller_must_execute_mag_guarded_command",
            "executor_override": None,
            "hermes_proof_executor_default": False,
        },
        executed_command=command,
    )


def _dispatch_notification_receipt(
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
) -> dict[str, Any]:
    notification = task.get("notification")
    if notification is not None and not isinstance(notification, Mapping):
        raise WorkspaceStateError("sidecar_task.notification 必须是 object。")
    return _dispatch_payload(
        action="notification/receipt",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="recorded",
        result={
            "surface_kind": "sidecar_notification_receipt",
            "receipt_status": "accepted",
            "notification": dict(notification or {}),
            "receipt_refs": _receipt_refs_for_task(
                task=task,
                action="notification/receipt",
                input_path=input_path,
            ),
            "write_policy": "receipt_only_no_domain_truth_mutation",
        },
        executed_command=None,
    )


def _dispatch_payload(
    *,
    action: str,
    task: Mapping[str, Any],
    task_path: Path,
    input_path: str,
    status: str,
    result: Mapping[str, Any],
    executed_command: str | None,
) -> dict[str, Any]:
    return {
        "ok": True,
        "command": "product-sidecar-dispatch",
        "sidecar_dispatch": {
            "surface_kind": SIDECAR_DISPATCH_KIND,
            "schema_version": SIDECAR_VERSION,
            "adapter_id": SIDECAR_ADAPTER_ID,
            "task_id": _optional_nonempty_string(task.get("task_id")) or f"{action}:{task_path.name}",
            "action": action,
            "status": status,
            "target_domain_id": TARGET_DOMAIN_ID,
            "input_path": str(Path(input_path).expanduser().resolve()),
            "task_path": str(task_path),
            "executed_by_sidecar": action in {"status/read", "user-loop/wakeup", "notification/receipt"},
            "executed_command": executed_command,
            "result": dict(result),
            "receipt_refs": _receipt_refs_for_task(
                task=task,
                action=action,
                input_path=input_path,
            ),
            "guardrails": {
                "allowed_actions": sorted(_ALLOWED_ACTIONS),
                "domain_truth_owner": TARGET_DOMAIN_ID,
                "opl_role": "typed_family_queue_control_plane",
                "hermes_role": "online_substrate_wakeup_carrier",
                "hermes_proof_executor_default": False,
            },
        },
    }


def _build_todo_wakeup_projection(
    *,
    automation: Mapping[str, Any],
    manifest: Mapping[str, Any],
    user_loop_command: str,
) -> dict[str, Any]:
    automations = automation.get("automations")
    if not isinstance(automations, list):
        raise WorkspaceStateError("sidecar_export.automation 缺少 automations。")
    authoring_wakeup = None
    for item in automations:
        if isinstance(item, Mapping) and item.get("automation_id") == "mag.authoring_loop_continuation":
            authoring_wakeup = dict(item)
            break
    if authoring_wakeup is None:
        raise WorkspaceStateError("sidecar_export 缺少 authoring loop continuation automation。")
    return {
        "surface_kind": "mag_todo_wakeup_projection",
        "explicit_wakeup_policy": "manual_or_opl_queue_triggered_authoring_loop_continuation",
        "todo_source_refs": [
            "/product_entry_manifest/remaining_gaps",
            "/product_entry_manifest/automation/automations/1",
            "/product_entry_manifest/autonomy_observability/attention_candidates",
        ],
        "remaining_gaps": list(manifest.get("remaining_gaps") or []),
        "authoring_loop_continuation": authoring_wakeup,
        "recommended_wakeup_command": user_loop_command,
        "hermes_wakeup_role": "24h_online_substrate_only",
        "opl_queue_role": "typed_family_queue_control_plane_only",
    }


def _build_autonomy_controller_projection(
    *,
    manifest: Mapping[str, Any],
    autonomy_observability: Mapping[str, Any],
) -> dict[str, Any]:
    workspace_path = _require_nonempty_string_from_mapping(
        _require_mapping(manifest, "workspace_locator", context="sidecar_export.product_entry_manifest"),
        "workspace_path",
        context="sidecar_export.workspace_locator",
    )
    return {
        "surface_kind": "mag_autonomy_controller_projection",
        "owner": TARGET_DOMAIN_ID,
        "observability": dict(autonomy_observability),
        "allowed_modes": ["dry_run", "guarded_run"],
        "default_mode": "dry_run",
        "command_template": public_cli_command(
            "execute-grant-autonomy-controller",
            "--input",
            workspace_path,
            "--output-dir",
            "<output-dir>",
            "--format",
            "json",
        ),
        "executor_override_allowed": False,
        "hermes_proof_executor_default": False,
    }


def _build_attention_queue_projection(
    *,
    manifest: Mapping[str, Any],
    autonomy_observability: Mapping[str, Any],
    user_loop_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_user_loop_attention_queue",
        "owner": TARGET_DOMAIN_ID,
        "queue_owner": "one-person-lab",
        "queue_write_policy": "enqueue_wakeup_only_no_grant_truth_writes",
        "attention_candidates": list(autonomy_observability.get("attention_candidates") or []),
        "operator_loop_surface": dict(
            _require_mapping(manifest, "operator_loop_surface", context="sidecar_export.product_entry_manifest")
        ),
        "recommended_wakeup_command": user_loop_command,
    }


def _default_executor_owner(manifest: Mapping[str, Any]) -> str:
    runtime_control = _require_mapping(manifest, "runtime_control", context="sidecar_export.product_entry_manifest")
    return _require_nonempty_string_from_mapping(
        runtime_control,
        "executor_owner",
        context="sidecar_export.runtime_control",
    )


def _first_skill(skill_catalog: Mapping[str, Any]) -> Mapping[str, Any]:
    skills = skill_catalog.get("skills")
    if not isinstance(skills, list) or not skills or not isinstance(skills[0], Mapping):
        raise WorkspaceStateError("sidecar_export.skill_catalog 缺少首个 skill。")
    return skills[0]


def _read_json_mapping(path: Path, *, context: str) -> Mapping[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise WorkspaceFileError(f"读取 {context} 失败: {path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(f"{context} 不是合法 JSON: {path}") from exc
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 JSON object: {path}")
    return payload


def _optional_nonempty_string(value: Any) -> str | None:
    if value is None:
        return None
    return _require_nonempty_string(value, field_name="task_id", context="sidecar_task")


def _receipt_refs_for_task(
    *,
    task: Mapping[str, Any],
    action: str,
    input_path: str,
) -> dict[str, Any]:
    task_id = _optional_nonempty_string(task.get("task_id")) or f"{action}:ad-hoc"
    return {
        "receipt_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/",
        "sidecar_dispatch_receipt_ref": (
            "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
            f"sidecar-dispatch/{task_id}.json"
        ),
        "input_path": str(Path(input_path).expanduser().resolve()),
        "write_policy": "receipt_ref_only_no_domain_truth_mutation",
        "opl_consumes_receipt_ref_only": True,
    }
