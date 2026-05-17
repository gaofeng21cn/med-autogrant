from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


def _build_privatized_functional_module_audit() -> dict[str, Any]:
    return {
        "surface_kind": "mag_privatized_functional_module_audit",
        "audit_id": "mag.privatized_functional_module_audit.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "state": "manifest_projected_for_opl_unified_audit",
        "classification_policy": (
            "classify_non_knowledge_functional_surfaces_without_reclassifying_grant_authority"
        ),
        "opl_unified_audit_read_model": True,
        "claims_generic_runtime_removed_from_mag": False,
        "claims_opl_replacement_exists": False,
        "claims_production_long_run_soak_complete": False,
        "opl_owned_generic_primitive_consumers": [
            _build_functional_module_audit_item(
                "runtime_registration",
                classification="opl_owned_generic_primitive_consumer",
                owner="one-person-lab",
                mag_role="descriptor_projection_consumer",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/runtime_registration.py",
                    "src/med_autogrant/product_entry_parts/opl_substrate_adapter.py",
                    "src/med_autogrant/product_entry_parts/manifest_runtime_companions.py",
                ],
                active_callers=[
                    "product-entry-manifest runtime registration projection",
                    "product sidecar export OPL control plane registration",
                    "contracts/runtime-program/opl-family-contract-adoption.json",
                ],
                active_caller_status="active_thin_projection_no_generic_runtime_owner",
                migration_action=(
                    "OPL owns domain runtime registry and provider-backed activation; "
                    "MAG keeps descriptor refs and safe action refs only."
                ),
                retention_reason=(
                    "MAG must expose its domain id, stage pack refs, and safe action refs "
                    "so OPL can discover the grant agent without owning grant truth."
                ),
                cannot_absorb_reason=(
                    "OPL can absorb the registry shell, but cannot absorb MAG's domain id, "
                    "stage semantics, or safe action metadata."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/skill_catalog/domain_projection/opl_stage_runtime_registration",
                    "/sidecar_export/opl_control_plane/registration",
                ],
                opl_expected_primitives=[
                    "domain_runtime_registry",
                    "stage_led_activation",
                    "provider_backed_runtime_registration",
                ],
                mag_retained_authority=["domain_id", "stage_pack_refs", "safe_action_refs"],
            ),
            _build_functional_module_audit_item(
                "task_lifecycle",
                classification="opl_owned_generic_primitive_consumer",
                owner="one-person-lab",
                mag_role="grant_checkpoint_read_model_provider",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/progress.py",
                    "src/med_autogrant/product_entry_parts/progress_projection_helpers.py",
                    "src/med_autogrant/product_entry_parts/runtime_surfaces.py",
                ],
                active_callers=[
                    "product-entry-manifest task_lifecycle/progress_projection",
                    "product status",
                    "product user-loop",
                ],
                active_caller_status="active_domain_checkpoint_projection",
                migration_action=(
                    "OPL should own generic task checkpoint and stage-attempt lifecycle; "
                    "MAG should keep grant checkpoint meaning as read projection."
                ),
                retention_reason=(
                    "Grant stages such as critique, revision, freeze, and package readiness "
                    "carry domain meaning that OPL cannot infer generically."
                ),
                cannot_absorb_reason=(
                    "Generic lifecycle can be absorbed; grant lifecycle stage semantics "
                    "and checkpoint interpretation remain MAG authority."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/task_lifecycle",
                    "/product_entry_manifest/progress_projection",
                ],
                opl_expected_primitives=[
                    "generic_task_checkpoint_shell",
                    "stage_attempt_lifecycle",
                    "human_gate_projection",
                ],
                mag_retained_authority=["grant_lifecycle_stage", "grant_checkpoint_meaning"],
            ),
            _build_functional_module_audit_item(
                "session_ledger_attention_queue",
                classification="opl_owned_generic_primitive_consumer",
                owner="one-person-lab",
                mag_role="wakeup_refs_and_safe_action_provider",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/loop_contracts.py",
                    "src/med_autogrant/product_entry_parts/runtime_surfaces.py",
                    "src/med_autogrant/hosted_contract_bundle.py",
                    "src/med_autogrant/domain_runtime_parts/io.py",
                    "src/med_autogrant/domain_runtime_parts/runtime_ops.py",
                ],
                active_callers=[
                    "product user-loop",
                    "product sidecar export user_loop_attention_queue",
                    "runtime run/resume local journal",
                ],
                active_caller_status="active_local_journal_and_refs_pending_opl_ledger_absorption",
                migration_action=(
                    "OPL should absorb session ledger, attention queue, wakeup scheduling, "
                    "and stage-attempt ledger; MAG should keep only safe action refs and "
                    "grant next-action meaning."
                ),
                retention_reason=(
                    "The current MAG journal/attention payload is still the local caller's "
                    "durable anchor until OPL production ledger consumption is proven."
                ),
                cannot_absorb_reason=(
                    "OPL can absorb ledger transport, but cannot decide the grant-specific "
                    "meaning of next actions or safe action refs."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/session_continuity",
                    "/product_entry_manifest/automation",
                    "/sidecar_export/user_loop_attention_queue",
                ],
                opl_expected_primitives=[
                    "session_ledger",
                    "typed_attention_queue",
                    "wakeup_scheduler",
                ],
                mag_retained_authority=["safe_action_refs", "grant_next_action_meaning"],
            ),
            _build_functional_module_audit_item(
                "lifecycle_adapter",
                classification="opl_owned_generic_primitive_consumer",
                owner="one-person-lab",
                mag_role="guarded_receipt_authority_provider",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/lifecycle_receipt_bundle.py",
                    "src/med_autogrant/product_entry_parts/owner_receipts.py",
                    "src/med_autogrant/product_entry_parts/continuous_reconciliation.py",
                    "src/med_autogrant/product_entry_parts/runtime_registration.py",
                ],
                active_callers=[
                    "product lifecycle-receipt-evidence",
                    "product lifecycle-receipt-bundle",
                    "product sidecar dispatch lifecycle/receipt",
                ],
                active_caller_status="active_receipt_authority_projection_no_generic_lifecycle_owner",
                migration_action=(
                    "OPL should provide cleanup/restore/retention lifecycle shell and "
                    "receipt transport; MAG should retain guarded owner receipt authority."
                ),
                retention_reason=(
                    "Cleanup, restore, and retention events that touch grant artifacts need "
                    "MAG owner receipt and package authority refs."
                ),
                cannot_absorb_reason=(
                    "Generic lifecycle transport is absorbable; domain mutation approval "
                    "and package authority cannot move out of MAG."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                    "/sidecar_export/opl_control_plane/family_lifecycle_adapter",
                ],
                opl_expected_primitives=[
                    "cleanup_restore_retention_shell",
                    "artifact_locator_ledger",
                    "lifecycle_receipt_transport",
                ],
                mag_retained_authority=[
                    "domain_mutation_requires_mag_owner_receipt",
                    "package_authority",
                ],
            ),
            _build_functional_module_audit_item(
                "observability",
                classification="opl_owned_generic_primitive_consumer",
                owner="one-person-lab",
                mag_role="refs_counts_blockers_provider",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/receipt_observability.py",
                    "src/med_autogrant/product_entry_parts/stage_attempt_observability.py",
                    "src/med_autogrant/product_entry_parts/autonomy_observability.py",
                    "src/med_autogrant/product_entry_parts/continuous_reconciliation.py",
                ],
                active_callers=[
                    "product controlled-soak-receipt-observability",
                    "product stage-attempt-observability",
                    "product continuous-receipt-reconciliation",
                ],
                active_caller_status="active_refs_counts_projection_no_repair_execution",
                migration_action=(
                    "OPL should own runtime observability export, SLO, repair projection, "
                    "and workbench display; MAG should provide refs, counts, blockers, and verdict refs."
                ),
                retention_reason=(
                    "MAG observability projections carry grant owner receipt refs, typed blockers, "
                    "and verdict refs needed by the OPL read model."
                ),
                cannot_absorb_reason=(
                    "OPL can absorb display/SLO/repair shell; it cannot create grant verdicts "
                    "or mutate receipt authority from observability data."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/mag_consumer_thinning_contract/opl_runtime_observability_consumption",
                    "/sidecar_export/opl_runtime_observability_consumption",
                ],
                opl_expected_primitives=[
                    "runtime_observability_export",
                    "slo_projection",
                    "repair_projection",
                ],
                mag_retained_authority=["owner_receipt_refs", "typed_blocker_refs", "verdict_refs"],
            ),
            _build_functional_module_audit_item(
                "sidecar_product_status_shell",
                classification="opl_owned_generic_primitive_consumer",
                owner="one-person-lab",
                mag_role="thin_product_projection_adapter",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/sidecar.py",
                    "src/med_autogrant/product_entry_parts/entry.py",
                    "src/med_autogrant/product_entry_parts/manifest.py",
                    "src/med_autogrant/product_entry.py",
                ],
                active_callers=[
                    "product sidecar export",
                    "product sidecar dispatch",
                    "product manifest/status/direct-entry/user-loop",
                ],
                active_caller_status="active_domain_sidecar_adapter_not_generic_product_shell",
                migration_action=(
                    "OPL should own product/operator/action-routing shell; MAG should keep "
                    "domain sidecar projection and guarded dispatch adapter."
                ),
                retention_reason=(
                    "OPL needs a MAG-owned sidecar adapter to read receipts and invoke guarded "
                    "domain actions without owning grant truth."
                ),
                cannot_absorb_reason=(
                    "The generic shell can be absorbed, but MAG-specific dispatch validation, "
                    "receipt refs, and safe action semantics remain domain owned."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/product_entry_status",
                    "/sidecar_export",
                ],
                opl_expected_primitives=[
                    "product_status_shell",
                    "operator_projection_shell",
                    "action_routing_shell",
                ],
                mag_retained_authority=[
                    "grant_status_meaning",
                    "owner_receipt_refs",
                    "safe_action_refs",
                ],
            ),
            _build_functional_module_audit_item(
                "package_lifecycle_shell",
                classification="opl_owned_generic_primitive_consumer",
                owner="one-person-lab",
                mag_role="package_authority_and_gap_refs_provider",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/package_lifecycle_handoff.py",
                    "src/med_autogrant/final_package.py",
                    "src/med_autogrant/final_package_validation.py",
                    "src/med_autogrant/domain_runtime_parts/package_surface.py",
                ],
                active_callers=[
                    "product package-lifecycle-handoff",
                    "package submission-ready",
                    "domain runtime package surface",
                ],
                active_caller_status="active_package_authority_projection_pending_opl_lifecycle_shell",
                migration_action=(
                    "OPL should own artifact/package lifecycle shell, restore/retention ledger, "
                    "and package refs index; MAG should retain export gate and submission-ready verdict."
                ),
                retention_reason=(
                    "Submission-ready export is a grant-domain authority surface, not a generic "
                    "artifact lifecycle success flag."
                ),
                cannot_absorb_reason=(
                    "OPL can absorb artifact lifecycle transport and gallery shell; it cannot "
                    "declare MAG package readiness or export verdict."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/artifact_locator_contract",
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                ],
                opl_expected_primitives=[
                    "artifact_package_lifecycle_shell",
                    "restore_retention_ledger",
                    "package_refs_index",
                ],
                mag_retained_authority=[
                    "submission_ready_verdict",
                    "export_gate",
                    "manual_portal_boundary",
                ],
            ),
            _build_functional_module_audit_item(
                "source_intake_shell",
                classification="opl_owned_generic_primitive_consumer",
                owner="one-person-lab",
                mag_role="funding_call_task_lock_adapter",
                code_paths=[
                    "src/med_autogrant/workspace.py",
                    "src/med_autogrant/workspace_index.py",
                    "src/med_autogrant/workspace_scaffold.py",
                    "src/med_autogrant/workspace_validation.py",
                    "src/med_autogrant/product_entry_parts/preflight.py",
                ],
                active_callers=[
                    "workspace summarize/validate/scaffold commands",
                    "product-entry preflight",
                    "product manifest workspace_locator",
                ],
                active_caller_status="active_workspace_truth_adapter_pending_opl_source_shell",
                migration_action=(
                    "OPL should own workspace/source intake shell, source receipts, freshness, "
                    "and repair projection; MAG should retain funding-call interpretation and task lock."
                ),
                retention_reason=(
                    "Funding-call interpretation, applicant profile fit, and grant task lock are "
                    "domain authority decisions."
                ),
                cannot_absorb_reason=(
                    "OPL can absorb source transport and freshness shell; it cannot own funding "
                    "call interpretation or grant task lock."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/workspace_locator",
                    "/product_entry_manifest/product_entry_preflight",
                ],
                opl_expected_primitives=[
                    "workspace_source_intake_shell",
                    "source_receipt",
                    "freshness_repair_projection",
                ],
                mag_retained_authority=[
                    "funding_call_interpretation",
                    "profile_selection",
                    "grant_task_lock",
                ],
            ),
            _build_functional_module_audit_item(
                "human_workbench_scheduler_daemon",
                classification="opl_owned_generic_primitive_consumer",
                owner="one-person-lab",
                mag_role="no_runtime_owner_refs_only",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/loop_contracts.py",
                    "src/med_autogrant/product_entry_parts/receipt_observability.py",
                    "src/med_autogrant/product_entry_parts/sidecar.py",
                    "src/med_autogrant/runtime_defaults.py",
                ],
                active_callers=[
                    "product user-loop and status projections",
                    "product sidecar export/dispatch",
                    "runtime defaults for local diagnostic commands",
                ],
                active_caller_status="active_refs_only_no_repo_daemon_owner",
                migration_action=(
                    "OPL should own app workbench, generic scheduler, provider daemon, and "
                    "repair command projection; MAG should expose only action metadata and blockers."
                ),
                retention_reason=(
                    "MAG still needs refs-only user-loop/status projections for direct skill "
                    "and OPL sidecar callers."
                ),
                cannot_absorb_reason=(
                    "The workbench and scheduler can be absorbed; MAG's domain action metadata "
                    "and typed blocker meaning cannot."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/mag_consumer_thinning_contract/consumed_opl_standard_surfaces",
                    "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard",
                ],
                opl_expected_primitives=[
                    "app_workbench_shell",
                    "generic_scheduler",
                    "provider_daemon",
                    "repair_command_projection",
                ],
                mag_retained_authority=["domain_action_metadata", "typed_blocker"],
            ),
        ],
        "mag_owned_grant_authority_surfaces": [
            _build_functional_module_audit_item(
                "grant_lifecycle_stage",
                classification="mag_owned_grant_truth_receipt_verdict",
                owner=TARGET_DOMAIN_ID,
                mag_role="grant_truth_owner",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/runtime_contracts.py",
                    "src/med_autogrant/product_entry_parts/progress.py",
                    "src/med_autogrant/product_entry_parts/owner_receipts.py",
                ],
                active_callers=[
                    "owner receipt contract identity lifecycle_stage",
                    "task lifecycle projection",
                    "stage attempt closeout",
                ],
                active_caller_status="active_mag_authority_keep",
                migration_action="Expose refs to OPL display/routing; do not migrate authority.",
                retention_reason="Grant lifecycle stage is domain truth and gates owner receipts.",
                cannot_absorb_reason=(
                    "OPL generic lifecycle cannot determine grant-stage readiness, critique meaning, "
                    "or package-stage transition validity."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/owner_receipt_contract/identity/lifecycle_stage",
                    "/product_entry_manifest/task_lifecycle",
                ],
                opl_expected_primitives=["display_and_route_only"],
                mag_retained_authority=["lifecycle_stage", "stage_meaning", "owner_receipt"],
            ),
            _build_functional_module_audit_item(
                "fundability_quality_export_verdicts",
                classification="mag_owned_grant_truth_receipt_verdict",
                owner=TARGET_DOMAIN_ID,
                mag_role="verdict_authority_owner",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/manifest_readiness.py",
                    "src/med_autogrant/product_entry_parts/consumer_thinning.py",
                    "src/med_autogrant/final_package_validation.py",
                ],
                active_callers=[
                    "product-entry manifest grant readiness",
                    "thin surface verdict_authority_refs",
                    "submission-ready package validation",
                ],
                active_caller_status="active_mag_verdict_authority_keep",
                migration_action="Expose verdict refs to OPL readiness shell; do not migrate verdict authority.",
                retention_reason="Fundability, authoring quality, and export readiness are grant-review judgments.",
                cannot_absorb_reason=(
                    "OPL can show readiness refs, but cannot make fundability, quality, or export verdicts."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/grant_authoring_readiness",
                    "/product_entry_manifest/mag_consumer_thinning_contract/verdict_authority_refs",
                ],
                opl_expected_primitives=["refs_only_quality_readiness_projection_shell"],
                mag_retained_authority=[
                    "fundability_verdict",
                    "authoring_quality_verdict",
                    "submission_ready_export_verdict",
                ],
            ),
            _build_functional_module_audit_item(
                "package_readiness_submission_ready",
                classification="mag_owned_grant_truth_receipt_verdict",
                owner=TARGET_DOMAIN_ID,
                mag_role="package_authority_owner",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/package_lifecycle_handoff.py",
                    "src/med_autogrant/final_package.py",
                    "src/med_autogrant/final_package_validation.py",
                ],
                active_callers=[
                    "product package-lifecycle-handoff",
                    "package submission-ready",
                    "artifact locator contract",
                ],
                active_caller_status="active_mag_package_authority_keep",
                migration_action=(
                    "Let OPL own artifact/package lifecycle shell; keep submission-ready "
                    "and export gate authority in MAG."
                ),
                retention_reason="Submission-ready is a domain export gate, not generic package existence.",
                cannot_absorb_reason=(
                    "OPL artifact lifecycle can manage refs and retention, but cannot approve a grant package."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/artifact_locator_contract",
                    "package submission-ready",
                ],
                opl_expected_primitives=["artifact_package_lifecycle_shell"],
                mag_retained_authority=[
                    "package_authority",
                    "submission_ready_verdict",
                    "export_gate",
                ],
            ),
            _build_functional_module_audit_item(
                "grant_transition_oracle",
                classification="mag_owned_grant_truth_receipt_verdict",
                owner=TARGET_DOMAIN_ID,
                mag_role="domain_transition_spec_owner",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/functional_closure.py",
                    "src/med_autogrant/product_entry_parts/orchestration_companions.py",
                    "src/med_autogrant/product_entry_parts/consumer_thinning.py",
                ],
                active_callers=[
                    "grant_transition_oracle manifest surface",
                    "family stage control plane",
                    "OPL generic transition runner expected input",
                ],
                active_caller_status="active_domain_oracle_keep_generic_runner_external",
                migration_action=(
                    "OPL should run the generic transition matrix; MAG keeps oracle fixtures "
                    "and grant guard semantics."
                ),
                retention_reason="The oracle encodes grant-specific stage guards and quality/export blockers.",
                cannot_absorb_reason=(
                    "OPL can execute a generic runner, but cannot own the grant transition table's meaning."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/grant_transition_oracle",
                    "/product_entry_manifest/ideal_state_closure_status/mag_owned_transition_oracle",
                ],
                opl_expected_primitives=["generic_transition_runner"],
                mag_retained_authority=[
                    "fundability_guards",
                    "authoring_quality_guards",
                    "package_human_gate_guards",
                ],
            ),
            _build_functional_module_audit_item(
                "owner_receipt_and_no_regression_evidence",
                classification="mag_owned_grant_truth_receipt_verdict",
                owner=TARGET_DOMAIN_ID,
                mag_role="receipt_authority_owner",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/owner_receipts.py",
                    "src/med_autogrant/product_entry_parts/hosted_receipt_verification.py",
                    "src/med_autogrant/product_entry_parts/continuous_reconciliation.py",
                    "src/med_autogrant/product_entry_parts/sidecar.py",
                ],
                active_callers=[
                    "product owner-receipt-evidence",
                    "product hosted-receipt-verification",
                    "product sidecar dispatch stage-attempt/closeout",
                ],
                active_caller_status="active_mag_receipt_authority_keep",
                migration_action=(
                    "OPL should own receipt transport/ledger projection; MAG retains receipt "
                    "authority and no-regression meaning."
                ),
                retention_reason="Owner receipt is the domain authorization boundary for grant mutations.",
                cannot_absorb_reason=(
                    "OPL ledger can store refs, but cannot sign or reinterpret MAG owner receipt."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/owner_receipt_contract",
                    "/product_entry_manifest/controlled_soak_no_regression_attempt",
                ],
                opl_expected_primitives=["receipt_transport_and_ledger_projection"],
                mag_retained_authority=[
                    "domain_owner_receipt",
                    "typed_blocker",
                    "no_regression_evidence",
                ],
            ),
            _build_functional_module_audit_item(
                "grant_memory_accept_reject",
                classification="mag_owned_grant_truth_receipt_verdict",
                owner=TARGET_DOMAIN_ID,
                mag_role="memory_body_decision_owner",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/domain_memory.py",
                    "src/med_autogrant/product_entry_parts/domain_memory_runtime.py",
                    "src/med_autogrant/product_entry_parts/memory_receipt_projection.py",
                    "contracts/runtime-program/domain-memory-seed-fixture.json",
                ],
                active_callers=[
                    "product domain-memory-receipt-evidence",
                    "product memory-receipt-projection",
                    "product sidecar dispatch domain-memory/decide",
                ],
                active_caller_status="active_mag_memory_body_decision_keep",
                migration_action=(
                    "OPL should own body-free memory locator/writeback transport; MAG keeps "
                    "memory body, accept/reject decision, and receipt writer."
                ),
                retention_reason="Grant strategy memory body and accept/reject policy are domain knowledge authority.",
                cannot_absorb_reason=(
                    "OPL can transport refs and writeback proposals, but cannot own memory body "
                    "or accept/reject decisions."
                ),
                current_surface_refs=[
                    "/product_entry_manifest/domain_memory_descriptor_locator",
                    "/product_entry_manifest/controlled_domain_memory_apply_proof",
                ],
                opl_expected_primitives=["memory_locator_writeback_transport"],
                mag_retained_authority=[
                    "grant_strategy_memory_body",
                    "writeback_accept_reject",
                    "memory_receipt_writer",
                ],
            ),
        ],
        "retire_or_tombstone_surfaces": [
            _build_retired_functional_module_audit_item(
                "default_hermes_gateway_local_manager_runtime_owner",
                code_paths=[
                    "src/med_autogrant/upstream_hermes.py",
                    "src/med_autogrant/hermes_native_executor.py",
                    "src/med_autogrant/opl_hermes_executor_helper.py",
                    "src/med_autogrant/product_entry_parts/executor_defaults.py",
                ],
                active_callers=[
                    "explicit hermes_agent proof lane",
                    "optional upstream Hermes session substrate probe",
                ],
                active_caller_status="optional_proof_only_not_default_runtime_owner",
                migration_action=(
                    "Keep as explicit executor/proof provenance only; OPL owns generic executor adapter "
                    "and production provider substrate."
                ),
                retention_reason=(
                    "Optional proof lane still validates non-default executor receipt behavior under MAG guards."
                ),
                cannot_absorb_reason=(
                    "Default runtime ownership must not stay in MAG; optional proof helpers remain only "
                    "because they bind MAG closeout packets to external executor receipts."
                ),
                evidence_refs=[
                    "/product_entry_manifest/controlled_domain_memory_apply_proof/repo_source_layout_audit",
                    "docs/status.md#旧面退役校准",
                ],
            ),
            _build_retired_functional_module_audit_item(
                "domain_runtime_patch_bridge",
                code_paths=[
                    "src/med_autogrant/domain_runtime_parts/patch_targets.py",
                    "src/med_autogrant/domain_runtime.py",
                ],
                active_callers=[],
                active_caller_status="retired_no_active_caller_expected",
                migration_action="Remove or keep only tombstone/provenance; do not add compatibility aliases.",
                retention_reason="No active runtime authority should depend on the patch bridge.",
                cannot_absorb_reason="This is retired compatibility glue, not an OPL primitive to absorb.",
                evidence_refs=[
                    "docs/decisions.md#2026-05-14：退役-domain-runtime-facade-patch-bridge",
                    "src/med_autogrant/domain_runtime_parts/patch_targets.py",
                ],
            ),
            _build_retired_functional_module_audit_item(
                "compatibility_only_product_entry_aggregate_test",
                code_paths=["tests/test_product_entry.py", "tests/product_entry_cases/"],
                active_callers=["focused product_entry_cases tests"],
                active_caller_status="aggregate_removed_focused_cases_active",
                migration_action="Keep focused tests and remove aggregate compatibility assertions.",
                retention_reason="Focused tests protect machine-readable contracts without preserving old facade shape.",
                cannot_absorb_reason="Testing layout is repo-local hygiene, not a generic OPL runtime primitive.",
                evidence_refs=[
                    "tests/test_product_entry.py",
                    "tests/product_entry_cases/",
                ],
            ),
            _build_retired_functional_module_audit_item(
                "legacy_flat_shell_aliases",
                code_paths=[
                    "src/med_autogrant/cli_parts/parser_adders.py",
                    "src/med_autogrant/cli_parts/handlers.py",
                    "src/med_autogrant/public_cli.py",
                ],
                active_callers=["grouped public command tokens"],
                active_caller_status="legacy_alias_retired_grouped_commands_active",
                migration_action="Route callers to grouped product/workspace/pass/package commands.",
                retention_reason="Machine command fields may stay stable, but user-facing flat aliases should not.",
                cannot_absorb_reason="Flat aliases are retired local CLI surface, not a reusable OPL primitive.",
                evidence_refs=[
                    "/product_entry_manifest/ideal_state_closure_status/direct_retirement_posture",
                    "docs/status.md#旧面退役校准",
                ],
            ),
            _build_retired_functional_module_audit_item(
                "repo_owned_scheduler_daemon",
                code_paths=[
                    "src/med_autogrant/runtime_defaults.py",
                    "src/med_autogrant/domain_runtime_parts/substrate.py",
                    "src/med_autogrant/product_entry_parts/runtime_surfaces.py",
                ],
                active_callers=[
                    "runtime run/resume local diagnostic commands",
                    "product-entry runtime_control projection",
                ],
                active_caller_status="no_default_daemon_local_diagnostic_only",
                migration_action=(
                    "OPL should own provider scheduler/daemon; MAG keeps local diagnostic run/resume "
                    "and refs-only runtime_control projection."
                ),
                retention_reason="Local diagnostic commands help direct callers, but are not production daemon ownership.",
                cannot_absorb_reason=(
                    "OPL can absorb production scheduler/daemon; MAG local diagnostics remain scoped to "
                    "workspace validation and grant route checks."
                ),
                evidence_refs=[
                    "/product_entry_manifest/mag_consumer_thinning_contract/forbidden_mag_generic_owner_roles",
                    "/product_entry_manifest/physical_skeleton_follow_through/active_path_scan_no_legacy_default_caller",
                ],
            ),
        ],
        "domain_authority_do_not_retire": [
            "grant_lifecycle_stage",
            "package_readiness_submission_ready",
            "fundability_verdict",
            "authoring_quality_verdict",
            "submission_ready_export_verdict",
            "grant_transition_oracle",
            "owner_receipt",
            "grant_strategy_memory_accept_reject",
        ],
        "opl_must_absorb_code_surfaces": [
            "workspace_source_intake_shell",
            "session_ledger",
            "attention_queue",
            "typed_queue",
            "stage_attempt_ledger",
            "generic_lifecycle_adapter",
            "artifact_package_lifecycle_shell",
            "runtime_observability_export",
            "operator_workbench_shell",
            "generic_scheduler_daemon",
        ],
        "mag_thin_adapter_code_surfaces": [
            "product_entry_manifest_builder",
            "product_sidecar_adapter",
            "domain_entry",
            "receipt_schema_and_writer",
            "grant_transition_oracle",
            "refs_only_projection_builders",
            "focused_contract_tests",
        ],
        "representative_private_functional_surfaces": {
            "local_runtime_journal_attempt_ledger": {
                "module_ref": "session_ledger_attention_queue",
                "active_caller_status": "active_local_journal_and_refs_pending_opl_ledger_absorption",
                "migration_action": (
                    "OPL_absorbs_session_and_attempt_ledger_MAG_keeps_safe_action_refs"
                ),
            },
            "sidecar_dispatch_product_shell": {
                "module_ref": "sidecar_product_status_shell",
                "active_caller_status": "active_domain_sidecar_adapter_not_generic_product_shell",
                "migration_action": (
                    "OPL_absorbs_product_operator_shell_MAG_keeps_guarded_domain_adapter"
                ),
            },
            "optional_hermes_state_db": {
                "module_ref": "default_hermes_gateway_local_manager_runtime_owner",
                "active_caller_status": "optional_proof_only_not_default_runtime_owner",
                "migration_action": (
                    "OPL_owns_generic_executor_adapter_MAG_keeps_explicit_receipt_proof_helper"
                ),
            },
        },
        "audit_refs": {
            "manifest_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
            "sidecar_projection_ref": "/sidecar_export/mag_consumer_thinning_contract",
            "consumer_thinning_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
            "thin_output_guard_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard"
            ),
            "ideal_state_ref": "/product_entry_manifest/ideal_state_closure_status",
        },
        "fail_closed_rules": {
            "delete_grant_lifecycle_stage_as_generic_lifecycle": False,
            "delete_package_readiness_as_generic_package_lifecycle": False,
            "delete_fundability_or_quality_verdict_as_generic_readiness": False,
            "provider_completion_is_grant_ready": False,
            "opl_observability_can_create_verdict": False,
            "mag_can_rebuild_generic_runtime": False,
        },
    }


def _build_functional_module_audit_item(
    module_id: str,
    *,
    classification: str,
    owner: str,
    mag_role: str,
    code_paths: list[str],
    active_callers: list[str],
    active_caller_status: str,
    migration_action: str,
    retention_reason: str,
    cannot_absorb_reason: str,
    current_surface_refs: list[str],
    opl_expected_primitives: list[str],
    mag_retained_authority: list[str],
) -> dict[str, Any]:
    return {
        "module_id": module_id,
        "classification": classification,
        "owner": owner,
        "mag_role": mag_role,
        "code_paths": code_paths,
        "active_callers": active_callers,
        "active_caller_status": active_caller_status,
        "migration_action": migration_action,
        "retention_reason": retention_reason,
        "cannot_absorb_reason": cannot_absorb_reason,
        "current_surface_refs": current_surface_refs,
        "opl_expected_primitives": opl_expected_primitives,
        "mag_retained_authority": mag_retained_authority,
        "implemented_as_generic_runtime_in_mag": False,
        "opl_can_write_grant_truth": False,
        "opl_can_declare_verdict": False,
    }


def _build_retired_functional_module_audit_item(
    module_id: str,
    *,
    code_paths: list[str],
    active_callers: list[str],
    active_caller_status: str,
    migration_action: str,
    retention_reason: str,
    cannot_absorb_reason: str,
    evidence_refs: list[str],
) -> dict[str, Any]:
    return {
        "module_id": module_id,
        "classification": "retire_tombstone",
        "owner": "none_active",
        "state": "retired_or_tombstone_only",
        "code_paths": code_paths,
        "active_callers": active_callers,
        "active_caller_status": active_caller_status,
        "migration_action": migration_action,
        "retention_reason": retention_reason,
        "cannot_absorb_reason": cannot_absorb_reason,
        "evidence_refs": evidence_refs,
        "active_caller_allowed": False,
        "compatibility_alias_allowed": False,
    }
