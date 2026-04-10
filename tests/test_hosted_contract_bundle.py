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
from med_autogrant import hosted_contract_bundle as hosted_contract_bundle_module  # noqa: E402


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

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_freeze_manifest_is_not_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "bad-freeze-manifest-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package["freeze_manifest"] = []
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

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
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("freeze_manifest", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_checkpoint_summary_is_not_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "bad-checkpoint-summary-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package["checkpoint_summary"] = []
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

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
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("checkpoint_summary", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_lineage_is_not_object(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "bad-lineage-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package["lineage"] = []
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

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
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("lineage", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_package_version_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "missing-package-version-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package.pop("package_version")
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

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
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("package_version", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_lifecycle_stage_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "missing-lifecycle-stage-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package.pop("lifecycle_stage")
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

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
            self.assertIn("final package 缺少字段", payload["error"])
            self.assertIn("lifecycle_stage", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_identity_fields_are_not_nonempty_strings(self) -> None:
        cases = (
            ("grant_run_id", []),
            ("workspace_id", {}),
            ("draft_id", []),
        )
        for field, bad_value in cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"bad-{field}-final-package.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package[field] = bad_value
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
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
                    self.assertIn("final package 缺少字段", payload["error"])
                    self.assertIn(field, payload["error"])
                    self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_freeze_manifest_missing_required_fields(self) -> None:
        required_fields = (
            "draft_version_label",
            "draft_status",
            "active_revision_plan_id",
            "critique_id",
            "checkpoint_status",
            "presubmission_frozen",
        )
        for field in required_fields:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"missing-freeze-manifest-{field}.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["freeze_manifest"].pop(field)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
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
                    self.assertIn("final package freeze_manifest 缺少字段", payload["error"])
                    self.assertIn(field, payload["error"])
                    self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_checkpoint_summary_missing_required_fields(self) -> None:
        required_fields = (
            "verification_checkpoint",
            "checkpoint_status",
        )
        for field in required_fields:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"missing-checkpoint-summary-{field}.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["checkpoint_summary"].pop(field)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
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
                    self.assertIn("final package checkpoint_summary 缺少字段", payload["error"])
                    self.assertIn(field, payload["error"])
                    self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_lineage_missing_required_fields(self) -> None:
        required_fields = (
            "frozen_question_id",
            "selected_direction_id",
            "selected_question_id",
            "active_fit_mapping_id",
            "draft_id",
            "revision_plan_id",
        )
        for field in required_fields:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"missing-lineage-{field}.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["lineage"].pop(field)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
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
                    self.assertIn("final package lineage 缺少字段", payload["error"])
                    self.assertIn(field, payload["error"])
                    self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_freeze_manifest_draft_status_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "bad-draft-status-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package["freeze_manifest"]["draft_status"] = "draft"
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

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
            self.assertIn("final package freeze_manifest.draft_status 非法", payload["error"])
            self.assertIn("draft", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_freeze_manifest_checkpoint_status_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "bad-freeze-manifest-checkpoint-status-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package["freeze_manifest"]["checkpoint_status"] = "forward_progress"
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

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
            self.assertIn("final package freeze_manifest.checkpoint_status 非法", payload["error"])
            self.assertIn("forward_progress", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_checkpoint_summary_checkpoint_status_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "bad-checkpoint-summary-checkpoint-status-final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
            final_package["checkpoint_summary"]["checkpoint_status"] = "forward_progress"
            final_package_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")

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
            self.assertIn("final package checkpoint_summary.checkpoint_status 非法", payload["error"])
            self.assertIn("forward_progress", payload["error"])
            self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_checkpoint_status_is_missing_or_mismatched(self) -> None:
        cases = (
            (
                "missing-verification-checkpoint-status",
                lambda final_package: final_package["checkpoint_summary"]["verification_checkpoint"].pop("checkpoint_status"),
                "final package verification_checkpoint.checkpoint_status 非法",
            ),
            (
                "mismatched-checkpoint-status",
                lambda final_package: final_package["checkpoint_summary"]["verification_checkpoint"].__setitem__(
                    "checkpoint_status", "freeze_ready"
                ),
                "final package checkpoint_status 不一致",
            ),
            (
                "mismatched-freeze-manifest-status",
                lambda final_package: final_package["freeze_manifest"].__setitem__("checkpoint_status", "freeze_ready"),
                "final package checkpoint_status 不一致",
            ),
        )
        for name, mutate, expected_error in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"{name}.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    mutate(final_package)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
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
                    self.assertIn(expected_error, payload["error"])
                    self.assertFalse(hosted_contract_path.exists())

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_lineage_values_are_not_nonempty_strings(self) -> None:
        cases = (
            ("frozen_question_id", ""),
            ("selected_direction_id", ""),
            ("selected_question_id", ""),
            ("active_fit_mapping_id", []),
            ("draft_id", ""),
            ("revision_plan_id", []),
        )
        for field, bad_value in cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"bad-lineage-value-{field}.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["lineage"][field] = bad_value
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
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
                    self.assertIn(f"final package lineage.{field} 非法", payload["error"])
                    self.assertFalse(hosted_contract_path.exists())

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

    def test_build_hosted_contract_bundle_fails_closed_when_existing_execution_identity_program_id_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
            hosted_contract_path.write_text(
                json.dumps(
                    {
                        "bundle_kind": "hosted_contract_bundle",
                        "execution_identity": {
                            "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
                            "workspace_id": "nsfc-demo-001",
                            "draft_id": "draft-v1",
                            "program_id": "other-program",
                        },
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
            self.assertIn("other-program", payload["error"])
            self.assertIn("med-autogrant-mainline", payload["error"])

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


class HostedContractBundleControlPlaneResolutionTest(unittest.TestCase):
    def test_resolve_control_plane_current_program_path_prefers_local_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir) / "repo-root"
            current_program_path = repo_root / ".omx" / "context" / "CURRENT_PROGRAM.md"
            current_program_path.parent.mkdir(parents=True, exist_ok=True)
            current_program_path.write_text("- program_id: `local-program`\n", encoding="utf-8")

            resolved_path = hosted_contract_bundle_module._resolve_control_plane_current_program_path(
                repo_root=repo_root,
            )

            self.assertEqual(resolved_path, current_program_path.resolve())

    def test_resolve_control_plane_current_program_path_falls_back_to_unique_main_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            feature_worktree = Path(tmp_dir) / "feature-worktree"
            feature_worktree.mkdir(parents=True, exist_ok=True)
            main_worktree = Path(tmp_dir) / "root-main"
            current_program_path = main_worktree / ".omx" / "context" / "CURRENT_PROGRAM.md"
            current_program_path.parent.mkdir(parents=True, exist_ok=True)
            current_program_path.write_text("- program_id: `root-program`\n", encoding="utf-8")

            worktree_list_text = "\n".join(
                (
                    f"worktree {feature_worktree}",
                    "HEAD 1111111111111111111111111111111111111111",
                    "branch refs/heads/post-r5a-local-runtime-hardening-20260410-a",
                    f"worktree {main_worktree}",
                    "HEAD 2222222222222222222222222222222222222222",
                    "branch refs/heads/main",
                )
            )

            resolved_path = hosted_contract_bundle_module._resolve_control_plane_current_program_path(
                repo_root=feature_worktree,
                worktree_list_text=worktree_list_text,
            )

            self.assertEqual(resolved_path, current_program_path.resolve())

    def test_resolve_control_plane_current_program_path_fails_closed_without_main_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            feature_worktree = Path(tmp_dir) / "feature-worktree"
            feature_worktree.mkdir(parents=True, exist_ok=True)
            other_worktree = Path(tmp_dir) / "other-worktree"
            current_program_path = other_worktree / ".omx" / "context" / "CURRENT_PROGRAM.md"
            current_program_path.parent.mkdir(parents=True, exist_ok=True)
            current_program_path.write_text("- program_id: `other-program`\n", encoding="utf-8")

            worktree_list_text = "\n".join(
                (
                    f"worktree {feature_worktree}",
                    "HEAD 1111111111111111111111111111111111111111",
                    "branch refs/heads/post-r5a-local-runtime-hardening-20260410-a",
                    f"worktree {other_worktree}",
                    "HEAD 2222222222222222222222222222222222222222",
                    "branch refs/heads/release-candidate",
                )
            )

            with self.assertRaisesRegex(
                hosted_contract_bundle_module.WorkspaceFileError,
                "未找到 `refs/heads/main`",
            ):
                hosted_contract_bundle_module._resolve_control_plane_current_program_path(
                    repo_root=feature_worktree,
                    worktree_list_text=worktree_list_text,
                )

    def test_resolve_control_plane_current_program_path_fails_closed_for_ambiguous_main_worktrees(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            feature_worktree = Path(tmp_dir) / "feature-worktree"
            feature_worktree.mkdir(parents=True, exist_ok=True)
            main_one = Path(tmp_dir) / "root-main-1"
            main_two = Path(tmp_dir) / "root-main-2"
            for main_worktree in (main_one, main_two):
                current_program_path = main_worktree / ".omx" / "context" / "CURRENT_PROGRAM.md"
                current_program_path.parent.mkdir(parents=True, exist_ok=True)
                current_program_path.write_text("- program_id: `root-program`\n", encoding="utf-8")

            worktree_list_text = "\n".join(
                (
                    f"worktree {feature_worktree}",
                    "HEAD 1111111111111111111111111111111111111111",
                    "branch refs/heads/post-r5a-local-runtime-hardening-20260410-a",
                    f"worktree {main_one}",
                    "HEAD 2222222222222222222222222222222222222222",
                    "branch refs/heads/main",
                    f"worktree {main_two}",
                    "HEAD 3333333333333333333333333333333333333333",
                    "branch refs/heads/main",
                )
            )

            with self.assertRaisesRegex(
                hosted_contract_bundle_module.WorkspaceStateError,
                "多个 `refs/heads/main` worktree",
            ):
                hosted_contract_bundle_module._resolve_control_plane_current_program_path(
                    repo_root=feature_worktree,
                    worktree_list_text=worktree_list_text,
                )


if __name__ == "__main__":
    unittest.main()
