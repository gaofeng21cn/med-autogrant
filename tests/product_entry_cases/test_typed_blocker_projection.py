from __future__ import annotations

import unittest


class ProductEntryTypedBlockerProjectionTest(unittest.TestCase):
    def test_non_typed_blocker_receipt_does_not_project_blocker_boundary(self) -> None:
        from med_autogrant.product_entry_parts.typed_blocker_projection import (
            build_typed_blocker_projection,
            package_submission_ready_human_gate_authority_boundary,
        )

        receipt = {
            "receipt_shape": "domain_owner_receipt",
            "stage_id": "review_and_rebuttal",
        }

        self.assertIsNone(
            build_typed_blocker_projection(
                receipt,
                blocker_kind="domain_owner_followup_required",
            )
        )
        self.assertEqual(package_submission_ready_human_gate_authority_boundary(receipt), {})

    def test_typed_blocker_projection_keeps_refs_only_owner_boundary(self) -> None:
        from med_autogrant.product_entry_parts.typed_blocker_projection import (
            build_typed_blocker_projection,
        )

        receipt = {
            "receipt_shape": "typed_blocker",
            "stage_id": "review_and_rebuttal",
            "receipt_instance_ref": "runtime://mag/receipts/typed-blocker-1.json",
            "source_ref": "opl-stage-attempt://attempt-1",
        }

        projection = build_typed_blocker_projection(
            receipt,
            blocker_kind="domain_owner_followup_required",
        )

        self.assertIsNotNone(projection)
        assert projection is not None
        self.assertEqual(projection["blocker_kind"], "domain_owner_followup_required")
        self.assertEqual(projection["owner"], "med-autogrant")
        self.assertEqual(projection["receipt_ref"], "runtime://mag/receipts/typed-blocker-1.json")
        self.assertEqual(projection["source_ref"], "opl-stage-attempt://attempt-1")
        self.assertEqual(projection["lineage"]["stage_id"], "review_and_rebuttal")
        self.assertEqual(projection["repeat_budget"]["max_repeats_before_escalation"], 2)
        self.assertFalse(projection["next_forced_delta"]["can_claim_grant_ready"])
        self.assertFalse(projection["next_forced_delta"]["can_claim_submission_ready"])
        self.assertEqual(projection["escalation_policy"]["route"], "mag_owner_surface")

    def test_package_submission_typed_blocker_requires_human_gate(self) -> None:
        from med_autogrant.product_entry_parts.typed_blocker_projection import (
            PACKAGE_SUBMISSION_READY_HUMAN_GATE_ID,
            build_typed_blocker_projection,
            package_submission_ready_human_gate_authority_boundary,
        )

        receipt = {
            "receipt_shape": "typed_blocker",
            "stage_id": "package_and_submit_ready",
            "receipt_instance_ref": "runtime://mag/receipts/package-blocker.json",
            "source_ref": "opl-stage-attempt://package",
        }

        projection = build_typed_blocker_projection(
            receipt,
            blocker_kind="manual_submission_portal_required",
        )
        boundary = package_submission_ready_human_gate_authority_boundary(receipt)

        self.assertIsNotNone(projection)
        assert projection is not None
        self.assertEqual(projection["human_gate_id"], PACKAGE_SUBMISSION_READY_HUMAN_GATE_ID)
        self.assertTrue(projection["human_gate_required"])
        self.assertFalse(projection["can_declare_submission_ready_export"])
        self.assertFalse(projection["opl_can_bypass_human_gate"])
        self.assertEqual(boundary["human_gate_id"], PACKAGE_SUBMISSION_READY_HUMAN_GATE_ID)
        self.assertTrue(boundary["human_gate_required"])
        self.assertFalse(boundary["provider_completion_is_submission_ready"])
