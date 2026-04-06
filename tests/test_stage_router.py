from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from med_autogrant.stage_router import determine_next_step  # noqa: E402


EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_minimal.json"


class StageRouterTest(unittest.TestCase):
    def load_example(self) -> dict[str, object]:
        return json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))

    def test_major_revision_routes_to_revision(self) -> None:
        route = determine_next_step(self.load_example())

        self.assertEqual(route["current_stage"], "critique")
        self.assertEqual(route["recommended_stage"], "revision")
        self.assertIn("major_revision", route["reason"])
        self.assertIn("执行 revision plan", route["actions"][0])

    def test_major_reframe_routes_back_to_question_refinement(self) -> None:
        document = copy.deepcopy(self.load_example())
        document["mentor_critiques"][0]["verdict"] = "major_reframe"

        route = determine_next_step(document)

        self.assertEqual(route["recommended_stage"], "question_refinement")
        self.assertIn("重塑科学问题", route["reason"])


if __name__ == "__main__":
    unittest.main()
