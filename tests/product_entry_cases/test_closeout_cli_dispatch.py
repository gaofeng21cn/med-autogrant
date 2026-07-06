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
from support.cli import public_cli_argv


class ProductEntryCloseoutCliDispatchTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_codex_stage_receipts_dispatches_authority_target(self) -> None:
        expected_payload = {
            "surface_kind": "mag_codex_stage_execution_receipt_bundle",
            "state": "codex_stage_receipts_ready_not_quality_ready",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            execution_attempt_path = Path(tmp_dir) / "execution.json"
            review_attempt_path = Path(tmp_dir) / "review.json"
            execution_attempt = {
                "attempt_id": "attempt-critique-001",
                "executor": "codex_cli",
                "invocation_ref": "codex://invocations/critique-001",
                "task_record_ref": "runtime://opl/stage-attempts/critique-001.json",
                "receipt_ref": "runtime://mag/receipts/stage/critique-001.json",
                "stage_pack_ref": "agent/prompts/review_and_rebuttal.md",
                "output_artifact_ref": "runtime://mag/artifacts/critique-001.json",
            }
            review_attempt = {
                "review_attempt_id": "review-critique-001",
                "reviewer_executor": "codex_cli",
                "review_invocation_ref": "codex://invocations/review-critique-001",
                "review_task_record_ref": "runtime://opl/stage-attempts/review-critique-001.json",
                "review_receipt_ref": "runtime://mag/receipts/review/review-critique-001.json",
                "review_artifact_ref": "runtime://mag/artifacts/review-critique-001.json",
                "review_target_attempt_id": "attempt-critique-001",
                "independent_context": True,
                "shared_context_with_execution": False,
            }
            execution_attempt_path.write_text(json.dumps(execution_attempt), encoding="utf-8")
            review_attempt_path.write_text(json.dumps(review_attempt), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_codex_stage_execution_receipt_bundle.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "authority",
                    "stage-receipts",
                    "--stage-id",
                    "review_and_rebuttal",
                    "--execution-attempt",
                    str(execution_attempt_path),
                    "--review-attempt",
                    str(review_attempt_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_codex_stage_execution_receipt_bundle.assert_called_once_with(
            stage_id="review_and_rebuttal",
            execution_attempts=[execution_attempt],
            review_attempts=[review_attempt],
        )

    def test_physical_morphology_guard_dispatches_authority_target(self) -> None:
        expected_payload = {
            "surface_kind": "mag_physical_morphology_guard_projection",
            "state": "allowed_evidence_gated",
            "public_readback_ref": "authority morphology-guard",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_item_path = Path(tmp_dir) / "source-item.json"
            source_item = {
                "path": "src/med_autogrant/product_entry.py",
                "module_id": "product_entry",
                "declared_role": "domain_handler_target",
                "evidence_refs": ["/product_entry_manifest/physical_morphology/product_entry"],
                "forbidden_role_flags": {
                    "scheduler_daemon_owner": False,
                    "attempt_ledger_owner": False,
                    "local_journal_owner": False,
                    "generic_runtime_owner": False,
                    "app_workbench_owner": False,
                    "compatibility_alias_owner": False,
                },
            }
            source_item_path.write_text(json.dumps(source_item), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_physical_morphology_guard_projection.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "authority",
                    "morphology-guard",
                    "--source-item",
                    str(source_item_path),
                    "--external-evidence-ref",
                    "opl://receipts/mag/physical-morphology/parity.json",
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload, expected_payload)
        self.assertEqual(payload["public_readback_ref"], "authority morphology-guard")
        product_entry.build_physical_morphology_guard_projection.assert_called_once_with(
            source_items=[source_item],
            external_evidence_refs=["opl://receipts/mag/physical-morphology/parity.json"],
        )

    def test_executor_first_closeout_bundle_dispatches_authority_target(self) -> None:
        expected_payload = {
            "surface_kind": "mag_executor_first_closeout_bundle",
            "state": "refs_ready_not_quality_ready",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            codex_bundle_path = Path(tmp_dir) / "codex-bundle.json"
            operator_projection_path = Path(tmp_dir) / "operator.json"
            physical_guard_path = Path(tmp_dir) / "physical.json"
            evidence_ledger_path = Path(tmp_dir) / "evidence-ledger.json"
            receipt_readiness_path = Path(tmp_dir) / "receipt-readiness.json"
            codex_bundle = {
                "surface_kind": "mag_codex_stage_execution_receipt_bundle",
                "state": "codex_stage_receipts_ready_not_quality_ready",
            }
            operator_projection = {
                "surface_kind": "mag_operator_closeout_readiness_projection",
                "state": "operator_closeout_refs_ready_not_quality_ready",
            }
            physical_guard = {
                "surface_kind": "mag_physical_morphology_guard_projection",
                "state": "allowed_external_evidence_present",
            }
            evidence_ledger = {
                "surface_kind": "mag_external_evidence_consumption_ledger",
                "state": "consumed_complete",
            }
            receipt_readiness = {
                "surface_kind": "mag_receipt_readiness_projection",
                "state": "receipt_refs_ready_not_quality_ready",
            }
            codex_bundle_path.write_text(json.dumps(codex_bundle), encoding="utf-8")
            operator_projection_path.write_text(json.dumps(operator_projection), encoding="utf-8")
            physical_guard_path.write_text(json.dumps(physical_guard), encoding="utf-8")
            evidence_ledger_path.write_text(json.dumps(evidence_ledger), encoding="utf-8")
            receipt_readiness_path.write_text(json.dumps(receipt_readiness), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_executor_first_closeout_bundle.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "authority",
                    "executor-closeout-bundle",
                    "--codex-stage-execution-receipt-bundle",
                    str(codex_bundle_path),
                    "--operator-closeout-readiness-projection",
                    str(operator_projection_path),
                    "--physical-morphology-guard-projection",
                    str(physical_guard_path),
                    "--external-evidence-consumption-ledger",
                    str(evidence_ledger_path),
                    "--receipt-readiness-projection",
                    str(receipt_readiness_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_executor_first_closeout_bundle.assert_called_once_with(
            codex_stage_execution_receipt_bundle=codex_bundle,
            operator_closeout_readiness_projection=operator_projection,
            physical_morphology_guard_projection=physical_guard,
            external_evidence_consumption_ledger=evidence_ledger,
            receipt_readiness_projection=receipt_readiness,
        )
