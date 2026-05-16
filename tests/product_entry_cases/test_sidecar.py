from __future__ import annotations

import json
import tempfile
from pathlib import Path

from product_entry_cases.support import *  # noqa: F401,F403


class ProductSidecarTest(unittest.TestCase):
    def test_sidecar_export_maps_runtime_and_attention_surfaces_without_grant_truth_transfer(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_sidecar_export(input_path=str(CRITIQUE_EXAMPLE_PATH))

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["command"], "product-sidecar-export")
        export = payload["sidecar_export"]
        self.assertEqual(export["surface_kind"], "mag_product_sidecar_export")
        self.assertEqual(export["adapter_id"], "mag.opl_stage_led.product_sidecar.v1")
        self.assertEqual(export["substrate_boundary"]["online_substrate_owner"], "explicit_opl_provider")
        self.assertEqual(export["substrate_boundary"]["control_plane_owner"], "one-person-lab")
        self.assertEqual(export["substrate_boundary"]["domain_truth_owner"], "med-autogrant")
        self.assertFalse(export["substrate_boundary"]["hermes_proof_executor_default"])
        self.assertIn("OPL may explicitly choose", export["substrate_boundary"]["default_executor_note"])
        self.assertEqual(export["runtime_control"]["surface_kind"], "runtime_control")
        self.assertEqual(export["runtime_continuity"]["surface_kind"], "skill_runtime_continuity")
        self.assertEqual(
            export["standard_domain_agent_skeleton"]["surface_kind"],
            "standard_domain_agent_skeleton",
        )
        self.assertEqual(
            export["artifact_locator_contract"]["surface_kind"],
            "domain_artifact_locator_contract",
        )
        self.assertEqual(
            export["controlled_stage_attempt_projection"]["surface_kind"],
            "controlled_stage_attempt_projection",
        )
        hosted_proof = export["controlled_stage_attempt_projection"][
            "opl_hosted_controlled_grant_stage_attempt_proof"
        ]
        self.assertEqual(
            hosted_proof["surface_kind"],
            "opl_hosted_controlled_grant_stage_attempt_proof",
        )
        self.assertEqual(
            hosted_proof["maps_to_opl_contract"],
            "opl_hosted_controlled_stage_attempt_proof.v1",
        )
        self.assertEqual(
            hosted_proof["consumed_memory_proof_ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator/controlled_consumed_memory_proof",
        )
        self.assertEqual(
            hosted_proof["writeback_receipt_proof_ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator/writeback_receipt_proof",
        )
        self.assertFalse(hosted_proof["repo_tracked_real_receipt_instance"])
        self.assertFalse(hosted_proof["repo_tracked_real_memory_body"])
        self.assertFalse(hosted_proof["authority_boundary"]["opl_can_hold_fundability_verdict"])
        self.assertFalse(hosted_proof["authority_boundary"]["opl_can_hold_authoring_quality_verdict"])
        self.assertFalse(hosted_proof["authority_boundary"]["opl_can_hold_export_verdict"])
        self.assertEqual(
            export["receipt_refs"],
            export["controlled_stage_attempt_projection"]["receipt_refs"],
        )
        apply_proof = export["controlled_domain_memory_apply_proof"]
        self.assertEqual(
            apply_proof["surface_kind"],
            "controlled_grant_stage_domain_memory_apply_proof",
        )
        self.assertEqual(
            apply_proof["operator_receipt_projection"]["surface_kind"],
            "mag_domain_memory_operator_receipt_projection",
        )
        self.assertFalse(apply_proof["authority_boundary"]["can_write_fundability_verdict"])
        self.assertEqual(
            export["memory_receipt_refs"],
            apply_proof["writeback_receipt_refs"],
        )
        self.assertEqual(
            export["repo_source_layout_audit"],
            apply_proof["repo_source_layout_audit"],
        )
        self.assertEqual(export["owner_receipt_contract"]["surface_kind"], "mag_owner_receipt_contract")
        self.assertEqual(
            export["owner_receipt_contract"]["allowed_return_shapes"],
            ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
        )
        thinning = export["mag_consumer_thinning_contract"]
        self.assertEqual(thinning["surface_kind"], "mag_consumer_thinning_contract")
        self.assertEqual(thinning["state"], "handoff_ready_external_opl_replacement_gated")
        self.assertEqual(
            thinning["sidecar_contract_ref"],
            "/product_entry_manifest/mag_consumer_thinning_contract",
        )
        self.assertEqual(
            thinning["exposed_sidecar_return_refs"],
            {
                "owner_receipt_contract_ref": "/product_entry_manifest/owner_receipt_contract",
                "controlled_stage_attempt_projection_ref": (
                    "/product_entry_manifest/controlled_stage_attempt_projection"
                ),
                "controlled_domain_memory_apply_proof_ref": (
                    "/product_entry_manifest/controlled_domain_memory_apply_proof"
                ),
                "lifecycle_guarded_apply_proof_ref": "/product_entry_manifest/lifecycle_guarded_apply_proof",
                "grant_transition_oracle_ref": "/product_entry_manifest/grant_transition_oracle",
            },
        )
        self.assertFalse(thinning["authority_boundary"]["mag_rebuilds_opl_runtime"])
        self.assertEqual(thinning["forbidden_mag_owned_generic_primitives"], [])
        self.assertIn("generic_workbench_owner", thinning["forbidden_mag_generic_owner_roles"])
        self.assertIn("generic_memory_transport_owner", thinning["forbidden_mag_generic_owner_roles"])
        self.assertIn("generic_artifact_lifecycle_owner", thinning["forbidden_mag_generic_owner_roles"])
        consumed = export["consumed_opl_standard_surfaces"]
        self.assertEqual(consumed, thinning["consumed_opl_standard_surfaces"])
        self.assertEqual(consumed["surface_kind"], "mag_consumed_opl_standard_surfaces")
        self.assertEqual(
            consumed["sidecar_projection_ref"],
            "/sidecar_export/mag_consumer_thinning_contract",
        )
        self.assertEqual(consumed["authority_boundary"]["opl_standard_scaffold_owner"], "one-person-lab")
        self.assertTrue(consumed["authority_boundary"]["mag_consumes_standard_scaffold"])
        self.assertTrue(consumed["authority_boundary"]["mag_consumes_generic_primitives"])
        self.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_memory_transport"])
        self.assertFalse(consumed["authority_boundary"]["mag_can_own_generic_artifact_lifecycle"])
        self.assertIn("grant_truth", consumed["mag_retained_authority"])
        self.assertIn("package_authority", consumed["mag_retained_authority"])
        output_guard = thinning["thin_surface_output_guard"]
        self.assertEqual(output_guard["surface_kind"], "mag_thin_surface_output_guard")
        self.assertEqual(output_guard["allowed_output_classes"], thinning["mag_owned_outputs"])
        self.assertEqual(output_guard["required_sidecar_return_refs"], thinning["exposed_sidecar_return_refs"])
        self.assertIn("generic_memory_transport_state", output_guard["forbidden_output_classes"])
        self.assertIn("generic_artifact_lifecycle_state", output_guard["forbidden_output_classes"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_generic_runtime_state"])
        self.assertFalse(output_guard["authority_boundary"]["mag_can_emit_generic_workbench_state"])
        scaffold_guard = thinning["standard_agent_scaffold_alignment"]
        self.assertEqual(
            scaffold_guard["surface_kind"],
            "mag_standard_agent_scaffold_thin_surface_guard",
        )
        self.assertFalse(scaffold_guard["knowledge_only_repository"])
        self.assertTrue(scaffold_guard["retains_domain_program_surfaces"])
        self.assertFalse(export["owner_receipt_contract"]["forbidden_write_proof"]["opl_can_write_grant_truth"])
        self.assertEqual(
            export["lifecycle_guarded_apply_proof"]["surface_kind"],
            "mag_lifecycle_guarded_apply_proof",
        )
        self.assertEqual(
            [operation["operation"] for operation in export["lifecycle_guarded_apply_proof"]["operations"]],
            ["cleanup", "restore", "retention"],
        )
        self.assertEqual(
            export["physical_skeleton_follow_through"]["surface_kind"],
            "mag_physical_skeleton_follow_through",
        )
        self.assertFalse(export["physical_skeleton_follow_through"]["moves_workspace_artifacts"])
        self.assertEqual(
            export["ideal_state_closure_status"]["surface_kind"],
            "mag_ideal_state_closure_status",
        )
        self.assertFalse(export["ideal_state_closure_status"]["claims_production_long_run_soak_complete"])
        self.assertFalse(
            export["controlled_stage_attempt_projection"]["opl_consumption_contract"][
                "can_hold_fundability_verdict"
            ]
        )
        self.assertFalse(
            export["controlled_stage_attempt_projection"]["opl_consumption_contract"][
                "can_hold_export_verdict"
            ]
        )
        self.assertEqual(export["todo_wakeup"]["surface_kind"], "mag_todo_wakeup_projection")
        self.assertEqual(
            export["todo_wakeup"]["authoring_loop_continuation"]["automation_id"],
            "mag.authoring_loop_continuation",
        )
        self.assertEqual(export["autonomy_controller"]["default_mode"], "dry_run")
        self.assertFalse(export["autonomy_controller"]["hermes_proof_executor_default"])
        self.assertEqual(export["user_loop_attention_queue"]["queue_owner"], "one-person-lab")
        self.assertEqual(
            export["user_loop_attention_queue"]["queue_write_policy"],
            "enqueue_wakeup_only_no_grant_truth_writes",
        )
        self.assertEqual(
            export["opl_control_plane"]["write_policy"],
            "opl_index_only_no_grant_truth_writes",
        )
        self.assertEqual(
            export["opl_control_plane"]["replacement_expectations_ref"],
            "/sidecar_export/mag_consumer_thinning_contract/opl_replacement_expectations",
        )
        self.assertEqual(
            export["opl_control_plane"]["allowed_dispatch_actions"],
            [
                "autonomy-controller/dry-run",
                "autonomy-controller/guarded-run",
                "domain-memory/decide",
                "domain-memory/propose",
                "lifecycle/receipt",
                "notification/receipt",
                "stage-attempt/closeout",
                "status/read",
                "user-loop/wakeup",
            ],
        )
        self.assertIn("hermes_proof_executor", export["guardrails"]["forbidden_defaults"])

    def test_sidecar_dispatch_status_read_and_user_loop_wakeup_are_mag_owned(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        with tempfile.TemporaryDirectory() as tmp_dir:
            status_task = Path(tmp_dir) / "status-task.json"
            status_task.write_text(
                json.dumps(
                    {
                        "task_id": "status-1",
                        "action": "status/read",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                    }
                ),
                encoding="utf-8",
            )
            status_payload = entry.dispatch_sidecar_task(task_path=status_task)
            wakeup_task = Path(tmp_dir) / "wakeup-task.json"
            wakeup_task.write_text(
                json.dumps(
                    {
                        "task_id": "wakeup-1",
                        "action": "user-loop/wakeup",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "task_intent": "continue-grant-loop",
                    }
                ),
                encoding="utf-8",
            )
            wakeup_payload = entry.dispatch_sidecar_task(task_path=wakeup_task)

        self.assertEqual(status_payload["sidecar_dispatch"]["action"], "status/read")
        self.assertTrue(status_payload["sidecar_dispatch"]["executed_by_sidecar"])
        self.assertEqual(
            status_payload["sidecar_dispatch"]["result"]["product_status"]["surface_kind"],
            "product_status",
        )
        self.assertEqual(wakeup_payload["sidecar_dispatch"]["action"], "user-loop/wakeup")
        self.assertTrue(wakeup_payload["sidecar_dispatch"]["executed_by_sidecar"])
        self.assertEqual(
            wakeup_payload["sidecar_dispatch"]["result"]["grant_user_loop"]["surface_kind"],
            "grant_user_loop",
        )
        self.assertFalse(wakeup_payload["sidecar_dispatch"]["guardrails"]["hermes_proof_executor_default"])

    def test_sidecar_dispatch_autonomy_controller_returns_guarded_command_without_execution(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            task_path = Path(tmp_dir) / "autonomy-task.json"
            output_dir = Path(tmp_dir) / "out"
            task_path.write_text(
                json.dumps(
                    {
                        "task_id": "autonomy-1",
                        "action": "autonomy-controller/dry-run",
                        "input_path": str(CRITIQUE_EXAMPLE_PATH),
                        "output_dir": str(output_dir),
                    }
                ),
                encoding="utf-8",
            )
            payload = MedAutoGrantProductEntry().dispatch_sidecar_task(task_path=task_path)

        dispatch = payload["sidecar_dispatch"]
        self.assertEqual(dispatch["status"], "accepted")
        self.assertFalse(dispatch["executed_by_sidecar"])
        self.assertEqual(dispatch["result"]["mode"], "dry_run")
        self.assertIn("autonomy-controller", dispatch["result"]["command"])
        self.assertFalse(dispatch["result"]["hermes_proof_executor_default"])

    def test_sidecar_dispatch_domain_memory_apply_flow_projects_refs_without_repo_artifacts(self) -> None:
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
            proposal_payload = entry.dispatch_sidecar_task(task_path=proposal_task)
            proposal_path = Path(tmp_dir) / "proposal.json"
            proposal_path.write_text(
                json.dumps(proposal_payload["sidecar_dispatch"]["result"]["proposal"]),
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
            decision_payload = entry.dispatch_sidecar_task(task_path=decision_task)
            receipt_evidence = decision_payload["sidecar_dispatch"]["result"]["receipt_evidence"]
            receipt_exists = Path(receipt_evidence["receipt_instance_ref"]).exists()

        proposal = proposal_payload["sidecar_dispatch"]["result"]["proposal"]
        self.assertEqual(proposal["surface_kind"], "mag_domain_memory_writeback_proposal")
        self.assertEqual(proposal["stage_id"], "review_and_rebuttal")
        self.assertEqual(proposal["write_policy"], "runtime_store_only_no_repo_write")
        self.assertFalse(proposal["forbidden_content_scan"]["contains_canonical_grant_artifact_content"])
        decision = decision_payload["sidecar_dispatch"]["result"]["decision"]
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

    def test_sidecar_dispatch_controlled_stage_closeout_writes_owner_receipt_evidence(self) -> None:
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
            payload = MedAutoGrantProductEntry().dispatch_sidecar_task(task_path=task_path)
            receipt = payload["sidecar_dispatch"]["result"]["owner_receipt_evidence"]
            receipt_exists = Path(receipt["receipt_instance_ref"]).exists()

        dispatch = payload["sidecar_dispatch"]
        self.assertEqual(dispatch["action"], "stage-attempt/closeout")
        self.assertTrue(dispatch["executed_by_sidecar"])
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

    def test_sidecar_dispatch_lifecycle_receipt_writes_guarded_apply_receipt_evidence(self) -> None:
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
            payload = MedAutoGrantProductEntry().dispatch_sidecar_task(task_path=task_path)
            receipt = payload["sidecar_dispatch"]["result"]["lifecycle_receipt_evidence"]
            receipt_exists = Path(receipt["receipt_instance_ref"]).exists()

        dispatch = payload["sidecar_dispatch"]
        self.assertEqual(dispatch["action"], "lifecycle/receipt")
        self.assertTrue(dispatch["executed_by_sidecar"])
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

    def test_sidecar_dispatch_fails_closed_on_unowned_action(self) -> None:
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
                MedAutoGrantProductEntry().dispatch_sidecar_task(task_path=task_path)

    def test_cli_accepts_three_token_product_sidecar_commands(self) -> None:
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
                exit_code = main(
                    [
                        "product",
                        "sidecar",
                        "dispatch",
                        "--task",
                        str(task_path),
                        "--format",
                        "json",
                    ]
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["sidecar_dispatch"]["action"], "notification/receipt")
        self.assertEqual(payload["sidecar_dispatch"]["result"]["receipt_status"], "accepted")
        self.assertTrue(payload["sidecar_dispatch"]["receipt_refs"]["opl_consumes_receipt_ref_only"])
        self.assertEqual(
            payload["sidecar_dispatch"]["result"]["receipt_refs"],
            payload["sidecar_dispatch"]["receipt_refs"],
        )
