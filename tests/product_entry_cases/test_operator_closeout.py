from __future__ import annotations

import unittest
from med_autogrant.workspace import WorkspaceStateError


def _production_acceptance() -> dict[str, object]:
    return {
        "surface_kind": "mag_production_acceptance_evidence.v1",
        "evidence_tail_status": "closed_by_domain_owned_acceptance_receipt",
        "closure_evidence": {
            "accepted_return_shape": "domain_owner_receipt_ref",
            "owner_receipt_ref": "receipt:mag/production-live-acceptance/2026-05-20",
        },
    }


def _external_evidence_ledger() -> dict[str, object]:
    return {
        "surface_kind": "mag_external_evidence_receipt_ledger.v1",
        "state": "request_pack_closed_by_receipt_or_domain_owned_typed_blockers",
        "summary": {
            "closed_request_count": 7,
            "remaining_open_request_count": 0,
            "domain_owned_typed_blocker_count": 6,
            "claims_external_runtime_evidence_received": False,
            "claims_direct_hosted_parity_passed": False,
            "claims_temporal_provider_long_soak_complete": False,
            "claims_grant_or_fundability_ready": False,
        },
        "remaining_real_evidence_gap_ids": [
            "external_opl_generated_or_hosted_caller_consumption_receipt",
            "codex_app_workbench_package_ref_consumption_receipt",
        ],
    }


def _receipt_readiness(*, missing: list[str] | None = None) -> dict[str, object]:
    missing_categories = missing if missing is not None else []
    return {
        "surface_kind": "mag_receipt_readiness_projection",
        "state": (
            "receipt_refs_ready_not_quality_ready"
            if not missing_categories
            else "partial_receipt_coverage"
        ),
        "missing_categories": missing_categories,
        "summary": {
            "covered_category_count": 4 - len(missing_categories),
            "missing_category_count": len(missing_categories),
            "total_receipt_ref_count": 8,
        },
    }


class ProductEntryOperatorCloseoutTest(unittest.TestCase):
    def test_operator_closeout_distinguishes_accounting_from_real_evidence_gap(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        projection = MedAutoGrantProductEntry().build_operator_closeout_readiness_projection(
            production_acceptance=_production_acceptance(),
            external_evidence_receipt_ledger=_external_evidence_ledger(),
            receipt_readiness_projection=_receipt_readiness(),
        )

        self.assertEqual(projection["surface_kind"], "mag_operator_closeout_readiness_projection")
        self.assertEqual(projection["state"], "real_external_evidence_missing")
        self.assertTrue(projection["production_acceptance_tail"]["closed"])
        self.assertTrue(projection["external_evidence_accounting"]["request_accounting_closed"])
        self.assertFalse(projection["external_evidence_accounting"]["real_external_evidence_complete"])
        self.assertEqual(
            projection["external_evidence_accounting"]["remaining_real_evidence_gap_count"],
            2,
        )
        self.assertEqual(
            projection["operator_attention"][0]["attention_id"],
            "real_external_evidence_missing",
        )
        self.assertFalse(
            projection["authority_boundary"]["request_accounting_closure_equals_real_evidence"]
        )
        self.assertFalse(projection["authority_boundary"]["receipt_refs_ready_equals_quality_ready"])
        self.assertFalse(projection["authority_boundary"]["production_tail_closure_equals_grant_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_submission_ready"])

    def test_operator_closeout_projects_receipt_coverage_gap_after_real_evidence_arrives(self) -> None:
        from med_autogrant.product_entry_parts.operator_closeout import (
            build_operator_closeout_readiness_projection,
        )

        ledger = _external_evidence_ledger()
        ledger["remaining_real_evidence_gap_ids"] = []
        projection = build_operator_closeout_readiness_projection(
            production_acceptance=_production_acceptance(),
            external_evidence_receipt_ledger=ledger,
            receipt_readiness_projection=_receipt_readiness(missing=["package_export_lifecycle"]),
        )

        self.assertEqual(projection["state"], "receipt_coverage_incomplete")
        self.assertEqual(
            projection["operator_attention"][0],
            {
                "attention_id": "receipt_coverage_incomplete",
                "state": "workspace_receipt_refs_required",
                "owner": "med-autogrant",
                "missing_categories": ["package_export_lifecycle"],
            },
        )
        self.assertFalse(projection["receipt_readiness"]["quality_ready"])
        self.assertFalse(projection["receipt_readiness"]["submission_ready"])

    def test_operator_closeout_all_refs_ready_still_not_quality_ready(self) -> None:
        from med_autogrant.product_entry_parts.operator_closeout import (
            build_operator_closeout_readiness_projection,
        )

        ledger = _external_evidence_ledger()
        ledger["remaining_real_evidence_gap_ids"] = []
        projection = build_operator_closeout_readiness_projection(
            production_acceptance=_production_acceptance(),
            external_evidence_receipt_ledger=ledger,
            receipt_readiness_projection=_receipt_readiness(),
        )

        self.assertEqual(projection["state"], "operator_closeout_refs_ready_not_quality_ready")
        self.assertEqual(
            projection["operator_attention"][0]["attention_id"],
            "quality_verdict_still_domain_owned",
        )
        self.assertFalse(projection["authority_boundary"]["can_declare_fundability_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_quality_ready"])

    def test_operator_closeout_rejects_ready_claim_or_private_body(self) -> None:
        from med_autogrant.product_entry_parts.operator_closeout import (
            build_operator_closeout_readiness_projection,
        )

        ledger = _external_evidence_ledger()
        ledger["summary"]["claims_grant_or_fundability_ready"] = True
        with self.assertRaises(WorkspaceStateError):
            build_operator_closeout_readiness_projection(
                production_acceptance=_production_acceptance(),
                external_evidence_receipt_ledger=ledger,
                receipt_readiness_projection=_receipt_readiness(),
            )

        production_acceptance = _production_acceptance()
        production_acceptance["grant_artifact_body"] = "PRIVATE_BODY_TOKEN"
        with self.assertRaises(WorkspaceStateError):
            build_operator_closeout_readiness_projection(
                production_acceptance=production_acceptance,
                external_evidence_receipt_ledger=_external_evidence_ledger(),
                receipt_readiness_projection=_receipt_readiness(),
            )

