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
from med_autogrant.domain_entry_contract import build_domain_entry_contract  # noqa: E402
from med_autogrant.public_cli import public_cli_argv, public_command_label  # noqa: E402
from med_autogrant import hosted_contract_bundle as hosted_contract_bundle_module  # noqa: E402
from support.domain_contracts import CANONICAL_EXPORT_SURFACES  # noqa: E402


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"

PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND = public_command_label("build-product-entry")



class HostedContractBundleCheckpointCasesTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(public_cli_argv(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_build_hosted_contract_bundle_fails_closed_when_final_package_freeze_manifest_values_are_invalid(self) -> None:
        cases = (
            ("draft_version_label", ""),
            ("active_revision_plan_id", []),
            ("critique_id", ""),
            ("presubmission_frozen", "false"),
        )
        for field, bad_value in cases:
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"bad-freeze-manifest-value-{field}.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    self._build_final_package(FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["freeze_manifest"][field] = bad_value
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
                    self.assertIn(f"final package freeze_manifest.{field} 非法", payload["error"])
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

    def _current_runtime_owner(self) -> dict[str, str]:
        contract = json.loads(CURRENT_PROGRAM_CONTRACT.read_text(encoding="utf-8"))
        return contract["runtime_owner"]


if __name__ == "__main__":
    unittest.main()
