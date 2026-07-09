from __future__ import annotations

import unittest
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import codex_execution_attempt, codex_review_attempt


class ProductEntryCodexStageReceiptTest(unittest.TestCase):
    def test_codex_stage_receipt_bundle_requires_independent_review_before_ready_refs(self) -> None:
        from med_autogrant.product_entry_parts.codex_stage_receipts import (
            build_codex_stage_execution_receipt_bundle,
        )

        projection = build_codex_stage_execution_receipt_bundle(
            stage_id="review_and_rebuttal",
            execution_attempts=[codex_execution_attempt(include_stage_pack_ref=True)],
            review_attempts=[codex_review_attempt()],
        )

        self.assertEqual(projection["surface_kind"], "mag_codex_stage_execution_receipt_bundle")
        self.assertEqual(projection["state"], "codex_stage_receipts_ready_not_quality_ready")
        self.assertEqual(projection["executor_policy"]["default_executor"], "codex_cli")
        self.assertTrue(projection["executor_policy"]["executor_first"])
        self.assertTrue(projection["executor_policy"]["review_must_have_separate_invocation"])
        self.assertEqual(projection["summary"]["execution_attempt_count"], 1)
        self.assertEqual(projection["summary"]["independent_review_attempt_count"], 1)
        self.assertEqual(projection["summary"]["reviewed_execution_attempt_count"], 1)
        self.assertEqual(
            projection["execution_attempts"][0]["refs"]["receipt_ref"],
            "runtime://mag/receipts/stage/critique-001.json",
        )
        self.assertEqual(
            projection["review_attempts"][0]["refs"]["review_receipt_ref"],
            "runtime://mag/receipts/review/review-critique-001.json",
        )
        self.assertEqual(
            projection["quality_gate_effect"]["state"],
            "independent_review_receipt_refs_ready_not_quality_ready",
        )
        self.assertFalse(projection["quality_gate_effect"]["ready_verdict_authorized"])
        self.assertFalse(projection["authority_boundary"]["review_receipt_refs_equal_quality_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_fundability_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_submission_ready"])

    def test_missing_review_fails_closed_for_ready_claims(self) -> None:
        from med_autogrant.product_entry_parts.codex_stage_receipts import (
            build_codex_stage_execution_receipt_bundle,
        )

        projection = build_codex_stage_execution_receipt_bundle(
            stage_id="review_and_rebuttal",
            execution_attempts=[codex_execution_attempt(include_stage_pack_ref=True)],
            review_attempts=[],
        )

        self.assertEqual(projection["state"], "independent_review_receipt_missing")
        self.assertEqual(projection["quality_gate_effect"]["state"], "fail_closed_typed_blocker_required")
        self.assertEqual(projection["quality_gate_effect"]["blocker_id"], "independent_review_receipt_required")
        self.assertTrue(projection["quality_gate_effect"]["typed_blocker_required"])
        self.assertFalse(projection["quality_gate_effect"]["ready_verdict_authorized"])

    def test_review_must_have_separate_invocation_task_and_context(self) -> None:
        from med_autogrant.product_entry_parts.codex_stage_receipts import (
            build_codex_stage_execution_receipt_bundle,
        )

        shared_invocation = codex_review_attempt()
        shared_invocation["review_invocation_ref"] = codex_execution_attempt()["invocation_ref"]
        with self.assertRaises(WorkspaceStateError):
            build_codex_stage_execution_receipt_bundle(
                stage_id="review_and_rebuttal",
                execution_attempts=[codex_execution_attempt()],
                review_attempts=[shared_invocation],
            )

        shared_task = codex_review_attempt()
        shared_task["review_task_record_ref"] = codex_execution_attempt()["task_record_ref"]
        with self.assertRaises(WorkspaceStateError):
            build_codex_stage_execution_receipt_bundle(
                stage_id="review_and_rebuttal",
                execution_attempts=[codex_execution_attempt()],
                review_attempts=[shared_task],
            )

        shared_context = codex_review_attempt()
        shared_context["independent_context"] = False
        with self.assertRaises(WorkspaceStateError):
            build_codex_stage_execution_receipt_bundle(
                stage_id="review_and_rebuttal",
                execution_attempts=[codex_execution_attempt()],
                review_attempts=[shared_context],
            )

    def test_receipt_bundle_rejects_bodies_and_ready_claims(self) -> None:
        from med_autogrant.product_entry_parts.codex_stage_receipts import (
            build_codex_stage_execution_receipt_bundle,
        )

        attempt_with_body = codex_execution_attempt()
        attempt_with_body["proposal_text_body"] = "PRIVATE_BODY_TOKEN"
        with self.assertRaises(WorkspaceStateError):
            build_codex_stage_execution_receipt_bundle(
                stage_id="review_and_rebuttal",
                execution_attempts=[attempt_with_body],
                review_attempts=[codex_review_attempt()],
            )

        review_with_ready_claim = codex_review_attempt()
        review_with_ready_claim["claims_quality_ready"] = True
        with self.assertRaises(WorkspaceStateError):
            build_codex_stage_execution_receipt_bundle(
                stage_id="review_and_rebuttal",
                execution_attempts=[codex_execution_attempt()],
                review_attempts=[review_with_ready_claim],
            )
