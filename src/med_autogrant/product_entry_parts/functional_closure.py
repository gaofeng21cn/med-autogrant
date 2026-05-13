from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts import domain_agent_skeleton
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _optional_string_from_mapping,
    _require_nonempty_string_from_mapping,
)


def build_manifest_functional_closure_surfaces(
    *,
    input_path: Path,
    progress_payload: Mapping[str, Any],
    verification_identity: Mapping[str, Any],
    family_stage_control_plane: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
    artifact_locator_contract: Mapping[str, Any],
    controlled_stage_attempt_projection: Mapping[str, Any],
    domain_memory_surfaces: Mapping[str, Any],
) -> dict[str, Any]:
    identity = _manifest_identity(
        progress_payload=progress_payload,
        verification_identity=verification_identity,
    )
    domain_memory_descriptor_locator = _require_mapping(
        domain_memory_surfaces,
        "domain_memory_descriptor_locator",
        context="domain_memory_surfaces",
    )
    standard_domain_agent_skeleton = domain_agent_skeleton.build_standard_domain_agent_skeleton(
        input_path=input_path,
        family_stage_control_plane=family_stage_control_plane,
        runtime_control=runtime_control,
        progress_projection=progress_projection,
        artifact_locator_contract=artifact_locator_contract,
        controlled_stage_attempt_projection=controlled_stage_attempt_projection,
        domain_memory_descriptor_locator=domain_memory_descriptor_locator,
        **identity,
    )
    controlled_domain_memory_apply_proof = _require_mapping(
        domain_memory_surfaces,
        "controlled_domain_memory_apply_proof",
        context="domain_memory_surfaces",
    )
    return {
        "standard_domain_agent_skeleton": standard_domain_agent_skeleton,
        "owner_receipt_contract": build_owner_receipt_contract(
            controlled_stage_attempt_projection=controlled_stage_attempt_projection,
            controlled_domain_memory_apply_proof=controlled_domain_memory_apply_proof,
            artifact_locator_contract=artifact_locator_contract,
            **identity,
        ),
        "lifecycle_guarded_apply_proof": build_lifecycle_guarded_apply_proof(
            artifact_locator_contract=artifact_locator_contract,
            **identity,
        ),
        "physical_skeleton_follow_through": build_physical_skeleton_follow_through(),
    }


def build_owner_receipt_contract(
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
    lifecycle_stage: str,
    controlled_stage_attempt_projection: Mapping[str, Any],
    controlled_domain_memory_apply_proof: Mapping[str, Any],
    artifact_locator_contract: Mapping[str, Any],
) -> dict[str, Any]:
    receipt_refs = _require_mapping(
        controlled_stage_attempt_projection,
        "receipt_refs",
        context="controlled_stage_attempt_projection",
    )
    memory_receipt_refs = _require_mapping(
        controlled_domain_memory_apply_proof,
        "writeback_receipt_refs",
        context="controlled_domain_memory_apply_proof",
    )
    artifact_runtime_root = _require_mapping(
        artifact_locator_contract,
        "runtime_artifact_root",
        context="artifact_locator_contract",
    )
    return {
        "surface_kind": "mag_owner_receipt_contract",
        "version": "v1",
        "contract_id": "mag.owner_receipt.contract.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "receipt_owner": TARGET_DOMAIN_ID,
        "maps_to_opl_contract": "opl_domain_owner_receipt_envelope.v1",
        "allowed_return_shapes": [
            "domain_owner_receipt",
            "typed_blocker",
            "no_regression_evidence",
        ],
        "identity": {
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
        },
        "receipt_ref_templates": {
            "stage_attempt_receipt_ref": _require_nonempty_string_from_mapping(
                receipt_refs,
                "stage_attempt_receipt_ref",
                context="controlled_stage_attempt_projection.receipt_refs",
            ),
            "sidecar_dispatch_receipt_ref": _require_nonempty_string_from_mapping(
                receipt_refs,
                "sidecar_dispatch_receipt_ref",
                context="controlled_stage_attempt_projection.receipt_refs",
            ),
            "memory_writeback_receipt_ref": _require_nonempty_string_from_mapping(
                memory_receipt_refs,
                "memory_writeback_receipt_ref",
                context="controlled_domain_memory_apply_proof.writeback_receipt_refs",
            ),
            "artifact_runtime_root": _require_nonempty_string_from_mapping(
                artifact_runtime_root,
                "path_template",
                context="artifact_locator_contract.runtime_artifact_root",
            ),
        },
        "required_receipt_fields": [
            "surface_kind",
            "receipt_id",
            "owner",
            "attempt_ref",
            "source_refs",
            "artifact_mutation",
            "memory_mutation",
            "lifecycle_mutation",
            "forbidden_write_proof",
        ],
        "source_refs": [
            "/product_entry_manifest/controlled_stage_attempt_projection",
            "/product_entry_manifest/controlled_domain_memory_apply_proof",
            "/product_entry_manifest/artifact_locator_contract",
            "/product_entry_manifest/grant_authoring_readiness",
        ],
        "forbidden_write_proof": {
            "opl_can_write_grant_truth": False,
            "opl_can_write_grant_artifacts": False,
            "opl_can_write_memory_body": False,
            "opl_can_hold_fundability_verdict": False,
            "opl_can_hold_authoring_quality_verdict": False,
            "opl_can_hold_submission_ready_export_verdict": False,
            "mag_owner_receipt_required_for_domain_mutation": True,
        },
    }


def build_lifecycle_guarded_apply_proof(
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
    lifecycle_stage: str,
    artifact_locator_contract: Mapping[str, Any],
) -> dict[str, Any]:
    workspace_locator = _require_mapping(
        artifact_locator_contract,
        "workspace_locator",
        context="artifact_locator_contract",
    )
    runtime_artifact_root = _require_mapping(
        artifact_locator_contract,
        "runtime_artifact_root",
        context="artifact_locator_contract",
    )
    return {
        "surface_kind": "mag_lifecycle_guarded_apply_proof",
        "version": "v1",
        "proof_id": "mag.lifecycle.guarded_apply.proof.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
        "identity": {
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
        },
        "source_refs": [
            "/product_entry_manifest/lifecycle_ledger",
            "/product_entry_manifest/owner_route",
            "/product_entry_manifest/artifact_locator_contract",
            "/product_entry_manifest/runtime_control/restore_point",
        ],
        "artifact_locator_refs": {
            "workspace_path": _require_nonempty_string_from_mapping(
                workspace_locator,
                "workspace_path",
                context="artifact_locator_contract.workspace_locator",
            ),
            "runtime_artifact_root": _require_nonempty_string_from_mapping(
                runtime_artifact_root,
                "path_template",
                context="artifact_locator_contract.runtime_artifact_root",
            ),
        },
        "operations": [
            _build_lifecycle_operation("cleanup"),
            _build_lifecycle_operation("restore"),
            _build_lifecycle_operation("retention"),
        ],
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "artifact_mutation_owner": TARGET_DOMAIN_ID,
            "fundability_verdict_owner": TARGET_DOMAIN_ID,
            "authoring_quality_verdict_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_verdict_owner": TARGET_DOMAIN_ID,
            "opl_role": "ledger_locator_apply_and_receipt_router_only",
            "opl_can_delete_grant_artifacts": False,
            "opl_can_restore_grant_artifacts": False,
            "opl_can_set_retention_for_grant_truth": False,
            "opl_can_write_submission_ready_export_verdict": False,
        },
    }


def build_physical_skeleton_follow_through() -> dict[str, Any]:
    roots = {
        "agent": {
            "owner": TARGET_DOMAIN_ID,
            "anchor_ref": "agent/README.md",
            "state": "physical_root_present",
            "role": "domain skill and stage ownership boundary anchor",
        },
        "contracts": {
            "owner": TARGET_DOMAIN_ID,
            "anchor_ref": "contracts/README.md",
            "state": "physical_root_present",
            "role": "machine-readable contract and schema boundary anchor",
        },
        "runtime": {
            "owner": TARGET_DOMAIN_ID,
            "anchor_ref": "runtime/README.md",
            "state": "physical_root_present",
            "role": "runtime descriptor and sidecar boundary anchor",
        },
        "docs": {
            "owner": TARGET_DOMAIN_ID,
            "anchor_ref": "docs/status.md",
            "state": "physical_root_present",
            "role": "human status and governance boundary anchor",
        },
    }
    repo_root = Path(__file__).resolve().parents[3]
    return {
        "surface_kind": "mag_physical_skeleton_follow_through",
        "version": "v1",
        "follow_through_id": "mag.physical_skeleton.follow_through.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "state": "minimum_repo_source_anchors_landed",
        "roots": roots,
        "root_status": [
            {
                "root": root_key,
                "anchor_ref": root["anchor_ref"],
                "exists": (repo_root / root["anchor_ref"]).exists(),
                "owner": root["owner"],
            }
            for root_key, root in roots.items()
        ],
        "moves_workspace_artifacts": False,
        "moves_runtime_receipt_instances": False,
        "moves_memory_body": False,
        "first_follow_through_scope": [
            "manifest exposes root anchors",
            "repo-source layout audit requires root anchors to exist",
            "workspace artifacts and runtime receipts stay outside repo source",
        ],
        "legacy_active_path_policy": "history_or_tombstone_only_after_no_active_caller",
        "next_physical_moves": [
            {
                "path_family": "domain entry and stage descriptors",
                "source_owner": TARGET_DOMAIN_ID,
                "condition": "path compatibility audit and no-active-caller proof",
            },
            {
                "path_family": "runtime descriptors and sidecar declarations",
                "source_owner": TARGET_DOMAIN_ID,
                "condition": "direct skill and OPL-hosted parity proof",
            },
        ],
    }


def _build_lifecycle_operation(operation: str) -> dict[str, Any]:
    return {
        "operation": operation,
        "opl_apply_scope": "opl_owned_ledger_and_locator_only",
        "domain_mutation_policy": "requires_mag_owner_receipt",
        "artifact_mutation_authority": TARGET_DOMAIN_ID,
        "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
        "typed_blocker": {
            "blocker_kind": "mag_domain_artifact_owner_receipt_required",
            "blocker_id": f"mag_lifecycle_{operation}_owner_receipt_required",
            "owner": TARGET_DOMAIN_ID,
            "source_contract": "opl_lifecycle_guarded_apply_contract",
            "required_return_shapes": [
                "domain_owner_receipt",
                "typed_blocker",
                "no_regression_evidence",
            ],
            "opl_can_execute_domain_artifact_mutation": False,
        },
    }


def _require_mapping(payload: Mapping[str, Any], field_name: str, *, context: str) -> Mapping[str, Any]:
    value = payload.get(field_name)
    if not isinstance(value, Mapping):
        raise ValueError(f"{context} 缺少合法字段: {field_name}")
    return value


def _manifest_identity(
    *,
    progress_payload: Mapping[str, Any],
    verification_identity: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "grant_run_id": _require_nonempty_string_from_mapping(
            progress_payload,
            "grant_run_id",
            context="grant-progress",
        ),
        "workspace_id": _require_nonempty_string_from_mapping(
            progress_payload,
            "workspace_id",
            context="grant-progress",
        ),
        "draft_id": _optional_string_from_mapping(verification_identity, "draft_id"),
        "lifecycle_stage": _require_nonempty_string_from_mapping(
            progress_payload,
            "lifecycle_stage",
            context="grant-progress",
        ),
    }
