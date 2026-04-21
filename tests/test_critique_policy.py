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

    def test_resolve_critique_policy_reads_nsfc_preset_from_project_profile(self) -> None:
        from med_autogrant.critique_policy import resolve_critique_policy_from_document
        from med_autogrant.workspace import load_workspace_document

        document = load_workspace_document(REPO_ROOT / "examples" / "nsfc_workspace_p2c_drafting.json")

        policy = resolve_critique_policy_from_document(document)

        self.assertEqual(policy["policy_id"], "nsfc_mentor_critique_v1")
        self.assertEqual(policy["persona"]["role"], "NSFC mentor reviewer")

    def test_resolve_critique_policy_reads_non_nsfc_preset_from_project_profile(self) -> None:
        from med_autogrant.critique_policy import resolve_critique_policy_from_document
        from med_autogrant.workspace import load_workspace_document

        document = load_workspace_document(REPO_ROOT / "examples" / "nih_r21_workspace_p2a_input_intake.json")

        policy = resolve_critique_policy_from_document(document)

        self.assertEqual(policy["policy_id"], "nih_r21_significance_innovation_v1")
        self.assertEqual(policy["persona"]["role"], "NIH R21 scientific reviewer")


if __name__ == "__main__":
    unittest.main()
