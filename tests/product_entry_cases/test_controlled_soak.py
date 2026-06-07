from __future__ import annotations

import tempfile

import json
import unittest
from pathlib import Path
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


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

    def test_controlled_soak_receipt_reconciliation_probe_links_mag_receipt_and_opl_ledger_ref(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "stage-closeout-task.json"
            runtime_root = Path(tmp_dir) / "runtime-state"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "controlled-soak-reconcile-1",
                        "action": "stage-attempt/closeout",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "receipt_shape": "no_regression_evidence",
                        "stage_id": "review_and_rebuttal",
                        "source_ref": "opl-ledger://mag/stage-attempt/closeout/1",
                        "closeout_summary": "MAG owner no-regression receipt for deferred controlled soak probe.",
                        "runtime_root": str(runtime_root),
                    }
                ),
                encoding="utf-8",
            )
            entry = MedAutoGrantProductEntry()
            closeout = entry.dispatch_domain_handler_task(task_path=task_path)["domain_handler_dispatch"]["result"]
            receipt = closeout["owner_receipt_evidence"]
            payload = entry.build_controlled_soak_receipt_reconciliation_proof(
                owner_receipt_evidence=receipt,
                opl_ledger_ref="opl-ledger://mag/stage-attempt/closeout/1",
                domain_handler_closeout_result=closeout,
            )

        proof = payload["receipt_reconciliation_proof"]
        self.assertEqual(
            proof["surface_kind"],
            "mag_controlled_soak_receipt_reconciliation_proof",
        )
        self.assertEqual(proof["state"], "probe_reconciled_not_live_soak_complete")
        self.assertFalse(proof["claims_production_long_run_soak_complete"])
        self.assertFalse(proof["rebuilds_opl_runtime"])
        self.assertEqual(
            proof["reconciliation"]["status"],
            "no_regression_evidence_reconciled",
        )
        self.assertTrue(proof["reconciliation"]["receipt_ref_matches_domain_handler"])
        self.assertTrue(proof["reconciliation"]["opl_ledger_ref_matches_receipt_source"])
        self.assertEqual(
            proof["mag_owner_receipt"]["receipt_ref"],
            closeout["receipt_ref"],
        )
        self.assertEqual(
            proof["no_regression_evidence"]["evidence_refs"],
            [closeout["receipt_ref"]],
        )
        self.assertIsNone(proof["typed_blocker"])
        self.assertFalse(proof["authority_boundary"]["can_declare_submission_ready_export"])
        self.assertFalse(proof["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(proof["forbidden_write_proof"]["memory_body_written"])

    def test_controlled_soak_receipt_reconciliation_probe_keeps_typed_blocker_as_blocker(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="typed_blocker",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/stage-attempt/blocked/1",
                closeout_summary="MAG owner route is still blocked; no live soak completion claim.",
                runtime_root=runtime_root,
                receipt_id="controlled-soak-blocker-1",
                closeout_refs={
                    "controlled_soak_no_regression_attempt_ref": (
                        "/product_entry_manifest/controlled_soak_no_regression_attempt"
                    ),
                },
            )["owner_receipt_evidence"]
            payload = entry.build_controlled_soak_receipt_reconciliation_proof(
                owner_receipt_evidence=receipt,
                opl_ledger_ref="opl-ledger://mag/stage-attempt/blocked/1",
            )

        proof = payload["receipt_reconciliation_proof"]
        self.assertEqual(
            proof["reconciliation"]["status"],
            "typed_blocker_reconciled",
        )
        self.assertIsNone(proof["reconciliation"]["receipt_ref_matches_domain_handler"])
        self.assertTrue(proof["reconciliation"]["opl_ledger_ref_matches_receipt_source"])
        self.assertEqual(
            proof["typed_blocker"]["blocker_kind"],
            "mag_stage_attempt_owner_receipt_required",
        )
        self.assertEqual(
            proof["typed_blocker"]["receipt_ref"],
            proof["mag_owner_receipt"]["receipt_ref"],
        )
        self.assertFalse(proof["no_regression_evidence"]["present"])
        self.assertFalse(proof["claims_production_long_run_soak_complete"])
        self.assertFalse(proof["authority_boundary"]["can_declare_fundability_ready"])

    def test_package_human_gate_typed_blocker_projects_submission_authority_boundary(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="typed_blocker",
                stage_id="package_and_submit_ready",
                source_ref="opl-ledger://mag/stage-attempt/package-human-gate/1",
                closeout_summary="MAG package stage is blocked on submission-ready export human gate.",
                runtime_root=runtime_root,
                receipt_id="package-human-gate-blocker-1",
            )["owner_receipt_evidence"]
            payload = entry.build_controlled_soak_receipt_reconciliation_proof(
                owner_receipt_evidence=receipt,
                opl_ledger_ref="opl-ledger://mag/stage-attempt/package-human-gate/1",
            )

        proof = payload["receipt_reconciliation_proof"]
        blocker = proof["typed_blocker"]
        self.assertEqual(blocker["human_gate_id"], "submission_ready_export_gate")
        self.assertTrue(blocker["human_gate_required"])
        self.assertEqual(blocker["human_gate_owner"], "med-autogrant")
        self.assertEqual(blocker["receipt_requirement"], "human_gate_receipt")
        self.assertFalse(blocker["opl_can_bypass_human_gate"])
        self.assertFalse(blocker["provider_completion_is_submission_ready"])
        self.assertFalse(blocker["can_declare_submission_ready_export"])
        self.assertIn("submission_ready", blocker["blocked_claims"])
        self.assertIn("export_ready", blocker["blocked_claims"])
        self.assertEqual(
            proof["authority_boundary"]["submission_ready_export_gate_owner"],
            "med-autogrant",
        )
        self.assertTrue(proof["authority_boundary"]["human_gate_required"])
        self.assertEqual(
            proof["authority_boundary"]["human_gate_id"],
            "submission_ready_export_gate",
        )
        self.assertFalse(proof["authority_boundary"]["provider_completion_is_submission_ready"])
        self.assertFalse(proof["claims_production_long_run_soak_complete"])

    def test_controlled_soak_receipt_reconciliation_inventory_summarizes_refs_only(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            entry = MedAutoGrantProductEntry()
            no_regression = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/stage-attempt/inventory",
                closeout_summary="MAG owner no-regression receipt for inventory projection.",
                runtime_root=runtime_root,
                receipt_id="inventory-no-regression",
            )["owner_receipt_evidence"]
            typed_blocker = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="typed_blocker",
                stage_id="package_and_submit_ready",
                source_ref="opl-ledger://mag/stage-attempt/inventory",
                closeout_summary="MAG owner blocker receipt for inventory projection.",
                runtime_root=runtime_root,
                receipt_id="inventory-typed-blocker",
            )["owner_receipt_evidence"]
            payload = entry.build_controlled_soak_receipt_reconciliation_inventory(
                owner_receipt_evidence_items=[no_regression, typed_blocker],
                opl_ledger_ref="opl-ledger://mag/stage-attempt/inventory",
                domain_handler_closeout_results=[{"receipt_ref": no_regression["receipt_instance_ref"]}],
            )

        inventory = payload["receipt_reconciliation_inventory"]
        self.assertEqual(
            inventory["surface_kind"],
            "mag_controlled_soak_receipt_reconciliation_inventory",
        )
        self.assertEqual(inventory["state"], "read_projection_only_not_live_soak_complete")
        self.assertFalse(inventory["claims_production_long_run_soak_complete"])
        self.assertEqual(inventory["summary"]["item_count"], 2)
        self.assertEqual(inventory["summary"]["domain_handler_closeout_result_count"], 1)
        self.assertEqual(inventory["summary"]["by_receipt_shape"]["no_regression_evidence"], 1)
        self.assertEqual(inventory["summary"]["by_receipt_shape"]["typed_blocker"], 1)
        self.assertEqual(inventory["summary"]["typed_blocker_count"], 1)
        self.assertEqual(inventory["summary"]["no_regression_evidence_ref_count"], 1)
        self.assertFalse(inventory["authority_boundary"]["can_declare_submission_ready_export"])
        self.assertFalse(inventory["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(inventory["forbidden_write_proof"]["grant_artifact_written"])
