from __future__ import annotations

import tempfile

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryHostedReceiptVerificationTest(unittest.TestCase):
    def test_hosted_receipt_verification_matches_opl_attempt_to_mag_receipt_refs(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/hosted-attempt/review-1",
                closeout_summary="Focused OPL-hosted attempt returned MAG no-regression evidence.",
                runtime_root=Path(tmp_dir) / "runtime-state",
                receipt_id="hosted-review-1",
            )["owner_receipt_evidence"]
            sidecar_closeout_result = {
                "surface_kind": "sidecar_stage_attempt_closeout_result",
                "receipt_ref": receipt["receipt_instance_ref"],
                "receipt_refs": {
                    "owner_receipt_ref": receipt["receipt_instance_ref"],
                    "no_regression_evidence_ref": receipt["receipt_instance_ref"],
                },
            }

        payload = entry.build_focused_hosted_receipt_verification(
            owner_receipt_evidence=receipt,
            opl_attempt_evidence={
                "surface_kind": "opl_hosted_stage_attempt_evidence",
                "attempt_ref": "opl-attempt://mag/review-1",
                "stage_id": "review_and_rebuttal",
                "ledger_ref": "opl-ledger://mag/hosted-attempt/review-1",
                "domain_breakdown": {
                    "target_domain_id": "med-autogrant",
                    "owner_receipt_ref": receipt["receipt_instance_ref"],
                    "no_regression_evidence_refs": [receipt["receipt_instance_ref"]],
                    "typed_blocker_refs": [],
                },
                "provider_completion": {
                    "completed": True,
                    "completion_ref": "opl-provider://attempt/review-1",
                },
            },
            sidecar_closeout_result=sidecar_closeout_result,
        )

        verification = payload["focused_hosted_receipt_verification"]
        self.assertEqual(verification["surface_kind"], "mag_focused_hosted_receipt_verification")
        self.assertEqual(verification["state"], "focused_hosted_receipt_refs_verified_not_live_soak")
        self.assertEqual(verification["stage_id"], "review_and_rebuttal")
        self.assertTrue(verification["matches"]["owner_receipt_ref_matches_opl"])
        self.assertTrue(verification["matches"]["ledger_ref_matches_receipt_source"])
        self.assertTrue(verification["matches"]["receipt_ref_matches_sidecar"])
        self.assertEqual(
            verification["allowed_result"]["result_shape"],
            "no_regression_evidence",
        )
        self.assertEqual(
            verification["allowed_result"]["no_regression_evidence_refs"],
            [receipt["receipt_instance_ref"]],
        )
        self.assertFalse(verification["claims"]["claims_production_long_run_soak_complete"])
        self.assertFalse(verification["claims"]["claims_grant_fundability_ready"])
        self.assertFalse(verification["claims"]["claims_authoring_quality_ready"])
        self.assertFalse(verification["claims"]["claims_submission_ready_export"])
        self.assertFalse(verification["authority_boundary"]["mag_implements_opl_provider"])
        self.assertFalse(verification["authority_boundary"]["mag_writes_opl_ledger"])
        self.assertFalse(verification["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(verification["forbidden_write_proof"]["memory_body_written"])

    def test_hosted_receipt_verification_keeps_typed_blocker_as_blocker_not_ready(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="typed_blocker",
                stage_id="package_and_submit_ready",
                source_ref="opl-ledger://mag/hosted-attempt/package-1",
                closeout_summary="Focused OPL-hosted attempt found a MAG package blocker.",
                runtime_root=Path(tmp_dir) / "runtime-state",
                receipt_id="hosted-package-blocker-1",
            )["owner_receipt_evidence"]

        payload = entry.build_focused_hosted_receipt_verification(
            owner_receipt_evidence=receipt,
            opl_attempt_evidence={
                "surface_kind": "opl_hosted_stage_attempt_evidence",
                "attempt_ref": "opl-attempt://mag/package-1",
                "stage_id": "package_and_submit_ready",
                "ledger_ref": "opl-ledger://mag/hosted-attempt/package-1",
                "domain_breakdown": {
                    "target_domain_id": "med-autogrant",
                    "owner_receipt_ref": receipt["receipt_instance_ref"],
                    "typed_blocker_refs": [receipt["receipt_instance_ref"]],
                    "no_regression_evidence_refs": [],
                },
            },
        )

        verification = payload["focused_hosted_receipt_verification"]
        self.assertEqual(verification["allowed_result"]["result_shape"], "typed_blocker")
        self.assertEqual(
            verification["allowed_result"]["typed_blocker_refs"],
            [receipt["receipt_instance_ref"]],
        )
        self.assertEqual(
            verification["focused_status"],
            "focused_typed_blocker_verified",
        )
        self.assertFalse(verification["claims"]["claims_submission_ready_export"])
        self.assertFalse(verification["claims"]["claims_production_long_run_soak_complete"])

    def test_hosted_receipt_verification_rejects_provider_completion_as_ready_claim(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/hosted-attempt/bad-ready",
                closeout_summary="Provider completion must not become grant readiness.",
                runtime_root=Path(tmp_dir) / "runtime-state",
                receipt_id="hosted-bad-ready",
            )["owner_receipt_evidence"]

        with self.assertRaisesRegex(WorkspaceStateError, "grant readiness"):
            entry.build_focused_hosted_receipt_verification(
                owner_receipt_evidence=receipt,
                opl_attempt_evidence={
                    "surface_kind": "opl_hosted_stage_attempt_evidence",
                    "attempt_ref": "opl-attempt://mag/bad-ready",
                    "stage_id": "review_and_rebuttal",
                    "ledger_ref": "opl-ledger://mag/hosted-attempt/bad-ready",
                    "domain_breakdown": {
                        "target_domain_id": "med-autogrant",
                        "owner_receipt_ref": receipt["receipt_instance_ref"],
                        "no_regression_evidence_refs": [receipt["receipt_instance_ref"]],
                    },
                    "provider_completion": {
                        "completed": True,
                        "grant_ready": True,
                    },
                },
            )

    def test_cli_hosted_receipt_verification_reads_json_evidence_files(self) -> None:
        from med_autogrant.cli import main
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/hosted-attempt/cli-1",
                closeout_summary="CLI focused verification fixture.",
                runtime_root=tmp_path / "runtime-state",
                receipt_id="hosted-cli-1",
            )["owner_receipt_evidence"]
            owner_receipt_path = tmp_path / "owner-receipt.json"
            opl_attempt_path = tmp_path / "opl-attempt.json"
            sidecar_closeout_path = tmp_path / "sidecar-closeout.json"
            owner_receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            opl_attempt_path.write_text(
                json.dumps(
                    {
                        "surface_kind": "opl_hosted_stage_attempt_evidence",
                        "attempt_ref": "opl-attempt://mag/cli-1",
                        "stage_id": "review_and_rebuttal",
                        "ledger_ref": "opl-ledger://mag/hosted-attempt/cli-1",
                        "domain_breakdown": {
                            "target_domain_id": "med-autogrant",
                            "owner_receipt_ref": receipt["receipt_instance_ref"],
                            "no_regression_evidence_refs": [receipt["receipt_instance_ref"]],
                            "typed_blocker_refs": [],
                        },
                    }
                ),
                encoding="utf-8",
            )
            sidecar_closeout_path.write_text(
                json.dumps({"receipt_ref": receipt["receipt_instance_ref"]}),
                encoding="utf-8",
            )

            exit_code, stdout, stderr = self.run_cli(
                main,
                "product",
                "hosted-receipt-verification",
                "--owner-receipt-evidence",
                str(owner_receipt_path),
                "--opl-attempt-evidence",
                str(opl_attempt_path),
                "--sidecar-closeout-result",
                str(sidecar_closeout_path),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        verification = payload["focused_hosted_receipt_verification"]
        self.assertEqual(verification["surface_kind"], "mag_focused_hosted_receipt_verification")
        self.assertTrue(verification["matches"]["owner_receipt_ref_matches_opl"])
        self.assertTrue(verification["matches"]["receipt_ref_matches_sidecar"])
        self.assertFalse(verification["claims"]["claims_production_long_run_soak_complete"])

    @staticmethod
    def run_cli(main_func, *argv: str) -> tuple[int, str, str]:
        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            exit_code = main_func(list(argv))
        return exit_code, stdout_buffer.getvalue(), stderr_buffer.getvalue()
