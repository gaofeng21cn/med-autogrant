from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.domain_agent_skeleton import (
    build_domain_memory_descriptor_locator,
)
from med_autogrant.product_entry_parts.domain_memory_runtime import (
    build_domain_memory_operator_projection_contract,
)
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
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
        "controlled_domain_memory_apply_proof": build_controlled_domain_memory_apply_proof(
            domain_memory_descriptor_locator=locator,
        ),
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


def build_controlled_domain_memory_apply_proof(
    *,
    domain_memory_descriptor_locator: Mapping[str, Any],
) -> dict[str, Any]:
    memory_locator = _require_mapping_from_locator(domain_memory_descriptor_locator, "memory_locator")
    proposal_generator = _require_mapping_from_locator(
        domain_memory_descriptor_locator,
        "writeback_proposal_generator",
    )
    accept_reject_command = _require_mapping_from_locator(
        domain_memory_descriptor_locator,
        "accept_reject_command",
    )
    operator_receipt_projection = _require_mapping_from_locator(
        domain_memory_descriptor_locator,
        "operator_receipt_projection",
    )
    receipt_locator = _require_mapping_from_locator(domain_memory_descriptor_locator, "receipt_locator")
    controlled_receipt_instances = _build_controlled_receipt_instances(
        receipt_locator=receipt_locator,
    )
    stage_refs = [
        stage_ref
        for stage_ref in domain_memory_descriptor_locator.get("stage_descriptor_refs") or []
        if isinstance(stage_ref, Mapping)
    ]
    accepted_template = _require_nonempty_string_from_mapping(
        memory_locator,
        "accepted_memory_ref_template",
        context="domain_memory_descriptor_locator.memory_locator",
    )
    return {
        "surface_kind": "controlled_grant_stage_domain_memory_apply_proof",
        "version": "v1",
        "proof_id": "mag.domain_memory.controlled_grant_stage_apply.proof.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "proof_state": "repo_source_audit_landed_no_runtime_artifact_write",
        "maps_to_opl_contract": "opl_controlled_domain_memory_apply_proof.v1",
        "domain_memory_descriptor_ref": "/product_entry_manifest/domain_memory_descriptor",
        "domain_memory_descriptor_locator_ref": "/product_entry_manifest/domain_memory_descriptor_locator",
        "stage_attempt_ref": "/product_entry_manifest/controlled_stage_attempt_projection",
        "consumed_grant_strategy_memory_refs": [
            {
                "stage_id": _require_nonempty_string_from_mapping(
                    stage_ref,
                    "stage_id",
                    context="domain_memory_descriptor_locator.stage_descriptor_refs",
                ),
                "stage_descriptor_ref": _require_nonempty_string_from_mapping(
                    stage_ref,
                    "ref",
                    context="domain_memory_descriptor_locator.stage_descriptor_refs",
                ),
                "accepted_memory_ref_template": accepted_template,
                "consumption_policy": "stage_context_ref_only_no_memory_body_in_repo",
            }
            for stage_ref in stage_refs
        ],
        "writeback_proposal_projection": {
            "surface_kind": proposal_generator["surface_kind"],
            "generator_id": proposal_generator["generator_id"],
            "command": proposal_generator["command"],
            "output_surface_kind": proposal_generator["output_surface_kind"],
            "write_policy": proposal_generator["write_policy"],
            "proposal_ref_template": _require_nonempty_string_from_mapping(
                memory_locator,
                "writeback_proposal_ref_template",
                context="domain_memory_descriptor_locator.memory_locator",
            ),
        },
        "accept_reject_decision_projection": {
            "surface_kind": accept_reject_command["surface_kind"],
            "command_id": accept_reject_command["command_id"],
            "command": accept_reject_command["command"],
            "decision_owner": accept_reject_command["decision_owner"],
            "output_surface_kind": accept_reject_command["output_surface_kind"],
            "write_policy": accept_reject_command["write_policy"],
            "requires_mag_decision_before_store_mutation": accept_reject_command[
                "requires_mag_decision_before_store_mutation"
            ],
            "decision_receipt_ref_template": receipt_locator["decision_receipt_ref_template"],
        },
        "runtime_receipt_evidence_projection": {
            "surface_kind": "domain_memory_runtime_receipt_evidence_projection",
            "command_id": "mag.domain_memory.runtime_receipt_evidence.v1",
            "command": (
                "uv run python -m med_autogrant product domain-memory-receipt-evidence "
                "--decision <decision-json> --runtime-root <runtime-state-root> --format json"
            ),
            "output_surface_kind": "mag_domain_memory_runtime_receipt_evidence",
            "write_policy": "runtime_receipt_instance_only_no_repo_write",
            "receipt_locator_ref": "/product_entry_manifest/domain_memory_descriptor_locator/receipt_locator",
            "requires_mag_decision_payload": True,
        },
        "operator_receipt_projection": dict(operator_receipt_projection),
        "writeback_receipt_refs": dict(
            _require_mapping_from_locator(domain_memory_descriptor_locator, "writeback_receipt_refs")
        ),
        "receipt_locator": dict(receipt_locator),
        "controlled_receipt_instances": controlled_receipt_instances,
        "repo_source_layout_audit": _build_repo_source_layout_audit(),
        "repo_payload_policy": {
            "repo_tracked_real_memory_body": False,
            "repo_tracked_real_receipt_instance": False,
            "repo_tracked_real_grant_artifact": False,
            "repo_contains_contracts_locators_and_seed_fixture_only": True,
        },
        "authority_boundary": {
            "domain_memory_owner": TARGET_DOMAIN_ID,
            "decision_owner": TARGET_DOMAIN_ID,
            "opl_role": "consumed_memory_ref_and_receipt_projection_consumer_only",
            "can_write_memory_body": False,
            "can_write_fundability_verdict": False,
            "can_write_authoring_quality_verdict": False,
            "can_write_submission_ready_export_verdict": False,
            "can_write_grant_artifact": False,
            "can_accept_or_reject_memory_writeback": False,
        },
    }


def _require_mapping_from_locator(locator: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = locator.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"domain_memory_descriptor_locator.{key} must be an object.")
    return value


def _build_controlled_receipt_instances(
    *,
    receipt_locator: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_domain_memory_controlled_receipt_instances",
        "version": "v1",
        "fixture_id": "mag.domain_memory.controlled_receipt_instances.v1",
        "state": "runtime_receipt_evidence_path_verified",
        "receipt_locator_ref": "/product_entry_manifest/domain_memory_descriptor_locator/receipt_locator",
        "runtime_receipt_evidence_command_ref": (
            "/product_entry_manifest/controlled_domain_memory_apply_proof/"
            "runtime_receipt_evidence_projection"
        ),
        "accepted_receipt_instance_ref": (
            "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
            "domain-memory/accepted-strategy-context-fixture.json"
        ),
        "rejected_receipt_instance_ref": (
            "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/"
            "domain-memory/rejected-strategy-context-fixture.json"
        ),
        "accepted_receipt": _build_memory_receipt_fixture(
            proposal_id="accepted-strategy-context-fixture",
            decision="accepted",
            receipt_locator=receipt_locator,
        ),
        "rejected_receipt": _build_memory_receipt_fixture(
            proposal_id="rejected-strategy-context-fixture",
            decision="rejected",
            receipt_locator=receipt_locator,
        ),
        "missing_receipt_blocker": {
            "blocker_kind": "domain_memory_owner_receipt_required",
            "blocker_id": "mag_domain_memory_missing_owner_receipt",
            "owner": TARGET_DOMAIN_ID,
            "required_surface": "mag_domain_memory_writeback_decision",
            "required_receipt_locator_ref": (
                "/product_entry_manifest/domain_memory_descriptor_locator/receipt_locator"
            ),
            "opl_can_synthesize_receipt": False,
        },
        "repo_tracked_real_receipt_instance": False,
        "runtime_receipt_instance_writable": True,
        "contains_memory_body": False,
        "contains_grant_artifact_content": False,
        "contains_quality_or_export_verdict": False,
        "opl_consumption_policy": "runtime_receipt_ref_only_no_memory_body",
    }


def _build_memory_receipt_fixture(
    *,
    proposal_id: str,
    decision: str,
    receipt_locator: Mapping[str, Any],
) -> dict[str, Any]:
    decision_ref_template = _require_nonempty_string_from_mapping(
        receipt_locator,
        "decision_receipt_ref_template",
        context="domain_memory_descriptor_locator.receipt_locator",
    )
    return {
        "surface_kind": "mag_domain_memory_writeback_decision",
        "proposal_id": proposal_id,
        "decision": decision,
        "decision_owner": TARGET_DOMAIN_ID,
        "stage_id": "review_and_rebuttal",
        "receipt_ref": decision_ref_template.replace("<proposal_id>", proposal_id),
        "accepted_memory_ref": (
            "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/"
            f"accepted/{proposal_id}.json"
            if decision == "accepted"
            else None
        ),
        "rejected_memory_ref": (
            "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/"
            f"rejected/{proposal_id}.json"
            if decision == "rejected"
            else None
        ),
        "contains_memory_body": False,
        "contains_grant_artifact_content": False,
        "contains_quality_or_export_verdict": False,
        "repo_tracked": False,
    }


def _build_repo_source_layout_audit() -> dict[str, Any]:
    boundary_refs = {
        "agent": [
            "agent/README.md",
            "src/med_autogrant/domain_entry.py",
            "src/med_autogrant/domain_entry_contract.py",
            "src/med_autogrant/stage_control_plane.py",
        ],
        "contracts": [
            "contracts/README.md",
            "contracts/runtime-program/current-program.json",
            "contracts/runtime-program/domain-memory-seed-fixture.json",
            "contracts/runtime-program/opl-family-contract-adoption.json",
            "schemas/v1/product-entry-manifest.schema.json",
        ],
        "runtime": [
            "runtime/README.md",
            "src/med_autogrant/product_entry_parts/domain_memory.py",
            "src/med_autogrant/product_entry_parts/domain_memory_runtime.py",
            "src/med_autogrant/product_entry_parts/functional_closure.py",
            "src/med_autogrant/product_entry_parts/sidecar.py",
        ],
        "docs": [
            "docs/status.md",
            "docs/project.md",
            "docs/invariants.md",
            "docs/references/grant_strategy_memory_policy.md",
            "docs/references/integration/opl-family-contract-adoption.md",
        ],
    }
    repo_root = Path(__file__).resolve().parents[3]
    return {
        "surface_kind": "mag_repo_source_layout_audit",
        "audit_id": "mag.standard_domain_agent_skeleton.repo_source_layout.audit.v1",
        "layout_state": "physical_skeleton_follow_through_landed_minimum_anchors",
        "boundary_keys": list(boundary_refs),
        "physical_move_required": (
            "low_risk_source_moves_only_after_direct_hosted_parity_restore_provenance_and_no_active_caller_proof"
        ),
        "repo_source_policy": "existing_repo_source_mapped_to_standard_agent_contracts_runtime_docs_boundaries",
        "retired_active_path_policy": "physically_removed_or_history_tombstone_only",
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
                "evidence_ref": "docs/decisions.md#2026-05-12-temporal-backed-opl-production-runtime-supersedes-gateway-manager-wording",
            },
            {
                "path_family": "repo-local host-agent runtime as product owner",
                "state": "physically_removed_from_active_source",
                "evidence_ref": "docs/status.md#旧面退役校准",
            },
        ],
        "forbidden_active_path_residue": [],
        "source_ref_status": [
            {
                "boundary": boundary,
                "path": path,
                "exists": (repo_root / path).exists(),
                "repo_source_role": _repo_source_role(boundary),
            }
            for boundary, paths in boundary_refs.items()
            for path in paths
        ],
    }


def _repo_source_role(boundary: str) -> str:
    return {
        "agent": "domain_entry_stage_pack_and_quality_gate_source",
        "contracts": "machine_readable_contract_schema_and_seed_fixture_source",
        "runtime": "sidecar_projection_and_memory_apply_contract_source",
        "docs": "human_policy_status_and_opl_adoption_source",
    }[boundary]
