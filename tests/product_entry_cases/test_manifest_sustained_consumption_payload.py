from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


def _owner_payload_response() -> dict[str, object]:
    return {
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
            "runtime://mag/receipts/package/lifecycle.json",
        ],
        "no_regression_evidence_refs": [
            "no-regression:mag/direct-hosted-parity/2026-05-20",
        ],
    }


def _workspace_scaleout_evidence() -> dict[str, object]:
    return {
        "surface_kind": "mag_workspace_receipt_scaleout_evidence.v1",
        "workspace_receipt_scaleout": {
            "workspace_count": 4,
            "total_receipt_ref_count": 36,
        },
    }


class ProductEntryManifestSustainedConsumptionPayloadTest(unittest.TestCase):
    def test_sustained_consumption_payload_success_path_is_signed_refs_only_without_ready_claim(
        self,
    ) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        response = MedAutoGrantProductEntry().build_manifest_sustained_consumption_payload_response(
            owner_payload_response=_owner_payload_response(),
            workspace_receipt_scaleout_evidence=_workspace_scaleout_evidence(),
            operator_payload={
                "app_operator_consumption_ref": [
                    "opl://app/operator/mag/owner-payload-consumed/2026-05-28"
                ],
                "default_caller_consumption_ref": [
                    "opl://release/default-caller/mag/owner-payload-consumed/2026-05-28"
                ],
                "owner_payload_response_ref": [
                    "/product_entry_manifest/owner_payload_response",
                ],
                "workspace_receipt_scaleout_evidence_ref": [
                    "/product_entry_manifest/workspace_receipt_scaleout_evidence",
                ],
                "no_forbidden_write_ref": [
                    "no-forbidden-write:mag/manifest-consumption/2026-05-28",
                ],
                "long_soak_or_typed_blocker_ref": [
                    "typed-blocker:opl/provider/temporal-long-soak-window/open/2026-05-28",
                ],
            },
        )

        self.assertEqual(
            response["surface_kind"],
            "mag_manifest_sustained_consumption_payload_response",
        )
        self.assertEqual(response["status"], "sustained_consumption_payload_refs_ready")
        self.assertEqual(response["recommended_payload_path"], "sustained_consumption_refs_path")
        self.assertTrue(response["operator_payload_submitted"])
        self.assertNotIn("domain_id", response["record_payload"])
        self.assertNotIn("typed_blocker_refs", response["record_payload"])
        self.assertEqual(
            response["record_payload"]["app_operator_consumption_refs"],
            ["opl://app/operator/mag/owner-payload-consumed/2026-05-28"],
        )
        self.assertEqual(
            response["record_payload"]["long_soak_or_typed_blocker_refs"],
            ["typed-blocker:opl/provider/temporal-long-soak-window/open/2026-05-28"],
        )
        self.assertEqual(
            response["opl_runtime_action_execute_payload"],
            response["record_payload"],
        )
        self.assertEqual(
            response["allowed_operator_payload_fields"],
            [
                "app_operator_consumption_ref",
                "default_caller_consumption_ref",
                "owner_payload_response_ref",
                "workspace_receipt_scaleout_evidence_ref",
                "no_forbidden_write_ref",
                "long_soak_or_typed_blocker_ref",
                "typed_blocker_refs",
            ],
        )
        self.assertTrue(response["rejects_unknown_operator_payload_fields"])
        self.assertFalse(response["claims_sustained_app_consumption_complete"])
        self.assertFalse(response["claims_provider_long_soak_complete"])
        self.assertFalse(response["claims_grant_ready"])
        self.assertFalse(response["claims_submission_ready"])
        self.assertFalse(response["authority_boundary"]["can_create_owner_receipt"])
        self.assertFalse(
            response["authority_boundary"]["can_declare_app_sustained_consumption_complete"]
        )

        encoded_record = json.dumps(response["record_payload"], ensure_ascii=False, sort_keys=True)
        self.assertNotIn("PRIVATE_BODY_TOKEN", encoded_record)
        self.assertNotIn("grant_artifact_body", encoded_record)

    def test_typed_blocker_payload_path_does_not_claim_success(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        response = MedAutoGrantProductEntry().build_manifest_sustained_consumption_payload_response(
            owner_payload_response=_owner_payload_response(),
            workspace_receipt_scaleout_evidence=_workspace_scaleout_evidence(),
            operator_payload={
                "typed_blocker_refs": [
                    "typed-blocker:app/operator/mag/sustained-consumption-missing/2026-05-28"
                ]
            },
        )

        self.assertEqual(response["status"], "blocked_by_app_operator_typed_blocker")
        self.assertEqual(response["recommended_payload_path"], "typed_blocker_path")
        self.assertFalse(response["claims_sustained_app_consumption_complete"])
        self.assertFalse(response["accepted_payload_paths"]["typed_blocker_path"]["success_claimed"])

    def test_rejects_empty_payload_and_private_body(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        with self.assertRaises(WorkspaceStateError):
            entry.build_manifest_sustained_consumption_payload_response(
                owner_payload_response=_owner_payload_response(),
                workspace_receipt_scaleout_evidence=_workspace_scaleout_evidence(),
                operator_payload={},
            )

        with self.assertRaises(WorkspaceStateError):
            entry.build_manifest_sustained_consumption_payload_response(
                owner_payload_response=_owner_payload_response(),
                workspace_receipt_scaleout_evidence=_workspace_scaleout_evidence(),
                operator_payload={
                    "typed_blocker_refs": [
                        "typed-blocker:app/operator/mag/sustained-consumption-missing/2026-05-28"
                    ],
                    "grant_artifact_body": "PRIVATE_BODY_TOKEN",
                },
            )

    def test_rejects_unknown_operator_payload_fields(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with self.assertRaisesRegex(WorkspaceStateError, "未声明字段"):
            MedAutoGrantProductEntry().build_manifest_sustained_consumption_payload_response(
                owner_payload_response=_owner_payload_response(),
                workspace_receipt_scaleout_evidence=_workspace_scaleout_evidence(),
                operator_payload={
                    "typed_blocker_refs": [
                        "typed-blocker:app/operator/mag/sustained-consumption-missing/2026-05-28"
                    ],
                    "operator_note": "do not smuggle uncontracted payload fields",
                },
            )
