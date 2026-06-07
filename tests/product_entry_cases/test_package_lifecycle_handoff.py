from __future__ import annotations

import json
import unittest

from med_autogrant.workspace import WorkspaceStateError


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


class ProductEntryPackageLifecycleHandoffTest(unittest.TestCase):
    def test_package_lifecycle_handoff_projects_refs_gap_verdict_and_receipts(self) -> None:
        from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
            build_package_lifecycle_handoff_projection,
        )

        projection = build_package_lifecycle_handoff_projection(
            package_refs=_package_refs(),
            gap_report={
                "gap_report_ref": "mag-gap://package-export/p3c",
                "state": "ready_for_shell",
                "summary": "All MAG package refs are ready for OPL display.",
                "gap_refs": ["mag-gap://package-export/p3c/manual-portal"],
            },
            export_verdict={
                "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                "verdict_state": "submission_ready",
                "owner": "med-autogrant",
                "source_kind": "mag_owner_receipt",
                "provenance_ref": "runtime://mag/receipts/export/p3c.json",
            },
            manual_portal_boundary={
                "manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
                "state": "human_portal_required_for_external_submit",
                "safe_action_ref": "mag-action://manual-portal/open",
            },
            lifecycle_receipt_refs={
                "lifecycle_receipt_ref": "runtime://mag/receipts/lifecycle/p3c.json",
                "owner_receipt_ref": "runtime://mag/receipts/owner/p3c.json",
            },
        )

        self.assertEqual(projection["surface_kind"], "mag_package_lifecycle_handoff_projection")
        self.assertEqual(
            projection["state"],
            "refs_ready_for_opl_artifact_package_lifecycle_shell",
        )
        self.assertEqual(
            projection["package_refs"]["submission_ready_package_ref"],
            "mag-package://submission-ready/p3c",
        )
        self.assertEqual(projection["physical_kernel_locator_refs"], _physical_kernel_locator_refs())
        self.assertEqual(
            projection["physical_kernel_conformance_refs"],
            _physical_kernel_conformance_refs(),
        )
        self.assertEqual(
            projection["stage_folder_lifecycle_projection"],
            {
                "surface_kind": "mag_stage_folder_lifecycle_projection",
                "stage_id": "package_and_submit_ready",
                "artifact_bundle": {
                    "ref": "mag-package://artifact-bundle/p3c",
                    "lifecycle_contract_role": "stage_output_artifact_ref",
                    "stage_output_role": "submission_ready_package_manifest_ref",
                    "physical_locator_roles": [
                        "stage_json_ref",
                        "attempt_json_ref",
                        "manifest_json_ref",
                        "receipt_json_ref",
                    ],
                },
                "final_package": {
                    "ref": "mag-package://final-package/p3c",
                    "lifecycle_contract_role": "canonical_promotion_ref",
                    "canonical_pointer_ref": _physical_kernel_locator_refs()["canonical_pointer_ref"],
                },
                "submission_ready_package": {
                    "ref": "mag-package://submission-ready/p3c",
                    "lifecycle_contract_role": "export_artifact_ref",
                    "export_artifact_ref": _physical_kernel_locator_refs()["export_artifact_ref"],
                },
                "physical_kernel_locators": _physical_kernel_locator_refs(),
                "physical_kernel_conformance_refs": _physical_kernel_conformance_refs(),
                "owner_receipt_or_typed_blocker_ref": "runtime://mag/receipts/owner/p3c.json",
                "missing_output_policy": "typed_blocker_required_no_opl_inference",
                "handoff_policy": "refs_manifest_missing_output_receipt_blocker_handoff_only",
                "authority_boundary": {
                    "mag_owns_package_authority": True,
                    "mag_owns_export_verdict": True,
                    "opl_can_read_artifact_body": False,
                    "opl_can_interpret_grant_quality": False,
                    "opl_can_declare_submission_ready": False,
                },
            },
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
        self.assertEqual(
            projection["gap_summary"],
            {
                "gap_report_ref": "mag-gap://package-export/p3c",
                "state": "ready_for_shell",
                "summary": "All MAG package refs are ready for OPL display.",
                "gap_refs": ["mag-gap://package-export/p3c/manual-portal"],
            },
        )
        self.assertEqual(
            projection["manual_portal_boundary"]["manual_portal_boundary_ref"],
            "mag-boundary://manual-portal/p3c",
        )
        self.assertEqual(
            projection["receipt_refs"]["lifecycle_receipt_ref"],
            "runtime://mag/receipts/lifecycle/p3c.json",
        )
        authority = projection["authority_boundary"]
        self.assertTrue(authority["mag_owns_submission_export_verdict"])
        self.assertTrue(authority["mag_owns_package_authority"])
        self.assertTrue(authority["mag_owns_stage_folder_lifecycle_projection"])
        self.assertTrue(authority["mag_owns_physical_kernel_handoff_refs"])
        self.assertTrue(authority["opl_owns_artifact_package_lifecycle_shell"])
        self.assertTrue(authority["opl_owns_stage_artifact_physical_kernel"])
        self.assertTrue(authority["opl_owns_locator"])
        self.assertTrue(authority["opl_owns_retention_ui"])
        self.assertFalse(authority["opl_can_interpret_grant_quality"])
        self.assertFalse(authority["opl_can_declare_submission_ready"])
        self.assertFalse(authority["opl_can_declare_export_ready"])
        self.assertFalse(authority["opl_can_write_artifact_body"])

    def test_package_lifecycle_handoff_requires_stage_folder_lifecycle_refs(self) -> None:
        from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
            build_package_lifecycle_handoff_projection,
        )

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
                    build_package_lifecycle_handoff_projection(
                        package_refs=package_refs,
                        gap_report={
                            "gap_report_ref": "mag-gap://package-export/p3c",
                            "summary": "missing lifecycle ref must fail closed",
                        },
                        export_verdict={
                            "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                            "verdict_state": "submission_ready",
                            "owner": "med-autogrant",
                            "source_kind": "mag_owner_receipt",
                            "provenance_ref": "runtime://mag/receipts/export/p3c.json",
                        },
                        manual_portal_boundary={
                            "manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
                        },
                        lifecycle_receipt_refs={
                            "owner_receipt_ref": "runtime://mag/receipts/owner/p3c.json",
                        },
                    )

    def test_package_lifecycle_handoff_accepts_typed_blocker_as_verdict_signature(self) -> None:
        from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
            build_package_lifecycle_handoff_projection,
        )

        projection = build_package_lifecycle_handoff_projection(
            package_refs=_package_refs(),
            gap_report={
                "gap_report_ref": "mag-gap://package-export/p3c",
                "summary": "export remains blocked by MAG typed blocker",
            },
            export_verdict={
                "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                "verdict_state": "blocked",
                "owner": "med-autogrant",
                "source_kind": "mag_owner_typed_blocker",
                "provenance_ref": "typed-blocker://mag/export/p3c",
            },
            manual_portal_boundary={
                "manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
            },
            lifecycle_receipt_refs={
                "typed_blocker_ref": "typed-blocker://mag/export/p3c",
            },
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
        from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
            build_package_lifecycle_handoff_projection,
        )

        with self.assertRaisesRegex(WorkspaceStateError, "OPL.*export"):
            build_package_lifecycle_handoff_projection(
                package_refs={**_package_refs(), "final_package_ref": "mag-package://final/p3c"},
                gap_report={
                    "gap_report_ref": "mag-gap://package-export/p3c",
                    "summary": "bad claim",
                },
                export_verdict={
                    "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                    "verdict_state": "submission_ready",
                    "owner": "med-autogrant",
                    "source_kind": "mag_owner_receipt",
                    "provenance_ref": "runtime://mag/receipts/export/p3c.json",
                    "opl_can_declare_export_ready": True,
                },
                manual_portal_boundary={
                    "manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
                },
                lifecycle_receipt_refs={
                    "lifecycle_receipt_ref": "runtime://mag/receipts/lifecycle/p3c.json",
                },
            )

    def test_package_lifecycle_handoff_rejects_export_verdict_without_owner_provenance(self) -> None:
        from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
            build_package_lifecycle_handoff_projection,
        )

        with self.assertRaisesRegex(WorkspaceStateError, "export_verdict.*owner|provenance"):
            build_package_lifecycle_handoff_projection(
                package_refs={**_package_refs(), "final_package_ref": "mag-package://final/p3c"},
                gap_report={
                    "gap_report_ref": "mag-gap://package-export/p3c",
                    "summary": "missing verdict provenance must fail closed",
                },
                export_verdict={
                    "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                    "verdict_state": "submission_ready",
                },
                manual_portal_boundary={
                    "manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
                },
                lifecycle_receipt_refs={
                    "lifecycle_receipt_ref": "runtime://mag/receipts/lifecycle/p3c.json",
                },
            )

    def test_package_lifecycle_handoff_rejects_private_body_tokens(self) -> None:
        from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
            build_package_lifecycle_handoff_projection,
        )

        with self.assertRaisesRegex(WorkspaceStateError, "package body|private evidence"):
            build_package_lifecycle_handoff_projection(
                package_refs={
                    "final_package_ref": "mag-package://final/p3c",
                    "package_body": "PRIVATE_EVIDENCE_TOKEN_DO_NOT_PROJECT",
                },
                gap_report={
                    "gap_report_ref": "mag-gap://package-export/p3c",
                    "summary": "body must fail closed",
                },
                export_verdict={
                    "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                    "verdict_state": "submission_ready",
                    "owner": "med-autogrant",
                    "source_kind": "mag_owner_receipt",
                    "provenance_ref": "runtime://mag/receipts/export/p3c.json",
                },
                manual_portal_boundary={
                    "manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
                },
                lifecycle_receipt_refs={
                    "lifecycle_receipt_ref": "runtime://mag/receipts/lifecycle/p3c.json",
                },
            )

        projection = build_package_lifecycle_handoff_projection(
            package_refs={**_package_refs(), "final_package_ref": "mag-package://final/p3c"},
            gap_report={
                "gap_report_ref": "mag-gap://package-export/p3c",
                "summary": "refs only",
            },
            export_verdict={
                "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                "verdict_state": "submission_ready",
                "owner": "med-autogrant",
                "source_kind": "mag_owner_receipt",
                "provenance_ref": "runtime://mag/receipts/export/p3c.json",
            },
            manual_portal_boundary={
                "manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
            },
            lifecycle_receipt_refs={
                "lifecycle_receipt_ref": "runtime://mag/receipts/lifecycle/p3c.json",
            },
        )
        encoded = json.dumps(projection, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("package_body", encoded)
        self.assertNotIn("private_evidence", encoded)
        self.assertNotIn("PRIVATE_EVIDENCE_TOKEN_DO_NOT_PROJECT", encoded)
