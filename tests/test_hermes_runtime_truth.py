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
FAST_CUTOVER_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md"
)
PRODUCT_ENTRY_CURRENT_TRUTH = (
    REPO_ROOT / "docs" / "specs" / "2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md"
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
    assert "CLI-first with real upstream Hermes-Agent runtime substrate" in invariants
    assert "domain adapter / entry adapter" in invariants

    decisions = _read(CORE_DECISIONS)
    assert "repo-local runtime" in decisions
    assert "上游 Hermes-Agent 目标" in decisions


@pytest.mark.meta
def test_domain_positioning_public_docs_follow_truth_reset_mainline() -> None:
    for path in (DOMAIN_POSITIONING_EN, DOMAIN_POSITIONING_ZH):
        text = _read(path)
        assert "real upstream Hermes-Agent runtime substrate" in text
        assert "compatibility bridge" in text
        assert "regression oracle" in text or "regression oracle" in text


@pytest.mark.meta
def test_readme_current_maturity_cards_follow_truth_reset_status() -> None:
    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)

    assert "real upstream `Hermes-Agent` runtime substrate" in readme_en
    assert "MedAutoGrantDomainEntry" in readme_en
    assert "actual hosted runtime" in readme_en

    assert "真实上游 `Hermes-Agent` runtime substrate" in readme_zh
    assert "MedAutoGrantDomainEntry" in readme_zh
    assert "submission-ready" in readme_zh


@pytest.mark.meta
def test_repo_tracks_truth_reset_surface_and_historical_migration_map() -> None:
    assert FAST_CUTOVER_CURRENT_TRUTH.exists(), f"Fast cutover current truth 不存在: {FAST_CUTOVER_CURRENT_TRUTH}"
    assert TRUTH_RESET_CURRENT_TRUTH.exists(), f"Truth reset current truth 不存在: {TRUTH_RESET_CURRENT_TRUTH}"
    assert HERMES_PROGRAM_TRUTH.exists(), f"Hermes runtime program truth 不存在: {HERMES_PROGRAM_TRUTH}"
    assert HERMES_MIGRATION_MAP.exists(), f"Hermes migration map 不存在: {HERMES_MIGRATION_MAP}"

    fast_cutover = _read(FAST_CUTOVER_CURRENT_TRUTH)
    truth_reset = _read(TRUTH_RESET_CURRENT_TRUTH)
    program_truth = _read(HERMES_PROGRAM_TRUTH)
    migration_map = _read(HERMES_MIGRATION_MAP)

    assert "landed / current truth" in fast_cutover
    assert "probe-upstream-hermes" in fast_cutover
    assert "MedAutoGrantDomainEntry" in fast_cutover
    assert "service-safe domain entry" in fast_cutover
    assert PRODUCT_ENTRY_CURRENT_TRUTH.exists(), f"Product entry current truth 不存在: {PRODUCT_ENTRY_CURRENT_TRUTH}"

    product_entry_truth = _read(PRODUCT_ENTRY_CURRENT_TRUTH)
    assert "build-product-entry" in product_entry_truth
    assert "direct" in product_entry_truth
    assert "opl-handoff" in product_entry_truth
    assert "runtime_session_contract" in product_entry_truth
    assert "return_surface_contract" in product_entry_truth
    assert "MedAutoGrantDomainEntry" in product_entry_truth

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


@pytest.mark.meta
def test_entry_docs_freeze_product_entry_and_opl_handoff_on_top_of_landed_runtime_substrate() -> None:
    reference = REPO_ROOT / "docs" / "references" / "lightweight_product_entry_and_opl_handoff.md"
    reference_text = _read(reference)

    for path in (README_EN, README_ZH, DOCS_README_EN, DOCS_README_ZH, CORE_PROJECT, CORE_ARCHITECTURE, CORE_STATUS):
        text = _read(path)
        assert "product entry" in text
        assert "OPL" in text

    readme_en = _read(README_EN)
    readme_zh = _read(README_ZH)
    docs_readme_en = _read(DOCS_README_EN)
    docs_readme_zh = _read(DOCS_README_ZH)
    architecture = _read(CORE_ARCHITECTURE)
    status = _read(CORE_STATUS)

    assert "lightweight structured `product entry` shell is now landed" in readme_en
    assert "`build-product-entry`" in readme_en
    assert "richer grant-facing product experience still remains future work" in readme_en
    assert "轻量结构化 `product entry` shell 已经落地" in readme_zh
    assert "`build-product-entry`" in readme_zh
    assert "更完整的 grant-facing 产品体验仍要继续补" in readme_zh

    assert "lightweight grant `product entry` shell" in docs_readme_en
    assert "Product-entry shell" in docs_readme_en
    assert "./specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md" in docs_readme_en
    assert "./references/lightweight_product_entry_and_opl_handoff.md" in docs_readme_en
    assert "轻量 grant `product entry` shell" in docs_readme_zh
    assert "产品入口 shell" in docs_readme_zh
    assert "./specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md" in docs_readme_zh
    assert "./references/lightweight_product_entry_and_opl_handoff.md" in docs_readme_zh

    assert "User -> OPL Product Entry -> OPL Gateway -> Hermes Kernel -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry" in architecture
    assert "build-product-entry" in architecture
    assert "workspace_id" in architecture
    assert "draft_id" in architecture
    assert "funding_call" in architecture
    assert "OPL -> Med Auto Grant" in status
    assert "build-product-entry" in status

    assert "target_domain_id" in reference_text
    assert "task_intent" in reference_text
    assert "entry_mode" in reference_text
    assert "workspace_locator" in reference_text
    assert "runtime_session_contract" in reference_text
    assert "return_surface_contract" in reference_text
    assert "workspace_id" in reference_text
    assert "draft_id" in reference_text
    assert "funding_call" in reference_text
    assert "runtime substrate 已经真正落在上游 `Hermes-Agent` 上" in reference_text
    assert "build-product-entry" in reference_text
