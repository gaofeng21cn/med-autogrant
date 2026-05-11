from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.domain_agent_skeleton import (
    build_domain_memory_descriptor_locator,
)
from med_autogrant.product_entry_parts.domain_memory_runtime import (
    build_domain_memory_operator_projection_contract,
)
from med_autogrant.product_entry_parts.primitives import (
    _optional_string_from_mapping,
    _require_nonempty_string_from_mapping,
)


def build_manifest_domain_memory_descriptor_locator(
    *,
    progress_payload: Mapping[str, Any],
    verification_identity: Mapping[str, Any],
) -> dict[str, Any]:
    return build_domain_memory_descriptor_locator(
        grant_run_id=_require_nonempty_string_from_mapping(
            progress_payload,
            "grant_run_id",
            context="grant-progress",
        ),
        workspace_id=_require_nonempty_string_from_mapping(
            progress_payload,
            "workspace_id",
            context="grant-progress",
        ),
        draft_id=_optional_string_from_mapping(verification_identity, "draft_id"),
        lifecycle_stage=_require_nonempty_string_from_mapping(
            progress_payload,
            "lifecycle_stage",
            context="grant-progress",
        ),
        operator_receipt_projection=build_domain_memory_operator_projection_contract(),
    )


def build_manifest_domain_memory_surfaces(
    *,
    progress_payload: Mapping[str, Any],
    verification_identity: Mapping[str, Any],
) -> dict[str, Any]:
    locator = build_manifest_domain_memory_descriptor_locator(
        progress_payload=progress_payload,
        verification_identity=verification_identity,
    )
    return {
        "domain_memory_descriptor": build_manifest_domain_memory_descriptor(
            domain_memory_descriptor_locator=locator,
        ),
        "domain_memory_descriptor_locator": locator,
    }


def build_manifest_domain_memory_descriptor(
    *,
    domain_memory_descriptor_locator: Mapping[str, Any],
) -> dict[str, Any]:
    stage_applicability = [
        _require_nonempty_string_from_mapping(
            stage_ref,
            "stage_id",
            context="domain_memory_descriptor_locator.stage_descriptor_refs",
        )
        for stage_ref in domain_memory_descriptor_locator.get("stage_descriptor_refs") or []
        if isinstance(stage_ref, Mapping)
    ]
    if not stage_applicability:
        raise ValueError("domain_memory_descriptor requires at least one stage_descriptor_ref stage_id.")

    return {
        "surface_kind": "family_domain_memory_ref",
        "version": "family-domain-memory-ref.v1",
        "memory_ref_id": "mag_grant_strategy_memory",
        "target_domain_id": "med-autogrant",
        "owner": "Med Auto Grant",
        "memory_family": "grant_strategy_memory",
        "memory_pack_ref": {
            "ref_kind": "repo_policy_and_runtime_locator",
            "ref": "docs/references/grant_strategy_memory_policy.md",
            "role": "grant_strategy_memory_policy_seed",
            "runtime_locator_ref": (
                "/product_entry_manifest/domain_memory_descriptor_locator/memory_locator"
            ),
        },
        "stage_applicability": stage_applicability,
        "retrieval_contract_ref": {
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/domain_memory_descriptor_locator/memory_locator",
            "role": "domain_owned_stage_retrieval_locator",
        },
        "writeback_contract_ref": {
            "ref_kind": "json_pointer",
            "ref": (
                "/product_entry_manifest/domain_memory_descriptor_locator/"
                "writeback_proposal_generator"
            ),
            "role": "domain_owned_writeback_proposal_contract",
            "accept_reject_ref": (
                "/product_entry_manifest/domain_memory_descriptor_locator/"
                "accept_reject_command"
            ),
        },
        "receipt_contract_ref": {
            "ref_kind": "json_pointer",
            "ref": (
                "/product_entry_manifest/domain_memory_descriptor_locator/"
                "operator_receipt_projection"
            ),
            "role": "operator_receipt_projection_no_memory_body",
        },
        "recall_projection_ref": {
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/domain_memory_descriptor_locator/stage_descriptor_refs",
            "role": "stage_memory_context_refs",
        },
        "migration_plan_ref": {
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/domain_memory_descriptor_locator/migration_plan",
            "role": "domain_owned_migration_plan",
        },
        "seed_corpus_ref": {
            "ref_kind": "repo_path",
            "ref": "contracts/runtime-program/domain-memory-seed-fixture.json",
            "role": "repo_source_seed_fixture_no_real_memory_entries",
        },
        "writeback_receipt_locator_ref": {
            "ref_kind": "json_pointer",
            "ref": "/product_entry_manifest/domain_memory_descriptor_locator/receipt_locator",
            "role": "domain_owned_writeback_receipt_locator",
        },
        "provenance_refs": [
            {
                "ref_kind": "json_pointer",
                "ref": "/product_entry_manifest/domain_memory_descriptor_locator",
                "role": "mag_domain_memory_locator",
            },
            {
                "ref_kind": "human_doc",
                "ref": "docs/references/grant_strategy_memory_policy.md",
                "role": "policy",
            },
            {
                "ref_kind": "repo_path",
                "ref": "contracts/runtime-program/domain-memory-seed-fixture.json",
                "role": "seed_fixture",
            },
        ],
        "freshness": {
            "status": "manifest_projection",
            "refresh_policy": "rebuild_product_entry_manifest_before_opl_discovery",
            "source_descriptor_ref": "/product_entry_manifest/domain_memory_descriptor_locator",
            "stale_if_locator_or_policy_missing": True,
        },
        "migration_readiness": {
            "status": "migration_plan_ready_descriptor_only",
            "seed_fixture_status": "repo_source_fixture_available",
            "memory_body_migration": "domain_owned_runtime_apply_required",
            "accept_reject_authority": "med-autogrant",
            "writeback_receipt_locator_status": "descriptor_locator_declared",
            "opl_apply_allowed": False,
        },
        "status": "active",
        "authority_boundary": {
            "opl_role": "locator_projection_owner",
            "domain_memory_owner": "med-autogrant",
            "domain_router_owner": "med-autogrant",
            "forbidden_opl_authority": [
                "memory_store_owner",
                "domain_truth_owner",
                "quality_verdict_owner",
                "artifact_authority",
                "fundability_verdict_owner",
                "authoring_quality_verdict_owner",
                "submission_ready_export_verdict_owner",
                "grant_artifact_authority",
                "memory_accept_reject_owner",
            ],
            "can_write_domain_truth": False,
            "can_authorize_quality_verdict": False,
            "can_authorize_fundability_verdict": False,
            "can_authorize_submission_readiness": False,
            "can_write_artifacts": False,
            "can_accept_or_reject_memory_writeback": False,
        },
    }
