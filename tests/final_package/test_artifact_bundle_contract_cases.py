from __future__ import annotations

import json
import tempfile
from pathlib import Path

from .context import (
    FORWARD_PROGRESS_EXAMPLE_PATH,
    FREEZE_READY_EXAMPLE_PATH,
    FROZEN_EXAMPLE_PATH,
    FinalPackageCliCase,
)


class TestFinalPackageArtifactBundleContractCases(FinalPackageCliCase):
    def test_build_final_package_fails_closed_when_artifact_bundle_identity_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "bundle.json"
            package_path = Path(tmp_dir) / "package.json"
            bundle_path.write_text(
                json.dumps(
                    {
                        "bundle_kind": "artifact_bundle",
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
                "package",
                "final-package",
                "--input",
                str(FREEZE_READY_EXAMPLE_PATH),
                "--artifact-bundle",
                str(bundle_path),
                "--output",
                str(package_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("artifact bundle identity 不匹配", payload["error"])

    def test_build_final_package_fails_closed_when_artifact_bundle_manifest_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "missing-manifest-bundle.json"
            package_path = Path(tmp_dir) / "package.json"
            self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
            bundle.pop("manifest")
            bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

            exit_code, stdout, stderr = self.run_cli(
                "package",
                "final-package",
                "--input",
                str(FROZEN_EXAMPLE_PATH),
                "--artifact-bundle",
                str(bundle_path),
                "--output",
                str(package_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("artifact bundle 缺少必填字段", payload["error"])
            self.assertIn("manifest", payload["error"])
            self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_artifacts_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "missing-artifacts-bundle.json"
            package_path = Path(tmp_dir) / "package.json"
            self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
            bundle.pop("artifacts")
            bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

            exit_code, stdout, stderr = self.run_cli(
                "package",
                "final-package",
                "--input",
                str(FROZEN_EXAMPLE_PATH),
                "--artifact-bundle",
                str(bundle_path),
                "--output",
                str(package_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertFalse(payload["ok"])
            self.assertIn("artifact bundle 缺少必填字段", payload["error"])
            self.assertIn("artifacts", payload["error"])
            self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_required_nested_fields_are_missing(self) -> None:
        cases = (
            ("selection", "selected_direction_id"),
            ("selection", "selected_question_id"),
            ("selection", "active_fit_mapping_id"),
            ("selection", "active_draft_id"),
            ("manifest", "direction_id"),
            ("manifest", "question_id"),
            ("manifest", "argument_chain_id"),
            ("manifest", "fit_mapping_id"),
            ("manifest", "draft_id"),
            ("manifest", "draft_version_label"),
            ("manifest", "draft_status"),
            ("lineage", "frozen_question_id"),
            ("lineage", "argument_chain_id"),
            ("lineage", "fit_mapping_id"),
            ("lineage", "draft_id"),
            ("bundle_summary", "outline_count"),
            ("bundle_summary", "section_count"),
            ("artifacts", "selected_direction"),
            ("artifacts", "selected_question"),
            ("artifacts", "argument_chain"),
            ("artifacts", "fit_mapping"),
            ("artifacts", "draft_outline"),
            ("artifacts", "draft_sections"),
        )
        for object_field, nested_field in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"missing-{object_field}-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle[object_field].pop(nested_field)
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "package",
                "final-package",
                "--input",
                        str(FROZEN_EXAMPLE_PATH),
                        "--artifact-bundle",
                        str(bundle_path),
                        "--output",
                        str(package_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"artifact bundle {object_field} 缺少字段", payload["error"])
                    self.assertIn(nested_field, payload["error"])
                    self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_required_scalar_values_are_not_nonempty_strings(self) -> None:
        cases = (
            ("selection", "selected_direction_id", ""),
            ("selection", "selected_question_id", None),
            ("selection", "active_fit_mapping_id", 123),
            ("selection", "active_draft_id", []),
            ("manifest", "direction_id", ""),
            ("manifest", "question_id", False),
            ("manifest", "argument_chain_id", 0),
            ("manifest", "fit_mapping_id", {}),
            ("manifest", "draft_id", []),
            ("manifest", "draft_version_label", None),
            ("manifest", "draft_status", {}),
            ("lineage", "frozen_question_id", ""),
            ("lineage", "argument_chain_id", {}),
            ("lineage", "fit_mapping_id", []),
            ("lineage", "draft_id", 0),
        )
        for object_field, nested_field, bad_value in cases:
            with self.subTest(object_field=object_field, nested_field=nested_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-{object_field}-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle[object_field][nested_field] = bad_value
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "package",
                "final-package",
                "--input",
                        str(FROZEN_EXAMPLE_PATH),
                        "--artifact-bundle",
                        str(bundle_path),
                        "--output",
                        str(package_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"artifact bundle {object_field}.{nested_field} 非法", payload["error"])
                    self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_artifact_bundle_summary_counts_are_not_nonnegative_integers(self) -> None:
        cases = (
            ("outline_count", "2"),
            ("outline_count", -1),
            ("outline_count", False),
            ("section_count", None),
            ("section_count", True),
        )
        for nested_field, bad_value in cases:
            with self.subTest(nested_field=nested_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-bundle-summary-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle["bundle_summary"][nested_field] = bad_value
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "package",
                "final-package",
                "--input",
                        str(FROZEN_EXAMPLE_PATH),
                        "--artifact-bundle",
                        str(bundle_path),
                        "--output",
                        str(package_path),
                        "--format",
                        "json",
                    )

                    self.assertEqual(exit_code, 1)
                    self.assertEqual(stderr, "")
                    payload = json.loads(stdout)
                    self.assertFalse(payload["ok"])
                    self.assertIn(f"artifact bundle bundle_summary.{nested_field} 非法", payload["error"])
                    self.assertFalse(package_path.exists())


