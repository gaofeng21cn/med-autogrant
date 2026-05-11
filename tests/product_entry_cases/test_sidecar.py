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
        self.assertEqual(export["adapter_id"], "mag.hermes_family.product_sidecar.v1")
        self.assertEqual(export["substrate_boundary"]["online_substrate_owner"], "hermes_agent")
        self.assertEqual(export["substrate_boundary"]["control_plane_owner"], "one-person-lab")
        self.assertEqual(export["substrate_boundary"]["domain_truth_owner"], "med-autogrant")
        self.assertFalse(export["substrate_boundary"]["hermes_proof_executor_default"])
        self.assertEqual(export["runtime_control"]["surface_kind"], "runtime_control")
        self.assertEqual(export["runtime_continuity"]["surface_kind"], "skill_runtime_continuity")
        self.assertEqual(
            export["domain_agent_skeleton_mapping"]["surface_kind"],
            "standard_domain_agent_skeleton_mapping",
        )
        self.assertEqual(
            export["artifact_locator_contract"]["surface_kind"],
            "domain_artifact_locator_contract",
        )
        self.assertEqual(
            export["controlled_stage_attempt_projection"]["surface_kind"],
            "controlled_stage_attempt_projection",
        )
        self.assertEqual(
            export["receipt_refs"],
            export["controlled_stage_attempt_projection"]["receipt_refs"],
        )
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
            export["opl_control_plane"]["allowed_dispatch_actions"],
            [
                "autonomy-controller/dry-run",
                "autonomy-controller/guarded-run",
                "notification/receipt",
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
