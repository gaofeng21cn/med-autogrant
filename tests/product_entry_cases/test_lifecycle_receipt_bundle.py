from __future__ import annotations

import tempfile

import json
import unittest
from pathlib import Path
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductEntryLifecycleReceiptBundleTest(unittest.TestCase):
    def test_lifecycle_receipt_bundle_groups_cleanup_restore_retention_refs_only(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.lifecycle_receipt_bundle import (
            build_lifecycle_receipt_bundle,
        )

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            receipts = [
                entry.write_lifecycle_receipt_evidence(
                    input_path=CRITIQUE_EXAMPLE_PATH,
                    operation=operation,
                    receipt_shape=receipt_shape,
                    source_ref=f"opl-lifecycle://{operation}/bundle-1",
                    closeout_summary=f"MAG lifecycle {operation} receipt for refs-only bundle.",
                    runtime_root=runtime_root,
                    receipt_id=f"bundle-{operation}",
                )["lifecycle_receipt_evidence"]
                for operation, receipt_shape in (
                    ("cleanup", "typed_blocker"),
                    ("restore", "domain_owner_receipt"),
                    ("retention", "no_regression_evidence"),
                )
            ]

        payload = build_lifecycle_receipt_bundle(lifecycle_receipt_evidence_items=receipts)
        bundle = payload["lifecycle_receipt_bundle"]

        self.assertEqual(bundle["surface_kind"], "mag_lifecycle_receipt_bundle")
        self.assertEqual(bundle["state"], "cleanup_restore_retention_refs_ready_for_opl_shell")
        self.assertEqual(bundle["summary"]["item_count"], 3)
        self.assertEqual(
            bundle["summary"]["operations_present"],
            ["cleanup", "restore", "retention"],
        )
        self.assertEqual(bundle["summary"]["missing_operations"], [])
        self.assertEqual(bundle["summary"]["typed_blocker_count"], 1)
        self.assertEqual(bundle["summary"]["no_regression_evidence_count"], 1)
        self.assertEqual(
            {item["operation"] for item in bundle["items"]},
            {"cleanup", "restore", "retention"},
        )
        self.assertEqual(
            set(bundle["receipt_refs"].values()),
            {receipt["receipt_instance_ref"] for receipt in receipts},
        )
        self.assertTrue(bundle["authority_boundary"]["mag_lifecycle_receipt_authority"])
        self.assertFalse(bundle["authority_boundary"]["opl_can_delete_grant_artifacts"])
        self.assertFalse(bundle["authority_boundary"]["opl_can_restore_grant_artifacts"])
        self.assertFalse(bundle["authority_boundary"]["opl_can_set_retention_for_grant_truth"])
        self.assertFalse(bundle["claims"]["claims_production_long_run_soak_complete"])
        self.assertFalse(bundle["claims"]["claims_submission_ready_export"])
        self.assertFalse(bundle["forbidden_write_proof"]["grant_artifact_written"])
        self.assertFalse(bundle["forbidden_write_proof"]["memory_body_written"])

    def test_lifecycle_receipt_bundle_rejects_missing_operation(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.lifecycle_receipt_bundle import (
            build_lifecycle_receipt_bundle,
        )

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt = entry.write_lifecycle_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                operation="cleanup",
                receipt_shape="typed_blocker",
                source_ref="opl-lifecycle://cleanup/missing",
                closeout_summary="Only cleanup exists.",
                runtime_root=Path(tmp_dir) / "runtime-state",
                receipt_id="missing-cleanup",
            )["lifecycle_receipt_evidence"]

        with self.assertRaisesRegex(WorkspaceStateError, "restore"):
            build_lifecycle_receipt_bundle(lifecycle_receipt_evidence_items=[receipt])

    def test_lifecycle_receipt_bundle_rejects_artifact_mutation_or_ready_claims(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.lifecycle_receipt_bundle import (
            build_lifecycle_receipt_bundle,
        )

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            receipts = [
                entry.write_lifecycle_receipt_evidence(
                    input_path=CRITIQUE_EXAMPLE_PATH,
                    operation=operation,
                    receipt_shape="domain_owner_receipt",
                    source_ref=f"opl-lifecycle://{operation}/invalid",
                    closeout_summary="Lifecycle receipt fixture.",
                    runtime_root=runtime_root,
                    receipt_id=f"invalid-{operation}",
                )["lifecycle_receipt_evidence"]
                for operation in ("cleanup", "restore", "retention")
            ]
        receipts[0]["forbidden_write_proof"]["grant_artifact_written"] = True

        with self.assertRaisesRegex(WorkspaceStateError, "forbidden write"):
            build_lifecycle_receipt_bundle(lifecycle_receipt_evidence_items=receipts)

        receipts[0]["forbidden_write_proof"]["grant_artifact_written"] = False
        receipts[1]["claims_submission_ready_export"] = True
        with self.assertRaisesRegex(WorkspaceStateError, "readiness"):
            build_lifecycle_receipt_bundle(lifecycle_receipt_evidence_items=receipts)

    def test_lifecycle_receipt_bundle_does_not_project_private_body_text(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.lifecycle_receipt_bundle import (
            build_lifecycle_receipt_bundle,
        )

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            receipts = []
            for operation in ("cleanup", "restore", "retention"):
                receipt = entry.write_lifecycle_receipt_evidence(
                    input_path=CRITIQUE_EXAMPLE_PATH,
                    operation=operation,
                    receipt_shape="domain_owner_receipt",
                    source_ref=f"opl-lifecycle://{operation}/no-leak",
                    closeout_summary="SECRET_LIFECYCLE_BODY must not be projected.",
                    runtime_root=runtime_root,
                    receipt_id=f"no-leak-{operation}",
                )["lifecycle_receipt_evidence"]
                receipt["grant_artifact_body"] = "SECRET_ARTIFACT_BODY"
                receipts.append(receipt)

        bundle = build_lifecycle_receipt_bundle(
            lifecycle_receipt_evidence_items=receipts,
        )["lifecycle_receipt_bundle"]
        serialized = json.dumps(bundle, ensure_ascii=False, sort_keys=True)

        self.assertNotIn("SECRET_LIFECYCLE_BODY", serialized)
        self.assertNotIn("SECRET_ARTIFACT_BODY", serialized)
        self.assertNotIn("closeout_summary", serialized)
        self.assertNotIn("grant_artifact_body", serialized)
