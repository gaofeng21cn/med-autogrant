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
        "ideal_state_closure_status": build_ideal_state_closure_status(),
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
            "domain-memory receipt evidence writer persists accepted/rejected receipt instances under runtime roots only",
        ],
        "legacy_active_path_policy": "physically_removed_or_history_tombstone_only",
        "legacy_active_path_residue": [
            {
                "path_family": "default Hermes active path",
                "state": "tombstone_only",
                "evidence_ref": "docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md",
            },
            {
                "path_family": "default Gateway active path",
                "state": "physically_removed_from_active_source",
                "evidence_ref": "docs/decisions.md#2026-05-12-temporal-backed-opl-production-runtime-supersedes-gateway-manager-wording",
            },
            {
                "path_family": "default local-manager active path",
                "state": "physically_removed_from_active_source",
                "evidence_ref": "docs/status.md#旧面退役校准",
            },
        ],
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


def build_ideal_state_closure_status() -> dict[str, Any]:
    return {
        "surface_kind": "mag_ideal_state_closure_status",
        "version": "v1",
        "closure_id": "mag.ideal_state.cross_repo_gap.closure_status.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "state": "repo_closure_landed_external_evidence_gated",
        "plan_ref": "docs/active/mag-ideal-state-cross-repo-gap-plan.md",
        "north_star_ref": "docs/references/med-auto-grant-ideal-state.md",
        "current_truth_refs": [
            "docs/status.md",
            "docs/architecture.md",
            "docs/invariants.md",
            "docs/decisions.md",
            "contracts/runtime-program/current-program.json",
            "/product_entry_manifest",
        ],
        "claims_production_long_run_soak_complete": False,
        "repo_source_exclusions": {
            "workspace_artifacts": True,
            "runtime_receipt_instances": True,
            "memory_body": True,
            "export_packages": True,
        },
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "fundability_verdict_owner": TARGET_DOMAIN_ID,
            "authoring_quality_verdict_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_verdict_owner": TARGET_DOMAIN_ID,
            "memory_body_owner": TARGET_DOMAIN_ID,
            "opl_role": "framework_ledger_projection_and_transport_only",
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_export_ready": False,
            "opl_can_mutate_grant_artifacts": False,
        },
        "mag_owned_transition_oracle": {
            "surface_kind": "mag_grant_transition_oracle_gap_status",
            "owner": TARGET_DOMAIN_ID,
            "state": "domain_spec_planned_external_runner_gate",
            "domain_spec_ref": "docs/active/mag-ideal-state-cross-repo-gap-plan.md#P5",
            "oracle_fixture_status": "not_landed",
            "transition_table_status": "not_landed",
            "runner_owner": "one-person-lab",
            "runner_status": "external_opl_generic_runner_gate",
            "mag_will_define": [
                "grant transition table",
                "fundability / aims / review / package guards",
                "typed blocker mapping",
                "domain owner action",
                "oracle fixtures",
            ],
            "mag_will_not_define": [
                "generic state-machine runner",
                "generic queue",
                "generic retry/dead-letter runtime",
                "OPL provider completion verdict",
            ],
            "opl_must_not_infer": [
                "fundability_ready",
                "authoring_quality_ready",
                "submission_ready_export_ready",
            ],
        },
        "direct_retirement_posture": {
            "state": "active",
            "policy": "migrate_active_callers_then_delete_or_history_tombstone",
            "forbidden_compatibility_surfaces": [
                "compatibility alias",
                "facade patch bridge",
                "re-export facade",
                "compatibility-only aggregate test",
                "legacy flat CLI shell alias",
            ],
            "current_manifest_surface_ref": "/product_entry_manifest/physical_skeleton_follow_through",
            "current_audit_surface_ref": "/product_entry_manifest/controlled_domain_memory_apply_proof/repo_source_layout_audit",
        },
        "phases": [
            _build_ideal_state_phase_status(
                phase_id="P0",
                title="gap plan and owner boundary",
                state="landed",
                mag_surface_refs=[
                    "docs/active/README.md",
                    "docs/docs_portfolio_consolidation.md",
                    "docs/active/mag-ideal-state-cross-repo-gap-plan.md",
                ],
                required_evidence_refs=["scripts_verify_meta"],
            ),
            _build_ideal_state_phase_status(
                phase_id="P1",
                title="OPL-hosted MAG grant-stage receipt evidence to live soak",
                state="external_evidence_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/controlled_stage_attempt_projection",
                    "/product_entry_manifest/owner_receipt_contract",
                    "/product_entry_manifest/controlled_soak_no_regression_attempt",
                    "product owner-receipt-evidence",
                    "product sidecar-dispatch stage-attempt/closeout",
                ],
                required_evidence_refs=[
                    "opl_runtime_ledger_mag_controlled_stage_attempt_ref",
                    "mag_runtime_owner_receipt_instance_ref",
                    "mag_no_regression_evidence_or_typed_blocker_ref",
                ],
            ),
            _build_ideal_state_phase_status(
                phase_id="P2",
                title="OPL generic primitive absorption",
                state="external_opl_primitive_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/family_action_catalog",
                    "/product_entry_manifest/family_stage_control_plane",
                    "/product_entry_manifest/artifact_locator_contract",
                    "/product_entry_manifest/domain_memory_descriptor",
                    "/product_entry_manifest/ideal_state_closure_status",
                ],
                required_evidence_refs=[
                    "opl_generic_primitive_consumes_two_or_more_domains_ref",
                    "opl_workbench_authority_boundary_projection_ref",
                ],
            ),
            _build_ideal_state_phase_status(
                phase_id="P3",
                title="grant strategy memory live apply generalization",
                state="runtime_workspace_evidence_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/domain_memory_descriptor_locator",
                    "/product_entry_manifest/controlled_domain_memory_apply_proof",
                    "product domain-memory-proposal",
                    "product domain-memory-decision",
                    "product domain-memory-receipt-evidence",
                ],
                required_evidence_refs=[
                    "mag_runtime_memory_body_migration_ref",
                    "mag_runtime_accepted_memory_receipt_ref",
                    "mag_runtime_rejected_memory_receipt_ref",
                    "opl_domain_memory_locator_projection_without_body_ref",
                ],
            ),
            _build_ideal_state_phase_status(
                phase_id="P4",
                title="package export and lifecycle productionization",
                state="runtime_workspace_evidence_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                    "/product_entry_manifest/artifact_locator_contract",
                    "package submission-ready",
                    "product lifecycle-receipt-evidence",
                    "product sidecar-dispatch lifecycle/receipt",
                ],
                required_evidence_refs=[
                    "mag_runtime_lifecycle_cleanup_receipt_ref",
                    "mag_runtime_lifecycle_restore_receipt_ref",
                    "mag_runtime_lifecycle_retention_receipt_ref",
                    "opl_package_export_lifecycle_shell_ref",
                ],
            ),
            _build_ideal_state_phase_status(
                phase_id="P5",
                title="physical skeleton follow-through and legacy direct retirement",
                state="landed_with_external_delete_audit_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/standard_domain_agent_skeleton",
                    "/product_entry_manifest/physical_skeleton_follow_through",
                    "/product_entry_manifest/controlled_domain_memory_apply_proof/repo_source_layout_audit",
                    "docs/status.md#旧面退役校准",
                ],
                required_evidence_refs=[
                    "opl_agents_list_mag_descriptor_no_drift_ref",
                    "active_path_scan_no_legacy_default_caller_ref",
                ],
            ),
        ],
    }


def _build_ideal_state_phase_status(
    *,
    phase_id: str,
    title: str,
    state: str,
    mag_surface_refs: list[str],
    required_evidence_refs: list[str],
) -> dict[str, Any]:
    return {
        "phase_id": phase_id,
        "title": title,
        "state": state,
        "mag_surface_refs": mag_surface_refs,
        "required_evidence_refs": required_evidence_refs,
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
