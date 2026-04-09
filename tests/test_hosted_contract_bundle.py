from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.cli import main  # noqa: E402


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class HostedContractBundleCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(list(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_build_hosted_contract_bundle_writes_expected_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "build-hosted-contract-bundle")
            self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
            self.assertEqual(payload["draft_id"], "draft-v1")
            self.assertEqual(payload["output_path"], str(hosted_contract_path.resolve()))

            contract_bundle = payload["hosted_contract_bundle"]
            self.assertEqual(contract_bundle["contract_version"], 1)
            self.assertEqual(contract_bundle["bundle_kind"], "hosted_contract_bundle")
            self.assertEqual(
                contract_bundle["formal_entry_matrix"],
                {
                    "default_formal_entry": "CLI",
                    "supported_protocol_layer": "MCP",
                    "internal_controller_surface": "controller",
                },
            )
            self.assertEqual(
                contract_bundle["execution_identity"],
                {
                    "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                    "workspace_id": "nsfc-demo-001",
                    "draft_id": "draft-v1",
                    "program_id": "med-autogrant-mainline",
                },
            )
            self.assertEqual(
                contract_bundle["session_contract"],
                {
                    "session_handle_kind": "grant_run_id",
                    "start_entry": "run-local",
                    "resume_entry": "resume-local",
                    "required_local_surfaces": [
                        "run-local",
                        "resume-local",
                        "build-artifact-bundle",
                        "build-final-package",
                        "run_journal",
                        "stage_action_envelope",
                    ],
                },
            )
            self.assertEqual(
                contract_bundle["state_contract"],
                {
                    "workspace_surface_kind": "nsfc_workspace",
                    "run_journal_kind": "local_run_journal",
                    "stage_action_envelope_kind": "stage_action_envelope",
                    "artifact_bundle_kind": "artifact_bundle",
                    "final_package_kind": "final_package",
                },
            )
            self.assertEqual(
                contract_bundle["artifact_contract"],
                {
                    "artifact_bundle_manifest_kind": "artifact_bundle_manifest",
                    "final_package_manifest_kind": "freeze_manifest",
                    "lineage_fields": [
                        "frozen_question_id",
                        "selected_direction_id",
                        "selected_question_id",
                        "active_fit_mapping_id",
                        "draft_id",
                        "revision_plan_id",
                    ],
                },
            )
            self.assertEqual(
                contract_bundle["audit_contract"],
                {
                    "verification_checkpoint_kind": "verification_checkpoint",
                    "checkpoint_status_kind": "checkpoint_status",
                    "reviewed_revision_evidence_kind": "reviewed_revision_evidence",
                },
            )
            self.assertEqual(json.loads(hosted_contract_path.read_text(encoding="utf-8")), contract_bundle)

    def test_build_hosted_contract_bundle_fails_closed_for_non_final_package_input(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "not-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            final_package_path.write_text(
                json.dumps(
                    {
                        "package_kind": "artifact_bundle",
                        "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                        "workspace_id": "nsfc-demo-001",
                        "draft_id": "draft-v1",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("final package kind 非法", payload["error"])

    def test_build_hosted_contract_bundle_fails_closed_when_existing_output_identity_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            hosted_contract_path.write_text(
                json.dumps(
                    {
                        "grant_run_id": "other-run",
                        "workspace_id": "other-workspace",
                        "draft_id": "other-draft",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            exit_code, stdout, stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("hosted contract output identity 不匹配", payload["error"])

    def test_build_hosted_contract_bundle_allows_overwrite_for_same_identity_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)

            first_exit, first_stdout, first_stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )
            self.assertEqual(first_exit, 0)
            self.assertEqual(first_stderr, "")
            first_payload = json.loads(first_stdout)
            self.assertTrue(first_payload["ok"])

            second_exit, second_stdout, second_stderr = self.run_cli(
                "build-hosted-contract-bundle",
                "--final-package",
                str(final_package_path),
                "--output",
                str(hosted_contract_path),
                "--format",
                "json",
            )

            self.assertEqual(second_exit, 0)
            self.assertEqual(second_stderr, "")
            second_payload = json.loads(second_stdout)
            self.assertTrue(second_payload["ok"])
            self.assertEqual(
                json.loads(hosted_contract_path.read_text(encoding="utf-8")),
                second_payload["hosted_contract_bundle"],
            )

    def _build_final_package(self, input_path: Path, final_package_path: Path) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "bundle.json"
            build_bundle_exit, _, build_bundle_stderr = self.run_cli(
                "build-artifact-bundle",
                "--input",
                str(input_path),
                "--output",
                str(bundle_path),
                "--format",
                "json",
            )
            self.assertEqual(build_bundle_exit, 0)
            self.assertEqual(build_bundle_stderr, "")

            build_package_exit, _, build_package_stderr = self.run_cli(
                "build-final-package",
                "--input",
                str(input_path),
                "--artifact-bundle",
                str(bundle_path),
                "--output",
                str(final_package_path),
                "--format",
                "json",
            )
            self.assertEqual(build_package_exit, 0)
            self.assertEqual(build_package_stderr, "")


if __name__ == "__main__":
    unittest.main()
