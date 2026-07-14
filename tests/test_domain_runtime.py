from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime  # noqa: E402
from med_autogrant.domain_runtime_parts.contracts import build_executor_routing_contract  # noqa: E402
import med_autogrant.domain_runtime_parts.handoff_surfaces as handoff_surfaces  # noqa: E402
from support.cli import run_cli  # noqa: E402
from med_autogrant.workspace_types import WorkspaceStateError  # noqa: E402


EXAMPLES = REPO_ROOT / "examples"
CRITIQUE_EXAMPLE_PATH = EXAMPLES / "nsfc_workspace_p2c_critique.json"
RE_REVIEW_EXAMPLE_PATH = EXAMPLES / "nsfc_workspace_p3b_re_review_major_revision.json"
FROZEN_EXAMPLE_PATH = EXAMPLES / "nsfc_workspace_p3c_presubmission_frozen.json"
IDENTITY = {
    "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
    "workspace_id": "nsfc-demo-001",
    "draft_id": "draft-v1",
}
EXPECTED_AUTHOR_SIDE_ROUTE_IDS = (
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
    "artifact_bundle",
    "final_package",
    "hosted_contract_bundle",
)


class MagRuntimeCliDispatchTest(unittest.TestCase):
    def test_runtime_run_public_cli_is_retired(self) -> None:
        with patch("med_autogrant.domain_entry.MedAutoGrantDomainEntry") as entry_class:
            exit_code, stdout, stderr = run_cli(
                "runtime", "run", "--input", str(CRITIQUE_EXAMPLE_PATH), "--format", "json",
                allow_system_exit=True,
            )

        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("invalid choice", stderr)
        entry_class.assert_not_called()


class MagDomainRuntimeFlowTest(unittest.TestCase):
    def test_identity_survives_revision_final_package_and_hosted_bundle(self) -> None:
        runtime = MagDomainRuntime()
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            revised_path = root / "revised.json"
            bundle_path = root / "bundle.json"
            final_path = root / "final.json"
            hosted_path = root / "hosted.json"

            critique_route = runtime.stage_route_report(input_path=str(CRITIQUE_EXAMPLE_PATH))
            revised = runtime.execute_revision_pass(
                input_path=str(RE_REVIEW_EXAMPLE_PATH),
                output_path=str(revised_path),
            )
            revised_route = runtime.stage_route_report(input_path=str(revised_path))
            bundle = runtime.build_artifact_bundle(
                input_path=str(FROZEN_EXAMPLE_PATH),
                output_path=str(bundle_path),
            )
            final = runtime.build_final_package(
                input_path=str(FROZEN_EXAMPLE_PATH),
                artifact_bundle_path=str(bundle_path),
                output_path=str(final_path),
            )
            hosted = runtime.build_hosted_contract_bundle(
                final_package_path=str(final_path),
                output_path=str(hosted_path),
            )

        self.assertEqual(critique_route["verification_checkpoint"]["identity"]["grant_run_id"], IDENTITY["grant_run_id"])
        self.assertEqual(critique_route["semantic_route_owner"], "decisive_codex_attempt")
        self.assertEqual(revised["grant_run_id"], IDENTITY["grant_run_id"])
        self.assertEqual(revised["draft_id"], IDENTITY["draft_id"])
        self.assertEqual(revised_route["verification_checkpoint"]["identity"]["reviewed_revision_plan_id"], "revision-v1")
        self.assertEqual(bundle["bundle"]["draft_id"], IDENTITY["draft_id"])
        self.assertEqual(final["final_package"]["checkpoint_summary"]["checkpoint_status"], "submission_frozen")
        self.assertEqual(
            hosted["hosted_contract_bundle"]["execution_identity"],
            {**IDENTITY, "program_id": "med-autogrant-mainline"},
        )

    def test_executor_route_catalog_contains_only_landed_author_routes(self) -> None:
        contract = build_executor_routing_contract(
            current_stage="drafting",
            recommended_next_stage="critique",
            include_route_catalog=True,
        )
        current = contract["current_stage_route"]
        recommended = contract["recommended_executor_route"]
        catalog = contract["author_side_route_catalog"]
        catalog_ids = tuple(route["route_id"] for route in catalog)

        self.assertEqual(current["route_id"], "drafting")
        self.assertEqual(recommended["route_id"], "critique")
        self.assertNotIn("handoff_requirements", recommended)
        self.assertTrue(catalog)
        self.assertEqual(catalog_ids, EXPECTED_AUTHOR_SIDE_ROUTE_IDS)
        self.assertEqual({route["route_status"] for route in catalog}, {"landed"})
        route_commands = {route["route_id"]: route["execution_surface"]["command"] for route in catalog}
        for route_id in ("direction_screening", "question_refinement", "argument_building", "fit_alignment", "outline", "drafting"):
            self.assertEqual(route_commands[route_id], "execute-strategy-authoring-pass")

    def test_critique_handoff_forwards_explicit_executor_kind(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir, patch.object(
            handoff_surfaces,
            "build_critique_execution_document",
            return_value={
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "draft_id": "draft-test",
                "active_revision_plan_id": "revision-plan-test",
                "lifecycle_stage": "critique",
                "critique_execution": {"critique_id": "critique-test", "verdict": "major_revision"},
                "critique_workspace": {"lifecycle_stage": "critique"},
            },
        ) as build_document, patch.object(
            handoff_surfaces, "_guard_critique_output_identity"
        ), patch.object(
            handoff_surfaces, "_write_revised_workspace_output"
        ):
            MagDomainRuntime().execute_critique_pass(
                input_path=str(RE_REVIEW_EXAMPLE_PATH),
                output_path=str(Path(tmp_dir) / "critique.json"),
                executor_kind="hermes_agent",
            )

        self.assertEqual(build_document.call_args.kwargs["executor_kind"], "hermes_agent")

    def test_critique_precondition_failure_keeps_route_authority_on_decisive_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir, patch.object(
            handoff_surfaces,
            "build_critique_execution_document",
            side_effect=WorkspaceStateError("critique output is not consumable"),
        ):
            result = MagDomainRuntime().execute_critique_pass(
                input_path=str(RE_REVIEW_EXAMPLE_PATH),
                output_path=str(Path(tmp_dir) / "critique.json"),
            )

        self.assertEqual(result["status"], "completed_with_quality_debt")
        self.assertEqual(
            result["route_back_selection_owner"],
            "decisive_codex_attempt",
        )

    def test_authoring_precondition_failure_becomes_progress_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir, patch.object(
            handoff_surfaces,
            "build_direction_screening_execution_document",
            side_effect=WorkspaceStateError("no candidate was produced"),
        ):
            result = MagDomainRuntime().execute_direction_screening_pass(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                output_path=str(Path(tmp_dir) / "direction.json"),
            )

        self.assertTrue(result["ok"])
        self.assertEqual(result["status"], "completed_with_quality_debt")
        self.assertTrue(result["next_stage_may_start"])
        self.assertFalse(result["quality_debt"]["blocks_stage_transition"])
        self.assertEqual(result["semantic_route_owner"], "decisive_codex_attempt")


if __name__ == "__main__":
    unittest.main()
