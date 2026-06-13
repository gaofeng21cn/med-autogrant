from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from med_autogrant.public_cli import public_cli_command
from med_autogrant.product_entry_parts import orchestration_companions as module
from med_autogrant.product_entry_parts.orchestration_companions import (
    _build_family_orchestration_companion,
)
from product_entry_cases.support import (
    _assert_family_orchestration_companion,
    _expected_runtime_output_path,
    CRITIQUE_EXAMPLE_PATH,
    DRAFTING_EXAMPLE_PATH,
)


class ProductEntryFamilyOrchestrationTest(unittest.TestCase):
    def test_family_orchestration_companion_is_projected_across_product_surfaces(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        entry = MedAutoGrantProductEntry()
        progress_payload = entry.read_grant_progress(input_path=str(CRITIQUE_EXAMPLE_PATH))
        cockpit_payload = entry.read_grant_cockpit(input_path=str(CRITIQUE_EXAMPLE_PATH))
        direct_entry_payload = entry.build_grant_direct_entry(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )
        user_loop_payload = entry.build_grant_user_loop(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            task_intent="tighten-grant-mainline",
        )
        manifest_payload = entry.build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        _assert_family_orchestration_companion(
            self,
            progress_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            cockpit_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            direct_entry_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            user_loop_payload.get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )
        _assert_family_orchestration_companion(
            self,
            manifest_payload["product_entry_manifest"].get("family_orchestration"),
            expected_resume_surface="grant_user_loop",
        )

    def test_family_orchestration_action_graph_uses_shared_product_entry_orchestration(self) -> None:
        captured: dict[str, object] = {}

        def _fake_build_family_product_entry_orchestration(**kwargs: object) -> dict[str, object]:
            captured.update(kwargs)
            return {
                "action_graph_ref": {
                    "ref_kind": "json_pointer",
                    "ref": "/family_orchestration/action_graph",
                    "label": "mag family action graph",
                },
                "action_graph": {
                    "graph_id": str(kwargs["graph_id"]),
                    "target_domain_id": str(kwargs["target_domain_id"]),
                    "graph_kind": str(kwargs["graph_kind"]),
                    "graph_version": str(kwargs["graph_version"]),
                    "nodes": list(kwargs["nodes"]),
                    "edges": list(kwargs["edges"]),
                    "entry_nodes": list(kwargs["entry_nodes"]),
                    "exit_nodes": list(kwargs["exit_nodes"]),
                    "human_gates": list(kwargs["human_gates"]),
                    "checkpoint_policy": {
                        "mode": "explicit_nodes",
                        "checkpoint_nodes": list(kwargs["checkpoint_nodes"]),
                    },
                },
                "human_gates": list(kwargs["human_gate_previews"]),
                "resume_contract": {
                    "surface_kind": str(kwargs["resume_surface_kind"]),
                    "session_locator_field": str(kwargs["session_locator_field"]),
                    "checkpoint_locator_field": str(kwargs["checkpoint_locator_field"]),
                },
            }

        with patch.object(
            module,
            "_build_shared_family_product_entry_orchestration",
            side_effect=_fake_build_family_product_entry_orchestration,
        ):
            payload = _build_family_orchestration_companion(
                current_route_id="drafting",
                recommended_route_id="critique",
                recommended_route_status="pending",
                needs_author_decision=True,
                review_surface_ref="/review",
                event_envelope_surface_ref="/events",
                checkpoint_lineage_surface_ref="/lineage",
                resume_surface_kind="grant_user_loop",
            )

        self.assertEqual(payload["action_graph"]["graph_id"], "mag_drafting_to_critique_graph")
        self.assertEqual(captured["graph_kind"], "grant_route_orchestration")
        self.assertEqual([node["node_id"] for node in captured["nodes"]], ["route:drafting", "route:critique"])
        self.assertEqual([edge["on"] for edge in captured["edges"]], ["decision"])
        self.assertEqual(captured["entry_nodes"], ["route:drafting"])
        self.assertEqual(captured["exit_nodes"], ["route:critique"])
        self.assertEqual(captured["checkpoint_nodes"], ["route:drafting", "route:critique"])
        self.assertEqual(captured["human_gate_previews"][0]["gate_id"], "mag_route_gate_critique")

    def test_grant_user_loop_projects_landed_critique_route_when_drafting_can_execute_directly(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_grant_user_loop(
            input_path=str(DRAFTING_EXAMPLE_PATH),
            task_intent="prepare-critique-handoff",
        )

        self.assertEqual(payload["command"], "grant-user-loop")
        self.assertEqual(payload["lifecycle_stage"], "drafting")
        self.assertEqual(
            payload["grant_user_loop"]["grant_direct_entry"]["recommended_executor_route"]["route_id"],
            "critique",
        )
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["action_kind"],
            "execute_landed_route",
        )
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_id"], "critique")
        self.assertEqual(payload["grant_user_loop"]["next_action"]["route_status"], "landed")
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["command"],
            public_cli_command(
                "execute-critique-pass",
                "--input",
                str(DRAFTING_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id="draft-v1",
                        file_name="critique-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )
        self.assertNotIn("<", payload["grant_user_loop"]["next_action"]["command"])
        self.assertEqual(
            payload["grant_user_loop"]["next_action"]["handoff_surfaces"],
            None,
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["run_recommended_route"],
            public_cli_command(
                "execute-critique-pass",
                "--input",
                str(DRAFTING_EXAMPLE_PATH.resolve()),
                "--output",
                str(
                    _expected_runtime_output_path(
                        grant_run_id="grant-run-nsfc-demo-001-baseline-001",
                        workspace_id="nsfc-demo-001",
                        draft_id="draft-v1",
                        file_name="critique-workspace.json",
                    )
                ),
                "--format",
                "json",
            ),
        )
        self.assertEqual(
            payload["grant_user_loop"]["user_loop"]["open_grant_direct_entry"],
            public_cli_command(
                "grant-direct-entry",
                "--input",
                str(DRAFTING_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "prepare-critique-handoff",
                "--format",
                "json",
            ),
        )

    def test_grant_user_loop_keeps_runtime_root_semantic_path_when_codex_projects_is_symlink(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            codex_home = tmp_root / "codex-home"
            workspace_target = tmp_root / "workspace-projects-target"
            codex_home.mkdir()
            workspace_target.mkdir()
            (codex_home / "projects").symlink_to(workspace_target, target_is_directory=True)

            with patch.dict(os.environ, {"CODEX_HOME": str(codex_home)}, clear=False):
                payload = MedAutoGrantProductEntry().build_grant_user_loop(
                    input_path=str(DRAFTING_EXAMPLE_PATH),
                    task_intent="prepare-critique-handoff",
                )

            command = payload["grant_user_loop"]["next_action"]["command"]
            expected_root = codex_home / "projects" / "med-autogrant" / "runtime-state"
            self.assertIn(str(expected_root), command)
            self.assertNotIn(str(workspace_target / "med-autogrant" / "runtime-state"), command)
