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
        workorder = manifest["owner_payload_response"]["manifest_consumer_evidence"][
            "sustained_consumption_followthrough_workorder"
        ]

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
