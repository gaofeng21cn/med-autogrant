from __future__ import annotations

import tempfile

import json
import unittest
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from med_autogrant.cli import main
from med_autogrant.workspace import WorkspaceStateError
from support.cli import public_cli_argv


def _owner_receipt() -> dict[str, object]:
    return {
        "surface_kind": "mag_owner_receipt_evidence",
        "receipt_id": "mag.owner.receipt.package-closeout",
        "receipt_shape": "domain_owner_receipt",
        "receipt_ref": "runtime://mag/receipts/owner/package-closeout.json",
        "receipt_instance_ref": "/runtime/receipts/owner/package-closeout.json",
        "stage_id": "package_and_submit_ready",
    }


def _memory_receipt() -> dict[str, object]:
    return {
        "surface_kind": "mag_domain_memory_runtime_receipt_evidence",
        "receipt_id": "mag.memory.receipt.accepted-risk",
        "receipt_ref": "runtime://mag/receipts/memory/accepted-risk.json",
        "receipt_instance_ref": "/runtime/receipts/memory/accepted-risk.json",
        "decision": "accepted",
        "decision_owner": "med-autogrant",
        "contains_memory_body": False,
        "contains_grant_artifact_content": False,
    }


def _package_lifecycle_projection() -> dict[str, object]:
    return {
        "package_lifecycle_handoff_projection": {
            "surface_kind": "mag_package_lifecycle_handoff_projection",
            "receipt_refs": {
                "lifecycle_receipt_ref": "runtime://mag/receipts/package/lifecycle.json",
                "owner_receipt_ref": "runtime://mag/receipts/package/owner.json",
            },
            "export_verdict_refs": {
                "export_verdict_ref": "mag-verdict://submission-ready-export/p3c",
                "verdict_state": "submission_ready",
            },
        }
    }


def _cleanup_restore_retention_bundle() -> dict[str, object]:
    return {
        "lifecycle_receipt_bundle": {
            "surface_kind": "mag_lifecycle_receipt_bundle",
            "receipt_refs": {
                "cleanup": "runtime://mag/receipts/lifecycle/cleanup.json",
                "restore": "runtime://mag/receipts/lifecycle/restore.json",
                "retention": "runtime://mag/receipts/lifecycle/retention.json",
            },
            "items": [
                {"operation": "cleanup", "receipt_shape": "typed_blocker"},
                {"operation": "restore", "receipt_shape": "domain_owner_receipt"},
                {"operation": "retention", "receipt_shape": "no_regression_evidence"},
            ],
        }
    }


class ProductEntryReceiptReadinessTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_missing_receipts_project_missing_without_quality_authority(self) -> None:
        from med_autogrant.product_entry_parts.receipt_readiness import (
            build_receipt_readiness_projection,
        )

        projection = build_receipt_readiness_projection(
            owner_receipt_evidence_items=[],
            memory_receipt_items=[],
            package_lifecycle_items=[],
            lifecycle_receipt_items=[],
        )

        self.assertEqual(projection["surface_kind"], "mag_receipt_readiness_projection")
        self.assertEqual(projection["state"], "receipts_missing")
        self.assertEqual(projection["missing_categories"], projection["required_categories"])
        self.assertEqual(projection["summary"]["total_receipt_ref_count"], 0)
        self.assertTrue(projection["authority_boundary"]["refs_only_projection"])
        self.assertFalse(projection["authority_boundary"]["can_declare_fundability_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_quality_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_export_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_submission_ready"])

    def test_partial_receipt_coverage_keeps_missing_categories_open(self) -> None:
        from med_autogrant.product_entry_parts.receipt_readiness import (
            build_receipt_readiness_projection,
        )

        projection = build_receipt_readiness_projection(
            owner_receipt_evidence_items=[_owner_receipt()],
            memory_receipt_items=[_memory_receipt()],
            package_lifecycle_items=[],
            lifecycle_receipt_items=[],
        )

        self.assertEqual(projection["state"], "partial_receipt_coverage")
        self.assertEqual(
            projection["missing_categories"],
            ["package_export_lifecycle", "cleanup_restore_retention_lifecycle"],
        )
        self.assertTrue(projection["categories"]["owner_receipt"]["covered"])
        self.assertTrue(projection["categories"]["memory_accept_reject"]["covered"])
        self.assertFalse(projection["categories"]["package_export_lifecycle"]["covered"])

    def test_complete_receipt_refs_are_ready_but_not_quality_ready(self) -> None:
        from med_autogrant.product_entry_parts.receipt_readiness import (
            build_receipt_readiness_projection,
        )

        projection = build_receipt_readiness_projection(
            owner_receipt_evidence_items=[{"owner_receipt_evidence": _owner_receipt()}],
            memory_receipt_items=[_memory_receipt()],
            package_lifecycle_items=[_package_lifecycle_projection()],
            lifecycle_receipt_items=[_cleanup_restore_retention_bundle()],
        )

        self.assertEqual(projection["state"], "receipt_refs_ready_not_quality_ready")
        self.assertEqual(projection["missing_categories"], [])
        self.assertEqual(projection["summary"]["covered_category_count"], 4)
        self.assertIn(
            "runtime://mag/receipts/owner/package-closeout.json",
            projection["receipt_refs"]["owner_receipt"],
        )
        self.assertIn(
            "runtime://mag/receipts/package/lifecycle.json",
            projection["receipt_refs"]["package_export_lifecycle"],
        )
        self.assertIn(
            "runtime://mag/receipts/lifecycle/cleanup.json",
            projection["receipt_refs"]["cleanup_restore_retention_lifecycle"],
        )
        self.assertFalse(projection["authority_boundary"]["can_declare_quality_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_submission_ready"])

        encoded = json.dumps(projection, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("PRIVATE_BODY_TOKEN", encoded)
        self.assertNotIn("proposal_text_body", encoded)

    def test_forbidden_body_or_ready_claim_fails_closed(self) -> None:
        from med_autogrant.product_entry_parts.receipt_readiness import (
            build_receipt_readiness_projection,
        )

        owner_receipt_with_body = dict(_owner_receipt())
        owner_receipt_with_body["grant_artifact_body"] = "PRIVATE_BODY_TOKEN"
        with self.assertRaises(WorkspaceStateError):
            build_receipt_readiness_projection(
                owner_receipt_evidence_items=[owner_receipt_with_body],
                memory_receipt_items=[],
                package_lifecycle_items=[],
                lifecycle_receipt_items=[],
            )

        memory_receipt_with_ready_claim = dict(_memory_receipt())
        memory_receipt_with_ready_claim["submission_ready"] = True
        with self.assertRaises(WorkspaceStateError):
            build_receipt_readiness_projection(
                owner_receipt_evidence_items=[],
                memory_receipt_items=[memory_receipt_with_ready_claim],
                package_lifecycle_items=[],
                lifecycle_receipt_items=[],
            )

    def test_receipt_readiness_dispatches_authority_target(self) -> None:
        expected_payload = {
            "surface_kind": "mag_receipt_readiness_projection",
            "state": "receipt_refs_ready_not_quality_ready",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            owner_receipt_path = Path(tmp_dir) / "owner-receipt.json"
            memory_receipt_path = Path(tmp_dir) / "memory-receipt.json"
            package_lifecycle_path = Path(tmp_dir) / "package-lifecycle.json"
            lifecycle_receipt_path = Path(tmp_dir) / "lifecycle-receipt.json"
            owner_receipt = _owner_receipt()
            memory_receipt = _memory_receipt()
            package_lifecycle = _package_lifecycle_projection()
            lifecycle_receipt = _cleanup_restore_retention_bundle()
            owner_receipt_path.write_text(json.dumps(owner_receipt), encoding="utf-8")
            memory_receipt_path.write_text(json.dumps(memory_receipt), encoding="utf-8")
            package_lifecycle_path.write_text(json.dumps(package_lifecycle), encoding="utf-8")
            lifecycle_receipt_path.write_text(json.dumps(lifecycle_receipt), encoding="utf-8")

            with patch(
                "med_autogrant.cli_parts.handlers.build_receipt_readiness_projection",
                return_value=expected_payload,
            ) as build_receipt_readiness:

                exit_code, stdout, stderr = self.run_cli(
                    "authority",
                    "receipt-readiness",
                    "--owner-receipt-evidence",
                    str(owner_receipt_path),
                    "--memory-receipt",
                    str(memory_receipt_path),
                    "--package-lifecycle",
                    str(package_lifecycle_path),
                    "--lifecycle-receipt",
                    str(lifecycle_receipt_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        build_receipt_readiness.assert_called_once_with(
            owner_receipt_evidence_items=[owner_receipt],
            memory_receipt_items=[memory_receipt],
            package_lifecycle_items=[package_lifecycle],
            lifecycle_receipt_items=[lifecycle_receipt],
        )
