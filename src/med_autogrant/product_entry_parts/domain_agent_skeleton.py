from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string_from_mapping,
)


SKELETON_SURFACE_KIND = "standard_domain_agent_skeleton_mapping"
SKELETON_ID = "mag.standard_domain_agent_skeleton.v1"
ARTIFACT_LOCATOR_KIND = "domain_artifact_locator_contract"
CONTROLLED_STAGE_ATTEMPT_KIND = "controlled_stage_attempt_projection"
DOMAIN_MEMORY_DESCRIPTOR_LOCATOR_KIND = "domain_memory_descriptor_locator"


def build_domain_agent_skeleton_mapping(
    *,
    input_path: str | Path,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
    lifecycle_stage: str,
    family_stage_control_plane: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
    artifact_locator_contract: Mapping[str, Any],
    controlled_stage_attempt_projection: Mapping[str, Any],
    domain_memory_descriptor_locator: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "surface_kind": SKELETON_SURFACE_KIND,
        "version": "v1",
        "skeleton_id": SKELETON_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "mapping_state": "descriptor_manifest_adapter_landed",
        "repo_source_boundary": {
            "agent": {
                "owner": TARGET_DOMAIN_ID,
                "role": "domain entry, prompt/skill references, stage descriptors, and MAG-owned quality gates",
                "source_refs": [
                    "src/med_autogrant/domain_entry.py",
                    "src/med_autogrant/domain_entry_contract.py",
                    "src/med_autogrant/stage_control_plane.py",
                ],
            },
            "contracts": {
                "owner": TARGET_DOMAIN_ID,
                "role": "machine-readable runtime-program, schema, adoption, and authority contracts",
                "source_refs": [
                    "contracts/runtime-program/current-program.json",
                    "contracts/runtime-program/opl-family-contract-adoption.json",
                    "schemas/v1/product-entry-manifest.schema.json",
                ],
            },
            "runtime": {
                "owner": TARGET_DOMAIN_ID,
                "role": "sidecar/projection/lifecycle adapter declarations only",
                "declared_surfaces": [
                    "product_sidecar_adapter",
                    "projection_builder",
                    "family_lifecycle_adapter",
                ],
                "source_refs": [
                    "src/med_autogrant/product_entry_parts/sidecar.py",
                    "src/med_autogrant/product_entry_parts/runtime_registration.py",
                    "src/med_autogrant/product_entry_parts/manifest_builder.py",
                ],
            },
            "docs": {
                "owner": TARGET_DOMAIN_ID,
                "role": "human-readable positioning, status, invariants, and adoption notes",
                "source_refs": [
                    "docs/status.md",
                    "docs/project.md",
                    "docs/invariants.md",
                    "docs/references/opl_family_contract_adoption.md",
                ],
            },
        },
        "runtime_declaration": {
            "runtime_only_declares": [
                "sidecar",
                "projection_builder",
                "lifecycle_adapter",
            ],
            "sidecar_ref": "/product_entry_manifest/skill_catalog/skills/0/domain_projection/opl_runtime_manager_registration",
            "projection_builder_ref": "/product_entry_manifest/family_stage_control_plane",
            "lifecycle_adapter_ref": (
                "/product_entry_manifest/skill_catalog/skills/0/domain_projection/"
                "opl_runtime_manager_registration/family_lifecycle_adapter"
            ),
            "default_runtime_owner": _require_nonempty_string_from_mapping(
                runtime_control,
                "runtime_owner",
                context="domain_agent_skeleton.runtime_control",
            ),
            "domain_truth_owner": TARGET_DOMAIN_ID,
        },
        "stage_mapping": {
            "stage_control_plane_ref": "/product_entry_manifest/family_stage_control_plane",
            "stage_ids": [
                str(stage["stage_id"])
                for stage in family_stage_control_plane.get("stages", [])
                if isinstance(stage, Mapping) and stage.get("stage_id")
            ],
            "descriptor_only": True,
        },
        "quality_gate_mapping": {
            "fundability_verdict_owner": TARGET_DOMAIN_ID,
            "authoring_quality_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_verdict_owner": TARGET_DOMAIN_ID,
            "opl_quality_role": "consume_refs_only_no_verdict_authority",
            "quality_refs": [
                "/product_entry_manifest/grant_authoring_readiness",
                "/product_entry_manifest/runtime_control/semantic_closure",
                "/product_entry_manifest/family_stage_control_plane/authority_boundary",
            ],
        },
        "artifact_locator_ref": "/product_entry_manifest/artifact_locator_contract",
        "controlled_stage_attempt_ref": "/product_entry_manifest/controlled_stage_attempt_projection",
        "domain_memory_descriptor_locator_ref": "/product_entry_manifest/domain_memory_descriptor_locator",
        "artifact_locator_contract": dict(artifact_locator_contract),
        "controlled_stage_attempt_projection": dict(controlled_stage_attempt_projection),
        "domain_memory_descriptor_locator": dict(domain_memory_descriptor_locator),
        "identity": {
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
            "input_path": str(Path(input_path).expanduser().resolve()),
        },
        "source_refs": [
            "/product_entry_manifest/family_action_catalog",
            "/product_entry_manifest/family_stage_control_plane",
            "/product_entry_manifest/runtime_control",
            "/product_entry_manifest/progress_projection",
            "/product_entry_manifest/artifact_locator_contract",
            "/product_entry_manifest/controlled_stage_attempt_projection",
            "/product_entry_manifest/domain_memory_descriptor_locator",
        ],
        "authority_boundary": {
            "opl_role": "descriptor_and_ref_consumer_only",
            "can_hold_fundability_verdict": False,
            "can_hold_export_verdict": False,
            "can_write_grant_artifacts": False,
            "can_mutate_runtime_artifact_root": False,
        },
    }


def build_domain_memory_descriptor_locator(
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
    lifecycle_stage: str,
) -> dict[str, Any]:
    return {
        "surface_kind": DOMAIN_MEMORY_DESCRIPTOR_LOCATOR_KIND,
        "version": "v1",
        "descriptor_id": "mag.domain_memory_descriptor_locator.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "memory_owner": TARGET_DOMAIN_ID,
        "memory_content_owner": TARGET_DOMAIN_ID,
        "fundability_verdict_owner": TARGET_DOMAIN_ID,
        "truth_owner": TARGET_DOMAIN_ID,
        "policy_ref": {
            "ref_kind": "repo_path",
            "ref": "docs/references/grant_strategy_memory_policy.md",
            "role": "human_policy",
        },
        "stage_descriptor_refs": [
            {
                "ref_kind": "json_pointer",
                "ref": f"/product_entry_manifest/family_stage_control_plane/stages/{stage_index}",
                "stage_id": stage_id,
                "role": "stage_memory_context_descriptor",
            }
            for stage_index, stage_id in enumerate(
                [
                    "call_and_candidate_intake",
                    "fundability_strategy",
                    "specific_aims_and_structure",
                    "proposal_authoring",
                    "review_and_rebuttal",
                    "package_and_submit_ready",
                ]
            )
        ],
        "memory_locator": {
            "locator_kind": "domain_memory_locator",
            "runtime_memory_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/",
            "repo_tracked": False,
            "content_policy": "locator_only_no_memory_content_in_repo_manifest",
            "retrieval_policy": "stage_specific_small_relevant_sets",
            "accepted_memory_ref_template": (
                "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/"
                "accepted/<memory_id>.json"
            ),
            "writeback_proposal_ref_template": (
                "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/"
                "writeback-proposals/<grant_run_id>/<proposal_id>.json"
            ),
        },
        "writeback_receipt_refs": {
            "receipt_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/",
            "memory_writeback_receipt_ref": (
                "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
                f"{grant_run_id}/memory-writeback/<proposal_id>.json"
            ),
            "receipt_write_policy": "receipt_ref_only_no_domain_memory_content_mutation",
        },
        "identity": {
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
        },
        "allowed_memory_roles": [
            "strategy_context",
            "stage_retrieval_hint",
            "writeback_proposal",
            "writeback_receipt_ref",
        ],
        "forbidden_memory_roles": [
            "fundability_verdict",
            "authoring_quality_verdict",
            "submission_ready_export_verdict",
            "canonical_grant_artifact_content",
            "workspace_private_evidence",
        ],
        "opl_consumption_contract": {
            "role": "locator_ref_and_receipt_ref_consumer_only",
            "consumes": [
                "descriptor",
                "policy_ref",
                "stage_descriptor_refs",
                "memory_locator",
                "writeback_receipt_refs",
            ],
            "does_not_consume": [
                "memory_content",
                "fundability_verdict",
                "authoring_quality_verdict",
                "submission_ready_export_verdict",
                "canonical_grant_artifact_content",
            ],
            "can_hold_memory_content": False,
            "can_issue_fundability_verdict": False,
            "can_issue_authoring_quality_verdict": False,
            "can_issue_export_verdict": False,
            "can_mutate_domain_memory_store": False,
        },
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "memory_content_owner": TARGET_DOMAIN_ID,
            "fundability_verdict_owner": TARGET_DOMAIN_ID,
            "authoring_quality_verdict_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_verdict_owner": TARGET_DOMAIN_ID,
            "opl_role": "memory_locator_ref_and_receipt_ref_consumer_only",
        },
    }


def build_artifact_locator_contract(
    *,
    input_path: str | Path,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
    lifecycle_stage: str,
    artifact_inventory: Mapping[str, Any],
) -> dict[str, Any]:
    runtime_artifact_root = (
        "$CODEX_HOME/projects/med-autogrant/runtime-state/artifacts/"
        f"{grant_run_id}/"
    )
    return {
        "surface_kind": ARTIFACT_LOCATOR_KIND,
        "version": "v1",
        "locator_id": "mag.artifact_locator.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "workspace_locator": {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": str(Path(input_path).expanduser().resolve()),
            "workspace_id": workspace_id,
            "grant_run_id": grant_run_id,
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
        },
        "runtime_artifact_root": {
            "root_kind": "runtime_artifact_root",
            "path_template": runtime_artifact_root,
            "repo_tracked": False,
            "owner": TARGET_DOMAIN_ID,
            "write_policy": "mag_runtime_or_export_surface_only",
        },
        "repo_source_policy": {
            "repo_source_contains_artifact_descriptors_only": True,
            "real_grant_artifacts_must_live_in": [
                "workspace document",
                "workspace-local artifact path",
                "runtime_artifact_root",
            ],
            "forbidden_repo_source_artifacts": [
                "final grant proposal body",
                "submission-ready export package",
                "receipt instance",
                "intermediate authoring artifact",
            ],
        },
        "artifact_inventory_ref": "/product_entry_manifest/artifact_inventory",
        "artifact_refs": list(artifact_inventory.get("artifacts") or []),
        "opl_consumption": {
            "role": "index_locator_refs_only",
            "can_copy_canonical_artifacts": False,
            "can_issue_fundability_verdict": False,
            "can_issue_export_verdict": False,
            "requires_mag_receipt_for_domain_artifact_mutation": True,
        },
    }


def build_controlled_stage_attempt_projection(
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
    lifecycle_stage: str,
    progress_projection: Mapping[str, Any],
    task_lifecycle: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "surface_kind": CONTROLLED_STAGE_ATTEMPT_KIND,
        "version": "v1",
        "attempt_id": f"{workspace_id}:{draft_id or 'no-draft'}:{lifecycle_stage}",
        "target_domain_id": TARGET_DOMAIN_ID,
        "attempt_owner": TARGET_DOMAIN_ID,
        "grant_run_id": grant_run_id,
        "workspace_id": workspace_id,
        "draft_id": draft_id,
        "lifecycle_stage": lifecycle_stage,
        "maps_to_opl_contract": "opl_family_runtime_attempt_contract.v1",
        "source_refs": [
            "/product_entry_manifest/task_lifecycle",
            "/product_entry_manifest/progress_projection",
            "/product_entry_manifest/runtime_control",
            "/product_entry_manifest/family_stage_control_plane",
            "/product_entry_manifest/artifact_locator_contract",
        ],
        "attempt_state": _require_nonempty_string_from_mapping(
            task_lifecycle,
            "status",
            context="controlled_stage_attempt.task_lifecycle",
        ),
        "last_observed_projection": dict(progress_projection),
        "receipt_refs": {
            "sidecar_dispatch_receipt_ref": (
                "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
                f"{grant_run_id}/sidecar-dispatch/<task_id>.json"
            ),
            "stage_attempt_receipt_ref": (
                "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
                f"{grant_run_id}/stage-attempt/{lifecycle_stage}.json"
            ),
        },
        "opl_consumption_contract": {
            "consumes": [
                "descriptor",
                "source_refs",
                "receipt_refs",
                "runtime_status_projection",
            ],
            "does_not_consume": [
                "fundability_verdict",
                "submission_ready_export_verdict",
                "canonical_grant_artifact_content",
            ],
            "can_hold_fundability_verdict": False,
            "can_hold_export_verdict": False,
        },
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "fundability_verdict_owner": TARGET_DOMAIN_ID,
            "submission_ready_export_verdict_owner": TARGET_DOMAIN_ID,
            "opl_role": "controlled_attempt_descriptor_and_receipt_ref_consumer",
        },
    }
