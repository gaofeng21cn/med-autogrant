from __future__ import annotations

from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "docs" / "history" / "plan-completion-audit-2026-05-01.md"


def test_plan_completion_audit_records_all_mag_related_plan_outcomes() -> None:
    text = AUDIT_PATH.read_text(encoding="utf-8")

    expected_entries = {
        "MAS/MAG AI-first 质量边界加固计划": "`completed`",
        "MedAutoGrant Sentrux 结构质量优化计划": "`completed`",
        "MedAutoGrant 长线结构质量一轮收口计划": "`completed`",
        "MedAutoGrant Sentrux 深层结构优化二轮计划": "`superseded`",
        "MedAutoGrant Sentrux 结构优化三轮计划": "`partial`",
        "OPL Family 外部编排经验一步到位落地计划中的 MAG adoption lane": "`resolved_unpushed`",
    }
    for plan_title, status in expected_entries.items():
        assert plan_title in text
        assert status in text


def test_plan_completion_audit_preserves_real_residual_debt_boundaries() -> None:
    text = AUDIT_PATH.read_text(encoding="utf-8")

    assert "不创建 import-only tests" in text
    assert "每轮只选一个 owner" in text
    assert "monkeypatch target" in text
    assert "`./scripts/verify.sh meta`" in text
    assert "`sentrux check .`" in text
