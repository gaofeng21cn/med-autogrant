from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string_from_mapping,
)


SKELETON_SURFACE_KIND = "standard_domain_agent_skeleton"
SKELETON_ID = "mag.standard_domain_agent_skeleton.v1"


def build_standard_domain_agent_skeleton(
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
        "canonical_semantic_pack_root": "agent/",
        "canonical_semantic_pack_role": "repo_source_declarative_grant_pack",
        "repo_source_boundary": {
            "agent": {
                "owner": TARGET_DOMAIN_ID,
                "role": "canonical declarative grant pack with prompts, stages, skills, quality gates, and knowledge boundaries",
                "source_refs": [
                    "agent/prompts/call_and_candidate_intake.md",
                    "agent/prompts/fundability_strategy.md",
                    "agent/prompts/specific_aims_and_structure.md",
                    "agent/prompts/proposal_authoring.md",
                    "agent/prompts/review_and_rebuttal.md",
                    "agent/prompts/package_and_submit_ready.md",
                    "agent/stages/call_and_candidate_intake.md",
                    "agent/stages/fundability_strategy.md",
                    "agent/stages/specific_aims_and_structure.md",
                    "agent/stages/proposal_authoring.md",
                    "agent/stages/review_and_rebuttal.md",
                    "agent/stages/package_and_submit_ready.md",
                    "agent/skills/grant_authoring.md",
                    "agent/quality_gates/fundability.md",
                    "agent/quality_gates/quality.md",
                    "agent/quality_gates/export_and_package.md",
                    "agent/quality_gates/memory_and_receipts.md",
                    "agent/quality_gates/authority_boundaries.md",
                    "agent/knowledge/grant_strategy_memory.md",
                    "agent/knowledge/package_authority.md",
                    "agent/knowledge/owner_receipt_boundary.md",
                ],
                "human_readable_provenance_refs": [
                    "agent/README.md",
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
                "role": "domain_handler/projection/lifecycle adapter declarations only",
                "declared_surfaces": [
                    "domain_handler_adapter",
                    "projection_builder",
                    "family_lifecycle_adapter",
                ],
                "source_refs": [
                    "src/med_autogrant/product_entry_parts/domain_handler.py",
                    "src/med_autogrant/product_entry_parts/runtime_registration.py",
                    "src/med_autogrant/product_entry_parts/manifest_builder.py",
                    "src/med_autogrant/product_entry_parts/manifest_shell/runtime_task_shell.py",
                    "src/med_autogrant/product_entry_parts/manifest_shell/shell_assembly.py",
                ],
            },
            "docs": {
                "owner": TARGET_DOMAIN_ID,
                "role": "human-readable positioning, status, invariants, and adoption notes",
                "source_refs": [
                    "docs/status.md",
                    "docs/project.md",
                    "docs/invariants.md",
                    "docs/references/integration/opl-family-contract-adoption.md",
                ],
            },
        },
        "runtime_declaration": {
            "runtime_only_declares": [
                "domain_handler",
                "projection_builder",
                "lifecycle_adapter",
            ],
            "domain_handler_ref": "/product_entry_manifest/skill_catalog/skills/0/domain_projection/opl_stage_runtime_registration",
            "projection_builder_ref": "/product_entry_manifest/family_stage_control_plane",
            "lifecycle_adapter_ref": (
                "/product_entry_manifest/skill_catalog/skills/0/domain_projection/"
                "opl_stage_runtime_registration/family_lifecycle_adapter"
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
            "canonical_prompt_ref_root": "agent/prompts",
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
        "controlled_domain_memory_apply_proof_ref": "/product_entry_manifest/controlled_domain_memory_apply_proof",
        "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
        "lifecycle_guarded_apply_proof_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
        "physical_skeleton_follow_through_ref": "/product_entry_manifest/physical_skeleton_follow_through",
        "repo_source_layout_audit_ref": (
            "/product_entry_manifest/controlled_domain_memory_apply_proof/repo_source_layout_audit"
        ),
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
            "/product_entry_manifest/owner_receipt_contract",
            "/product_entry_manifest/lifecycle_guarded_apply_proof",
            "/product_entry_manifest/physical_skeleton_follow_through",
        ],
        "authority_boundary": {
            "opl_role": "descriptor_and_ref_consumer_only",
            "can_hold_fundability_verdict": False,
            "can_hold_export_verdict": False,
            "can_write_grant_artifacts": False,
            "can_mutate_runtime_artifact_root": False,
        },
    }
