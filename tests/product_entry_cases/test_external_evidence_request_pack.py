from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryExternalEvidenceRequestPackTest(unittest.TestCase):
    def test_manifest_projects_external_evidence_request_pack_without_claiming_evidence(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        thinning = payload["product_entry_manifest"]["mag_consumer_thinning_contract"]
        evidence_pack = thinning["external_evidence_request_pack"]

        self.assertEqual(evidence_pack["surface_kind"], "mag_external_evidence_request_pack")
        self.assertEqual(evidence_pack["owner"], "med-autogrant")
        self.assertEqual(evidence_pack["state"], "request_pack_declared_external_evidence_not_claimed")
        self.assertEqual(
            evidence_pack["policy"],
            "request_refs_receipt_shapes_and_parity_only_no_runtime_implementation",
        )
        self.assertEqual(
            evidence_pack["sidecar_projection_ref"],
            "/sidecar_export/external_evidence_request_pack",
        )
        self.assertEqual(
            evidence_pack["required_request_ids"],
            [
                "opl_generated_hosted_caller_pack_consumption",
                "app_workbench_package_ref_consumption",
                "production_default_caller_release_dist_consumption",
                "owner_receipt_typed_blocker_ref_roundtrip",
                "continuous_no_forbidden_write_guard",
                "direct_hosted_parity_no_regression",
                "temporal_provider_long_soak_receipt_reconciliation",
            ],
        )
        request_by_id = {item["request_id"]: item for item in evidence_pack["requests"]}
        self.assertEqual(set(request_by_id), set(evidence_pack["required_request_ids"]))
        self.assertEqual(
            request_by_id["direct_hosted_parity_no_regression"]["state"],
            "requested_not_received",
        )
        self.assertIn(
            "direct_hosted_parity_receipt",
            request_by_id["direct_hosted_parity_no_regression"]["required_receipt_shapes"],
        )
        self.assertIn(
            "temporal_provider_long_soak_receipt",
            request_by_id["temporal_provider_long_soak_receipt_reconciliation"][
                "required_receipt_shapes"
            ],
        )
        self.assertIn(
            "no_forbidden_write_scan_receipt",
            request_by_id["continuous_no_forbidden_write_guard"]["required_receipt_shapes"],
        )
        for request in evidence_pack["requests"]:
            with self.subTest(evidence_request=request["request_id"]):
                self.assertEqual(request["mag_role"], "requester_and_contract_owner_only")
                self.assertTrue(request["evidence_not_claimed_by_mag_repo"])
                self.assertEqual(
                    request["accepted_payload_policy"],
                    "refs_receipts_and_shape_metadata_only",
                )
                self.assertIn("memory_body", request["forbidden_payload_classes"])
                self.assertIn("opl_runtime_state_body", request["forbidden_payload_classes"])
                self.assertIn("app_workbench_state_body", request["forbidden_payload_classes"])
        self.assertFalse(
            evidence_pack["forbidden_completion_claims"][
                "provider_completion_is_fundability_ready"
            ]
        )
        self.assertFalse(
            evidence_pack["forbidden_completion_claims"]["provider_completion_is_quality_ready"]
        )
        self.assertFalse(
            evidence_pack["forbidden_completion_claims"]["provider_completion_is_export_ready"]
        )
        self.assertFalse(
            evidence_pack["forbidden_completion_claims"]["claims_opl_replacement_exists"]
        )
        self.assertFalse(
            evidence_pack["forbidden_completion_claims"]["claims_all_bridge_exits_complete"]
        )
        self.assertFalse(
            evidence_pack["forbidden_completion_claims"][
                "claims_production_long_run_soak_complete"
            ]
        )
        self.assertTrue(evidence_pack["authority_boundary"]["mag_request_pack_only"])
        self.assertFalse(evidence_pack["authority_boundary"]["mag_implements_opl_runtime"])
        self.assertFalse(evidence_pack["authority_boundary"]["mag_implements_app_workbench"])
        self.assertFalse(evidence_pack["authority_boundary"]["mag_claims_external_evidence_exists"])
        self.assertFalse(evidence_pack["authority_boundary"]["mag_claims_long_soak_complete"])
