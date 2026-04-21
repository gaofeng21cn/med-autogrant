from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class CritiquePolicyContractTest(unittest.TestCase):
    def test_default_nsfc_policy_exposes_explicit_weight_and_output_contract(self) -> None:
        from med_autogrant.critique_policy import (
            DEFAULT_NSFC_CRITIQUE_POLICY,
            build_weight_contract,
        )

        self.assertEqual(DEFAULT_NSFC_CRITIQUE_POLICY["policy_id"], "nsfc_mentor_critique_v1")
        self.assertEqual(
            build_weight_contract(DEFAULT_NSFC_CRITIQUE_POLICY),
            {
                "necessity_scientific_value": 60,
                "applicant_fit": 30,
                "feasibility": 10,
            },
        )
        self.assertIn(
            "clearly separate scientific question framing from engineering task decomposition",
            DEFAULT_NSFC_CRITIQUE_POLICY["hard_rules"],
        )
        self.assertIn(
            "logic_chain_repairs",
            [item["field"] for item in DEFAULT_NSFC_CRITIQUE_POLICY["required_outputs"]],
        )


if __name__ == "__main__":
    unittest.main()
