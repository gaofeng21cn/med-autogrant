from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID

from opl_harness_shared.family_action_catalog import (
    build_family_action,
    build_family_action_catalog,
    project_family_action_catalog,
    validate_family_action_catalog_parity,
)


CATALOG_ID = "med_autogrant_action_catalog"
ACTION_CATALOG_REF = "/product_entry_manifest/family_action_catalog"


def build_mag_family_action_catalog(
    *,
    action_commands: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    actions = [
        _build_action(
            action_commands,
            key="open_loop",
            action_id="open_grant_user_loop",
            title="Open MAG user loop",
            summary="进入当前 MAG grant user loop，并继续同一 funding call 下的 authoring loop。",
            effect="mutating",
            input_schema_ref="schemas/v1/grant-user-loop.schema.json",
            output_schema_ref="schemas/v1/grant-user-loop.schema.json",
            workspace_locator_fields=["input_path", "task_intent"],
        ),
        _build_action(
            action_commands,
            key="inspect_progress",
            action_id="inspect_progress",
            title="Inspect MAG progress",
            summary="读取当前 MAG workspace 的阶段摘要、checkpoint 与下一步。",
            effect="read_only",
            input_schema_ref="schemas/v1/grant-progress.schema.json",
            output_schema_ref="schemas/v1/grant-progress.schema.json",
            workspace_locator_fields=["input_path"],
        ),
        _build_action(
            action_commands,
            key="inspect_cockpit",
            action_id="inspect_cockpit",
            title="Inspect MAG cockpit",
            summary="查看 MAG 主线 snapshot、对象面和当前 route action 汇总。",
            effect="read_only",
            input_schema_ref="schemas/v1/grant-cockpit.schema.json",
            output_schema_ref="schemas/v1/grant-cockpit.schema.json",
            workspace_locator_fields=["input_path"],
        ),
        _build_action(
            action_commands,
            key="build_direct_entry",
            action_id="build_direct_entry",
            title="Build MAG direct entry",
            summary="把用户意图组合成当前 MAG grant direct-entry contract。",
            effect="mutating",
            input_schema_ref="schemas/v1/product-entry.schema.json",
            output_schema_ref="schemas/v1/grant-direct-entry.schema.json",
            workspace_locator_fields=["input_path", "task_intent"],
        ),
        _build_action(
            action_commands,
            key="build_submission_ready_package",
            action_id="build_submission_ready_package",
            title="Build MAG submission-ready package",
            summary="检查 MAG submission-ready gate，并在通过时导出本地交付目录。",
            effect="mutating",
            input_schema_ref="schemas/v1/submission-ready-package.schema.json",
            output_schema_ref="schemas/v1/submission-ready-package.schema.json",
            workspace_locator_fields=["input_path", "output_dir"],
            human_gate_ids=["submission_ready_export_gate"],
        ),
    ]
    catalog = build_family_action_catalog(
        catalog_id=CATALOG_ID,
        target_domain_id=TARGET_DOMAIN_ID,
        owner=TARGET_DOMAIN_ID,
        actions=actions,
        notes=[
            "MCP projection is descriptor-only",
            "public_runtime=false until a public MCP runtime is explicitly landed.",
            "OPL consumes schema/helper/validator/discovery projections and does not own MAG grant truth.",
        ],
    )
    parity = validate_family_action_catalog_parity(catalog)
    if parity["status"] != "aligned":
        raise ValueError(f"MAG family action catalog parity failed: {parity['issues']}")
    return catalog


def project_mag_family_action_catalog(
    catalog: Mapping[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    return {
        "cli": project_family_action_catalog(catalog, "cli"),
        "mcp": project_family_action_catalog(catalog, "mcp"),
        "skill": project_family_action_catalog(catalog, "skill"),
        "openai": project_family_action_catalog(catalog, "openai"),
        "ai-sdk": project_family_action_catalog(catalog, "ai-sdk"),
    }


def annotate_operator_loop_actions_with_catalog_refs(
    *,
    operator_loop_actions: Mapping[str, Mapping[str, Any]],
    action_catalog: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    action_ids = {
        "open_loop": "open_grant_user_loop",
        "inspect_progress": "inspect_progress",
        "inspect_cockpit": "inspect_cockpit",
        "build_direct_entry": "build_direct_entry",
        "build_submission_ready_package": "build_submission_ready_package",
    }
    actions_by_id = {
        str(action["action_id"]): action
        for action in action_catalog["actions"]
        if isinstance(action, Mapping)
    }
    annotated: dict[str, dict[str, Any]] = {}
    for key, action in operator_loop_actions.items():
        payload = dict(action)
        action_id = action_ids[key]
        catalog_action = actions_by_id[action_id]
        payload["action_catalog_ref"] = action_id
        payload["command"] = catalog_action["source_command"]["command"]
        payload["surface_kind"] = catalog_action["source_command"]["surface_kind"]
        annotated[key] = payload
    return annotated


def _build_action(
    action_commands: Mapping[str, Mapping[str, Any]],
    *,
    key: str,
    action_id: str,
    title: str,
    summary: str,
    effect: str,
    input_schema_ref: str,
    output_schema_ref: str,
    workspace_locator_fields: list[str],
    human_gate_ids: list[str] | None = None,
) -> dict[str, Any]:
    command_spec = action_commands[key]
    return build_family_action(
        action_id=action_id,
        title=title,
        summary=summary,
        owner=TARGET_DOMAIN_ID,
        effect=effect,
        command=str(command_spec["command"]),
        surface_kind=str(command_spec["surface_kind"]),
        input_schema_ref=input_schema_ref,
        output_schema_ref=output_schema_ref,
        workspace_locator_fields=workspace_locator_fields,
        human_gate_ids=human_gate_ids or [],
        mcp_public_runtime=False,
        authority_boundary={
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "opl_role": "schema_helper_validator_discovery_only",
            "public_runtime": False,
            "descriptor_only": True,
        },
    )
