from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from support.hosted_contract_bundle import (  # noqa: E402
    assert_hosted_contract_bundle_cli_failure,
    assert_hosted_contract_bundle_contract,
    build_final_package,
    current_runtime_owner,
    run_hosted_contract_bundle_cli,
)


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"


class HostedContractBundleCliTest(unittest.TestCase):
    def test_build_hosted_contract_bundle_writes_expected_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)

            exit_code, stdout, stderr = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)

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
            assert_hosted_contract_bundle_contract(
                self,
                contract_bundle,
                current_runtime_owner=current_runtime_owner(CURRENT_PROGRAM_CONTRACT),
            )
            self.assertEqual(json.loads(hosted_contract_path.read_text(encoding="utf-8")), contract_bundle)

    def test_build_hosted_contract_bundle_fails_closed_on_invalid_hosted_contract_shape(self) -> None:
        from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime
        from med_autogrant.workspace import WorkspaceStateError

        runtime = MagDomainRuntime()
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)

            with patch(
                "med_autogrant.domain_runtime_parts.package_surface.build_hosted_contract_bundle_document",
                return_value={
                    "contract_version": 1,
                    "bundle_kind": "hosted_contract_bundle",
                },
            ):
                with self.assertRaises(WorkspaceStateError):
                    runtime.build_hosted_contract_bundle(
                        final_package_path=str(final_package_path),
                        output_path=str(hosted_contract_path),
                    )

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

            result = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)
            assert_hosted_contract_bundle_cli_failure(self, result, hosted_contract_path, "final package kind 非法")

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
                    build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["freeze_manifest"].pop(field)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    result = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)
                    assert_hosted_contract_bundle_cli_failure(
                        self,
                        result,
                        hosted_contract_path,
                        "final package freeze_manifest 缺少字段",
                        field,
                    )

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
                    build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["lineage"][field] = bad_value
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    result = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)
                    assert_hosted_contract_bundle_cli_failure(
                        self,
                        result,
                        hosted_contract_path,
                        f"final package lineage.{field} 非法",
                    )

    def test_build_hosted_contract_bundle_fails_closed_when_existing_output_identity_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)
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

            exit_code, stdout, stderr = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("hosted contract output identity 不匹配", payload["error"])

    def test_build_hosted_contract_bundle_allows_overwrite_for_same_identity_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            final_package_path = Path(tmp_dir) / "final-package.json"
            hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
            build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)

            first_exit, first_stdout, first_stderr = run_hosted_contract_bundle_cli(
                final_package_path,
                hosted_contract_path,
            )
            self.assertEqual(first_exit, 0)
            self.assertEqual(first_stderr, "")
            first_payload = json.loads(first_stdout)
            self.assertTrue(first_payload["ok"])

            second_exit, second_stdout, second_stderr = run_hosted_contract_bundle_cli(
                final_package_path,
                hosted_contract_path,
            )

            self.assertEqual(second_exit, 0)
            self.assertEqual(second_stderr, "")
            second_payload = json.loads(second_stdout)
            self.assertTrue(second_payload["ok"])
            self.assertEqual(
                json.loads(hosted_contract_path.read_text(encoding="utf-8")),
                second_payload["hosted_contract_bundle"],
            )


if __name__ == "__main__":
    unittest.main()
