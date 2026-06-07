from __future__ import annotations

import json
import unittest

from med_autogrant.workspace import WorkspaceStateError


class ProductEntryConflictEnvelopeTest(unittest.TestCase):
    def test_receipt_conflict_envelope_projects_owner_receipt_refs_only(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.conflict_envelopes import (
            build_opl_conflict_or_blocker_envelope,
        )

        envelope = build_opl_conflict_or_blocker_envelope(
            classification="receipt_conflict",
            severity="blocking",
            owner_receipt={
                "receipt_instance_ref": "runtime://mag/receipts/owner/attempt-1.json",
                "receipt_id": "mag.owner_receipt.attempt-1",
                "receipt_shape": "typed_blocker",
                "source_ref": "opl-ledger://stage-attempt/attempt-1",
                "closeout_summary": "MAG owner receipt ref exists; OPL displays it read-only.",
            },
            source_refs=["/product_entry_manifest/owner_receipt_contract"],
            verdict_refs={"quality_verdict_ref": "mag-verdict://quality/review-1"},
            safe_action_refs={"operator_action_ref": "mag-action://repair/request-human-review"},
        )
        method_envelope = MedAutoGrantProductEntry().build_opl_conflict_or_blocker_envelope(
            classification="receipt_conflict",
            severity="blocking",
            owner_receipt={
                "receipt_instance_ref": "runtime://mag/receipts/owner/attempt-1.json",
                "receipt_id": "mag.owner_receipt.attempt-1",
                "receipt_shape": "typed_blocker",
                "source_ref": "opl-ledger://stage-attempt/attempt-1",
                "closeout_summary": "MAG owner receipt ref exists; OPL displays it read-only.",
            },
            source_refs=["/product_entry_manifest/owner_receipt_contract"],
            verdict_refs={"quality_verdict_ref": "mag-verdict://quality/review-1"},
            safe_action_refs={"operator_action_ref": "mag-action://repair/request-human-review"},
        )

        self.assertEqual(envelope["surface_kind"], "mag_opl_conflict_or_blocker_envelope")
        self.assertEqual(method_envelope, envelope)
        self.assertEqual(envelope["envelope_kind"], "opl_conflict_or_blocker.v1")
        self.assertEqual(envelope["owner"], "med-autogrant")
        self.assertEqual(envelope["target_domain_id"], "med-autogrant")
        self.assertEqual(envelope["classification"], "receipt_conflict")
        self.assertEqual(envelope["severity"], "blocking")
        self.assertEqual(
            envelope["receipt_refs"]["owner_receipt_ref"],
            "runtime://mag/receipts/owner/attempt-1.json",
        )
        self.assertEqual(envelope["receipt_refs"]["receipt_shape"], "typed_blocker")
        self.assertIn("/product_entry_manifest/owner_receipt_contract", envelope["source_refs"])
        self.assertIn("opl-ledger://stage-attempt/attempt-1", envelope["source_refs"])
        self.assertEqual(
            envelope["verdict_refs"],
            {"quality_verdict_ref": "mag-verdict://quality/review-1"},
        )
        self.assertEqual(
            envelope["safe_action_refs"],
            {"operator_action_ref": "mag-action://repair/request-human-review"},
        )
        boundary = envelope["authority_boundary"]
        self.assertTrue(boundary["mag_owns_domain_truth"])
        self.assertTrue(boundary["mag_owns_verdicts"])
        self.assertTrue(boundary["mag_owns_owner_receipt"])
        self.assertTrue(boundary["opl_ref_consumer_only"])
        self.assertFalse(boundary["provider_completion_is_domain_ready"])
        self.assertFalse(boundary["fallback_complete"])
        self.assertFalse(boundary["export_ready"])
        self.assertFalse(boundary["grant_ready"])
        self.assertIn("fallback_complete", envelope["forbidden_claims"])

    def test_quality_blocker_envelope_accepts_mapping_payload(self) -> None:
        from med_autogrant.product_entry_parts.conflict_envelopes import (
            build_opl_conflict_or_blocker_envelope,
        )

        envelope = build_opl_conflict_or_blocker_envelope(
            {
                "classification": "quality_blocker",
                "severity": "critical",
                "typed_blocker": {
                    "blocker_ref": "mag-blocker://quality/ai-review-required",
                    "blocker_kind": "quality_review_required",
                    "source_ref": "/product_entry_manifest/grant_authoring_readiness",
                    "details": "Display may mention the blocker, but not a grant artifact body.",
                },
                "no_regression_evidence": {
                    "evidence_refs": ["runtime://mag/evidence/no-regression/attempt-9.json"],
                },
                "verdict_refs": {
                    "fundability_verdict_ref": "mag-verdict://fundability/current",
                    "quality_verdict_ref": "mag-verdict://quality/current",
                },
                "safe_action_refs": {
                    "repair_action_ref": "mag-action://quality/request-ai-review",
                },
            }
        )

        self.assertEqual(envelope["classification"], "quality_blocker")
        self.assertEqual(envelope["severity"], "critical")
        self.assertEqual(
            envelope["typed_blocker_refs"],
            {
                "blocker_ref": "mag-blocker://quality/ai-review-required",
                "blocker_kind": "quality_review_required",
                "source_ref": "/product_entry_manifest/grant_authoring_readiness",
            },
        )
        self.assertEqual(
            envelope["no_regression_evidence_refs"],
            {"evidence_refs": ["runtime://mag/evidence/no-regression/attempt-9.json"]},
        )
        self.assertFalse(envelope["authority_boundary"]["provider_completion_is_domain_ready"])
        self.assertFalse(envelope["authority_boundary"]["grant_ready"])
        self.assertFalse(envelope["authority_boundary"]["export_ready"])

    def test_invalid_classification_fails_closed(self) -> None:
        from med_autogrant.product_entry_parts.conflict_envelopes import (
            build_opl_conflict_or_blocker_envelope,
        )

        with self.assertRaises(WorkspaceStateError):
            build_opl_conflict_or_blocker_envelope(
                classification="provider_complete",
                severity="blocking",
                source_refs=["/product_entry_manifest/owner_receipt_contract"],
            )

    def test_envelope_does_not_include_grant_artifact_or_memory_body(self) -> None:
        from med_autogrant.product_entry_parts.conflict_envelopes import (
            build_opl_conflict_or_blocker_envelope,
        )

        envelope = build_opl_conflict_or_blocker_envelope(
            {
                "classification": "human_gate",
                "severity": "blocking",
                "owner_receipt": {
                    "receipt_instance_ref": "runtime://mag/receipts/human-gate.json",
                    "receipt_id": "mag.owner_receipt.human-gate",
                    "receipt_shape": "typed_blocker",
                    "source_ref": "opl-ledger://human-gate/1",
                    "memory_body": "private grant strategy body",
                    "grant_artifact": "full application content",
                },
                "typed_blocker": {
                    "blocker_ref": "mag-blocker://human-gate/manual-portal",
                    "blocker_kind": "manual_portal_required",
                    "source_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
                    "memory_body": "do not project this",
                    "grant_artifact": {"title": "do not project this either"},
                },
                "safe_action_refs": {"manual_gate_ref": "mag-action://portal/open-human-gate"},
            }
        )

        encoded = json.dumps(envelope, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("private grant strategy body", encoded)
        self.assertNotIn("full application content", encoded)
        self.assertNotIn("do not project this", encoded)
        for projection in (
            envelope["receipt_refs"],
            envelope["typed_blocker_refs"],
            envelope["verdict_refs"],
            envelope["safe_action_refs"],
        ):
            self.assertNotIn("memory_body", projection)
            self.assertNotIn("grant_artifact", projection)
