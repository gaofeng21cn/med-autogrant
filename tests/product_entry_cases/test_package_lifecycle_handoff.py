from __future__ import annotations

import json
import unittest

from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
    build_package_lifecycle_handoff_projection,
)
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import assert_false_keys, assert_path_values, assert_true_keys


def _physical_kernel_locator_refs() -> dict[str, str]:
    stage_root = (
        "runtime-state/domains/med-autogrant/deliverables/local-program/grant-run-p3c/"
        "workspace-p3c/draft-p3c/stages/package_and_submit_ready"
    )
    attempt_root = f"{stage_root}/attempts/attempt-p3c"
    return {
        "stage_json_ref": f"{attempt_root}/stage.json",
        "attempt_json_ref": f"{attempt_root}/attempt.json",
        "manifest_json_ref": f"{attempt_root}/manifest.json",
        "receipt_json_ref": f"{attempt_root}/receipts/receipt.json",
        "current_json_ref": f"{stage_root}/current.json",
        "latest_json_ref": f"{stage_root}/latest.json",
        "canonical_pointer_ref": f"{stage_root}/canonical/current.json",
        "export_artifact_ref": f"{stage_root}/exports/submission_ready_package_manifest_ref.json",
        "lineage_events_ref": f"{stage_root}/lineage/events.jsonl",
        "lineage_graph_ref": f"{stage_root}/lineage/graph.json",
        "retention_policy_ref": f"{stage_root}/retention/policy.json",
        "conformance_summary_ref": (
            "opl-conformance://stage-artifact/med-autogrant/"
            "package_and_submit_ready/attempt-p3c"
        ),
    }


def _package_refs() -> dict[str, str]:
    return {
        "artifact_bundle_ref": "mag-package://artifact-bundle/p3c",
        "final_package_ref": "mag-package://final-package/p3c",
        "submission_ready_package_ref": "mag-package://submission-ready/p3c",
        **_physical_kernel_locator_refs(),
    }


def _physical_kernel_conformance_refs() -> dict[str, str | bool]:
    return {
        "surface_kind": "mag_package_stage_physical_kernel_conformance_refs",
        "opl_contract_ref": "contracts/opl-framework/stage-artifact-runtime-contract.json",
        "opl_conformance_contract_ref": (
            "contracts/opl-framework/stage-artifact-runtime-contract.json#/conformance_gate"
        ),
        "conformance_summary_ref": _physical_kernel_locator_refs()["conformance_summary_ref"],
        "domain_readiness_claim": False,
    }


def _gap_report(**overrides: object) -> dict[str, object]:
    return {
        "gap_report_ref": "mag-gap://package-export/p3c",
        "summary": "All MAG package refs are ready for OPL display.",
        **overrides,
    }


def _export_verdict(**overrides: object) -> dict[str, object]:
    return {
        "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
        "verdict_state": "submission_ready",
        "owner": "med-autogrant",
        "source_kind": "mag_owner_receipt",
        "provenance_ref": "runtime://mag/receipts/export/p3c.json",
        **overrides,
    }


def _manual_portal_boundary(**overrides: object) -> dict[str, object]:
    return {
        "manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
        **overrides,
    }


def _lifecycle_receipt_refs(**overrides: object) -> dict[str, object]:
    return {
        "lifecycle_receipt_ref": "runtime://mag/receipts/lifecycle/p3c.json",
        **overrides,
    }


def _build_projection(**overrides: object) -> dict[str, object]:
    args: dict[str, object] = {
        "package_refs": _package_refs(),
        "gap_report": _gap_report(),
        "export_verdict": _export_verdict(),
        "manual_portal_boundary": _manual_portal_boundary(),
        "lifecycle_receipt_refs": _lifecycle_receipt_refs(),
    }
    args.update(overrides)
    return build_package_lifecycle_handoff_projection(**args)  # type: ignore[arg-type]


class ProductEntryPackageLifecycleHandoffTest(unittest.TestCase):
    def test_package_lifecycle_handoff_projects_refs_gap_verdict_and_receipts(self) -> None:
        projection = _build_projection(
            gap_report=_gap_report(
                state="ready_for_shell",
                summary="All MAG package refs are ready for OPL display.",
                gap_refs=["mag-gap://package-export/p3c/manual-portal"],
            ),
            manual_portal_boundary=_manual_portal_boundary(
                state="human_portal_required_for_external_submit",
                safe_action_ref="mag-action://manual-portal/open",
            ),
            lifecycle_receipt_refs=_lifecycle_receipt_refs(
                owner_receipt_ref="runtime://mag/receipts/owner/p3c.json",
            ),
        )

        assert_path_values(
            self,
            projection,
            {
                "surface_kind": "mag_package_lifecycle_handoff_projection",
                "state": "refs_ready_for_opl_artifact_package_lifecycle_shell",
                "package_refs.submission_ready_package_ref": "mag-package://submission-ready/p3c",
                "stage_folder_lifecycle_projection.surface_kind": "mag_stage_folder_lifecycle_projection",
                "stage_folder_lifecycle_projection.stage_id": "package_and_submit_ready",
                "stage_folder_lifecycle_projection.artifact_bundle.ref": "mag-package://artifact-bundle/p3c",
                "stage_folder_lifecycle_projection.final_package.ref": "mag-package://final-package/p3c",
                "stage_folder_lifecycle_projection.submission_ready_package.ref": "mag-package://submission-ready/p3c",
                "stage_folder_lifecycle_projection.owner_receipt_or_typed_blocker_ref": "runtime://mag/receipts/owner/p3c.json",
                "stage_folder_lifecycle_projection.missing_output_policy": "typed_blocker_required_no_opl_inference",
                "export_verdict_refs.verdict_state": "submission_ready",
                "gap_summary.state": "ready_for_shell",
                "manual_portal_boundary.manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
                "receipt_refs.lifecycle_receipt_ref": "runtime://mag/receipts/lifecycle/p3c.json",
            },
        )
        self.assertEqual(projection["physical_kernel_locator_refs"], _physical_kernel_locator_refs())
        self.assertEqual(
            projection["physical_kernel_conformance_refs"],
            _physical_kernel_conformance_refs(),
        )
        self.assertEqual(
            projection["stage_folder_lifecycle_projection"]["artifact_bundle"]["physical_locator_roles"],
            ["stage_json_ref", "attempt_json_ref", "manifest_json_ref", "receipt_json_ref"],
        )
        self.assertEqual(
            projection["export_verdict_refs"],
            {
                "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                "verdict_state": "submission_ready",
                "owner": "med-autogrant",
                "source_kind": "mag_owner_receipt",
                "provenance_ref": "runtime://mag/receipts/export/p3c.json",
            },
        )
        authority = projection["authority_boundary"]
        assert_true_keys(self, authority, ("mag_owns_submission_export_verdict", "mag_owns_package_authority", "mag_owns_stage_folder_lifecycle_projection", "mag_owns_physical_kernel_handoff_refs", "opl_owns_artifact_package_lifecycle_shell", "opl_owns_stage_artifact_physical_kernel", "opl_owns_locator", "opl_owns_retention_ui"))
        assert_false_keys(self, authority, ("opl_can_interpret_grant_quality", "opl_can_declare_submission_ready", "opl_can_declare_export_ready", "opl_can_write_artifact_body"))

    def test_package_lifecycle_handoff_requires_stage_folder_lifecycle_refs(self) -> None:
        for missing_key in (
            "artifact_bundle_ref",
            "final_package_ref",
            "submission_ready_package_ref",
            "stage_json_ref",
            "conformance_summary_ref",
        ):
            with self.subTest(missing_key=missing_key):
                package_refs = _package_refs()
                package_refs.pop(missing_key)

                with self.assertRaisesRegex(WorkspaceStateError, missing_key):
                    _build_projection(
                        package_refs=package_refs,
                        gap_report=_gap_report(summary="missing lifecycle ref must fail closed"),
                        lifecycle_receipt_refs=_lifecycle_receipt_refs(
                            owner_receipt_ref="runtime://mag/receipts/owner/p3c.json"
                        ),
                    )

    def test_package_lifecycle_handoff_accepts_typed_blocker_as_verdict_signature(self) -> None:
        projection = _build_projection(
            gap_report=_gap_report(summary="export remains blocked by MAG typed blocker"),
            export_verdict=_export_verdict(
                verdict_state="blocked",
                source_kind="mag_owner_typed_blocker",
                provenance_ref="typed-blocker://mag/export/p3c",
            ),
            lifecycle_receipt_refs=_lifecycle_receipt_refs(typed_blocker_ref="typed-blocker://mag/export/p3c"),
        )

        self.assertEqual(
            projection["export_verdict_refs"]["source_kind"],
            "mag_owner_typed_blocker",
        )
        self.assertEqual(
            projection["stage_folder_lifecycle_projection"]["owner_receipt_or_typed_blocker_ref"],
            "typed-blocker://mag/export/p3c",
        )

    def test_package_lifecycle_handoff_rejects_opl_export_ready_claim(self) -> None:
        with self.assertRaisesRegex(WorkspaceStateError, "cannot claim domain export"):
            _build_projection(
                package_refs={**_package_refs(), "final_package_ref": "mag-package://final/p3c"},
                gap_report=_gap_report(summary="bad claim"),
                export_verdict=_export_verdict(opl_can_declare_export_ready=True),
            )

    def test_package_lifecycle_handoff_rejects_export_verdict_without_owner_provenance(self) -> None:
        with self.assertRaisesRegex(WorkspaceStateError, "export_verdict.*owner|provenance"):
            _build_projection(
                package_refs={**_package_refs(), "final_package_ref": "mag-package://final/p3c"},
                gap_report=_gap_report(summary="missing verdict provenance must fail closed"),
                export_verdict={
                    "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                    "verdict_state": "submission_ready",
                },
            )

    def test_package_lifecycle_handoff_rejects_private_body_tokens(self) -> None:
        with self.assertRaisesRegex(WorkspaceStateError, "package body|private evidence"):
            _build_projection(
                package_refs={
                    "final_package_ref": "mag-package://final/p3c",
                    "package_body": "PRIVATE_EVIDENCE_TOKEN_DO_NOT_PROJECT",
                },
                gap_report=_gap_report(summary="body must fail closed"),
            )

        projection = _build_projection(
            package_refs={**_package_refs(), "final_package_ref": "mag-package://final/p3c"},
            gap_report=_gap_report(summary="refs only"),
        )
        encoded = json.dumps(projection, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("package_body", encoded)
        self.assertNotIn("private_evidence", encoded)
        self.assertNotIn("PRIVATE_EVIDENCE_TOKEN_DO_NOT_PROJECT", encoded)
