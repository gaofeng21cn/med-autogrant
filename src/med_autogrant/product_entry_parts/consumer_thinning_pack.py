from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID

REPO_ROOT = Path(__file__).resolve().parents[3]

MAG_MINIMAL_AUTHORITY_FUNCTION_IDS = (
    "fundability_verdict",
    "quality_verdict",
    "export_verdict",
    "package_authority",
    "memory_accept_reject",
    "owner_receipt_signer",
    "grant_helper",
)

AI_FIRST_AUTHORITY_SURFACE_IDS = (
    "fundability_verdict",
    "quality_verdict",
    "export_verdict",
    "memory_accept_reject",
)

PROGRAMMATIC_AUTHORITY_SURFACE_IDS = (
    "package_authority",
    "owner_receipt_signer",
    "grant_helper",
)

GENERATED_OR_BRIDGE_SURFACE_IDS = (
    "product_status",
    "product_user_loop",
    "product_sidecar",
    "grouped_cli_api",
    "projection_builder",
    "lifecycle_wrapper",
)

GENERATED_SURFACE_BRIDGE_EXIT_EVIDENCE = (
    "opl_generated_or_hosted_caller_consumes_mag_pack_input",
    "direct_mag_domain_handler_no_regression",
    "owner_receipt_or_typed_blocker_ref_roundtrip",
    "no_forbidden_write_proof",
    "no_active_legacy_wrapper_caller_scan",
)

GENERATED_SURFACE_BRIDGE_EXIT_EVIDENCE_REFS = {
    "opl_generated_or_hosted_caller_consumes_mag_pack_input": [
        "contracts/generated_surface_handoff.json",
        "tests/test_opl_standard_pack.py::test_opl_generated_interfaces_compile_mag_standard_pack",
        "tests/test_opl_standard_pack.py::test_opl_standard_scaffold_validates_mag_pack",
    ],
    "direct_mag_domain_handler_no_regression": [
        "tests/product_entry_cases/test_manifest_and_status.py",
        "tests/product_entry_cases/test_sidecar.py",
        "tests/product_entry_cases/test_functional_closure.py",
    ],
    "owner_receipt_or_typed_blocker_ref_roundtrip": [
        "/product_entry_manifest/owner_receipt_contract",
        "/product_entry_manifest/controlled_stage_attempt_projection",
        "tests/product_entry_cases/test_functional_closure.py::"
        "ProductEntryFunctionalClosureTest::test_owner_receipt_evidence_writer_persists_no_regression_receipt_without_domain_writes",
    ],
    "no_forbidden_write_proof": [
        "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard",
        "/product_entry_manifest/physical_skeleton_follow_through/active_path_scan_no_legacy_default_caller",
    ],
    "no_active_legacy_wrapper_caller_scan": [
        "/product_entry_manifest/physical_skeleton_follow_through/active_path_scan_no_legacy_default_caller",
        "tests/test_domain_entry.py::DomainEntryDispatchTest::test_domain_entry_rejects_retired_runtime_commands",
        "tests/test_domain_runtime.py::MagRuntimeCliDispatchTest::test_runtime_run_public_cli_is_retired",
    ],
}

EXTERNAL_EVIDENCE_REQUEST_IDS = (
    "opl_generated_hosted_caller_pack_consumption",
    "app_workbench_package_ref_consumption",
    "production_default_caller_release_dist_consumption",
    "owner_receipt_typed_blocker_ref_roundtrip",
    "continuous_no_forbidden_write_guard",
    "direct_hosted_parity_no_regression",
    "temporal_provider_long_soak_receipt_reconciliation",
)


def build_external_evidence_request_pack() -> dict[str, Any]:
    return {
        "surface_kind": "mag_external_evidence_request_pack",
        "request_pack_id": "mag.external_evidence_request_pack.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "request_owner": TARGET_DOMAIN_ID,
        "requested_from": ["one-person-lab", "codex_app", "production_caller"],
        "state": "request_pack_declared_external_evidence_not_claimed",
        "policy": "request_refs_receipt_shapes_and_parity_only_no_runtime_implementation",
        "plan_ref": "docs/active/mag-ideal-state-cross-repo-gap-plan.md",
        "consumer_thinning_contract_ref": "/product_entry_manifest/mag_consumer_thinning_contract",
        "sidecar_projection_ref": "/sidecar_export/external_evidence_request_pack",
        "required_request_ids": list(EXTERNAL_EVIDENCE_REQUEST_IDS),
        "requests": [
            _external_evidence_request(
                "opl_generated_hosted_caller_pack_consumption",
                requested_from="one-person-lab",
                evidence_class="generated_hosted_caller_consumption",
                required_refs=[
                    "opl://generated-surfaces/mag/product-entry-manifest",
                    "opl://generated-surfaces/mag/product-sidecar",
                    "/product_entry_manifest/mag_consumer_thinning_contract/declarative_grant_pack_compiler_input",
                    "/product_entry_manifest/mag_consumer_thinning_contract/generated_surface_handoff",
                ],
                required_receipt_shapes=[
                    "opl_generated_interface_compile_receipt",
                    "opl_hosted_domain_handler_call_receipt",
                ],
            ),
            _external_evidence_request(
                "app_workbench_package_ref_consumption",
                requested_from="codex_app",
                evidence_class="app_workbench_refs_consumption",
                required_refs=[
                    "/product_entry_manifest/artifact_locator_contract",
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                    "/product_entry_manifest/grant_transition_oracle",
                    "/product_entry_manifest/owner_receipt_contract",
                ],
                required_receipt_shapes=[
                    "app_consumed_package_ref_receipt",
                    "app_consumed_quality_ref_receipt",
                    "app_consumed_safe_action_ref_receipt",
                ],
            ),
            _external_evidence_request(
                "production_default_caller_release_dist_consumption",
                requested_from="production_caller",
                evidence_class="external_default_caller_consumption",
                required_refs=[
                    "release://med-autogrant/direct-domain-handler",
                    "dist://med-autogrant/declarative-grant-pack",
                    "/product_entry_manifest/mag_consumer_thinning_contract/exposed_sidecar_return_refs",
                ],
                required_receipt_shapes=[
                    "production_default_caller_receipt",
                    "release_dist_consumption_receipt",
                ],
            ),
            _external_evidence_request(
                "owner_receipt_typed_blocker_ref_roundtrip",
                requested_from="one-person-lab",
                evidence_class="receipt_shape_roundtrip",
                required_refs=[
                    "/product_entry_manifest/owner_receipt_contract",
                    "/product_entry_manifest/controlled_stage_attempt_projection",
                    "/product_entry_manifest/mag_consumer_thinning_contract/allowed_return_shapes",
                ],
                required_receipt_shapes=[
                    "domain_owner_receipt",
                    "typed_blocker",
                    "no_regression_evidence",
                ],
            ),
            _external_evidence_request(
                "continuous_no_forbidden_write_guard",
                requested_from="production_caller",
                evidence_class="continuous_no_forbidden_write",
                required_refs=[
                    "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard",
                    "/product_entry_manifest/physical_skeleton_follow_through/active_path_scan_no_legacy_default_caller",
                ],
                required_receipt_shapes=[
                    "no_forbidden_write_scan_receipt",
                    "continuous_guard_snapshot_receipt",
                ],
            ),
            _external_evidence_request(
                "direct_hosted_parity_no_regression",
                requested_from="one-person-lab",
                evidence_class="direct_hosted_parity",
                required_refs=[
                    "/product_entry_manifest/mag_consumer_thinning_contract/generated_surface_handoff/bridge_exit_gate",
                    "/product_entry_manifest/owner_receipt_contract",
                    "/product_entry_manifest/grant_transition_oracle",
                ],
                required_receipt_shapes=[
                    "direct_hosted_parity_receipt",
                    "direct_mag_domain_handler_no_regression_receipt",
                ],
            ),
            _external_evidence_request(
                "temporal_provider_long_soak_receipt_reconciliation",
                requested_from="one-person-lab",
                evidence_class="long_soak_receipt_reconciliation",
                required_refs=[
                    "opl://runtime/temporal-provider/long-soak",
                    "/product_entry_manifest/controlled_stage_attempt_projection",
                    "/product_entry_manifest/controlled_domain_memory_apply_proof",
                    "/product_entry_manifest/lifecycle_guarded_apply_proof",
                ],
                required_receipt_shapes=[
                    "temporal_provider_long_soak_receipt",
                    "continuous_receipt_reconciliation_snapshot",
                    "repair_cadence_evidence_receipt",
                ],
            ),
        ],
        "required_refs_summary": {
            "mag_request_surface_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "external_evidence_request_pack"
            ),
            "sidecar_projection_ref": "/sidecar_export/external_evidence_request_pack",
            "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
            "thin_output_guard_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "thin_surface_output_guard"
            ),
            "direct_hosted_parity_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "external_evidence_request_pack/requests/direct_hosted_parity_no_regression"
            ),
        },
        "forbidden_completion_claims": {
            "provider_completion_is_fundability_ready": False,
            "provider_completion_is_quality_ready": False,
            "provider_completion_is_export_ready": False,
            "provider_completion_is_submission_ready": False,
            "claims_opl_replacement_exists": False,
            "claims_all_bridge_exits_complete": False,
            "claims_production_soak_complete": False,
            "claims_production_long_run_soak_complete": False,
        },
        "authority_boundary": {
            "mag_request_pack_only": True,
            "mag_implements_opl_runtime": False,
            "mag_implements_app_workbench": False,
            "mag_claims_external_evidence_exists": False,
            "mag_claims_production_default_caller_migrated": False,
            "mag_claims_direct_hosted_parity_passed": False,
            "mag_claims_long_soak_complete": False,
            "opl_can_write_grant_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_mutate_grant_artifacts": False,
            "opl_can_declare_fundability_verdict": False,
            "opl_can_declare_quality_verdict": False,
            "opl_can_declare_export_verdict": False,
        },
    }


def build_generated_hosted_default_caller_proof() -> dict[str, Any]:
    return {
        "surface_kind": "mag_generated_hosted_default_caller_proof",
        "proof_id": "mag.generated_hosted_default_caller.proof.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "active_default_caller": "mag_domain_handler_until_opl_generated_hosted_default_caller_evidence",
        "target_default_caller": "opl_generated_or_hosted_product_shell",
        "current_mag_role": "domain_handler_ref_only_adapter_and_migration_input",
        "default_caller_cutover_state": "mag_handler_boundary_ready_external_default_caller_evidence_gated",
        "generated_surface_handoff_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/generated_surface_handoff"
        ),
        "external_evidence_request_pack_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/external_evidence_request_pack"
        ),
        "direct_hosted_parity_workorder": {
            "workorder_id": "mag.direct_hosted_parity.workorder.v1",
            "required_request_id": "direct_hosted_parity_no_regression",
            "required_receipt_shapes": [
                "direct_hosted_parity_receipt",
                "direct_mag_domain_handler_no_regression_receipt",
            ],
            "direct_surface_refs": [
                "/product_entry_manifest/product_entry_surface",
                "/product_entry_manifest/operator_loop_surface",
                "/product_entry_manifest/mag_consumer_thinning_contract/generated_surface_handoff",
            ],
            "hosted_surface_refs": [
                "opl://generated-surfaces/mag/product-entry-manifest",
                "opl://generated-surfaces/mag/product-sidecar",
                "opl://generated-surfaces/mag/product-entry-session#resume",
            ],
            "parity_owner": "one-person-lab",
            "mag_role": "domain_handler_target_and_refs_only_oracle",
            "claims_parity_passed": False,
        },
        "no_forbidden_write_boundary": {
            "boundary_id": "mag.generated_hosted_default_caller.no_forbidden_write.v1",
            "required_request_id": "continuous_no_forbidden_write_guard",
            "thin_surface_output_guard_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard"
            ),
            "forbidden_payload_classes": [
                "grant_artifact_content",
                "memory_body",
                "workspace_private_evidence_body",
                "opl_runtime_state_body",
                "app_workbench_state_body",
            ],
            "forbidden_write_targets": [
                "grant_truth",
                "memory_body",
                "grant_artifact_body",
                "fundability_verdict_body",
                "quality_verdict_body",
                "export_verdict_body",
                "owner_receipt_instance_repo_source",
            ],
            "mag_repo_source_write_allowed": [
                "contracts",
                "schemas",
                "domain_handler_code",
                "refs_only_read_models",
                "tests",
                "docs",
            ],
            "runtime_receipt_write_policy": "runtime_store_only_no_repo_source_receipt_instances",
            "claims_no_forbidden_write_passed": False,
        },
        "repo_local_product_shell_classification": {
            "product_status": "domain_handler_ref_only_adapter",
            "product_user_loop": "domain_handler_ref_only_adapter",
            "product_sidecar": "guarded_domain_handler_target",
            "grouped_cli_api": "domain_handler_command_adapter",
            "projection_builder": "refs_only_read_model_adapter",
            "lifecycle_wrapper": "owner_receipt_refs_only_adapter",
            "generic_runtime_owner": False,
            "migration_input": True,
        },
        "authority_boundary": {
            "mag_domain_handler_owner": TARGET_DOMAIN_ID,
            "target_generated_caller_owner": "one-person-lab",
            "mag_owns_generic_runtime": False,
            "mag_owns_app_workbench": False,
            "mag_claims_default_caller_cutover_complete": False,
            "mag_claims_direct_hosted_parity_passed": False,
            "mag_claims_no_forbidden_write_passed": False,
            "opl_generated_caller_can_write_grant_truth": False,
            "opl_generated_caller_can_write_memory_body": False,
            "opl_generated_caller_can_mutate_grant_artifacts": False,
            "opl_generated_caller_can_declare_fundability_verdict": False,
            "opl_generated_caller_can_declare_quality_verdict": False,
            "opl_generated_caller_can_declare_export_verdict": False,
            "opl_generated_caller_can_sign_owner_receipt": False,
        },
    }


def _external_evidence_request(
    request_id: str,
    *,
    requested_from: str,
    evidence_class: str,
    required_refs: list[str],
    required_receipt_shapes: list[str],
) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "requested_from": requested_from,
        "evidence_class": evidence_class,
        "state": "requested_not_received",
        "required_refs": required_refs,
        "required_receipt_shapes": required_receipt_shapes,
        "mag_role": "requester_and_contract_owner_only",
        "evidence_not_claimed_by_mag_repo": True,
        "accepted_payload_policy": "refs_receipts_and_shape_metadata_only",
        "forbidden_payload_classes": [
            "grant_artifact_content",
            "memory_body",
            "workspace_private_evidence_body",
            "opl_runtime_state_body",
            "app_workbench_state_body",
        ],
    }


def build_mag_minimal_authority_functions() -> list[dict[str, Any]]:
    return [
        _authority_function(
            "fundability_verdict",
            authority_output_class="verdict_refs",
            work_mode="ai_first_domain_judgment_surface",
            judgment_owner="ai_first_grant_review_or_fundability_stage_artifact",
            programmatic_role="validator_and_verdict_ref_materializer",
            ai_stage_artifact_required=True,
            allowed_return_shapes=["verdict_refs", "typed_blocker", "domain_owner_receipt"],
            source_refs=[
                "/product_entry_manifest/family_stage_control_plane/stages",
                "/product_entry_manifest/grant_transition_oracle",
            ],
            cannot_generate_reason="Fundability is a grant-review judgment over call fit and applicant evidence.",
            ai_first_guard=(
                "fundability must be backed by a grant-review or fundability stage artifact; "
                "schema completeness or OPL provider completion cannot set this verdict"
            ),
        ),
        _authority_function(
            "quality_verdict",
            authority_output_class="verdict_refs",
            work_mode="ai_first_domain_judgment_surface",
            judgment_owner="ai_authored_critique_or_quality_closure_artifact",
            programmatic_role="critique_artifact_aggregator_and_guard",
            ai_stage_artifact_required=True,
            allowed_return_shapes=["verdict_refs", "typed_blocker", "domain_owner_receipt"],
            source_refs=[
                "/product_entry_manifest/grant_authoring_readiness",
                "/product_entry_manifest/controlled_stage_attempt_projection",
            ],
            cannot_generate_reason="Authoring quality requires MAG-owned AI critique and issue closure semantics.",
            ai_first_guard=(
                "quality must be backed by an AI-authored critique, quality closure dossier, "
                "or reviewer artifact; numeric scorecards cannot independently declare ready"
            ),
        ),
        _authority_function(
            "export_verdict",
            authority_output_class="verdict_refs",
            work_mode="ai_first_domain_judgment_surface",
            judgment_owner="ai_or_owner_backed_package_export_stage_artifact",
            programmatic_role="export_stage_ref_validator_and_blocker",
            ai_stage_artifact_required=True,
            allowed_return_shapes=["verdict_refs", "typed_blocker", "domain_owner_receipt"],
            source_refs=[
                "package submission-ready",
                "/product_entry_manifest/artifact_locator_contract",
            ],
            cannot_generate_reason="Submission/export readiness is a grant package gate, not package existence.",
            ai_first_guard=(
                "export readiness must trace to MAG package/export stage authority; "
                "artifact presence or generic lifecycle completion cannot declare submission-ready"
            ),
        ),
        _authority_function(
            "package_authority",
            authority_output_class="grant_owned_refs",
            work_mode="programmatic_authority_guard_surface",
            judgment_owner="mag_owner_receipt_or_package_stage_authority",
            programmatic_role="package_materializer_and_owner_receipt_guard",
            ai_stage_artifact_required=False,
            allowed_return_shapes=["domain_owner_receipt", "typed_blocker", "grant_owned_refs"],
            source_refs=[
                "/product_entry_manifest/artifact_locator_contract",
                "/product_entry_manifest/lifecycle_guarded_apply_proof",
            ],
            cannot_generate_reason="Grant package mutation and release require MAG package authority.",
            ai_first_guard=(
                "package mutation requires MAG owner receipt tied to the grant package stage; "
                "OPL artifact lifecycle may only carry refs and receipts"
            ),
        ),
        _authority_function(
            "memory_accept_reject",
            authority_output_class="owner_receipt",
            work_mode="ai_first_domain_judgment_surface",
            judgment_owner="ai_first_grant_strategy_memory_stage_artifact",
            programmatic_role="memory_receipt_writer_and_refs_projection",
            ai_stage_artifact_required=True,
            allowed_return_shapes=["domain_owner_receipt", "typed_blocker", "ref"],
            source_refs=[
                "/product_entry_manifest/domain_memory_descriptor_locator",
                "/product_entry_manifest/controlled_domain_memory_apply_proof",
            ],
            cannot_generate_reason="Grant strategy memory body and accept/reject decisions are MAG authority.",
            ai_first_guard=(
                "memory accept/reject must be a grant-strategy decision over domain memory meaning; "
                "OPL memory transport can only carry body-free refs and writeback proposals"
            ),
        ),
        _authority_function(
            "owner_receipt_signer",
            authority_output_class="owner_receipt",
            work_mode="programmatic_authority_guard_surface",
            judgment_owner="mag_owner_receipt_schema_and_domain_provenance",
            programmatic_role="receipt_schema_signer_and_blocker_guard",
            ai_stage_artifact_required=False,
            allowed_return_shapes=["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
            source_refs=[
                "/product_entry_manifest/owner_receipt_contract",
                "/product_entry_manifest/controlled_soak_no_regression_attempt",
            ],
            cannot_generate_reason="Only MAG can sign domain owner receipts or no-regression evidence.",
            ai_first_guard=(
                "owner receipts can sign only MAG domain receipts, typed blockers, safe action refs, "
                "or no-regression evidence; they cannot create grant verdicts from runtime state"
            ),
        ),
        _authority_function(
            "grant_helper",
            authority_output_class="domain_action_metadata",
            work_mode="programmatic_authority_guard_surface",
            judgment_owner="deterministic_grant_metadata_route_and_blocker_policy",
            programmatic_role="grant_metadata_route_blocker_helper",
            ai_stage_artifact_required=False,
            allowed_return_shapes=["domain_action_metadata", "typed_blocker", "ref"],
            source_refs=[
                "/product_entry_manifest/family_action_catalog",
                "/product_entry_manifest/grant_transition_oracle",
            ],
            cannot_generate_reason="Grant-native helpers encode funder, route, and blocker semantics.",
            ai_first_guard=(
                "grant helpers may validate funder, route, blocker, and action metadata only; "
                "they cannot bypass grant-stage AI review or owner receipt authority"
            ),
        ),
    ]


def build_mag_minimal_authority_surface_taxonomy() -> dict[str, Any]:
    return {
        "surface_kind": "mag_minimal_authority_surface_taxonomy",
        "taxonomy_id": "mag.minimal_authority_surface_taxonomy.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "legacy_function_id_compatibility": True,
        "ai_first_judgment_surface_ids": list(AI_FIRST_AUTHORITY_SURFACE_IDS),
        "programmatic_authority_surface_ids": list(PROGRAMMATIC_AUTHORITY_SURFACE_IDS),
        "all_surface_ids": list(MAG_MINIMAL_AUTHORITY_FUNCTION_IDS),
        "policy": (
            "verdict_and_memory_surfaces_materialize_refs_from_ai_first_stage_artifacts; "
            "programmatic_surfaces_sign_receipts_or_validate_refs_only"
        ),
        "mechanical_decision_forbidden_for_all_surfaces": True,
        "programmatic_verdict_generation_allowed": False,
    }


def build_declarative_grant_pack_compiler_input() -> dict[str, Any]:
    return {
        "surface_kind": "mag_declarative_grant_pack_compiler_input",
        "compiler_input_id": "mag.declarative_grant_pack.compiler_input.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "pack_owner": TARGET_DOMAIN_ID,
        "compiler_owner": "one-person-lab",
        "state": "ready_for_opl_pack_compiler_ingest",
        "input_policy": "declarative_refs_and_authority_manifest_only",
        "generated_surface_handoff_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/generated_surface_handoff"
        ),
        "minimal_authority_functions_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/minimal_authority_functions"
        ),
        "minimal_authority_surface_taxonomy_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/minimal_authority_surface_taxonomy"
        ),
        "source_refs": {
            "stage_graph_ref": "/product_entry_manifest/family_stage_control_plane",
            "action_metadata_ref": "/product_entry_manifest/family_action_catalog",
            "transition_oracle_ref": "/product_entry_manifest/grant_transition_oracle",
            "receipt_schema_ref": "/product_entry_manifest/owner_receipt_contract",
            "memory_policy_ref": "/product_entry_manifest/domain_memory_descriptor_locator",
            "artifact_locator_ref": "/product_entry_manifest/artifact_locator_contract",
            "lifecycle_policy_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
            "output_guard_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/thin_surface_output_guard"
            ),
        },
        "pack_sections": [
            "stage_graph",
            "action_metadata",
            "transition_oracle",
            "receipt_schema",
            "memory_policy",
            "artifact_locator",
            "authority_function_manifest",
        ],
        "generated_surface_targets": list(GENERATED_OR_BRIDGE_SURFACE_IDS),
        "forbidden_payload_classes": [
            "grant_artifact_content",
            "memory_body",
            "workspace_private_evidence",
            "generic_runtime_state",
            "generic_workbench_state",
            "generic_lifecycle_ledger",
        ],
        "authority_boundary": {
            "mag_pack_owner": TARGET_DOMAIN_ID,
            "opl_compiler_owner": "one-person-lab",
            "opl_can_generate_product_status": True,
            "opl_can_generate_user_loop": True,
            "opl_can_generate_sidecar_wrapper": True,
            "opl_can_generate_grouped_cli_api": True,
            "opl_can_generate_projection_wrapper": True,
            "opl_can_generate_lifecycle_wrapper": True,
            "opl_can_write_grant_truth": False,
            "opl_can_write_memory_body": False,
            "opl_can_sign_owner_receipt": False,
            "opl_can_declare_fundability_verdict": False,
            "opl_can_declare_quality_verdict": False,
            "opl_can_declare_export_verdict": False,
        },
    }


def build_generated_surface_handoff() -> dict[str, Any]:
    generated_surfaces = [
        _generated_surface(
            "product_status",
            current_mag_paths=["src/med_autogrant/product_entry_parts/manifest.py"],
            input_refs=[
                "/product_entry_manifest/product_entry_status",
                "/product_entry_manifest/grant_authoring_readiness",
            ],
        ),
        _generated_surface(
            "product_user_loop",
            current_mag_paths=[
                "src/med_autogrant/product_entry_parts/loop_contracts.py",
                "src/med_autogrant/product_entry_parts/entry.py",
            ],
            input_refs=[
                "/product_entry_manifest/operator_loop_surface",
                "/product_entry_manifest/operator_loop_actions",
            ],
        ),
        _generated_surface(
            "product_sidecar",
            current_mag_paths=["src/med_autogrant/product_entry_parts/sidecar.py"],
            input_refs=[
                "/product_entry_manifest/runtime_control",
                "/product_entry_manifest/mag_consumer_thinning_contract",
            ],
        ),
        _generated_surface(
            "grouped_cli_api",
            current_mag_paths=[
                "src/med_autogrant/cli_parts/parser_adders.py",
                "src/med_autogrant/cli_parts/handlers.py",
                "src/med_autogrant/public_cli.py",
            ],
            input_refs=[
                "/product_entry_manifest/family_action_catalog",
                "/product_entry_manifest/product_entry_shell",
            ],
        ),
        _generated_surface(
            "projection_builder",
            current_mag_paths=[
                "src/med_autogrant/product_entry_parts/progress.py",
                "src/med_autogrant/product_entry_parts/manifest_builder.py",
                "src/med_autogrant/product_entry_parts/receipt_observability.py",
            ],
            input_refs=[
                "/product_entry_manifest/progress_projection",
                "/product_entry_manifest/artifact_inventory",
                "/product_entry_manifest/controlled_stage_attempt_projection",
            ],
        ),
        _generated_surface(
            "lifecycle_wrapper",
            current_mag_paths=[
                "src/med_autogrant/product_entry_parts/lifecycle_receipt_bundle.py",
                "src/med_autogrant/product_entry_parts/package_lifecycle_handoff.py",
            ],
            input_refs=[
                "/product_entry_manifest/lifecycle_guarded_apply_proof",
                "/product_entry_manifest/artifact_locator_contract",
            ],
        ),
    ]
    currentness_proof = _handoff_currentness_proof(generated_surfaces)
    return {
        "surface_kind": "mag_generated_surface_handoff",
        "handoff_id": "mag.generated_surface_handoff.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "target_generator_owner": "one-person-lab",
        "active_caller_owner": TARGET_DOMAIN_ID,
        "active_caller_surface": "mag_direct_domain_entry_until_opl_caller_evidence",
        "domain_handler_target": TARGET_DOMAIN_ID,
        "domain_handler_owner": TARGET_DOMAIN_ID,
        "mag_role": "domain_handler_ref_only_adapter_and_minimal_authority_functions",
        "state": "mag_handler_boundary_ready_external_caller_evidence_gated",
        "handoff_policy": "OPL_generates_or_hosts_generic_wrappers_from_MAG_pack_input",
        "bridge_policy": (
            "MAG handwritten product/status/sidecar/projection wrappers are migration bridges, "
            "not long-term MAG owner surfaces."
        ),
        "bridge_exit_gate": _bridge_exit_gate(
            gate_id="mag.generated_surface_handoff.bridge_exit.v1",
            applies_to_surface_ids=list(GENERATED_OR_BRIDGE_SURFACE_IDS),
            exit_action="delete_or_history_tombstone_mag_handwritten_wrapper_keep_domain_handler",
        ),
        "declarative_input_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/"
            "declarative_grant_pack_compiler_input"
        ),
        "generated_surface_ids": list(GENERATED_OR_BRIDGE_SURFACE_IDS),
        "current_mag_path_status": currentness_proof,
        "missing_current_mag_path_count": currentness_proof["missing_current_mag_path_count"],
        "stale_path_policy": "history_or_source_ref_refresh_only",
        "generated_or_bridge_surfaces": generated_surfaces,
        "mag_long_term_owner_surface_ids": [],
        "authority_boundary": {
            "long_term_generated_surface_owner": "one-person-lab",
            "mag_long_term_owner": False,
            "mag_can_own_generated_product_status": False,
            "mag_can_own_generated_user_loop": False,
            "mag_can_own_generated_sidecar": False,
            "mag_can_own_generated_grouped_cli_api": False,
            "mag_can_own_generated_projection": False,
            "mag_can_own_generated_lifecycle_wrapper": False,
            "generated_surface_can_write_grant_truth": False,
            "generated_surface_can_write_memory_body": False,
            "generated_surface_can_sign_owner_receipt": False,
            "generated_surface_can_declare_verdict": False,
        },
    }


def _authority_function(
    function_id: str,
    *,
    authority_output_class: str,
    work_mode: str,
    judgment_owner: str,
    programmatic_role: str,
    ai_stage_artifact_required: bool,
    allowed_return_shapes: list[str],
    source_refs: list[str],
    cannot_generate_reason: str,
    ai_first_guard: str,
) -> dict[str, Any]:
    stage_or_owner_receipt_required = ai_stage_artifact_required or function_id in {
        "package_authority",
        "owner_receipt_signer",
    }
    return {
        "surface_kind": "mag_minimal_authority_surface",
        "authority_surface_id": function_id,
        "function_id": function_id,
        "legacy_function_id_compatibility": True,
        "owner": TARGET_DOMAIN_ID,
        "retention_class": "mag_minimal_authority_function",
        "generated_by_opl": False,
        "opl_generated_wrapper_allowed": True,
        "work_mode": work_mode,
        "judgment_owner": judgment_owner,
        "programmatic_role": programmatic_role,
        "ai_stage_artifact_required": ai_stage_artifact_required,
        "stage_or_owner_receipt_evidence_required": stage_or_owner_receipt_required,
        "mechanical_decision_forbidden": True,
        "programmatic_verdict_generation_allowed": False,
        "authority_output_class": authority_output_class,
        "allowed_return_shapes": allowed_return_shapes,
        "output_boundary": {
            "allowed_return_shapes": allowed_return_shapes,
            "forbidden_outputs": [
                "grant_truth_write",
                "memory_body_write",
                "artifact_body_write_without_owner_receipt",
                "opl_owned_runtime_state",
                "mechanical_ready_verdict",
                "programmatic_ready_verdict",
                "ai_free_quality_verdict",
                "schema_completeness_ready_verdict",
                "generic_lifecycle_completion_verdict",
            ],
        },
        "forbidden_decision_sources": [
            "schema_completeness",
            "opl_provider_completion",
            "generic_lifecycle_completion",
            "package_file_presence",
            "numeric_scorecard_alone",
            "controller_route_state",
            "runtime_queue_state",
        ],
        "decision_boundary": {
            "ai_first_judgment_required": ai_stage_artifact_required,
            "programmatic_role_may_materialize_refs_only": True,
            "programmatic_role_may_compute_ready_verdict": False,
            "owner_receipt_or_typed_blocker_required_when_evidence_missing": True,
        },
        "source_refs": source_refs,
        "cannot_generate_reason": cannot_generate_reason,
        "cannot_absorb_reason": cannot_generate_reason,
        "ai_first_guard": ai_first_guard,
        "ai_first_guard_policy": "stage_artifact_or_owner_receipt_required",
    }


def _generated_surface(
    surface_id: str,
    *,
    current_mag_paths: list[str],
    input_refs: list[str],
) -> dict[str, Any]:
    current_mag_path_status = _current_mag_path_status(current_mag_paths)
    return {
        "surface_id": surface_id,
        "surface_status": "mag_handler_ref_only_adapter_waiting_for_opl_generated_or_hosted_caller_evidence",
        "active_caller_owner": TARGET_DOMAIN_ID,
        "current_owner": TARGET_DOMAIN_ID,
        "target_owner": "one-person-lab",
        "domain_handler_target": TARGET_DOMAIN_ID,
        "domain_handler_owner": TARGET_DOMAIN_ID,
        "current_mag_path_role": "domain_handler_ref_only_adapter_not_generic_wrapper_owner",
        "bridge_exit_gate": _bridge_exit_gate(
            gate_id=f"mag.generated_surface_handoff.{surface_id}.bridge_exit.v1",
            applies_to_surface_ids=[surface_id],
            exit_action="delete_or_history_tombstone_this_mag_wrapper_keep_domain_handler",
        ),
        "current_mag_paths": current_mag_paths,
        "current_mag_path_status": current_mag_path_status,
        "missing_current_mag_path_count": current_mag_path_status["missing_count"],
        "stale_path_policy": "history_or_source_ref_refresh_only",
        "compiler_input_refs": input_refs,
        "generated_by_opl_in_target": True,
        "current_mag_long_term_owner": False,
        "keeps_mag_authority_functions": False,
    }


def _current_mag_path_status(current_mag_paths: list[str]) -> dict[str, Any]:
    path_statuses = []
    for path in current_mag_paths:
        path_statuses.append(
            {
                "path": path,
                "exists": (REPO_ROOT / path).is_file(),
                "proof_kind": "repo_file_exists_at_manifest_build_time",
                "role": "current_mag_domain_handler_or_refs_only_adapter_path",
            }
        )
    missing_paths = [status["path"] for status in path_statuses if not status["exists"]]
    return {
        "surface_kind": "mag_current_path_status",
        "status": "current" if not missing_paths else "missing_current_paths",
        "checked_path_count": len(path_statuses),
        "missing_count": len(missing_paths),
        "missing_paths": missing_paths,
        "stale_path_policy": "history_or_source_ref_refresh_only",
        "paths": path_statuses,
    }


def _handoff_currentness_proof(generated_surfaces: list[dict[str, Any]]) -> dict[str, Any]:
    missing_paths = [
        path
        for surface in generated_surfaces
        for path in surface["current_mag_path_status"]["missing_paths"]
    ]
    return {
        "surface_kind": "mag_generated_surface_handoff_currentness_proof",
        "status": "current" if not missing_paths else "missing_current_paths",
        "checked_surface_count": len(generated_surfaces),
        "checked_path_count": sum(
            surface["current_mag_path_status"]["checked_path_count"]
            for surface in generated_surfaces
        ),
        "missing_current_mag_path_count": len(missing_paths),
        "missing_current_mag_paths": missing_paths,
        "stale_path_policy": "history_or_source_ref_refresh_only",
        "proof_policy": (
            "listed current_mag_paths must exist in the MAG repo; stale paths may only be "
            "moved to history/provenance or refreshed as source refs."
        ),
        "claims_opl_replacement_exists": False,
        "claims_all_bridge_exits_complete": False,
        "claims_production_long_run_soak_complete": False,
    }


def _bridge_exit_gate(
    *,
    gate_id: str,
    applies_to_surface_ids: list[str],
    exit_action: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_bridge_exit_gate",
        "gate_id": gate_id,
        "gate_status": "mag_handler_boundary_ready_external_caller_evidence_required",
        "target_domain_id": TARGET_DOMAIN_ID,
        "replacement_owner": "one-person-lab",
        "domain_handler_owner": TARGET_DOMAIN_ID,
        "domain_handler_target": TARGET_DOMAIN_ID,
        "applies_to_surface_ids": applies_to_surface_ids,
        "required_evidence": list(GENERATED_SURFACE_BRIDGE_EXIT_EVIDENCE),
        "satisfied_evidence_refs": {
            evidence: list(refs)
            for evidence, refs in GENERATED_SURFACE_BRIDGE_EXIT_EVIDENCE_REFS.items()
        },
        "exit_action": exit_action,
        "claims_exit_complete": False,
        "claims_production_long_run_soak_complete": False,
        "production_soak_gate_status": "external_live_soak_and_caller_evidence_not_claimed_by_mag_repo",
        "mag_handler_boundary_ready": True,
        "external_opl_generated_or_hosted_caller_evidence_required": True,
        "authority_boundary": {
            "mag_keeps_domain_handler": True,
            "mag_keeps_grant_authority_functions": True,
            "mag_can_keep_generic_wrapper_after_exit": False,
            "opl_generated_surface_can_write_grant_truth": False,
            "opl_generated_surface_can_write_memory_body": False,
            "opl_generated_surface_can_sign_owner_receipt": False,
            "opl_generated_surface_can_declare_verdict": False,
        },
    }
