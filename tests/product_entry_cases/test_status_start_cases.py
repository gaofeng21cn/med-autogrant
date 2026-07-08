from __future__ import annotations

from copy import deepcopy
import unittest
from unittest.mock import patch

from med_autogrant.public_cli import public_cli_command
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import (
    _expected_runtime_output_path,
    CRITIQUE_EXAMPLE_PATH,
    DIRECTION_EXAMPLE_PATH,
)


def _command_for(input_path, command: str, *extra_args: str) -> str:
    return public_cli_command(
        command,
        "--input",
        str(input_path.resolve()),
        *extra_args,
        "--format",
        "json",
    )


def _question_refinement_command() -> str:
    return _command_for(
        DIRECTION_EXAMPLE_PATH,
        "execute-question-refinement-pass",
        "--output",
        str(
            _expected_runtime_output_path(
                grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                workspace_id="nsfc-demo-001",
                draft_id=None,
                file_name="question-refinement-workspace.json",
            )
        ),
    )


class ProductEntryStatusStartCaseTest(unittest.TestCase):
    def test_grant_user_loop_projects_landed_question_refinement_route_when_direction_screening_can_execute_directly(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(DIRECTION_EXAMPLE_PATH),
            task_intent="advance-grant-mainline",
        )

        self.assertEqual(payload["command"], "grant-user-loop")
        self.assertEqual(payload["lifecycle_stage"], "direction_screening")
        self.assertEqual(
            payload["grant_user_loop"]["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "question_refinement",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["action_kind"],
            "execute_landed_route",
        )
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_id"], "question_refinement")
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_status"], "landed")
        expected_route_command = _question_refinement_command()
        self.assertEqual(payload["grant_user_loop"]["next_action"]["command"], expected_route_command)
        self.assertNotIn("<", payload["grant_user_loop"]["next_action"]["command"])
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["run_recommended_route"],
            expected_route_command,
        )

    def test_product_entry_manifest_fails_closed_on_invalid_mainline_snapshot_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry_parts.manifest_builder._build_mainline_snapshot",
            return_value={
                "current_owner_line": "OPL/Temporal hosted autonomous runtime is the default task runtime; MAG stays a grant-domain authority surface with Codex CLI as the default stage executor",
                "active_phase": "P4 mature direct grant product entry",
                "active_tranche": "P4.G authoring-quality-first completion semantics alignment",
                "phase_map": [{"phase_id": "P4", "phase_name": "mature direct grant product entry", "status": "next"}],
                "next_focus": [1],
                "remaining_gaps": ["mature direct grant Web UI / hosted runtime 仍未 landed。"],
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "product_entry_manifest"):
                MedAutoGrantProductEntry().build_product_entry_manifest(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )

    def test_product_status_fails_closed_on_invalid_operator_loop_action_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        manifest_payload = deepcopy(
            entry.build_product_entry_manifest(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
            )
        )
        manifest_payload["product_entry_manifest"]["operator_loop_actions"]["open_loop"] = {
            "command": public_cli_command("grant-user-loop", "--format", "json"),
        }

        with patch.object(
            MedAutoGrantProductEntry,
            "build_product_entry_manifest",
            return_value=manifest_payload,
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "product_status"):
                MedAutoGrantProductEntry().build_product_status(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )

    def test_grant_progress_fails_closed_on_invalid_projection_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry_parts.progress._build_focus_payload",
            return_value={
                "applicant_name": "示例申请人",
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_progress"):
                MedAutoGrantProductEntry().read_grant_progress(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )

    def test_grant_cockpit_fails_closed_on_invalid_command_catalog_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry_parts.progress._build_product_command_catalog",
            return_value={
                "grant_progress": public_cli_command("grant-progress", "--format", "json"),
            },
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_cockpit"):
                MedAutoGrantProductEntry().read_grant_cockpit(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                )
