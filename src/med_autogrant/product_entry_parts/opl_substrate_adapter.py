from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.public_cli import public_cli_command


def build_manifest_opl_substrate_adapter_export(
    *,
    resolved_input_path: str | Path,
    progress_payload: Mapping[str, Any],
    verification_identity: Mapping[str, Any],
    domain_memory_surfaces: Mapping[str, Any],
    functional_closure_surfaces: Mapping[str, Any],
    skill_catalog: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
    session_continuity: Mapping[str, Any],
    task_lifecycle: Mapping[str, Any],
    manifest_progress_projection: Mapping[str, Any],
    artifact_inventory: Mapping[str, Any],
    artifact_locator_contract: Mapping[str, Any],
    controlled_stage_attempt_projection: Mapping[str, Any],
) -> dict[str, Any]:
    domain_projection = _require_mapping(
        skill_catalog["skills"][0],
        "domain_projection",
        context="skill_catalog.skills.0",
    )
    return build_opl_substrate_adapter_export(
        input_path=resolved_input_path,
        grant_run_id=_require_nonempty_string_from_mapping(progress_payload, "grant_run_id", context="grant-progress"),
        workspace_id=_require_nonempty_string_from_mapping(progress_payload, "workspace_id", context="grant-progress"),
        draft_id=verification_identity.get("draft_id") if isinstance(verification_identity.get("draft_id"), str) else None,
        lifecycle_stage=_require_nonempty_string_from_mapping(progress_payload, "lifecycle_stage", context="grant-progress"),
        workspace_locator={
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_root": str(Path(resolved_input_path).expanduser().resolve()),
            "workspace_path": str(Path(resolved_input_path).expanduser().resolve()),
        },
        runtime_control=runtime_control,
        session_continuity=session_continuity,
        task_lifecycle=task_lifecycle,
        progress_projection=manifest_progress_projection,
        artifact_inventory=artifact_inventory,
        artifact_locator_contract=artifact_locator_contract,
        domain_memory_descriptor=domain_memory_surfaces["domain_memory_descriptor"],
        domain_memory_descriptor_locator=domain_memory_surfaces["domain_memory_descriptor_locator"],
        controlled_domain_memory_apply_proof=domain_memory_surfaces["controlled_domain_memory_apply_proof"],
        controlled_stage_attempt_projection=controlled_stage_attempt_projection,
        owner_receipt_contract=functional_closure_surfaces["owner_receipt_contract"],
        lifecycle_guarded_apply_proof=functional_closure_surfaces["lifecycle_guarded_apply_proof"],
        runtime_registration=_require_mapping(
            domain_projection,
            "opl_stage_runtime_registration",
            context="skill_catalog.skills.0.domain_projection",
        ),
    )


def build_opl_substrate_adapter_export(
    *,
    input_path: str | Path,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
    lifecycle_stage: str,
    workspace_locator: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
    session_continuity: Mapping[str, Any],
    task_lifecycle: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
    artifact_inventory: Mapping[str, Any],
    artifact_locator_contract: Mapping[str, Any],
    domain_memory_descriptor: Mapping[str, Any],
    domain_memory_descriptor_locator: Mapping[str, Any],
    controlled_domain_memory_apply_proof: Mapping[str, Any],
    controlled_stage_attempt_projection: Mapping[str, Any],
    owner_receipt_contract: Mapping[str, Any],
    lifecycle_guarded_apply_proof: Mapping[str, Any],
    runtime_registration: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    workspace_surface_kind = _require_nonempty_string_from_mapping(
        workspace_locator,
        "workspace_surface_kind",
        context="opl_substrate_adapter.workspace_locator",
    )
    memory_locator = _require_mapping(
        domain_memory_descriptor_locator,
        "memory_locator",
        context="opl_substrate_adapter.domain_memory_descriptor_locator",
    )
    receipt_locator = _require_mapping(
        domain_memory_descriptor_locator,
        "receipt_locator",
        context="opl_substrate_adapter.domain_memory_descriptor_locator",
    )
    runtime_artifact_root = _require_mapping(
        artifact_locator_contract,
        "runtime_artifact_root",
        context="opl_substrate_adapter.artifact_locator_contract",
    )
    receipt_refs = _require_mapping(
        controlled_stage_attempt_projection,
        "receipt_refs",
        context="opl_substrate_adapter.controlled_stage_attempt_projection",
    )
    writeback_receipt_refs = _require_mapping(
        controlled_domain_memory_apply_proof,
        "writeback_receipt_refs",
        context="opl_substrate_adapter.controlled_domain_memory_apply_proof",
    )
    return {
        "surface_kind": "mag_opl_substrate_adapter_export",
        "version": "v1",
        "adapter_id": "mag.opl_substrate_adapter.export.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "export_owner": TARGET_DOMAIN_ID,
        "consumer_owner": "one-person-lab",
        "export_policy": "opaque_index_only_refs_no_domain_truth_payloads",
        "refresh_command": public_cli_command(
            "domain-handler-export",
            "--input",
            str(resolved_input_path),
            "--format",
            "json",
        ),
        "identity": {
            "opaque_workspace_ref": f"mag://workspace/{workspace_id}",
            "opaque_run_ref": f"mag://run/{grant_run_id}",
            "opaque_draft_ref": f"mag://draft/{draft_id or 'no-draft'}",
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
        },
        "workspace_ref_index": {
            "surface_kind": "mag_workspace_ref_index",
            "opaque_ref": f"mag://workspace/{workspace_id}",
            "workspace_surface_kind": workspace_surface_kind,
            "locator_ref": "/product_entry_manifest/workspace_locator",
            "session_ref": "/product_entry_manifest/session_continuity",
            "runtime_restore_ref": "/product_entry_manifest/runtime_control/restore_point",
            "progress_ref": "/product_entry_manifest/progress_projection",
            "index_fields": ["workspace_id", "grant_run_id", "lifecycle_stage"],
            "body_policy": "locator_only_no_workspace_body",
        },
        "source_ref_index": {
            "surface_kind": "mag_source_ref_index",
            "index_policy": "source_refs_only_no_source_body",
            "source_refs": [
                {"role": "domain_entry_contract", "ref": "/product_entry_manifest/domain_entry_contract"},
                {"role": "family_action_catalog", "ref": "/product_entry_manifest/family_action_catalog"},
                {"role": "stage_control_plane", "ref": "/product_entry_manifest/family_stage_control_plane"},
                {"role": "task_lifecycle", "ref": "/product_entry_manifest/task_lifecycle"},
                {"role": "runtime_control", "ref": "/product_entry_manifest/runtime_control"},
                {"role": "progress_projection", "ref": "/product_entry_manifest/progress_projection"},
            ],
            "registration_ref": (
                "/product_entry_manifest/skill_catalog/skills/0/domain_projection/"
                "opl_stage_runtime_registration"
            ),
            "runtime_registration_surface_kind": (
                _require_nonempty_string_from_mapping(
                    runtime_registration,
                    "surface_kind",
                    context="opl_substrate_adapter.runtime_registration",
                )
                if runtime_registration is not None
                else "opl_stage_runtime_domain_registration"
            ),
        },
        "artifact_ref_index": {
            "surface_kind": "mag_artifact_ref_index",
            "artifact_locator_contract_ref": "/product_entry_manifest/artifact_locator_contract",
            "artifact_inventory_ref": "/product_entry_manifest/artifact_inventory",
            "runtime_artifact_root_ref": (
                "/product_entry_manifest/artifact_locator_contract/runtime_artifact_root"
            ),
            "runtime_artifact_root_repo_tracked": bool(runtime_artifact_root.get("repo_tracked")),
            "artifact_ref_count": len(artifact_inventory.get("artifacts") or []),
            "body_policy": "locator_and_inventory_refs_only_no_package_body",
        },
        "memory_ref_index": {
            "surface_kind": "mag_memory_ref_index",
            "domain_memory_descriptor_ref": "/product_entry_manifest/domain_memory_descriptor",
            "domain_memory_descriptor_locator_ref": (
                "/product_entry_manifest/domain_memory_descriptor_locator"
            ),
            "memory_locator_ref": "/product_entry_manifest/domain_memory_descriptor_locator/memory_locator",
            "receipt_locator_ref": "/product_entry_manifest/domain_memory_descriptor_locator/receipt_locator",
            "controlled_apply_proof_ref": (
                "/product_entry_manifest/controlled_domain_memory_apply_proof"
            ),
            "memory_locator_repo_tracked": bool(memory_locator.get("repo_tracked")),
            "receipt_locator_repo_tracked": bool(receipt_locator.get("repo_tracked")),
            "writeback_receipt_refs": dict(writeback_receipt_refs),
            "body_policy": "locator_and_receipt_refs_only_no_memory_body",
        },
        "lifecycle_ref_index": {
            "surface_kind": "mag_lifecycle_ref_index",
            "session_continuity_ref": "/product_entry_manifest/session_continuity",
            "task_lifecycle_ref": "/product_entry_manifest/task_lifecycle",
            "controlled_stage_attempt_ref": "/product_entry_manifest/controlled_stage_attempt_projection",
            "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
            "lifecycle_guarded_apply_proof_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
            "receipt_refs": dict(receipt_refs),
            "runtime_state_refs": [
                "/product_entry_manifest/runtime_control/restore_point",
                "/product_entry_manifest/session_continuity",
                "/product_entry_manifest/task_lifecycle",
            ],
        },
        "projection_ref_index": {
            "surface_kind": "mag_projection_ref_index",
            "runtime_control_ref": "/product_entry_manifest/runtime_control",
            "runtime_continuity_ref": (
                "/product_entry_manifest/skill_catalog/skills/0/domain_projection/runtime_continuity"
            ),
            "progress_projection_ref": "/product_entry_manifest/progress_projection",
            "artifact_inventory_ref": "/product_entry_manifest/artifact_inventory",
            "operator_loop_surface_ref": "/product_entry_manifest/operator_loop_surface",
        },
        "body_exposure_policy": {
            "workspace": "opaque_ref_and_locator_ref_only",
            "source": "json_pointer_refs_only",
            "artifact": "locator_index_only_no_package_body",
            "memory": "locator_receipt_refs_only_no_memory_body",
            "owner_receipt": "receipt_ref_only_no_authority_transfer",
        },
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "fundability_verdict_owner": TARGET_DOMAIN_ID,
            "authoring_quality_verdict_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_verdict_owner": TARGET_DOMAIN_ID,
            "package_body_owner": TARGET_DOMAIN_ID,
            "memory_body_owner": TARGET_DOMAIN_ID,
            "owner_receipt_authority_owner": TARGET_DOMAIN_ID,
            "opl_role": "opaque_index_and_locator_ref_consumer_only",
            "opl_can_write_grant_truth": False,
            "opl_can_hold_fundability_verdict": False,
            "opl_can_hold_authoring_quality_verdict": False,
            "opl_can_hold_submission_ready_export_verdict": False,
            "opl_can_read_package_body": False,
            "opl_can_read_memory_body": False,
            "opl_can_mutate_artifact_body": False,
            "opl_can_accept_or_reject_memory_writeback": False,
            "opl_can_issue_owner_receipt": False,
        },
        "forbidden_payload_classes": [
            "grant_truth",
            "fundability_verdict",
            "authoring_quality_verdict",
            "submission_ready_export_verdict",
            "package_body",
            "memory_body",
            "owner_receipt_authority",
            "canonical_grant_artifact_content",
        ],
        "source_surface_refs": [
            "/product_entry_manifest/workspace_locator",
            "/product_entry_manifest/session_continuity",
            "/product_entry_manifest/task_lifecycle",
            "/product_entry_manifest/runtime_control",
            "/product_entry_manifest/progress_projection",
            "/product_entry_manifest/artifact_inventory",
            "/product_entry_manifest/artifact_locator_contract",
            "/product_entry_manifest/domain_memory_descriptor",
            "/product_entry_manifest/domain_memory_descriptor_locator",
            "/product_entry_manifest/controlled_domain_memory_apply_proof",
            "/product_entry_manifest/owner_receipt_contract",
            "/product_entry_manifest/lifecycle_guarded_apply_proof",
        ],
        "freshness": {
            "status": "manifest_projection",
            "refresh_policy": "rebuild_product_entry_manifest_or_domain_handler_export_before_opl_indexing",
            "stale_if_source_refs_missing": True,
        },
    }
