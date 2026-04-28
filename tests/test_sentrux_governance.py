from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.meta
def test_sentrux_governance_files_are_tracked_and_advisory() -> None:
    baseline_path = REPO_ROOT / ".sentrux" / "baseline.json"
    rules_path = REPO_ROOT / ".sentrux" / "rules.toml"
    workflow_path = REPO_ROOT / ".github" / "workflows" / "sentrux-advisory.yml"

    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    assert baseline["quality_signal"] >= 0.44
    assert baseline["cycle_count"] <= 2

    rules_text = rules_path.read_text(encoding="utf-8")
    assert "max_cycles" in rules_text
    assert "runtime_facade" in rules_text
    assert "runtime_parts" in rules_text
    assert "export_package" in rules_text

    workflow_text = workflow_path.read_text(encoding="utf-8")
    assert "continue-on-error: true" in workflow_text
    assert "sentrux gate ." in workflow_text
    assert "sentrux check ." in workflow_text

    docs_text = (REPO_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    docs_zh_text = (REPO_ROOT / "docs" / "README.zh-CN.md").read_text(encoding="utf-8")
    assert "sentrux gate ." in docs_text
    assert "sentrux check ." in docs_text
    assert "sentrux gate ." in docs_zh_text
    assert "sentrux check ." in docs_zh_text


@pytest.mark.meta
def test_no_mechanical_split_residue_in_tracked_paths() -> None:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    residue = [
        path
        for path in result.stdout.splitlines()
        if any(token in Path(path).name for token in ("chunk_", "part_", "split_"))
    ]

    assert residue == []
