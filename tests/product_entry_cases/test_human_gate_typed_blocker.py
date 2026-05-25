from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductEntryHumanGateTypedBlockerTest(unittest.TestCase):
    def test_sidecar_dispatch_package_stage_typed_blocker_exposes_human_gate_boundary(self) -> None:
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
            payload = MedAutoGrantProductEntry().dispatch_sidecar_task(task_path=task_path)

        blocker = payload["sidecar_dispatch"]["result"]["typed_blocker"]
        self.assertEqual(blocker["blocker_kind"], "mag_stage_attempt_owner_receipt_required")
        self.assertEqual(blocker["human_gate_id"], "submission_ready_export_gate")
        self.assertTrue(blocker["human_gate_required"])
        self.assertEqual(blocker["human_gate_owner"], "med-autogrant")
        self.assertEqual(blocker["receipt_requirement"], "human_gate_receipt")
        self.assertFalse(blocker["opl_can_bypass_human_gate"])
        self.assertFalse(blocker["can_declare_submission_ready_export"])
        self.assertFalse(blocker["provider_completion_is_submission_ready"])
        self.assertIn("production_ready", blocker["blocked_claims"])
