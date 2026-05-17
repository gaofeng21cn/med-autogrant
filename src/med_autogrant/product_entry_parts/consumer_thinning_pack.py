from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID

MAG_MINIMAL_AUTHORITY_FUNCTION_IDS = (
    "fundability_verdict",
    "quality_verdict",
    "export_verdict",
    "package_authority",
    "memory_accept_reject",
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


def build_mag_minimal_authority_functions() -> list[dict[str, Any]]:
    return [
        _authority_function(
            "fundability_verdict",
            authority_output_class="verdict_refs",
            source_refs=[
                "/product_entry_manifest/family_stage_control_plane/stages",
                "/product_entry_manifest/grant_transition_oracle",
            ],
            cannot_generate_reason="Fundability is a grant-review judgment over call fit and applicant evidence.",
        ),
        _authority_function(
            "quality_verdict",
            authority_output_class="verdict_refs",
            source_refs=[
                "/product_entry_manifest/grant_authoring_readiness",
                "/product_entry_manifest/controlled_stage_attempt_projection",
            ],
            cannot_generate_reason="Authoring quality requires MAG-owned AI critique and issue closure semantics.",
        ),
        _authority_function(
            "export_verdict",
            authority_output_class="verdict_refs",
            source_refs=[
                "package submission-ready",
                "/product_entry_manifest/artifact_locator_contract",
            ],
            cannot_generate_reason="Submission/export readiness is a grant package gate, not package existence.",
        ),
        _authority_function(
            "package_authority",
            authority_output_class="grant_owned_refs",
            source_refs=[
                "/product_entry_manifest/artifact_locator_contract",
                "/product_entry_manifest/lifecycle_guarded_apply_proof",
            ],
            cannot_generate_reason="Grant package mutation and release require MAG package authority.",
        ),
        _authority_function(
            "memory_accept_reject",
            authority_output_class="owner_receipt",
            source_refs=[
                "/product_entry_manifest/domain_memory_descriptor_locator",
                "/product_entry_manifest/controlled_domain_memory_apply_proof",
            ],
            cannot_generate_reason="Grant strategy memory body and accept/reject decisions are MAG authority.",
        ),
        _authority_function(
            "owner_receipt_signer",
            authority_output_class="owner_receipt",
            source_refs=[
                "/product_entry_manifest/owner_receipt_contract",
                "/product_entry_manifest/controlled_soak_no_regression_attempt",
            ],
            cannot_generate_reason="Only MAG can sign domain owner receipts or no-regression evidence.",
        ),
        _authority_function(
            "grant_helper",
            authority_output_class="domain_action_metadata",
            source_refs=[
                "/product_entry_manifest/family_action_catalog",
                "/product_entry_manifest/grant_transition_oracle",
            ],
            cannot_generate_reason="Grant-native helpers encode funder, route, and blocker semantics.",
        ),
    ]


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
    return {
        "surface_kind": "mag_generated_surface_handoff",
        "handoff_id": "mag.generated_surface_handoff.v1",
        "target_domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "target_generator_owner": "one-person-lab",
        "state": "declarative_input_landed_external_generated_surface_gate",
        "handoff_policy": "OPL_generates_or_hosts_generic_wrappers_from_MAG_pack_input",
        "bridge_policy": (
            "MAG handwritten product/status/sidecar/projection wrappers are migration bridges, "
            "not long-term MAG owner surfaces."
        ),
        "declarative_input_ref": (
            "/product_entry_manifest/mag_consumer_thinning_contract/"
            "declarative_grant_pack_compiler_input"
        ),
        "generated_surface_ids": list(GENERATED_OR_BRIDGE_SURFACE_IDS),
        "generated_or_bridge_surfaces": [
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
        ],
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
    source_refs: list[str],
    cannot_generate_reason: str,
) -> dict[str, Any]:
    return {
        "function_id": function_id,
        "owner": TARGET_DOMAIN_ID,
        "retention_class": "mag_minimal_authority_function",
        "generated_by_opl": False,
        "opl_generated_wrapper_allowed": True,
        "authority_output_class": authority_output_class,
        "source_refs": source_refs,
        "cannot_generate_reason": cannot_generate_reason,
    }


def _generated_surface(
    surface_id: str,
    *,
    current_mag_paths: list[str],
    input_refs: list[str],
) -> dict[str, Any]:
    return {
        "surface_id": surface_id,
        "surface_status": "migration_bridge_until_opl_generated_surface",
        "current_owner": TARGET_DOMAIN_ID,
        "target_owner": "one-person-lab",
        "current_mag_paths": current_mag_paths,
        "compiler_input_refs": input_refs,
        "generated_by_opl_in_target": True,
        "current_mag_long_term_owner": False,
        "keeps_mag_authority_functions": False,
    }
