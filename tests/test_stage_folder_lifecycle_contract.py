from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
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


def _stage_control_plane() -> dict[str, object]:
    return json.loads((REPO_ROOT / "contracts" / "stage_control_plane.json").read_text(encoding="utf-8"))


def test_mag_stage_control_plane_projects_package_lifecycle_into_stage_folder_contract() -> None:
    plane = _stage_control_plane()
    package_stage = next(
        stage for stage in plane["stages"] if stage["stage_id"] == "package_and_submit_ready"
    )
    artifact_contract = package_stage["stage_contract"]["stage_native_artifact_contract"]

    assert artifact_contract["stage_folder_lifecycle_contract"] == {
        "artifact_bundle_role": "stage_output_artifact_ref",
        "artifact_bundle_output_role": "submission_ready_package_manifest_ref",
        "artifact_bundle_manifest_required": True,
        "artifact_bundle_owner_receipt_or_typed_blocker_required": True,
        "physical_kernel_locator_roles": PHYSICAL_KERNEL_LOCATOR_ROLES,
        "conformance_required": True,
        "opl_consumption": "refs_manifest_missing_output_receipt_blocker_handoff_only",
        "opl_can_interpret_grant_quality": False,
    }
    physical_kernel = artifact_contract["physical_stage_folder_kernel"]
    assert physical_kernel["maps_to_opl_contract"] == "opl_stage_artifact_runtime_contract.v1"
    assert (
        physical_kernel["opl_contract_ref"]
        == "contracts/opl-framework/stage-artifact-runtime-contract.json"
    )
    assert physical_kernel["required_physical_locator_roles"] == PHYSICAL_KERNEL_LOCATOR_ROLES
    assert physical_kernel["required_attempt_entries"] == [
        "stage.json",
        "attempt.json",
        "manifest.json",
        "inputs/",
        "outputs/",
        "evidence/",
        "receipts/receipt.json",
    ]
    assert physical_kernel["physical_locator_templates"]["stage_json_ref"].endswith("/stage.json")
    assert (
        physical_kernel["physical_locator_templates"]["conformance_summary_ref"]
        == "opl-conformance://stage-artifact/med-autogrant/package_and_submit_ready/{attempt_id}"
    )
    assert physical_kernel["manifest_hash_semantics"]["algorithm"] == "sha256"
    assert physical_kernel["read_model_semantics"]["status_source_of_truth"] == "physical_stage_folder"
    assert physical_kernel["read_model_semantics"]["orphan_artifact_is_completion"] is False
    assert physical_kernel["conformance_refs"]["domain_readiness_claim"] is False
    assert physical_kernel["workbench_projection_refs"]["artifact_body_access"] is False
    assert physical_kernel["retention_restore_boundary"]["restore_requires_restore_proof_ref"] is True
    assert physical_kernel["authority_boundary"]["opl_can_create_mag_owner_receipt"] is False
    assert physical_kernel["authority_boundary"]["opl_can_interpret_grant_quality"] is False
    assert artifact_contract["owner_verdict_signature_policy"]["required_verdicts"] == [
        "fundability_verdict",
        "authoring_quality_verdict",
        "export_verdict",
        "submission_ready_verdict",
    ]
    assert artifact_contract["owner_verdict_signature_policy"]["accepted_signature_shapes"] == [
        "mag_owner_receipt_ref",
        "mag_owned_typed_blocker_ref",
    ]
    assert artifact_contract["owner_verdict_signature_policy"]["opl_can_sign_or_infer_verdict"] is False
    assert artifact_contract["package_stage_lifecycle_projection"]["final_package"][
        "lifecycle_contract_role"
    ] == "canonical_promotion_ref"
    assert artifact_contract["package_stage_lifecycle_projection"]["final_package"][
        "physical_locator_role"
    ] == "canonical_pointer_ref"
    assert artifact_contract["package_stage_lifecycle_projection"]["submission_ready_package"][
        "lifecycle_contract_role"
    ] == "export_artifact_ref"
    assert artifact_contract["package_stage_lifecycle_projection"]["submission_ready_package"][
        "physical_locator_role"
    ] == "export_artifact_ref"
    assert artifact_contract["package_stage_lifecycle_projection"][
        "physical_kernel_handoff_requirements"
    ] == {
        "required_locator_roles": PHYSICAL_KERNEL_LOCATOR_ROLES,
        "conformance_summary_required": True,
        "locator_policy": "physical_stage_folder_refs_only_no_package_body",
        "opl_contract_ref": "contracts/opl-framework/stage-artifact-runtime-contract.json",
    }
    assert artifact_contract["package_stage_lifecycle_projection"]["authority_boundary"][
        "opl_can_interpret_grant_quality"
    ] is False
