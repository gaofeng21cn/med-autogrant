from __future__ import annotations

import tempfile

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

    def test_oracle_domain_handler_closeout_writes_no_regression_owner_receipt_refs(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        manifest_payload = entry.build_product_entry_manifest(input_path=str(CRITIQUE_EXAMPLE_PATH))
        manifest = manifest_payload["product_entry_manifest"]
        oracle = manifest["grant_transition_oracle"]
        fixture = next(
            item
            for item in oracle["oracle_fixtures"]
            if item["fixture_id"] == "quality_closed_to_package"
        )
        transition = next(
            item
            for item in oracle["transition_table"]
            if item["transition_id"] == fixture["expected_transition_id"]
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "oracle-no-regression-closeout.json"
            runtime_root = Path(tmp_dir) / "runtime-state"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "oracle-no-regression-closeout-1",
                        "action": "stage-attempt/closeout",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "receipt_shape": "no_regression_evidence",
                        "stage_id": transition["from_stage_id"],
                        "source_ref": "opl-transition-oracle://quality_closed_to_package",
                        "closeout_summary": "Oracle fixture closed with no regression over MAG-owned refs.",
                        "runtime_root": str(runtime_root),
                        "grant_transition_oracle_ref": "/product_entry_manifest/grant_transition_oracle",
                        "oracle_fixture_id": fixture["fixture_id"],
                        "transition_id": transition["transition_id"],
                    }
                ),
                encoding="utf-8",
            )
            closeout_payload = entry.dispatch_domain_handler_task(task_path=task_path)
            receipt = closeout_payload["domain_handler_dispatch"]["result"]["owner_receipt_evidence"]
            receipt_path = Path(receipt["receipt_instance_ref"])
            persisted_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

        dispatch = closeout_payload["domain_handler_dispatch"]
        result = dispatch["result"]
        receipt_refs = result["receipt_refs"]
        closeout_refs = result["closeout_refs"]

        self.assertEqual(dispatch["action"], "stage-attempt/closeout")
        self.assertEqual(result["surface_kind"], "domain_handler_stage_attempt_closeout_result")
        self.assertEqual(result["return_shape"], "no_regression_evidence")
        self.assertEqual(result["receipt_ref"], receipt_refs["owner_receipt_ref"])
        self.assertEqual(receipt_refs["no_regression_evidence_ref"], receipt["receipt_instance_ref"])
        self.assertTrue(receipt_refs["opl_consumes_receipt_ref_only"])
        self.assertEqual(closeout_refs["grant_transition_oracle_ref"], "/product_entry_manifest/grant_transition_oracle")
        self.assertEqual(closeout_refs["controlled_soak_no_regression_attempt_ref"], "/product_entry_manifest/controlled_soak_no_regression_attempt")
        self.assertEqual(closeout_refs["oracle_fixture_id"], fixture["fixture_id"])
        self.assertEqual(closeout_refs["transition_id"], transition["transition_id"])
        self.assertEqual(receipt["closeout_refs"], closeout_refs)
        self.assertEqual(persisted_receipt["closeout_refs"], closeout_refs)
        self.assertFalse(receipt["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(receipt["forbidden_write_proof"]["grant_artifact_written"])
        self.assertFalse(receipt["forbidden_write_proof"]["memory_body_written"])
        self.assertFalse(manifest["ideal_state_closure_status"]["claims_production_long_run_soak_complete"])
