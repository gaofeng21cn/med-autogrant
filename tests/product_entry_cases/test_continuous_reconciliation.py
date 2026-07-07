from __future__ import annotations

import tempfile

from copy import deepcopy
import json
import unittest
from pathlib import Path
from med_autogrant.product_entry_parts.owner_receipt_reconciliation import (
    build_controlled_soak_receipt_reconciliation_inventory,
)
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductEntryContinuousReconciliationTest(unittest.TestCase):
    def test_continuous_reconciliation_snapshot_summarizes_mixed_verified_receipts(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.continuous_reconciliation import (
            build_continuous_receipt_reconciliation_snapshot,
        )
        from med_autogrant.product_entry_parts.hosted_receipt_verification import (
            build_focused_hosted_receipt_verification,
        )
        from med_autogrant.product_entry_parts.receipt_observability import (
            build_controlled_soak_receipt_observability_summary,
        )
        from med_autogrant.product_entry_parts.stage_attempt_observability import (
            build_stage_attempt_observability_projection,
        )

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            no_regression = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-ledger://mag/continuous-reconciliation",
                closeout_summary="MAG no-regression receipt for continuous reconciliation.",
                runtime_root=runtime_root,
                receipt_id="continuous-no-regression",
            )["owner_receipt_evidence"]
            typed_blocker = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="typed_blocker",
                stage_id="package_and_submit_ready",
                source_ref="opl-ledger://mag/continuous-reconciliation",
                closeout_summary="MAG typed blocker receipt for continuous reconciliation.",
                runtime_root=runtime_root,
                receipt_id="continuous-typed-blocker",
            )["owner_receipt_evidence"]
            domain_owner = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="domain_owner_receipt",
                stage_id="fundability_strategy",
                source_ref="opl-ledger://mag/continuous-reconciliation",
                closeout_summary="MAG domain-owner receipt for continuous reconciliation.",
                runtime_root=runtime_root,
                receipt_id="continuous-domain-owner",
            )["owner_receipt_evidence"]
            inventory_payload = build_controlled_soak_receipt_reconciliation_inventory(
                owner_receipt_evidence_items=[no_regression, typed_blocker, domain_owner],
                opl_ledger_ref="opl-ledger://mag/continuous-reconciliation",
                domain_handler_closeout_results=[{"receipt_ref": no_regression["receipt_instance_ref"]}],
            )
            no_regression_verification = build_focused_hosted_receipt_verification(
                owner_receipt_evidence=no_regression,
                opl_attempt_evidence={
                    "surface_kind": "opl_hosted_stage_attempt_evidence",
                    "attempt_ref": "opl-attempt://mag/continuous/no-regression",
                    "stage_id": "review_and_rebuttal",
                    "ledger_ref": "opl-ledger://mag/continuous-reconciliation",
                    "domain_breakdown": {
                        "target_domain_id": "med-autogrant",
                        "owner_receipt_ref": no_regression["receipt_instance_ref"],
                        "no_regression_evidence_refs": [no_regression["receipt_instance_ref"]],
                        "typed_blocker_refs": [],
                    },
                },
            )
            typed_blocker_verification = build_focused_hosted_receipt_verification(
                owner_receipt_evidence=typed_blocker,
                opl_attempt_evidence={
                    "surface_kind": "opl_hosted_stage_attempt_evidence",
                    "attempt_ref": "opl-attempt://mag/continuous/blocker",
                    "stage_id": "package_and_submit_ready",
                    "ledger_ref": "opl-ledger://mag/continuous-reconciliation",
                    "domain_breakdown": {
                        "target_domain_id": "med-autogrant",
                        "owner_receipt_ref": typed_blocker["receipt_instance_ref"],
                        "no_regression_evidence_refs": [],
                        "typed_blocker_refs": [typed_blocker["receipt_instance_ref"]],
                    },
                },
            )
            observability_summary = build_controlled_soak_receipt_observability_summary(
                inventory_payload
            )
            stage_attempt_projection = build_stage_attempt_observability_projection(
                controlled_stage_attempt_projection={
                    "surface_kind": "controlled_stage_attempt_projection",
                    "attempt_id": "mag-continuous-reconciliation",
                    "attempt_state": "receipts_returned",
                    "attempt_owner": "med-autogrant",
                    "maps_to_opl_contract": "opl_family_runtime_attempt_contract.v1",
                    "receipt_refs": {
                        "owner_receipt_ref": domain_owner["receipt_instance_ref"],
                        "typed_blocker_refs": [typed_blocker["receipt_instance_ref"]],
                        "no_regression_evidence_refs": [no_regression["receipt_instance_ref"]],
                    },
                },
                receipt_reconciliation_inventory=inventory_payload,
                opl_usage_projection_ref="opl-usage://mag/continuous-reconciliation",
                opl_control_loop_projection_ref="opl-control://mag/continuous-reconciliation",
            )

        snapshot = build_continuous_receipt_reconciliation_snapshot(
            focused_hosted_receipt_verification_items=[
                no_regression_verification,
                typed_blocker_verification,
            ],
            receipt_reconciliation_inventory=inventory_payload,
            receipt_observability_summary=observability_summary,
            stage_attempt_observability_projection=stage_attempt_projection,
        )

        self.assertEqual(
            snapshot["surface_kind"],
            "mag_continuous_receipt_reconciliation_snapshot",
        )
        self.assertEqual(snapshot["state"], "read_only_snapshot_not_live_soak_complete")
        self.assertEqual(snapshot["summary"]["verified_count"], 2)
        self.assertEqual(snapshot["summary"]["typed_blocker_count"], 1)
        self.assertEqual(snapshot["summary"]["no_regression_evidence_count"], 1)
        self.assertEqual(snapshot["summary"]["domain_owner_receipt_count"], 1)
        self.assertEqual(snapshot["summary"]["unmatched_count"], 1)
        self.assertEqual(
            snapshot["receipt_refs"]["verified_refs"],
            [
                no_regression["receipt_instance_ref"],
                typed_blocker["receipt_instance_ref"],
            ],
        )
        self.assertEqual(
            snapshot["receipt_refs"]["unmatched_refs"],
            [domain_owner["receipt_instance_ref"]],
        )
        self.assertEqual(
            snapshot["receipt_refs"]["all_inventory_refs"],
            [
                no_regression["receipt_instance_ref"],
                typed_blocker["receipt_instance_ref"],
                domain_owner["receipt_instance_ref"],
            ],
        )
        self.assertFalse(snapshot["authority_boundary"]["mag_writes_opl_ledger"])
        self.assertFalse(snapshot["authority_boundary"]["mag_implements_opl_provider"])
        self.assertFalse(snapshot["authority_boundary"]["mag_declares_live_soak_complete"])
        self.assertFalse(snapshot["claims"]["claims_production_long_run_soak_complete"])

    def test_continuous_reconciliation_rejects_provider_or_grant_ready_claims(self) -> None:
        from med_autogrant.product_entry_parts.continuous_reconciliation import (
            build_continuous_receipt_reconciliation_snapshot,
        )

        inventory = _minimal_inventory("receipt://ready-claim")
        verification = _minimal_verification(
            "receipt://ready-claim",
            result_shape="no_regression_evidence",
            provider_completion_ready=True,
        )

        with self.assertRaisesRegex(WorkspaceStateError, "ready|soak"):
            build_continuous_receipt_reconciliation_snapshot(
                focused_hosted_receipt_verification_items=[verification],
                receipt_reconciliation_inventory=inventory,
            )

        bad_inventory = deepcopy(inventory)
        bad_inventory["claims_grant_ready"] = True
        with self.assertRaisesRegex(WorkspaceStateError, "ready|soak"):
            build_continuous_receipt_reconciliation_snapshot(
                focused_hosted_receipt_verification_items=[
                    _minimal_verification(
                        "receipt://ready-claim",
                        result_shape="no_regression_evidence",
                    )
                ],
                receipt_reconciliation_inventory=bad_inventory,
            )

    def test_continuous_reconciliation_does_not_leak_body_or_artifact_content(self) -> None:
        from med_autogrant.product_entry_parts.continuous_reconciliation import (
            build_continuous_receipt_reconciliation_snapshot,
        )

        inventory = _minimal_inventory("receipt://no-leak")
        inventory["items"][0]["grant_artifact_body"] = "SECRET_GRANT_ARTIFACT_BODY"
        inventory["items"][0]["memory_body"] = "SECRET_MEMORY_BODY"
        inventory["items"][0]["closeout_summary"] = "SECRET_CLOSEOUT_SUMMARY"
        verification = _minimal_verification(
            "receipt://no-leak",
            result_shape="no_regression_evidence",
        )
        verification["grant_artifact_body"] = "SECRET_GRANT_ARTIFACT_BODY"
        verification["memory_body"] = "SECRET_MEMORY_BODY"
        verification["closeout_summary"] = "SECRET_CLOSEOUT_SUMMARY"

        snapshot = build_continuous_receipt_reconciliation_snapshot(
            focused_hosted_receipt_verification_items=[verification],
            receipt_reconciliation_inventory=inventory,
        )
        serialized = json.dumps(snapshot, ensure_ascii=False, sort_keys=True)

        self.assertNotIn("SECRET_GRANT_ARTIFACT_BODY", serialized)
        self.assertNotIn("SECRET_MEMORY_BODY", serialized)
        self.assertNotIn("SECRET_CLOSEOUT_SUMMARY", serialized)
        self.assertNotIn("grant_artifact_body", serialized)
        self.assertNotIn("memory_body", serialized)
        self.assertNotIn("closeout_summary", serialized)
        self.assertEqual(snapshot["receipt_refs"]["verified_refs"], ["receipt://no-leak"])


def _minimal_inventory(receipt_ref: str) -> dict[str, Any]:
    return {
        "surface_kind": "mag_controlled_soak_receipt_reconciliation_inventory",
        "version": "v1",
        "state": "read_projection_only_not_live_soak_complete",
        "target_domain_id": "med-autogrant",
        "owner": "med-autogrant",
        "opl_ledger": {
            "ledger_ref": "opl-ledger://mag/continuous/minimal",
            "role": "external_ref_for_inventory_reconciliation_only",
            "mag_writes_opl_ledger": False,
            "opl_holds_grant_truth": False,
        },
        "summary": {
            "item_count": 1,
            "domain_handler_closeout_result_count": 0,
            "by_receipt_shape": {"no_regression_evidence": 1},
            "by_reconciliation_status": {"no_regression_evidence_reconciled": 1},
            "typed_blocker_count": 0,
            "no_regression_evidence_ref_count": 1,
        },
        "items": [
            {
                "receipt_ref": receipt_ref,
                "receipt_shape": "no_regression_evidence",
                "stage_id": "review_and_rebuttal",
                "source_ref": "opl-ledger://mag/continuous/minimal",
                "reconciliation_status": "no_regression_evidence_reconciled",
                "receipt_ref_matches_domain_handler": None,
                "opl_ledger_ref_matches_receipt_source": True,
                "typed_blocker_present": False,
                "no_regression_evidence_refs": [receipt_ref],
                "authority_boundary": {
                    "mag_owner_receipt_authority": True,
                    "opl_ref_consumer_only": True,
                    "can_declare_fundability_ready": False,
                    "can_declare_authoring_quality_ready": False,
                    "can_declare_submission_ready_export": False,
                },
            }
        ],
        "claims_production_long_run_soak_complete": False,
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "opl_ref_consumer_only": True,
            "can_declare_fundability_ready": False,
            "can_declare_authoring_quality_ready": False,
            "can_declare_submission_ready_export": False,
        },
        "forbidden_write_proof": {
            "repo_receipt_instance_written": False,
            "grant_truth_written": False,
            "grant_artifact_written": False,
            "memory_body_written": False,
            "fundability_verdict_written": False,
            "authoring_quality_verdict_written": False,
            "submission_ready_export_verdict_written": False,
        },
    }


def _minimal_verification(
    receipt_ref: str,
    *,
    result_shape: str,
    provider_completion_ready: bool = False,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_focused_hosted_receipt_verification",
        "version": "v1",
        "state": "focused_hosted_receipt_refs_verified_not_live_soak",
        "focused_status": f"focused_{result_shape}_verified",
        "owner": "med-autogrant",
        "target_domain_id": "med-autogrant",
        "stage_id": "review_and_rebuttal",
        "opl_attempt": {
            "attempt_ref": "opl-attempt://mag/continuous/minimal",
            "ledger_ref": "opl-ledger://mag/continuous/minimal",
            "provider_completion_ref": "opl-provider://mag/continuous/minimal",
            "provider_completion_consumed_as_readiness": provider_completion_ready,
        },
        "mag_owner_receipt": {
            "receipt_ref": receipt_ref,
            "receipt_id": "mag.owner_receipt.minimal",
            "receipt_shape": result_shape,
            "source_ref": "opl-ledger://mag/continuous/minimal",
        },
        "matches": {
            "owner_receipt_ref_matches_opl": True,
            "ledger_ref_matches_receipt_source": True,
            "receipt_ref_matches_domain_handler": None,
        },
        "allowed_result": {
            "result_shape": result_shape,
            "owner_receipt_ref": receipt_ref,
            "typed_blocker_refs": [receipt_ref] if result_shape == "typed_blocker" else [],
            "no_regression_evidence_refs": (
                [receipt_ref] if result_shape == "no_regression_evidence" else []
            ),
        },
        "claims": {
            "claims_opl_provider_completion": True,
            "claims_production_long_run_soak_complete": False,
            "claims_grant_fundability_ready": False,
            "claims_authoring_quality_ready": False,
            "claims_submission_ready_export": False,
        },
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "opl_attempt_owner": "one-person-lab",
            "mag_implements_opl_provider": False,
            "mag_writes_opl_ledger": False,
            "opl_can_write_grant_truth": False,
            "opl_can_write_memory_body": False,
            "provider_completion_can_declare_grant_ready": False,
            "provider_completion_can_declare_export_ready": False,
        },
    }
