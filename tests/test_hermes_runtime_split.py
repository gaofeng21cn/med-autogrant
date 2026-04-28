from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class HermesRuntimeSplitStructureTest(unittest.TestCase):
    def test_facade_re_exports_split_runtime_helpers(self) -> None:
        from med_autogrant import hermes_runtime
        from med_autogrant.hermes_runtime_parts import runtime_ops

        self.assertIs(
            hermes_runtime._build_autonomy_quality_evaluator_output,
            runtime_ops.build_autonomy_quality_evaluator_output,
        )

    def test_package_builders_do_not_import_runtime_facade(self) -> None:
        package_builders = [
            SRC_ROOT / "med_autogrant" / "artifact_bundle.py",
            SRC_ROOT / "med_autogrant" / "final_package.py",
            SRC_ROOT / "med_autogrant" / "hosted_contract_bundle.py",
            SRC_ROOT / "med_autogrant" / "revision_executor.py",
        ]

        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in package_builders
            if "med_autogrant.hermes_runtime import" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)

    def test_workspace_parts_do_not_import_workspace_facade(self) -> None:
        workspace_parts = [
            SRC_ROOT / "med_autogrant" / "workspace_parts.py",
            SRC_ROOT / "med_autogrant" / "workspace_projection_parts.py",
        ]

        offenders = [
            path.relative_to(REPO_ROOT).as_posix()
            for path in workspace_parts
            if "med_autogrant.workspace import" in path.read_text(encoding="utf-8")
        ]

        self.assertEqual([], offenders)


if __name__ == "__main__":
    unittest.main()
