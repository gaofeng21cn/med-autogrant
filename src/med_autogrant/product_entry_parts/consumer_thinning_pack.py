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


def build_mag_minimal_authority_functions() -> list[dict[str, Any]]:
    return [
        _authority_function(
            "fundability_verdict",
            authority_output_class="verdict_refs",
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
    allowed_return_shapes: list[str],
    source_refs: list[str],
    cannot_generate_reason: str,
    ai_first_guard: str,
) -> dict[str, Any]:
    return {
        "function_id": function_id,
        "owner": TARGET_DOMAIN_ID,
        "retention_class": "mag_minimal_authority_function",
        "generated_by_opl": False,
        "opl_generated_wrapper_allowed": True,
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
            ],
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
        "compiler_input_refs": input_refs,
        "generated_by_opl_in_target": True,
        "current_mag_long_term_owner": False,
        "keeps_mag_authority_functions": False,
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
