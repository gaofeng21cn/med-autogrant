from __future__ import annotations

import tempfile

import json
import unittest
from pathlib import Path

from med_autogrant.product_entry_parts.domain_memory_runtime import (
    DOMAIN_MEMORY_RUNTIME_RECEIPT_EVIDENCE_KIND,
    build_domain_memory_writeback_decision,
    build_domain_memory_writeback_proposal,
    write_domain_memory_receipt_evidence,
)
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductEntryDomainMemoryReceiptEvidenceTest(unittest.TestCase):
    def _write_proposal(self, proposal_payload: dict[str, object]) -> Path:
        proposal_path = Path(tempfile.mkdtemp()) / "proposal.json"
        proposal_path.write_text(json.dumps(proposal_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return proposal_path

    def test_writes_accepted_runtime_receipt_instance_without_memory_body(self) -> None:
        proposal_payload = build_domain_memory_writeback_proposal(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            stage_id="review_and_rebuttal",
            source_ref="runtime-closeout://grant-run/example",
            lesson_summary="Keep reusable reviewer risk framing as strategy memory.",
            proposal_id="review-risk-framing",
        )
        decision_payload = build_domain_memory_writeback_decision(
            proposal_path=self._write_proposal(proposal_payload),
            decision="accepted",
            decision_reason="Reusable reviewer risk framing.",
            memory_id="review-risk-framing",
        )

        with tempfile.TemporaryDirectory() as runtime_root:
            evidence = write_domain_memory_receipt_evidence(
                decision_payload=decision_payload,
                runtime_root=runtime_root,
            )

            receipt = evidence["domain_memory_receipt_evidence"]
            receipt_path = Path(receipt["receipt_instance_ref"])
            self.assertTrue(receipt_path.exists())
            self.assertEqual(receipt["surface_kind"], DOMAIN_MEMORY_RUNTIME_RECEIPT_EVIDENCE_KIND)
            self.assertEqual(receipt["state"], "runtime_receipt_instance_written")
            self.assertEqual(receipt["decision"], "accepted")
            self.assertEqual(receipt["owner"], "med-autogrant")
            self.assertFalse(receipt["repo_tracked"])
            self.assertFalse(receipt["contains_memory_body"])
            self.assertFalse(receipt["contains_grant_artifact_content"])
            self.assertFalse(receipt["contains_quality_or_export_verdict"])
            self.assertIsNotNone(receipt["accepted_memory_ref"])
            self.assertIsNone(receipt["rejected_memory_ref"])

            receipt_instance = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt_instance, receipt)
            self.assertNotIn("lesson_summary", receipt_instance)

    def test_writes_rejected_runtime_receipt_instance_without_memory_body(self) -> None:
        proposal_payload = build_domain_memory_writeback_proposal(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            stage_id="review_and_rebuttal",
            source_ref="runtime-closeout://grant-run/example",
            lesson_summary="Do not store this text in the receipt evidence.",
            proposal_id="reject-review-risk-framing",
        )
        decision_payload = build_domain_memory_writeback_decision(
            proposal_path=self._write_proposal(proposal_payload),
            decision="rejected",
            decision_reason="Not broadly reusable enough.",
        )

        with tempfile.TemporaryDirectory() as runtime_root:
            evidence = write_domain_memory_receipt_evidence(
                decision_payload=decision_payload,
                runtime_root=runtime_root,
            )

            receipt = evidence["domain_memory_receipt_evidence"]
            receipt_path = Path(receipt["receipt_instance_ref"])
            self.assertTrue(receipt_path.exists())
            self.assertEqual(receipt["decision"], "rejected")
            self.assertIsNone(receipt["accepted_memory_ref"])
            self.assertIsNotNone(receipt["rejected_memory_ref"])
            self.assertFalse(receipt["contains_memory_body"])
            self.assertNotIn("lesson_summary", json.loads(receipt_path.read_text(encoding="utf-8")))
