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
    assert "test-meta:" in makefile
    assert "uv run pytest -q -m meta" in makefile
    assert "test-cli-smoke:" in makefile
    assert "uv run pytest tests/test_cli_validate_workspace.py tests/test_local_runtime.py -q" in makefile
    assert "test-full:" in makefile
    assert "uv run pytest -q" in makefile


def test_pyproject_registers_meta_marker() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    markers = pyproject["tool"]["pytest"]["ini_options"]["markers"]

    assert "meta: repo-tracked program control and repository hygiene checks" in markers


def test_public_readmes_publish_layered_test_entrypoints() -> None:
    readme = _read("README.md")
    readme_zh = _read("README.zh-CN.md")

    for text in (readme, readme_zh):
        assert "make test-full" in text
        assert "make test-fast" in text
        assert "make test-meta" in text
        assert "make test-cli-smoke" in text


def test_root_agents_freezes_layered_test_governance() -> None:
    agents = _read("AGENTS.md")

    assert "`make test-fast` is the default developer slice and excludes the `meta` suite" in agents
    assert "`make test-meta` is reserved for repo-tracked program-control and repository-hygiene checks" in agents
    assert "`make test-cli-smoke` is the dedicated CLI/local-runtime smoke lane, and `make test-full` remains the clean-clone baseline" in agents
    assert "update `Makefile`, `pyproject.toml`, `README*`, runtime prompt docs, and command-surface tests together" in agents
