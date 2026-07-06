from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def test_line_budget_script_accepts_current_tracked_files() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        ["python", "scripts/line_budget.py"],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout


def _make_line_budget_case(tmp_path: Path) -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    case_root = tmp_path / "line-budget-case"
    scripts_dir = case_root / "scripts"
    scripts_dir.mkdir(parents=True)
    shutil.copy2(repo_root / "scripts" / "line_budget.py", scripts_dir / "line_budget.py")
    (case_root / "tmp_line_budget_case.py").write_text("\n".join("x = 1" for _ in range(1001)), encoding="utf-8")
    subprocess.run(["git", "init"], cwd=case_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["git", "add", "."], cwd=case_root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return case_root


def test_line_budget_script_fails_for_new_oversized_tracked_files(tmp_path: Path) -> None:
    case_root = _make_line_budget_case(tmp_path)

    result = subprocess.run(
        ["python", "scripts/line_budget.py"],
        cwd=case_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 1, result.stdout
    assert "line budget check failed" in result.stdout
    assert "tmp_line_budget_case.py" in result.stdout


def test_default_verify_delegates_line_budget_to_fast_lane_once() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    verify_script = (repo_root / "scripts" / "verify.sh").read_text(encoding="utf-8")
    makefile = (repo_root / "Makefile").read_text(encoding="utf-8")

    assert "python scripts/line_budget.py" not in verify_script
    assert 'lane="${1:-fast}"' in verify_script
    assert 'exec make "test-${lane}"' in verify_script
    assert "$(MAKE) test-line-budget" in makefile
    assert "test-line-budget-strict:" in makefile
    assert "$(PYTHON_CLEAN) scripts/line_budget.py --strict" not in makefile
    assert makefile.index("$(MAKE) test-line-budget") < makefile.index(
        '$(PYTEST_CLEAN) -q -m "not meta and not regression and not proof"'
    )


def test_line_budget_argparse_help_exposes_single_budget_gate() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        ["python", "scripts/line_budget.py", "--help"],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )

    assert "Fail when tracked code files exceed the line budget" in result.stdout
    assert "--list" in result.stdout
    assert "--strict" not in result.stdout
