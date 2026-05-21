from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    _require_mapping,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.workspace_types import WorkspaceStateError


def build_todo_wakeup_projection(
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
        "opl_wakeup_contract": {
            "owner": "one-person-lab",
            "provider_role": "typed_family_queue_and_provider_wakeup_shell",
            "mag_role": "refs_only_authoring_continuation_action_target",
            "target_action_ref": "open_grant_user_loop",
            "target_surface": "product user-loop",
            "target_command": user_loop_command,
            "sidecar_dispatch_action": None,
            "queue_write_policy": "enqueue_wakeup_only_no_grant_truth_writes",
            "required_return_shapes": [
                "domain_owner_receipt",
                "typed_blocker",
                "no_regression_evidence",
            ],
        },
        "forbidden_private_runtime_roles": {
            "hermes_24h_substrate_owner": False,
            "mag_scheduler_daemon_owner": False,
            "mag_attempt_ledger_owner": False,
            "mag_app_workbench_owner": False,
        },
        "opl_queue_role": "typed_family_queue_control_plane_only",
    }


def build_autonomy_controller_projection(
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
        "owner": "med-autogrant",
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


def build_attention_queue_projection(
    *,
    manifest: Mapping[str, Any],
    autonomy_observability: Mapping[str, Any],
    user_loop_command: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_user_loop_attention_queue",
        "owner": "med-autogrant",
        "queue_owner": "one-person-lab",
        "queue_write_policy": "enqueue_wakeup_only_no_grant_truth_writes",
        "attention_candidates": list(autonomy_observability.get("attention_candidates") or []),
        "operator_loop_surface": dict(
            _require_mapping(manifest, "operator_loop_surface", context="sidecar_export.product_entry_manifest")
        ),
        "recommended_wakeup_command": user_loop_command,
    }


def default_executor_owner(manifest: Mapping[str, Any]) -> str:
    runtime_control = _require_mapping(manifest, "runtime_control", context="sidecar_export.product_entry_manifest")
    return _require_nonempty_string_from_mapping(
        runtime_control,
        "executor_owner",
        context="sidecar_export.runtime_control",
    )


def first_skill(skill_catalog: Mapping[str, Any]) -> Mapping[str, Any]:
    skills = skill_catalog.get("skills")
    if not isinstance(skills, list) or not skills or not isinstance(skills[0], Mapping):
        raise WorkspaceStateError("sidecar_export.skill_catalog 缺少首个 skill。")
    return skills[0]
