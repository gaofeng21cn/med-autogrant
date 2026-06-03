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
from med_autogrant.public_cli import public_cli_command
from med_autogrant.stage_control_plane import build_mag_family_stage_control_plane
from opl_harness_shared.product_entry_companions import build_operator_loop_action_catalog


REPO_ROOT = Path(__file__).resolve().parents[2]
DOMAIN_LABEL = "Med Auto Grant"
GENERATED_SURFACE_OWNER = "one-person-lab"
INPUT_PLACEHOLDER = "<input_path>"
TASK_INTENT_PLACEHOLDER = "<task_intent>"
OUTPUT_DIR_PLACEHOLDER = "<output_dir>"
SHARED_POLICY_RELEASE = {
    "policy_release_contract_ref": (
        "contracts/opl-framework/foundry-agent-series-policy-release.json"
    ),
    "policy_bundle_fingerprint": (
        "sha256:5d77102e99e6e49acd88714cd94dcafe0969b8f2a5529928d753002ac3d4619d"
    ),
    "fingerprint_algorithm": "sha256:stable-json",
    "domain_contract_policy_release_pin_required": True,
    "domain_adapter_must_not_copy_policy_body_as_authority": True,
    "consumer_alignment_check": "foundry:policy-release",
}

SERIES_DESIGN_PROFILE = {
    "surface_kind": "opl_foundry_agent_series_design_profile",
    "version": "foundry-agent-series-design-profile.v1",
    "profile_id": "opl_foundry_agent_series_design_profile.v1",
    "profile_summary": (
        "All Foundry Agents share the same OPL domain-pack to stage-led execution "
        "to gate/receipt to handoff lifecycle; domain inputs, outputs, aliases, "
        "and authority functions vary by agent."
    ),
    "shared_lifecycle_pipeline": [
        "domain_material_intake",
        "domain_pack_interpretation",
        "stage_led_agent_execution",
        "independent_quality_gate_or_owner_review",
        "owner_receipt_or_typed_blocker_closeout",
        "artifact_or_deliverable_handoff",
        "opl_refs_only_projection_and_recovery",
    ],
    "domain_io_profile": {
        "input_slot": "domain_materials_or_task_request",
        "output_slot": "domain_deliverable_or_owner_handoff",
        "input_is_domain_specific": True,
        "output_is_domain_specific": True,
        "shared_runtime_interpretation": (
            "OPL treats input/output as opaque domain refs and projects identity, "
            "stage, progress, closeout, evidence, and recovery metadata only."
        ),
    },
    "stage_pack_sections": [
        "prompts",
        "stages",
        "skills",
        "knowledge",
        "quality_gates",
    ],
    "shared_closeout_contract": {
        "success_shape": "domain_owner_receipt_ref",
        "blocked_shape": "domain_owned_typed_blocker_ref",
        "route_back_shape": "route_back_or_human_gate_ref",
        "provider_completion_is_closeout": False,
    },
    "authority_invariants": {
        "opl_can_infer_domain_output": False,
        "opl_can_read_domain_body": False,
        "opl_can_write_domain_truth": False,
        "opl_can_authorize_quality_or_export": False,
        "domain_owns_input_truth_and_output_authority": True,
    },
}

DOMAIN_SPECIFIC_PROFILE = {
    "profile_id": "mag_domain_specific_series_profile.v1",
    "series_members": ["MAS", "MAG", "RCA", "OMA"],
    "shared_opl_agent_lifecycle": [
        "domain_pack",
        "stage_led_execution",
        "independent_quality_gate",
        "owner_receipt_or_typed_blocker",
        "handoff",
    ],
    "mag_domain_input_profile": {
        "domain_pack_kind": "declarative_grant_pack",
        "primary_inputs": [
            "funding_call_refs",
            "applicant_profile_refs",
            "grant_strategy_memory_refs",
            "source_material_refs",
        ],
    },
    "mag_domain_output_profile": {
        "primary_outputs": [
            "grant_proposal_refs",
            "revision_package_refs",
            "submission_ready_package_refs",
            "owner_receipt_or_typed_blocker_refs",
        ],
        "domain_specific_gate": "independent_fundability_quality_export_and_submission_gate",
    },
    "series_variation_policy": (
        "MAG differs from MAS/RCA/OMA by grant and fund-material inputs plus grant proposal "
        "and package outputs, not by lifecycle ownership."
    ),
    "opl_scope": "refs_projection_runtime_only",
    "mag_authority_retained": [
        "grant_truth",
        "fundability_verdict",
        "authoring_quality_verdict",
        "export_verdict",
        "submission_verdict",
        "artifact_authority",
        "memory_accept_reject",
        "owner_receipt",
    ],
    "forbidden_series_drift": [
        "mag_specific_lifecycle_fork",
        "opl_claims_grant_truth",
        "opl_claims_quality_or_submission_verdict",
        "generated_surface_signs_owner_receipt",
    ],
}

FORBIDDEN_GENERIC_OWNER_ROLES = [
    "generic_scheduler_owner",
    "generic_daemon_owner",
    "generic_lifecycle_owner",
    "generic_queue_owner",
    "generic_attempt_ledger_owner",
    "generic_state_machine_runner_owner",
    "generic_cli_mcp_product_wrapper_owner",
    "generic_domain_handler_owner",
    "generic_sidecar_owner",
    "generic_session_store_owner",
    "generic_status_workbench_owner",
    "generic_workspace_source_intake_owner",
    "generic_memory_transport_owner",
    "generic_artifact_gallery_owner",
    "generic_operator_workbench_owner",
    "generic_observability_slo_owner",
    "generic_persistence_engine_owner",
    "generic_sqlite_lifecycle_owner",
    "generic_native_helper_envelope_owner",
    "generic_review_repair_transport_owner",
    "generated_surface_owner_in_domain_repo",
]

GENERATED_SURFACES = [
    "cli",
    "mcp",
    "skill",
    "product_entry_manifest",
    "domain_handler",
    "status_read_model",
    "workbench_drilldown",
    "functional_harness_cases",
]

DECLARATIVE_DOMAIN_PACK = [
    "stage_descriptors",
    "action_catalog",
    "transition_oracle",
    "funding_call_source_policy",
    "domain_memory_locator",
    "artifact_locator_contract",
    "owner_receipt_schema",
]

REQUIRED_DOMAIN_PACK_PATHS = [
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
]

MINIMAL_AUTHORITY_FUNCTIONS = [
    "fundability_verdict",
    "quality_verdict",
    "export_verdict",
    "package_authority",
    "memory_accept_reject",
    "owner_receipt_signer",
    "grant_helper",
]

PHYSICAL_SOURCE_CLASSIFICATION_BUCKETS = [
    "declarative_grant_handler",
    "refs_only_adapter",
    "minimal_authority_function",
    "legacy_proof_tombstone",
]

RETIREMENT_EVIDENCE_REFS = [
    "external_evidence://physical_morphology_hygiene/active_caller_migration_receipt",
    "external_evidence://physical_morphology_hygiene/direct_hosted_parity_no_regression",
    "external_evidence://physical_morphology_hygiene/owner_receipt_or_typed_blocker_roundtrip",
    "external_evidence://physical_morphology_hygiene/continuous_no_forbidden_write",
    "physical_morphology://no_active_compat_alias_or_facade_scan",
]

FORBIDDEN_PHYSICAL_RESIDUE_CLASSES = [
    "legacy_local_persistence_surface",
    "legacy_attempt_record_surface",
    "legacy_repo_cadence_owner",
    "legacy_executor_runtime_probe",
    "legacy_compat_alias_surface",
]

PHYSICAL_SOURCE_SURFACE_CLASSIFICATIONS = [
    {
        "surface_id": "domain_runtime",
        "classification": "declarative_grant_handler",
        "source_refs": [
            "src/med_autogrant/domain_runtime_parts/substrate.py",
            "src/med_autogrant/domain_entry.py",
        ],
        "allowed_role": "route_authority_adapter_without_facade_reexport",
        "forbidden_roles": [
            "generic_runner",
            "generic_queue",
            "legacy_attempt_record_surface",
            "session_shell",
        ],
    },
    {
        "surface_id": "product_entry",
        "classification": "refs_only_adapter",
        "source_refs": [
            "src/med_autogrant/product_entry.py",
            "src/med_autogrant/product_entry_parts/manifest.py",
            "src/med_autogrant/product_entry_parts/manifest_builder.py",
            "src/med_autogrant/product_entry_parts/manifest_builder_parts/runtime_task_shell.py",
            "src/med_autogrant/product_entry_parts/manifest_builder_parts/shell_assembly.py",
            "src/med_autogrant/product_entry_parts/entry.py",
        ],
        "allowed_role": "grant_handler_target_receipt_refs_and_typed_blockers",
        "forbidden_roles": [
            "generated_product_shell_owner",
            "app_workbench_owner",
            "generic_status_owner",
        ],
    },
    {
        "surface_id": "grouped_cli_wrapper",
        "classification": "refs_only_adapter",
        "source_refs": [
            "src/med_autogrant/cli.py",
            "src/med_autogrant/cli_parts/handlers.py",
            "src/med_autogrant/cli_parts/parser_adders.py",
        ],
        "allowed_role": "direct_cli_domain_handler_target_until_generated_caller_migration",
        "forbidden_roles": [
            "generic_cli_mcp_product_wrapper_owner",
            "legacy_flat_alias_surface",
            "generated_surface_owner_in_domain_repo",
        ],
    },
    {
        "surface_id": "status",
        "classification": "refs_only_adapter",
        "source_refs": [
            "src/med_autogrant/product_entry_parts/preflight.py",
            "src/med_autogrant/product_entry_parts/progress.py",
            "src/med_autogrant/product_entry_parts/progress_projection_helpers.py",
            "src/med_autogrant/mainline_status.py",
        ],
        "allowed_role": "grant_status_refs_and_typed_blocker_projection",
        "forbidden_roles": [
            "generic_status_workbench_owner",
            "operator_workbench_owner",
            "generic_observability_runtime",
        ],
    },
    {
        "surface_id": "user_loop",
        "classification": "refs_only_adapter",
        "source_refs": [
            "src/med_autogrant/action_catalog.py",
            "src/med_autogrant/product_entry_parts/loop_contracts.py",
            "src/med_autogrant/product_entry_parts/primitives.py",
            "src/med_autogrant/stage_control_plane.py",
        ],
        "allowed_role": "grant_user_loop_domain_action_target_and_receipt_refs",
        "forbidden_roles": [
            "generic_daemon_owner",
            "generic_scheduler_owner",
            "app_workbench_owner",
        ],
    },
    {
        "surface_id": "domain_handler",
        "classification": "refs_only_adapter",
        "source_refs": [
            "src/med_autogrant/product_entry_parts/domain_handler.py",
        ],
        "allowed_role": "guarded_domain_dispatch_and_refs_projection",
        "forbidden_roles": [
            "generic_domain_handler_owner",
            "generic_sidecar_owner",
            "operator_workbench_owner",
            "action_routing_shell_owner",
        ],
    },
    {
        "surface_id": "runtime_registration",
        "classification": "declarative_grant_handler",
        "source_refs": [
            "src/med_autogrant/product_entry_parts/runtime_registration.py",
            "src/med_autogrant/product_entry_parts/opl_substrate_adapter.py",
        ],
        "allowed_role": "domain_descriptor_and_stage_pack_registration_refs",
        "forbidden_roles": [
            "provider_runtime_owner",
            "repo_daemon_owner",
            "local_manager_owner",
        ],
    },
    {
        "surface_id": "control_plane",
        "classification": "refs_only_adapter",
        "source_refs": [
            "src/med_autogrant/control_plane.py",
            "src/med_autogrant/product_entry_parts/runtime_surfaces.py",
        ],
        "allowed_role": "body_free_runtime_control_refs_projection",
        "forbidden_roles": [
            "generic_transition_runner",
            "provider_repair_executor",
            "attempt_ledger_owner",
        ],
    },
    {
        "surface_id": "lifecycle",
        "classification": "refs_only_adapter",
        "source_refs": [
            "src/med_autogrant/product_entry_parts/lifecycle_receipt_bundle.py",
            "src/med_autogrant/product_entry_parts/continuous_reconciliation.py",
        ],
        "allowed_role": "cleanup_restore_retention_receipt_refs_adapter",
        "forbidden_roles": [
            "generic_lifecycle_owner",
            "artifact_lifecycle_shell_owner",
            "lifecycle_ledger_owner",
        ],
    },
    {
        "surface_id": "memory",
        "classification": "minimal_authority_function",
        "source_refs": [
            "src/med_autogrant/product_entry_parts/domain_memory.py",
            "src/med_autogrant/product_entry_parts/memory_receipt_projection.py",
        ],
        "allowed_role": "grant_strategy_memory_accept_reject_receipt_refs",
        "forbidden_roles": [
            "generic_memory_transport_owner",
            "memory_body_transport_owner",
            "mechanical_memory_acceptance",
        ],
    },
    {
        "surface_id": "package",
        "classification": "minimal_authority_function",
        "source_refs": [
            "src/med_autogrant/final_package.py",
            "src/med_autogrant/final_package_validation.py",
            "src/med_autogrant/product_entry_parts/package_lifecycle_handoff.py",
        ],
        "allowed_role": "submission_ready_package_authority_and_gap_refs",
        "forbidden_roles": [
            "generic_artifact_lifecycle_owner",
            "artifact_gallery_owner",
            "provider_completion_export_verdict",
        ],
    },
    {
        "surface_id": "autonomy_controller",
        "classification": "minimal_authority_function",
        "source_refs": [
            "src/med_autogrant/grant_autonomy_controller.py",
            "src/med_autogrant/grant_autonomy_loop_shell.py",
            "src/med_autogrant/grant_autonomy_loop_parts.py",
            "src/med_autogrant/grant_autonomy_start.py",
            "src/med_autogrant/grant_autonomy_common.py",
            "src/med_autogrant/grant_autonomy_controller_plan.py",
            "src/med_autogrant/grant_autonomy_quality_payload.py",
            "src/med_autogrant/grant_autonomy_report_resume.py",
        ],
        "allowed_role": "grant_route_budget_blocker_policy",
        "forbidden_roles": [
            "long_running_runtime_loop",
            "repo_scheduler_daemon",
            "repo_owned_durable_attempt_loop",
            "repo_owned_default_executor_helper",
            "mechanical_quality_or_export_verdict",
        ],
        "execution_boundary": {
            "required_runtime_owner": "one-person-lab",
            "required_default_executor": "codex_cli",
            "required_evidence": "OPL stage attempt lease or default executor receipt",
            "missing_evidence_return_shape": "typed_blocker",
            "mag_owns_durable_loop": False,
            "hermes_agent_role": "explicit_non_default_opl_executor_adapter_receipt_lane_only",
        },
    },
    {
        "surface_id": "owner_receipt_helper",
        "classification": "minimal_authority_function",
        "source_refs": [
            "src/med_autogrant/product_entry_parts/owner_receipt_writers.py",
            "src/med_autogrant/product_entry_parts/owner_receipt_reconciliation.py",
            "src/med_autogrant/product_entry_parts/production_live_acceptance.py",
            "contracts/owner_receipt_contract.json",
        ],
        "allowed_role": "domain_owner_receipt_signer_and_body_free_refs_projection",
        "forbidden_roles": [
            "generic_attempt_ledger_owner",
            "generic_persistence_engine_owner",
            "mechanical_quality_or_export_verdict",
        ],
    },
    {
        "surface_id": "legacy_runtime_residue",
        "classification": "legacy_proof_tombstone",
        "source_refs": [
            "docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md",
        ],
        "evidence_refs": [
            "/product_entry_manifest/physical_skeleton_follow_through/active_path_scan_no_legacy_default_caller",
        ],
        "allowed_role": "history_or_tombstone_only",
        "forbidden_roles": FORBIDDEN_PHYSICAL_RESIDUE_CLASSES,
    },
]

TARGET_OWNER_BY_PHYSICAL_CLASSIFICATION = {
    "declarative_grant_handler": TARGET_DOMAIN_ID,
    "refs_only_adapter": GENERATED_SURFACE_OWNER,
    "minimal_authority_function": TARGET_DOMAIN_ID,
    "legacy_proof_tombstone": "history_tombstone",
}

ACTIVE_CALLER_STATUS_BY_PHYSICAL_CLASSIFICATION = {
    "declarative_grant_handler": "active_domain_pack_or_handler_target",
    "refs_only_adapter": "active_refs_only_adapter_until_opl_generated_caller_migration",
    "minimal_authority_function": "retained_mag_authority_function",
    "legacy_proof_tombstone": "no_active_caller_history_or_tombstone_only",
}


def _json_ready(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def build_standard_pack() -> dict[str, Any]:
    action_catalog = build_mag_family_action_catalog(
        action_commands=_base_operator_loop_actions(),
    )
    stage_control_plane = build_mag_family_stage_control_plane(
        family_action_catalog=action_catalog,
    )
    physical_skeleton_follow_through = build_physical_skeleton_follow_through()
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
        "series_design_profile": SERIES_DESIGN_PROFILE,
        "domain_specific_profile": DOMAIN_SPECIFIC_PROFILE,
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
