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


if __name__ == "__main__":
    unittest.main()
