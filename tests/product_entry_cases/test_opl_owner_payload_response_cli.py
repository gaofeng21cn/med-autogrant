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

    def run_manifest_consumption_payload_cli(
        self,
        *,
        owner_payload_response: dict[str, object],
        workspace_receipt_scaleout_evidence: dict[str, object],
        operator_payload: dict[str, object],
    ) -> tuple[int, str, str]:
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

            return self.run_cli(
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

    def test_manifest_consumption_payload_cli_returns_provider_followthrough_shape(self) -> None:
        owner_payload_response = {
            "surface_kind": "mag_opl_owner_payload_response",
            "status": "blocked_by_submission_ready_human_gate",
            "domain_owner_receipt_refs": [
                "receipt:mag/production-live-acceptance/2026-05-20",
            ],
            "typed_blocker_refs": [
                "typed-blocker:mag/package_and_submit_ready/"
                "submission_ready_export_gate/human-approval-required/2026-05-22"
            ],
            "owner_chain_refs": [
                "receipt:mag/production-live-acceptance/2026-05-20",
            ],
            "no_regression_evidence_refs": [
                "no-regression:mag/direct-hosted-parity/2026-05-20",
            ],
        }
        workspace_receipt_scaleout_evidence = {
            "surface_kind": "mag_workspace_receipt_scaleout_evidence.v1",
            "workspace_receipt_scaleout": {"workspace_count": 4},
        }
        provider_long_soak_typed_blocker_ref = (
            "typed-blocker:mag/manifest-sustained-consumption/"
            "provider-long-soak-window-still-open/2026-05-31"
        )
        operator_payload = {
            "app_operator_consumption_ref": [
                "opl://app/operator/mag/owner-payload-consumed/2026-05-31"
            ],
            "default_caller_consumption_ref": [
                "opl://release/default-caller/mag/owner-payload-consumed/2026-05-31"
            ],
            "owner_payload_response_ref": ["/product_entry_manifest/owner_payload_response"],
            "workspace_receipt_scaleout_evidence_ref": [
                "/product_entry_manifest/workspace_receipt_scaleout_evidence"
            ],
            "no_forbidden_write_ref": [
                "no-forbidden-write:mag/manifest-consumption/2026-05-31",
            ],
            "long_soak_or_typed_blocker_ref": [provider_long_soak_typed_blocker_ref],
        }

        exit_code, stdout, stderr = self.run_manifest_consumption_payload_cli(
            owner_payload_response=owner_payload_response,
            workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
            operator_payload=operator_payload,
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        response = json.loads(stdout)
        self.assertEqual(
            response["surface_kind"],
            "mag_manifest_sustained_consumption_payload_response",
        )
        self.assertEqual(response["status"], "sustained_consumption_payload_refs_ready")
        self.assertEqual(response["recommended_payload_path"], "sustained_consumption_refs_path")
        self.assertEqual(
            response["record_payload"]["long_soak_or_typed_blocker_refs"],
            [provider_long_soak_typed_blocker_ref],
        )
        self.assertEqual(
            response["provider_long_soak_followthrough"]["status"],
            "blocked_by_provider_long_soak_typed_blocker",
        )
        self.assertEqual(
            response["provider_long_soak_followthrough"]["typed_blocker_refs"],
            [provider_long_soak_typed_blocker_ref],
        )
        self.assertEqual(response["provider_long_soak_followthrough"]["long_soak_evidence_refs"], [])
        self.assertFalse(
            response["provider_long_soak_followthrough"]["claims_provider_long_soak_complete"]
        )
        self.assertFalse(response["provider_long_soak_followthrough"]["closes_provider_long_soak"])
        self.assertFalse(response["authority_boundary"]["can_satisfy_provider_long_soak"])
        self.assertFalse(response["claims_sustained_app_consumption_complete"])
        self.assertFalse(response["claims_provider_long_soak_complete"])
        self.assertEqual(response["operator_payload_attempt_summary"]["attempt_count"], 1)
        self.assertFalse(
            response["operator_payload_attempt_summary"][
                "attempt_records_are_app_sustained_consumption_closeout"
            ]
        )

        encoded_payload = json.dumps(
            {
                "record_payload": response["record_payload"],
                "opl_runtime_action_execute_payload": response["opl_runtime_action_execute_payload"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        self.assertNotIn("grant_artifact_body", encoded_payload)
        self.assertNotIn("memory_body", encoded_payload)
        self.assertNotIn("proposal_text", encoded_payload)

    def test_manifest_consumption_payload_cli_accepts_attempt_batch_without_closeout_claim(
        self,
    ) -> None:
        owner_payload_response = {
            "surface_kind": "mag_opl_owner_payload_response",
            "status": "blocked_by_submission_ready_human_gate",
            "domain_owner_receipt_refs": [
                "receipt:mag/production-live-acceptance/2026-05-20",
            ],
            "typed_blocker_refs": [
                "typed-blocker:mag/package_and_submit_ready/"
                "submission_ready_export_gate/human-approval-required/2026-05-22"
            ],
            "owner_chain_refs": [
                "receipt:mag/production-live-acceptance/2026-05-20",
            ],
            "no_regression_evidence_refs": [
                "no-regression:mag/direct-hosted-parity/2026-05-20",
            ],
        }
        workspace_receipt_scaleout_evidence = {
            "surface_kind": "mag_workspace_receipt_scaleout_evidence.v1",
            "workspace_receipt_scaleout": {"workspace_count": 4},
        }
        provider_long_soak_typed_blocker_ref = (
            "typed-blocker:mag/manifest-sustained-consumption/"
            "provider-long-soak-window-still-open/2026-06-01"
        )
        operator_payload = {
            "operator_payload_attempts": [
                {
                    "attempt_id": "manifest-sustained-consumption-cli-a",
                    "observed_at": "2026-06-01T00:00:00Z",
                    "app_operator_consumption_ref": [
                        "opl://app/operator/mag/owner-payload-consumed/2026-06-01-a"
                    ],
                    "default_caller_consumption_ref": [
                        "opl://release/default-caller/mag/owner-payload-consumed/2026-06-01-a"
                    ],
                    "owner_payload_response_ref": [
                        "/product_entry_manifest/owner_payload_response"
                    ],
                    "workspace_receipt_scaleout_evidence_ref": [
                        "/product_entry_manifest/workspace_receipt_scaleout_evidence"
                    ],
                    "no_forbidden_write_ref": [
                        "no-forbidden-write:mag/manifest-consumption/2026-06-01-a",
                    ],
                    "long_soak_or_typed_blocker_ref": [provider_long_soak_typed_blocker_ref],
                },
                {
                    "attempt_id": "manifest-sustained-consumption-cli-b",
                    "observed_at": "2026-06-01T00:10:00Z",
                    "typed_blocker_refs": [
                        "typed-blocker:app/operator/mag/sustained-consumption-missing/2026-06-01"
                    ],
                },
            ]
        }

        exit_code, stdout, stderr = self.run_manifest_consumption_payload_cli(
            owner_payload_response=owner_payload_response,
            workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
            operator_payload=operator_payload,
        )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        response = json.loads(stdout)
        self.assertEqual(response["recommended_payload_path"], "operator_payload_attempts_path")
        self.assertEqual(len(response["operator_payload_attempt_records"]), 2)
        self.assertEqual(response["operator_payload_attempt_summary"]["attempt_count"], 2)
        self.assertTrue(
            response["operator_payload_attempt_summary"]["repeated_attempt_evidence_observed"]
        )
        self.assertFalse(
            response["operator_payload_attempt_summary"][
                "attempt_records_are_app_sustained_consumption_closeout"
            ]
        )
        self.assertFalse(
            response["operator_payload_attempt_summary"][
                "attempt_records_are_provider_long_soak_closeout"
            ]
        )
        self.assertFalse(response["claims_sustained_app_consumption_complete"])
        self.assertFalse(response["claims_provider_long_soak_complete"])

    def test_manifest_consumption_payload_cli_rejects_unknown_operator_field(self) -> None:
        owner_payload_response = {
            "surface_kind": "mag_opl_owner_payload_response",
            "status": "blocked_by_submission_ready_human_gate",
        }
        workspace_receipt_scaleout_evidence = {
            "surface_kind": "mag_workspace_receipt_scaleout_evidence.v1",
            "workspace_receipt_scaleout": {"workspace_count": 4},
        }
        operator_payload = {
            "typed_blocker_refs": [
                "typed-blocker:app/operator/mag/sustained-consumption-missing/2026-05-31"
            ],
            "operator_note": "do not smuggle uncontracted payload fields",
        }

        exit_code, stdout, stderr = self.run_manifest_consumption_payload_cli(
            owner_payload_response=owner_payload_response,
            workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
            operator_payload=operator_payload,
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        response = json.loads(stdout)
        self.assertFalse(response["ok"])
        self.assertEqual(response["command"], "manifest-sustained-consumption-payload")
        self.assertIn("未声明字段", response["error"])
        self.assertIn("operator_note", response["error"])

    def test_manifest_consumption_payload_cli_rejects_mixed_success_and_blocker_paths(
        self,
    ) -> None:
        owner_payload_response = {
            "surface_kind": "mag_opl_owner_payload_response",
            "status": "blocked_by_submission_ready_human_gate",
        }
        workspace_receipt_scaleout_evidence = {
            "surface_kind": "mag_workspace_receipt_scaleout_evidence.v1",
            "workspace_receipt_scaleout": {"workspace_count": 4},
        }
        operator_payload = {
            "app_operator_consumption_ref": [
                "opl://app/operator/mag/owner-payload-consumed/2026-05-31"
            ],
            "default_caller_consumption_ref": [
                "opl://release/default-caller/mag/owner-payload-consumed/2026-05-31"
            ],
            "owner_payload_response_ref": ["/product_entry_manifest/owner_payload_response"],
            "workspace_receipt_scaleout_evidence_ref": [
                "/product_entry_manifest/workspace_receipt_scaleout_evidence"
            ],
            "no_forbidden_write_ref": [
                "no-forbidden-write:mag/manifest-consumption/2026-05-31",
            ],
            "long_soak_or_typed_blocker_ref": [
                "typed-blocker:mag/manifest-sustained-consumption/"
                "provider-long-soak-window-still-open/2026-05-31"
            ],
            "typed_blocker_refs": [
                "typed-blocker:app/operator/mag/sustained-consumption-missing/2026-05-31"
            ],
        }

        exit_code, stdout, stderr = self.run_manifest_consumption_payload_cli(
            owner_payload_response=owner_payload_response,
            workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
            operator_payload=operator_payload,
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        response = json.loads(stdout)
        self.assertFalse(response["ok"])
        self.assertEqual(response["command"], "manifest-sustained-consumption-payload")
        self.assertIn("只能选择 success refs path 或 typed blocker path", response["error"])
