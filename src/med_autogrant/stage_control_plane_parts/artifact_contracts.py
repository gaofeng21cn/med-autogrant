from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID


STAGE_OUTPUT_ARTIFACT_LIFECYCLE_ROLE = "stage_output_artifact_ref"
PACKAGE_STAGE_ID = "package_and_submit_ready"
FINAL_PACKAGE_LIFECYCLE_ROLE = "canonical_promotion_ref"
SUBMISSION_READY_PACKAGE_LIFECYCLE_ROLE = "export_artifact_ref"
PACKAGE_LIFECYCLE_OPL_CONSUMPTION = "refs_manifest_missing_output_receipt_blocker_handoff_only"
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
            "opl_consumption": PACKAGE_LIFECYCLE_OPL_CONSUMPTION,
            "opl_can_interpret_grant_quality": False,
        },
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
        },
        "final_package": {
            "lifecycle_contract_role": FINAL_PACKAGE_LIFECYCLE_ROLE,
            "canonical_ref_template": "mag-package://final-package/{grant_run_id}/{workspace_id}/{draft_id}",
            "current_pointer_ref": "current:mag/package/final-package",
        },
        "submission_ready_package": {
            "lifecycle_contract_role": SUBMISSION_READY_PACKAGE_LIFECYCLE_ROLE,
            "export_ref_template": "mag-package://submission-ready/{grant_run_id}/{workspace_id}/{draft_id}",
            "current_pointer_ref": "current:mag/package/submission-ready",
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
