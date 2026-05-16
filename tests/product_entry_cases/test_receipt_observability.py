from __future__ import annotations

import tempfile

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryReceiptObservabilityTest(unittest.TestCase):
    def test_receipt_observability_summarizes_no_regression_and_typed_blocker_refs(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.receipt_observability import (
            build_controlled_soak_receipt_observability_summary,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            entry = MedAutoGrantProductEntry()
            no_regression = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/stage-attempt/observability",
                closeout_summary="MAG no-regression receipt for refs-only observability.",
                runtime_root=runtime_root,
                receipt_id="observability-no-regression",
            )["owner_receipt_evidence"]
            typed_blocker = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="typed_blocker",
                stage_id="package_and_submit_ready",
                source_ref="opl-ledger://mag/stage-attempt/observability",
                closeout_summary="MAG typed blocker receipt for refs-only observability.",
                runtime_root=runtime_root,
                receipt_id="observability-typed-blocker",
            )["owner_receipt_evidence"]
            inventory_payload = entry.build_controlled_soak_receipt_reconciliation_inventory(
                owner_receipt_evidence_items=[no_regression, typed_blocker],
                opl_ledger_ref="opl-ledger://mag/stage-attempt/observability",
                sidecar_closeout_results=[{"receipt_ref": no_regression["receipt_instance_ref"]}],
            )

        summary = build_controlled_soak_receipt_observability_summary(inventory_payload)
        method_summary = entry.build_controlled_soak_receipt_observability_summary(
            receipt_reconciliation_inventory=inventory_payload,
        )

        self.assertEqual(
            summary["surface_kind"],
            "mag_controlled_soak_receipt_observability_summary",
        )
        self.assertEqual(method_summary, summary)
        self.assertEqual(summary["owner"], "med-autogrant")
        self.assertEqual(summary["target_domain_id"], "med-autogrant")
        self.assertEqual(summary["state"], "read_only_observability_summary_not_live_soak_complete")
        self.assertEqual(summary["source_inventory_summary"]["item_count"], 2)
        self.assertEqual(summary["source_inventory_summary"]["typed_blocker_count"], 1)
        self.assertEqual(summary["source_inventory_summary"]["no_regression_evidence_ref_count"], 1)
        self.assertEqual(
            summary["source_inventory_summary"]["by_receipt_shape"],
            {"no_regression_evidence": 1, "typed_blocker": 1},
        )
        self.assertEqual(
            summary["source_inventory_summary"]["by_reconciliation_status"],
            {
                "no_regression_evidence_reconciled": 1,
                "typed_blocker_reconciled": 1,
            },
        )
        self.assertEqual(
            summary["operator_observability"]["observability_export_kind"],
            "opl_runtime_observability_export",
        )
        self.assertEqual(
            summary["operator_observability"]["consumption_policy"],
            "read_only_refs_and_counts_no_repair_execution",
        )
        self.assertEqual(
            summary["operator_observability"]["status"],
            "attention_required_typed_blocker_present",
        )
        self.assertEqual(summary["operator_observability"]["receipt_ref_count"], 2)
        self.assertEqual(summary["operator_observability"]["typed_blocker_ref_count"], 1)
        self.assertEqual(summary["operator_observability"]["no_regression_evidence_ref_count"], 1)
        self.assertEqual(
            summary["blocker_summary"]["typed_blocker_refs"],
            [typed_blocker["receipt_instance_ref"]],
        )
        self.assertEqual(
            summary["no_regression_summary"]["no_regression_evidence_refs"],
            [no_regression["receipt_instance_ref"]],
        )
        self.assertEqual(
            summary["stage_summary"]["by_stage_id"],
            {"review_and_rebuttal": 1, "package_and_submit_ready": 1},
        )
        self.assertTrue(summary["authority_boundary"]["opl_ref_consumer_only"])
        self.assertTrue(summary["authority_boundary"]["mag_owner_receipt_authority"])
        self.assertFalse(summary["authority_boundary"]["can_execute_repair"])
        self.assertFalse(summary["authority_boundary"]["can_schedule_retry"])
        self.assertFalse(summary["authority_boundary"]["can_write_opl_stage_attempt_ledger"])
        self.assertFalse(summary["authority_boundary"]["can_declare_grant_ready"])
        self.assertFalse(summary["authority_boundary"]["can_declare_export_ready"])
        self.assertFalse(summary["source_inventory_ref"]["mag_writes_opl_ledger"])
        self.assertFalse(summary["source_inventory_ref"]["opl_holds_grant_truth"])
        self.assertFalse(summary["source_inventory_ref"]["claims_production_long_run_soak_complete"])
        self.assertFalse(summary["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(summary["forbidden_write_proof"]["grant_artifact_written"])
        self.assertFalse(summary["forbidden_write_proof"]["memory_body_written"])

    def test_receipt_observability_fails_closed_for_empty_or_invalid_inventory(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.receipt_observability import (
            build_controlled_soak_receipt_observability_summary,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/stage-attempt/invalid-observability",
                closeout_summary="MAG no-regression receipt for fail-closed observability.",
                runtime_root=runtime_root,
                receipt_id="observability-invalid",
            )["owner_receipt_evidence"]
            inventory = entry.build_controlled_soak_receipt_reconciliation_inventory(
                owner_receipt_evidence_items=[receipt],
                opl_ledger_ref="opl-ledger://mag/stage-attempt/invalid-observability",
            )["receipt_reconciliation_inventory"]

        empty_inventory = deepcopy(inventory)
        empty_inventory["items"] = []
        empty_inventory["summary"] = dict(inventory["summary"], item_count=0)
        with self.assertRaises(WorkspaceStateError):
            build_controlled_soak_receipt_observability_summary(empty_inventory)

        wrong_surface = deepcopy(inventory)
        wrong_surface["surface_kind"] = "grant_ready_receipt_inventory"
        with self.assertRaises(WorkspaceStateError):
            build_controlled_soak_receipt_observability_summary(wrong_surface)

        inconsistent_summary = deepcopy(inventory)
        inconsistent_summary["summary"]["item_count"] = 99
        with self.assertRaises(WorkspaceStateError):
            build_controlled_soak_receipt_observability_summary(inconsistent_summary)

        forbidden_write = deepcopy(inventory)
        forbidden_write["forbidden_write_proof"]["grant_artifact_written"] = True
        with self.assertRaises(WorkspaceStateError):
            build_controlled_soak_receipt_observability_summary(forbidden_write)

    def test_receipt_observability_does_not_leak_body_or_artifact_content(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.receipt_observability import (
            build_controlled_soak_receipt_observability_summary,
        )

        forbidden_tokens = {
            "SECRET_GRANT_ARTIFACT_BODY",
            "SECRET_STRATEGY_MEMORY_BODY",
            "specific aims narrative content",
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/stage-attempt/no-leak",
                closeout_summary=(
                    "SECRET_GRANT_ARTIFACT_BODY and SECRET_STRATEGY_MEMORY_BODY "
                    "must remain outside observability."
                ),
                runtime_root=runtime_root,
                receipt_id="observability-no-leak",
                closeout_refs={
                    "grant_artifact_ref": "artifact://safe/ref",
                    "grant_artifact_body": "specific aims narrative content",
                    "strategy_memory_body": "SECRET_STRATEGY_MEMORY_BODY",
                },
            )["owner_receipt_evidence"]
            inventory_payload = entry.build_controlled_soak_receipt_reconciliation_inventory(
                owner_receipt_evidence_items=[receipt],
                opl_ledger_ref="opl-ledger://mag/stage-attempt/no-leak",
                sidecar_closeout_results=[{"receipt_ref": receipt["receipt_instance_ref"]}],
            )

        summary = build_controlled_soak_receipt_observability_summary(
            inventory_payload["receipt_reconciliation_inventory"]
        )
        serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)

        for token in forbidden_tokens:
            self.assertNotIn(token, serialized)
        self.assertNotIn("closeout_summary", serialized)
        self.assertNotIn("grant_artifact_body", serialized)
        self.assertNotIn("strategy_memory_body", serialized)
        self.assertNotIn("artifact://safe/ref", serialized)
        self.assertEqual(
            set(summary["operator_observability"]["receipt_refs"]),
            {receipt["receipt_instance_ref"]},
        )
        self.assertEqual(
            set(summary["operator_observability"]["no_regression_evidence_refs"]),
            {receipt["receipt_instance_ref"]},
        )
