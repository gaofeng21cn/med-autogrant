from __future__ import annotations

import json

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryPackageLifecycleHandoffTest(unittest.TestCase):
    def test_package_lifecycle_handoff_projects_refs_gap_verdict_and_receipts(self) -> None:
        from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
            build_package_lifecycle_handoff_projection,
        )

        projection = build_package_lifecycle_handoff_projection(
            package_refs={
                "artifact_bundle_ref": "mag-package://artifact-bundle/p3c",
                "final_package_ref": "mag-package://final-package/p3c",
                "submission_ready_package_ref": "mag-package://submission-ready/p3c",
            },
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
        self.assertTrue(authority["opl_owns_artifact_package_lifecycle_shell"])
        self.assertTrue(authority["opl_owns_locator"])
        self.assertTrue(authority["opl_owns_retention_ui"])
        self.assertFalse(authority["opl_can_declare_export_ready"])
        self.assertFalse(authority["opl_can_write_artifact_body"])

    def test_package_lifecycle_handoff_rejects_opl_export_ready_claim(self) -> None:
        from med_autogrant.product_entry_parts.package_lifecycle_handoff import (
            build_package_lifecycle_handoff_projection,
        )

        with self.assertRaisesRegex(WorkspaceStateError, "OPL.*export"):
            build_package_lifecycle_handoff_projection(
                package_refs={"final_package_ref": "mag-package://final/p3c"},
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
                package_refs={"final_package_ref": "mag-package://final/p3c"},
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
            package_refs={"final_package_ref": "mag-package://final/p3c"},
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
