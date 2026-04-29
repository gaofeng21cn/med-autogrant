from __future__ import annotations

import ast
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
    assert baseline["quality_signal"] >= 0.58
    assert baseline["cycle_count"] == 0

    rules_text = rules_path.read_text(encoding="utf-8")
    assert "min_quality = 0.58" in rules_text
    assert "max_cycles = 0" in rules_text
    assert "max_depth = 14" in rules_text
    assert "runtime_facade" in rules_text
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
    assert "small score movement is acceptable" in docs_text
    assert "Sentrux 分数小幅波动可以接受" in docs_zh_text


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


def _function_line_span(relative_path: str, function_name: str) -> int:
    tree = ast.parse((REPO_ROOT / relative_path).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return int(node.end_lineno or node.lineno) - node.lineno + 1
    raise AssertionError(f"function not found: {relative_path}:{function_name}")


@pytest.mark.meta
def test_selected_structural_hotspots_stay_within_reviewed_spans() -> None:
    assert _function_line_span(
        "src/med_autogrant/grant_autonomy_controller.py",
        "run_grant_autonomy_controller",
    ) <= 950
    assert _function_line_span(
        "src/med_autogrant/grant_autonomy_request.py",
        "validate_grant_autonomy_request",
    ) <= 180
    assert _function_line_span(
        "src/med_autogrant/cli_rendering_parts.py",
        "_render_text",
    ) <= 600
