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

    def test_codex_stage_receipts_dispatches_product_surface(self) -> None:
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
                    "product",
                    "codex-stage-receipts",
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

    def test_operator_closeout_readiness_dispatches_product_surface(self) -> None:
        expected_payload = {
            "surface_kind": "mag_operator_closeout_readiness_projection",
            "state": "operator_closeout_refs_ready_not_quality_ready",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            production_acceptance_path = Path(tmp_dir) / "acceptance.json"
            ledger_path = Path(tmp_dir) / "ledger.json"
            receipt_readiness_path = Path(tmp_dir) / "readiness.json"
            production_acceptance = {
                "surface_kind": "mag_production_acceptance_evidence.v1",
                "evidence_tail_status": "closed_by_domain_owned_acceptance_receipt",
            }
            ledger = {
                "surface_kind": "mag_external_evidence_receipt_ledger.v1",
                "remaining_real_evidence_gap_ids": [],
                "summary": {"claims_grant_or_fundability_ready": False},
            }
            receipt_readiness = {
                "surface_kind": "mag_receipt_readiness_projection",
                "state": "receipt_refs_ready_not_quality_ready",
                "missing_categories": [],
            }
            production_acceptance_path.write_text(json.dumps(production_acceptance), encoding="utf-8")
            ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
            receipt_readiness_path.write_text(json.dumps(receipt_readiness), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_operator_closeout_readiness_projection.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "product",
                    "operator-closeout-readiness",
                    "--production-acceptance",
                    str(production_acceptance_path),
                    "--external-evidence-receipt-ledger",
                    str(ledger_path),
                    "--receipt-readiness-projection",
                    str(receipt_readiness_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_operator_closeout_readiness_projection.assert_called_once_with(
            production_acceptance=production_acceptance,
            external_evidence_receipt_ledger=ledger,
            receipt_readiness_projection=receipt_readiness,
        )

    def test_physical_morphology_guard_dispatches_product_surface(self) -> None:
        expected_payload = {
            "surface_kind": "mag_physical_morphology_guard_projection",
            "state": "allowed_evidence_gated",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_item_path = Path(tmp_dir) / "source-item.json"
            source_item = {
                "path": "src/med_autogrant/product_entry_parts/entry.py",
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
                    "product",
                    "physical-morphology-guard",
                    "--source-item",
                    str(source_item_path),
                    "--external-evidence-ref",
                    "opl://receipts/mag/physical-morphology/parity.json",
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_physical_morphology_guard_projection.assert_called_once_with(
            source_items=[source_item],
            external_evidence_refs=["opl://receipts/mag/physical-morphology/parity.json"],
        )

    def test_executor_first_closeout_bundle_dispatches_product_surface(self) -> None:
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
                    "product",
                    "executor-first-closeout-bundle",
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

    def test_lifecycle_receipt_bundle_dispatches_product_surface(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "lifecycle-receipt-bundle",
            "lifecycle_receipt_bundle": {
                "surface_kind": "mag_lifecycle_receipt_bundle",
            },
        }
        cleanup_receipt = {
            "surface_kind": "mag_lifecycle_receipt_evidence",
            "operation": "cleanup",
            "receipt_instance_ref": "/tmp/runtime-state/receipts/lifecycle/cleanup.json",
        }
        restore_receipt = {
            "surface_kind": "mag_lifecycle_receipt_evidence",
            "operation": "restore",
            "receipt_instance_ref": "/tmp/runtime-state/receipts/lifecycle/restore.json",
        }
        retention_receipt = {
            "surface_kind": "mag_lifecycle_receipt_evidence",
            "operation": "retention",
            "receipt_instance_ref": "/tmp/runtime-state/receipts/lifecycle/retention.json",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            cleanup_path = Path(tmp_dir) / "cleanup.json"
            restore_path = Path(tmp_dir) / "restore.json"
            retention_path = Path(tmp_dir) / "retention.json"
            cleanup_path.write_text(json.dumps(cleanup_receipt), encoding="utf-8")
            restore_path.write_text(json.dumps(restore_receipt), encoding="utf-8")
            retention_path.write_text(json.dumps(retention_receipt), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_lifecycle_receipt_bundle.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "product",
                    "lifecycle-receipt-bundle",
                    "--lifecycle-receipt-evidence",
                    str(cleanup_path),
                    "--lifecycle-receipt-evidence",
                    str(restore_path),
                    "--lifecycle-receipt-evidence",
                    str(retention_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_lifecycle_receipt_bundle.assert_called_once_with(
            lifecycle_receipt_evidence_items=[
                cleanup_receipt,
                restore_receipt,
                retention_receipt,
            ],
        )

    def test_memory_receipt_projection_dispatches_product_surface(self) -> None:
        expected_payload = {
            "surface_kind": "mag_memory_receipt_read_projection",
            "accepted_count": 1,
            "rejected_count": 0,
        }
        receipt = {
            "surface_kind": "mag_domain_memory_runtime_receipt_evidence",
            "receipt_ref": "runtime://receipts/domain-memory/review-risk.json",
            "proposal_id": "review-risk",
            "decision": "accepted",
            "decision_owner": "med-autogrant",
            "accepted_memory_ref": "runtime://domain-memory/accepted/review-risk.json",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt_path = Path(tmp_dir) / "memory-receipt.json"
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_memory_receipt_read_projection.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "product",
                    "memory-receipt-projection",
                    "--receipt",
                    str(receipt_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_memory_receipt_read_projection.assert_called_once_with(
            receipt_items=[receipt],
        )

    def test_package_lifecycle_handoff_dispatches_product_surface(self) -> None:
        expected_payload = {
            "surface_kind": "mag_package_lifecycle_handoff_projection",
            "state": "refs_ready_for_opl_artifact_package_lifecycle_shell",
        }
        package_refs = {"final_package_ref": "mag-package://final/p3c"}
        gap_report = {
            "gap_report_ref": "mag-gap://package-export/p3c",
            "summary": "manual portal remains external",
        }
        export_verdict = {"export_verdict_ref": "mag-verdict://submission-ready-export/p3c"}
        manual_portal_boundary = {
            "manual_portal_boundary_ref": "mag-boundary://manual-portal/p3c",
        }
        lifecycle_receipt_refs = {
            "lifecycle_receipt_ref": "runtime://mag/receipts/lifecycle/p3c.json",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            package_refs_path = Path(tmp_dir) / "package-refs.json"
            gap_report_path = Path(tmp_dir) / "gap-report.json"
            export_verdict_path = Path(tmp_dir) / "export-verdict.json"
            manual_portal_boundary_path = Path(tmp_dir) / "manual-portal-boundary.json"
            lifecycle_receipt_refs_path = Path(tmp_dir) / "lifecycle-receipt-refs.json"
            package_refs_path.write_text(json.dumps(package_refs), encoding="utf-8")
            gap_report_path.write_text(json.dumps(gap_report), encoding="utf-8")
            export_verdict_path.write_text(json.dumps(export_verdict), encoding="utf-8")
            manual_portal_boundary_path.write_text(
                json.dumps(manual_portal_boundary),
                encoding="utf-8",
            )
            lifecycle_receipt_refs_path.write_text(
                json.dumps(lifecycle_receipt_refs),
                encoding="utf-8",
            )

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_package_lifecycle_handoff_projection.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "product",
                    "package-lifecycle-handoff",
                    "--package-refs",
                    str(package_refs_path),
                    "--gap-report",
                    str(gap_report_path),
                    "--export-verdict",
                    str(export_verdict_path),
                    "--manual-portal-boundary",
                    str(manual_portal_boundary_path),
                    "--lifecycle-receipt-refs",
                    str(lifecycle_receipt_refs_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_package_lifecycle_handoff_projection.assert_called_once_with(
            package_refs=package_refs,
            gap_report=gap_report,
            export_verdict=export_verdict,
            manual_portal_boundary=manual_portal_boundary,
            lifecycle_receipt_refs=lifecycle_receipt_refs,
        )

    def test_continuous_receipt_reconciliation_dispatches_product_surface(self) -> None:
        expected_payload = {
            "surface_kind": "mag_continuous_receipt_reconciliation_snapshot",
            "state": "read_only_snapshot_not_live_soak_complete",
        }
        verification = {
            "surface_kind": "mag_focused_hosted_receipt_verification",
            "mag_owner_receipt": {
                "receipt_ref": "/tmp/runtime-state/receipts/receipt-1.json",
            },
        }
        inventory = {
            "surface_kind": "mag_controlled_soak_receipt_reconciliation_inventory",
            "items": [],
        }
        observability_summary = {
            "surface_kind": "mag_receipt_observability_summary",
            "state": "summary",
        }
        stage_attempt_projection = {
            "surface_kind": "mag_stage_attempt_observability_projection",
            "state": "projection",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            verification_path = Path(tmp_dir) / "verification.json"
            inventory_path = Path(tmp_dir) / "inventory.json"
            observability_path = Path(tmp_dir) / "observability.json"
            stage_attempt_path = Path(tmp_dir) / "stage-attempt.json"
            verification_path.write_text(json.dumps(verification), encoding="utf-8")
            inventory_path.write_text(json.dumps(inventory), encoding="utf-8")
            observability_path.write_text(json.dumps(observability_summary), encoding="utf-8")
            stage_attempt_path.write_text(json.dumps(stage_attempt_projection), encoding="utf-8")

            with patch("med_autogrant.product_entry.MedAutoGrantProductEntry") as product_entry_class:
                product_entry = product_entry_class.return_value
                product_entry.build_continuous_receipt_reconciliation_snapshot.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "product",
                    "continuous-receipt-reconciliation",
                    "--hosted-receipt-verification",
                    str(verification_path),
                    "--receipt-reconciliation-inventory",
                    str(inventory_path),
                    "--receipt-observability-summary",
                    str(observability_path),
                    "--stage-attempt-observability-projection",
                    str(stage_attempt_path),
                    "--format",
                    "json",
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        product_entry.build_continuous_receipt_reconciliation_snapshot.assert_called_once_with(
            focused_hosted_receipt_verification_items=[verification],
            receipt_reconciliation_inventory=inventory,
            receipt_observability_summary=observability_summary,
            stage_attempt_observability_projection=stage_attempt_projection,
        )
