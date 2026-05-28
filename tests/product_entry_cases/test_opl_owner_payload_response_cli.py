from __future__ import annotations

import tempfile

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryOplOwnerPayloadResponseCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_opl_owner_payload_response_dispatches_product_surface(self) -> None:
        expected_payload = {
            "surface_kind": "mag_opl_owner_payload_response",
            "status": "blocked_by_submission_ready_human_gate",
        }
        production_acceptance = {
            "surface_kind": "mag_production_acceptance_evidence.v1",
            "closure_evidence": {
                "owner_receipt_ref": "receipt:mag/production-live-acceptance/2026-05-20",
            },
        }
        external_evidence_ledger = {
            "surface_kind": "mag_external_evidence_receipt_ledger.v1",
            "grant_stage_controlled_attempt_closeout": {},
        }
        receipt_readiness = {
            "surface_kind": "mag_receipt_readiness_projection",
            "state": "receipt_refs_ready_not_quality_ready",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            production_acceptance_path = Path(tmp_dir) / "production-acceptance.json"
            external_evidence_ledger_path = Path(tmp_dir) / "external-evidence-ledger.json"
            receipt_readiness_path = Path(tmp_dir) / "receipt-readiness.json"
            production_acceptance_path.write_text(
                json.dumps(production_acceptance),
                encoding="utf-8",
            )
            external_evidence_ledger_path.write_text(
                json.dumps(external_evidence_ledger),
                encoding="utf-8",
            )
            receipt_readiness_path.write_text(json.dumps(receipt_readiness), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_opl_owner_payload_response.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "authority",
                    "owner-payload-response",
                    "--production-acceptance",
                    str(production_acceptance_path),
                    "--external-evidence-receipt-ledger",
                    str(external_evidence_ledger_path),
                    "--receipt-readiness-projection",
                    str(receipt_readiness_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_opl_owner_payload_response.assert_called_once_with(
            production_acceptance=production_acceptance,
            external_evidence_receipt_ledger=external_evidence_ledger,
            receipt_readiness_projection=receipt_readiness,
        )

    def test_manifest_sustained_consumption_payload_dispatches_product_surface(self) -> None:
        expected_payload = {
            "surface_kind": "mag_manifest_sustained_consumption_payload_response",
            "status": "blocked_by_app_operator_typed_blocker",
        }
        owner_payload_response = {
            "surface_kind": "mag_opl_owner_payload_response",
            "status": "blocked_by_submission_ready_human_gate",
        }
        workspace_receipt_scaleout_evidence = {
            "surface_kind": "mag_workspace_receipt_scaleout_evidence.v1",
        }
        operator_payload = {
            "typed_blocker_refs": [
                "typed-blocker:app/operator/mag/sustained-consumption-missing/2026-05-28"
            ]
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            owner_payload_response_path = Path(tmp_dir) / "owner-payload-response.json"
            workspace_receipt_scaleout_evidence_path = Path(tmp_dir) / "workspace-scaleout.json"
            operator_payload_path = Path(tmp_dir) / "operator-payload.json"
            owner_payload_response_path.write_text(
                json.dumps(owner_payload_response),
                encoding="utf-8",
            )
            workspace_receipt_scaleout_evidence_path.write_text(
                json.dumps(workspace_receipt_scaleout_evidence),
                encoding="utf-8",
            )
            operator_payload_path.write_text(json.dumps(operator_payload), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_manifest_sustained_consumption_payload_response.return_value = (
                    expected_payload
                )

                exit_code, stdout, stderr = self.run_cli(
                    "authority",
                    "manifest-consumption-payload",
                    "--owner-payload-response",
                    str(owner_payload_response_path),
                    "--workspace-receipt-scaleout-evidence",
                    str(workspace_receipt_scaleout_evidence_path),
                    "--operator-payload",
                    str(operator_payload_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_manifest_sustained_consumption_payload_response.assert_called_once_with(
            owner_payload_response=owner_payload_response,
            workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
            operator_payload=operator_payload,
        )
