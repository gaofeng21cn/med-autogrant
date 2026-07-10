from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.product_entry_parts.domain_handler_contract import (
    ALLOWED_ACTIONS,
    DOMAIN_HANDLER_ADAPTER_ID,
    DOMAIN_HANDLER_EXPORT_KIND,
    DOMAIN_HANDLER_VERSION,
)
from med_autogrant.product_entry_parts.domain_handler_dispatch import (
    dispatch_domain_handler_task,
)
from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_mapping


def build_domain_handler_export(
    product_entry: Any,
    *,
    input_path: str | Path,
) -> dict[str, Any]:
    manifest_payload = product_entry.build_product_entry_manifest(input_path=input_path)
    manifest = _require_mapping(
        manifest_payload,
        "product_entry_manifest",
        context="domain_handler_export",
    )
    export = {
        "surface_kind": DOMAIN_HANDLER_EXPORT_KIND,
        "schema_version": DOMAIN_HANDLER_VERSION,
        "adapter_id": DOMAIN_HANDLER_ADAPTER_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "identity": {
            "grant_run_id": manifest_payload["grant_run_id"],
            "workspace_id": manifest_payload["workspace_id"],
            "draft_id": manifest_payload["draft_id"],
            "lifecycle_stage": manifest_payload["lifecycle_stage"],
            "input_path": manifest_payload["input_path"],
        },
        "workspace_locator": dict(
            _require_mapping(manifest, "workspace_locator", context="product_entry_manifest")
        ),
        "progress_projection": dict(
            _require_mapping(manifest, "progress_projection", context="product_entry_manifest")
        ),
        "family_action_catalog": dict(
            _require_mapping(manifest, "family_action_catalog", context="product_entry_manifest")
        ),
        "family_stage_control_plane": dict(
            _require_mapping(
                manifest, "family_stage_control_plane", context="product_entry_manifest"
            )
        ),
        "grant_transition_oracle": dict(
            _require_mapping(manifest, "grant_transition_oracle", context="product_entry_manifest")
        ),
        "owner_receipt_contract": dict(
            _require_mapping(manifest, "owner_receipt_contract", context="product_entry_manifest")
        ),
        "minimal_authority_functions": list(manifest["minimal_authority_functions"]),
        "allowed_dispatch_actions": sorted(ALLOWED_ACTIONS),
        "generated_surface_handoff_ref": "contracts/generated_surface_handoff.json",
        "caller_boundary": {
            "direct_handler_owner": TARGET_DOMAIN_ID,
            "generated_caller_owner": "one-person-lab",
            "mag_role": "grant_authority_action_target",
            "opl_role": "generated_caller_runtime_and_lifecycle_owner",
        },
        "authority_boundary": dict(
            _require_mapping(manifest, "authority_boundary", context="product_entry_manifest")
        ),
    }
    return {
        "ok": True,
        "command": "domain-handler-export",
        "grant_run_id": manifest_payload["grant_run_id"],
        "workspace_id": manifest_payload["workspace_id"],
        "draft_id": manifest_payload["draft_id"],
        "lifecycle_stage": manifest_payload["lifecycle_stage"],
        "input_path": manifest_payload["input_path"],
        "domain_handler_export": export,
    }
