from __future__ import annotations

import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_makefile_exposes_layered_test_entrypoints() -> None:
    makefile = _read("Makefile")

    assert "test-fast:" in makefile
    assert 'uv run pytest -q -m "not meta"' in makefile
    assert "test-line-budget:" in makefile
    assert "uv run python scripts/line_budget.py" in makefile
    line_budget_script = _read("scripts/check-line-budget.py")
    assert 'with_name("line_budget.py")' in line_budget_script
    assert "LEGACY_OVER_TARGET_BUDGETS" not in line_budget_script
    assert "test-family:" in makefile
    assert (
        "uv run pytest tests/test_repository_hygiene.py tests/test_test_command_surfaces.py "
        "tests/test_domain_entry.py tests/test_editable_shared_bootstrap.py -q"
    ) in makefile
    assert "test-meta:" in makefile
    assert "uv run pytest -q -m meta" in makefile
    assert "test-cli-smoke:" in makefile
    assert (
        "uv run pytest tests/test_cli_validate_workspace.py tests/test_local_runtime.py "
        "tests/test_hermes_runtime.py tests/test_product_entry.py -q"
    ) in makefile
    assert "test-full:" in makefile
    assert "uv run pytest -q" in makefile


def test_pyproject_registers_meta_marker() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    markers = pyproject["tool"]["pytest"]["ini_options"]["markers"]

    assert "meta: repo-tracked program control and repository hygiene checks" in markers


def test_verify_script_wraps_canonical_make_lanes() -> None:
    verify_script = _read("scripts/verify.sh")

    assert "make test-line-budget" in verify_script
    assert "make test-fast" in verify_script
    assert "make test-family" in verify_script
    assert "make test-meta" in verify_script
    assert "make test-cli-smoke" in verify_script
    assert "make test-full" in verify_script


def test_opl_module_healthcheck_uses_product_smoke_lane() -> None:
    healthcheck = _read("scripts/opl-module-healthcheck.sh")

    assert "python scripts/line_budget.py" in healthcheck
    assert "make test-cli-smoke" in healthcheck
    assert "make test-fast" not in healthcheck
    assert "make test-family" not in healthcheck
