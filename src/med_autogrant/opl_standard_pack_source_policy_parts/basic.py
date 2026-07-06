from __future__ import annotations

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

REPO_VERIFICATION_SCRIPT_REFS = [
    "scripts/check_generated_aggregate_sources.py",
    "scripts/check_source_purity_guard.py",
    "scripts/install-codex-plugin.sh",
    "scripts/line_budget.py",
    "scripts/opl-module-healthcheck.sh",
    "scripts/repo-hygiene.sh",
    "scripts/run-pytest-clean.sh",
    "scripts/run-python-clean.sh",
    "scripts/verify.sh",
]
