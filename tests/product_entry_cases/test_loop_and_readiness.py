from __future__ import annotations

import unittest
from unittest.mock import patch

from med_autogrant.public_cli import public_cli_command
from product_entry_cases.support import (
    _expected_runtime_output_path,
    CRITIQUE_EXAMPLE_PATH,
)


class ProductEntryLoopReadinessTest(unittest.TestCase):
    def test_grant_user_loop_packages_mainline_snapshot_and_landed_next_action(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )

        self.assertEqual(payload["command"], "grant-user-loop")
        self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
        self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
        self.assertEqual(payload["draft_id"], "draft-v1")
        self.assertEqual(payload["lifecycle_stage"], "critique")
        self.assertEqual(payload["grant_user_loop"]["entry_kind"], "grant_user_loop")
        self.assertEqual(
            payload["grant_user_loop"]["mainline_snapshot"]["active_tranche"],
            "P4.G authoring-quality-first completion semantics alignment",
        )
        self.assertEqual(
            payload["grant_user_loop"]["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "revision",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["action_kind"],
            "execute_landed_route",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["route_id"],
            "revision",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["command"],
            public_cli_command(
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
            ),
        )
        self.assertNotIn("<", payload["grant_user_loop"]["next_action"]["command"])
        self.assertIsNone(payload["grant_user_loop"]["next_action"]["handoff_surfaces"])
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["mainline_status"],
            public_cli_command("mainline-status", "--format", "json"),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["phase_status_current"],
            public_cli_command("mainline-phase", "--phase", "current", "--format", "json"),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_cockpit"],
            public_cli_command(
                "grant-cockpit", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_direct_entry"],
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
        self.assertEqual(
            payload["grant_user_loop"]["session_continuity"]["surface_kind"],
            "session_continuity",
        )
        self.assertEqual(
            payload["grant_user_loop"]["session_continuity"]["session_id"],
            payload["grant_run_id"],
        )
        self.assertEqual(
            payload["grant_user_loop"]["progress_projection"]["surface_kind"],
            "progress_projection",
        )
        self.assertEqual(
            payload["grant_user_loop"]["artifact_inventory"]["surface_kind"],
            "artifact_inventory",
        )
        self.assertEqual(
            payload["grant_user_loop"]["runtime_control"]["surface_kind"],
            "runtime_control",
        )
        self.assertEqual(
            payload["grant_user_loop"]["runtime_control"]["runtime_owner"],
            "one-person-lab",
        )
        self.assertEqual(payload["grant_user_loop"]["runtime_control"]["executor_owner"], "codex_cli")
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
            payload["grant_user_loop"]["user_loop"]["open_grant_direct_entry"],
        )

    def test_product_preflight_uses_shared_program_companion_builder(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        captured: dict[str, object] = {}

        def _fake_build_product_entry_preflight(**kwargs: object) -> dict[str, object]:
            captured.update(kwargs)
            return {
                "surface_kind": "product_entry_preflight",
                "summary": "[shared-builder] preflight",
                "ready_to_try_now": True,
                "recommended_check_command": str(kwargs["recommended_check_command"]),
                "recommended_start_command": str(kwargs["recommended_start_command"]),
                "blocking_check_ids": [],
                "checks": list(kwargs["checks"]),  # type: ignore[arg-type]
            }

        with patch(
            "med_autogrant.product_entry_parts.preflight._build_shared_product_entry_preflight",
            side_effect=_fake_build_product_entry_preflight,
        ) as preflight_builder:
            payload = MedAutoGrantProductEntry().build_product_entry_preflight(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
            )

        preflight_builder.assert_called_once()
        self.assertEqual(payload["product_entry_preflight"]["summary"], "[shared-builder] preflight")
        self.assertEqual(
            [check["check_id"] for check in captured["checks"]],  # type: ignore[index]
            [
                "workspace_document_valid",
                "default_runtime_owner_line",
                "direct_product entry surface_contract_landed",
                "submission_ready_export_gate",
            ],
        )
        self.assertEqual(
            captured["recommended_check_command"],
            public_cli_command(
                "validate-workspace",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--format",
                "json",
            ),
        )

    def test_grant_authoring_readiness_uses_shared_detailed_builders(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        workflow_calls: list[dict[str, object]] = []

        def _fake_build_workflow_coverage_item(**kwargs: object) -> dict[str, str]:
            payload = {key: str(value) for key, value in kwargs.items()}
            payload["remaining_gap"] = f"[shared-item] {payload['remaining_gap']}"
            workflow_calls.append(dict(kwargs))
            return payload

        def _fake_build_detailed_readiness(**kwargs: object) -> dict[str, object]:
            payload = dict(kwargs)
            payload["summary"] = f"{payload['summary']} [shared-detailed-readiness]"
            return payload

        with patch(
            "med_autogrant.product_entry_parts.manifest_readiness._build_shared_workflow_coverage_item",
            side_effect=_fake_build_workflow_coverage_item,
        ) as workflow_builder, patch(
            "med_autogrant.product_entry_parts.manifest_readiness._build_shared_detailed_readiness",
            side_effect=_fake_build_detailed_readiness,
        ) as readiness_builder:
            manifest = MedAutoGrantProductEntry().build_product_entry_manifest(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
            )["product_entry_manifest"]

        workflow_builder.assert_called()
        readiness_builder.assert_called_once()
        self.assertEqual(len(workflow_calls), 9)
        self.assertEqual(workflow_calls[0]["step_id"], "accumulation_direction_screening")
        readiness = manifest["grant_authoring_readiness"]
        self.assertTrue(readiness["summary"].endswith("[shared-detailed-readiness]"))
        self.assertTrue(
            readiness["workflow_coverage"][0]["remaining_gap"].startswith("[shared-item] ")
        )
