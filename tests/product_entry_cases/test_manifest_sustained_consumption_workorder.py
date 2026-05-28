from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryManifestSustainedConsumptionWorkorderTest(unittest.TestCase):
    def test_manifest_consumer_exposes_sustained_consumption_workorder_without_ready_claim(
        self,
    ) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        manifest = payload["product_entry_manifest"]
        owner_payload = manifest["owner_payload_response"]
        manifest_consumer = owner_payload["manifest_consumer_evidence"]
        workorder = manifest["owner_payload_response"]["manifest_consumer_evidence"][
            "sustained_consumption_followthrough_workorder"
        ]
        sustained_evidence = manifest["manifest_sustained_consumption_evidence"]

        self.assertEqual(
            workorder["surface_kind"],
            "mag_manifest_sustained_consumption_followthrough_workorder",
        )
        self.assertEqual(workorder["status"], "requires_real_app_operator_or_default_caller_payload")
        self.assertEqual(workorder["authority_command"], "authority manifest-consumption-payload")
        self.assertEqual(
            workorder["authority_command_internal"],
            "manifest-sustained-consumption-payload",
        )
        self.assertEqual(workorder["payload_owner"], "app_operator_or_release_default_caller")
        self.assertEqual(
            workorder["required_operator_payload_refs"],
            [
                "app_operator_consumption_ref",
                "default_caller_consumption_ref",
                "owner_payload_response_ref",
                "workspace_receipt_scaleout_evidence_ref",
                "no_forbidden_write_ref",
                "long_soak_or_typed_blocker_ref",
            ],
        )
        self.assertEqual(
            workorder["allowed_operator_payload_fields"],
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
        self.assertTrue(
            workorder["accepted_payload_paths"]["sustained_consumption_refs_path"][
                "requires_long_soak_or_typed_blocker_ref"
            ]
        )
        self.assertFalse(workorder["accepted_payload_paths"]["typed_blocker_path"]["success_claimed"])
        self.assertFalse(workorder["empty_payload_template_is_success_evidence"])
        self.assertTrue(workorder["rejects_unknown_operator_payload_fields"])
        self.assertFalse(workorder["operator_payload_submitted"])
        self.assertFalse(workorder["claims_sustained_app_consumption_complete"])
        self.assertFalse(workorder["claims_grant_ready"])
        self.assertFalse(workorder["claims_submission_ready"])
        self.assertFalse(workorder["claims_provider_long_soak_complete"])
        self.assertFalse(workorder["authority_boundary"]["can_create_owner_receipt"])
        self.assertFalse(
            workorder["authority_boundary"]["can_declare_app_sustained_consumption_complete"]
        )
        self.assertFalse(
            workorder["authority_boundary"]["can_declare_provider_long_soak_complete"]
        )
        self.assertEqual(
            owner_payload["source_surface_refs"]["manifest_sustained_consumption_evidence_ref"],
            "contracts/production_acceptance/"
            "mag-manifest-sustained-consumption-evidence-20260528.json",
        )
        self.assertEqual(
            owner_payload["manifest_sustained_consumption_evidence_ref"],
            "contracts/production_acceptance/"
            "mag-manifest-sustained-consumption-evidence-20260528.json",
        )
        self.assertEqual(
            manifest_consumer["consumed_surface_refs"][
                "manifest_sustained_consumption_evidence_ref"
            ],
            "/product_entry_manifest/manifest_sustained_consumption_evidence",
        )
        self.assertEqual(
            manifest_consumer["consumed_surface_refs"][
                "manifest_sustained_consumption_payload_response_ref"
            ],
            "/product_entry_manifest/manifest_sustained_consumption_evidence/"
            "manifest_sustained_consumption_payload_response",
        )
        self.assertEqual(
            manifest_consumer["observed_counts"][
                "manifest_sustained_consumption_payload_response_count"
            ],
            1,
        )
        self.assertEqual(
            manifest_consumer["manifest_sustained_consumption_payload_status"],
            "sustained_consumption_payload_refs_ready",
        )
        self.assertEqual(
            manifest_consumer["manifest_sustained_consumption_recommended_payload_path"],
            "sustained_consumption_refs_path",
        )
        self.assertTrue(
            manifest_consumer["manifest_sustained_consumption_operator_payload_submitted"]
        )
        self.assertTrue(
            sustained_evidence["manifest_sustained_consumption_payload_response"][
                "operator_payload_submitted"
            ]
        )
        self.assertEqual(
            owner_payload["manifest_sustained_consumption_payload_response"],
            sustained_evidence["manifest_sustained_consumption_payload_response"],
        )
        self.assertEqual(
            sustained_evidence["surface_kind"],
            "mag_manifest_sustained_consumption_evidence.v1",
        )
        self.assertEqual(
            sustained_evidence["manifest_sustained_consumption_payload_response"][
                "recommended_payload_path"
            ],
            "sustained_consumption_refs_path",
        )
        self.assertFalse(
            sustained_evidence["manifest_sustained_consumption_payload_response"][
                "claims_sustained_app_consumption_complete"
            ]
        )
        self.assertFalse(
            sustained_evidence["manifest_sustained_consumption_payload_response"][
                "claims_provider_long_soak_complete"
            ]
        )
        self.assertFalse(sustained_evidence["claims"]["claims_submission_ready"])
        self.assertFalse(sustained_evidence["authority_boundary"]["can_create_owner_receipt"])
