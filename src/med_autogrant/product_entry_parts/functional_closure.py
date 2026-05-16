from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.stage_control_plane import build_mag_grant_transition_oracle
from med_autogrant.product_entry_parts import domain_agent_skeleton
from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _optional_string_from_mapping,
    _require_nonempty_string_from_mapping,
)

_ACTIVE_PATH_SCAN_ROOTS = ("src", "tests", "schemas", "contracts", "scripts", "plugins")
_ACTIVE_PATH_SCAN_FILES = ("Makefile", "pyproject.toml", ".agents/plugins/marketplace.json")
_ACTIVE_PATH_SCAN_SUFFIXES = {".py", ".json", ".toml", ".sh", ".yaml", ".yml"}
_RETIRED_ACTIVE_PATHS = (
    "tests/test_product_entry.py",
    "src/med_autogrant/domain_runtime_parts/patch_targets.py",
    "src/med_autogrant/gateway.py",
    "src/med_autogrant/local_manager.py",
    "src/med_autogrant/" + "host" + "_agent.py",
)
MAG_THIN_SURFACE_OUTPUT_CLASSES = (
    "grant_owned_refs",
    "owner_receipt",
    "typed_blocker",
    "verdict_refs",
    "domain_action_metadata",
)
FORBIDDEN_MAG_GENERIC_OWNER_ROLES = (
    "generic_scheduler_owner",
    "generic_daemon_owner",
    "generic_lifecycle_owner",
    "generic_queue_owner",
    "generic_attempt_ledger_owner",
    "generic_state_machine_runner_owner",
    "generic_workbench_owner",
    "generic_memory_transport_owner",
    "generic_artifact_lifecycle_owner",
)
_FORBIDDEN_DEFAULT_CALLER_PATTERNS = (
    {
        "pattern_id": "domain_runtime_patch_bridge_import",
        "literal_parts": ("med_autogrant.domain_runtime_parts", ".patch_targets"),
        "policy": "patch runtime owner modules directly; do not use retired facade patch bridge",
    },
    {
        "pattern_id": "hermes_default_runtime_owner",
        "literal_parts": ("DEFAULT_RUNTIME_OWNER = \"", "hermes_agent", "\""),
        "policy": "Hermes-Agent remains explicit proof/provider provenance only",
    },
    {
        "pattern_id": "hermes_default_executor_owner",
        "literal_parts": ("DEFAULT_EXECUTOR_OWNER = \"", "hermes_agent", "\""),
        "policy": "default executor stays Codex CLI",
    },
    {
        "pattern_id": "claude_default_executor_owner",
        "literal_parts": ("DEFAULT_EXECUTOR_OWNER = \"", "claude_code", "\""),
        "policy": "non-default executors require explicit OPL adapter selection",
    },
    {
        "pattern_id": "gateway_default_runtime_owner",
        "literal_parts": ("DEFAULT_RUNTIME_OWNER = \"", "gateway", "\""),
        "policy": "Gateway/local-manager wording is retired from active runtime ownership",
    },
    {
        "pattern_id": "local_manager_default_runtime_owner",
        "literal_parts": ("DEFAULT_RUNTIME_OWNER = \"", "local_manager", "\""),
        "policy": "local-manager is not a default product/runtime owner",
    },
    {
        "pattern_id": "host" + "_agent_default_runtime_owner",
        "literal_parts": ("DEFAULT_RUNTIME_OWNER = \"", "host" + "_agent", "\""),
        "policy": "repo-local host-agent runtime is not a product owner",
    },
    {
        "pattern_id": "json_hermes_default_executor",
        "literal_parts": ("\"default_executor_name\": \"", "hermes_agent", "\""),
        "policy": "manifest/contracts must keep Codex CLI as default executor",
    },
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
    physical_skeleton_follow_through = build_physical_skeleton_follow_through()
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
        "physical_skeleton_follow_through": physical_skeleton_follow_through,
        "mag_consumer_thinning_contract": build_mag_consumer_thinning_contract(
            physical_skeleton_follow_through=physical_skeleton_follow_through,
        ),
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
    active_path_scan = _build_active_path_scan_no_legacy_default_caller(repo_root)
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
        "active_path_scan_no_legacy_default_caller_ref": (
            "/product_entry_manifest/physical_skeleton_follow_through/"
            "active_path_scan_no_legacy_default_caller"
        ),
        "active_path_scan_no_legacy_default_caller": active_path_scan,
        "first_follow_through_scope": [
            "manifest exposes root anchors",
            "repo-source layout audit requires root anchors to exist",
            "workspace artifacts and runtime receipts stay outside repo source",
            "active-path scan proves retired default callers are not used by machine surfaces",
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


def build_mag_consumer_thinning_contract(
    *,
    physical_skeleton_follow_through: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    active_path_scan = {}
    if physical_skeleton_follow_through is not None:
        candidate = physical_skeleton_follow_through.get("active_path_scan_no_legacy_default_caller")
        if isinstance(candidate, Mapping):
            active_path_scan = dict(candidate)
    return {
        "surface_kind": "mag_consumer_thinning_contract",
        "version": "v1",
        "contract_id": "mag.consumer_thinning.contract.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "adapter_role": "domain_authority_pack_with_thin_program_surface",
        "state": "handoff_ready_external_opl_replacement_gated",
        "consumes_opl_family_primitive": "family_scheduler_replacement",
        "claims_opl_replacement_exists": False,
        "claims_production_long_run_soak_complete": False,
        "sidecar_contract_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
        "consumed_opl_standard_surfaces": _build_consumed_opl_standard_surfaces(),
        "allowed_return_shapes": [
            "domain_owner_receipt",
            "typed_blocker",
            "no_regression_evidence",
        ],
        "mag_owned_outputs": list(MAG_THIN_SURFACE_OUTPUT_CLASSES),
        "thin_surface_output_guard": _build_thin_surface_output_guard(),
        "standard_agent_scaffold_alignment": _build_standard_agent_scaffold_alignment(),
        "exposed_sidecar_return_refs": {
            "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
            "controlled_stage_attempt_projection_ref": (
                "/product_entry_manifest/controlled_stage_attempt_projection"
            ),
            "controlled_domain_memory_apply_proof_ref": (
                "/product_entry_manifest/controlled_domain_memory_apply_proof"
            ),
            "lifecycle_guarded_apply_proof_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
            "grant_transition_oracle_ref": "/product_entry_manifest/grant_transition_oracle",
        },
        "verdict_authority_refs": {
            "fundability_verdict_owner": TARGET_DOMAIN_ID,
            "quality_verdict_owner": TARGET_DOMAIN_ID,
            "export_verdict_owner": TARGET_DOMAIN_ID,
            "submission_ready_gate_ref": "package submission-ready",
        },
        "domain_action_metadata_refs": [
            "/product_entry_manifest/family_action_catalog",
            "/product_entry_manifest/family_stage_control_plane",
            "/product_entry_manifest/grant_transition_oracle",
        ],
        "opl_replacement_expectations": [
            _build_opl_replacement_expectation(
                "workspace_source_intake_shell",
                mag_keeps=["funding_call_profile_task_lock_adapter", "domain_blocker", "owner_receipt"],
                opl_provides=["workspace_locator", "source_receipt", "freshness", "repair_command"],
            ),
            _build_opl_replacement_expectation(
                "memory_locator_writeback_transport",
                mag_keeps=["strategy_memory_policy", "writeback_proposal", "accept_reject", "receipt_writer"],
                opl_provides=["body_free_locator", "index", "freshness", "receipt_ref_projection"],
            ),
            _build_opl_replacement_expectation(
                "package_export_lifecycle_shell",
                mag_keeps=["package_refs", "gap_report", "submission_ready_verdict", "manual_portal_boundary"],
                opl_provides=["package_lifecycle_shell", "restore_provenance", "retention", "artifact_index"],
            ),
            _build_opl_replacement_expectation(
                "generic_transition_runner",
                mag_keeps=["grant_transition_oracle", "stage_guard", "typed_blocker", "owner_action_metadata"],
                opl_provides=["matrix_runner", "retry_dead_letter", "dispatch_receipt", "transition_audit"],
            ),
            _build_opl_replacement_expectation(
                "operator_workbench_observability_slo",
                mag_keeps=["quality_verdict_refs", "hard_blockers", "safe_action_refs"],
                opl_provides=["workbench_panel", "attention_queue", "repair_command_projection", "slo"],
            ),
            _build_opl_replacement_expectation(
                "agent_scaffold_checklist",
                mag_keeps=["grant_domain_authority_pack", "receipt_schema_examples", "docs_taxonomy_example"],
                opl_provides=["new_agent_template", "owner_boundary_checklist", "no_forbidden_write_rule"],
            ),
        ],
        "forbidden_mag_owned_generic_primitives": [],
        "forbidden_mag_generic_owner_roles": list(FORBIDDEN_MAG_GENERIC_OWNER_ROLES),
        "guarded_by_active_path_scan_ref": (
            "/product_entry_manifest/physical_skeleton_follow_through/"
            "active_path_scan_no_legacy_default_caller"
        ),
        "active_path_scan_state": active_path_scan.get("state", "not_available"),
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "memory_body_owner": TARGET_DOMAIN_ID,
            "grant_truth_owner": TARGET_DOMAIN_ID,
            "grant_memory_body_owner": TARGET_DOMAIN_ID,
            "quality_verdict_owner": TARGET_DOMAIN_ID,
            "export_authority_owner": TARGET_DOMAIN_ID,
            "safe_action_refs_owner": TARGET_DOMAIN_ID,
            "package_authority_owner": TARGET_DOMAIN_ID,
            "owner_receipt_authority": TARGET_DOMAIN_ID,
            "opl_family_scheduler_replacement_owner": "one-person-lab",
            "opl_role": "replacement_owner_and_ref_consumer_only",
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_export_ready": False,
            "opl_can_mutate_grant_artifacts": False,
            "mag_rebuilds_opl_runtime": False,
            "mag_implements_generic_scheduler": False,
            "mag_implements_generic_daemon": False,
            "mag_implements_generic_lifecycle_owner": False,
            "mag_implements_generic_queue": False,
            "mag_implements_generic_attempt_ledger": False,
            "mag_implements_generic_runner": False,
            "mag_implements_app_workbench": False,
            "mag_implements_generic_memory_transport": False,
            "mag_implements_generic_artifact_lifecycle": False,
        },
    }


def _build_consumed_opl_standard_surfaces() -> dict[str, Any]:
    return {
        "surface_kind": "mag_consumed_opl_standard_surfaces",
        "standard_scaffold_manifest_ref": "/product_entry_manifest/standard_domain_agent_skeleton",
        "generic_primitives_contract_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/opl_replacement_expectations"
        ),
        "sidecar_projection_ref": "/sidecar_export/mag_consumer_thinning_contract",
        "consumption_policy": (
            "consume_opl_standard_scaffold_and_generic_primitives_no_mag_runtime_rebuild"
        ),
        "consumed_generic_primitives": [
            "workspace_source_intake_shell",
            "memory_locator_writeback_transport",
            "package_export_lifecycle_shell",
            "generic_transition_runner",
            "operator_workbench_observability_slo",
            "agent_scaffold_checklist",
        ],
        "mag_retained_authority": [
            "grant_truth",
            "fundability_verdict",
            "quality_verdict",
            "export_verdict",
            "memory_body_accept_reject",
            "package_authority",
            "owner_receipt",
        ],
        "authority_boundary": {
            "opl_standard_scaffold_owner": "one-person-lab",
            "opl_generic_primitives_owner": "one-person-lab",
            "mag_consumes_standard_scaffold": True,
            "mag_consumes_generic_primitives": True,
            "mag_can_own_generic_scheduler": False,
            "mag_can_own_generic_daemon": False,
            "mag_can_own_generic_queue": False,
            "mag_can_own_generic_attempt_ledger": False,
            "mag_can_own_generic_runner": False,
            "mag_can_own_generic_workbench": False,
            "mag_can_own_generic_memory_transport": False,
            "mag_can_own_generic_artifact_lifecycle": False,
        },
    }


def _build_thin_surface_output_guard() -> dict[str, Any]:
    return {
        "surface_kind": "mag_thin_surface_output_guard",
        "guard_id": "mag.thin_surface.output_guard.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "output_policy": "grant_refs_and_receipts_only_no_generic_runtime_state",
        "allowed_output_classes": list(MAG_THIN_SURFACE_OUTPUT_CLASSES),
        "required_sidecar_return_refs": {
            "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
            "controlled_stage_attempt_projection_ref": "/product_entry_manifest/controlled_stage_attempt_projection",
            "controlled_domain_memory_apply_proof_ref": "/product_entry_manifest/controlled_domain_memory_apply_proof",
            "lifecycle_guarded_apply_proof_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
            "grant_transition_oracle_ref": "/product_entry_manifest/grant_transition_oracle",
        },
        "forbidden_output_classes": [
            "generic_scheduler_state",
            "generic_daemon_state",
            "generic_lifecycle_ledger",
            "generic_queue_record",
            "generic_attempt_ledger_record",
            "generic_runner_decision",
            "generic_workbench_state",
            "generic_memory_transport_state",
            "generic_artifact_lifecycle_state",
            "grant_artifact_content",
            "memory_body",
        ],
        "consumes_opl_replacement_expectations": True,
        "replacement_expectations_ref": "/product_entry_manifest/mag_consumer_thinning_contract/opl_replacement_expectations",
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "owner_receipt_authority": TARGET_DOMAIN_ID,
            "opl_role": "replacement_owner_and_ref_consumer_only",
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_export_ready": False,
            "mag_can_emit_generic_runtime_state": False,
            "mag_can_emit_generic_workbench_state": False,
        },
    }


def _build_standard_agent_scaffold_alignment() -> dict[str, Any]:
    return {
        "surface_kind": "mag_standard_agent_scaffold_thin_surface_guard",
        "guard_id": "mag.standard_agent_scaffold.thin_surface_guard.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "scaffold_ref": "/product_entry_manifest/standard_domain_agent_skeleton",
        "physical_follow_through_ref": "/product_entry_manifest/physical_skeleton_follow_through",
        "output_guard_ref": "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard",
        "forbidden_owner_roles_ref": "/product_entry_manifest/mag_consumer_thinning_contract/forbidden_mag_generic_owner_roles",
        "knowledge_only_repository": False,
        "retains_domain_program_surfaces": True,
        "required_repo_boundaries": ["agent", "contracts", "runtime", "docs"],
        "retained_program_surface_refs": [
            "src/med_autogrant/domain_entry.py",
            "src/med_autogrant/product_entry.py",
            "src/med_autogrant/product_entry_parts/sidecar.py",
            "schemas/v1/product-entry-manifest.schema.json",
            "tests/product_entry_cases/test_sidecar.py",
            "tests/product_entry_cases/test_functional_closure.py",
        ],
        "retained_program_surface_kinds": [
            "domain_entry",
            "product_entry_manifest_builder",
            "product_sidecar_adapter",
            "schema_contract",
            "focused_product_entry_tests",
        ],
        "authority_boundary": {
            "domain_truth_owner": TARGET_DOMAIN_ID,
            "domain_entry_owner": TARGET_DOMAIN_ID,
            "sidecar_owner": TARGET_DOMAIN_ID,
            "schema_owner": TARGET_DOMAIN_ID,
            "test_owner": TARGET_DOMAIN_ID,
            "opl_scaffold_owner": "one-person-lab",
            "mag_owns_generic_scaffold_template": False,
            "mag_owns_generic_runtime_framework": False,
            "mag_is_knowledge_only_repository": False,
        },
    }


def _build_opl_replacement_expectation(
    primitive_id: str,
    *,
    mag_keeps: list[str],
    opl_provides: list[str],
) -> dict[str, Any]:
    return {
        "primitive_id": primitive_id,
        "owner": "one-person-lab",
        "state": "external_replacement_contract_expected",
        "mag_handoff_policy": "contract_expectation_only",
        "implemented_in_mag": False,
        "mag_keeps": mag_keeps,
        "opl_provides": opl_provides,
        "authority_boundary": {
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_declare_export_ready": False,
        },
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
        "consumer_thinning_contract_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
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
        "mag_owned_transition_oracle": build_mag_grant_transition_oracle(
            family_stage_control_plane=_minimal_family_stage_control_plane_for_transition_oracle(),
            family_action_catalog=_minimal_family_action_catalog_for_transition_oracle(),
        ),
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
            "active_path_scan_no_legacy_default_caller_ref": (
                "/product_entry_manifest/physical_skeleton_follow_through/"
                "active_path_scan_no_legacy_default_caller"
            ),
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
                title="OPL generic primitive absorption design and MAG adapter thinning",
                state="mag_adapter_thinning_contract_landed_external_opl_replacement_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/mag_consumer_thinning_contract",
                    "/product_entry_manifest/ideal_state_closure_status",
                    "/product_entry_manifest/owner_receipt_contract",
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                    "/product_entry_manifest/grant_transition_oracle",
                    "product sidecar export",
                ],
                required_evidence_refs=[
                    "mag_consumer_thinning_contract_ref",
                    "sidecar_refs_only_projection_ref",
                    "opl_generic_primitive_replacement_contract_ref",
                ],
            ),
            _build_ideal_state_phase_status(
                phase_id="P2",
                title="package export and artifact lifecycle shell handoff",
                state="external_opl_package_lifecycle_shell_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                    "/product_entry_manifest/artifact_locator_contract",
                    "package submission-ready",
                    "product lifecycle-receipt-evidence",
                    "product sidecar-dispatch lifecycle/receipt",
                    "/product_entry_manifest/mag_consumer_thinning_contract",
                ],
                required_evidence_refs=[
                    "opl_package_export_lifecycle_shell_ref",
                    "mag_runtime_lifecycle_cleanup_receipt_ref",
                    "mag_runtime_lifecycle_restore_receipt_ref",
                    "mag_runtime_lifecycle_retention_receipt_ref",
                ],
            ),
            _build_ideal_state_phase_status(
                phase_id="P3",
                title="grant strategy memory locator/writeback handoff",
                state="runtime_workspace_evidence_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/domain_memory_descriptor_locator",
                    "/product_entry_manifest/controlled_domain_memory_apply_proof",
                    "product domain-memory-proposal",
                    "product domain-memory-decision",
                    "product domain-memory-receipt-evidence",
                    "/product_entry_manifest/mag_consumer_thinning_contract",
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
                title="physical skeleton template extraction and legacy direct retirement",
                state="landed_with_external_scaffold_template_handoff_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/standard_domain_agent_skeleton",
                    "/product_entry_manifest/physical_skeleton_follow_through",
                    (
                        "/product_entry_manifest/physical_skeleton_follow_through/"
                        "active_path_scan_no_legacy_default_caller"
                    ),
                    "/product_entry_manifest/controlled_domain_memory_apply_proof/repo_source_layout_audit",
                    "/product_entry_manifest/mag_consumer_thinning_contract",
                    "docs/status.md#旧面退役校准",
                ],
                required_evidence_refs=[
                    "opl_agent_scaffold_checklist_ref",
                    "opl_agents_list_mag_descriptor_no_drift_ref",
                    "active_path_scan_no_legacy_default_caller_ref",
                ],
            ),
            _build_ideal_state_phase_status(
                phase_id="P5",
                title="focused OPL-hosted receipt verification",
                state="external_evidence_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/controlled_stage_attempt_projection",
                    "/product_entry_manifest/owner_receipt_contract",
                    "/product_entry_manifest/controlled_soak_no_regression_attempt",
                    "/product_entry_manifest/mag_consumer_thinning_contract",
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
                phase_id="P6",
                title="live soak and production closure",
                state="production_soak_gate",
                mag_surface_refs=[
                    "/product_entry_manifest/controlled_stage_attempt_projection",
                    "/product_entry_manifest/owner_receipt_contract",
                    "/product_entry_manifest/controlled_soak_no_regression_attempt",
                    "/product_entry_manifest/mag_consumer_thinning_contract",
                    "product controlled-soak-receipt-reconciliation-proof",
                    "product controlled-soak-receipt-reconciliation-inventory",
                ],
                required_evidence_refs=[
                    "long_run_soak_opl_provider_receipt_ref",
                    "long_run_soak_mag_owner_receipt_or_typed_blocker_ref",
                    "long_run_soak_no_forbidden_write_proof_ref",
                    "app_operator_drilldown_refs_only_ref",
                ],
            ),
        ],
    }


def _build_active_path_scan_no_legacy_default_caller(repo_root: Path) -> dict[str, Any]:
    scanned_paths = _active_path_scan_paths(repo_root)
    forbidden_patterns = [
        {
            "pattern_id": str(pattern["pattern_id"]),
            "literal": "".join(pattern["literal_parts"]),
            "policy": str(pattern["policy"]),
        }
        for pattern in _FORBIDDEN_DEFAULT_CALLER_PATTERNS
    ]
    matches: list[dict[str, Any]] = []
    for path in scanned_paths:
        text = _read_scan_text(path)
        if text is None:
            continue
        relative_path = path.relative_to(repo_root).as_posix()
        for pattern in forbidden_patterns:
            literal = pattern["literal"]
            if literal in text:
                matches.append(
                    {
                        "path": relative_path,
                        "pattern_id": pattern["pattern_id"],
                        "literal": literal,
                    }
                )
    retired_surface_path_status = [
        {
            "path": path,
            "exists": (repo_root / path).exists(),
            "state": "absent" if not (repo_root / path).exists() else "present_forbidden",
        }
        for path in _RETIRED_ACTIVE_PATHS
    ]
    retired_surface_path_matches = [
        status for status in retired_surface_path_status if status["state"] != "absent"
    ]
    return {
        "surface_kind": "mag_active_path_scan_no_legacy_default_caller",
        "version": "v1",
        "scan_id": "mag.active_path_scan.no_legacy_default_caller.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "state": "passed" if not matches and not retired_surface_path_matches else "failed",
        "evidence_ref_id": "active_path_scan_no_legacy_default_caller_ref",
        "no_legacy_default_caller": not matches and not retired_surface_path_matches,
        "scanned_scope": {
            "roots": list(_ACTIVE_PATH_SCAN_ROOTS),
            "files": list(_ACTIVE_PATH_SCAN_FILES),
            "suffixes": sorted(_ACTIVE_PATH_SCAN_SUFFIXES),
            "excludes_human_docs": True,
            "human_doc_policy": "docs/history/provenance may name retired surfaces without making them default callers",
            "scans_repo_source_only": True,
        },
        "scanned_file_count": len(scanned_paths),
        "scanned_sample_refs": [
            path.relative_to(repo_root).as_posix()
            for path in scanned_paths[:12]
        ],
        "forbidden_default_caller_patterns": forbidden_patterns,
        "forbidden_default_caller_matches": matches,
        "retired_surface_path_status": retired_surface_path_status,
        "claims_production_long_run_soak_complete": False,
        "authority_boundary": {
            "proves_repo_local_active_machine_surface_only": True,
            "proves_opl_hosted_production_soak": False,
            "proves_grant_quality_or_export_readiness": False,
            "opl_can_write_domain_truth": False,
            "opl_can_declare_export_ready": False,
        },
    }


def _active_path_scan_paths(repo_root: Path) -> list[Path]:
    paths: set[Path] = set()
    for root_name in _ACTIVE_PATH_SCAN_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in _ACTIVE_PATH_SCAN_SUFFIXES:
                paths.add(path)
    for file_name in _ACTIVE_PATH_SCAN_FILES:
        path = repo_root / file_name
        if path.is_file():
            paths.add(path)
    return sorted(paths, key=lambda path: path.relative_to(repo_root).as_posix())


def _read_scan_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def _minimal_family_stage_control_plane_for_transition_oracle() -> dict[str, Any]:
    return {
        "stages": [
            {"stage_id": "call_and_candidate_intake"},
            {"stage_id": "fundability_strategy"},
            {"stage_id": "specific_aims_and_structure"},
            {"stage_id": "proposal_authoring"},
            {"stage_id": "review_and_rebuttal"},
            {"stage_id": "package_and_submit_ready"},
        ]
    }


def _minimal_family_action_catalog_for_transition_oracle() -> dict[str, Any]:
    return {
        "actions": [
            {"action_id": "open_grant_user_loop"},
            {"action_id": "build_submission_ready_package"},
        ]
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
