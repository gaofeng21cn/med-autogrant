from __future__ import annotations

from typing import Any

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


AHE_PATCH_LOOP_REF_KEYS = [
    "blocked_suite_result_ref",
    "developer_patch_work_order_ref",
    "patch_traceability_matrix_ref",
    "target_repo_verification_refs",
    "target_runtime_read_model_consumption_ref",
    "workspace_environment_proof_ref",
    "no_forbidden_write_proof_ref",
    "target_owner_receipt_or_typed_blocker_ref",
    "patch_absorption_ref",
    "worktree_cleanup_ref",
    "agent_lab_re_evaluation_ref",
]

AHE_PATCH_LOOP_CLOSEOUT_REFS = {
    "blocked_suite_result_ref": "agent-lab-suite-result:oma/mag/blocked-suite",
    "developer_patch_work_order_ref": (
        "developer-work-order:oma/mag/ahe-real-target-scaleout-smoke"
    ),
    "patch_traceability_matrix_ref": (
        "patch-traceability:oma/mag/ahe-real-target-scaleout-smoke"
    ),
    "target_repo_verification_refs": [
        (
            "rtk ./scripts/run-pytest-clean.sh "
            "tests/product_entry_cases/test_production_live_acceptance.py "
            "tests/test_production_acceptance.py "
            "tests/test_opl_standard_pack.py -q"
        ),
        "rtk ./scripts/verify.sh",
        "rtk git diff --check",
    ],
    "target_runtime_read_model_consumption_ref": (
        "/product_entry_manifest/production_live_acceptance_receipt"
    ),
    "workspace_environment_proof_ref": (
        "workspace-proof:med-autogrant/.worktrees/codex/ahe-real-target-scaleout-smoke"
    ),
    "no_forbidden_write_proof_ref": (
        "contracts/agent_lab_handoff.json#/authority_boundary/oma_consumes_mag_refs_only"
    ),
    "target_owner_receipt_or_typed_blocker_ref": (
        "receipt:mag/production-live-acceptance/2026-05-20"
    ),
    "patch_absorption_ref": "git-commit:pending/codex-ahe-real-target-scaleout-smoke",
    "worktree_cleanup_ref": "worktree-cleanup:pending/ahe-real-target-scaleout-smoke",
    "agent_lab_re_evaluation_ref": (
        "agent-lab-run:oma/mag/ahe-real-target-scaleout-smoke/re-evaluation"
    ),
}


def build_agent_lab_handoff(*, generated_surface_owner: str) -> dict[str, Any]:
    return {
        "surface_kind": "agent_lab_handoff.v1",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "consumer": "opl-meta-agent",
        "consumer_contract": "agent:evidence",
        "state": "domain_owned_refs_ready",
        "payload_policy": "refs_only_no_body_material",
        "accepted_payload_classes": [
            "contract_ref",
            "json_pointer_ref",
            "command_ref",
            "receipt_ref",
            "receipt_projection_ref",
            "typed_blocker_ref",
            "test_ref",
            "human_doc_ref",
        ],
        "forbidden_payload_classes": [
            "grant_truth_body",
            "grant_artifact_body",
            "memory_body",
            "proposal_text_body",
            "review_artifact_body",
            "package_archive_body",
            "fundability_verdict_body",
            "authoring_quality_verdict_body",
            "submission_ready_export_verdict_body",
            "opl_runtime_state_body",
            "app_workbench_state_body",
        ],
        "handoff_refs": _handoff_refs(generated_surface_owner=generated_surface_owner),
        "authority_boundary": _authority_boundary(),
    }


def build_oma_handoff_refs(*, agent_lab_handoff: dict[str, Any]) -> dict[str, Any]:
    return {
        "surface_kind": "mag_oma_handoff_refs.v1",
        "schema_version": 1,
        "domain_id": TARGET_DOMAIN_ID,
        "owner": TARGET_DOMAIN_ID,
        "consumer": "opl-meta-agent",
        "consumer_contract": "agent:evidence",
        "state": "standard_agent_lab_handoff_available",
        "standard_contract_ref": "contracts/agent_lab_handoff.json",
        "payload_policy": "refs_only_no_body_material",
        "handoff_refs": {
            "standard_agent_lab_handoff": "contracts/agent_lab_handoff.json",
            "real_target_patch_loop_closeout": (
                "contracts/agent_lab_handoff.json#/handoff_refs/"
                "real_target_patch_loop_closeout"
            ),
        },
        "authority_boundary": dict(agent_lab_handoff["authority_boundary"]),
    }


def _handoff_refs(*, generated_surface_owner: str) -> dict[str, Any]:
    return {
        "production_acceptance": {
            "state_ref": "contracts/production_acceptance/mag-production-acceptance.json",
            "receipt_chain_ref": "contracts/production_acceptance/mag-production-acceptance.json#/grant_receipt_chain",
            "closure_ref": "contracts/production_acceptance/mag-production-acceptance.json#/closure_evidence",
            "external_evidence_ledger_ref": "contracts/external_evidence/mag-evidence-receipt-ledger.json",
            "verification_refs": [
                "tests/test_production_acceptance.py",
                "tests/product_entry_cases/test_production_live_acceptance.py",
            ],
        },
        "agent_lab_handoff": {
            "suite_result_shape": "opl_agent_lab_suite_result",
            "consumption_ref": "/product_entry_manifest/production_live_acceptance_receipt",
            "coordination_ref": "contracts/production_acceptance/mag-production-acceptance.json#/closure_evidence",
            "boundary": "agent_lab_result_is_refs_only_input_not_mag_owner_receipt_authority",
        },
        "owner_route": {
            "manifest_ref": "/product_entry_manifest/owner_route",
            "route_id": "mag_product_entry_owner_route",
            "route_truth_owner": TARGET_DOMAIN_ID,
            "next_owner": TARGET_DOMAIN_ID,
            "verification_refs": [
                "tests/product_entry_cases/test_manifest_and_status.py::ManifestAndStatusTest::test_manifest_contains_runtime_companions",
                "tests/test_opl_family_contract_adoption.py::test_family_adapter_preserves_mag_owner_route_discovery",
            ],
        },
        "owner_receipt": {
            "contract_ref": "contracts/owner_receipt_contract.json",
            "manifest_ref": "/product_entry_manifest/owner_receipt_contract",
            "production_owner_receipt_ref": "receipt:mag/production-live-acceptance/2026-05-20",
            "production_receipt_projection_ref": "receipt-projection:mag/production-live-acceptance-owner-receipt",
            "authority": "mag_issues_owner_receipts_oma_consumes_refs_only",
        },
        "typed_blocker": {
            "ledger_ref": "contracts/external_evidence/mag-evidence-receipt-ledger.json",
            "domain_owned_typed_blocker_ids_ref": (
                "contracts/external_evidence/mag-evidence-receipt-ledger.json#/"
                "domain_owned_typed_blocker_request_ids"
            ),
            "continuous_no_forbidden_write_blocker_ref": (
                "contracts/external_evidence/mag-evidence-receipt-ledger.json#/request_closures/4"
            ),
            "accepted_return_shapes": [
                "domain_owner_receipt_ref",
                "typed_blocker_ref",
                "no_regression_evidence_ref",
            ],
        },
        "generated_surface_handoff": {
            "contract_ref": "contracts/generated_surface_handoff.json",
            "manifest_ref": "/product_entry_manifest/mag_consumer_thinning_contract/generated_surface_handoff",
            "bridge_exit_gate_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "generated_surface_handoff/bridge_exit_gate"
            ),
            "generator_owner": generated_surface_owner,
        },
        "editable_surface_hints": {
            "editable_shared_bootstrap_ref": "src/med_autogrant/editable_shared_bootstrap.py",
            "clean_runner_refs": [
                "scripts/run-python-clean.sh",
                "scripts/run-pytest-clean.sh",
            ],
            "environment_hint_refs": [
                "MED_AUTOGRANT_EDITABLE_SHARED_ENV_ROOT",
                "PYTHONPYCACHEPREFIX",
                "PYTEST_ADDOPTS",
            ],
            "verification_refs": [
                "tests/test_editable_shared_bootstrap.py",
                "tests/test_test_command_surfaces.py",
            ],
            "boundary": "editable_hints_are_dependency_path_hints_not_runtime_or_artifact_authority",
        },
        "no_forbidden_write_proof": {
            "functional_privatization_ref": (
                "contracts/functional_privatization_audit.json#/"
                "mag_consumer_thinning_contract/external_evidence_request_pack/"
                "requests/continuous_no_forbidden_write_guard"
            ),
            "external_evidence_ledger_ref": (
                "contracts/external_evidence/mag-evidence-receipt-ledger.json#/request_closures/4"
            ),
            "generated_surface_required_ref": (
                "contracts/generated_surface_handoff.json#/required_domain_handoff/3"
            ),
            "verification_refs": [
                "tests/product_entry_cases/test_external_evidence_request_pack.py",
                "tests/product_entry_cases/test_grant_transition_oracle.py",
                "tests/product_entry_cases/test_functional_closure.py",
            ],
            "boundary": "proof_refs_do_not_grant_oma_write_authority",
        },
        "real_target_patch_loop_closeout": _real_target_patch_loop_closeout(),
    }


def _real_target_patch_loop_closeout() -> dict[str, Any]:
    return {
        "state": "refs_only_closeout_smoke_ready",
        "closeout_kind": "ahe_real_target_scaleout_smoke",
        "required_closeout_ref_keys": list(AHE_PATCH_LOOP_REF_KEYS),
        "closeout_refs": dict(AHE_PATCH_LOOP_CLOSEOUT_REFS),
        "production_acceptance_ref": (
            "contracts/production_acceptance/mag-production-acceptance.json#/patch_loop_refs"
        ),
        "read_model_consumption_ref": "/product_entry_manifest/production_live_acceptance_receipt",
        "boundary": "patch_loop_refs_are_body_free_closeout_evidence_not_mag_truth_or_verdict",
    }


def _authority_boundary() -> dict[str, Any]:
    return {
        "oma_can_write_grant_truth": False,
        "oma_can_write_memory_body": False,
        "oma_can_write_artifact_body": False,
        "oma_can_issue_owner_receipt": False,
        "oma_can_declare_fundability_ready": False,
        "oma_can_declare_quality_ready": False,
        "oma_can_declare_export_ready": False,
        "oma_consumes_mag_refs_only": True,
        "owner_receipt_authority_owner": TARGET_DOMAIN_ID,
        "quality_verdict_owner": TARGET_DOMAIN_ID,
        "artifact_authority_owner": TARGET_DOMAIN_ID,
        "memory_authority_owner": TARGET_DOMAIN_ID,
    }
