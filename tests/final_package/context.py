from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from support.cli import run_cli  # noqa: E402


FREEZE_READY_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3a_ready_for_submission.json"
FROZEN_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p3c_presubmission_frozen.json"
FORWARD_PROGRESS_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"
REMOVE = object()


class FinalPackageCliCase(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        return run_cli(*args)

    def _read_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_json(self, path: Path, payload: dict) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _build_bundle(self, input_path: Path, output_path: Path) -> None:
        exit_code, stdout, stderr = self.run_cli(
            "package",
            "artifact-bundle",
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

    def _build_final_package(
        self,
        input_path: Path,
        bundle_path: Path,
        package_path: Path,
    ) -> tuple[int, str, str]:
        return self.run_cli(
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

    def _assert_final_package_ok(self, input_path: Path, bundle_path: Path, package_path: Path) -> dict:
        exit_code, stdout, stderr = self._build_final_package(input_path, bundle_path, package_path)
        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertTrue(payload["ok"])
        return payload

    def _assert_final_package_fails(
        self,
        input_path: Path,
        bundle_path: Path,
        package_path: Path,
        *error_snippets: str,
        assert_package_absent: bool = True,
    ) -> dict:
        exit_code, stdout, stderr = self._build_final_package(input_path, bundle_path, package_path)
        self.assertEqual(exit_code, 1)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertFalse(payload["ok"])
        for snippet in error_snippets:
            self.assertIn(snippet, payload["error"])
        if assert_package_absent:
            self.assertFalse(package_path.exists())
        return payload

    def _assert_mutated_bundle_fails(
        self,
        filename: str,
        mutate_bundle,
        *error_snippets: str,
        input_path: Path = FROZEN_EXAMPLE_PATH,
    ) -> dict:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / filename
            package_path = Path(tmp_dir) / "package.json"
            self._build_bundle(input_path, bundle_path)
            bundle = self._read_json(bundle_path)
            mutate_bundle(bundle)
            self._write_json(bundle_path, bundle)
            return self._assert_final_package_fails(input_path, bundle_path, package_path, *error_snippets)

    def _assert_bundle_path_fails(
        self,
        filename: str,
        path: tuple,
        *error_snippets: str,
        bad_value=REMOVE,
        input_path: Path = FROZEN_EXAMPLE_PATH,
    ) -> dict:
        def mutate_bundle(bundle: dict) -> None:
            target = bundle
            for key in path[:-1]:
                target = target[key]
            key = path[-1]
            if bad_value is REMOVE:
                target.pop(key, None)
            else:
                target[key] = bad_value

        return self._assert_mutated_bundle_fails(filename, mutate_bundle, *error_snippets, input_path=input_path)
