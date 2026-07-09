from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from support.hosted_contract_bundle import (  # noqa: E402
    assert_hosted_contract_bundle_cli_failure,
    build_final_package,
    run_hosted_contract_bundle_cli,
)


FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"


class HostedContractBundleCheckpointCasesTest(unittest.TestCase):
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
                    build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["freeze_manifest"][field] = bad_value
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    result = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)
                    assert_hosted_contract_bundle_cli_failure(
                        self,
                        result,
                        hosted_contract_path,
                        f"final package freeze_manifest.{field} 非法",
                    )

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
                    build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["checkpoint_summary"].pop(field)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    result = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)
                    assert_hosted_contract_bundle_cli_failure(
                        self,
                        result,
                        hosted_contract_path,
                        "final package checkpoint_summary 缺少字段",
                        field,
                    )

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
                    build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    final_package["lineage"].pop(field)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    result = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)
                    assert_hosted_contract_bundle_cli_failure(
                        self,
                        result,
                        hosted_contract_path,
                        "final package lineage 缺少字段",
                        field,
                    )

    def test_build_hosted_contract_bundle_fails_closed_when_checkpoint_status_values_are_invalid(self) -> None:
        cases = (
            (
                "bad-draft-status",
                lambda final_package: final_package["freeze_manifest"].__setitem__("draft_status", "draft"),
                "final package freeze_manifest.draft_status 非法",
                "draft",
            ),
            (
                "bad-freeze-manifest-checkpoint-status",
                lambda final_package: final_package["freeze_manifest"].__setitem__(
                    "checkpoint_status", "forward_progress"
                ),
                "final package freeze_manifest.checkpoint_status 非法",
                "forward_progress",
            ),
            (
                "bad-checkpoint-summary-checkpoint-status",
                lambda final_package: final_package["checkpoint_summary"].__setitem__(
                    "checkpoint_status", "forward_progress"
                ),
                "final package checkpoint_summary.checkpoint_status 非法",
                "forward_progress",
            ),
        )
        for name, mutate, expected_error, bad_value in cases:
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    final_package_path = Path(tmp_dir) / f"{name}.json"
                    hosted_contract_path = Path(tmp_dir) / "hosted-contract.json"
                    build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    mutate(final_package)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    result = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)
                    assert_hosted_contract_bundle_cli_failure(
                        self,
                        result,
                        hosted_contract_path,
                        expected_error,
                        bad_value,
                    )

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
                    build_final_package(self, FROZEN_EXAMPLE_PATH, final_package_path)
                    final_package = json.loads(final_package_path.read_text(encoding="utf-8"))
                    mutate(final_package)
                    final_package_path.write_text(
                        json.dumps(final_package, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                    result = run_hosted_contract_bundle_cli(final_package_path, hosted_contract_path)
                    assert_hosted_contract_bundle_cli_failure(
                        self,
                        result,
                        hosted_contract_path,
                        expected_error,
                    )


if __name__ == "__main__":
    unittest.main()
