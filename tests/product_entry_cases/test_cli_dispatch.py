from __future__ import annotations

import tempfile

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryCliDispatchTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_build_product_entry_dispatches_shell(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "build-product-entry",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "output_path": None,
            "product_entry": {
                "entry_kind": "med_auto_grant_product_entry",
                "entry_mode": "direct",
                "task_intent": "tighten-grant-mainline",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "product",
                "build-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--entry-mode",
                "direct",
                "--task-intent",
                "tighten-grant-mainline",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            entry_mode="direct",
            task_intent="tighten-grant-mainline",
            output_path=None,
            funding_call=None,
        )

    def test_grant_progress_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-progress",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "progress_projection": {
                "projection_kind": "grant_progress",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.read_grant_progress.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "workspace",
                "progress",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.read_grant_progress.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

    def test_grant_cockpit_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-cockpit",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "grant_cockpit": {
                "cockpit_kind": "grant_cockpit",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.read_grant_cockpit.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "workspace",
                "cockpit",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.read_grant_cockpit.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

    def test_grant_direct_entry_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "grant-direct-entry",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "grant_direct_entry": {
                "entry_kind": "grant_direct_entry",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_grant_direct_entry.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "product",
                "direct-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--task-intent",
                "tighten-grant-mainline",
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_grant_direct_entry.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
            funding_call=None,
        )

    def test_product_entry_manifest_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "product-entry-manifest",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "product_entry_manifest": {
                "manifest_kind": "med_auto_grant_product_entry_manifest",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_product_entry_manifest.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "product",
                "manifest",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_product_entry_manifest.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            funding_call=None,
        )

    def test_skill_catalog_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "skill-catalog",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "skill_catalog": {
                "surface_kind": "skill_catalog",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_skill_catalog.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "product",
                "skill-catalog",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_skill_catalog.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            funding_call=None,
        )

    def test_product_preflight_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "product-preflight",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
            "input_path": str(CRITIQUE_EXAMPLE_PATH),
            "product_entry_preflight": {
                "surface_kind": "product_entry_preflight",
                "ready_to_try_now": True,
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_product_entry_preflight.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "product",
                "preflight",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_product_entry_preflight.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

    def test_flat_product_status_alias_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            SystemExit,
            "Legacy flat command `product-status` has been removed. Use `product status` instead.",
        ):
            main(
                [
                    "product-status",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH),
                    "--format",
                    "json",
                ]
            )

    def test_domain_memory_writeback_proposal_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "domain-memory-writeback-proposal",
            "domain_memory_writeback_proposal": {
                "surface_kind": "mag_domain_memory_writeback_proposal",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_domain_memory_writeback_proposal.return_value = expected_payload

            stdout_buffer = StringIO()
            stderr_buffer = StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exit_code = main(
                    [
                        "product",
                        "domain-memory-proposal",
                        "--input",
                        str(CRITIQUE_EXAMPLE_PATH),
                        "--stage-id",
                        "review_and_rebuttal",
                        "--source-ref",
                        "runtime-closeout://grant-run/example",
                        "--lesson-summary",
                        "Keep reusable reviewer risk framing as strategy memory.",
                        "--proposal-id",
                        "review-risk-framing",
                        "--format",
                        "json",
                    ]
                )
            stdout = stdout_buffer.getvalue()
            stderr = stderr_buffer.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_domain_memory_writeback_proposal.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            stage_id="review_and_rebuttal",
            source_ref="runtime-closeout://grant-run/example",
            lesson_summary="Keep reusable reviewer risk framing as strategy memory.",
            proposal_id="review-risk-framing",
        )

    def test_domain_memory_writeback_decision_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "domain-memory-writeback-decision",
            "domain_memory_writeback_decision": {
                "surface_kind": "mag_domain_memory_writeback_decision",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.build_domain_memory_writeback_decision.return_value = expected_payload

            stdout_buffer = StringIO()
            stderr_buffer = StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exit_code = main(
                    [
                        "product",
                        "domain-memory-decision",
                        "--proposal",
                        "/tmp/proposal.json",
                        "--decision",
                        "accepted",
                        "--decision-reason",
                        "Reusable strategy memory.",
                        "--memory-id",
                        "review-risk-framing",
                        "--format",
                        "json",
                    ]
                )
            stdout = stdout_buffer.getvalue()
            stderr = stderr_buffer.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_domain_memory_writeback_decision.assert_called_once_with(
            proposal_path="/tmp/proposal.json",
            decision="accepted",
            decision_reason="Reusable strategy memory.",
            memory_id="review-risk-framing",
        )

    def test_domain_memory_receipt_evidence_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "domain-memory-receipt-evidence",
            "domain_memory_receipt_evidence": {
                "surface_kind": "mag_domain_memory_runtime_receipt_evidence",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.write_domain_memory_receipt_evidence.return_value = expected_payload

            stdout_buffer = StringIO()
            stderr_buffer = StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exit_code = main(
                    [
                        "product",
                        "domain-memory-receipt-evidence",
                        "--decision",
                        "/tmp/decision.json",
                        "--runtime-root",
                        "/tmp/runtime-state",
                        "--format",
                        "json",
                    ]
                )
            stdout = stdout_buffer.getvalue()
            stderr = stderr_buffer.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.write_domain_memory_receipt_evidence.assert_called_once_with(
            decision_payload="/tmp/decision.json",
            runtime_root="/tmp/runtime-state",
        )

    def test_owner_receipt_evidence_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "owner-receipt-evidence",
            "owner_receipt_evidence": {
                "surface_kind": "mag_owner_receipt_evidence",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.write_owner_receipt_evidence.return_value = expected_payload

            stdout_buffer = StringIO()
            stderr_buffer = StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exit_code = main(
                    [
                        "product",
                        "owner-receipt-evidence",
                        "--input",
                        str(CRITIQUE_EXAMPLE_PATH),
                        "--receipt-shape",
                        "no_regression_evidence",
                        "--stage-id",
                        "review_and_rebuttal",
                        "--source-ref",
                        "opl-stage-attempt://attempt-1",
                        "--closeout-summary",
                        "No regression evidence.",
                        "--runtime-root",
                        "/tmp/runtime-state",
                        "--receipt-id",
                        "attempt-1",
                        "--format",
                        "json",
                    ]
                )
            stdout = stdout_buffer.getvalue()
            stderr = stderr_buffer.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.write_owner_receipt_evidence.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            receipt_shape="no_regression_evidence",
            stage_id="review_and_rebuttal",
            source_ref="opl-stage-attempt://attempt-1",
            closeout_summary="No regression evidence.",
            runtime_root="/tmp/runtime-state",
            receipt_id="attempt-1",
        )

    def test_lifecycle_receipt_evidence_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "lifecycle-receipt-evidence",
            "lifecycle_receipt_evidence": {
                "surface_kind": "mag_lifecycle_receipt_evidence",
            },
        }

        with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
            product_entry = product_entry_class.return_value
            product_entry.write_lifecycle_receipt_evidence.return_value = expected_payload

            stdout_buffer = StringIO()
            stderr_buffer = StringIO()
            with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                exit_code = main(
                    [
                        "product",
                        "lifecycle-receipt-evidence",
                        "--input",
                        str(CRITIQUE_EXAMPLE_PATH),
                        "--operation",
                        "cleanup",
                        "--receipt-shape",
                        "typed_blocker",
                        "--source-ref",
                        "opl-lifecycle://cleanup/1",
                        "--closeout-summary",
                        "Cleanup requires MAG owner receipt.",
                        "--runtime-root",
                        "/tmp/runtime-state",
                        "--receipt-id",
                        "cleanup-1",
                        "--format",
                        "json",
                    ]
                )
            stdout = stdout_buffer.getvalue()
            stderr = stderr_buffer.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.write_lifecycle_receipt_evidence.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            operation="cleanup",
            receipt_shape="typed_blocker",
            source_ref="opl-lifecycle://cleanup/1",
            closeout_summary="Cleanup requires MAG owner receipt.",
            runtime_root="/tmp/runtime-state",
            receipt_id="cleanup-1",
        )

    def test_receipt_reconciliation_proof_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "controlled-soak-receipt-reconciliation-proof",
            "receipt_reconciliation_proof": {
                "surface_kind": "mag_controlled_soak_receipt_reconciliation_proof",
            },
        }
        owner_receipt = {
            "surface_kind": "mag_owner_receipt_evidence",
            "receipt_instance_ref": "/tmp/runtime-state/receipts/receipt-1.json",
        }
        sidecar_closeout_result = {
            "receipt_ref": "/tmp/runtime-state/receipts/receipt-1.json",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            owner_receipt_path = Path(tmp_dir) / "owner-receipt.json"
            sidecar_closeout_path = Path(tmp_dir) / "sidecar-closeout.json"
            owner_receipt_path.write_text(json.dumps(owner_receipt), encoding="utf-8")
            sidecar_closeout_path.write_text(json.dumps(sidecar_closeout_result), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_controlled_soak_receipt_reconciliation_proof.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "product",
                    "receipt-reconciliation-proof",
                    "--owner-receipt-evidence",
                    str(owner_receipt_path),
                    "--opl-ledger-ref",
                    "opl-ledger://mag/stage-attempt/closeout/1",
                    "--sidecar-closeout-result",
                    str(sidecar_closeout_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_controlled_soak_receipt_reconciliation_proof.assert_called_once_with(
            owner_receipt_evidence=owner_receipt,
            opl_ledger_ref="opl-ledger://mag/stage-attempt/closeout/1",
            sidecar_closeout_result=sidecar_closeout_result,
        )

    def test_receipt_reconciliation_inventory_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "controlled-soak-receipt-reconciliation-inventory",
            "receipt_reconciliation_inventory": {
                "surface_kind": "mag_controlled_soak_receipt_reconciliation_inventory",
            },
        }
        owner_receipt = {
            "surface_kind": "mag_owner_receipt_evidence",
            "receipt_instance_ref": "/tmp/runtime-state/receipts/receipt-1.json",
        }
        sidecar_closeout_result = {
            "receipt_ref": "/tmp/runtime-state/receipts/receipt-1.json",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            owner_receipt_path = Path(tmp_dir) / "owner-receipt.json"
            sidecar_closeout_path = Path(tmp_dir) / "sidecar-closeout.json"
            owner_receipt_path.write_text(json.dumps(owner_receipt), encoding="utf-8")
            sidecar_closeout_path.write_text(json.dumps(sidecar_closeout_result), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_controlled_soak_receipt_reconciliation_inventory.return_value = (
                    expected_payload
                )

                exit_code, stdout, stderr = self.run_cli(
                    "product",
                    "receipt-reconciliation-inventory",
                    "--owner-receipt-evidence",
                    str(owner_receipt_path),
                    "--opl-ledger-ref",
                    "opl-ledger://mag/stage-attempt/closeout/1",
                    "--sidecar-closeout-result",
                    str(sidecar_closeout_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_controlled_soak_receipt_reconciliation_inventory.assert_called_once_with(
            owner_receipt_evidence_items=[owner_receipt],
            opl_ledger_ref="opl-ledger://mag/stage-attempt/closeout/1",
            sidecar_closeout_results=[sidecar_closeout_result],
        )

    def test_focused_hosted_receipt_verification_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "focused-hosted-receipt-verification",
            "focused_hosted_receipt_verification": {
                "surface_kind": "mag_focused_hosted_receipt_verification",
            },
        }
        owner_receipt = {
            "surface_kind": "mag_owner_receipt_evidence",
            "receipt_instance_ref": "/tmp/runtime-state/receipts/receipt-1.json",
        }
        opl_attempt_evidence = {
            "surface_kind": "opl_hosted_stage_attempt_evidence",
            "attempt_ref": "opl-attempt://mag/review-1",
        }
        sidecar_closeout_result = {
            "receipt_ref": "/tmp/runtime-state/receipts/receipt-1.json",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            owner_receipt_path = Path(tmp_dir) / "owner-receipt.json"
            opl_attempt_path = Path(tmp_dir) / "opl-attempt.json"
            sidecar_closeout_path = Path(tmp_dir) / "sidecar-closeout.json"
            owner_receipt_path.write_text(json.dumps(owner_receipt), encoding="utf-8")
            opl_attempt_path.write_text(json.dumps(opl_attempt_evidence), encoding="utf-8")
            sidecar_closeout_path.write_text(json.dumps(sidecar_closeout_result), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_focused_hosted_receipt_verification.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
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
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_focused_hosted_receipt_verification.assert_called_once_with(
            owner_receipt_evidence=owner_receipt,
            opl_attempt_evidence=opl_attempt_evidence,
            sidecar_closeout_result=sidecar_closeout_result,
        )
