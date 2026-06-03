from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


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
        "opl_consumption": "refs_manifest_missing_output_receipt_blocker_handoff_only",
        "opl_can_interpret_grant_quality": False,
    }
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
    assert artifact_contract["package_stage_lifecycle_projection"]["submission_ready_package"][
        "lifecycle_contract_role"
    ] == "export_artifact_ref"
    assert artifact_contract["package_stage_lifecycle_projection"]["authority_boundary"][
        "opl_can_interpret_grant_quality"
    ] is False
