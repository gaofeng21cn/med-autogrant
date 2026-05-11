from __future__ import annotations

import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_makefile_exposes_layered_test_entrypoints() -> None:
    makefile = _read("Makefile")

    assert "test-fast:" in makefile
    assert 'uv run pytest -q -m "not meta and not regression and not proof"' in makefile
    assert "test-line-budget:" in makefile
    assert "uv run python scripts/line_budget.py" in makefile
    assert "test-cli-smoke:" in makefile
    assert "uv run pytest -q -m smoke" in makefile
    assert "test-regression:" in makefile
    assert 'uv run pytest -q -m "regression and not proof"' in makefile
    assert "test-proof:" in makefile
    assert "uv run --extra proof pytest -q -m proof" in makefile
    assert "test-family:" in makefile
    assert (
        "uv run pytest tests/test_repository_hygiene.py tests/test_test_command_surfaces.py "
        "tests/test_domain_entry.py tests/test_editable_shared_bootstrap.py -q"
    ) in makefile
    assert "test-meta:" in makefile
    assert "uv run pytest -q -m meta" in makefile
    assert "test-full:" in makefile
    assert 'uv run pytest -q -m "not proof"' in makefile


def test_pyproject_registers_test_lane_markers() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    markers = pyproject["tool"]["pytest"]["ini_options"]["markers"]

    assert "meta: repo-tracked program control and repository hygiene checks" in markers
    assert (
        "smoke: minimal default CLI/product entry health checks that do not require optional proof dependencies"
        in markers
    )
    assert "integration: cross-surface integration checks that are broader than unit contracts" in markers
    assert (
        "regression: heavier matrix, historical compatibility, runtime/export, and product regression checks"
        in markers
    )
    assert "proof: explicit optional hosted/Hermes proof lane that may require optional dependencies" in markers
    assert "structure: repository structure and architecture governance checks" in markers


def test_verify_script_wraps_canonical_make_lanes() -> None:
    verify_script = _read("scripts/verify.sh")

    assert "make test-line-budget" in verify_script
    assert "make test-fast" in verify_script
    assert "make test-family" in verify_script
    assert "make test-meta" in verify_script
    assert "make test-cli-smoke" in verify_script
    assert "make test-regression" in verify_script
    assert "make test-proof" in verify_script
    assert "make test-full" in verify_script
    assert "python scripts/line_budget.py" not in verify_script
    assert "Usage: $0 [fast|smoke|cli-smoke|family|meta|regression|proof|structure|full]" in verify_script


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
    assert "make test-cli-smoke" in healthcheck
    assert "make test-fast" not in healthcheck
    assert "make test-family" not in healthcheck


def test_mag_skill_registers_repo_local_product_entry_commands() -> None:
    skill = _read("plugins/mag/skills/mag/SKILL.md")

    for command_surface in (
        "product skill-catalog",
        "product status",
        "product user-loop",
        "product direct-entry",
    ):
        assert f"uv run --directory <med-autogrant-repo> medautogrant {command_surface}" in skill
