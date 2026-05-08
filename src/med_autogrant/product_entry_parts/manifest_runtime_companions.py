from __future__ import annotations

import hashlib
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID
from med_autogrant.product_entry_parts.runtime_contracts import PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE

from opl_harness_shared.runtime_task_companions import (
    build_family_lifecycle_ledger as _build_shared_family_lifecycle_ledger,
    build_family_owner_route as _build_shared_family_owner_route,
    build_family_persistence_policy as _build_shared_family_persistence_policy,
)


def build_manifest_runtime_companions(
    *,
    progress_payload: Mapping[str, Any],
    checkpoint_status: str,
    continuation_route_id: str,
    continuation_route_status: str,
    grant_user_loop_command: str,
) -> dict[str, dict[str, Any]]:
    current_program_ref = {
        "ref_kind": "repo_path",
        "ref": "contracts/runtime-program/current-program.json",
        "label": "MAG repo-tracked current program truth",
    }
    lifecycle_checksum = _build_lifecycle_checksum(
        progress_payload=progress_payload,
        checkpoint_status=checkpoint_status,
        continuation_route_id=continuation_route_id,
    )
    return {
        "persistence_policy": _build_persistence_policy(current_program_ref),
        "lifecycle_ledger": _build_lifecycle_ledger(
            current_program_ref=current_program_ref,
            lifecycle_checksum=lifecycle_checksum,
            checkpoint_status=checkpoint_status,
        ),
        "owner_route": _build_owner_route(
            current_program_ref=current_program_ref,
            lifecycle_checksum=lifecycle_checksum,
            progress_payload=progress_payload,
            continuation_route_id=continuation_route_id,
            continuation_route_status=continuation_route_status,
            grant_user_loop_command=grant_user_loop_command,
        ),
    }


def _build_lifecycle_checksum(
    *,
    progress_payload: Mapping[str, Any],
    checkpoint_status: str,
    continuation_route_id: str,
) -> str:
    checksum_fields = (
        progress_payload["grant_run_id"],
        progress_payload["workspace_id"],
        progress_payload["draft_id"],
        progress_payload["lifecycle_stage"],
        checkpoint_status,
        continuation_route_id,
    )
    return hashlib.sha256("\n".join(str(value) for value in checksum_fields).encode("utf-8")).hexdigest()


def _build_persistence_policy(current_program_ref: Mapping[str, Any]) -> dict[str, Any]:
    return _build_shared_family_persistence_policy(
        target_domain_id=TARGET_DOMAIN_ID,
        policy_id="mag_product_entry_persistence_policy",
        summary=(
            "Repo-tracked current-program and workspace inputs remain the authority; "
            "product-entry projections are rebuildable read models."
        ),
        authority_surfaces=[
            {
                "surface_id": "mag_current_program",
                "surface_role": "repo_tracked_program_authority",
                "storage_role": "file_authority",
                "owner": TARGET_DOMAIN_ID,
                "ref": current_program_ref,
                "rebuild_from_refs": [],
            }
        ],
        projection_caches=[
            {
                "surface_id": "mag_product_entry_manifest",
                "surface_role": "product_entry_read_model",
                "storage_role": "projection_cache",
                "owner": TARGET_DOMAIN_ID,
                "ref": {
                    "ref_kind": "json_pointer",
                    "ref": "/product_entry_manifest",
                    "label": "generated product-entry manifest",
                },
                "rebuild_from_refs": [current_program_ref],
            }
        ],
    )


def _build_lifecycle_ledger(
    *,
    current_program_ref: Mapping[str, Any],
    lifecycle_checksum: str,
    checkpoint_status: str,
) -> dict[str, Any]:
    return _build_shared_family_lifecycle_ledger(
        target_domain_id=TARGET_DOMAIN_ID,
        ledger_id="mag_product_entry_contract_ledger",
        phase="verify",
        status=checkpoint_status,
        summary="Current product-entry manifest was generated from MAG-owned truth and validated fail-closed.",
        actions=[
            {
                "action_id": "validate_product_entry_manifest",
                "action_kind": "verify",
                "target_ref": {
                    "ref_kind": "json_pointer",
                    "ref": "/product_entry_manifest",
                    "label": "generated product-entry manifest",
                },
                "authority_owner": TARGET_DOMAIN_ID,
                "safety_gate": "schema_and_shared_family_validator",
                "result": "validated",
                "manifest_ref": {
                    "ref_kind": "repo_path",
                    "ref": f"schemas/v1/{PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE}",
                    "label": "MAG product-entry manifest schema",
                },
                "sha256": lifecycle_checksum,
                "restore_ref": current_program_ref,
            }
        ],
    )


def _build_owner_route(
    *,
    current_program_ref: Mapping[str, Any],
    lifecycle_checksum: str,
    progress_payload: Mapping[str, Any],
    continuation_route_id: str,
    continuation_route_status: str,
    grant_user_loop_command: str,
) -> dict[str, Any]:
    return _build_shared_family_owner_route(
        target_domain_id=TARGET_DOMAIN_ID,
        route_id="mag_product_entry_owner_route",
        route_epoch=f"{progress_payload['grant_run_id']}:{progress_payload['lifecycle_stage']}",
        source_fingerprint=lifecycle_checksum,
        next_owner=TARGET_DOMAIN_ID,
        allowed_actions=["open_product_entry", "continue_grant_loop", "inspect_progress"],
        idempotency_key=f"mag_product_entry:{progress_payload['grant_run_id']}:{progress_payload['lifecycle_stage']}",
        status=continuation_route_status,
        summary=f"MAG owns continuation through {continuation_route_id} via the grant user loop.",
        handoff_refs=[
            {"ref_kind": "cli", "ref": grant_user_loop_command, "label": "grant user loop continuation command"}
        ],
        projection_refs=[
            {
                "ref_kind": "json_pointer",
                "ref": "/product_entry_manifest/progress_projection",
                "label": "current grant progress projection",
            },
            current_program_ref,
        ],
    )
