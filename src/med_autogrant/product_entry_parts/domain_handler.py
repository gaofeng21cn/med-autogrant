from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.domain_entry import MedAutoGrantDomainEntry
from med_autogrant.product_entry_parts.domain_handler_contract import (
    ALLOWED_ACTIONS,
    DOMAIN_HANDLER_ADAPTER_ID,
    DOMAIN_HANDLER_EXPORT_KIND,
    DOMAIN_HANDLER_VERSION,
)
from med_autogrant.product_entry_parts.domain_handler_dispatch import (
    dispatch_domain_handler_task,
)
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
AUTHORITY_FUNCTION_REFS = {
    "fundability_verdict": "src/med_autogrant/grant_quality.py",
    "quality_verdict": "src/med_autogrant/grant_quality.py",
    "export_verdict": "src/med_autogrant/submission_ready.py",
    "package_authority": "src/med_autogrant/final_package.py",
    "memory_accept_reject": "src/med_autogrant/product_entry_parts/domain_memory_runtime.py",
    "owner_receipt_signer": "src/med_autogrant/product_entry_parts/owner_receipt_writers.py",
    "grant_native_helper": "src/med_autogrant/product_entry_parts/domain_handler.py",
}


def build_domain_handler_export(
    *,
    input_path: str | Path,
) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    route_report = MedAutoGrantDomainEntry().dispatch(
        {"command": "stage-route-report", "input_path": str(resolved_input_path)}
    )
    verification_checkpoint = _require_mapping(
        route_report, "verification_checkpoint", context="stage-route-report"
    )
    identity = _require_mapping(
        verification_checkpoint, "identity", context="stage-route-report.verification_checkpoint"
    )
    grant_run_id = _require_nonempty_string_from_mapping(
        route_report, "grant_run_id", context="stage-route-report"
    )
    workspace_id = _require_nonempty_string_from_mapping(
        route_report, "workspace_id", context="stage-route-report"
    )
    lifecycle_stage = _require_nonempty_string_from_mapping(
        route_report, "lifecycle_stage", context="stage-route-report"
    )
    draft_id = identity.get("draft_id")
    export = {
        "surface_kind": DOMAIN_HANDLER_EXPORT_KIND,
        "schema_version": DOMAIN_HANDLER_VERSION,
        "adapter_id": DOMAIN_HANDLER_ADAPTER_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "identity": {
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
            "input_path": str(resolved_input_path),
        },
        "workspace_locator": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": str(resolved_input_path),
        },
        "family_action_catalog": _read_contract("action_catalog.json"),
        "declarative_stage_manifest_ref": "agent/stages/manifest.json",
        "family_stage_control_plane_ref": "/product_entry_manifest/family_stage_control_plane",
        "owner_receipt_contract": _read_contract("owner_receipt_contract.json"),
        "minimal_authority_functions": [
            {"authority_id": authority_id, "ref": ref}
            for authority_id, ref in AUTHORITY_FUNCTION_REFS.items()
        ],
        "ai_route_policy_ref": "src/med_autogrant/stage_control_plane_parts/ai_route_policy.py",
        "allowed_dispatch_actions": sorted(ALLOWED_ACTIONS),
        "generated_surface_handoff_ref": "contracts/generated_surface_handoff.json",
        "caller_boundary": {
            "direct_handler_owner": TARGET_DOMAIN_ID,
            "generated_caller_owner": "one-person-lab",
            "mag_role": "grant_authority_action_target",
            "opl_role": "generated_caller_runtime_and_lifecycle_owner",
        },
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "opl_can_write_grant_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_sign_mag_owner_receipt": False,
            "opl_can_authorize_quality_or_export": False,
            "generated_surface_ready_counts_as_domain_ready": False,
        },
    }
    return {
        "ok": True,
        "command": "domain-handler-export",
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "draft_id": draft_id,
        "lifecycle_stage": lifecycle_stage,
        "input_path": str(resolved_input_path),
        "domain_handler_export": export,
    }


def _read_contract(filename: str) -> dict[str, Any]:
    payload = json.loads((REPO_ROOT / "contracts" / filename).read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError(f"MAG contract must be a JSON object: {filename}")
    return dict(payload)
