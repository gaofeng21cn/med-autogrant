from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID
from med_autogrant.submission_ready import (
    SubmissionReadyExportVerdictError,
    normalize_submission_ready_export_verdict,
)
from med_autogrant.workspace_types import WorkspaceStateError
from opl_harness_shared.artifact_lifecycle import (
    build_refs_only_artifact_lifecycle_handoff,
)


PACKAGE_LIFECYCLE_HANDOFF_PROJECTION_KIND = "mag_package_lifecycle_handoff_projection"
PACKAGE_STAGE_ID = "package_and_submit_ready"
STAGE_OUTPUT_ARTIFACT_LIFECYCLE_ROLE = "stage_output_artifact_ref"
PACKAGE_STAGE_OUTPUT_ROLE = "submission_ready_package_manifest_ref"
FINAL_PACKAGE_LIFECYCLE_ROLE = "canonical_promotion_ref"
SUBMISSION_READY_PACKAGE_LIFECYCLE_ROLE = "export_artifact_ref"
PACKAGE_LIFECYCLE_HANDOFF_POLICY = "refs_manifest_missing_output_receipt_blocker_handoff_only"
OPL_STAGE_ARTIFACT_RUNTIME_CONTRACT_REF = (
    "contracts/opl-framework/stage-artifact-runtime-contract.json"
)
PHYSICAL_KERNEL_LOCATOR_REF_KEYS = (
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
)
REQUIRED_STAGE_FOLDER_PACKAGE_REF_KEYS = (
    "artifact_bundle_ref",
    "final_package_ref",
    "submission_ready_package_ref",
    *PHYSICAL_KERNEL_LOCATOR_REF_KEYS,
)

_PACKAGE_LIFECYCLE_PROFILE = {
    "surface_kind": PACKAGE_LIFECYCLE_HANDOFF_PROJECTION_KIND,
    "version": "v1",
    "state": "refs_ready_for_opl_artifact_package_lifecycle_shell",
    "domain_id": TARGET_DOMAIN_ID,
    "stage_id": PACKAGE_STAGE_ID,
    "required_package_ref_keys": REQUIRED_STAGE_FOLDER_PACKAGE_REF_KEYS,
    "locator_ref_keys": PHYSICAL_KERNEL_LOCATOR_REF_KEYS,
    "artifact_roles": {
        "artifact_bundle_ref_key": "artifact_bundle_ref",
        "artifact_bundle_lifecycle_role": STAGE_OUTPUT_ARTIFACT_LIFECYCLE_ROLE,
        "artifact_bundle_stage_output_role": PACKAGE_STAGE_OUTPUT_ROLE,
        "final_package_ref_key": "final_package_ref",
        "final_package_lifecycle_role": FINAL_PACKAGE_LIFECYCLE_ROLE,
        "canonical_pointer_ref_key": "canonical_pointer_ref",
        "export_package_ref_key": "submission_ready_package_ref",
        "export_package_lifecycle_role": SUBMISSION_READY_PACKAGE_LIFECYCLE_ROLE,
        "export_artifact_ref_key": "export_artifact_ref",
    },
    "stage_artifact_contract_ref": OPL_STAGE_ARTIFACT_RUNTIME_CONTRACT_REF,
    "stage_projection_surface_kind": "mag_stage_folder_lifecycle_projection",
    "stage_export_package_field": "submission_ready_package",
    "verdict_output_field": "export_verdict_refs",
    "manual_boundary_output_field": "manual_portal_boundary",
    "conformance_surface_kind": "mag_package_stage_physical_kernel_conformance_refs",
    "artifact_bundle_physical_locator_roles": [
        "stage_json_ref",
        "attempt_json_ref",
        "manifest_json_ref",
        "receipt_json_ref",
    ],
    "owner_closeout_ref_keys": [
        "owner_receipt_ref",
        "typed_blocker_ref",
        "lifecycle_receipt_ref",
    ],
    "handoff_policy": PACKAGE_LIFECYCLE_HANDOFF_POLICY,
    "authority_boundary": {
        "mag_owns_submission_export_verdict": True,
        "mag_owns_submission_ready_export_verdict": True,
        "mag_owns_export_verdict": True,
        "mag_owns_package_authority": True,
        "mag_owns_stage_folder_lifecycle_projection": True,
        "mag_owns_package_refs": True,
        "mag_owns_gap_report": True,
        "mag_owns_manual_portal_boundary": True,
        "mag_owns_lifecycle_receipt_refs": True,
        "mag_owns_physical_kernel_handoff_refs": True,
        "opl_owns_artifact_package_lifecycle_shell": True,
        "opl_owns_stage_artifact_physical_kernel": True,
        "opl_owns_locator": True,
        "opl_owns_retention_ui": True,
        "opl_role": "artifact_package_lifecycle_shell_consumer",
        "opl_can_declare_export_ready": False,
        "opl_can_declare_submission_ready": False,
        "opl_can_issue_export_verdict": False,
        "opl_can_write_artifact_body": False,
        "opl_can_write_package_content": False,
        "opl_can_hold_package_authority": False,
        "opl_can_interpret_grant_quality": False,
    },
    "projection_policy": "refs_and_gap_summary_only_no_content_payloads_no_private_material",
    "forbidden_claim_keys": [
        "opl_can_declare_export_ready",
        "opl_can_declare_submission_ready_export",
        "opl_can_issue_export_verdict",
        "opl_declares_export_ready",
        "opl_holds_export_verdict",
        "opl_submission_ready_export",
    ],
    "forbidden_write_keys": [
        "opl_can_write_artifact_body",
        "opl_can_write_package_body",
        "opl_writes_artifact_body",
        "opl_writes_package_body",
        "opl_writes_package_artifact",
    ],
}


def build_package_lifecycle_handoff_projection(
    *,
    package_refs: Mapping[str, Any],
    gap_report: Mapping[str, Any],
    export_verdict: Mapping[str, Any],
    manual_portal_boundary: Mapping[str, Any],
    lifecycle_receipt_refs: Mapping[str, Any],
) -> dict[str, Any]:
    _reject_grant_body_fields(
        package_refs,
        gap_report,
        export_verdict,
        manual_portal_boundary,
        lifecycle_receipt_refs,
    )
    try:
        verdict_refs = normalize_submission_ready_export_verdict(
            export_verdict,
            context="export_verdict",
        )
        return build_refs_only_artifact_lifecycle_handoff(
            profile=_PACKAGE_LIFECYCLE_PROFILE,
            package_refs=package_refs,
            gap_report=gap_report,
            verdict_refs=verdict_refs,
            verdict_source=export_verdict,
            manual_boundary=manual_portal_boundary,
            receipt_refs=lifecycle_receipt_refs,
        )
    except (SubmissionReadyExportVerdictError, ValueError) as exc:
        raise WorkspaceStateError(str(exc)) from exc


def _reject_grant_body_fields(*payloads: Mapping[str, Any]) -> None:
    pending: list[Any] = list(payloads)
    while pending:
        value = pending.pop()
        if isinstance(value, Mapping):
            for raw_key, child in value.items():
                if isinstance(raw_key, str):
                    key = raw_key.strip().lower().replace("-", "_").replace(" ", "_")
                    if "grant" in key and ("artifact" in key or "body" in key):
                        raise WorkspaceStateError(
                            "MAG package lifecycle handoff cannot expose grant artifact or body fields."
                        )
                pending.append(child)
        elif isinstance(value, list):
            pending.extend(value)


__all__ = [
    "PACKAGE_LIFECYCLE_HANDOFF_PROJECTION_KIND",
    "build_package_lifecycle_handoff_projection",
]
