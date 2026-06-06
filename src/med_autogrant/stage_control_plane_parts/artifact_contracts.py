from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


STAGE_OUTPUT_ARTIFACT_LIFECYCLE_ROLE = "stage_output_artifact_ref"
PACKAGE_STAGE_ID = "package_and_submit_ready"
FINAL_PACKAGE_LIFECYCLE_ROLE = "canonical_promotion_ref"
SUBMISSION_READY_PACKAGE_LIFECYCLE_ROLE = "export_artifact_ref"
PACKAGE_LIFECYCLE_OPL_CONSUMPTION = "refs_manifest_missing_output_receipt_blocker_handoff_only"
OPL_STAGE_ARTIFACT_RUNTIME_CONTRACT_REF = (
    "contracts/opl-framework/stage-artifact-runtime-contract.json"
)
PHYSICAL_KERNEL_LOCATOR_ROLES = [
    "stage_json_ref",
    "attempt_json_ref",
    "manifest_json_ref",
    "receipt_json_ref",
    "current_json_ref",
    "latest_json_ref",
    "canonical_pointer_ref",
    "export_artifact_ref",
    "lineage_events_ref",
    "lineage_graph_ref",
    "retention_policy_ref",
    "conformance_summary_ref",
]
OWNER_VERDICT_SIGNATURE_POLICY = {
    "surface_kind": "mag_owner_verdict_signature_policy",
    "version": "mag-owner-verdict-signature-policy.v1",
    "owner": TARGET_DOMAIN_ID,
    "required_verdicts": [
        "fundability_verdict",
        "authoring_quality_verdict",
        "export_verdict",
        "submission_ready_verdict",
    ],
    "accepted_signature_shapes": [
        "mag_owner_receipt_ref",
        "mag_owned_typed_blocker_ref",
    ],
    "source_surfaces": [
        "MAG owner receipt",
        "MAG-owned typed blocker",
        "owner-backed export artifact ref",
    ],
    "opl_can_sign_or_infer_verdict": False,
    "provider_completion_can_sign_verdict": False,
}


def _physical_stage_folder_kernel_contract(*, stage_id: str, output_role: str) -> dict[str, Any]:
    attempt_root = (
        "runtime-state/domains/med-autogrant/deliverables/{program_id}/{grant_run_id}/"
        "{workspace_id}/{draft_id_or_no_draft}/"
        f"stages/{stage_id}/attempts/{{attempt_id}}"
    )
    stage_root = (
        "runtime-state/domains/med-autogrant/deliverables/{program_id}/{grant_run_id}/"
        "{workspace_id}/{draft_id_or_no_draft}/"
        f"stages/{stage_id}"
    )
    return {
        "surface_kind": "mag_stage_physical_folder_kernel_contract",
        "version": "mag-stage-physical-folder-kernel-contract.v1",
        "maps_to_opl_contract": "opl_stage_artifact_runtime_contract.v1",
        "opl_contract_ref": OPL_STAGE_ARTIFACT_RUNTIME_CONTRACT_REF,
        "domain": TARGET_DOMAIN_ID,
        "stage_id": stage_id,
        "stage_output_role": output_role,
        "attempt_root_ref_template": attempt_root,
        "stage_root_ref_template": stage_root,
        "required_physical_locator_roles": list(PHYSICAL_KERNEL_LOCATOR_ROLES),
        "required_attempt_entries": [
            "stage.json",
            "attempt.json",
            "manifest.json",
            "inputs/",
            "outputs/",
            "evidence/",
            "receipts/receipt.json",
        ],
        "physical_locator_templates": {
            "stage_json_ref": f"{attempt_root}/stage.json",
            "attempt_json_ref": f"{attempt_root}/attempt.json",
            "manifest_json_ref": f"{attempt_root}/manifest.json",
            "receipt_json_ref": f"{attempt_root}/receipts/receipt.json",
            "current_json_ref": f"{stage_root}/current.json",
            "latest_json_ref": f"{stage_root}/latest.json",
            "canonical_pointer_ref": f"{stage_root}/canonical/current.json",
            "export_artifact_ref": f"{stage_root}/exports/{output_role}.json",
            "lineage_events_ref": f"{stage_root}/lineage/events.jsonl",
            "lineage_graph_ref": f"{stage_root}/lineage/graph.json",
            "retention_policy_ref": f"{stage_root}/retention/policy.json",
            "conformance_summary_ref": (
                f"opl-conformance://stage-artifact/med-autogrant/{stage_id}/{{attempt_id}}"
            ),
        },
        "manifest_hash_semantics": {
            "algorithm": "sha256",
            "required_hash_fields": [
                "output_hashes",
                "evidence_hashes",
                "receipt_hashes",
            ],
            "hash_entries_required_for_physical_files": True,
            "success_with_hash_mismatch_is_broken": True,
        },
        "read_model_semantics": {
            "status_source_of_truth": "physical_stage_folder",
            "success_requires": [
                "valid_manifest",
                "required_outputs_present",
                "mag_owner_receipt_ref_and_receipt_file",
            ],
            "blocked_requires": [
                "mag_owned_typed_blocker_ref",
                "blocker_evidence_file",
            ],
            "orphan_artifact_is_completion": False,
            "missing_deltas_must_be_reported": True,
        },
        "conformance_refs": {
            "surface_kind": "mag_opl_stage_artifact_conformance_refs",
            "opl_conformance_contract_ref": (
                f"{OPL_STAGE_ARTIFACT_RUNTIME_CONTRACT_REF}#/conformance_gate"
            ),
            "strict_units": [
                "Stage Folder",
                "Manifest",
                "Receipt",
                "content_hashes",
                "latest_pointer",
                "current_pointer",
                "lineage_events",
            ],
            "fails_on_ref": f"{OPL_STAGE_ARTIFACT_RUNTIME_CONTRACT_REF}#/conformance_gate/fails_on",
            "domain_readiness_claim": False,
        },
        "workbench_projection_refs": {
            "projects": [
                "current_pointer",
                "stage_status",
                "attempt_manifest_refs",
                "owner_receipt_refs",
                "typed_blocker_refs",
                "decision_receipt_refs",
                "content_hashes",
                "canonical_artifacts",
                "export_artifacts",
                "lineage_refs",
                "retention_policy",
                "conformance_summary",
            ],
            "artifact_body_access": False,
            "domain_verdict_authority": False,
        },
        "retention_restore_boundary": {
            "retention_policy_ref_template": f"{stage_root}/retention/policy.json",
            "retention_archive_ref_template": (
                f"{stage_root}/retention/attempts/{stage_id}/{{attempt_id}}"
            ),
            "restore_requires_restore_proof_ref": True,
            "restore_does_not_create_owner_receipt": True,
            "restore_does_not_declare_domain_truth_or_quality": True,
        },
        "authority_boundary": {
            "mag_owns_grant_truth": True,
            "mag_owns_package_authority": stage_id == PACKAGE_STAGE_ID,
            "mag_owns_export_verdict": True,
            "opl_can_index_refs": True,
            "opl_can_index_canonical_pointer_ref": True,
            "opl_can_rebuild_projection": True,
            "opl_can_promote_canonical_pointer": False,
            "opl_can_create_mag_owner_receipt": False,
            "opl_can_write_grant_truth": False,
            "opl_can_mutate_artifact_body": False,
            "opl_can_interpret_grant_quality": False,
            "opl_can_declare_export_ready": False,
            "opl_can_declare_submission_ready": False,
        },
    }


def stage_native_artifact_contract(
    *,
    stage_id: str,
    output_role: str,
    expected_receipt_refs: list[dict[str, Any]],
) -> dict[str, Any]:
    contract = {
        "surface_kind": "mag_stage_native_artifact_contract",
        "version": "mag-stage-native-artifact-contract.v1",
        "stage_id": stage_id,
        "owner": TARGET_DOMAIN_ID,
        "required_output_roles": [output_role],
        "manifest_requirements": {
            "required_fields": [
                "grant_run_id",
                "workspace_id",
                "lifecycle_stage",
                "stage_id",
                "stage_output_role",
                "lifecycle_contract_role",
                "artifact_classification",
                "manifest_ref",
                "current_pointer_ref",
                "owner_receipt_or_typed_blocker_ref",
            ],
            "identity_fields": [
                "grant_run_id",
                "workspace_id",
                "draft_id",
                "lifecycle_stage",
                "stage_id",
                "stage_output_role",
            ],
            "body_free_projection_required": True,
            "manifest_ref_template": (
                f"mag-artifact://{stage_id}/{output_role}/"
                "{grant_run_id}/{workspace_id}/{draft_id_or_no_draft}/manifest"
            ),
        },
        "owner_closeout_requirements": {
            "accepted_return_shapes": [
                "domain_owner_receipt_ref",
                "typed_blocker_ref",
                "no_regression_evidence_ref",
            ],
            "expected_receipt_refs": expected_receipt_refs,
            "typed_blocker_required_when_output_missing": True,
            "owner_receipt_required_for_current_pointer_advance": True,
            "provider_completion_is_not_owner_closeout": True,
        },
        "stage_folder_lifecycle_contract": {
            "artifact_bundle_role": STAGE_OUTPUT_ARTIFACT_LIFECYCLE_ROLE,
            "artifact_bundle_output_role": output_role,
            "artifact_bundle_manifest_required": True,
            "artifact_bundle_owner_receipt_or_typed_blocker_required": True,
            "physical_kernel_locator_roles": list(PHYSICAL_KERNEL_LOCATOR_ROLES),
            "conformance_required": True,
            "opl_consumption": PACKAGE_LIFECYCLE_OPL_CONSUMPTION,
            "opl_can_interpret_grant_quality": False,
        },
        "physical_stage_folder_kernel": _physical_stage_folder_kernel_contract(
            stage_id=stage_id,
            output_role=output_role,
        ),
        "owner_verdict_signature_policy": dict(OWNER_VERDICT_SIGNATURE_POLICY),
        "current_pointer_rules": {
            "pointer_owner": TARGET_DOMAIN_ID,
            "pointer_ref_template": f"current:mag/stages/{stage_id}/{output_role}",
            "advance_requires": [
                "stage_output_manifest_ref",
                "domain_owner_receipt_ref_or_typed_blocker_ref",
            ],
            "opl_can_advance_pointer": False,
            "missing_pointer_policy": "typed_blocker_no_opl_inference",
        },
        "artifact_classification_boundary": {
            "classification": "grant_stage_output_ref",
            "artifact_body_owner": TARGET_DOMAIN_ID,
            "artifact_authority_owner": TARGET_DOMAIN_ID,
            "opl_consumes": [
                "stage_output_role",
                "lifecycle_contract_role",
                "manifest_ref",
                "current_pointer_ref",
                "owner_receipt_or_typed_blocker_ref",
                "missing_output_ref",
                "handoff_ref",
            ],
            "opl_forbidden_inferences": [
                "fundability_ready",
                "authoring_quality_ready",
                "export_ready",
                "submission_ready",
                "grant_truth",
            ],
            "opl_can_read_artifact_body": False,
            "opl_can_write_artifact_body": False,
            "opl_can_declare_fundability_ready": False,
            "opl_can_declare_quality_ready": False,
            "opl_can_declare_export_ready": False,
            "opl_can_declare_submission_ready": False,
        },
    }
    if stage_id == PACKAGE_STAGE_ID:
        contract["package_stage_lifecycle_projection"] = package_stage_lifecycle_projection(
            output_role=output_role,
        )
    return contract


def package_stage_lifecycle_projection(*, output_role: str) -> dict[str, Any]:
    owner_closeout_ref = (
        f"receipt:mag/grant-stage-controlled-attempt/{PACKAGE_STAGE_ID}/owner-receipt-or-typed-blocker"
    )
    return {
        "surface_kind": "mag_package_stage_folder_lifecycle_projection_contract",
        "version": "mag-package-stage-folder-lifecycle-projection.v1",
        "stage_id": PACKAGE_STAGE_ID,
        "artifact_bundle": {
            "lifecycle_contract_role": STAGE_OUTPUT_ARTIFACT_LIFECYCLE_ROLE,
            "stage_output_role": output_role,
            "manifest_ref_template": (
                f"mag-artifact://{PACKAGE_STAGE_ID}/{output_role}/"
                "{grant_run_id}/{workspace_id}/{draft_id_or_no_draft}/manifest"
            ),
            "physical_locator_roles": [
                "stage_json_ref",
                "attempt_json_ref",
                "manifest_json_ref",
                "receipt_json_ref",
            ],
        },
        "final_package": {
            "lifecycle_contract_role": FINAL_PACKAGE_LIFECYCLE_ROLE,
            "canonical_ref_template": "mag-package://final-package/{grant_run_id}/{workspace_id}/{draft_id}",
            "current_pointer_ref": "current:mag/package/final-package",
            "physical_locator_role": "canonical_pointer_ref",
        },
        "submission_ready_package": {
            "lifecycle_contract_role": SUBMISSION_READY_PACKAGE_LIFECYCLE_ROLE,
            "export_ref_template": "mag-package://submission-ready/{grant_run_id}/{workspace_id}/{draft_id}",
            "current_pointer_ref": "current:mag/package/submission-ready",
            "physical_locator_role": "export_artifact_ref",
        },
        "physical_kernel_handoff_requirements": {
            "required_locator_roles": list(PHYSICAL_KERNEL_LOCATOR_ROLES),
            "conformance_summary_required": True,
            "locator_policy": "physical_stage_folder_refs_only_no_package_body",
            "opl_contract_ref": OPL_STAGE_ARTIFACT_RUNTIME_CONTRACT_REF,
        },
        "owner_receipt_or_typed_blocker_ref": owner_closeout_ref,
        "missing_output_policy": "typed_blocker_required_no_opl_inference",
        "handoff_policy": PACKAGE_LIFECYCLE_OPL_CONSUMPTION,
        "authority_boundary": {
            "mag_owns_package_authority": True,
            "mag_owns_export_verdict": True,
            "mag_owns_submission_ready_verdict": True,
            "opl_can_read_artifact_body": False,
            "opl_can_interpret_grant_quality": False,
            "opl_can_declare_submission_ready": False,
        },
    }


def build_stage_native_artifact_contract(
    *,
    stage: Mapping[str, Any],
    expected_receipt_refs: list[dict[str, Any]],
    output_role: str,
) -> dict[str, Any]:
    return stage_native_artifact_contract(
        stage_id=str(stage["stage_id"]),
        output_role=output_role,
        expected_receipt_refs=expected_receipt_refs,
    )
