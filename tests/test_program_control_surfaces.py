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
        self.assertEqual(contract["runtime_owner"]["active_phase"], "Upstream Hermes-Agent Fast Cutover")
        self.assertEqual(
            contract["runtime_owner"]["active_tranche"],
            "Real Hermes substrate / service-safe domain entry / fresh proof",
        )
        self.assertEqual(
            contract["runtime_owner"]["historical_baseline"],
            "NO_NEW_POST_R5A_LOCAL_RUNTIME_DELTA_HONEST_STOP",
        )
        self.assertEqual(contract["machine_local_runtime_state"]["root"], RUNTIME_STATE_ROOT)
        self.assertEqual(contract["machine_local_runtime_state"]["not_repo_tracked"], True)
        self.assertIn("contracts/runtime-program/current-program.json", contract["repo_tracked_truth_surfaces"])
        self.assertIn("docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md", contract["repo_tracked_truth_surfaces"])
        self.assertIn("docs/specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md", contract["repo_tracked_truth_surfaces"])

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

        decisions = _read(CORE_DECISIONS)
        self.assertIn("上游 Hermes-Agent 目标", decisions)

    def test_current_truth_specs_align_with_repo_tracked_contract(self) -> None:
        contract = json.loads(_read(CURRENT_PROGRAM_CONTRACT))
        fast_cutover = _read(FAST_CUTOVER_CURRENT_TRUTH)
        truth_reset = _read(TRUTH_RESET_CURRENT_TRUTH)
        migration_map = _read(HERMES_MIGRATION_MAP)
        formal_entry = _read(FORMAL_ENTRY_MATRIX)
        durability = _read(DURABILITY_MODEL)

        self.assertIn("landed / current truth", fast_cutover)
        self.assertIn("probe-upstream-hermes", fast_cutover)
        self.assertIn("MedAutoGrantDomainEntry", fast_cutover)
        self.assertIn("SessionDB", fast_cutover)
        self.assertIn("还没有", truth_reset)
        self.assertIn("repo-local code", truth_reset)
        self.assertIn("current-program pointer", truth_reset)
        self.assertIn("contracts/runtime-program/current-program.json", migration_map)
        self.assertIn("build-hosted-contract-bundle", migration_map)
        self.assertIn("contracts/runtime-program/current-program.json", formal_entry)
        self.assertIn("contracts/runtime-program/current-program.json", durability)
        self.assertIn(RUNTIME_STATE_ROOT, durability)

    def test_public_surfaces_no_longer_require_project_runtime_program_directory(self) -> None:
        for path in (README_EN, README_ZH, DOCS_README_EN, DOCS_README_ZH):
            text = _read(path)
            self.assertNotIn(".runtime-program/", text, path.name)
            self.assertNotIn(".codex/", text, path.name)
            self.assertNotIn(".omx/", text, path.name)


if __name__ == "__main__":
    unittest.main()
