from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from support.cli import run_cli, run_json_cli  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
FREEZE_READY = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
FROZEN = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
FORWARD = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"


class FinalPackageTest(unittest.TestCase):
    def test_final_package_accepts_only_final_gate_states(self) -> None:
        cases = ((FREEZE_READY, "freeze_ready", "revised"), (FROZEN, "submission_frozen", "frozen"))
        for input_path, checkpoint, draft_status in cases:
            with self.subTest(checkpoint=checkpoint), tempfile.TemporaryDirectory() as tmp_dir:
                bundle_path = Path(tmp_dir) / "bundle.json"
                package_path = Path(tmp_dir) / "final.json"
                self._build_bundle(input_path, bundle_path)
                final_package = self._build_final(input_path, bundle_path, package_path)["final_package"]

                self.assertEqual(final_package["package_kind"], "final_package")
                self.assertEqual(final_package["freeze_manifest"]["checkpoint_status"], checkpoint)
                self.assertEqual(final_package["freeze_manifest"]["draft_status"], draft_status)
                self.assertEqual(final_package["checkpoint_summary"]["checkpoint_status"], checkpoint)
                self.assertEqual(json.loads(package_path.read_text(encoding="utf-8")), final_package)

    def test_nonfinal_checkpoint_and_output_identity_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            bundle_path = tmp_root / "bundle.json"
            package_path = tmp_root / "final.json"
            self._build_bundle(FORWARD, bundle_path)
            self._assert_failure(FORWARD, bundle_path, package_path, "checkpoint_status")

            self._build_bundle(FREEZE_READY, bundle_path)
            existing = {"grant_run_id": "other", "workspace_id": "other", "draft_id": "other"}
            package_path.write_text(json.dumps(existing), encoding="utf-8")
            self._assert_failure(
                FREEZE_READY,
                bundle_path,
                package_path,
                "final package output identity 不匹配",
                package_must_be_absent=False,
            )
            self.assertEqual(json.loads(package_path.read_text(encoding="utf-8")), existing)

    def test_malformed_artifact_bundle_categories_fail_closed(self) -> None:
        cases = (
            ("identity", lambda bundle: bundle.__setitem__("grant_run_id", "other"), "identity 不匹配"),
            ("required", lambda bundle: bundle.pop("manifest"), "缺少必填字段: manifest"),
            ("scalar", lambda bundle: bundle["selection"].__setitem__("selected_direction_id", ""), "selection.selected_direction_id 非法"),
            ("list", lambda bundle: bundle["artifacts"].__setitem__("draft_sections", {}), "artifacts.draft_sections 非法"),
            ("object", lambda bundle: bundle["artifacts"].__setitem__("selected_direction", []), "artifacts.selected_direction 非法"),
            (
                "nested-list",
                lambda bundle: bundle["artifacts"]["draft_outline"][0].__setitem__("linked_object_ids", [None]),
                "linked_object_ids[0] 非法",
            ),
        )
        for name, mutate, error in cases:
            with self.subTest(category=name), tempfile.TemporaryDirectory() as tmp_dir:
                bundle_path = Path(tmp_dir) / "bundle.json"
                package_path = Path(tmp_dir) / "final.json"
                self._build_bundle(FROZEN, bundle_path)
                bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
                mutate(bundle)
                bundle_path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
                self._assert_failure(FROZEN, bundle_path, package_path, error)

    @staticmethod
    def _build_bundle(input_path: Path, output_path: Path) -> None:
        run_json_cli(
            "package", "artifact-bundle", "--input", str(input_path), "--output", str(output_path), "--format", "json"
        )

    @staticmethod
    def _build_final(input_path: Path, bundle_path: Path, package_path: Path) -> dict[str, object]:
        return run_json_cli(
            "package",
            "final-package",
            "--input",
            str(input_path),
            "--artifact-bundle",
            str(bundle_path),
            "--output",
            str(package_path),
            "--format",
            "json",
        )

    def _assert_failure(
        self,
        input_path: Path,
        bundle_path: Path,
        package_path: Path,
        error: str,
        *,
        package_must_be_absent: bool = True,
    ) -> None:
        exit_code, stdout, stderr = run_cli(
            "package",
            "final-package",
            "--input",
            str(input_path),
            "--artifact-bundle",
            str(bundle_path),
            "--output",
            str(package_path),
            "--format",
            "json",
        )
        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        self.assertIn(error, json.loads(stdout)["error"])
        if package_must_be_absent:
            self.assertFalse(package_path.exists())
