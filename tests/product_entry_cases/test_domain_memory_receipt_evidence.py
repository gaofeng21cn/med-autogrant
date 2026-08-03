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
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


CRITIQUE_EXAMPLE_PATH = (
    Path(__file__).resolve().parents[2] / "examples" / "nsfc_workspace_p2c_critique.json"
)


class ProductEntryDomainMemoryReceiptEvidenceTest(unittest.TestCase):
    def _write_proposal(self, proposal_payload: dict[str, object]) -> Path:
        proposal_path = Path(tempfile.mkdtemp()) / "proposal.json"
        proposal_path.write_text(json.dumps(proposal_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return proposal_path

    def test_preserves_proposal_json_loader_errors(self) -> None:
        cases = (
            ("{", WorkspaceStateError, "domain_memory_writeback_proposal 不是合法 JSON"),
            ("[]", WorkspaceStateError, "domain_memory_writeback_proposal 必须是 JSON object"),
            (None, WorkspaceFileError, "读取 domain_memory_writeback_proposal 失败"),
        )

        for contents, error_type, message in cases:
            with self.subTest(contents=contents):
                proposal_path = Path(tempfile.mkdtemp()) / "proposal.json"
                if contents is not None:
                    proposal_path.write_text(contents, encoding="utf-8")

                with self.assertRaises(error_type) as raised:
                    build_domain_memory_writeback_decision(
                        proposal_path=proposal_path,
                        decision="accepted",
                        decision_reason="Characterization only.",
                    )

                self.assertIs(type(raised.exception), error_type)
                self.assertEqual(str(raised.exception), f"{message}: {proposal_path.resolve()}")

    def test_preserves_decision_json_loader_errors(self) -> None:
        cases = (
            ("{", WorkspaceStateError, "domain_memory_writeback_decision 不是合法 JSON"),
            ("[]", WorkspaceStateError, "domain_memory_writeback_decision 必须是 JSON object"),
            (None, WorkspaceFileError, "读取 domain_memory_writeback_decision 失败"),
        )

        for contents, error_type, message in cases:
            with self.subTest(contents=contents):
                decision_path = Path(tempfile.mkdtemp()) / "decision.json"
                if contents is not None:
                    decision_path.write_text(contents, encoding="utf-8")

                with self.assertRaises(error_type) as raised:
                    write_domain_memory_receipt_evidence(decision_payload=decision_path)

                self.assertIs(type(raised.exception), error_type)
                self.assertEqual(str(raised.exception), f"{message}: {decision_path.resolve()}")

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
