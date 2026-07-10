from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402
import med_autogrant.domain_runtime_parts.handoff_surfaces as handoff_surfaces  # noqa: E402
from med_autogrant.domain_runtime_parts.contracts import build_author_side_route_contract  # noqa: E402
from support.cli import public_cli_argv  # noqa: E402
from med_autogrant.domain_runtime_parts.shared import AUTHOR_SIDE_ROUTE_IDS  # noqa: E402


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"

def _expected_route(route_id: str, *, source_stage: str) -> dict[str, object]:
    return build_author_side_route_contract(route_id, source_stage=source_stage)


class MagRuntimeCliDispatchTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_validate_workspace_dispatches_through_domain_entry(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "validate-workspace",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "lifecycle_stage": "critique",
            "error_count": 0,
            "errors": [],
        }

        with patch("med_autogrant.domain_entry.MedAutoGrantDomainEntry") as entry_class:
            entry = entry_class.return_value
            entry.dispatch.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "workspace",
                "validate",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        entry.dispatch.assert_called_once_with(
            {
                "command": "validate-workspace",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
            }
        )

    def test_runtime_run_public_cli_is_retired(self) -> None:
        with patch("med_autogrant.domain_entry.MedAutoGrantDomainEntry") as entry_class:
            exit_code, stdout, stderr = self.run_cli(
                "runtime",
                "run",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("invalid choice", stderr)
        entry_class.assert_not_called()


class MagDomainRuntimeFlowTest(unittest.TestCase):
    def test_mag_runtime_keeps_revision_and_export_paths_identity_stable(self) -> None:
        from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime

        runtime = MagDomainRuntime()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            revised_workspace_path = tmp_root / "revised.json"
            revised_bundle_path = tmp_root / "revised-bundle.json"
            frozen_bundle_path = tmp_root / "frozen-bundle.json"
            final_package_path = tmp_root / "final-package.json"
            hosted_contract_path = tmp_root / "hosted-contract.json"

            critique_report = runtime.stage_route_report(input_path=str(CRITIQUE_EXAMPLE_PATH))
            self.assertTrue(critique_report["ok"])
            self.assertEqual(critique_report["verification_checkpoint"]["identity"]["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(
                critique_report["route"]["next_step"]["recommended_stage"],
                "argument_building",
            )

            revised_payload = runtime.execute_revision_pass(
                input_path=str(RE_REVIEW_EXAMPLE_PATH),
                output_path=str(revised_workspace_path),
            )
            self.assertTrue(revised_payload["ok"])
            self.assertEqual(revised_payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(revised_payload["draft_id"], "draft-v1")

            revised_report = runtime.stage_route_report(input_path=str(revised_workspace_path))
            self.assertTrue(revised_report["ok"])
            self.assertEqual(
                revised_report["verification_checkpoint"]["identity"]["reviewed_revision_plan_id"],
                "revision-v1",
            )

            revised_bundle = runtime.build_artifact_bundle(
                input_path=str(revised_workspace_path),
                output_path=str(revised_bundle_path),
            )
            self.assertTrue(revised_bundle["ok"])
            self.assertEqual(revised_bundle["bundle"]["draft_id"], "draft-v1")

            revised_route_report = runtime.stage_route_report(input_path=str(revised_workspace_path))
            self.assertTrue(revised_route_report["ok"])
            self.assertEqual(
                revised_route_report["route"]["next_step"]["recommended_stage"],
                "argument_building",
            )

            frozen_bundle = runtime.build_artifact_bundle(
                input_path=str(FROZEN_EXAMPLE_PATH),
                output_path=str(frozen_bundle_path),
            )
            self.assertTrue(frozen_bundle["ok"])

            final_package = runtime.build_final_package(
                input_path=str(FROZEN_EXAMPLE_PATH),
                artifact_bundle_path=str(frozen_bundle_path),
                output_path=str(final_package_path),
            )
            self.assertTrue(final_package["ok"])
            self.assertEqual(final_package["final_package"]["checkpoint_summary"]["checkpoint_status"], "submission_frozen")

            hosted_contract = runtime.build_hosted_contract_bundle(
                final_package_path=str(final_package_path),
                output_path=str(hosted_contract_path),
            )
            self.assertTrue(hosted_contract["ok"])
            self.assertEqual(
                hosted_contract["hosted_contract_bundle"]["execution_identity"],
                {
                    "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    "workspace_id": "nsfc-demo-001",
                    "draft_id": "draft-v1",
                    "program_id": "med-autogrant-mainline",
                },
            )

    def test_executor_routing_contract_publishes_landed_route_catalog_only(self) -> None:
        from med_autogrant.domain_runtime_parts.contracts import build_executor_routing_contract

        drafting_contract = build_executor_routing_contract(
            current_stage="drafting",
            recommended_next_stage="critique",
            include_route_catalog=True,
        )
        self.assertEqual(
            drafting_contract["current_stage_route"],
            _expected_route("drafting", source_stage="drafting"),
        )
        self.assertEqual(
            drafting_contract["recommended_executor_route"],
            _expected_route("critique", source_stage="drafting"),
        )
        self.assertNotIn("handoff_requirements", drafting_contract["recommended_executor_route"])

        critique_reroute_contract = build_executor_routing_contract(
            current_stage="critique",
            recommended_next_stage="question_refinement",
        )
        self.assertEqual(
            critique_reroute_contract["recommended_executor_route"],
            _expected_route("question_refinement", source_stage="critique"),
        )
        self.assertNotIn("handoff_requirements", critique_reroute_contract["recommended_executor_route"])

        self.assertEqual(
            [
                route["route_id"]
                for route in drafting_contract["author_side_route_catalog"]
            ],
            list(AUTHOR_SIDE_ROUTE_IDS),
        )

class RevisionExecutionHandoffTest(unittest.TestCase):
    def test_execute_critique_pass_forwards_explicit_executor_kind(self) -> None:
        from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime

        runtime = MagDomainRuntime()

        with tempfile.TemporaryDirectory() as tmp_dir:
            workspace_path = Path(tmp_dir) / "critique.json"
            with patch.object(
                handoff_surfaces,
                "build_critique_execution_document",
                return_value={
                    "grant_run_id": "grant-run-test",
                    "workspace_id": "workspace-test",
                    "draft_id": "draft-test",
                    "active_revision_plan_id": "revision-plan-test",
                    "lifecycle_stage": "critique",
                    "critique_execution": {
                        "critique_id": "critique-test",
                        "active_revision_plan_id": "revision-plan-test",
                        "verdict": "major_revision",
                    },
                    "critique_workspace": {
                        "grant_run_id": "grant-run-test",
                        "workspace_id": "workspace-test",
                        "lifecycle_stage": "critique",
                    },
                },
            ) as build_document, patch.object(
                handoff_surfaces,
                "_guard_critique_output_identity",
            ), patch.object(
                handoff_surfaces,
                "_write_revised_workspace_output",
            ):
                runtime.execute_critique_pass(
                    input_path=str(REVISION_EXAMPLE_PATH),
                    output_path=str(workspace_path),
                    executor_kind="hermes_agent",
                )

        _, kwargs = build_document.call_args
        self.assertEqual(kwargs["executor_kind"], "hermes_agent")


if __name__ == "__main__":
    unittest.main()
