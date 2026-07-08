from __future__ import annotations

import unittest
from unittest.mock import (
    Mock,
    patch,
)

from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class ProductEntryFailureModeTest(unittest.TestCase):
    def test_product_entry_fails_closed_on_blank_task_intent(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with self.assertRaisesRegex(WorkspaceStateError, "task_intent"):
            MedAutoGrantProductEntry().build(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                entry_mode="direct",
                task_intent="   ",
            )

    def test_product_entry_rejects_missing_workspace_identity_from_stage_snapshot(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        domain_entry = Mock()
        domain_entry.dispatch.side_effect = [
            {
                "ok": True,
                "grant_run_id": "grant-run-test",
                "workspace_id": None,
                "lifecycle_stage": "critique",
                "verification_checkpoint": {
                    "checkpoint_status": "forward_progress",
                    "identity": {
                        "draft_id": "draft-test",
                    },
                },
                "route": {
                    "next_step": {
                        "recommended_stage": "revision",
                    }
                },
            },
            {
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "intake_snapshot": {
                    "funding_program": "nsfc-2026-general",
                },
            },
        ]

        with self.assertRaisesRegex(WorkspaceStateError, "workspace_id"):
            MedAutoGrantProductEntry(domain_entry=domain_entry).build(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                entry_mode="direct",
                task_intent="tighten-grant-mainline",
            )

    def test_product_entry_fails_closed_on_invalid_executor_routing_contract_shape(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry._build_executor_routing_contract",
            return_value={
                "contract_version": 1,
                "current_stage_route": {
                    "route_id": "critique",
                    "route_status": "pending",
                },
            },
            ):
                with self.assertRaises(WorkspaceStateError):
                    MedAutoGrantProductEntry().build(
                        input_path=str(CRITIQUE_EXAMPLE_PATH),
                        entry_mode="direct",
                        task_intent="tighten-grant-mainline",
                    )

    def test_grant_direct_entry_fails_closed_on_mismatched_entry_mode(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with patch(
            "med_autogrant.product_entry.MedAutoGrantProductEntry.build",
            side_effect=[
                _mismatched_entry_mode_payload(),
                _mismatched_entry_mode_payload(),
            ],
        ):
            with self.assertRaisesRegex(WorkspaceStateError, "grant_direct_entry.direct_entry"):
                MedAutoGrantProductEntry().build_grant_direct_entry(
                    input_path=str(CRITIQUE_EXAMPLE_PATH),
                    task_intent="tighten-grant-mainline",
                )


def _mismatched_entry_mode_payload() -> dict[str, object]:
    return {
        "ok": True,
        "grant_run_id": "grant-run-test",
        "workspace_id": "workspace-test",
        "draft_id": "draft-test",
        "lifecycle_stage": "critique",
        "input_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
        "product_entry": {
            "entry_mode": "opl-handoff",
        },
    }
