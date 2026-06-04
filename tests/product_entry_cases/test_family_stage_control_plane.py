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
        expected_stage_output_roles = {
            "call_and_candidate_intake": "call_candidate_intake_manifest_ref",
            "fundability_strategy": "fundability_strategy_owner_receipt_ref",
            "specific_aims_and_structure": "specific_aims_structure_manifest_ref",
            "proposal_authoring": "reviewable_grant_artifact_bundle_ref",
            "review_and_rebuttal": "review_quality_closure_receipt_ref",
            "package_and_submit_ready": "submission_ready_package_manifest_ref",
        }
        independent_gate_stage_ids = {
            "fundability_strategy",
            "specific_aims_and_structure",
            "review_and_rebuttal",
            "package_and_submit_ready",
        }
        default_executor_stage_ids = [
            stage["stage_id"]
            for stage in stage_plane["stages"]
            if stage["selected_executor"]["default_executor"] is True
        ]
        self.assertEqual(default_executor_stage_ids, ["call_and_candidate_intake"])

        for stage in stage_plane["stages"]:
            with self.subTest(stage=stage["stage_id"]):
                for required_field in required_stage_fields:
                    _assert_required_field_path(self, stage, required_field)
                self.assertEqual(stage["owner"], "med-autogrant")
                self.assertEqual(stage["stage_goal"], stage["goal"])
                self.assertEqual(stage["selected_executor"]["executor_kind"], "codex_cli")
                self.assertEqual(stage["selected_executor"]["executor_binding_ref"], "default_codex_cli")
                self.assertEqual(
                    stage["selected_executor"]["default_executor"],
                    stage["stage_id"] == "call_and_candidate_intake",
                )
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
                progress_delta_policy = stage["stage_contract"]["progress_delta_policy"]
                self.assertEqual(progress_delta_policy["surface_kind"], "opl_stage_progress_delta_policy")
                self.assertTrue(
                    {
                        "progress_delta_classification",
                        "deliverable_progress_delta",
                        "platform_repair_delta",
                        "next_forced_delta",
                    }
                    <= set(progress_delta_policy["required_fields"])
                )
                self.assertEqual(
                    progress_delta_policy["deliverable_delta_aliases"]["grant_work_progress"],
                    "deliverable_progress_delta",
                )
                self.assertEqual(
                    progress_delta_policy["platform_delta_aliases"]["platform_evidence_progress"],
                    "platform_repair_delta",
                )
                self.assertTrue(progress_delta_policy["platform_only_is_not_deliverable_progress"])
                typed_blocker_lineage_policy = stage["stage_contract"]["typed_blocker_lineage_policy"]
                self.assertEqual(typed_blocker_lineage_policy["surface_kind"], "family-stall-lineage.v1")
                self.assertTrue(
                    {
                        "blocker_family",
                        "repeat_count",
                        "next_forced_delta",
                        "escalation_owner",
                    }
                    <= set(typed_blocker_lineage_policy["required_fields"])
                )
                self.assertEqual(
                    typed_blocker_lineage_policy["repeat_budget"],
                    {
                        "mechanism_repair_after_repeat_count": 2,
                        "human_gate_or_stop_loss_after_repeat_count": 3,
                    },
                )
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
                stage_native_artifact_contract = stage["stage_contract"]["stage_native_artifact_contract"]
                expected_stage_output_role = expected_stage_output_roles[stage["stage_id"]]
                self.assertEqual(
                    stage_native_artifact_contract["surface_kind"],
                    "mag_stage_native_artifact_contract",
                )
                self.assertEqual(stage_native_artifact_contract["owner"], "med-autogrant")
                self.assertEqual(stage_native_artifact_contract["stage_id"], stage["stage_id"])
                self.assertEqual(
                    stage_native_artifact_contract["required_output_roles"],
                    [expected_stage_output_role],
                )
                self.assertIn(
                    {
                        "ref_kind": "stage_output_role",
                        "ref": expected_stage_output_role,
                        "role": "stage_native_artifact_output_role",
                    },
                    stage["outputs"],
                )
                manifest_requirements = stage_native_artifact_contract["manifest_requirements"]
                self.assertTrue(manifest_requirements["body_free_projection_required"])
                self.assertTrue(
                    {
                        "stage_id",
                        "stage_output_role",
                        "lifecycle_contract_role",
                        "artifact_classification",
                        "manifest_ref",
                        "current_pointer_ref",
                        "owner_receipt_or_typed_blocker_ref",
                    }
                    <= set(manifest_requirements["required_fields"])
                )
                self.assertIn("stage_output_role", manifest_requirements["identity_fields"])
                self.assertEqual(
                    stage_native_artifact_contract["stage_folder_lifecycle_contract"],
                    {
                        "artifact_bundle_role": "stage_output_artifact_ref",
                        "artifact_bundle_output_role": expected_stage_output_role,
                        "artifact_bundle_manifest_required": True,
                        "artifact_bundle_owner_receipt_or_typed_blocker_required": True,
                        "physical_kernel_locator_roles": [
                            "stage_json_ref",
                            "attempt_json_ref",
                            "manifest_json_ref",
                            "receipt_json_ref",
                            "current_json_ref",
                            "latest_json_ref",
                            "canonical_pointer_ref",
                            "export_artifact_ref",
                            "lineage_events_ref",
                            "lineage_graph_ref",
                            "retention_policy_ref",
                            "conformance_summary_ref",
                        ],
                        "conformance_required": True,
                        "opl_consumption": "refs_manifest_missing_output_receipt_blocker_handoff_only",
                        "opl_can_interpret_grant_quality": False,
                    },
                )
                physical_kernel = stage_native_artifact_contract["physical_stage_folder_kernel"]
                self.assertEqual(
                    physical_kernel["maps_to_opl_contract"],
                    "opl_stage_artifact_runtime_contract.v1",
                )
                self.assertEqual(
                    physical_kernel["stage_output_role"],
                    expected_stage_output_role,
                )
                self.assertIn("stage.json", physical_kernel["required_attempt_entries"])
                self.assertIn("attempt.json", physical_kernel["required_attempt_entries"])
                self.assertIn("manifest.json", physical_kernel["required_attempt_entries"])
                self.assertIn("receipts/receipt.json", physical_kernel["required_attempt_entries"])
                self.assertIn("current_json_ref", physical_kernel["required_physical_locator_roles"])
                self.assertIn("lineage_events_ref", physical_kernel["required_physical_locator_roles"])
                self.assertIn("retention_policy_ref", physical_kernel["required_physical_locator_roles"])
                self.assertFalse(physical_kernel["conformance_refs"]["domain_readiness_claim"])
                self.assertFalse(
                    physical_kernel["authority_boundary"]["opl_can_create_mag_owner_receipt"]
                )
                self.assertFalse(
                    physical_kernel["authority_boundary"]["opl_can_interpret_grant_quality"]
                )
                verdict_policy = stage_native_artifact_contract["owner_verdict_signature_policy"]
                self.assertEqual(verdict_policy["owner"], "med-autogrant")
                self.assertEqual(
                    verdict_policy["required_verdicts"],
                    [
                        "fundability_verdict",
                        "authoring_quality_verdict",
                        "export_verdict",
                        "submission_ready_verdict",
                    ],
                )
                self.assertEqual(
                    verdict_policy["accepted_signature_shapes"],
                    [
                        "mag_owner_receipt_ref",
                        "mag_owned_typed_blocker_ref",
                    ],
                )
                self.assertFalse(verdict_policy["opl_can_sign_or_infer_verdict"])
                owner_closeout_requirements = stage_native_artifact_contract[
                    "owner_closeout_requirements"
                ]
                self.assertEqual(
                    owner_closeout_requirements["accepted_return_shapes"],
                    [
                        "domain_owner_receipt_ref",
                        "typed_blocker_ref",
                        "no_regression_evidence_ref",
                    ],
                )
                self.assertEqual(
                    owner_closeout_requirements["expected_receipt_refs"],
                    stage["stage_contract"]["expected_receipt_refs"],
                )
                self.assertTrue(owner_closeout_requirements["typed_blocker_required_when_output_missing"])
                self.assertTrue(
                    owner_closeout_requirements["owner_receipt_required_for_current_pointer_advance"]
                )
                self.assertTrue(owner_closeout_requirements["provider_completion_is_not_owner_closeout"])
                current_pointer_rules = stage_native_artifact_contract["current_pointer_rules"]
                self.assertEqual(current_pointer_rules["pointer_owner"], "med-autogrant")
                self.assertEqual(
                    current_pointer_rules["pointer_ref_template"],
                    f"current:mag/stages/{stage['stage_id']}/{expected_stage_output_role}",
                )
                self.assertFalse(current_pointer_rules["opl_can_advance_pointer"])
                self.assertEqual(
                    current_pointer_rules["missing_pointer_policy"],
                    "typed_blocker_no_opl_inference",
                )
                classification_boundary = stage_native_artifact_contract[
                    "artifact_classification_boundary"
                ]
                self.assertEqual(classification_boundary["classification"], "grant_stage_output_ref")
                self.assertEqual(classification_boundary["artifact_body_owner"], "med-autogrant")
                self.assertFalse(classification_boundary["opl_can_read_artifact_body"])
                self.assertFalse(classification_boundary["opl_can_write_artifact_body"])
                self.assertFalse(classification_boundary["opl_can_declare_fundability_ready"])
                self.assertFalse(classification_boundary["opl_can_declare_quality_ready"])
                self.assertFalse(classification_boundary["opl_can_declare_export_ready"])
                self.assertFalse(classification_boundary["opl_can_declare_submission_ready"])
                self.assertEqual(
                    classification_boundary["opl_consumes"],
                    [
                        "stage_output_role",
                        "lifecycle_contract_role",
                        "manifest_ref",
                        "current_pointer_ref",
                        "owner_receipt_or_typed_blocker_ref",
                        "missing_output_ref",
                        "handoff_ref",
                    ],
                )
                if stage["stage_id"] == "package_and_submit_ready":
                    package_projection = stage_native_artifact_contract[
                        "package_stage_lifecycle_projection"
                    ]
                    self.assertEqual(package_projection["stage_id"], "package_and_submit_ready")
                    self.assertEqual(
                        package_projection["artifact_bundle"]["lifecycle_contract_role"],
                        "stage_output_artifact_ref",
                    )
                    self.assertEqual(
                        package_projection["artifact_bundle"]["stage_output_role"],
                        "submission_ready_package_manifest_ref",
                    )
                    self.assertEqual(
                        package_projection["final_package"]["lifecycle_contract_role"],
                        "canonical_promotion_ref",
                    )
                    self.assertEqual(
                        package_projection["final_package"]["physical_locator_role"],
                        "canonical_pointer_ref",
                    )
                    self.assertEqual(
                        package_projection["final_package"]["canonical_ref_template"],
                        "mag-package://final-package/{grant_run_id}/{workspace_id}/{draft_id}",
                    )
                    self.assertEqual(
                        package_projection["submission_ready_package"]["lifecycle_contract_role"],
                        "export_artifact_ref",
                    )
                    self.assertEqual(
                        package_projection["submission_ready_package"]["physical_locator_role"],
                        "export_artifact_ref",
                    )
                    self.assertEqual(
                        package_projection["submission_ready_package"]["export_ref_template"],
                        "mag-package://submission-ready/{grant_run_id}/{workspace_id}/{draft_id}",
                    )
                    self.assertTrue(
                        package_projection["physical_kernel_handoff_requirements"][
                            "conformance_summary_required"
                        ]
                    )
                    self.assertEqual(
                        package_projection["owner_receipt_or_typed_blocker_ref"],
                        "receipt:mag/grant-stage-controlled-attempt/package_and_submit_ready/owner-receipt-or-typed-blocker",
                    )
                    self.assertEqual(
                        package_projection["missing_output_policy"],
                        "typed_blocker_required_no_opl_inference",
                    )
                    self.assertFalse(
                        package_projection["authority_boundary"]["opl_can_interpret_grant_quality"]
                    )
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
