from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryGrantTransitionOracleTest(unittest.TestCase):
    def test_manifest_exposes_mag_owned_transition_table_and_oracle_fixtures(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]

        transition_oracle = manifest["grant_transition_oracle"]
        self.assertEqual(transition_oracle["surface_kind"], "mag_grant_transition_oracle")
        self.assertEqual(transition_oracle["state"], "domain_spec_landed_external_runner_gate")
        self.assertEqual(transition_oracle["runner_owner"], "one-person-lab")
        self.assertEqual(transition_oracle["transition_table_status"], "landed")
        self.assertEqual(transition_oracle["oracle_fixture_status"], "landed")
        self.assertEqual(
            transition_oracle["stage_control_plane_ref"],
            "/product_entry_manifest/family_stage_control_plane",
        )
        self.assertEqual(
            transition_oracle["action_catalog_ref"],
            "/product_entry_manifest/family_action_catalog",
        )
        self.assertFalse(transition_oracle["authority_boundary"]["opl_can_infer_fundability_ready"])
        self.assertFalse(transition_oracle["authority_boundary"]["opl_can_infer_authoring_quality_ready"])
        self.assertFalse(transition_oracle["authority_boundary"]["opl_can_infer_submission_ready_export_ready"])

        transition_ids = {transition["transition_id"] for transition in transition_oracle["transition_table"]}
        self.assertIn("fundability_blocked_to_human_gate", transition_ids)
        self.assertIn("review_closed_to_package_and_submit_ready", transition_ids)
        self.assertIn("package_blocked_to_human_gate", transition_ids)
        fixture_transition_ids = {
            fixture["expected_transition_id"]
            for fixture in transition_oracle["oracle_fixtures"]
        }
        self.assertLessEqual(fixture_transition_ids, transition_ids)
        self.assertEqual(transition_oracle["validation"]["status"], "ready_for_opl_runner_ingestion")
        self.assertEqual(transition_oracle["validation"]["missing_stage_refs"], [])
        self.assertEqual(transition_oracle["validation"]["missing_action_refs"], [])
        self.assertEqual(transition_oracle["validation"]["missing_fixture_transition_refs"], [])

    def test_ideal_state_closure_reuses_landed_transition_oracle_surface(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]

        closure_oracle = manifest["ideal_state_closure_status"]["mag_owned_transition_oracle"]
        manifest_oracle = manifest["grant_transition_oracle"]
        self.assertEqual(closure_oracle["oracle_id"], manifest_oracle["oracle_id"])
        self.assertEqual(closure_oracle["state"], manifest_oracle["state"])
        self.assertEqual(closure_oracle["transition_table"], manifest_oracle["transition_table"])
        self.assertEqual(closure_oracle["oracle_fixtures"], manifest_oracle["oracle_fixtures"])
        self.assertEqual(closure_oracle["transition_table_status"], "landed")
        self.assertEqual(closure_oracle["oracle_fixture_status"], "landed")
