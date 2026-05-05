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
    assert baseline["quality_signal"] >= 0.59
    assert baseline["cycle_count"] == 0

    rules_text = rules_path.read_text(encoding="utf-8")
    assert "min_quality = 0.59" in rules_text
    assert "max_cycles = 0" in rules_text
    assert "max_depth = 14" in rules_text
    assert "runtime_facade" in rules_text
    assert "export_package" in rules_text

    workflow_text = workflow_path.read_text(encoding="utf-8")
    assert "continue-on-error: true" in workflow_text
    assert "fetch-depth: 0" in workflow_text
    assert "git fetch --no-tags --prune origin main:refs/remotes/origin/main" in workflow_text
    assert "./scripts/run-structural-quality-gate.sh --advisory" in workflow_text
    assert "compare-ref: origin/main" in workflow_text

    structural_gate_script = (REPO_ROOT / "scripts" / "run-structural-quality-gate.sh").read_text(
        encoding="utf-8"
    )
    quality_details_script = (REPO_ROOT / "scripts" / "run-opl-quality-details.sh").read_text(encoding="utf-8")
    verify_script = (REPO_ROOT / "scripts" / "verify.sh").read_text(encoding="utf-8")
    makefile_text = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    assert "sentrux gate ." in structural_gate_script
    assert "sentrux check ." in structural_gate_script
    assert "complete .sentrux/rules.toml sidecar" in structural_gate_script
    assert 'compare_ref="${OPL_QUALITY_DETAILS_COMPARE_REF:-origin/main}"' in quality_details_script
    assert 'quality details --root . --format markdown --limit 20 --compare-ref "${compare_ref}"' in quality_details_script
    assert 'quality details --root . --format json --compare-ref "${compare_ref}"' in quality_details_script
    assert "sentrux-rules.toml" in quality_details_script
    assert "structure)" in verify_script
    assert "test-structure:" in makefile_text


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
