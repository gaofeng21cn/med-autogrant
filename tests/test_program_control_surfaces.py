from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"
RUNTIME_STATE_ROOT = "$CODEX_HOME/projects/med-autogrant/runtime-state/"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ProgramControlSurfaceTest(unittest.TestCase):
    def test_current_program_contract_tracks_repo_truth_and_runtime_state_boundary(self) -> None:
        contract = json.loads(_read(CURRENT_PROGRAM_CONTRACT))

        self.assertEqual(contract["program_id"], "med-autogrant-mainline")
        self.assertEqual(contract["formal_entry"]["default_formal_entry"], "CLI")
        self.assertEqual(contract["formal_entry"]["supported_protocol_layer"], ["MCP"])
        self.assertEqual(contract["formal_entry"]["internal_controller_surface"], "controller")
        self.assertEqual(
            contract["runtime_owner"]["current_owner_line"],
            "CLI/domain-entry stable capability surface with Codex-default execution and optional hosted runtime carriers",
        )
        self.assertEqual(contract["runtime_owner"]["active_phase"], "P4 mature direct grant product entry")
        self.assertEqual(
            contract["runtime_owner"]["active_tranche"],
            "P4.G authoring-quality-first completion semantics alignment",
        )
        framework_boundary = contract["runtime_owner"]["stage_led_framework_boundary"]
        self.assertEqual(
            framework_boundary["framework"],
            "OPL Codex-first stage-led agent runtime framework",
        )
        self.assertIn("queue", framework_boundary["layer_role"])
        self.assertIn("handoff", framework_boundary["layer_role"])
        self.assertIn("operator projection", framework_boundary["layer_role"])
        self.assertIn("external provider orchestration", framework_boundary["layer_role"])
        self.assertIn("author-side route truth", framework_boundary["mag_owned_truth"])
        self.assertIn("submission-ready export gate", framework_boundary["mag_owned_truth"])
        self.assertIn(
            "runtime_control.semantic_closure",
            framework_boundary["framework_consumed_projection"],
        )
        self.assertIn(
            "skill_catalog.domain_projection.opl_stage_runtime_registration",
            framework_boundary["framework_consumed_projection"],
        )
        self.assertIn(
            "skill_catalog.domain_projection.opl_stage_runtime_registration.family_lifecycle_adapter",
            framework_boundary["framework_consumed_projection"],
        )
        self.assertIn(
            "skill_catalog.domain_projection.opl_stage_runtime_registration.native_helper_consumption.proof_surface",
            framework_boundary["framework_consumed_projection"],
        )
        self.assertIn(
            "skill_catalog.domain_projection.standard_domain_agent_skeleton",
            framework_boundary["framework_consumed_projection"],
        )
        self.assertIn(
            "opl_substrate_adapter_export",
            framework_boundary["framework_consumed_projection"],
        )
        self.assertIn(
            "controlled stage attempt projection and sidecar receipt refs",
            framework_boundary["framework_consumed_projection"],
        )
        self.assertIn("owner_receipt_contract", framework_boundary["framework_consumed_projection"])
        self.assertIn("owner_receipt_runtime_evidence", framework_boundary["framework_consumed_projection"])
        self.assertIn("lifecycle_guarded_apply_proof", framework_boundary["framework_consumed_projection"])
        self.assertIn("lifecycle_receipt_runtime_evidence", framework_boundary["framework_consumed_projection"])
        self.assertIn("physical_skeleton_follow_through", framework_boundary["framework_consumed_projection"])
        self.assertIn("ideal_state_closure_status", framework_boundary["framework_consumed_projection"])
        skeleton = framework_boundary["standard_domain_agent_skeleton"]
        self.assertEqual(skeleton["skeleton_id"], "mag.standard_domain_agent_skeleton.v1")
        self.assertEqual(skeleton["repo_source_boundary"], ["agent", "contracts", "runtime", "docs"])
        self.assertEqual(
            skeleton["runtime_declares_only"],
            ["sidecar", "projection_builder", "lifecycle_adapter", "receipt_evidence_writer"],
        )
        self.assertEqual(skeleton["artifact_locator_ref"], "/product_entry_manifest/artifact_locator_contract")
        self.assertEqual(
            skeleton["controlled_stage_attempt_ref"],
            "/product_entry_manifest/controlled_stage_attempt_projection",
        )
        self.assertEqual(
            skeleton["controlled_domain_memory_apply_proof_ref"],
            "/product_entry_manifest/controlled_domain_memory_apply_proof",
        )
        self.assertEqual(
            skeleton["opl_substrate_adapter_export_ref"],
            "/product_entry_manifest/opl_substrate_adapter_export",
        )
        self.assertEqual(
            skeleton["owner_receipt_contract_ref"],
            "/product_entry_manifest/owner_receipt_contract",
        )
        self.assertEqual(
            skeleton["lifecycle_guarded_apply_proof_ref"],
            "/product_entry_manifest/lifecycle_guarded_apply_proof",
        )
        self.assertEqual(
            skeleton["physical_skeleton_follow_through_ref"],
            "/product_entry_manifest/physical_skeleton_follow_through",
        )
        self.assertEqual(
            skeleton["ideal_state_closure_status_ref"],
            "/product_entry_manifest/ideal_state_closure_status",
        )
        self.assertEqual(
            skeleton["repo_source_layout_audit_ref"],
            "/product_entry_manifest/controlled_domain_memory_apply_proof/repo_source_layout_audit",
        )
        self.assertFalse(skeleton["opl_verdict_authority"]["fundability"])
        self.assertFalse(skeleton["opl_verdict_authority"]["submission_ready_export"])
        self.assertEqual(
            framework_boundary["product_sidecar_adapter"]["adapter_id"],
            "mag.opl_stage_led.product_sidecar.v1",
        )
        self.assertIn(
            "grant-domain truth owner",
            framework_boundary["framework_non_goals"],
        )
        self.assertIn("fundability judgment owner", framework_boundary["framework_non_goals"])
        self.assertIn("authoring quality verdict owner", framework_boundary["framework_non_goals"])
        self.assertIn("submission-ready export authority", framework_boundary["framework_non_goals"])
        self.assertEqual(contract["executor_defaults"]["default_executor_name"], "codex_cli")
        self.assertEqual(contract["executor_defaults"]["default_executor_mode"], "autonomous")
        self.assertEqual(contract["executor_defaults"]["default_model"], "inherit_local_codex_default")
        self.assertEqual(
            contract["executor_defaults"]["default_reasoning_effort"],
            "inherit_local_codex_default",
        )
        self.assertEqual(
            contract["executor_defaults"]["canonical_executor_backends"],
            ["codex_cli", "hermes_agent", "claude_code"],
        )
        self.assertEqual(
            contract["executor_defaults"]["executor_registry"],
            {
                "surface_kind": "opl_agent_executor_registry",
                "request_contract": "AgentExecutionRequest",
                "receipt_contract": "AgentExecutionReceipt",
                "default_resolution_order": [
                    "cli_flag",
                    "stage_attempt_input",
                    "OPL_EXECUTOR_KIND",
                    "codex_cli",
                ],
                "non_default_equivalence": "connectivity_lifecycle_receipt_audit_only",
            },
        )
        self.assertEqual(
            contract["executor_defaults"]["executor_labels"],
            {
                "codex_cli": "Codex CLI",
                "hermes_agent": "Hermes-Agent",
                "claude_code": "Claude Code",
            },
        )
        self.assertEqual(
            contract["executor_defaults"]["executor_statuses"],
            {
                "codex_cli": "default",
                "hermes_agent": "experimental",
                "claude_code": "experimental",
            },
        )
        self.assertTrue(contract["executor_defaults"]["chat_completion_only_executor_forbidden"])
        self.assertTrue(contract["executor_defaults"]["hermes_agent_requires_full_agent_loop"])
        self.assertTrue(contract["executor_defaults"]["non_default_executor_requires_explicit_selection"])
        self.assertTrue(contract["executor_defaults"]["non_default_executor_forbids_silent_codex_fallback"])
        self.assertNotIn("default_executor", contract["executor_defaults"])
        self.assertNotIn("hermes_native_requires_full_agent_loop", contract["executor_defaults"])
        self.assertEqual(contract["experimental_executor_proofs"][0]["route_id"], "critique")
        self.assertEqual(contract["experimental_executor_proofs"][0]["executor_kind"], "hermes_agent")
        self.assertEqual(
            contract["experimental_executor_proofs"][0]["entrypoint"],
            "run_agent.AIAgent.run_conversation",
        )
        self.assertEqual(contract["experimental_executor_proofs"][0]["status"], "experimental")
        self.assertEqual(contract["experimental_executor_proofs"][0]["adapter_owner"], "one-person-lab")
        self.assertEqual(
            contract["experimental_executor_proofs"][0]["adapter_contract_ref"],
            "contracts/opl-framework/family-executor-adapter-defaults.json",
        )
        self.assertEqual(contract["experimental_executor_proofs"][0]["request_contract"], "AgentExecutionRequest")
        self.assertEqual(contract["experimental_executor_proofs"][0]["receipt_contract"], "AgentExecutionReceipt")
        self.assertFalse(contract["experimental_executor_proofs"][0]["fallback_allowed"])
        self.assertTrue(contract["experimental_executor_proofs"][0]["explicit_selection_required"])
        self.assertEqual(
            contract["experimental_executor_proofs"][0]["non_equivalence_notice"],
            "connectivity_lifecycle_receipt_audit_only",
        )
        self.assertEqual(
            contract["experimental_executor_proofs"][0]["default_executor_name_unchanged"],
            "codex_cli",
        )
        self.assertEqual(
            contract["experimental_executor_proofs"][0]["default_executor_mode_unchanged"],
            "autonomous",
        )
        self.assertEqual(
            contract["task_boundary"]["primary_scope"],
            "target-locked grant narrative authoring and scientific quality closure",
        )
        self.assertEqual(
            contract["task_boundary"]["submission_ready_relation"],
            "package submission-ready remains a stricter local export gate than MAG authoring completion.",
        )
        self.assertEqual(
            contract["task_boundary"]["closure_proof_surface"],
            "runtime_control.semantic_closure plus skill_catalog.domain_projection.runtime_continuity",
        )
        self.assertEqual(
            contract["task_boundary"]["ad_hoc_bypass_policy"],
            {
                "forbid_ad_hoc_runtime_bypass": True,
                "allowed_surfaces": [
                    "product_entry",
                    "product_status",
                    "user_loop",
                    "direct_entry",
                    "schema_backed_authoring_contract",
                ],
                "local_scripts_contracts_rule": "Local scripts/contracts are allowed only when schema-backed and surfaced through product-entry/user-loop/direct-entry runtime semantics; they must not bypass the MAG authoring runtime.",
                "generic_document_tools_rule": "Generic documents/Office tools, direct .docx edits, prompt-only drafting, hand-written export packages, and one-off ad-hoc scripts must not replace MAG grant-authoring runtime surfaces for MAG-scoped work.",
            },
        )
        self.assertIn(
            "TODO and explicit wake-up follow-ups",
            contract["task_boundary"]["objective_material_policy"],
        )
        self.assertEqual(contract["machine_local_runtime_state"]["root"], RUNTIME_STATE_ROOT)
        self.assertEqual(contract["machine_local_runtime_state"]["not_repo_tracked"], True)
        self.assertIn("contracts/runtime-program/current-program.json", contract["repo_tracked_truth_surfaces"])
        self.assertIn(
            "human_doc:2026_04_23_authoring_completion_semantics_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_22_quality_autonomy_family_grammar_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_27_ai_first_quality_boundary_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_12_opl_aligned_ideal_target_and_phase_map_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_12_hosted_caller_consumption_proof_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_12_lightweight_product_entry_and_opl_handoff_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_12_p4a_direct_grant_cockpit_and_progress_projection_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_12_p4b_direct_grant_entry_composition_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_12_p4c_mainline_status_and_grant_user_loop_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_13_p4e_schema_backed_product_status_and_manifest_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_13_p4f_local_submission_ready_package_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "human_doc:2026_04_13_critique_codex_cli_executor_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertNotIn(
            "human_doc:2026_04_13_" + "critique_codex_cli" + "_autonomous_executor_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertNotIn(
            "human_doc:2026_04_13_" + "hermes_native" + "_critique_proof_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertNotIn(
            "human_doc:2026_04_12_upstream_hermes_agent_fast_cutover_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertNotIn(
            "human_doc:2026_04_12_pending_authoring_route_handoff_matrix_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertNotIn(
            "human_doc:2026_04_11_upstream_hermes_agent_truth_reset_current_truth",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertEqual(
            contract["ideal_target"]["family_top_entry"],
            "OPL Codex-first stage-led agent runtime framework",
        )
        self.assertEqual(contract["ideal_target"]["family_runtime_framework"], "OPL stage-led runtime framework")
        self.assertEqual(contract["ideal_target"]["stage_attempt_minimum_execution_unit"], "Codex CLI")
        self.assertEqual(contract["ideal_target"]["domain_direct_entry"], "Med Auto Grant Product Entry")
        self.assertEqual(
            contract["ideal_target"]["runtime_substrate_owner"],
            "OPL stage-led runtime framework may explicitly select external providers for wakeup/control-plane "
            "consumption; route-selected authoring executor remains Codex/domain-selected by default",
        )
        self.assertEqual(contract["ideal_target"]["authoring_truth_owner"], "Med Auto Grant")
        stage_led_framework = contract["ideal_target"]["opl_stage_led_framework"]
        self.assertIn("queue/wakeup", stage_led_framework["role"])
        self.assertIn("runtime_control", stage_led_framework["consumes_mag_surfaces"])
        self.assertIn(
            "opl_stage_runtime_registration",
            stage_led_framework["consumes_mag_surfaces"],
        )
        self.assertIn(
            "family_lifecycle_adapter",
            stage_led_framework["consumes_mag_surfaces"],
        )
        self.assertIn(
            "native_helper_consumption",
            stage_led_framework["consumes_mag_surfaces"],
        )
        self.assertIn(
            "native_helper_consumption.proof_surface",
            stage_led_framework["consumes_mag_surfaces"],
        )
        self.assertIn(
            "artifact_locator_contract",
            stage_led_framework["consumes_mag_surfaces"],
        )
        self.assertIn(
            "controlled_stage_attempt_projection",
            stage_led_framework["consumes_mag_surfaces"],
        )
        self.assertIn(
            "controlled_domain_memory_apply_proof",
            stage_led_framework["consumes_mag_surfaces"],
        )
        self.assertIn("owner_receipt_runtime_evidence", stage_led_framework["consumes_mag_surfaces"])
        self.assertIn("lifecycle_receipt_runtime_evidence", stage_led_framework["consumes_mag_surfaces"])
        self.assertIn("owner_receipt_contract", stage_led_framework["consumes_mag_surfaces"])
        self.assertIn("lifecycle_guarded_apply_proof", stage_led_framework["consumes_mag_surfaces"])
        self.assertIn("physical_skeleton_follow_through", stage_led_framework["consumes_mag_surfaces"])
        self.assertIn("ideal_state_closure_status", stage_led_framework["consumes_mag_surfaces"])
        self.assertIn(
            "repo_source_layout_audit",
            stage_led_framework["consumes_mag_surfaces"],
        )
        self.assertTrue(
            any(
                "OPL Rust native helper" in item
                for item in framework_boundary["framework_consumed_projection"]
            )
        )
        self.assertIn("grant authoring truth", stage_led_framework["does_not_own"])
        self.assertIn("fundability judgment", stage_led_framework["does_not_own"])
        self.assertIn("concrete executor selection", stage_led_framework["does_not_own"])
        self.assertEqual(contract["phase_map"][0]["phase_id"], "P1")
        self.assertEqual(contract["phase_map"][0]["status"], "completed")
        self.assertEqual(contract["phase_map"][1]["phase_id"], "P2")
        self.assertEqual(contract["phase_map"][1]["status"], "completed")
        self.assertEqual(contract["phase_map"][2]["phase_id"], "P3")
        self.assertEqual(contract["phase_map"][2]["status"], "completed")
        self.assertEqual(contract["phase_map"][3]["phase_id"], "P4")
        self.assertEqual(contract["phase_map"][3]["status"], "next")

    def test_repo_tracked_truth_surfaces_use_machine_paths_or_semantic_docs(self) -> None:
        contract = json.loads(_read(CURRENT_PROGRAM_CONTRACT))
        for surface_ref in contract["repo_tracked_truth_surfaces"]:
            with self.subTest(surface_ref=surface_ref):
                if surface_ref.startswith("human_doc:"):
                    self.assertRegex(surface_ref, r"^human_doc:[a-z0-9_]+$")
                else:
                    self.assertTrue((REPO_ROOT / surface_ref).exists(), surface_ref)


if __name__ == "__main__":
    unittest.main()
