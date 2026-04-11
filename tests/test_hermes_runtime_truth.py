from __future__ import annotations

from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
README_EN = REPO_ROOT / "README.md"
README_ZH = REPO_ROOT / "README.zh-CN.md"
DOCS_README_EN = REPO_ROOT / "docs" / "README.md"
DOCS_README_ZH = REPO_ROOT / "docs" / "README.zh-CN.md"
CORE_PROJECT = REPO_ROOT / "docs" / "project.md"
CORE_ARCHITECTURE = REPO_ROOT / "docs" / "architecture.md"
CORE_INVARIANTS = REPO_ROOT / "docs" / "invariants.md"
CORE_DECISIONS = REPO_ROOT / "docs" / "decisions.md"
CORE_STATUS = REPO_ROOT / "docs" / "status.md"
DOMAIN_POSITIONING_EN = REPO_ROOT / "docs" / "domain-positioning.md"
DOMAIN_POSITIONING_ZH = REPO_ROOT / "docs" / "domain-positioning.zh-CN.md"
TRUTH_RESET_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md"
)
HERMES_PROGRAM_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md"
)
HERMES_MIGRATION_MAP = (
    REPO_ROOT / "docs" / "specs" / "2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md"
)
RUNTIME_STATE_SESSIONS_DISPLAY = "$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@pytest.mark.meta
def test_core_docs_publish_truth_reset_runtime_topology_and_bridge_boundary() -> None:
    for path in (
        README_EN,
        README_ZH,
        DOCS_README_EN,
        DOCS_README_ZH,
        CORE_PROJECT,
        CORE_ARCHITECTURE,
        CORE_STATUS,
    ):
        text = _read(path)
        assert "Hermes-Agent" in text
        assert "CLI" in text
        assert "MCP" in text
        assert "controller" in text

    invariants = _read(CORE_INVARIANTS)
    assert "repo-local runtime baseline with upstream Hermes-Agent pending" in invariants
    assert "migration scaffold" in invariants

    decisions = _read(CORE_DECISIONS)
    assert "repo-local runtime" in decisions
    assert "上游 Hermes-Agent 目标" in decisions


@pytest.mark.meta
def test_domain_positioning_public_docs_follow_truth_reset_mainline() -> None:
    for path in (DOMAIN_POSITIONING_EN, DOMAIN_POSITIONING_ZH):
        text = _read(path)
        assert "repo-local runtime baseline" in text
        assert "compatibility bridge" in text
        assert "target substrate" in text or "目标 substrate" in text


@pytest.mark.meta
def test_readme_current_maturity_cards_follow_truth_reset_status() -> None:
    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)

    assert "landed a true upstream `Hermes-Agent` integration yet" in readme_en
    assert "repo-local migration scaffold" in readme_en
    assert "actual hosted runtime" in readme_en

    assert "还没有**真正完成上游 `Hermes-Agent` 集成" in readme_zh or "尚未落地" in readme_zh
    assert "migration scaffold" in readme_zh
    assert "submission-ready" in readme_zh


@pytest.mark.meta
def test_repo_tracks_truth_reset_surface_and_historical_migration_map() -> None:
    assert TRUTH_RESET_CURRENT_TRUTH.exists(), f"Truth reset current truth 不存在: {TRUTH_RESET_CURRENT_TRUTH}"
    assert HERMES_PROGRAM_TRUTH.exists(), f"Hermes runtime program truth 不存在: {HERMES_PROGRAM_TRUTH}"
    assert HERMES_MIGRATION_MAP.exists(), f"Hermes migration map 不存在: {HERMES_MIGRATION_MAP}"

    truth_reset = _read(TRUTH_RESET_CURRENT_TRUTH)
    program_truth = _read(HERMES_PROGRAM_TRUTH)
    migration_map = _read(HERMES_MIGRATION_MAP)

    assert "还没有**真正完成上游 `Hermes-Agent` 集成" in truth_reset or "还没有" in truth_reset
    assert "repo-local code" in truth_reset
    assert "run-local" in truth_reset
    assert "build-hosted-contract-bundle" in truth_reset

    assert "Hermes-backed runtime substrate" in program_truth
    assert "history" not in program_truth.lower()
    assert "CLI" in program_truth
    assert "MCP" in program_truth
    assert "controller" in program_truth
    assert "Auto-only" in program_truth
    assert "compatibility bridge" in program_truth
    assert "regression oracle" in program_truth
    assert RUNTIME_STATE_SESSIONS_DISPLAY in program_truth
    assert "runtime_substrate_contract" in program_truth
    assert "runtime_state_contract" in program_truth
    assert "operator_contract" in program_truth

    assert "validate-workspace" in migration_map
    assert "summarize-workspace" in migration_map
    assert "next-step" in migration_map
    assert "critique-summary" in migration_map
    assert "stage-route-report" in migration_map
    assert "run-local" in migration_map
    assert "resume-local" in migration_map
    assert "execute-revision-pass" in migration_map
    assert "build-final-package" in migration_map
    assert "build-hosted-contract-bundle" in migration_map
    assert "revised-workspace output identity guard" in migration_map
    assert "artifact-bundle 输入加载" in migration_map
    assert "bundle output identity guard" in migration_map
    assert "final package document assembly" in migration_map
    assert "Hermes substrate" in migration_map
    assert "Grant domain logic" in migration_map
    assert RUNTIME_STATE_SESSIONS_DISPLAY in migration_map
    assert "runtime_substrate_contract" in migration_map
    assert "runtime_state_contract" in migration_map
    assert "operator_contract" in migration_map
