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


class TestFinalPackageOutputIdentityCases(FinalPackageCliCase):
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
            self.assertIn("final package output identity 不匹配", payload["error"])


