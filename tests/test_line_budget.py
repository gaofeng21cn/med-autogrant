from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import scripts.line_budget as line_budget


def test_line_budget_baseline_is_an_explicit_numeric_mapping() -> None:
    baseline = line_budget.BASELINE

    assert isinstance(baseline, dict)
    for relative_path, limit in baseline.items():
        assert isinstance(relative_path, str)
        assert relative_path
        assert isinstance(limit, int)
        assert limit > line_budget.DEFAULT_LIMIT


def test_line_budget_script_accepts_current_locked_baseline() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        ["python", "scripts/line_budget.py"],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout


def _make_line_budget_case(tmp_path: Path, filename: str) -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    case_root = tmp_path / "line-budget-case"
    scripts_dir = case_root / "scripts"
    scripts_dir.mkdir(parents=True)
    shutil.copy2(repo_root / "scripts" / "line_budget.py", scripts_dir / "line_budget.py")
    (case_root / filename).write_text("\n".join("x = 1" for _ in range(1001)), encoding="utf-8")
    subprocess.run(["git", "init"], cwd=case_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["git", "add", "."], cwd=case_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return case_root


def test_line_budget_script_is_advisory_by_default_for_new_oversized_files(tmp_path: Path) -> None:
    case_root = _make_line_budget_case(tmp_path, "tmp_line_budget_advisory_case.py")

    result = subprocess.run(
        ["python", "scripts/line_budget.py"],
        cwd=case_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "line budget advisory found" in result.stdout
    assert "ordinary development is not blocked" in result.stdout
    assert "tmp_line_budget_advisory_case.py" in result.stdout


def test_line_budget_script_fails_only_when_strict_is_explicit(tmp_path: Path) -> None:
    case_root = _make_line_budget_case(tmp_path, "tmp_line_budget_strict_case.py")

    strict_result = subprocess.run(
        ["python", "scripts/line_budget.py", "--strict"],
        cwd=case_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    env_result = subprocess.run(
        ["python", "scripts/line_budget.py"],
        cwd=case_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={**os.environ, "OPL_LINE_BUDGET_STRICT": "1"},
    )

    assert strict_result.returncode == 1, strict_result.stdout
    assert "line budget strict check failed" in strict_result.stdout
    assert "tmp_line_budget_strict_case.py" in strict_result.stdout
    assert env_result.returncode == 1, env_result.stdout
    assert "line budget strict check failed" in env_result.stdout


def test_default_verify_delegates_line_budget_to_fast_lane_once() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    verify_script = (repo_root / "scripts" / "verify.sh").read_text(encoding="utf-8")
    makefile = (repo_root / "Makefile").read_text(encoding="utf-8")

    assert "python scripts/line_budget.py" not in verify_script
    assert "make test-fast" in verify_script
    assert verify_script.count("make test-fast") == 1
    assert "$(MAKE) test-line-budget" in makefile
    assert "test-line-budget-strict:" in makefile
    assert "$(PYTHON_CLEAN) scripts/line_budget.py --strict" in makefile
    assert makefile.index("$(MAKE) test-line-budget") < makefile.index(
        '$(PYTEST_CLEAN) -q -m "not meta and not regression and not proof"'
    )


def test_line_budget_argparse_help_exposes_advisory_strict_boundary() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        ["python", "scripts/line_budget.py", "--help"],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )

    assert "Report the tracked code line budget" in result.stdout
    assert "--strict" in result.stdout
    assert "exit non-zero when line-budget issues are found" in result.stdout
