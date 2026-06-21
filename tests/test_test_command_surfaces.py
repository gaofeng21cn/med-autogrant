from __future__ import annotations

import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_makefile_exposes_layered_test_entrypoints() -> None:
    makefile = _read("Makefile")

    assert "test-fast:" in makefile
    assert "PYTHON_CLEAN := ./scripts/run-python-clean.sh" in makefile
    assert "PYTEST_CLEAN := ./scripts/run-pytest-clean.sh" in makefile
    assert '$(PYTEST_CLEAN) -q -m "not meta and not regression and not proof"' in makefile
    assert "test-line-budget:" in makefile
    assert "$(PYTHON_CLEAN) scripts/line_budget.py" in makefile
    assert "test-line-budget-strict:" in makefile
    assert "$(PYTHON_CLEAN) scripts/line_budget.py --strict" in makefile
    assert "test-cli-smoke:" in makefile
    assert "$(PYTEST_CLEAN) -q -m smoke" in makefile
    assert "test-regression:" in makefile
    assert '$(PYTEST_CLEAN) -q -m "regression and not proof"' in makefile
    assert "test-proof:" in makefile
    assert "MAG_CLEAN_RUNNER_UV_EXTRA=proof $(PYTEST_CLEAN) -q -m proof" in makefile
    assert "test-family:" in makefile
    assert (
        "$(PYTEST_CLEAN) tests/test_repository_hygiene.py tests/test_test_command_surfaces.py "
        'tests/test_domain_entry.py tests/test_editable_shared_bootstrap.py -q -m "not proof"'
    ) in makefile
    assert "test-meta:" in makefile
    assert "$(PYTEST_CLEAN) -q -m meta" in makefile
    assert "test-full:" in makefile
    assert '$(PYTEST_CLEAN) -q -m "not proof"' in makefile


def test_clean_python_runners_route_caches_outside_checkout() -> None:
    python_runner = _read("scripts/run-python-clean.sh")
    pytest_runner = _read("scripts/run-pytest-clean.sh")

    assert "PYTHONDONTWRITEBYTECODE=1" in python_runner
    assert "PYTHONPYCACHEPREFIX" in python_runner
    assert 'path_is_inside_checkout "${UV_PROJECT_ENVIRONMENT:-}"' in python_runner
    assert 'path_is_inside_checkout "${PYTHONPYCACHEPREFIX:-}"' in python_runner
    assert 'export UV_PROJECT_ENVIRONMENT="${UV_PROJECT_ENVIRONMENT:-${tmp_root}/venv}"' in python_runner
    assert "MED_AUTOGRANT_EDITABLE_SHARED_ENV_ROOT" in _read("src/med_autogrant/editable_shared_bootstrap.py")
    assert "-p no:cacheprovider -o cache_dir=${tmp_root}/pytest-cache" in python_runner
    assert "uv sync --frozen --group dev --no-install-project --inexact" in python_runner
    assert 'venv_python="${UV_PROJECT_ENVIRONMENT}/bin/python"' in python_runner
    assert 'venv_python="${repo_root}/.venv/bin/python"' not in python_runner
    assert "-m pytest" in pytest_runner


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

    assert "make test-line-budget" in verify_script
    assert "make test-line-budget-strict" not in verify_script
    assert "make test-fast" in verify_script
    assert "make test-family" in verify_script
    assert "make test-meta" in verify_script
    assert "make test-cli-smoke" in verify_script
    assert "make test-regression" in verify_script
    assert "make test-proof" in verify_script
    assert "make test-full" in verify_script
    assert 'lane" == "cleanup"' in verify_script
    assert "scripts/repo-hygiene.sh --fix" in verify_script
    assert "scripts/repo-hygiene.sh" in verify_script
    assert "python scripts/line_budget.py" not in verify_script
    assert (
        "Usage: $0 [fast|smoke|cli-smoke|family|meta|regression|proof|structure|"
        "source-purity|source-purity:strict|full|cleanup]"
    ) in verify_script


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
    skill = _read("plugins/mag/skills/mag/SKILL.md")

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
