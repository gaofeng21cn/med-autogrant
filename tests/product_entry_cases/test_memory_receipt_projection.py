from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryMemoryReceiptProjectionTest(unittest.TestCase):
    def test_aggregates_accepted_and_rejected_receipts_refs_only(self) -> None:
        from med_autogrant.product_entry_parts.memory_receipt_projection import (
            build_memory_receipt_read_projection,
        )

        accepted_receipt = {
            "surface_kind": "mag_domain_memory_runtime_receipt_evidence",
            "receipt_id": "mag.domain_memory.receipt.accepted-review-risk",
            "receipt_ref": "runtime://receipts/domain-memory/accepted-review-risk.json",
            "receipt_instance_ref": "/runtime/receipts/domain-memory/accepted-review-risk.json",
            "proposal_id": "accepted-review-risk",
            "proposal_ref": "runtime://domain-memory/writeback-proposals/accepted-review-risk.json",
            "decision": "accepted",
            "decision_owner": "med-autogrant",
            "stage_id": "review_and_rebuttal",
            "accepted_memory_ref": "runtime://domain-memory/accepted/accepted-review-risk.json",
            "rejected_memory_ref": None,
            "decision_reason": "SECRET_BODY_TOKEN should never be projected.",
            "contains_memory_body": False,
            "contains_grant_artifact_content": False,
            "contains_quality_or_export_verdict": False,
        }
        rejected_receipt = {
            "surface_kind": "mag_domain_memory_runtime_receipt_evidence",
            "receipt_id": "mag.domain_memory.receipt.rejected-review-risk",
            "receipt_ref": "runtime://receipts/domain-memory/rejected-review-risk.json",
            "receipt_instance_ref": "/runtime/receipts/domain-memory/rejected-review-risk.json",
            "proposal_id": "rejected-review-risk",
            "proposal_ref": "runtime://domain-memory/writeback-proposals/rejected-review-risk.json",
            "decision": "rejected",
            "decision_owner": "med-autogrant",
            "stage_id": "review_and_rebuttal",
            "accepted_memory_ref": None,
            "rejected_memory_ref": "runtime://domain-memory/rejected/rejected-review-risk.json",
            "contains_memory_body": False,
            "contains_grant_artifact_content": False,
            "contains_quality_or_export_verdict": False,
        }

        projection = build_memory_receipt_read_projection(
            [
                {"domain_memory_receipt_evidence": accepted_receipt},
                rejected_receipt,
            ]
        )

        self.assertEqual(projection["surface_kind"], "mag_memory_receipt_read_projection")
        self.assertEqual(
            projection["state"],
            "body_free_receipt_refs_ready_for_opl_consumption",
        )
        self.assertEqual(projection["accepted_count"], 1)
        self.assertEqual(projection["rejected_count"], 1)
        self.assertEqual(
            projection["receipt_refs"],
            [
                {
                    "decision": "accepted",
                    "proposal_id": "accepted-review-risk",
                    "receipt_id": "mag.domain_memory.receipt.accepted-review-risk",
                    "receipt_ref": "runtime://receipts/domain-memory/accepted-review-risk.json",
                    "receipt_instance_ref": "/runtime/receipts/domain-memory/accepted-review-risk.json",
                },
                {
                    "decision": "rejected",
                    "proposal_id": "rejected-review-risk",
                    "receipt_id": "mag.domain_memory.receipt.rejected-review-risk",
                    "receipt_ref": "runtime://receipts/domain-memory/rejected-review-risk.json",
                    "receipt_instance_ref": "/runtime/receipts/domain-memory/rejected-review-risk.json",
                },
            ],
        )
        self.assertEqual(
            projection["proposal_refs"],
            [
                {
                    "decision": "accepted",
                    "proposal_id": "accepted-review-risk",
                    "proposal_ref": "runtime://domain-memory/writeback-proposals/accepted-review-risk.json",
                },
                {
                    "decision": "rejected",
                    "proposal_id": "rejected-review-risk",
                    "proposal_ref": "runtime://domain-memory/writeback-proposals/rejected-review-risk.json",
                },
            ],
        )
        self.assertEqual(
            projection["memory_refs"],
            [
                {
                    "decision": "accepted",
                    "proposal_id": "accepted-review-risk",
                    "memory_ref_kind": "accepted_memory_ref",
                    "memory_ref": "runtime://domain-memory/accepted/accepted-review-risk.json",
                },
                {
                    "decision": "rejected",
                    "proposal_id": "rejected-review-risk",
                    "memory_ref_kind": "rejected_memory_ref",
                    "memory_ref": "runtime://domain-memory/rejected/rejected-review-risk.json",
                },
            ],
        )
        self.assertTrue(projection["authority_boundary"]["mag_owns_memory_body"])
        self.assertTrue(projection["authority_boundary"]["mag_owns_accept_reject"])
        self.assertTrue(projection["authority_boundary"]["opl_consumes_refs_only"])
        self.assertFalse(projection["authority_boundary"]["opl_can_hold_memory_body"])

        encoded = json.dumps(projection, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("SECRET_BODY_TOKEN", encoded)
        self.assertNotIn("decision_reason", encoded)

    def test_forbidden_body_or_ready_verdict_claim_fails_closed(self) -> None:
        from med_autogrant.product_entry_parts.memory_receipt_projection import (
            build_memory_receipt_read_projection,
        )

        base_receipt = {
            "surface_kind": "mag_domain_memory_runtime_receipt_evidence",
            "receipt_id": "mag.domain_memory.receipt.review-risk",
            "receipt_ref": "runtime://receipts/domain-memory/review-risk.json",
            "proposal_id": "review-risk",
            "decision": "accepted",
            "decision_owner": "med-autogrant",
            "accepted_memory_ref": "runtime://domain-memory/accepted/review-risk.json",
            "contains_memory_body": False,
            "contains_grant_artifact_content": False,
            "contains_quality_or_export_verdict": False,
        }
        forbidden_cases = [
            {"memory_body": "SECRET_BODY_TOKEN"},
            {"grant_artifact": {"body": "SECRET_ARTIFACT_TOKEN"}},
            {"fundability_ready": True},
            {"quality_verdict": "ready"},
            {"export_verdict": {"state": "ready"}},
        ]

        for forbidden in forbidden_cases:
            receipt = dict(base_receipt)
            receipt.update(forbidden)
            with self.subTest(forbidden=sorted(forbidden)):
                with self.assertRaises(WorkspaceStateError):
                    build_memory_receipt_read_projection([receipt])

