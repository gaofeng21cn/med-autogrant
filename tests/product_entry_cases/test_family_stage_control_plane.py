from __future__ import annotations

import unittest

from med_autogrant.product_entry_parts import MedAutoGrantProductEntry
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


def _assert_required_field_path(test_case: unittest.TestCase, payload: dict[str, object], path: str) -> None:
    current: object = payload
    for part in path.split("."):
        test_case.assertIsInstance(current, dict, path)
        test_case.assertIn(part, current, path)
        current = current[part]  # type: ignore[index]


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
                for required_field in required_stage_fields:
                    _assert_required_field_path(self, stage, required_field)
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
                self.assertTrue(stage["stage_contract"]["source_scope_refs"])
                self.assertTrue(stage["stage_contract"]["cohort_query_refs"])
                self.assertTrue(stage["stage_contract"]["trigger_refs"])
                self.assertTrue(stage["stage_contract"]["monitor_refs"])
                self.assertTrue(stage["stage_contract"]["dashboard_metric_refs"])
                self.assertTrue(stage["stage_contract"]["expected_receipt_refs"])
                self.assertTrue(stage["stage_contract"]["monitor_freshness_refs"])
                self.assertTrue(stage["stage_contract"]["replay_evidence_refs"])
                self.assertTrue(stage["stage_contract"]["stage_production_evidence_refs"])
                admission_packet = stage["stage_contract"]["stage_admission_packet"]
                self.assertEqual(admission_packet["surface_kind"], "mag_stage_admission_packet")
                self.assertEqual(admission_packet["stage_id"], stage["stage_id"])
                self.assertEqual(admission_packet["expected_grant_delta"]["owner"], "med-autogrant")
                self.assertEqual(
                    admission_packet["expected_grant_delta"]["domain_stage_refs"],
                    stage["domain_stage_refs"],
                )
                self.assertEqual(
                    admission_packet["closeout_target"]["accepted_return_shapes"],
                    [
                        "domain_owner_receipt_ref",
                        "typed_blocker_ref",
                        "no_regression_evidence_ref",
                    ],
                )
                self.assertEqual(
                    admission_packet["human_gate"]["gate_id"],
                    "submission_ready_export_gate",
                )
                self.assertEqual(
                    admission_packet["human_gate"]["required"],
                    stage["stage_id"] == "package_and_submit_ready",
                )
                self.assertEqual(admission_packet["blocker_budget"]["repeat_budget"], 2)
                self.assertEqual(admission_packet["blocker_budget"]["escalation_owner"], "med-autogrant")
                self.assertTrue(
                    any(
                        ref["role"] == "opl_provider_stage_launch_trigger"
                        for ref in stage["stage_contract"]["trigger_refs"]
                    )
                )
                expected_receipt = stage["stage_contract"]["expected_receipt_refs"][0]
                replay_refs_by_role = {
                    ref["role"]: ref
                    for ref in stage["stage_contract"]["replay_evidence_refs"]
                }
                self.assertEqual(expected_receipt["owner"], "med-autogrant")
                self.assertEqual(
                    expected_receipt["required_return_shapes"],
                    [
                        "domain_owner_receipt_ref",
                        "typed_blocker_ref",
                        "no_regression_evidence_ref",
                    ],
                )
                self.assertTrue(expected_receipt["body_free_payload_required"])
                self.assertEqual(
                    replay_refs_by_role["recorded_runtime_event_ref"]["ref"],
                    expected_receipt["runtime_event_refs"][0],
                )
                self.assertEqual(
                    replay_refs_by_role["stage_closeout_receipt_ref"]["ref"],
                    expected_receipt["ref"],
                )
                monitor_roles = {ref["role"] for ref in stage["stage_contract"]["monitor_refs"]}
                self.assertIn("stage_replay_monitor", monitor_roles)
                self.assertIn("stage_owner_receipt_handoff_monitor", monitor_roles)
                self.assertIn("live_stage_attempt_monitor", monitor_roles)
                self.assertIn("no_forbidden_write_guard_monitor", monitor_roles)
                self.assertIn("direct_hosted_parity_no_regression_monitor", monitor_roles)
                closeout = stage["stage_production_evidence_closeout"]
                self.assertEqual(
                    closeout["surface_kind"],
                    "mag_stage_production_evidence_closeout_refs",
                )
                self.assertEqual(closeout["stage_id"], stage["stage_id"])
                self.assertEqual(
                    closeout["expected_receipt_refs"],
                    stage["stage_contract"]["expected_receipt_refs"],
                )
                self.assertEqual(
                    closeout["monitor_freshness_refs"],
                    stage["stage_contract"]["monitor_freshness_refs"],
                )
                self.assertFalse(closeout["authority_boundary"]["opl_can_sign_owner_receipt"])
                self.assertFalse(closeout["authority_boundary"]["opl_can_write_grant_truth"])
                self.assertFalse(closeout["authority_boundary"]["opl_can_declare_export_ready"])
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
