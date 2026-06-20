from __future__ import annotations

from med_autogrant.opl_standard_pack_constants import GENERATED_SURFACE_OWNER
from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID

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
    "tool_affordance_catalog",
    "cognitive_kernel_adoption_contract",
    "golden_path_profile",
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
    "agent/tools/domain_affordances.md",
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
    "repo_native_verification_wrapper",
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

ACTIVE_PATH_SCAN_POLICY = {
    "surface_kind": "mag_active_path_scan_policy",
    "policy_id": "mag.active_path_scan.no_legacy_default_caller.policy.v1",
    "target_domain_id": TARGET_DOMAIN_ID,
    "state": "contract_owned_no_resurrection_scan_policy",
    "roots": ["src", "tests", "schemas", "contracts", "scripts", "plugins"],
    "files": ["Makefile", "pyproject.toml", ".agents/plugins/marketplace.json"],
    "suffixes": [".json", ".py", ".sh", ".toml", ".yaml", ".yml"],
    "excludes_human_docs": True,
    "human_doc_policy": (
        "docs/history/provenance may name retired surfaces without making them default callers"
    ),
    "scans_repo_source_only": True,
    "retired_active_paths": [
        "tests/test_product_entry.py",
        "src/med_autogrant/domain_runtime_parts/patch_targets.py",
        "src/med_autogrant/gateway.py",
        "src/med_autogrant/local_manager.py",
        "src/med_autogrant/" + "host" + "_agent.py",
    ],
    "forbidden_default_caller_patterns": [
        {
            "pattern_id": "domain_runtime_patch_bridge_import",
            "literal_parts": ["med_autogrant.domain_runtime_parts", ".patch_targets"],
            "policy": "patch runtime owner modules directly; do not use retired facade patch bridge",
        },
        {
            "pattern_id": "hermes_default_runtime_owner",
            "literal_parts": ["DEFAULT_RUNTIME_OWNER = \"", "hermes_agent", "\""],
            "policy": "Hermes-Agent remains explicit proof/provider provenance only",
        },
        {
            "pattern_id": "hermes_default_executor_owner",
            "literal_parts": ["DEFAULT_EXECUTOR_OWNER = \"", "hermes_agent", "\""],
            "policy": "default executor stays Codex CLI",
        },
        {
            "pattern_id": "claude_default_executor_owner",
            "literal_parts": ["DEFAULT_EXECUTOR_OWNER = \"", "claude_code", "\""],
            "policy": "non-default executors require explicit OPL adapter selection",
        },
        {
            "pattern_id": "gateway_default_runtime_owner",
            "literal_parts": ["DEFAULT_RUNTIME_OWNER = \"", "gateway", "\""],
            "policy": "Gateway/local-manager wording is retired from active runtime ownership",
        },
        {
            "pattern_id": "local_manager_default_runtime_owner",
            "literal_parts": ["DEFAULT_RUNTIME_OWNER = \"", "local_manager", "\""],
            "policy": "local-manager is not a default product/runtime owner",
        },
        {
            "pattern_id": "host" + "_agent_default_runtime_owner",
            "literal_parts": ["DEFAULT_RUNTIME_OWNER = \"", "host" + "_agent", "\""],
            "policy": "repo-local host-agent runtime is not a product owner",
        },
        {
            "pattern_id": "json_hermes_default_executor",
            "literal_parts": ["\"default_executor_name\": \"", "hermes_agent", "\""],
            "policy": "manifest/contracts must keep Codex CLI as default executor",
        },
    ],
    "authority_boundary": {
        "policy_can_authorize_physical_delete": False,
        "policy_can_claim_production_long_run_soak": False,
        "policy_can_claim_grant_readiness": False,
    },
}

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
            "src/med_autogrant/product_entry_parts/manifest_shell/runtime_task_shell.py",
            "src/med_autogrant/product_entry_parts/manifest_shell/shell_assembly.py",
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
        "surface_id": "repo_shell_verification_wrappers",
        "classification": "repo_native_verification_wrapper",
        "source_refs": [
            "scripts/install-codex-plugin.sh",
            "scripts/opl-module-healthcheck.sh",
            "scripts/repo-hygiene.sh",
            "scripts/run-opl-quality-details.sh",
            "scripts/run-pytest-clean.sh",
            "scripts/run-python-clean.sh",
            "scripts/run-structural-quality-gate.sh",
            "scripts/verify.sh",
        ],
        "allowed_role": "repo_native_verification_hygiene_temp_env_bootstrap_and_quality_entry",
        "forbidden_roles": [
            "generic_scheduler_owner",
            "generic_daemon_owner",
            "generic_queue_owner",
            "generic_attempt_ledger_owner",
            "generic_state_machine_runner_owner",
            "generic_cli_mcp_product_wrapper_owner",
            "generic_domain_handler_owner",
            "generic_session_store_owner",
            "generic_status_workbench_owner",
            "generic_workspace_source_intake_owner",
            "generic_memory_transport_owner",
            "generic_artifact_gallery_owner",
            "generic_operator_workbench_owner",
            "generic_observability_slo_owner",
            "generic_native_helper_envelope_owner",
            "generic_review_repair_transport_owner",
            "generated_surface_owner_in_domain_repo",
        ],
        "authority_boundary": {
            "can_own_generic_runtime": False,
            "can_own_generated_wrapper": False,
            "can_authorize_physical_delete": False,
            "can_claim_grant_readiness": False,
            "can_claim_production_long_run_soak": False,
        },
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
    "repo_native_verification_wrapper": "repo_hygiene_boundary",
    "legacy_proof_tombstone": "history_tombstone",
}

ACTIVE_CALLER_STATUS_BY_PHYSICAL_CLASSIFICATION = {
    "declarative_grant_handler": "active_domain_pack_or_handler_target",
    "refs_only_adapter": "active_refs_only_adapter_until_opl_generated_caller_migration",
    "minimal_authority_function": "retained_mag_authority_function",
    "repo_native_verification_wrapper": "active_repo_verification_entry",
    "legacy_proof_tombstone": "no_active_caller_history_or_tombstone_only",
}
