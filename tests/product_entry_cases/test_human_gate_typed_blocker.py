from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductEntryHumanGateTypedBlockerTest(unittest.TestCase):
    def test_domain_handler_dispatch_package_stage_typed_blocker_exposes_human_gate_boundary(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "stage-closeout-task.json"
            runtime_root = Path(tmp_dir) / "runtime-state"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "stage-closeout-package-blocked",
                        "action": "stage-attempt/closeout",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "receipt_shape": "typed_blocker",
                        "stage_id": "package_and_submit_ready",
                        "source_ref": "opl-stage-attempt://stage-closeout-package-blocked",
                        "closeout_summary": "Submission-ready export is blocked on MAG-owned human gate.",
                        "runtime_root": str(runtime_root),
                    }
                ),
                encoding="utf-8",
            )
            payload = MedAutoGrantProductEntry().dispatch_domain_handler_task(task_path=task_path)

        blocker = payload["domain_handler_dispatch"]["result"]["typed_blocker"]
        self.assertEqual(blocker["blocker_kind"], "mag_stage_attempt_owner_receipt_required")
        self.assertEqual(blocker["human_gate_id"], "submission_ready_export_gate")
        self.assertTrue(blocker["human_gate_required"])
        self.assertEqual(blocker["human_gate_owner"], "med-autogrant")
        self.assertEqual(blocker["receipt_requirement"], "human_gate_receipt")
        self.assertFalse(blocker["opl_can_bypass_human_gate"])
        self.assertFalse(blocker["can_declare_submission_ready_export"])
        self.assertFalse(blocker["provider_completion_is_submission_ready"])
        self.assertIn("production_ready", blocker["blocked_claims"])
        self.assertEqual(blocker["lineage"]["stage_id"], "package_and_submit_ready")
        self.assertEqual(blocker["lineage"]["source_ref"], "opl-stage-attempt://stage-closeout-package-blocked")
        self.assertEqual(blocker["lineage"]["receipt_ref"], blocker["receipt_ref"])
        self.assertEqual(blocker["repeat_budget"]["max_repeats_before_escalation"], 2)
        self.assertEqual(blocker["repeat_budget"]["budget_scope"], "same_stage_same_blocker_kind")
        self.assertEqual(
            blocker["next_forced_delta"]["required_delta_kind"],
            "grant_deliverable_progress_delta_or_domain_owned_typed_blocker",
        )
        self.assertEqual(blocker["next_forced_delta"]["stage_id"], "package_and_submit_ready")
        self.assertEqual(blocker["next_forced_delta"]["blocker_kind"], "mag_stage_attempt_owner_receipt_required")
        self.assertEqual(blocker["next_forced_delta"]["next_owner"], "med-autogrant")
        self.assertIn("typed_blocker_ref", blocker["next_forced_delta"]["accepted_return_shapes"])
        self.assertFalse(blocker["next_forced_delta"]["can_claim_grant_ready"])
        self.assertFalse(blocker["next_forced_delta"]["can_claim_submission_ready"])
        self.assertEqual(blocker["escalation_owner"], "med-autogrant")
        self.assertEqual(blocker["escalation_policy"]["route"], "mag_owner_surface")
