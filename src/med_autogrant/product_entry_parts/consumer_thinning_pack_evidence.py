from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID

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
        "domain_handler_projection_ref": "/domain_handler_export/external_evidence_request_pack",
        "required_request_ids": list(EXTERNAL_EVIDENCE_REQUEST_IDS),
        "requests": [
            _external_evidence_request(
                "opl_generated_hosted_caller_pack_consumption",
                requested_from="one-person-lab",
                evidence_class="generated_hosted_caller_consumption",
                required_refs=[
                    "opl://generated-surfaces/mag/product-entry-manifest",
                    "opl://generated-surfaces/mag/domain-handler",
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
                    "/product_entry_manifest/mag_consumer_thinning_contract/exposed_domain_handler_return_refs",
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
                    "/product_entry_manifest/physical_skeleton_follow_through/active_path_current_role_guard",
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
            "domain_handler_projection_ref": "/domain_handler_export/external_evidence_request_pack",
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
                "opl://generated-surfaces/mag/domain-handler",
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
            "domain_handler": "guarded_domain_handler_target",
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
