from __future__ import annotations

import tempfile

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryProductionLiveAcceptanceCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_production_live_acceptance_receipt_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "production-live-acceptance-receipt",
            "production_live_acceptance_receipt": {
                "surface_kind": "mag_production_live_acceptance_receipt_projection",
            },
        }
        owner_receipt = {"surface_kind": "mag_owner_receipt_evidence"}
        suite_result = {"surface_kind": "opl_agent_lab_suite_result"}
        meta_result = {"surface_kind": "opl_meta_agent_external_suite_self_evolution_result"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            owner_receipt_path = Path(tmp_dir) / "owner-receipt.json"
            suite_result_path = Path(tmp_dir) / "agent-lab-suite-result.json"
            meta_result_path = Path(tmp_dir) / "meta-agent-result.json"
            owner_receipt_path.write_text(json.dumps(owner_receipt), encoding="utf-8")
            suite_result_path.write_text(json.dumps(suite_result), encoding="utf-8")
            meta_result_path.write_text(json.dumps(meta_result), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_production_live_acceptance_receipt_projection.return_value = (
                    expected_payload
                )

                exit_code, stdout, stderr = self.run_cli(
                    "product",
                    "production-live-acceptance-receipt",
                    "--owner-receipt-evidence",
                    str(owner_receipt_path),
                    "--agent-lab-suite-result",
                    str(suite_result_path),
                    "--meta-agent-coordination-result",
                    str(meta_result_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_production_live_acceptance_receipt_projection.assert_called_once_with(
            owner_receipt_evidence=owner_receipt,
            agent_lab_suite_result=suite_result,
            meta_agent_coordination_result=meta_result,
        )

    def test_production_live_acceptance_receipt_dispatches_text_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "production-live-acceptance-receipt",
            "production_live_acceptance_receipt": {
                "surface_kind": "mag_production_live_acceptance_receipt_projection",
                "state": "closed_by_mag_domain_owner_live_acceptance_receipt",
                "target_domain_id": "med-autogrant",
                "receipt": {
                    "receipt_ref": "receipt:mag/production-live-acceptance/2026-05-20",
                    "receipt_shape": "domain_owner_receipt",
                },
                "agent_lab_coordination": {"status": "passed"},
                "meta_agent_coordination": {"developer_work_order_status": "no_patch_required"},
                "production_acceptance": {"accepted_return_shape": "domain_owner_receipt_ref"},
            },
        }
        owner_receipt = {"surface_kind": "mag_owner_receipt_evidence"}
        suite_result = {"surface_kind": "opl_agent_lab_suite_result"}
        meta_result = {"surface_kind": "opl_meta_agent_external_suite_self_evolution_result"}

        with tempfile.TemporaryDirectory() as tmp_dir:
            owner_receipt_path = Path(tmp_dir) / "owner-receipt.json"
            suite_result_path = Path(tmp_dir) / "agent-lab-suite-result.json"
            meta_result_path = Path(tmp_dir) / "meta-agent-result.json"
            owner_receipt_path.write_text(json.dumps(owner_receipt), encoding="utf-8")
            suite_result_path.write_text(json.dumps(suite_result), encoding="utf-8")
            meta_result_path.write_text(json.dumps(meta_result), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_production_live_acceptance_receipt_projection.return_value = (
                    expected_payload
                )

                exit_code, stdout, stderr = self.run_cli(
                    "product",
                    "production-live-acceptance-receipt",
                    "--owner-receipt-evidence",
                    str(owner_receipt_path),
                    "--agent-lab-suite-result",
                    str(suite_result_path),
                    "--meta-agent-coordination-result",
                    str(meta_result_path),
                    "--format",
                    "text",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertIn("state: closed_by_mag_domain_owner_live_acceptance_receipt", stdout)
        self.assertIn("receipt_ref: receipt:mag/production-live-acceptance/2026-05-20", stdout)
        self.assertIn("meta_agent_work_order_status: no_patch_required", stdout)
