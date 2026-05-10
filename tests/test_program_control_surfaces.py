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
        self.assertEqual(
            contract["runtime_owner"]["runtime_manager_boundary"]["manager"],
            "OPL Runtime Manager",
        )
        self.assertIn(
            "runtime_control.semantic_closure",
            contract["runtime_owner"]["runtime_manager_boundary"]["manager_consumed_projection"],
        )
        self.assertIn(
            "skill_catalog.domain_projection.opl_runtime_manager_registration",
            contract["runtime_owner"]["runtime_manager_boundary"]["manager_consumed_projection"],
        )
        self.assertIn(
            "skill_catalog.domain_projection.opl_runtime_manager_registration.family_lifecycle_adapter",
            contract["runtime_owner"]["runtime_manager_boundary"]["manager_consumed_projection"],
        )
        self.assertIn(
            "skill_catalog.domain_projection.opl_runtime_manager_registration.native_helper_consumption.proof_surface",
            contract["runtime_owner"]["runtime_manager_boundary"]["manager_consumed_projection"],
        )
        self.assertIn(
            "grant-domain truth owner",
            contract["runtime_owner"]["runtime_manager_boundary"]["manager_non_goals"],
        )
        self.assertEqual(contract["executor_defaults"]["default_executor_name"], "codex_cli")
        self.assertEqual(contract["executor_defaults"]["default_executor_mode"], "autonomous")
        self.assertEqual(contract["executor_defaults"]["default_model"], "inherit_local_codex_default")
        self.assertEqual(
            contract["executor_defaults"]["default_reasoning_effort"],
            "inherit_local_codex_default",
        )
        self.assertEqual(
            contract["executor_defaults"]["executor_labels"],
            {
                "codex_cli": "Codex CLI",
                "hermes_agent": "Hermes-Agent",
            },
        )
        self.assertEqual(
            contract["executor_defaults"]["executor_statuses"],
            {
                "codex_cli": "default",
                "hermes_agent": "experimental",
            },
        )
        self.assertTrue(contract["executor_defaults"]["chat_completion_only_executor_forbidden"])
        self.assertTrue(contract["executor_defaults"]["hermes_agent_requires_full_agent_loop"])
        self.assertNotIn("default_executor", contract["executor_defaults"])
        self.assertNotIn("hermes_native_requires_full_agent_loop", contract["executor_defaults"])
        self.assertEqual(contract["experimental_executor_proofs"][0]["route_id"], "critique")
        self.assertEqual(contract["experimental_executor_proofs"][0]["executor_kind"], "hermes_agent")
        self.assertEqual(
            contract["experimental_executor_proofs"][0]["entrypoint"],
            "run_agent.AIAgent.run_conversation",
        )
        self.assertEqual(contract["experimental_executor_proofs"][0]["status"], "experimental")
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
        self.assertIn("human_doc:2026_04_12_upstream_hermes_agent_fast_cutover_current_truth", contract["repo_tracked_truth_surfaces"])
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
        self.assertIn("human_doc:2026_04_11_upstream_hermes_agent_truth_reset_current_truth", contract["repo_tracked_truth_surfaces"])
        self.assertEqual(
            contract["ideal_target"]["family_top_entry"],
            "OPL family-level orchestration surface",
        )
        self.assertEqual(contract["ideal_target"]["family_runtime_manager"], "OPL Runtime Manager")
        self.assertEqual(contract["ideal_target"]["domain_direct_entry"], "Med Auto Grant Product Entry")
        self.assertEqual(
            contract["ideal_target"]["runtime_substrate_owner"],
            "OPL-managed Hermes as online substrate for family runtime wakeup/control-plane consumption; "
            "route-selected authoring executor remains Codex/domain-selected by default",
        )
        self.assertEqual(contract["ideal_target"]["authoring_truth_owner"], "Med Auto Grant")
        self.assertIn("runtime_control", contract["ideal_target"]["opl_runtime_manager"]["consumes_mag_surfaces"])
        self.assertIn(
            "opl_runtime_manager_registration",
            contract["ideal_target"]["opl_runtime_manager"]["consumes_mag_surfaces"],
        )
        self.assertIn(
            "family_lifecycle_adapter",
            contract["ideal_target"]["opl_runtime_manager"]["consumes_mag_surfaces"],
        )
        self.assertIn(
            "native_helper_consumption",
            contract["ideal_target"]["opl_runtime_manager"]["consumes_mag_surfaces"],
        )
        self.assertIn(
            "native_helper_consumption.proof_surface",
            contract["ideal_target"]["opl_runtime_manager"]["consumes_mag_surfaces"],
        )
        self.assertTrue(
            any(
                "OPL Rust native helper" in item
                for item in contract["runtime_owner"]["runtime_manager_boundary"]["manager_consumed_projection"]
            )
        )
        self.assertIn("grant authoring truth", contract["ideal_target"]["opl_runtime_manager"]["does_not_own"])
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
