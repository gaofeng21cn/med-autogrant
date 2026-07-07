from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductCloseoutDomainHandlerTest(unittest.TestCase):
    def test_domain_handler_dispatch_codex_stage_receipts_returns_read_projection(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "codex-stage-receipts-task.json"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "codex-stage-receipts-1",
                        "action": "closeout/codex-stage-receipts",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "stage_id": "review_and_rebuttal",
                        "execution_attempts": [
                            {
                                "attempt_id": "attempt-critique-001",
                                "executor": "codex_cli",
                                "invocation_ref": "codex://invocations/critique-001",
                                "task_record_ref": "runtime://opl/stage-attempts/critique-001.json",
                                "receipt_ref": "runtime://mag/receipts/stage/critique-001.json",
                                "stage_pack_ref": "agent/prompts/review_and_rebuttal.md",
                                "output_artifact_ref": "runtime://mag/artifacts/critique-001.json",
                            }
                        ],
                        "review_attempts": [
                            {
                                "review_attempt_id": "review-critique-001",
                                "reviewer_executor": "codex_cli",
                                "review_invocation_ref": "codex://invocations/review-critique-001",
                                "review_task_record_ref": (
                                    "runtime://opl/stage-attempts/review-critique-001.json"
                                ),
                                "review_receipt_ref": "runtime://mag/receipts/review/review-critique-001.json",
                                "review_artifact_ref": "runtime://mag/artifacts/review-critique-001.json",
                                "review_target_attempt_id": "attempt-critique-001",
                                "independent_context": True,
                                "shared_context_with_execution": False,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            payload = MedAutoGrantProductEntry().dispatch_domain_handler_task(task_path=task_path)

        dispatch = payload["domain_handler_dispatch"]
        self.assertEqual(dispatch["action"], "closeout/codex-stage-receipts")
        self.assertTrue(dispatch["executed_by_domain_handler"])
        self.assertIsNone(dispatch["executed_command"])
        result = dispatch["result"]
        self.assertEqual(result["surface_kind"], "domain_handler_codex_stage_receipts_result")
        self.assertEqual(result["write_policy"], "read_projection_only_no_domain_truth_mutation")
        bundle = result["receipt_bundle"]
        self.assertEqual(bundle["surface_kind"], "mag_codex_stage_execution_receipt_bundle")
        self.assertEqual(bundle["state"], "codex_stage_receipts_ready_not_quality_ready")
        self.assertFalse(bundle["quality_gate_effect"]["ready_verdict_authorized"])
        self.assertFalse(bundle["authority_boundary"]["can_declare_submission_ready"])

    def test_domain_handler_dispatch_operator_readiness_returns_no_ready_authority(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "operator-readiness-task.json"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "operator-readiness-1",
                        "action": "closeout/operator-readiness",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "production_acceptance": {
                            "surface_kind": "mag_production_acceptance_evidence.v1",
                            "evidence_tail_status": "closed_by_domain_owned_acceptance_receipt",
                            "closure_evidence": {
                                "accepted_return_shape": "domain_owner_receipt_ref",
                                "owner_receipt_ref": "receipt:mag/production-live-acceptance/2026-05-20",
                            },
                        },
                        "external_evidence_receipt_ledger": {
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
                            "remaining_real_evidence_gap_ids": [],
                        },
                        "receipt_readiness_projection": {
                            "surface_kind": "mag_receipt_readiness_projection",
                            "state": "receipt_refs_ready_not_quality_ready",
                            "missing_categories": [],
                            "summary": {
                                "covered_category_count": 4,
                                "missing_category_count": 0,
                                "total_receipt_ref_count": 8,
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            payload = MedAutoGrantProductEntry().dispatch_domain_handler_task(task_path=task_path)

        dispatch = payload["domain_handler_dispatch"]
        self.assertEqual(dispatch["action"], "closeout/operator-readiness")
        self.assertTrue(dispatch["executed_by_domain_handler"])
        result = dispatch["result"]
        self.assertEqual(result["surface_kind"], "domain_handler_operator_closeout_readiness_result")
        self.assertEqual(result["write_policy"], "read_projection_only_no_domain_truth_mutation")
        readiness = result["operator_closeout_readiness"]
        self.assertEqual(readiness["surface_kind"], "mag_operator_closeout_readiness_projection")
        self.assertEqual(readiness["state"], "operator_closeout_refs_ready_not_quality_ready")
        self.assertFalse(readiness["authority_boundary"]["can_declare_submission_ready"])
        self.assertFalse(readiness["authority_boundary"]["can_declare_fundability_ready"])

    def test_domain_handler_dispatch_physical_morphology_guard_returns_guard_projection(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "physical-morphology-task.json"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "physical-morphology-1",
                        "action": "closeout/physical-morphology-guard",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "source_items": [
                            {
                                "path": "src/med_autogrant/product_entry.py",
                                "module_id": "product_entry",
                                "declared_role": "domain_handler_target",
                                "evidence_refs": ["/product_entry_manifest/physical_morphology/product_entry"],
                                "forbidden_role_flags": {
                                    "scheduler_daemon_owner": False,
                                    "attempt_ledger_owner": False,
                                    "local_journal_owner": False,
                                    "generic_runtime_owner": False,
                                    "app_workbench_owner": False,
                                    "compatibility_alias_owner": False,
                                },
                            }
                        ],
                        "external_evidence_refs": [],
                    }
                ),
                encoding="utf-8",
            )
            payload = MedAutoGrantProductEntry().dispatch_domain_handler_task(task_path=task_path)

        dispatch = payload["domain_handler_dispatch"]
        self.assertEqual(dispatch["action"], "closeout/physical-morphology-guard")
        self.assertTrue(dispatch["executed_by_domain_handler"])
        result = dispatch["result"]
        self.assertEqual(result["surface_kind"], "domain_handler_physical_morphology_guard_result")
        self.assertEqual(result["write_policy"], "read_projection_only_no_domain_truth_mutation")
        guard = result["physical_morphology_guard"]
        self.assertEqual(guard["surface_kind"], "mag_physical_morphology_guard_projection")
        self.assertEqual(guard["state"], "allowed_evidence_gated")
        self.assertFalse(guard["claims"]["claims_physical_morphology_cleanup_complete"])
        self.assertFalse(guard["authority_boundary"]["can_declare_physical_cleanup_complete"])

    def test_domain_handler_dispatch_executor_first_bundle_returns_refs_only_bundle(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.product_entry_parts.codex_stage_receipts import (
            build_codex_stage_execution_receipt_bundle,
        )
        from med_autogrant.product_entry_parts.operator_closeout import (
            build_operator_closeout_readiness_projection,
        )
        from med_autogrant.product_entry_parts.physical_morphology_guard import (
            build_physical_morphology_guard_projection,
        )

        codex_bundle = build_codex_stage_execution_receipt_bundle(
            stage_id="review_and_rebuttal",
            execution_attempts=[
                {
                    "attempt_id": "attempt-critique-001",
                    "executor": "codex_cli",
                    "invocation_ref": "codex://invocations/critique-001",
                    "task_record_ref": "runtime://opl/stage-attempts/critique-001.json",
                    "receipt_ref": "runtime://mag/receipts/stage/critique-001.json",
                    "output_artifact_ref": "runtime://mag/artifacts/critique-001.json",
                }
            ],
            review_attempts=[
                {
                    "review_attempt_id": "review-critique-001",
                    "reviewer_executor": "codex_cli",
                    "review_invocation_ref": "codex://invocations/review-critique-001",
                    "review_task_record_ref": "runtime://opl/stage-attempts/review-critique-001.json",
                    "review_receipt_ref": "runtime://mag/receipts/review/review-critique-001.json",
                    "review_artifact_ref": "runtime://mag/artifacts/review-critique-001.json",
                    "review_target_attempt_id": "attempt-critique-001",
                    "independent_context": True,
                    "shared_context_with_execution": False,
                }
            ],
        )
        operator_projection = build_operator_closeout_readiness_projection(
            production_acceptance={
                "surface_kind": "mag_production_acceptance_evidence.v1",
                "evidence_tail_status": "closed_by_domain_owned_acceptance_receipt",
                "closure_evidence": {
                    "accepted_return_shape": "domain_owner_receipt_ref",
                    "owner_receipt_ref": "receipt:mag/production-live-acceptance/2026-05-20",
                },
            },
            external_evidence_receipt_ledger={
                "surface_kind": "mag_external_evidence_receipt_ledger.v1",
                "state": "request_pack_closed_by_receipt_or_domain_owned_typed_blockers",
                "summary": {
                    "closed_request_count": 7,
                    "remaining_open_request_count": 0,
                    "domain_owned_typed_blocker_count": 0,
                    "claims_external_runtime_evidence_received": False,
                    "claims_direct_hosted_parity_passed": False,
                    "claims_temporal_provider_long_soak_complete": False,
                    "claims_grant_or_fundability_ready": False,
                },
                "remaining_real_evidence_gap_ids": [],
            },
            receipt_readiness_projection={
                "surface_kind": "mag_receipt_readiness_projection",
                "state": "receipt_refs_ready_not_quality_ready",
                "missing_categories": [],
                "summary": {
                    "covered_category_count": 4,
                    "missing_category_count": 0,
                    "total_receipt_ref_count": 8,
                },
            },
        )
        physical_guard = build_physical_morphology_guard_projection(
            source_items=[
                {
                    "path": "src/med_autogrant/product_entry.py",
                    "module_id": "product_entry",
                    "declared_role": "domain_handler_target",
                    "evidence_refs": ["/product_entry_manifest/physical_morphology/product_entry"],
                    "forbidden_role_flags": {
                        "scheduler_daemon_owner": False,
                        "attempt_ledger_owner": False,
                        "local_journal_owner": False,
                        "generic_runtime_owner": False,
                        "app_workbench_owner": False,
                        "compatibility_alias_owner": False,
                    },
                }
            ],
            external_evidence_refs=[
                "opl://receipts/mag/physical-morphology/active-caller-migration.json",
                "opl://receipts/mag/physical-morphology/direct-hosted-parity.json",
                "receipt:mag/physical-morphology/owner-receipt-roundtrip.json",
                "opl://receipts/mag/physical-morphology/no-forbidden-write.json",
            ],
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "executor-first-bundle-task.json"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "executor-first-bundle-1",
                        "action": "closeout/executor-first-bundle",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "codex_stage_execution_receipt_bundle": codex_bundle,
                        "operator_closeout_readiness_projection": operator_projection,
                        "physical_morphology_guard_projection": physical_guard,
                        "external_evidence_consumption_ledger": {
                            "surface_kind": "mag_external_evidence_consumption_ledger",
                            "state": "consumed_complete",
                            "summary": {
                                "required_request_count": 2,
                                "satisfied_request_count": 2,
                                "missing_request_count": 0,
                                "accepted_receipt_count": 2,
                            },
                            "missing_request_ids": [],
                            "claims": {
                                "mag_claims_external_evidence_exists": True,
                                "mag_authorizes_fundability_ready": False,
                                "mag_authorizes_quality_ready": False,
                                "mag_authorizes_export_ready": False,
                                "mag_authorizes_submission_ready": False,
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            payload = MedAutoGrantProductEntry().dispatch_domain_handler_task(task_path=task_path)

        dispatch = payload["domain_handler_dispatch"]
        self.assertEqual(dispatch["action"], "closeout/executor-first-bundle")
        self.assertTrue(dispatch["executed_by_domain_handler"])
        result = dispatch["result"]
        self.assertEqual(result["surface_kind"], "domain_handler_executor_first_closeout_bundle_result")
        self.assertEqual(result["write_policy"], "read_projection_only_no_domain_truth_mutation")
        bundle = result["executor_first_closeout_bundle"]
        self.assertEqual(bundle["surface_kind"], "mag_executor_first_closeout_bundle")
        self.assertEqual(bundle["state"], "refs_ready_not_quality_ready")
        self.assertFalse(bundle["can_declare_submission_ready"])
        self.assertFalse(bundle["bundle_ready_equals_grant_ready"])
