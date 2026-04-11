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
def test_core_docs_publish_hermes_runtime_topology_and_bridge_boundary() -> None:
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
        assert "Hermes-backed runtime" in text
        assert "CLI" in text
        assert "MCP" in text
        assert "controller" in text

    invariants = _read(CORE_INVARIANTS)
    assert "Hermes-backed runtime substrate" in invariants
    assert "compatibility bridge" in invariants
    assert "regression oracle" in invariants

    decisions = _read(CORE_DECISIONS)
    assert "Hermes-backed runtime substrate" in decisions
    assert "post-R5A" in decisions


@pytest.mark.meta
def test_domain_positioning_public_docs_follow_hermes_mainline() -> None:
    for path in (DOMAIN_POSITIONING_EN, DOMAIN_POSITIONING_ZH):
        text = _read(path)
        assert "Hermes-backed runtime" in text
        assert "compatibility bridge" in text
        assert "regression oracle" in text
        assert "Codex-default host-agent runtime" not in text
        assert "baseline freeze / local-runtime upper-bound closeout" not in text


@pytest.mark.meta
def test_readme_current_maturity_cards_follow_hermes_program_status() -> None:
    for path in (README_EN, README_ZH):
        text = _read(path)
        assert "Hermes Runtime Substrate Program" in text
        assert "Hermes-backed runtime" in text
        assert "Current Maturity" in text or "当前成熟度" in text
        assert "baseline freeze / local-runtime upper-bound closeout" not in text


@pytest.mark.meta
def test_repo_tracks_hermes_runtime_program_and_capability_migration_map() -> None:
    assert HERMES_PROGRAM_TRUTH.exists(), f"Hermes runtime program truth 不存在: {HERMES_PROGRAM_TRUTH}"
    assert HERMES_MIGRATION_MAP.exists(), f"Hermes migration map 不存在: {HERMES_MIGRATION_MAP}"

    program_truth = _read(HERMES_PROGRAM_TRUTH)
    migration_map = _read(HERMES_MIGRATION_MAP)

    assert "Hermes-backed runtime substrate" in program_truth
    assert "CLI" in program_truth
    assert "MCP" in program_truth
    assert "controller" in program_truth
    assert "Auto-only" in program_truth
    assert "compatibility bridge" in program_truth
    assert "regression oracle" in program_truth
    assert RUNTIME_STATE_SESSIONS_DISPLAY in program_truth

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
