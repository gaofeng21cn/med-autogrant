from __future__ import annotations

import subprocess
from pathlib import Path


def test_line_budget_baseline_has_no_semantic_holdouts() -> None:
    import runpy

    repo_root = Path(__file__).resolve().parents[1]
    module_globals = runpy.run_path(str(repo_root / "scripts" / "line_budget.py"))

    assert module_globals["BASELINE"] == {}


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


def test_default_verify_delegates_line_budget_to_fast_lane_once() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    verify_script = (repo_root / "scripts" / "verify.sh").read_text(encoding="utf-8")
    makefile = (repo_root / "Makefile").read_text(encoding="utf-8")

    assert "python scripts/line_budget.py" not in verify_script
    assert "make test-fast" in verify_script
    assert makefile.count("$(MAKE) test-line-budget") == 1
    assert makefile.index("$(MAKE) test-line-budget") < makefile.index(
        'uv run pytest -q -m "not meta and not regression and not proof"'
    )
