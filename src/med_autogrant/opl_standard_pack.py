from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.action_catalog import build_mag_family_action_catalog
from med_autogrant.product_entry_parts.consumer_thinning import build_mag_consumer_thinning_contract
from med_autogrant.product_entry_parts.consumer_thinning_pack import (
    build_mag_minimal_authority_surface_taxonomy,
)
from med_autogrant.product_entry_parts.functional_closure import build_physical_skeleton_follow_through
from med_autogrant.opl_standard_pack_constants import DOMAIN_LABEL, GENERATED_SURFACE_OWNER
from med_autogrant.product_entry_parts.primitives import (
    GRANT_COCKPIT_KIND,
    GRANT_DIRECT_ENTRY_KIND,
    GRANT_PROGRESS_PROJECTION_KIND,
    GRANT_USER_LOOP_KIND,
    PRODUCT_STATUS_KIND,
    TARGET_DOMAIN_ID,
)
from med_autogrant.opl_standard_pack_handoff_refs import (
    build_agent_lab_handoff,
    build_oma_handoff_refs,
)
from med_autogrant.opl_standard_pack_private_policy import (
    build_private_functional_surface_policy,
)
from med_autogrant.opl_standard_pack_profiles import (
    AGENT_MEMBERSHIP_PROJECTION_POLICY,
    DOMAIN_SPECIFIC_PROFILE,
    SERIES_DESIGN_PROFILE,
    SHARED_POLICY_RELEASE,
    STANDARD_PUBLIC_PROJECTION_POLICY,
    WORKSPACE_TOPOLOGY_PROFILE,
)
from med_autogrant.opl_standard_pack_source_policy import (
    ACTIVE_PATH_SCAN_POLICY,
    ACTIVE_CALLER_STATUS_BY_PHYSICAL_CLASSIFICATION,
    DECLARATIVE_DOMAIN_PACK,
    FORBIDDEN_GENERIC_OWNER_ROLES,
    FORBIDDEN_PHYSICAL_RESIDUE_CLASSES,
    GENERATED_SURFACES,
    MINIMAL_AUTHORITY_FUNCTIONS,
    PHYSICAL_SOURCE_CLASSIFICATION_BUCKETS,
    PHYSICAL_SOURCE_SURFACE_CLASSIFICATIONS,
    REQUIRED_DOMAIN_PACK_PATHS,
    RETIREMENT_EVIDENCE_REFS,
    TARGET_OWNER_BY_PHYSICAL_CLASSIFICATION,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.stage_control_plane import build_mag_family_stage_control_plane
from med_autogrant.stage_control_plane_parts.cognitive_kernel import (
    pack_compiler_cognitive_kernel_fields,
)
from opl_harness_shared.product_entry_companions import build_operator_loop_action_catalog


REPO_ROOT = Path(__file__).resolve().parents[2]
INPUT_PLACEHOLDER = "<input_path>"
TASK_INTENT_PLACEHOLDER = "<task_intent>"
OUTPUT_DIR_PLACEHOLDER = "<output_dir>"


def _json_ready(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def build_standard_pack() -> dict[str, Any]:
    action_catalog = build_mag_family_action_catalog(
        action_commands=_base_operator_loop_actions(),
    )
    stage_control_plane = build_mag_family_stage_control_plane(
        family_action_catalog=action_catalog,
    )
    physical_skeleton_follow_through = build_physical_skeleton_follow_through(
        active_path_scan_policy=ACTIVE_PATH_SCAN_POLICY,
    )
    consumer_thinning_contract = build_mag_consumer_thinning_contract(
        physical_skeleton_follow_through=physical_skeleton_follow_through,
    )

    agent_lab_handoff = _agent_lab_handoff()
    return {
        "domain_descriptor": _domain_descriptor(),
        "pack_compiler_input": _pack_compiler_input(
            consumer_thinning_contract["minimal_authority_functions"]
        ),
        "generated_surface_handoff": _generated_surface_handoff(),
        "foundry_agent_series": _foundry_agent_series_contract(stage_control_plane),
        "action_catalog": _with_forbidden_roles(action_catalog),
        "stage_control_plane": stage_control_plane,
        "memory_descriptor": _memory_descriptor(),
        "artifact_locator_contract": _artifact_locator_contract(),
        "owner_receipt_contract": _owner_receipt_contract(),
        "agent_lab_handoff": agent_lab_handoff,
        "oma_handoff_refs": _oma_handoff_refs(agent_lab_handoff=agent_lab_handoff),
        "functional_privatization_audit": _functional_privatization_audit(consumer_thinning_contract),
        "private_functional_surface_policy": _private_functional_surface_policy(),
    }


def sync_standard_pack(*, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    contracts = build_standard_pack()
    contract_dir = repo_root / "contracts"
    contract_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for name, payload in contracts.items():
        relative = Path("contracts") / f"{name}.json"
        path = repo_root / relative
        path.write_text(
            json.dumps(_json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(str(relative))
    return {
        "surface_kind": "mag_opl_standard_pack_sync",
        "target_domain_id": TARGET_DOMAIN_ID,
        "written": written,
    }


def _base_operator_loop_actions() -> dict[str, Mapping[str, Any]]:
    command_catalog = {
        "grant_progress": public_cli_command(
            "grant-progress",
            "--input",
            INPUT_PLACEHOLDER,
            "--format",
            "json",
        ),
        "build_submission_ready_package": public_cli_command(
            "build-submission-ready-package",
            "--input",
            INPUT_PLACEHOLDER,
            "--output-dir",
            OUTPUT_DIR_PLACEHOLDER,
            "--format",
            "json",
        ),
    }
    return build_operator_loop_action_catalog(
        {
            "open_loop": {
                "command": public_cli_command(
                    "grant-user-loop",
                    "--input",
                    INPUT_PLACEHOLDER,
                    "--task-intent",
                    TASK_INTENT_PLACEHOLDER,
                    "--format",
                    "json",
                ),
                "surface_kind": GRANT_USER_LOOP_KIND,
                "summary": "Open the MAG grant user loop through the existing domain action target.",
                "requires": ["input_path", "task_intent"],
            },
            "inspect_progress": {
                "command": command_catalog["grant_progress"],
                "surface_kind": GRANT_PROGRESS_PROJECTION_KIND,
                "summary": "Read MAG grant progress through the existing domain action target.",
                "requires": ["input_path"],
            },
            "inspect_cockpit": {
                "command": public_cli_command(
                    "grant-cockpit",
                    "--input",
                    INPUT_PLACEHOLDER,
                    "--format",
                    "json",
                ),
                "surface_kind": GRANT_COCKPIT_KIND,
                "summary": "Read the MAG cockpit projection through the existing domain action target.",
                "requires": ["input_path"],
            },
            "build_direct_entry": {
                "command": public_cli_command(
                    "grant-direct-entry",
                    "--input",
                    INPUT_PLACEHOLDER,
                    "--task-intent",
                    TASK_INTENT_PLACEHOLDER,
                    "--format",
                    "json",
                ),
                "surface_kind": GRANT_DIRECT_ENTRY_KIND,
                "summary": "Build a MAG direct-entry contract through the existing domain action target.",
                "requires": ["input_path", "task_intent"],
            },
            "build_submission_ready_package": {
                "command": command_catalog["build_submission_ready_package"],
                "surface_kind": "submission_ready_package",
                "summary": "Run the MAG submission-ready package gate through the existing domain action target.",
                "requires": ["input_path", "output_dir"],
            },
        }
    )


def _domain_descriptor() -> dict[str, Any]:
    return {
        "surface_kind": "domain_agent_descriptor",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "domain_label": DOMAIN_LABEL,
        "package_role": "opl_standard_domain_agent",
        "generated_surface_owner": GENERATED_SURFACE_OWNER,
        "domain_repo_can_own_generated_surface": False,
        "standard_contract_refs": {
            "action_catalog": "contracts/action_catalog.json",
            "foundry_agent_series": "contracts/foundry_agent_series.json",
            "foundry_agent_series_policy_release": (
                "contracts/opl-framework/foundry-agent-series-policy-release.json"
            ),
            "stage_control_plane": "contracts/stage_control_plane.json",
            "pack_compiler_input": "contracts/pack_compiler_input.json",
            "generated_surface_handoff": "contracts/generated_surface_handoff.json",
            "agent_lab_handoff": "contracts/agent_lab_handoff.json",
            "oma_handoff_refs": "contracts/oma_handoff_refs.json",
            "functional_privatization_audit": "contracts/functional_privatization_audit.json",
        },
        "authority_boundary": {
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_authorize_quality_or_export": False,
            "domain_owns_truth_quality_artifact_memory_and_receipts": True,
            "domain_truth_owner": TARGET_DOMAIN_ID,
        },
    }


def _foundry_agent_series_contract(stage_control_plane: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "surface_kind": "opl_foundry_agent_series_contract",
        "version": "foundry-agent-series.v1",
        "owner": "one-person-lab",
        "product_layer": "foundry_agent",
        "product_model": "OPL Framework -> One Person Lab App -> Foundry Agents",
        "standard_agent_requirement": (
            "foundry_agents_share_identity_stage_authority_progress_currentness_closeout_"
            "and_app_projection_packets"
        ),
        "contract_version_policy": {
            "current_version": "foundry-agent-series.v1",
            "domain_contract_ref": "contracts/foundry_agent_series.json",
            "exact_version_pin_required": True,
            "compatible_version_range": ["foundry-agent-series.v1"],
            "breaking_change_requires_new_version": True,
            "domain_descriptor_must_reference_domain_contract": True,
        },
        "shared_release_pin_strategy": {
            "owner_release_contract_ref": "contracts/family-release/shared-owner-release.json",
            "owner_commit_pin_required": True,
            "domain_dependency_pin_required": True,
            "supported_pin_sources": [
                "pyproject.toml",
                "uv.lock",
                "package.json",
                "package-lock.json",
            ],
            "consumer_alignment_check": "family:shared-release",
            "domain_contract_version_pin_does_not_authorize_domain_truth": True,
        },
        "shared_policy_release": SHARED_POLICY_RELEASE,
        "agent_membership_projection_policy": AGENT_MEMBERSHIP_PROJECTION_POLICY,
        "standard_public_projection_policy": STANDARD_PUBLIC_PROJECTION_POLICY,
        "series_design_profile": SERIES_DESIGN_PROFILE,
        "domain_specific_profile": DOMAIN_SPECIFIC_PROFILE,
        "workspace_topology_profile": WORKSPACE_TOPOLOGY_PROFILE,
        "domain_id": "medautogrant",
        "foundry_agent_id": "medautogrant",
        "domain_label": "Grant Foundry",
        "domain_aliases": [TARGET_DOMAIN_ID],
        "authority_owner": stage_control_plane["owner"],
        "stage_control_plane_ref": "contracts/stage_control_plane.json",
        "stage_control_plane_target_domain_id": stage_control_plane["target_domain_id"],
        "app_projection_ref": "contracts/generated_surface_handoff.json#/product_entry",
        "required_identity_fields": [
            "domain_id",
            "foundry_agent_id",
            "product_layer",
            "domain_label",
            "authority_owner",
            "stage_control_plane_ref",
        ],
        "required_stage_packets": [
            "user_stage_log_contract",
            "progress_delta_policy",
            "typed_blocker_lineage_policy",
            "stage_completion_policy",
            "effective_current_context",
            "owner_receipt_or_typed_blocker_closeout",
        ],
        "shared_progress_projection_fields": [
            "progress_delta_classification",
            "deliverable_progress_delta",
            "platform_repair_delta",
            "next_forced_delta",
        ],
        "domain_progress_aliases": {
            "deliverable": ["grant_work_progress"],
            "platform": ["platform_evidence_progress", "platform_repair_delta"],
        },
        "domain_adapter_policy": {
            "domain_specific_aliases_only": True,
            "no_parallel_progress_schema": True,
            "no_parallel_blocker_lineage_schema": True,
            "no_domain_runtime_fork": True,
        },
        "purpose_first_adapter_thinning_policy": {
            "policy_id": "mag.purpose_first_adapter_thinning.v1",
            "default_retained_surface_roles": [
                "refs_only_adapter",
                "domain_handler_target",
                "minimal_authority_function",
                "migration_input",
                "history_or_tombstone_provenance",
            ],
            "default_operator_delta_shape": (
                "grant_deliverable_progress_delta_or_mag_owned_typed_blocker"
            ),
            "physical_delete_required_gates": [
                "replacement_parity",
                "no_active_caller",
                "owner_receipt_or_typed_blocker",
                "no_forbidden_write",
                "tombstone_or_provenance",
            ],
            "evidence_tail_boundary": {
                "structural_conformance_is_domain_ready": False,
                "provider_completion_is_submission_ready": False,
                "grouped_cli_success_is_grant_ready": False,
                "generated_surface_can_claim_production_ready": False,
                "submission_ready_export_gate_closeout_requires": (
                    "human_gate_receipt_or_mag_owned_typed_blocker"
                ),
            },
            "private_surface_policy_ref": "contracts/private_functional_surface_policy.json",
            "active_plan_ref": "docs/active/mag-ideal-state-cross-repo-gap-plan.md",
        },
        "app_projection_policy": {
            "app_consumes_shared_progress_projection_only": True,
            "app_can_read_domain_body": False,
            "app_can_write_domain_truth": False,
            "app_can_claim_quality_or_export": False,
            "display_policy": "classification_only_no_domain_artifact_body",
        },
        "authority_boundary": {
            "opl_owns_series_contract": True,
            "domain_owns_truth_quality_artifact_memory_and_receipts": True,
            "app_owns_display_and_user_action_shell": True,
            "generated_surface_can_claim_domain_ready": False,
        },
    }


def _pack_compiler_input(minimal_authority_surfaces: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "surface_kind": "opl_domain_pack_compiler_input",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "domain_pack_owner": TARGET_DOMAIN_ID,
        "generated_surface_owner": GENERATED_SURFACE_OWNER,
        "canonical_semantic_pack_root": "agent/",
        "canonical_semantic_pack_role": "repo_source_declarative_grant_pack",
        "required_domain_pack_paths": REQUIRED_DOMAIN_PACK_PATHS,
        "declarative_domain_pack": DECLARATIVE_DOMAIN_PACK,
        **pack_compiler_cognitive_kernel_fields(),
        "minimal_authority_functions": MINIMAL_AUTHORITY_FUNCTIONS,
        "minimal_authority_surface_taxonomy": build_mag_minimal_authority_surface_taxonomy(),
        "minimal_authority_surface_contracts": _json_ready(minimal_authority_surfaces),
        "generated_surfaces_requested": GENERATED_SURFACES,
        "domain_repo_can_own_generated_surface": False,
        "source_refs": {
            "canonical_domain_pack": "agent/",
            "action_catalog": "src/med_autogrant/action_catalog.py::build_mag_family_action_catalog",
            "stage_control_plane": "src/med_autogrant/stage_control_plane.py::build_mag_family_stage_control_plane",
            "functional_audit": (
                "src/med_autogrant/product_entry_parts/consumer_thinning.py::"
                "build_mag_consumer_thinning_contract"
            ),
        },
        "authority_boundary": {
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_authorize_quality_or_export": False,
            "domain_can_claim_generated_surface_owner": False,
        },
    }


def _generated_surface_handoff() -> dict[str, Any]:
    return {
        "surface_kind": "opl_generated_surface_handoff",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "generated_surface_owner": GENERATED_SURFACE_OWNER,
        "domain_repo_can_own_generated_surface": False,
        "source_contract_ref": "contracts/pack_compiler_input.json",
        "consumes_domain_pack_refs": True,
        "domain_pack_ref": "agent/",
        "generated_surfaces": [
            {
                "surface_id": surface_id,
                "owner": GENERATED_SURFACE_OWNER,
                "domain_repo_can_own_generated_surface": False,
                "consumes_domain_pack_refs": True,
                "status": "descriptor_source_available",
            }
            for surface_id in GENERATED_SURFACES
        ],
        "consumption_boundary": {
            "opl_generated_surfaces_consume": [
                "agent/prompts",
                "agent/stages",
                "agent/skills",
                "agent/quality_gates",
                "agent/knowledge",
                "contracts",
            ],
            "opl_generated_surfaces_do_not_write": [
                "grant_truth",
                "grant_body",
                "fundability_verdict",
                "authoring_quality_verdict",
                "submission_ready_export_verdict",
                "package_body",
                "memory_body",
                "owner_receipt_instance",
            ],
            "src_role": "domain_handler_minimal_authority_and_native_helper_only",
        },
        "required_domain_handoff": [
            "owner_receipt_schema",
            "typed_blocker_schema",
            "minimal_authority_function_refs",
            "no_forbidden_write_evidence",
        ],
    }


def _with_forbidden_roles(action_catalog: Mapping[str, Any]) -> dict[str, Any]:
    payload = dict(action_catalog)
    payload["forbidden_generic_owner_roles"] = FORBIDDEN_GENERIC_OWNER_ROLES
    payload["generated_surface_owner"] = GENERATED_SURFACE_OWNER
    payload["domain_repo_can_own_generated_surface"] = False
    return payload


def _memory_descriptor() -> dict[str, Any]:
    return {
        "surface_kind": "domain_memory_descriptor_locator",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "memory_body_owner": TARGET_DOMAIN_ID,
        "opl_projection_policy": "locator_and_receipt_refs_only",
        "authority_boundary": {
            "opl_can_write_memory_body": False,
            "opl_can_accept_or_reject_writeback": False,
            "domain_memory_accept_reject_owner": TARGET_DOMAIN_ID,
        },
    }


def _artifact_locator_contract() -> dict[str, Any]:
    return {
        "surface_kind": "artifact_locator_contract",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "canonical_artifact_authority": TARGET_DOMAIN_ID,
        "opl_projection_policy": "locator_lifecycle_and_receipt_refs_only",
        "authority_boundary": {
            "opl_can_mutate_artifacts": False,
            "opl_can_authorize_quality_or_export": False,
            "domain_artifact_authority_owner": TARGET_DOMAIN_ID,
        },
    }


def _owner_receipt_contract() -> dict[str, Any]:
    return {
        "surface_kind": "owner_receipt_contract",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "allowed_receipt_classes": [
            "owner_receipt",
            "typed_blocker",
            "no_regression_evidence",
            "memory_writeback_receipt",
            "artifact_lifecycle_receipt",
        ],
        "forbidden_claims": [
            "opl_authorized_domain_ready",
            "opl_authorized_quality_or_export_verdict",
            "opl_wrote_domain_truth",
            "opl_wrote_memory_body",
        ],
    }


def _agent_lab_handoff() -> dict[str, Any]:
    return build_agent_lab_handoff(generated_surface_owner=GENERATED_SURFACE_OWNER)


def _oma_handoff_refs(*, agent_lab_handoff: dict[str, Any]) -> dict[str, Any]:
    return build_oma_handoff_refs(agent_lab_handoff=agent_lab_handoff)


def _functional_privatization_audit(consumer_thinning_contract: Mapping[str, Any]) -> dict[str, Any]:
    privatized_functional_module_audit = dict(
        consumer_thinning_contract["privatized_functional_module_audit"]
    )
    return {
        "surface_kind": "functional_privatization_audit",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        **privatized_functional_module_audit,
        "mag_consumer_thinning_contract": dict(consumer_thinning_contract),
        "privatized_functional_module_audit": privatized_functional_module_audit,
        "functional_followthrough_gap_classification": dict(
            consumer_thinning_contract["functional_followthrough_gap_classification"]
        ),
        "authority_boundary": {
            "opl_can_write_domain_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_authorize_quality_or_export": False,
            "domain_can_claim_generic_runtime_owner": False,
            "domain_repo_can_own_generated_surface": False,
        },
    }


def _private_functional_surface_policy() -> dict[str, Any]:
    return build_private_functional_surface_policy(
        forbidden_generic_owner_roles=FORBIDDEN_GENERIC_OWNER_ROLES,
        physical_source_classification_buckets=PHYSICAL_SOURCE_CLASSIFICATION_BUCKETS,
        physical_source_surface_classifications=PHYSICAL_SOURCE_SURFACE_CLASSIFICATIONS,
        forbidden_physical_residue_classes=FORBIDDEN_PHYSICAL_RESIDUE_CLASSES,
        active_path_scan_policy=ACTIVE_PATH_SCAN_POLICY,
        retirement_evidence_refs=RETIREMENT_EVIDENCE_REFS,
        target_owner_by_physical_classification=TARGET_OWNER_BY_PHYSICAL_CLASSIFICATION,
        active_caller_status_by_physical_classification=ACTIVE_CALLER_STATUS_BY_PHYSICAL_CLASSIFICATION,
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync MAG OPL standard domain-agent pack contracts.")
    parser.add_argument("--check", action="store_true", help="Print the generated pack without writing.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.check:
        print(json.dumps(build_standard_pack(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    print(json.dumps(sync_standard_pack(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
