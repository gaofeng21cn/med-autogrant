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


CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
RE_REVIEW_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3b_re_review_major_revision.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class HermesRuntimeCliDispatchTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(list(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_validate_workspace_dispatches_through_hermes_runtime_substrate(self) -> None:
        expected_payload = {
            "ok": True,
            "command": "validate-workspace",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "lifecycle_stage": "critique",
            "error_count": 0,
            "errors": [],
        }

        with patch("med_autogrant.cli.HermesRuntimeSubstrate") as substrate_class:
            substrate = substrate_class.return_value
            substrate.validate_workspace.return_value = expected_payload

            exit_code, stdout, stderr = self.run_cli(
                "validate-workspace",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH),
                "--format",
                "json",
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        self.assertEqual(json.loads(stdout), expected_payload)
        substrate.validate_workspace.assert_called_once_with(input_path=str(CRITIQUE_EXAMPLE_PATH))

    def test_run_local_dispatches_through_hermes_runtime_substrate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            journal_path = Path(tmp_dir) / "journal.json"
            expected_payload = {
                "ok": True,
                "command": "run-local",
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "draft_id": "draft-test",
                "lifecycle_stage": "critique",
                "input_path": str(CRITIQUE_EXAMPLE_PATH),
                "journal_path": str(journal_path),
                "attempt_index": 1,
                "stop_reason": {
                    "code": "stage_action_required",
                    "reason": "runtime owned by Hermes",
                    "current_stage": "critique",
                    "recommended_next_stage": "revision",
                    "checkpoint_status": "forward_progress",
                    "requires_human_confirmation": False,
                    "forced_rollback_stage": None,
                    "forced_rollback_reason": None,
                },
                "stage_action_envelope": None,
                "route_report": {"ok": True},
                "resume": {
                    "command": "resume-local",
                    "journal_path": str(journal_path),
                },
            }

            with patch("med_autogrant.cli.HermesRuntimeSubstrate") as substrate_class:
                substrate = substrate_class.return_value
                substrate.run_local.return_value = expected_payload

                exit_code, stdout, stderr = self.run_cli(
                    "run-local",
                    "--input",
                    str(CRITIQUE_EXAMPLE_PATH),
                    "--journal",
                    str(journal_path),
                    "--format",
                    "json",
                )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            self.assertEqual(json.loads(stdout), expected_payload)
            substrate.run_local.assert_called_once_with(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                journal_path=str(journal_path),
            )


class HermesRuntimeSubstrateFlowTest(unittest.TestCase):
    def test_hermes_runtime_substrate_keeps_revision_and_export_paths_identity_stable(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        runtime = HermesRuntimeSubstrate()
        self.assertEqual(runtime.runtime_owner, "Hermes")

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            revised_workspace_path = tmp_root / "revised.json"
            revised_bundle_path = tmp_root / "revised-bundle.json"
            revised_journal_path = tmp_root / "revised-journal.json"
            frozen_bundle_path = tmp_root / "frozen-bundle.json"
            final_package_path = tmp_root / "final-package.json"
            hosted_contract_path = tmp_root / "hosted-contract.json"

            critique_report = runtime.stage_route_report(input_path=str(CRITIQUE_EXAMPLE_PATH))
            self.assertTrue(critique_report["ok"])
            self.assertEqual(critique_report["verification_checkpoint"]["identity"]["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")

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

            revised_run = runtime.run_local(
                input_path=str(revised_workspace_path),
                journal_path=str(revised_journal_path),
            )
            self.assertTrue(revised_run["ok"])
            self.assertEqual(revised_run["stop_reason"]["recommended_next_stage"], "revision")

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


class LocalRuntimeBridgeTest(unittest.TestCase):
    def test_run_local_runtime_uses_hermes_runtime_as_compatibility_bridge(self) -> None:
        from med_autogrant.local_runtime import run_local_runtime

        expected_payload = {"ok": True, "command": "run-local"}
        with patch("med_autogrant.local_runtime.HermesRuntimeSubstrate") as substrate_class:
            substrate = substrate_class.return_value
            substrate.run_local.return_value = expected_payload

            payload = run_local_runtime(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                journal_path="/tmp/test-journal.json",
            )

        self.assertEqual(payload, expected_payload)
        substrate.run_local.assert_called_once_with(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
            journal_path="/tmp/test-journal.json",
            trigger="run-local",
        )

    def test_resume_local_runtime_uses_hermes_runtime_as_compatibility_bridge(self) -> None:
        from med_autogrant.local_runtime import resume_local_runtime

        expected_payload = {"ok": True, "command": "resume-local"}
        with patch("med_autogrant.local_runtime.HermesRuntimeSubstrate") as substrate_class:
            substrate = substrate_class.return_value
            substrate.resume_local.return_value = expected_payload

            payload = resume_local_runtime(journal_path="/tmp/test-journal.json")

        self.assertEqual(payload, expected_payload)
        substrate.resume_local.assert_called_once_with(journal_path="/tmp/test-journal.json")


class HostedContractBundleBridgeTest(unittest.TestCase):
    def test_hosted_contract_bundle_payload_uses_hermes_runtime_as_handoff_owner(self) -> None:
        from med_autogrant.hosted_contract_bundle import build_hosted_contract_bundle_payload

        expected_payload = {"ok": True, "command": "build-hosted-contract-bundle"}
        with patch("med_autogrant.hermes_runtime.HermesRuntimeSubstrate") as substrate_class:
            substrate = substrate_class.return_value
            substrate.build_hosted_contract_bundle.return_value = expected_payload

            payload = build_hosted_contract_bundle_payload(
                final_package_path="/tmp/final-package.json",
                output_path="/tmp/hosted-contract.json",
            )

        self.assertEqual(payload, expected_payload)
        substrate.build_hosted_contract_bundle.assert_called_once_with(
            final_package_path="/tmp/final-package.json",
            output_path="/tmp/hosted-contract.json",
        )


class ArtifactBundleHandoffTest(unittest.TestCase):
    def test_build_artifact_bundle_uses_hermes_handoff_owner(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        runtime = HermesRuntimeSubstrate()
        expected_bundle = {
            "bundle_version": 1,
            "bundle_kind": "artifact_bundle",
            "grant_run_id": "grant-run-test",
            "workspace_id": "workspace-test",
            "draft_id": "draft-test",
            "lifecycle_stage": "critique",
        }

        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "bundle.json"
            with patch(
                "med_autogrant.hermes_runtime.build_artifact_bundle_document",
                create=True,
                return_value=expected_bundle,
            ) as build_document, patch(
                "med_autogrant.hermes_runtime._guard_artifact_bundle_output_identity",
                create=True,
            ) as guard_output, patch(
                "med_autogrant.hermes_runtime._write_artifact_bundle_output",
                create=True,
            ) as write_output:
                payload = runtime.build_artifact_bundle(
                    input_path=str(FROZEN_EXAMPLE_PATH),
                    output_path=str(bundle_path),
                )

        self.assertEqual(payload["bundle"], expected_bundle)
        build_document.assert_called_once()
        guard_output.assert_called_once()
        write_output.assert_called_once_with(bundle_path.resolve(), expected_bundle)


class FinalPackageHandoffTest(unittest.TestCase):
    def test_build_final_package_uses_hermes_handoff_owner(self) -> None:
        from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

        runtime = HermesRuntimeSubstrate()
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            bundle_path = tmp_root / "bundle.json"
            package_path = tmp_root / "package.json"
            runtime.build_artifact_bundle(
                input_path=str(FROZEN_EXAMPLE_PATH),
                output_path=str(bundle_path),
            )
            expected_final_package = {
                "package_version": 1,
                "package_kind": "final_package",
                "grant_run_id": "grant-run-test",
                "workspace_id": "workspace-test",
                "draft_id": "draft-test",
                "lifecycle_stage": "frozen",
            }

            with patch(
                "med_autogrant.hermes_runtime._read_artifact_bundle",
                create=True,
                return_value={"manifest": {}, "artifacts": [1, 2]},
            ) as read_bundle, patch(
                "med_autogrant.hermes_runtime.build_final_package_document",
                create=True,
                return_value=expected_final_package,
            ) as build_document, patch(
                "med_autogrant.hermes_runtime._guard_final_package_output_identity",
                create=True,
            ) as guard_output, patch(
                "med_autogrant.hermes_runtime._write_final_package_output",
                create=True,
            ) as write_output:
                payload = runtime.build_final_package(
                    input_path=str(FROZEN_EXAMPLE_PATH),
                    artifact_bundle_path=str(bundle_path),
                    output_path=str(package_path),
                )

        self.assertEqual(payload["final_package"], expected_final_package)
        read_bundle.assert_called_once()
        build_document.assert_called_once()
        guard_output.assert_called_once()
        write_output.assert_called_once_with(package_path.resolve(), expected_final_package)


if __name__ == "__main__":
    unittest.main()
