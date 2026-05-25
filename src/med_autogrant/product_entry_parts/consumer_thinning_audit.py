from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.consumer_thinning_audit_parts import (
    build_retire_or_tombstone_surfaces,
)
from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


def _build_privatized_functional_module_audit() -> dict[str, Any]:
    return {
        "surface_kind": "mag_privatized_functional_module_audit",
        "audit_id": "mag.privatized_functional_module_audit.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "state": "manifest_projected_for_opl_unified_audit",
        "standard_agent_source_shape_status": "landed",
        "mag_repo_active_source_shape_landed": True,
        "claims_descriptor_source_available_for_opl_generation": True,
        "classification_policy": (
            "classify_private_functional_surfaces_as_pack_refs_authority_or_legacy_proof"
        ),
        "opl_unified_audit_read_model": True,
        "claims_generic_runtime_removed_from_mag": False,
        "claims_opl_replacement_exists": True,
        "claims_domain_repo_physical_delete_authorized": False,
        "claims_production_long_run_soak_complete": False,
        "classification_buckets": [
            "declarative_pack_surface",
            "refs_only_adapter",
            "minimal_authority_function",
            "legacy_proof_tombstone",
        ],
        "declarative_pack_surfaces": [
            _build_functional_module_audit_item(
                "runtime_registration",
                classification="declarative_pack_surface",
                owner=TARGET_DOMAIN_ID,
                mag_role="domain_descriptor_pack_input",
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
                active_caller_status="active_declarative_pack_projection",
                migration_action=(
                    "Express as declarative grant pack metadata; OPL generated registry surfaces "
                    "consume refs without MAG owning generic runtime registration."
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
                classification="declarative_pack_surface",
                owner=TARGET_DOMAIN_ID,
                mag_role="grant_stage_pack_and_checkpoint_semantics",
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
                active_caller_status="active_declarative_stage_pack_projection",
                migration_action=(
                    "Move generic checkpoint/lifecycle shell to generated OPL surfaces; keep MAG "
                    "stage ids and checkpoint semantics in the declarative grant pack."
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
                "source_intake_shell",
                classification="declarative_pack_surface",
                owner=TARGET_DOMAIN_ID,
                mag_role="funding_call_task_lock_pack_input",
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
                active_caller_status="active_declarative_source_requirements_pack_projection",
                migration_action=(
                    "Represent funding-call/task-lock requirements as declarative pack inputs; "
                    "OPL owns source transport, freshness, and repair shell."
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
        ],
        "refs_only_adapter_surfaces": [
            _build_functional_module_audit_item(
                "lifecycle_adapter",
                classification="refs_only_adapter",
                owner=TARGET_DOMAIN_ID,
                mag_role="guarded_receipt_refs_adapter",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/lifecycle_receipt_bundle.py",
                    "src/med_autogrant/product_entry_parts/owner_receipt_writers.py",
                    "src/med_autogrant/product_entry_parts/owner_receipt_reconciliation.py",
                    "src/med_autogrant/product_entry_parts/continuous_reconciliation.py",
                    "src/med_autogrant/product_entry_parts/runtime_registration.py",
                ],
                active_callers=[
                    "product lifecycle-receipt-evidence",
                    "product lifecycle-receipt-bundle",
                    "product sidecar dispatch lifecycle/receipt",
                ],
                active_caller_status="active_refs_only_adapter_no_generic_lifecycle_owner",
                migration_action=(
                    "Keep only owner receipt/blocker refs for OPL lifecycle shell; do not expose "
                    "MAG package body, memory body, or lifecycle state."
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
                classification="refs_only_adapter",
                owner=TARGET_DOMAIN_ID,
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
                active_caller_status="active_refs_only_observability_adapter_no_repair_execution",
                migration_action=(
                    "Expose refs, counts, blockers, and verdict refs only; OPL owns display, SLO, "
                    "repair projection, and workbench shell."
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
                classification="refs_only_adapter",
                owner=TARGET_DOMAIN_ID,
                mag_role="guarded_domain_sidecar_refs_adapter",
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
                active_caller_status="active_refs_only_domain_sidecar_adapter",
                migration_action=(
                    "Keep guarded domain dispatch and sidecar refs; OPL generated surfaces own "
                    "product/operator/action-routing shell."
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
                    "product_status",
                    "status_read_model",
                    "sidecar_export_dispatch",
                    "workbench_drilldown",
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
                classification="refs_only_adapter",
                owner=TARGET_DOMAIN_ID,
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
                active_caller_status="active_refs_only_package_authority_adapter",
                migration_action=(
                    "Expose package refs, gap refs, and verdict refs only; OPL owns lifecycle shell, "
                    "restore/retention ledger, and package refs index."
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
                "human_workbench_scheduler_daemon",
                classification="refs_only_adapter",
                owner=TARGET_DOMAIN_ID,
                mag_role="action_metadata_and_blocker_refs_only",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/loop_contracts.py",
                    "src/med_autogrant/product_entry_parts/receipt_observability.py",
                    "src/med_autogrant/product_entry_parts/sidecar.py",
                    "src/med_autogrant/runtime_defaults.py",
                ],
                active_callers=[
                    "product user-loop and status refs projections",
                    "product sidecar export/dispatch",
                    "executor default metadata for OPL adapter refs",
                ],
                active_caller_status="active_refs_only_no_repo_daemon_owner",
                migration_action=(
                    "Expose action metadata and typed blockers only; OPL owns app workbench, generic "
                    "scheduler, provider daemon, and repair command projection."
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
                    "cli",
                    "mcp",
                    "skill",
                    "product_entry",
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
                classification="minimal_authority_function",
                owner=TARGET_DOMAIN_ID,
                mag_role="grant_truth_owner",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/runtime_contracts.py",
                    "src/med_autogrant/product_entry_parts/progress.py",
                    "src/med_autogrant/product_entry_parts/owner_receipt_writers.py",
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
                classification="minimal_authority_function",
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
                classification="minimal_authority_function",
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
                classification="minimal_authority_function",
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
                classification="minimal_authority_function",
                owner=TARGET_DOMAIN_ID,
                mag_role="receipt_authority_owner",
                code_paths=[
                    "src/med_autogrant/product_entry_parts/owner_receipt_writers.py",
                    "src/med_autogrant/product_entry_parts/owner_receipt_reconciliation.py",
                    "src/med_autogrant/product_entry_parts/production_live_acceptance.py",
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
                classification="minimal_authority_function",
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
        "retire_or_tombstone_surfaces": build_retire_or_tombstone_surfaces(
            build_retired_functional_module_audit_item=(
                _build_retired_functional_module_audit_item
            ),
            build_legacy_exit_gate=_build_legacy_exit_gate,
        ),
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
            "product_sidecar_guarded_domain_adapter",
            "domain_entry",
            "receipt_schema_and_writer",
            "grant_transition_oracle",
            "refs_only_projection_builders",
            "focused_contract_tests",
        ],
        "representative_private_functional_surfaces": {
            "local_runtime_journal_attempt_ledger": {
                "module_ref": "local_runtime_journal_attempt_ledger",
                "active_caller_status": "legacy_local_journal_attempt_ledger_absent_no_active_caller",
                "migration_action": (
                    "OPL_owns_session_attempt_ledger_MAG_deleted_local_journal_code"
                ),
            },
            "sidecar_dispatch_product_shell": {
                "module_ref": "sidecar_product_status_shell",
                "active_caller_status": "active_refs_only_domain_sidecar_adapter",
                "migration_action": (
                    "OPL_generates_product_operator_shell_and_generic_dispatch_actions_"
                    "MAG_keeps_guarded_domain_adapter_refs"
                ),
            },
            "optional_hermes_state_db": {
                "module_ref": "default_hermes_gateway_local_manager_runtime_owner",
                "active_caller_status": (
                    "legacy_runtime_owner_absent_executor_adapter_metadata_only"
                ),
                "migration_action": (
                    "OPL_owns_generic_executor_adapter_MAG_deleted_legacy_runtime_probe"
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
            "generated_surface_bridge_exit_gate_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff/bridge_exit_gate"
            ),
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
    bridge_exit_gate = _build_default_caller_deletion_bridge_exit_gate(
        module_id=module_id,
        classification=classification,
        current_surface_refs=current_surface_refs,
        mag_retained_authority=mag_retained_authority,
    )
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
        "bridge_exit_gate": bridge_exit_gate,
        "implemented_as_generic_runtime_in_mag": False,
        "opl_can_write_grant_truth": False,
        "opl_can_declare_verdict": False,
    }


def _build_default_caller_deletion_bridge_exit_gate(
    *,
    module_id: str,
    classification: str,
    current_surface_refs: list[str],
    mag_retained_authority: list[str],
) -> dict[str, Any]:
    is_authority = classification == "minimal_authority_function"
    return {
        "surface_kind": "mag_default_caller_deletion_bridge_exit_gate",
        "gate_id": f"mag.default_caller_deletion.{module_id}.bridge_exit.v1",
        "bridge_owner": "med-autogrant",
        "replacement_owner": "one-person-lab",
        "current_status": (
            "retained_mag_authority"
            if is_authority
            else "bridge_until_explicit_owner_receipt_authorizes_physical_delete"
        ),
        "required_before_retire": [] if is_authority else [
            "domain_authority_refs_preserved",
            "no_forbidden_write_proof_recorded",
            "explicit_owner_receipt_authorizes_physical_delete",
        ],
        "current_surface_refs": list(current_surface_refs),
        "retained_mag_authority": list(mag_retained_authority),
        "default_caller_deletion_evidence_scope": (
            "domain_owned_typed_blocker_and_no_forbidden_write_refs_only_no_physical_delete_authorization"
        ),
        "typed_blocker_refs": [
            (
                "typed-blocker:mag/default-caller-deletion/"
                f"{module_id}/physical-delete-requires-explicit-owner-receipt"
            )
        ],
        "no_forbidden_write_refs": [
            f"no-forbidden-write:mag/default-caller-deletion/{module_id}/refs-only-boundary"
        ],
        "no_forbidden_write_evidence_refs": [
            f"no-forbidden-write:mag/default-caller-deletion/{module_id}/refs-only-boundary"
        ],
        "provenance_refs": list(current_surface_refs),
        "domain_repo_physical_delete_authorized": False,
        "physical_delete_authorized_by_refs": False,
        "mag_can_write_generic_runtime": False,
        "mag_can_own_generated_default_caller": False,
        "opl_can_write_grant_truth": False,
        "opl_can_declare_fundability_or_export_verdict": False,
        "opl_can_issue_mag_owner_receipt": False,
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
    exit_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "module_id": module_id,
        "classification": "legacy_proof_tombstone",
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
    if exit_gate is not None:
        payload["exit_gate"] = exit_gate
    return payload


def _build_legacy_exit_gate(
    *,
    gate_id: str,
    replacement_primitives: list[str],
    exit_action: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_legacy_surface_exit_gate",
        "gate_id": gate_id,
        "gate_status": "mag_handler_boundary_ready_external_caller_evidence_required",
        "replacement_owner": "one-person-lab",
        "replacement_primitives": replacement_primitives,
        "required_evidence": [
            "no_active_caller_scan",
            "replacement_surface_consumes_mag_refs",
            "direct_mag_domain_handler_no_regression",
            "history_or_tombstone_ref",
        ],
        "satisfied_evidence_refs": {
            "no_active_caller_scan": (
                "/product_entry_manifest/physical_skeleton_follow_through/"
                "active_path_scan_no_legacy_default_caller"
            ),
            "replacement_surface_consumes_mag_refs": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff"
            ),
            "direct_mag_domain_handler_no_regression": (
                "tests/product_entry_cases/test_sidecar.py"
            ),
            "history_or_tombstone_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "privatized_functional_module_audit"
            ),
        },
        "exit_action": exit_action,
        "claims_exit_complete": False,
        "claims_production_long_run_soak_complete": False,
        "mag_handler_boundary_ready": True,
        "external_opl_generated_or_hosted_caller_evidence_required": True,
        "authority_boundary": {
            "mag_can_keep_compatibility_alias": False,
            "mag_can_keep_generic_runtime_owner": False,
            "mag_keeps_safe_action_refs": True,
            "opl_can_write_grant_truth": False,
            "opl_can_declare_verdict": False,
        },
    }
