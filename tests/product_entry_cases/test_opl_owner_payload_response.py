from __future__ import annotations

import unittest
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import (
    assert_false_keys,
    assert_path_values,
    production_acceptance_evidence,
    receipt_readiness_projection,
)


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
                    "expected_receipt_ref": (
                        "contracts/stage_control_plane.json#/stages/2/"
                        "stage_contract/expected_receipt_refs/0"
                    ),
                    "owner_receipt_or_typed_blocker_ref": (
                        "receipt:mag/grant-stage-controlled-attempt/"
                        "specific_aims_and_structure/owner-receipt-or-typed-blocker"
                    ),
                    "monitor_freshness_refs": [
                        "contracts/stage_control_plane.json#/stages/2/stage_contract/monitor_freshness_refs/0"
                    ],
                }
            ],
            "opl_stage_source_runtime_evidence_typed_blocker_handoff": {
                "stage_typed_blocker_refs": [
                    {
                        "stage_id": "specific_aims_and_structure",
                        "typed_blocker_ref": (
                            "typed-blocker:mag/stage-source-runtime-live-evidence/"
                            "specific_aims_and_structure/pending"
                        ),
                        "blocked_runtime_event_refs": [
                            "runtime_event:specific_aims_and_structure.ai_decision_gate_recorded"
                        ],
                    }
                ]
            },
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


class ProductEntryOplOwnerPayloadResponseTest(unittest.TestCase):
    def test_owner_payload_response_exposes_success_refs_and_human_gate_blocker_path(self) -> None:
        from med_autogrant.product_entry_parts.opl_owner_payload_response import (
            build_opl_owner_payload_response,
        )

        response = build_opl_owner_payload_response(
            production_acceptance=production_acceptance_evidence(include_owner_refs=True),
            external_evidence_receipt_ledger=_external_evidence_ledger(),
            receipt_readiness_projection=receipt_readiness_projection(include_receipt_refs=True),
        )

        assert_path_values(
            self,
            response,
            {
                "surface_kind": "mag_opl_owner_payload_response",
                "status": "blocked_by_submission_ready_human_gate",
                "payload_path_policy": (
                    "operator_must_choose_success_refs_path_or_domain_owned_typed_blocker_path_empty_template_blocks"
                ),
                "stage_expected_receipt_payload_summary.surface_kind": "mag_stage_expected_receipt_payload_summary",
                "stage_expected_receipt_payload_summary.stage_count": 1,
                "stage_expected_receipt_payload_summary.stage_ids": ["specific_aims_and_structure"],
                ("stage_expected_receipt_payload_summary", "stages", 0, "stage_id"): "specific_aims_and_structure",
                "opl_runtime_action_execute_payload.typed_blocker_refs": [_submission_gate_blocker_ref()],
            },
        )
        self.assertIn("domain_owner_receipt_ref", response["required_return_shapes"])
        self.assertIn("typed_blocker_ref", response["required_return_shapes"])
        self.assertIn("receipt:mag/production-live-acceptance/2026-05-20", response["domain_owner_receipt_refs"])
        self.assertIn("runtime://mag/receipts/owner/package-closeout.json", response["domain_owner_receipt_refs"])
        self.assertNotIn("contracts/owner_receipt_contract.json", response["domain_owner_receipt_refs"])
        self.assertNotIn(
            "/product_entry_manifest/production_live_acceptance_receipt",
            response["domain_owner_receipt_refs"],
        )
        self.assertIn("contracts/owner_receipt_contract.json", response["owner_chain_refs"])
        self.assertEqual(response["typed_blocker_refs"], [_submission_gate_blocker_ref()])
        self.assertNotIn("domain_receipt_refs", response)
        self.assertNotIn("no_regression_refs", response)
        self.assertNotIn("legacy_payload_field_aliases", response)
        self.assertNotIn("stage_expected_receipt_payload_summary", response["record_payload"])
        self.assertNotIn(
            "stage_expected_receipt_payload_summary",
            response["opl_runtime_action_execute_payload"],
        )
        stage_summary = response["stage_expected_receipt_payload_summary"]
        assert_false_keys(
            self,
            stage_summary,
            (
                "payload_body_allowed",
                "empty_payload_template_is_success_evidence",
                "operator_payload_submitted",
                "success_refs_visible_is_completion",
                "grant_ready_claimed",
                "quality_ready_claimed",
                "export_ready_claimed",
                "submission_ready_claimed",
            ),
        )
        assert_false_keys(
            self,
            stage_summary["authority_boundary"],
            ("can_declare_submission_ready", "typed_blocker_is_submission_ready"),
        )
        stage_payload = stage_summary["stages"][0]
        self.assertIn(
            "runtime_event:specific_aims_and_structure.ai_decision_gate_recorded",
            stage_payload["success_refs_path_payload"]["runtime_event_refs"],
        )
        self.assertTrue(stage_payload["typed_blocker_path_payload"]["typed_blocker_refs"])
        assert_false_keys(self, stage_payload, ("success_refs_visible_is_completion", "grant_ready_claimed"))
        self.assertFalse(stage_payload["authority_boundary"]["can_create_owner_receipt"])
        assert_false_keys(
            self,
            response["authority_boundary"],
            ("can_declare_submission_ready", "typed_blocker_is_submission_ready"),
        )

    def test_owner_payload_response_rejects_private_body_or_ready_claim(self) -> None:
        from med_autogrant.product_entry_parts.opl_owner_payload_response import (
            build_opl_owner_payload_response,
        )

        production_acceptance = production_acceptance_evidence(include_owner_refs=True)
        production_acceptance["grant_artifact_body"] = "PRIVATE_BODY_TOKEN"
        with self.assertRaises(WorkspaceStateError):
            build_opl_owner_payload_response(
                production_acceptance=production_acceptance,
                external_evidence_receipt_ledger=_external_evidence_ledger(),
                receipt_readiness_projection=receipt_readiness_projection(include_receipt_refs=True),
            )

        ledger = _external_evidence_ledger()
        ledger["grant_stage_controlled_attempt_closeout"]["submission_ready_export_gate_tail"][
            "readiness_claims"
        ]["claims_submission_ready_export"] = True
        with self.assertRaises(WorkspaceStateError):
            build_opl_owner_payload_response(
                production_acceptance=production_acceptance_evidence(include_owner_refs=True),
                external_evidence_receipt_ledger=ledger,
                receipt_readiness_projection=receipt_readiness_projection(include_receipt_refs=True),
            )


def _submission_gate_blocker_ref() -> str:
    return (
        "typed-blocker:mag/package_and_submit_ready/"
        "submission_ready_export_gate/human-approval-required/2026-05-22"
    )
