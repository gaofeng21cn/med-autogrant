from __future__ import annotations

import tempfile
from pathlib import Path

from .context import FREEZE_READY_EXAMPLE_PATH, FinalPackageCliCase


class TestFinalPackageOutputIdentityCases(FinalPackageCliCase):
    def test_build_final_package_fails_closed_when_existing_output_identity_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            bundle_path = Path(tmp_dir) / "bundle.json"
            package_path = Path(tmp_dir) / "package.json"
            self._build_bundle(FREEZE_READY_EXAMPLE_PATH, bundle_path)
            self._write_json(
                package_path,
                {
                    "grant_run_id": "other-run",
                    "workspace_id": "other-workspace",
                    "draft_id": "other-draft",
                },
            )

            self._assert_final_package_fails(
                FREEZE_READY_EXAMPLE_PATH,
                bundle_path,
                package_path,
                "final package output identity 不匹配",
                assert_package_absent=False,
            )

