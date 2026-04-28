from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.runtime_surfaces import _build_opl_runtime_manager_registration
from med_autogrant.product_entry_parts.shared import (
    PRODUCT_FRONTDESK_KIND,
    TARGET_DOMAIN_ID,
    _build_shared_skill_catalog,
    _build_shared_skill_descriptor,
    public_cli_command,
)


def build_product_entry_skill_catalog(
    *,
    resolved_input_path: Path,
    runtime_summary: Mapping[str, Any],
    runtime_continuity: Mapping[str, Any],
    shell_commands: Mapping[str, str],
    domain_entry_contract: Mapping[str, Any],
) -> dict[str, Any]:
    skill_catalog_command = public_cli_command(
        "skill-catalog",
        "--input",
        str(resolved_input_path),
        "--format",
        "json",
    )
    opl_runtime_manager_registration = _build_opl_runtime_manager_registration(
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
                opl_runtime_manager_registration=opl_runtime_manager_registration,
            )
        ],
        supported_commands=list(domain_entry_contract.get("supported_commands") or []),
        command_contracts=list(domain_entry_contract.get("command_contracts") or []),
    )


def _build_med_autogrant_skill_descriptor(
    *,
    shell_commands: Mapping[str, str],
    runtime_continuity: Mapping[str, Any],
    opl_runtime_manager_registration: Mapping[str, Any],
) -> dict[str, Any]:
    return _build_shared_skill_descriptor(
        skill_id="med-autogrant",
        title="Med Auto Grant",
        owner=TARGET_DOMAIN_ID,
        distribution_mode="repo_tracked_codex_plugin",
        surface_kind=PRODUCT_FRONTDESK_KIND,
        description="Canonical Med Auto Grant domain app skill for Codex and OPL callers.",
        command=shell_commands["product_frontdesk"],
        readiness="landed",
        tags=["med-autogrant", "domain-app", "grant-authoring"],
        domain_projection={
            "plugin_name": "med-autogrant",
            "skill_entry": "med-autogrant",
            "skill_semantics": "domain_app",
            "entry_shell_key": "product_frontdesk",
            "entry_command": shell_commands["product_frontdesk"],
            "recommended_shell": "product_frontdesk",
            "supporting_shell_keys": [
                "grant_progress",
                "grant_cockpit",
                "grant_direct_entry",
                "grant_user_loop",
            ],
            "shell_commands": shell_commands,
            "runtime_continuity": dict(runtime_continuity),
            "opl_runtime_manager_registration": dict(opl_runtime_manager_registration),
        },
    )
