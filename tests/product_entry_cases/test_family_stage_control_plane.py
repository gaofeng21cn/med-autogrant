from __future__ import annotations

import unittest

from med_autogrant.product_entry_parts import MedAutoGrantProductEntry
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


class FamilyStageControlPlaneTest(unittest.TestCase):
    def test_stage_control_plane_preserves_opl_projection_and_mag_authority(self) -> None:
        manifest = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )["product_entry_manifest"]
        action_catalog = manifest["family_action_catalog"]
        stage_plane = manifest["family_stage_control_plane"]

        self.assertEqual(stage_plane["surface_kind"], "family_stage_control_plane")
        self.assertEqual(stage_plane["version"], "family-stage-control-plane.v1")
        self.assertEqual(stage_plane["plane_id"], "med_autogrant_stage_control_plane")
        self.assertEqual(stage_plane["target_domain_id"], "med-autogrant")
        self.assertEqual(stage_plane["authority_boundary"]["opl_role"], "projection_consumer_only")
        self.assertFalse(stage_plane["authority_boundary"]["can_write_grant_truth"])
        self.assertFalse(stage_plane["authority_boundary"]["can_override_fundability_judgment"])
        self.assertFalse(stage_plane["authority_boundary"]["can_bypass_submission_ready_gate"])
        self.assertEqual(stage_plane["discovery_smoke"]["status"], "ready")
        self.assertEqual(
            stage_plane["discovery_smoke"]["allowed_action_catalog_ref"],
            "/product_entry_manifest/family_action_catalog",
        )
        self.assertEqual(stage_plane["parity"]["status"], "aligned")
        self.assertEqual(
            stage_plane["freshness"]["refresh_policy"],
            "rebuild_product_entry_manifest_before_opl_discovery",
        )
        self.assertIn(
            {
                "ref_kind": "json_pointer",
                "ref": "/product_entry_manifest/family_action_catalog",
                "role": "action_catalog",
            },
            stage_plane["source_refs"],
        )
        self.assertEqual(
            [stage["stage_id"] for stage in stage_plane["stages"]],
            [
                "call_and_candidate_intake",
                "fundability_strategy",
                "specific_aims_and_structure",
                "proposal_authoring",
                "review_and_rebuttal",
                "package_and_submit_ready",
            ],
        )

        action_ids = {action["action_id"] for action in action_catalog["actions"]}
        required_stage_fields = set(stage_plane["discovery_smoke"]["required_stage_fields"])
        expected_next_stage_refs = {
            "call_and_candidate_intake": ["fundability_strategy"],
            "fundability_strategy": ["specific_aims_and_structure"],
            "specific_aims_and_structure": ["proposal_authoring"],
            "proposal_authoring": ["review_and_rebuttal"],
            "review_and_rebuttal": ["package_and_submit_ready"],
            "package_and_submit_ready": [],
        }
        independent_gate_stage_ids = {
            "fundability_strategy",
            "specific_aims_and_structure",
            "review_and_rebuttal",
            "package_and_submit_ready",
        }

        for stage in stage_plane["stages"]:
            with self.subTest(stage=stage["stage_id"]):
                self.assertLessEqual(required_stage_fields, set(stage))
                self.assertEqual(stage["owner"], "med-autogrant")
                self.assertEqual(stage["stage_goal"], stage["goal"])
                self.assertEqual(
                    stage["prompt_refs"],
                    [
                        {
                            "ref_kind": "repo_path",
                            "ref": f"agent/prompts/{stage['stage_id']}.md",
                            "role": "stage_prompt",
                        }
                    ],
                )
                self.assertTrue(set(stage["allowed_action_refs"]) <= action_ids)
                self.assertEqual(stage["handoff"]["shared_handoff_ref"], "/shared_handoff")
                self.assertEqual(
                    stage["handoff"]["next_stage_refs"],
                    expected_next_stage_refs[stage["stage_id"]],
                )
                self.assertEqual(stage["handoff"]["provides"], stage["stage_contract"]["ensures"])
                self.assertTrue(stage["stage_contract"]["requires"])
                self.assertTrue(stage["stage_contract"]["ensures"])
                self.assertTrue(any(ref["role"] == "owner_receipt_gate" for ref in stage["evaluation"]))
                self.assertTrue(stage["trust_boundary"]["owner_receipt_required"])
                self.assertTrue(stage["trust_boundary"]["runtime_guard_required"])
                self.assertEqual(
                    stage["authority_boundary"]["independent_gate_receipt_required"],
                    stage["stage_id"] in independent_gate_stage_ids,
                )
                if stage["stage_id"] in {
                    "fundability_strategy",
                    "specific_aims_and_structure",
                    "review_and_rebuttal",
                }:
                    self.assertEqual(stage["trust_boundary"]["lane"], "ai_decision")
                    self.assertTrue(stage["trust_boundary"]["effect_boundary"])
                self.assertGreaterEqual(len(stage["source_refs"]), 5)
                self.assertEqual(
                    stage["freshness"]["refresh_policy"],
                    "rebuild_product_entry_manifest_before_opl_discovery",
                )
                self.assertFalse(stage["authority_boundary"]["can_write_grant_truth"])
                self.assertFalse(stage["authority_boundary"]["can_override_fundability_judgment"])
                self.assertFalse(stage["authority_boundary"]["can_bypass_submission_ready_gate"])

        proposal_stage = next(
            stage for stage in stage_plane["stages"] if stage["stage_id"] == "proposal_authoring"
        )
        self.assertEqual(proposal_stage["stage_kind"], "creation")
        self.assertEqual(
            proposal_stage["domain_stage_refs"],
            ["drafting", "revision", "grant-progress", "grant-user-loop"],
        )
        self.assertEqual(
            proposal_stage["authority_boundary"]["submission_ready_export_gate_owner"],
            "med-autogrant",
        )


if __name__ == "__main__":
    unittest.main()
