from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryControlledSoakTest(unittest.TestCase):
    def test_manifest_exposes_deferred_controlled_soak_blocker_without_opl_truth_ownership(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        controlled_soak = payload["product_entry_manifest"]["controlled_soak_no_regression_attempt"]
        self.assertEqual(controlled_soak["surface_kind"], "controlled_soak_no_regression_attempt")
        self.assertEqual(controlled_soak["attempt_id"], "mag.controlled_soak.no_regression_attempt.v1")
        self.assertEqual(controlled_soak["state"], "deferred_typed_blocker")
        self.assertTrue(controlled_soak["controlled_soak_apply_contract_open"])
        self.assertEqual(
            controlled_soak["deferred_blocker"]["blocker_kind"],
            "domain_owner_receipt_required",
        )
        self.assertEqual(
            controlled_soak["deferred_blocker"]["source_contract"],
            "opl_temporal_controlled_stage_attempt_apply_contract",
        )
        self.assertEqual(
            controlled_soak["deferred_blocker"]["required_return_shapes"],
            ["domain_owner_receipt_ref", "typed_blocker", "no_regression_evidence_ref"],
        )
        self.assertIn(
            "/product_entry_manifest/controlled_stage_attempt_projection",
            controlled_soak["no_regression_surface_refs"],
        )
        self.assertFalse(controlled_soak["authority_boundary"]["can_hold_fundability_verdict"])
        self.assertFalse(controlled_soak["authority_boundary"]["can_hold_submission_ready_export_verdict"])
        self.assertFalse(controlled_soak["repository_boundary"]["repo_tracks_grant_artifact"])
        self.assertFalse(controlled_soak["repository_boundary"]["repo_tracks_receipt_instance"])
