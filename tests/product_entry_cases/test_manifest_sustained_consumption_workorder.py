from __future__ import annotations

import unittest
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


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
                "operator_payload_attempts",
            ],
        )
        self.assertTrue(
            workorder["accepted_payload_paths"]["sustained_consumption_refs_path"][
                "requires_long_soak_or_typed_blocker_ref"
            ]
        )
        self.assertEqual(
            workorder["provider_long_soak_followthrough"]["status"],
            "requires_temporal_provider_long_soak_window_evidence",
        )
        self.assertTrue(
            workorder["provider_long_soak_followthrough"][
                "requires_temporal_provider_long_soak_window_evidence"
            ]
        )
        self.assertFalse(
            workorder["provider_long_soak_followthrough"][
                "claims_provider_long_soak_complete"
            ]
        )
        self.assertFalse(workorder["accepted_payload_paths"]["typed_blocker_path"]["success_claimed"])
        self.assertEqual(
            workorder["accepted_payload_paths"]["operator_payload_attempts_path"][
                "required_operator_payload_refs"
            ],
            ["operator_payload_attempts"],
        )
        self.assertFalse(
            workorder["accepted_payload_paths"]["operator_payload_attempts_path"][
                "success_claimed"
            ]
        )
        self.assertIn("attempt_id", workorder["operator_payload_attempt_template"])
        self.assertFalse(workorder["operator_payload_attempts_are_success_evidence"])
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
            manifest_consumer["consumed_surface_refs"][
                "manifest_sustained_consumption_grouped_cli_regression_evidence_ref"
            ],
            "/product_entry_manifest/manifest_sustained_consumption_evidence/"
            "grouped_cli_regression_evidence",
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
        self.assertEqual(
            manifest_consumer["manifest_sustained_consumption_provider_long_soak_status"],
            "blocked_by_provider_long_soak_typed_blocker",
        )
        self.assertEqual(
            manifest_consumer["manifest_sustained_consumption_provider_long_soak_typed_blocker_refs"],
            [
                "typed-blocker:mag/manifest-sustained-consumption/"
                "provider-long-soak-window-still-open/2026-05-28"
            ],
        )
        self.assertEqual(
            manifest_consumer["manifest_sustained_consumption_provider_long_soak_evidence_refs"],
            [],
        )
        self.assertTrue(
            manifest_consumer["manifest_sustained_consumption_operator_payload_submitted"]
        )
        self.assertEqual(
            manifest_consumer["manifest_sustained_consumption_grouped_cli_regression_status"],
            "direct_cli_default_caller_payload_path_and_fail_closed_errors_verified",
        )
        self.assertTrue(
            manifest_consumer[
                "manifest_sustained_consumption_grouped_cli_success_path_verified"
            ]
        )
        self.assertTrue(
            manifest_consumer[
                "manifest_sustained_consumption_grouped_cli_unknown_field_rejection_verified"
            ]
        )
        self.assertTrue(
            manifest_consumer[
                "manifest_sustained_consumption_grouped_cli_mixed_path_rejection_verified"
            ]
        )
        self.assertFalse(
            manifest_consumer[
                "manifest_sustained_consumption_grouped_cli_claims_provider_long_soak_complete"
            ]
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
        self.assertFalse(
            sustained_evidence["manifest_sustained_consumption_payload_response"][
                "provider_long_soak_followthrough"
            ]["claims_provider_long_soak_complete"]
        )
        self.assertFalse(sustained_evidence["claims"]["claims_submission_ready"])
        self.assertFalse(sustained_evidence["authority_boundary"]["can_create_owner_receipt"])
