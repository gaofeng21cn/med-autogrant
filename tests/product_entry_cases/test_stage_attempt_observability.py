from __future__ import annotations

import tempfile

import unittest
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductEntryStageAttemptObservabilityTest(unittest.TestCase):
    def test_stage_attempt_observability_projection_summarizes_refs_only_for_opl(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.stage_attempt_observability import (
            build_stage_attempt_observability_projection,
        )

        entry = MedAutoGrantProductEntry()
        manifest = entry.build_product_entry_manifest(
            input_path=CRITIQUE_EXAMPLE_PATH,
        )["product_entry_manifest"]
        with tempfile.TemporaryDirectory() as tmp_dir:
            no_regression = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/stage-attempt/observability",
                closeout_summary="MAG owner no-regression receipt for OPL usage projection.",
                runtime_root=tmp_dir,
                receipt_id="observability-no-regression",
            )["owner_receipt_evidence"]
            typed_blocker = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="typed_blocker",
                stage_id="package_and_submit_ready",
                source_ref="opl-ledger://mag/stage-attempt/observability",
                closeout_summary="MAG owner typed blocker for OPL control-loop projection.",
                runtime_root=tmp_dir,
                receipt_id="observability-typed-blocker",
            )["owner_receipt_evidence"]
            inventory = entry.build_controlled_soak_receipt_reconciliation_inventory(
                owner_receipt_evidence_items=[no_regression, typed_blocker],
                opl_ledger_ref="opl-ledger://mag/stage-attempt/observability",
            )["receipt_reconciliation_inventory"]

        payload = build_stage_attempt_observability_projection(
            controlled_stage_attempt_projection=manifest["controlled_stage_attempt_projection"],
            receipt_reconciliation_inventory=inventory,
            opl_usage_projection_ref="opl://family/stage-attempt/usage-projection/mag",
            opl_control_loop_projection_ref="opl://family/stage-attempt/control-loop/mag",
        )
        method_payload = entry.build_stage_attempt_observability_projection(
            controlled_stage_attempt_projection=manifest["controlled_stage_attempt_projection"],
            receipt_reconciliation_inventory=inventory,
            opl_usage_projection_ref="opl://family/stage-attempt/usage-projection/mag",
            opl_control_loop_projection_ref="opl://family/stage-attempt/control-loop/mag",
        )

        projection = payload["stage_attempt_observability_projection"]
        self.assertEqual(method_payload, payload)
        self.assertEqual(projection["surface_kind"], "mag_stage_attempt_observability_projection")
        self.assertEqual(projection["state"], "refs_only_projection_ready_for_opl_consumption")
        self.assertEqual(
            projection["stage_attempt"]["receipt_refs"],
            manifest["controlled_stage_attempt_projection"]["receipt_refs"],
        )
        self.assertEqual(projection["receipt_inventory_summary"]["item_count"], 2)
        self.assertEqual(projection["receipt_inventory_summary"]["typed_blocker_count"], 1)
        self.assertEqual(
            projection["control_loop_handoff"]["handoff_state"],
            "typed_blocker_refs_ready_for_opl_control_loop",
        )
        self.assertEqual(projection["blocked_receipt_refs"], [typed_blocker["receipt_instance_ref"]])
        self.assertEqual(projection["no_regression_evidence_refs"], [no_regression["receipt_instance_ref"]])
        self.assertFalse(projection["claims"]["claims_opl_provider_completion"])
        self.assertFalse(projection["claims"]["claims_production_long_run_soak_complete"])
        self.assertFalse(projection["claims"]["claims_grant_fundability_ready"])
        self.assertFalse(projection["claims"]["claims_authoring_quality_ready"])
        self.assertFalse(projection["claims"]["claims_submission_ready_export"])
        self.assertFalse(projection["authority_boundary"]["mag_implements_generic_attempt_ledger"])
        self.assertFalse(projection["authority_boundary"]["mag_implements_generic_runner"])
        self.assertFalse(projection["consumes_opl_surfaces"]["mag_writes_opl_stage_attempt_records"])
        self.assertFalse(projection["consumes_opl_surfaces"]["mag_dispatches_opl_retries"])
        self.assertFalse(projection["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(projection["forbidden_write_proof"]["memory_body_written"])

    def test_stage_attempt_observability_rejects_inventory_that_claims_live_soak_ready(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.stage_attempt_observability import (
            build_stage_attempt_observability_projection,
        )

        entry = MedAutoGrantProductEntry()
        manifest = entry.build_product_entry_manifest(
            input_path=CRITIQUE_EXAMPLE_PATH,
        )["product_entry_manifest"]
        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/stage-attempt/invalid",
                closeout_summary="MAG owner no-regression receipt for invalid projection fixture.",
                runtime_root=tmp_dir,
                receipt_id="invalid-live-soak",
            )["owner_receipt_evidence"]
            inventory = entry.build_controlled_soak_receipt_reconciliation_inventory(
                owner_receipt_evidence_items=[receipt],
                opl_ledger_ref="opl-ledger://mag/stage-attempt/invalid",
            )["receipt_reconciliation_inventory"]
        inventory["claims_production_long_run_soak_complete"] = True

        with self.assertRaisesRegex(WorkspaceStateError, "production long-run soak"):
            build_stage_attempt_observability_projection(
                controlled_stage_attempt_projection=manifest["controlled_stage_attempt_projection"],
                receipt_reconciliation_inventory=inventory,
                opl_usage_projection_ref="opl://family/stage-attempt/usage-projection/mag",
                opl_control_loop_projection_ref="opl://family/stage-attempt/control-loop/mag",
            )
