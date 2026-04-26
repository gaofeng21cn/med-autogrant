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
        self.assertEqual(contract["experimental_executor_proofs"][0]["executor_kind"], "hermes_native_proof")
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
            contract["runtime_owner"]["historical_baseline"],
            "NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP",
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
                    "frontdesk",
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
            "docs/specs/2026-04-23-authoring-completion-semantics-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn("docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md", contract["repo_tracked_truth_surfaces"])
        self.assertIn(
            "docs/specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "docs/specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "docs/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "docs/specs/2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "docs/specs/2026-04-12-p4b-direct-grant-entry-composition-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "docs/specs/2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "docs/specs/2026-04-13-p4e-schema-backed-frontdesk-and-manifest-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "docs/specs/2026-04-13-p4f-local-submission-ready-package-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn(
            "docs/specs/2026-04-13-hermes-native-critique-proof-current-truth.md",
            contract["repo_tracked_truth_surfaces"],
        )
        self.assertIn("docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md", contract["repo_tracked_truth_surfaces"])
        self.assertEqual(
            contract["ideal_target"]["family_top_entry"],
            "OPL family-level orchestration surface",
        )
        self.assertEqual(contract["ideal_target"]["family_runtime_manager"], "OPL Runtime Manager")
        self.assertEqual(contract["ideal_target"]["domain_direct_entry"], "Med Auto Grant Product Entry")
        self.assertEqual(
            contract["ideal_target"]["runtime_substrate_owner"],
            "explicit hosted runtime carrier (for example Hermes-Agent)",
        )
        self.assertEqual(contract["ideal_target"]["authoring_truth_owner"], "Med Auto Grant")
        self.assertIn("runtime_control", contract["ideal_target"]["opl_runtime_manager"]["consumes_mag_surfaces"])
        self.assertIn("grant authoring truth", contract["ideal_target"]["opl_runtime_manager"]["does_not_own"])
        self.assertEqual(contract["phase_map"][0]["phase_id"], "P1")
        self.assertEqual(contract["phase_map"][0]["status"], "completed")
        self.assertEqual(contract["phase_map"][1]["phase_id"], "P2")
        self.assertEqual(contract["phase_map"][1]["status"], "completed")
        self.assertEqual(contract["phase_map"][2]["phase_id"], "P3")
        self.assertEqual(contract["phase_map"][2]["status"], "completed")
        self.assertEqual(contract["phase_map"][3]["phase_id"], "P4")
        self.assertEqual(contract["phase_map"][3]["status"], "next")

    def test_repo_tracked_truth_surfaces_exist(self) -> None:
        contract = json.loads(_read(CURRENT_PROGRAM_CONTRACT))
        for relative_path in contract["repo_tracked_truth_surfaces"]:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((REPO_ROOT / relative_path).exists(), relative_path)


if __name__ == "__main__":
    unittest.main()
