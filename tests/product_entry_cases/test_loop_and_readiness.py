from __future__ import annotations

import unittest

import med_autogrant.product_entry_parts.loop_route_shell as loop_route_shell
from med_autogrant.public_cli import public_cli_command
from product_entry_cases.support import (
    _expected_runtime_output_path,
    assert_path_values,
    CRITIQUE_EXAMPLE_PATH,
)


class ProductEntryLoopReadinessTest(unittest.TestCase):
    def test_grant_user_loop_packages_mainline_snapshot_and_landed_next_action(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )

        expected_next_command = public_cli_command(
            "execute-revision-pass",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH.resolve()),
            "--output",
            str(
                _expected_runtime_output_path(
                    grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                    workspace_id="nsfc-demo-001",
                    draft_id="draft-v1",
                    file_name="revision-workspace.json",
                )
            ),
            "--format",
            "json",
        )
        assert_path_values(
            self,
            payload,
            {
                "command": "grant-user-loop",
                "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                "workspace_id": "nsfc-demo-001",
                "draft_id": "draft-v1",
                "lifecycle_stage": "critique",
                "grant_user_loop.entry_kind": "grant_user_loop",
                "grant_user_loop.grant_direct_entry.recommended_executor_route.route_id": "revision",
                "grant_user_loop.next_action.action_kind": "execute_landed_route",
                "grant_user_loop.next_action.route_id": "revision",
                "grant_user_loop.next_action.command": expected_next_command,
                "grant_user_loop.session_continuity.session_id": payload["grant_run_id"],
                "grant_user_loop.runtime_control.runtime_owner": "one-person-lab",
                "grant_user_loop.runtime_control.executor_owner": "codex_cli",
            },
        )
        self.assertEqual(
            loop_route_shell._build_route_execution_command(
                route_id="revision",
                input_path=CRITIQUE_EXAMPLE_PATH,
                grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                workspace_id="nsfc-demo-001",
                draft_id="draft-v1",
            ),
            payload["grant_user_loop"]["next_action"]["command"],
        )
        self.assertNotIn("<", payload["grant_user_loop"]["next_action"]["command"])
        self.assertIsNone(payload["grant_user_loop"]["next_action"]["handoff_surfaces"])
        self.assertEqual(
            payload["grant_user_loop"]["runtime_control"]["approval_control_surface"]["command"],
            public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "tighten-grant-mainline",
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            payload["grant_user_loop"]["runtime_control"]["direct_entry"]["command"],
            public_cli_command(
                "grant-direct-entry",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "tighten-grant-mainline",
                "--format",
                "json",
            ),
        )
