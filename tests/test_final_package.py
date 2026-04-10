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
from med_autogrant.route_report import build_stage_route_report  # noqa: E402
from med_autogrant.workspace import load_workspace_document  # noqa: E402


FREEZE_READY_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
FORWARD_PROGRESS_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"


class FinalPackageCliTest(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(list(args))
            except SystemExit as exc:
                exit_code = int(exc.code)
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def test_build_final_package_writes_freeze_ready_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "freeze-ready-bundle.json"
            package_path = Path(tmp_dir) / "freeze-ready-package.json"
            self._build_bundle(FREEZE_READY_EXAMPLE_PATH, bundle_path)

            exit_code, stdout, stderr = self.run_cli(
                "build-final-package",
                "--input",
                str(FREEZE_READY_EXAMPLE_PATH),
                "--artifact-bundle",
                str(bundle_path),
                "--output",
                str(package_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["command"], "build-final-package")
            self.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
            self.assertEqual(payload["workspace_id"], "nsfc-demo-001")
            self.assertEqual(payload["draft_id"], "draft-v1")
            self.assertEqual(payload["lifecycle_stage"], "critique")
            self.assertEqual(payload["output_path"], str(package_path.resolve()))

            final_package = payload["final_package"]
            self.assertEqual(final_package["package_version"], 1)
            self.assertEqual(final_package["package_kind"], "final_package")
            self.assertEqual(
                final_package["freeze_manifest"],
                {
                    "draft_version_label": "v0.4",
                    "draft_status": "revised",
                    "active_revision_plan_id": "revision-v1",
                    "critique_id": "critique-v1",
                    "checkpoint_status": "freeze_ready",
                    "presubmission_frozen": False,
                },
            )
            self.assertEqual(
                final_package["lineage"],
                {
                    "frozen_question_id": "question-immune-fibrosis",
                    "selected_direction_id": "dir-inflammatory-remodeling",
                    "selected_question_id": "question-immune-fibrosis",
                    "active_fit_mapping_id": "fit-001",
                    "draft_id": "draft-v1",
                    "revision_plan_id": "revision-v1",
                },
            )

            route_report = build_stage_route_report(load_workspace_document(FREEZE_READY_EXAMPLE_PATH))
            self.assertEqual(
                final_package["checkpoint_summary"],
                {
                    "verification_checkpoint": route_report["verification_checkpoint"],
                    "checkpoint_status": "freeze_ready",
                },
            )
            self.assertEqual(
                final_package["export_summary"],
                {
                    "outline_count": 2,
                    "section_count": 3,
                    "artifact_count": 6,
                },
            )

            bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
            self.assertEqual(final_package["deliverables"]["artifact_bundle_manifest"], bundle["manifest"])
            self.assertEqual(len(final_package["deliverables"]["final_draft_outline"]), 2)
            self.assertEqual(len(final_package["deliverables"]["final_draft_sections"]), 3)
            self.assertEqual(json.loads(package_path.read_text(encoding="utf-8")), final_package)

    def test_build_final_package_writes_submission_frozen_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "frozen-bundle.json"
            package_path = Path(tmp_dir) / "frozen-package.json"
            self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)

            exit_code, stdout, stderr = self.run_cli(
                "build-final-package",
                "--input",
                str(FROZEN_EXAMPLE_PATH),
                "--artifact-bundle",
                str(bundle_path),
                "--output",
                str(package_path),
                "--format",
                "json",
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr, "")
            payload = json.loads(stdout)
            final_package = payload["final_package"]
            self.assertEqual(final_package["freeze_manifest"]["draft_status"], "frozen")
            self.assertEqual(final_package["freeze_manifest"]["checkpoint_status"], "submission_frozen")
            self.assertTrue(final_package["freeze_manifest"]["presubmission_frozen"])
            self.assertEqual(final_package["checkpoint_summary"]["checkpoint_status"], "submission_frozen")

    def test_build_final_package_fails_closed_when_checkpoint_is_not_final_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "forward-progress-bundle.json"
            package_path = Path(tmp_dir) / "forward-progress-package.json"
            self._build_bundle(FORWARD_PROGRESS_EXAMPLE_PATH, bundle_path)

            exit_code, stdout, stderr = self.run_cli(
                "build-final-package",
                "--input",
                str(FORWARD_PROGRESS_EXAMPLE_PATH),
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
            self.assertIn("checkpoint_status", payload["error"])
            self.assertFalse(package_path.exists())

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
                "build-final-package",
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
                "build-final-package",
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
                "build-final-package",
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
                        "build-final-package",
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
                        "build-final-package",
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
                        "build-final-package",
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

    def test_build_final_package_fails_closed_when_artifact_bundle_artifact_lists_are_not_lists(self) -> None:
        cases = (
            ("draft_outline", {}),
            ("draft_outline", "oops"),
            ("draft_sections", {}),
            ("draft_sections", None),
            ("draft_sections", "oops"),
        )
        for nested_field, bad_value in cases:
            with self.subTest(nested_field=nested_field, bad_value=bad_value):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    bundle_path = Path(tmp_dir) / f"bad-artifacts-{nested_field}.json"
                    package_path = Path(tmp_dir) / "package.json"
                    self._build_bundle(FROZEN_EXAMPLE_PATH, bundle_path)
                    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                    bundle["artifacts"][nested_field] = bad_value
                    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")

                    exit_code, stdout, stderr = self.run_cli(
                        "build-final-package",
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
                    self.assertIn(f"artifact bundle artifacts.{nested_field} 非法", payload["error"])
                    self.assertFalse(package_path.exists())

    def test_build_final_package_fails_closed_when_existing_output_identity_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "bundle.json"
            package_path = Path(tmp_dir) / "package.json"
            self._build_bundle(FREEZE_READY_EXAMPLE_PATH, bundle_path)
            package_path.write_text(
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
                "build-final-package",
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
            self.assertIn("final package output identity 不匹配", payload["error"])

    def _build_bundle(self, input_path: Path, output_path: Path) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "build-artifact-bundle",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])


if __name__ == "__main__":
    unittest.main()
