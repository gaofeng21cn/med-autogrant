from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
from io import StringIO
from pathlib import Path

from med_autogrant.cli import main
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.domain_handler_export_assertions import (
    assert_domain_handler_export_maps_runtime_and_attention_surfaces,
)
from product_entry_cases.support import (
    CRITIQUE_EXAMPLE_PATH,
    REPO_ROOT,
)


class ProductDomainHandlerTest(unittest.TestCase):
    def test_domain_handler_export_maps_runtime_and_attention_surfaces_without_grant_truth_transfer(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_domain_handler_export(input_path=str(CRITIQUE_EXAMPLE_PATH))

        assert_domain_handler_export_maps_runtime_and_attention_surfaces(
            self,
            payload,
            REPO_ROOT,
        )

    def test_domain_handler_shell_projection_fixes_caller_owner_readback_guard(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        export = MedAutoGrantProductEntry().build_domain_handler_export(input_path=str(CRITIQUE_EXAMPLE_PATH))[
            "domain_handler_export"
        ]

        caller_owner = export["caller_owner_contract"]
        self.assertEqual(
            caller_owner["active_caller_readback_state"],
            "mag_direct_domain_handler_active_until_opl_caller_evidence",
        )
        self.assertFalse(caller_owner["opl_generated_or_hosted_caller_evidence_observed"])
        readback_guard = caller_owner["readback_guard"]
        self.assertEqual(readback_guard["active_caller_owner_until_evidence"], "med-autogrant")
        self.assertEqual(readback_guard["active_caller_surface_until_evidence"], "mag_direct_domain_handler")
        self.assertEqual(readback_guard["evidence_owner"], "one-person-lab")
        self.assertFalse(readback_guard["grant_truth_write_authorized"])
        self.assertFalse(readback_guard["external_evidence_authorized_by_mag_repo"])
        self.assertFalse(readback_guard["physical_delete_authorized"])
        self.assertFalse(readback_guard["provider_completion_is_grant_ready"])
        self.assertFalse(readback_guard["provider_completion_is_submission_ready"])
        self.assertEqual(
            export["guardrails"]["readback_boundary"],
            {
                "active_caller_remains": "mag_direct_domain_handler_until_opl_caller_evidence",
                "grant_truth_write_authorized": False,
                "external_evidence_authorized_by_mag_repo": False,
                "physical_delete_authorized": False,
                "provider_completion_is_grant_ready": False,
                "provider_completion_is_submission_ready": False,
            },
        )

    def test_domain_handler_dispatch_retires_generic_wrapper_actions(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        for action in (
            "status/read",
            "user-loop/wakeup",
            "notification/receipt",
            "autonomy-controller/dry-run",
            "autonomy-controller/guarded-run",
        ):
            with self.subTest(action=action), tempfile.TemporaryDirectory() as tmp_dir:
                task_path = Path(tmp_dir) / "generic-action.json"
                task_path.write_text(
                    json.dumps(
                        {
                            "task_id": "retired-generic-action",
                            "action": action,
                            "input_path": str(CRITIQUE_EXAMPLE_PATH),
                            "task_intent": "continue-grant-loop",
                            "notification": {"kind": "opl_wakeup_ack"},
                        }
                    ),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(WorkspaceStateError, "action 不允许"):
                    entry.dispatch_domain_handler_task(task_path=task_path)

    def test_domain_handler_dispatch_domain_memory_apply_flow_projects_refs_without_repo_artifacts(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            proposal_task = Path(tmp_dir) / "proposal-task.json"
            proposal_task.write_text(
                json.dumps(
                    {
                        "task_id": "memory-proposal-1",
                        "action": "domain-memory/propose",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "stage_id": "review_and_rebuttal",
                        "source_ref": "runtime-closeout://grant-run/example",
                        "lesson_summary": "Reviewer risk framing should be handled before rebuttal closure.",
                        "proposal_id": "review-risk-framing",
                    }
                ),
                encoding="utf-8",
            )
            proposal_payload = entry.dispatch_domain_handler_task(task_path=proposal_task)
            proposal_path = Path(tmp_dir) / "proposal.json"
            proposal_path.write_text(
                json.dumps(proposal_payload["domain_handler_dispatch"]["result"]["proposal"]),
                encoding="utf-8",
            )
            decision_task = Path(tmp_dir) / "decision-task.json"
            runtime_root = Path(tmp_dir) / "runtime-state"
            decision_task.write_text(
                json.dumps(
                    {
                        "task_id": "memory-decision-1",
                        "action": "domain-memory/decide",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "proposal_path": str(proposal_path),
                        "decision": "accepted",
                        "decision_reason": "Reusable stage strategy without grant artifact content.",
                        "memory_id": "review-risk-framing",
                        "runtime_root": str(runtime_root),
                    }
                ),
                encoding="utf-8",
            )
            decision_payload = entry.dispatch_domain_handler_task(task_path=decision_task)
            receipt_evidence = decision_payload["domain_handler_dispatch"]["result"]["receipt_evidence"]
            receipt_exists = Path(receipt_evidence["receipt_instance_ref"]).exists()

        proposal = proposal_payload["domain_handler_dispatch"]["result"]["proposal"]
        self.assertEqual(proposal["surface_kind"], "mag_domain_memory_writeback_proposal")
        self.assertEqual(proposal["stage_id"], "review_and_rebuttal")
        self.assertEqual(proposal["write_policy"], "runtime_store_only_no_repo_write")
        self.assertFalse(proposal["forbidden_content_scan"]["contains_canonical_grant_artifact_content"])
        decision = decision_payload["domain_handler_dispatch"]["result"]["decision"]
        self.assertEqual(decision["surface_kind"], "mag_domain_memory_writeback_decision")
        self.assertEqual(decision["decision"], "accepted")
        self.assertEqual(decision["write_policy"], "runtime_store_only_no_repo_write")
        receipt_projection = decision["operator_receipt_projection"]
        self.assertTrue(receipt_projection["opl_consumes_receipt_ref_only"])
        self.assertFalse(receipt_projection["contains_memory_body"])
        self.assertFalse(receipt_projection["contains_quality_or_export_verdict"])
        self.assertEqual(receipt_evidence["surface_kind"], "mag_domain_memory_runtime_receipt_evidence")
        self.assertEqual(receipt_evidence["state"], "runtime_receipt_instance_written")
        self.assertFalse(receipt_evidence["repo_tracked"])
        self.assertFalse(receipt_evidence["contains_memory_body"])
        self.assertTrue(receipt_exists)

    def test_domain_handler_dispatch_controlled_stage_closeout_writes_owner_receipt_evidence(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "stage-closeout-task.json"
            runtime_root = Path(tmp_dir) / "runtime-state"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "stage-closeout-1",
                        "action": "stage-attempt/closeout",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "receipt_shape": "no_regression_evidence",
                        "stage_id": "review_and_rebuttal",
                        "source_ref": "opl-stage-attempt://stage-closeout-1",
                        "closeout_summary": "No regression evidence over MAG-owned refs.",
                        "runtime_root": str(runtime_root),
                        "consumed_memory_refs": [
                            "mag-memory:accepted:review-risk-framing",
                        ],
                        "writeback_receipt_refs": [
                            "mag-memory-writeback:accepted:review-risk-framing",
                            "mag-memory-writeback:rejected:review-style",
                        ],
                    }
                ),
                encoding="utf-8",
            )
            payload = MedAutoGrantProductEntry().dispatch_domain_handler_task(task_path=task_path)
            receipt = payload["domain_handler_dispatch"]["result"]["owner_receipt_evidence"]
            receipt_exists = Path(receipt["receipt_instance_ref"]).exists()

        dispatch = payload["domain_handler_dispatch"]
        self.assertEqual(dispatch["action"], "stage-attempt/closeout")
        self.assertTrue(dispatch["executed_by_domain_handler"])
        self.assertEqual(dispatch["result"]["return_shape"], "no_regression_evidence")
        self.assertEqual(dispatch["result"]["receipt_ref"], receipt["receipt_instance_ref"])
        self.assertEqual(
            dispatch["result"]["receipt_refs"]["owner_receipt_ref"],
            receipt["receipt_instance_ref"],
        )
        self.assertEqual(
            dispatch["result"]["consumed_memory_refs"],
            ["mag-memory:accepted:review-risk-framing"],
        )
        self.assertEqual(
            dispatch["result"]["writeback_receipt_refs"],
            [
                "mag-memory-writeback:accepted:review-risk-framing",
                "mag-memory-writeback:rejected:review-style",
            ],
        )
        self.assertTrue(dispatch["result"]["receipt_refs"]["opl_consumes_receipt_ref_only"])
        self.assertIn(
            "/product_entry_manifest/owner_receipt_contract",
            dispatch["result"]["source_refs"],
        )
        self.assertIsNone(dispatch["result"]["typed_blocker"])
        self.assertEqual(receipt["surface_kind"], "mag_owner_receipt_evidence")
        self.assertEqual(receipt["receipt_shape"], "no_regression_evidence")
        self.assertFalse(receipt["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(receipt["forbidden_write_proof"]["memory_body_written"])
        self.assertTrue(receipt_exists)

    def test_domain_handler_dispatch_lifecycle_receipt_writes_guarded_apply_receipt_evidence(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "lifecycle-task.json"
            runtime_root = Path(tmp_dir) / "runtime-state"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "lifecycle-cleanup-1",
                        "action": "lifecycle/receipt",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "operation": "cleanup",
                        "receipt_shape": "typed_blocker",
                        "source_ref": "opl-lifecycle://cleanup/1",
                        "closeout_summary": "OPL cleanup can only route ledger refs.",
                        "runtime_root": str(runtime_root),
                    }
                ),
                encoding="utf-8",
            )
            payload = MedAutoGrantProductEntry().dispatch_domain_handler_task(task_path=task_path)
            receipt = payload["domain_handler_dispatch"]["result"]["lifecycle_receipt_evidence"]
            receipt_exists = Path(receipt["receipt_instance_ref"]).exists()

        dispatch = payload["domain_handler_dispatch"]
        self.assertEqual(dispatch["action"], "lifecycle/receipt")
        self.assertTrue(dispatch["executed_by_domain_handler"])
        self.assertEqual(dispatch["result"]["return_shape"], "typed_blocker")
        self.assertEqual(dispatch["result"]["receipt_ref"], receipt["receipt_instance_ref"])
        self.assertEqual(
            dispatch["result"]["receipt_refs"]["lifecycle_receipt_ref"],
            receipt["receipt_instance_ref"],
        )
        self.assertEqual(
            dispatch["result"]["typed_blocker"]["blocker_kind"],
            "mag_lifecycle_owner_receipt_required",
        )
        self.assertTrue(dispatch["result"]["receipt_refs"]["opl_consumes_receipt_ref_only"])
        self.assertEqual(receipt["surface_kind"], "mag_lifecycle_receipt_evidence")
        self.assertEqual(receipt["operation"], "cleanup")
        self.assertEqual(receipt["artifact_mutation"], "none")
        self.assertFalse(receipt["forbidden_write_proof"]["grant_artifact_written"])
        self.assertTrue(receipt_exists)

    def test_domain_handler_dispatch_fails_closed_on_unowned_action(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "bad-task.json"
            task_path.write_text(
                json.dumps(
                    {
                        "action": "proof-executor/run",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(WorkspaceStateError, "action 不允许"):
                MedAutoGrantProductEntry().dispatch_domain_handler_task(task_path=task_path)

    def test_cli_rejects_retired_notification_receipt_domain_handler_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "receipt-task.json"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "receipt-1",
                        "action": "notification/receipt",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "notification": {"kind": "opl_wakeup_ack"},
                    }
                ),
                encoding="utf-8",
            )
            stdout = StringIO()
            stderr = StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as raised:
                    main(
                        [
                            "product",
                            "domain_handler",
                            "dispatch",
                            "--task",
                            str(task_path),
                            "--format",
                            "json",
                        ]
                    )

        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("invalid choice: 'product'", stderr.getvalue())
