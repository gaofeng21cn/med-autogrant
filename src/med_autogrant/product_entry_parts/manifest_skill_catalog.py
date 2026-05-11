from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import PRODUCT_STATUS_KIND, TARGET_DOMAIN_ID
from med_autogrant.product_entry_parts.runtime_registration import _build_opl_stage_runtime_registration
from med_autogrant.public_cli import public_cli_command
from med_autogrant.action_catalog import ACTION_CATALOG_REF

from opl_harness_shared.skill_catalog import (
    build_skill_catalog as _build_shared_skill_catalog,
    build_skill_descriptor as _build_shared_skill_descriptor,
)


def build_product_entry_skill_catalog(
    *,
    resolved_input_path: Path,
    runtime_summary: Mapping[str, Any],
    runtime_continuity: Mapping[str, Any],
    shell_commands: Mapping[str, str],
    domain_entry_contract: Mapping[str, Any],
    action_catalog_projections: Mapping[str, list[dict[str, Any]]],
    domain_agent_skeleton_mapping: Mapping[str, Any],
) -> dict[str, Any]:
    skill_catalog_command = public_cli_command(
        "skill-catalog",
        "--input",
        str(resolved_input_path),
        "--format",
        "json",
    )
    opl_stage_runtime_registration = _build_opl_stage_runtime_registration(
        runtime_summary=runtime_summary,
        runtime_continuity=runtime_continuity,
        shell_commands=shell_commands,
        skill_catalog_command=skill_catalog_command,
    )
    return _build_shared_skill_catalog(
        summary="Canonical Med Auto Grant app skill plus machine-readable command contracts.",
        skills=[
            _build_med_autogrant_skill_descriptor(
                shell_commands=shell_commands,
                runtime_continuity=runtime_continuity,
                opl_stage_runtime_registration=opl_stage_runtime_registration,
                action_catalog_projections=action_catalog_projections,
                domain_agent_skeleton_mapping=domain_agent_skeleton_mapping,
            )
        ],
        supported_commands=list(domain_entry_contract.get("supported_commands") or []),
        command_contracts=list(domain_entry_contract.get("command_contracts") or []),
    )


def _build_med_autogrant_skill_descriptor(
    *,
    shell_commands: Mapping[str, str],
    runtime_continuity: Mapping[str, Any],
    opl_stage_runtime_registration: Mapping[str, Any],
    action_catalog_projections: Mapping[str, list[dict[str, Any]]],
    domain_agent_skeleton_mapping: Mapping[str, Any],
) -> dict[str, Any]:
    mcp_descriptors = list(action_catalog_projections["mcp"])
    return _build_shared_skill_descriptor(
        skill_id="med-autogrant",
        title="Med Auto Grant",
        owner=TARGET_DOMAIN_ID,
        distribution_mode="repo_tracked_codex_plugin",
        surface_kind=PRODUCT_STATUS_KIND,
        description="Canonical Med Auto Grant domain app skill for Codex and OPL callers.",
        command=shell_commands["product_status"],
        readiness="landed",
        tags=["med-autogrant", "domain-app", "grant-authoring"],
        domain_projection={
            "plugin_name": "med-autogrant",
            "skill_entry": "med-autogrant",
            "skill_semantics": "domain_app",
            "entry_shell_key": "product_status",
            "entry_command": shell_commands["product_status"],
            "recommended_shell": "product_status",
            "supporting_shell_keys": [
                "grant_progress",
                "grant_cockpit",
                "grant_direct_entry",
                "grant_user_loop",
            ],
            "shell_commands": shell_commands,
            "runtime_continuity": dict(runtime_continuity),
            "opl_stage_runtime_registration": dict(opl_stage_runtime_registration),
            "domain_agent_skeleton_mapping": dict(domain_agent_skeleton_mapping),
            "action_catalog_ref": ACTION_CATALOG_REF,
            "mcp_descriptor": dict(mcp_descriptors[0]),
            "action_catalog_projections": {
                "skill": list(action_catalog_projections["skill"]),
                "mcp": mcp_descriptors,
            },
        },
    )
