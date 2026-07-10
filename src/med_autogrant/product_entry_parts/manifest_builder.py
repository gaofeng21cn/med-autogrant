from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.action_catalog import build_mag_family_action_catalog
from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.mainline_status import read_mainline_status
from med_autogrant.product_entry_parts.loop_contracts import (
    _validate_product_entry_manifest_contract,
)
from med_autogrant.product_entry_parts.primitives import (
    GRANT_COCKPIT_KIND,
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_PROGRESS_PROJECTION_KIND,
    GRANT_USER_LOOP_KIND,
    PRODUCT_ENTRY_MANIFEST_KIND,
    PRODUCT_STATUS_KIND,
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.runtime_defaults import build_default_runtime_summary
from med_autogrant.stage_control_plane import (
    build_mag_family_stage_control_plane,
    build_mag_grant_transition_oracle,
)


class ProductEntryManifestBuilderMixin:
    def build_product_entry_manifest(
        self,
        *,
        input_path: str | Path,
        funding_call: str | None = None,
    ) -> dict[str, Any]:
        del funding_call
        resolved_input_path = Path(input_path).expanduser().resolve()
        progress_payload = self.read_grant_progress(input_path=resolved_input_path)
        progress_projection = dict(
            _require_mapping(progress_payload, "progress_projection", context="grant-progress")
        )
        mainline = read_mainline_status()
        current_line = _require_mapping(mainline, "current_line", context="mainline_status")
        current_focus = _require_mapping(mainline, "current_focus", context="mainline_status")
        current_record = _require_mapping(
            _require_mapping(mainline, "maintainer_references", context="mainline_status"),
            "current_record_detail",
            context="mainline_status.maintainer_references",
        )
        runtime_owner = _require_mapping(
            _require_mapping(mainline, "maintainer_references", context="mainline_status"),
            "runtime_owner",
            context="mainline_status.maintainer_references",
        )
        commands = _product_commands(resolved_input_path)
        operator_loop_actions = _operator_loop_actions(commands)
        action_catalog = build_mag_family_action_catalog(
            action_commands=operator_loop_actions
        )
        stage_control_plane = build_mag_family_stage_control_plane(
            family_action_catalog=action_catalog
        )
        grant_transition_oracle = build_mag_grant_transition_oracle(
            family_stage_control_plane=stage_control_plane,
            family_action_catalog=action_catalog,
        )
        runtime = build_default_runtime_summary(
            current_owner_line=_require_nonempty_string_from_mapping(
                current_line,
                "current_owner_line",
                context="mainline_status.current_line",
            )
        )
        product_entry_shell = {
            "product_status": _shell(commands["product_status"], PRODUCT_STATUS_KIND),
            "grant_progress": _shell(commands["grant_progress"], GRANT_PROGRESS_PROJECTION_KIND),
            "grant_cockpit": _shell(commands["grant_cockpit"], GRANT_COCKPIT_KIND),
            "grant_direct_entry": _shell(commands["grant_direct_entry"], GRANT_DIRECT_ENTRY_KIND),
            "grant_user_loop": _shell(commands["grant_user_loop"], GRANT_USER_LOOP_KIND),
        }
        product_entry_status = {
            "summary": _require_nonempty_string_from_mapping(
                current_focus, "summary", context="mainline_status.current_focus"
            ),
            "current_stage": progress_payload["lifecycle_stage"],
            "recommended_next_stage": progress_projection["recommended_next_stage"],
        }
        product_entry_manifest = {
            "manifest_version": 2,
            "manifest_kind": PRODUCT_ENTRY_MANIFEST_KIND,
            "target_domain_id": TARGET_DOMAIN_ID,
            "formal_entry": {
                "default": "CLI",
                "supported_protocols": ["MCP"],
                "internal_surface": "MedAutoGrantDomainEntry",
            },
            "workspace_locator": {
                "workspace_surface_kind": "nsfc_workspace",
                "workspace_path": str(resolved_input_path),
            },
            "runtime": runtime,
            "repo_mainline": {
                "program_id": mainline["program_id"],
                "phase_id": current_record["phase_id"],
                "phase_name": current_record["phase_name"],
                "phase_status": current_record["status"],
                "phase_summary": product_entry_status["summary"],
                "active_phase": runtime_owner["active_phase"],
                "active_tranche": runtime_owner["active_tranche"],
            },
            "product_entry_status": product_entry_status,
            "product_entry_shell": product_entry_shell,
            "operator_loop_actions": operator_loop_actions,
            "progress_projection": progress_projection,
            "family_action_catalog": action_catalog,
            "family_stage_control_plane": stage_control_plane,
            "grant_transition_oracle": grant_transition_oracle,
            "domain_entry_contract": build_domain_entry_contract(),
            "skill_catalog": _skill_catalog(commands["product_status"]),
            "product_entry_start": _product_entry_start(product_entry_shell),
            "owner_receipt_contract": _owner_receipt_contract(),
            "minimal_authority_functions": _minimal_authority_functions(),
            "authority_boundary": {
                "domain_truth_owner": TARGET_DOMAIN_ID,
                "fundability_verdict_owner": TARGET_DOMAIN_ID,
                "authoring_quality_verdict_owner": TARGET_DOMAIN_ID,
                "submission_ready_export_verdict_owner": TARGET_DOMAIN_ID,
                "package_authority_owner": TARGET_DOMAIN_ID,
                "memory_accept_reject_owner": TARGET_DOMAIN_ID,
                "owner_receipt_signer": TARGET_DOMAIN_ID,
                "opl_owns_runtime_generated_surfaces_and_lifecycle": True,
                "opl_can_write_grant_truth": False,
                "opl_can_authorize_quality_or_export": False,
            },
            "notes": [
                "OPL generates and hosts product, status, user-loop, lifecycle, and workbench surfaces.",
                "This direct manifest exposes only MAG handler descriptors and grant authority refs.",
                "Structural conformance is not external runtime, grant, quality, export, or submission readiness.",
            ],
        }
        payload = {
            "ok": True,
            "command": "product-entry-manifest",
            "grant_run_id": progress_payload["grant_run_id"],
            "workspace_id": progress_payload["workspace_id"],
            "draft_id": progress_payload["draft_id"],
            "lifecycle_stage": progress_payload["lifecycle_stage"],
            "input_path": progress_payload["input_path"],
            "product_entry_manifest": product_entry_manifest,
        }
        _validate_product_entry_manifest_contract(
            payload,
            grant_run_id=progress_payload["grant_run_id"],
            workspace_id=progress_payload["workspace_id"],
            lifecycle_stage=progress_payload["lifecycle_stage"],
        )
        return payload


def _product_commands(input_path: Path) -> dict[str, str]:
    task_intent = "<describe-task-intent>"
    return {
        "product_status": public_cli_command(
            "product-status", "--input", str(input_path), "--format", "json"
        ),
        "grant_progress": public_cli_command(
            "grant-progress", "--input", str(input_path), "--format", "json"
        ),
        "grant_cockpit": public_cli_command(
            "grant-cockpit", "--input", str(input_path), "--format", "json"
        ),
        "grant_direct_entry": public_cli_command(
            "grant-direct-entry",
            "--input",
            str(input_path),
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
        "grant_user_loop": public_cli_command(
            "grant-user-loop",
            "--input",
            str(input_path),
            "--task-intent",
            task_intent,
            "--format",
            "json",
        ),
        "build_submission_ready_package": public_cli_command(
            "build-submission-ready-package",
            "--input",
            str(input_path),
            "--output-dir",
            "<submission-ready-output-dir>",
            "--format",
            "json",
        ),
    }


def _operator_loop_actions(commands: Mapping[str, str]) -> dict[str, dict[str, Any]]:
    return {
        "open_loop": {
            "command": commands["grant_user_loop"],
            "surface_kind": GRANT_USER_LOOP_KIND,
            "summary": "Open the direct MAG grant action target.",
            "requires": ["task_intent"],
        },
        "inspect_progress": {
            "command": commands["grant_progress"],
            "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
            "summary": "Read MAG grant progress from workspace truth.",
            "requires": [],
        },
        "inspect_cockpit": {
            "command": commands["grant_cockpit"],
            "surface_kind": GRANT_COCKPIT_KIND,
            "summary": "Read the direct MAG cockpit projection.",
            "requires": [],
        },
        "build_direct_entry": {
            "command": commands["grant_direct_entry"],
            "surface_kind": GRANT_DIRECT_ENTRY_KIND,
            "summary": "Build a direct MAG domain-entry contract.",
            "requires": ["task_intent"],
        },
        "build_submission_ready_package": {
            "command": commands["build_submission_ready_package"],
            "surface_kind": "submission_ready_package",
            "summary": "Invoke MAG package authority and export gates.",
            "requires": ["output_dir"],
        },
    }


def _shell(command: str, surface_kind: str) -> dict[str, str]:
    return {"command": command, "surface_kind": surface_kind}


def _skill_catalog(command: str) -> dict[str, Any]:
    return {
        "catalog_kind": "mag_domain_skill_catalog",
        "skills": [
            {
                "skill_id": "mag",
                "target_surface_kind": PRODUCT_STATUS_KIND,
                "command": command,
                "primary_skill_ref": "agent/primary_skill/SKILL.md",
            }
        ],
    }


def _product_entry_start(shell: Mapping[str, Mapping[str, str]]) -> dict[str, Any]:
    return {
        "recommended_mode_id": "status",
        "modes": [
            {"mode_id": "status", "command": shell["product_status"]["command"]},
            {"mode_id": "direct", "command": shell["grant_direct_entry"]["command"]},
            {"mode_id": "user_loop", "command": shell["grant_user_loop"]["command"]},
        ],
    }


def _owner_receipt_contract() -> dict[str, Any]:
    return {
        "surface_kind": "mag_owner_receipt_contract",
        "contract_ref": "contracts/owner_receipt_contract.json",
        "allowed_return_shapes": [
            "owner_receipt_ref",
            "typed_blocker_ref",
            "human_gate_ref",
            "route_back_ref",
        ],
        "receipt_instance_write_boundary": "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/",
    }


def _minimal_authority_functions() -> list[dict[str, str]]:
    return [
        {"authority_id": "fundability_and_quality_verdict", "ref": "src/med_autogrant/grant_quality.py"},
        {"authority_id": "package_and_export_verdict", "ref": "src/med_autogrant/submission_ready.py"},
        {"authority_id": "grant_transition_oracle", "ref": "src/med_autogrant/stage_control_plane_parts/transition_oracle.py"},
        {"authority_id": "memory_accept_reject", "ref": "src/med_autogrant/product_entry_parts/domain_memory_runtime.py"},
        {"authority_id": "owner_receipt_signer", "ref": "src/med_autogrant/product_entry_parts/owner_receipt_writers.py"},
    ]
