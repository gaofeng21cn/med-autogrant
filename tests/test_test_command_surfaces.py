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
    fast = _make_dry_run("test-fast")
    structure = _make_dry_run("test-structure")
    structure_strict = _make_dry_run("test-structure-strict")

    assert "scripts/line_budget.py" in fast
    assert "-m smoke" in fast
    assert "not meta and not regression and not proof" in fast

    assert "scripts/line_budget.py" in structure
    assert "scripts/check_generated_aggregate_sources.py" in structure
    assert "scripts/check_source_purity_guard.py" in structure
    assert "run-structural-quality-gate" not in structure
    assert "sentrux" not in structure.lower()

    assert "scripts/line_budget.py --strict" in structure_strict
    assert "scripts/check_source_purity_guard.py" in structure_strict
    assert "scripts/check_generated_aggregate_sources.py" in structure_strict


def test_clean_python_runners_route_caches_outside_checkout() -> None:
    python_runner = _read("scripts/run-python-clean.sh")

    subprocess.run(["bash", "-n", "scripts/run-python-clean.sh"], cwd=REPO_ROOT, check=True)
    subprocess.run(["bash", "-n", "scripts/run-pytest-clean.sh"], cwd=REPO_ROOT, check=True)
    assert "PYTHONDONTWRITEBYTECODE=1" in python_runner
    assert "PYTHONPYCACHEPREFIX" in python_runner
    assert "MED_AUTOGRANT_EDITABLE_SHARED_ENV_ROOT" in _read("src/med_autogrant/editable_shared_bootstrap.py")
    assert 'venv_python="${repo_root}/.venv/bin/python"' not in python_runner


def test_pyproject_registers_test_lane_markers() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    scripts = pyproject["project"]["scripts"]
    assert scripts["medautogrant"] == "med_autogrant.cli:entrypoint"
    assert scripts["mag"] == "med_autogrant.cli:entrypoint"
    pytest_options = pyproject["tool"]["pytest"]["ini_options"]
    markers = pytest_options["markers"]

    assert pytest_options["cache_dir"] == "/tmp/med-autogrant-pytest-cache"
    assert "meta: repo-tracked program control and repository hygiene checks" in markers
    assert (
        "smoke: minimal default CLI/product entry health checks that do not require optional proof dependencies"
        in markers
    )
    assert "integration: cross-surface integration checks that are broader than unit contracts" in markers
    assert (
        "regression: heavier matrix, provenance oracle, runtime/export, and product regression checks"
        in markers
    )
    assert "proof: explicit optional hosted/Hermes proof lane that may require optional dependencies" in markers
    assert "structure: repository structure and architecture governance checks" in markers


def test_verify_script_wraps_canonical_make_lanes() -> None:
    verify_script = _read("scripts/verify.sh")

    subprocess.run(["bash", "-n", "scripts/verify.sh"], cwd=REPO_ROOT, check=True)
    assert "make test-line-budget" in verify_script
    assert "make test-fast" in verify_script
    assert "make test-family" in verify_script
    assert "make test-meta" in verify_script
    assert "make test-cli-smoke" in verify_script
    assert "make test-regression" in verify_script
    assert "make test-proof" in verify_script
    assert "make test-full" in verify_script
    assert "make test-structure" in verify_script
    assert 'lane" == "cleanup"' in verify_script
    assert "scripts/repo-hygiene.sh --fix" in verify_script
    assert "scripts/repo-hygiene.sh" in verify_script
    assert "python scripts/line_budget.py" not in verify_script
    assert "sentrux" not in verify_script.lower()


def test_sentrux_sidecar_is_not_a_tracked_structure_dependency() -> None:
    tracked = _tracked_files()

    assert ".sentrux/baseline.json" not in tracked
    assert ".sentrux/rules.toml" not in tracked
    assert ".github/workflows/sentrux-advisory.yml" not in tracked
    assert "scripts/run-structural-quality-gate.sh" not in tracked
    assert "scripts/run-opl-quality-details.sh" not in tracked


def test_product_entry_cases_are_direct_regression_cases() -> None:
    conftest = _read("tests/conftest.py")

    assert 'relative_path.startswith("tests/product_entry_cases/")' in conftest
    assert "PRODUCT_ENTRY_AGGREGATOR" not in conftest
    assert "pytest_ignore_collect" not in conftest


def test_opl_module_healthcheck_uses_product_smoke_lane() -> None:
    healthcheck = _read("scripts/opl-module-healthcheck.sh")

    assert 'export PATH="${HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:${PATH}"' in healthcheck
    assert "command -v python3" in healthcheck
    assert "command -v uv" in healthcheck
    assert "python3 scripts/line_budget.py" in healthcheck
    assert "python3 scripts/line_budget.py --strict" not in healthcheck
    assert "make test-cli-smoke" in healthcheck
    assert "make test-fast" not in healthcheck
    assert "make test-family" not in healthcheck


def test_mag_skill_keeps_generic_shells_out_of_repo_local_public_commands() -> None:
    skill = _read("plugins/med-autogrant/skills/med-autogrant/SKILL.md")

    expected_public_command_surfaces = (
        "foundry status",
        "foundry inspect",
        "foundry interfaces",
        "foundry validate",
        "foundry doctor",
        "foundry peers",
        "status",
        "workspace route-report",
        "workspace quality-scorecard",
        "pass revision",
        "package submission-ready",
        "authority memory-proposal",
        "authority memory-decision",
        "authority source-purity",
    )
    command_lines = [
        line
        for line in skill.splitlines()
        if line.startswith("- `<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli ")
    ]
    for command_surface in expected_public_command_surfaces:
        assert f"<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli {command_surface}" in skill
    assert len(command_lines) == len(expected_public_command_surfaces)
    assert "uv run --directory <med-autogrant-repo>" not in skill
