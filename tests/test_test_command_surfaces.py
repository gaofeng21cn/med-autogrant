from __future__ import annotations

import tomllib
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _make_dry_run(target: str) -> str:
    result = subprocess.run(
        ["make", "-n", target],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.stdout


def _tracked_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return set(result.stdout.splitlines())


def test_makefile_lanes_route_to_repo_native_checks() -> None:
    structure = _make_dry_run("test-structure")
    structure_strict = _make_dry_run("test-structure-strict")

    assert "scripts/check_descriptor_contracts.py" in structure
    assert "run-structural-quality-gate" not in structure
    assert "sentrux" not in structure.lower()

    assert "scripts/check_descriptor_contracts.py" in structure_strict


def test_clean_python_runners_route_caches_outside_checkout() -> None:
    python_runner = _read("scripts/run-python-clean.sh")

    subprocess.run(["bash", "-n", "scripts/run-python-clean.sh"], cwd=REPO_ROOT, check=True)
    subprocess.run(["bash", "-n", "scripts/run-pytest-clean.sh"], cwd=REPO_ROOT, check=True)
    assert "PYTHONDONTWRITEBYTECODE=1" in python_runner
    assert "PYTHONPYCACHEPREFIX" in python_runner
    assert 'venv_python="${repo_root}/.venv/bin/python"' not in python_runner


def test_pyproject_registers_cli_scripts_and_external_cache() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    scripts = pyproject["project"]["scripts"]
    assert scripts["medautogrant"] == "med_autogrant.cli:entrypoint"

    pytest_options = pyproject["tool"]["pytest"]["ini_options"]
    assert pytest_options["cache_dir"] == "/tmp/med-autogrant-pytest-cache"


def test_sentrux_sidecar_is_not_a_tracked_structure_dependency() -> None:
    tracked = _tracked_files()

    assert ".sentrux/baseline.json" not in tracked
    assert ".sentrux/rules.toml" not in tracked
    assert ".github/workflows/sentrux-advisory.yml" not in tracked
    assert "scripts/run-structural-quality-gate.sh" not in tracked
    assert "scripts/run-opl-quality-details.sh" not in tracked


def test_mag_skill_keeps_authority_command_public_without_generic_shells() -> None:
    skill = _read("plugins/med-autogrant/skills/med-autogrant/SKILL.md")

    assert "med_autogrant.cli authority source-purity" in skill
    assert "uv run --directory <med-autogrant-repo>" not in skill
