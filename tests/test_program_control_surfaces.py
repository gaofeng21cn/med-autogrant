from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"
CONTRACTS_README = REPO_ROOT / "contracts" / "README.md"
README_EN = REPO_ROOT / "README.md"
README_ZH = REPO_ROOT / "README.zh-CN.md"
DOCS_README_EN = REPO_ROOT / "docs" / "README.md"
DOCS_README_ZH = REPO_ROOT / "docs" / "README.zh-CN.md"
CORE_PROJECT = REPO_ROOT / "docs" / "project.md"
CORE_ARCHITECTURE = REPO_ROOT / "docs" / "architecture.md"
CORE_INVARIANTS = REPO_ROOT / "docs" / "invariants.md"
CORE_STATUS = REPO_ROOT / "docs" / "status.md"
CORE_DECISIONS = REPO_ROOT / "docs" / "decisions.md"
ROOT_AGENTS = REPO_ROOT / "AGENTS.md"
TRUTH_RESET_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md"
)
FAST_CUTOVER_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md"
)
HERMES_PROGRAM_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md"
)
HERMES_MIGRATION_MAP = (
    REPO_ROOT / "docs" / "specs" / "2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md"
)
P4A_PRODUCT_PROJECTION_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md"
)
P4B_DIRECT_ENTRY_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-p4b-direct-grant-entry-composition-current-truth.md"
)
P4C_USER_LOOP_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md"
)
P4F_SUBMISSION_READY_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-13-p4f-local-submission-ready-package-current-truth.md"
)
HERMES_NATIVE_CRITIQUE_PROOF_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-13-hermes-native-critique-proof-current-truth.md"
)
FORMAL_ENTRY_MATRIX = REPO_ROOT / "docs" / "specs" / "2026-04-07-formal-entry-matrix-current-truth.md"
DURABILITY_MODEL = REPO_ROOT / "docs" / "specs" / "2026-04-07-durability-model-clarification.md"
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
            "CLI-first with real upstream Hermes-Agent runtime substrate",
        )
        self.assertEqual(contract["runtime_owner"]["active_phase"], "P4 mature direct grant product entry")
        self.assertEqual(
            contract["runtime_owner"]["active_tranche"],
            "P4.F local submission-ready package landing",
        )
        self.assertEqual(contract["executor_defaults"]["default_executor"], "codex_cli_autonomous")
        self.assertEqual(contract["executor_defaults"]["default_model"], "inherit_local_codex_default")
        self.assertEqual(
            contract["executor_defaults"]["default_reasoning_effort"],
            "inherit_local_codex_default",
        )
        self.assertTrue(contract["executor_defaults"]["chat_completion_only_executor_forbidden"])
        self.assertTrue(contract["executor_defaults"]["hermes_native_requires_full_agent_loop"])
        self.assertEqual(contract["experimental_executor_proofs"][0]["route_id"], "critique")
        self.assertEqual(contract["experimental_executor_proofs"][0]["executor_kind"], "hermes_native_proof")
        self.assertEqual(
            contract["experimental_executor_proofs"][0]["entrypoint"],
            "run_agent.AIAgent.run_conversation",
        )
        self.assertEqual(contract["experimental_executor_proofs"][0]["status"], "experimental")
        self.assertEqual(
            contract["experimental_executor_proofs"][0]["default_executor_unchanged"],
            "codex_cli_autonomous",
        )
        self.assertEqual(
            contract["runtime_owner"]["historical_baseline"],
            "NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP",
        )
        self.assertEqual(contract["machine_local_runtime_state"]["root"], RUNTIME_STATE_ROOT)
        self.assertEqual(contract["machine_local_runtime_state"]["not_repo_tracked"], True)
        self.assertIn("contracts/runtime-program/current-program.json", contract["repo_tracked_truth_surfaces"])
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
        self.assertEqual(contract["ideal_target"]["family_top_entry"], "OPL Gateway")
        self.assertEqual(contract["ideal_target"]["domain_direct_entry"], "Med Auto Grant Product Entry")
        self.assertEqual(contract["ideal_target"]["runtime_substrate_owner"], "Hermes-Agent")
        self.assertEqual(contract["ideal_target"]["authoring_truth_owner"], "Med Auto Grant")
        self.assertEqual(contract["phase_map"][0]["phase_id"], "P1")
        self.assertEqual(contract["phase_map"][0]["status"], "completed")
        self.assertEqual(contract["phase_map"][1]["phase_id"], "P2")
        self.assertEqual(contract["phase_map"][1]["status"], "completed")
        self.assertEqual(contract["phase_map"][2]["phase_id"], "P3")
        self.assertEqual(contract["phase_map"][2]["status"], "completed")
        self.assertEqual(contract["phase_map"][3]["phase_id"], "P4")
        self.assertEqual(contract["phase_map"][3]["status"], "next")

    def test_core_docs_publish_repo_tracked_contract_and_user_level_runtime_state(self) -> None:
        for path in (
            README_EN,
            DOCS_README_EN,
            CORE_ARCHITECTURE,
            CORE_INVARIANTS,
            CORE_STATUS,
            ROOT_AGENTS,
            CONTRACTS_README,
        ):
            text = _read(path)
            self.assertIn("contracts/runtime-program/current-program.json", text, path.name)
            self.assertIn(RUNTIME_STATE_ROOT, text, path.name)

        project = _read(CORE_PROJECT)
        self.assertIn("CLI-first with real upstream Hermes-Agent runtime substrate", project)
        self.assertIn("P4.A", project)
        self.assertIn("P4.B", project)

        decisions = _read(CORE_DECISIONS)
        self.assertIn("上游 Hermes-Agent 目标", decisions)
        self.assertIn("grant-progress", decisions)
        self.assertIn("grant-user-loop", decisions)
        self.assertIn("build-submission-ready-package", decisions)
        self.assertIn("executor_kind=hermes_native_proof", decisions)

    def test_current_truth_specs_align_with_repo_tracked_contract(self) -> None:
        contract = json.loads(_read(CURRENT_PROGRAM_CONTRACT))
        fast_cutover = _read(FAST_CUTOVER_CURRENT_TRUTH)
        truth_reset = _read(TRUTH_RESET_CURRENT_TRUTH)
        migration_map = _read(HERMES_MIGRATION_MAP)
        p4a_product_projection = _read(P4A_PRODUCT_PROJECTION_CURRENT_TRUTH)
        p4b_direct_entry = _read(P4B_DIRECT_ENTRY_CURRENT_TRUTH)
        p4c_user_loop = _read(P4C_USER_LOOP_CURRENT_TRUTH)
        p4f_submission_ready = _read(P4F_SUBMISSION_READY_CURRENT_TRUTH)
        hermes_native_critique_proof = _read(HERMES_NATIVE_CRITIQUE_PROOF_CURRENT_TRUTH)
        formal_entry = _read(FORMAL_ENTRY_MATRIX)
        durability = _read(DURABILITY_MODEL)

        self.assertIn("landed / current truth", fast_cutover)
        self.assertIn("probe-upstream-hermes", fast_cutover)
        self.assertIn("MedAutoGrantDomainEntry", fast_cutover)
        self.assertIn("SessionDB", fast_cutover)
        self.assertIn(
            "docs/specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md",
            fast_cutover,
        )
        self.assertIn("还没有", truth_reset)
        self.assertIn("repo-local code", truth_reset)
        self.assertIn("current-program pointer", truth_reset)
        self.assertIn("contracts/runtime-program/current-program.json", migration_map)
        self.assertIn("build-hosted-contract-bundle", migration_map)
        self.assertIn("grant-progress", p4a_product_projection)
        self.assertIn("grant-cockpit", p4a_product_projection)
        self.assertIn("controller-owned", p4a_product_projection)
        self.assertIn("schema-backed", p4a_product_projection)
        self.assertIn("fail-closed", p4a_product_projection)
        self.assertIn("grant-progress.schema.json", p4a_product_projection)
        self.assertIn("grant-cockpit.schema.json", p4a_product_projection)
        self.assertIn("也不进入 hosted contract bundle 的 command catalog", p4a_product_projection)
        self.assertIn("contracts/runtime-program/current-program.json", formal_entry)
        self.assertIn("contracts/runtime-program/current-program.json", durability)
        self.assertIn(RUNTIME_STATE_ROOT, durability)
        self.assertIn("grant-direct-entry", p4b_direct_entry)
        self.assertIn("grant_direct_entry", p4b_direct_entry)
        self.assertIn("build-product-entry", p4b_direct_entry)
        self.assertIn("grant-cockpit", p4b_direct_entry)
        self.assertIn("P4.B", p4b_direct_entry)
        self.assertIn("mainline-status", p4c_user_loop)
        self.assertIn("mainline-phase", p4c_user_loop)
        self.assertIn("grant-user-loop", p4c_user_loop)
        self.assertIn("P4.C", p4c_user_loop)
        self.assertIn("build-submission-ready-package", p4f_submission_ready)
        self.assertIn("submission-ready-package.schema.json", p4f_submission_ready)
        self.assertIn("fail-closed", p4f_submission_ready)
        self.assertIn("外部官网提交", p4f_submission_ready)
        self.assertIn("executor_kind = hermes_native_proof", hermes_native_critique_proof)
        self.assertIn("run_agent.AIAgent.run_conversation", hermes_native_critique_proof)
        self.assertIn("full agent loop", hermes_native_critique_proof)
        self.assertIn("~/.hermes/config.yaml", hermes_native_critique_proof)
        self.assertIn("MED_AUTOGRANT_HERMES_MODEL", hermes_native_critique_proof)
        self.assertIn("tool_start / tool_complete", hermes_native_critique_proof)

    def test_core_docs_publish_schema_backed_projection_contract_boundary(self) -> None:
        architecture = _read(CORE_ARCHITECTURE)
        status = _read(CORE_STATUS)
        decisions = _read(CORE_DECISIONS)
        contracts_readme = _read(CONTRACTS_README)

        self.assertIn("grant-progress.schema.json", architecture)
        self.assertIn("grant-cockpit.schema.json", architecture)
        self.assertIn("grant-direct-entry.schema.json", architecture)
        self.assertIn("grant-user-loop.schema.json", architecture)
        self.assertIn("product-entry-manifest.schema.json", architecture)
        self.assertIn("product-frontdesk.schema.json", architecture)
        self.assertIn("schema-backed", status)
        self.assertIn("fail-closed", status)
        self.assertIn("schema-backed", decisions)
        self.assertIn("product-entry-manifest.schema.json", contracts_readme)
        self.assertIn("product-frontdesk.schema.json", contracts_readme)
        self.assertIn("grant-progress.schema.json", contracts_readme)
        self.assertIn("grant-cockpit.schema.json", contracts_readme)
        self.assertIn("grant-direct-entry.schema.json", contracts_readme)
        self.assertIn("grant-user-loop.schema.json", contracts_readme)
        self.assertIn("submission-ready-package.schema.json", architecture)
        self.assertIn("submission-ready-package.schema.json", contracts_readme)

    def test_public_surfaces_no_longer_require_project_runtime_program_directory(self) -> None:
        for path in (README_EN, README_ZH, DOCS_README_EN, DOCS_README_ZH):
            text = _read(path)
            self.assertNotIn(".runtime-program/", text, path.name)
            self.assertNotIn(".codex/", text, path.name)
            self.assertNotIn(".omx/", text, path.name)


if __name__ == "__main__":
    unittest.main()
