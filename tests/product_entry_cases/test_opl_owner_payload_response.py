from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


def _production_acceptance() -> dict[str, object]:
    return {
        "surface_kind": "mag_production_acceptance_evidence.v1",
        "evidence_tail_status": "closed_by_domain_owned_acceptance_receipt",
        "closure_evidence": {
            "accepted_return_shape": "domain_owner_receipt_ref",
            "owner_receipt_ref": "receipt:mag/production-live-acceptance/2026-05-20",
        },
        "refs": {
            "grant_owner_receipt_refs": [
                "contracts/owner_receipt_contract.json",
                "receipt:mag/grant-stage-controlled-attempt/body-free-closeout/2026-05-20",
            ],
            "owner_receipt_refs": [
                "receipt:mag/production-live-acceptance/2026-05-20",
                "/product_entry_manifest/production_live_acceptance_receipt",
            ],
        },
    }


def _external_evidence_ledger() -> dict[str, object]:
    return {
        "surface_kind": "mag_external_evidence_receipt_ledger.v1",
        "state": "request_pack_closed_by_receipt_or_domain_owned_typed_blockers",
        "summary": {
            "closed_request_count": 7,
            "remaining_open_request_count": 0,
            "domain_owned_typed_blocker_count": 1,
            "claims_external_runtime_evidence_received": False,
            "claims_direct_hosted_parity_passed": False,
            "claims_temporal_provider_long_soak_complete": False,
            "claims_grant_or_fundability_ready": False,
        },
        "grant_stage_controlled_attempt_closeout": {
            "stage_closeout_refs": [
                {
                    "stage_id": "specific_aims_and_structure",
                    "owner_receipt_or_typed_blocker_ref": (
                        "receipt:mag/grant-stage-controlled-attempt/"
                        "specific_aims_and_structure/owner-receipt-or-typed-blocker"
                    ),
                    "monitor_freshness_refs": [
                        "contracts/stage_control_plane.json#/stages/2/stage_contract/monitor_freshness_refs/0"
                    ],
                }
            ],
            "submission_ready_export_gate_tail": {
                "state": "blocked_by_domain_owned_human_gate_typed_blocker",
                "typed_blocker_ref": (
                    "typed-blocker:mag/package_and_submit_ready/"
                    "submission_ready_export_gate/human-approval-required/2026-05-22"
                ),
                "readiness_claims": {
                    "claims_submission_ready_export": False,
                    "claims_human_approval_obtained": False,
                },
            },
        },
    }


def _receipt_readiness() -> dict[str, object]:
    return {
        "surface_kind": "mag_receipt_readiness_projection",
        "state": "receipt_refs_ready_not_quality_ready",
        "missing_categories": [],
        "summary": {
            "covered_category_count": 4,
            "missing_category_count": 0,
            "total_receipt_ref_count": 3,
        },
        "receipt_refs": {
            "owner_receipt": ["runtime://mag/receipts/owner/package-closeout.json"],
            "memory_accept_reject": ["runtime://mag/receipts/memory/accepted-risk.json"],
            "package_export_lifecycle": ["runtime://mag/receipts/package/lifecycle.json"],
            "cleanup_restore_retention_lifecycle": [
                "runtime://mag/receipts/lifecycle/cleanup.json"
            ],
        },
    }


class ProductEntryOplOwnerPayloadResponseTest(unittest.TestCase):
    def test_owner_payload_response_exposes_success_refs_and_human_gate_blocker_path(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        response = MedAutoGrantProductEntry().build_opl_owner_payload_response(
            production_acceptance=_production_acceptance(),
            external_evidence_receipt_ledger=_external_evidence_ledger(),
            receipt_readiness_projection=_receipt_readiness(),
        )

        self.assertEqual(response["surface_kind"], "mag_opl_owner_payload_response")
        self.assertEqual(response["status"], "blocked_by_submission_ready_human_gate")
        self.assertEqual(
            response["required_return_shapes"],
            [
                "domain_owner_receipt_ref",
                "no_regression_evidence_ref",
                "owner_chain_ref",
                "typed_blocker_ref",
            ],
        )
        self.assertEqual(
            response["payload_path_policy"],
            "operator_must_choose_success_refs_path_or_domain_owned_typed_blocker_path_empty_template_blocks",
        )
        self.assertEqual(
            response["domain_owner_receipt_refs"],
            [
                "receipt:mag/production-live-acceptance/2026-05-20",
                "receipt:mag/grant-stage-controlled-attempt/body-free-closeout/2026-05-20",
                "receipt:mag/grant-stage-controlled-attempt/"
                "specific_aims_and_structure/owner-receipt-or-typed-blocker",
                "runtime://mag/receipts/owner/package-closeout.json",
            ],
        )
        self.assertNotIn("contracts/owner_receipt_contract.json", response["domain_owner_receipt_refs"])
        self.assertNotIn(
            "/product_entry_manifest/production_live_acceptance_receipt",
            response["domain_owner_receipt_refs"],
        )
        self.assertIn("contracts/owner_receipt_contract.json", response["owner_chain_refs"])
        self.assertEqual(
            response["typed_blocker_refs"],
            [
                "typed-blocker:mag/package_and_submit_ready/"
                "submission_ready_export_gate/human-approval-required/2026-05-22"
            ],
        )
        self.assertIn(
            "runtime://mag/receipts/package/lifecycle.json",
            response["owner_chain_refs"],
        )
        self.assertEqual(response["domain_receipt_refs"], response["domain_owner_receipt_refs"])
        self.assertEqual(response["no_regression_refs"], response["no_regression_evidence_refs"])
        self.assertEqual(
            response["opl_runtime_action_execute_payload"]["typed_blocker_refs"],
            response["typed_blocker_refs"],
        )
        self.assertFalse(response["accepted_payload_paths"]["typed_blocker_path"]["success_claimed"])
        self.assertFalse(response["authority_boundary"]["can_declare_submission_ready"])
        self.assertFalse(response["authority_boundary"]["typed_blocker_is_submission_ready"])

    def test_owner_payload_response_rejects_private_body_or_ready_claim(self) -> None:
        from med_autogrant.product_entry_parts.opl_owner_payload_response import (
            build_opl_owner_payload_response,
        )

        production_acceptance = _production_acceptance()
        production_acceptance["grant_artifact_body"] = "PRIVATE_BODY_TOKEN"
        with self.assertRaises(WorkspaceStateError):
            build_opl_owner_payload_response(
                production_acceptance=production_acceptance,
                external_evidence_receipt_ledger=_external_evidence_ledger(),
                receipt_readiness_projection=_receipt_readiness(),
            )

        ledger = _external_evidence_ledger()
        ledger["grant_stage_controlled_attempt_closeout"]["submission_ready_export_gate_tail"][
            "readiness_claims"
        ]["claims_submission_ready_export"] = True
        with self.assertRaises(WorkspaceStateError):
            build_opl_owner_payload_response(
                production_acceptance=_production_acceptance(),
                external_evidence_receipt_ledger=ledger,
                receipt_readiness_projection=_receipt_readiness(),
            )
