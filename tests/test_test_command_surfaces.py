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

    assert "默认最小验证入口是 `scripts/verify.sh`" in agents
    assert "默认 smoke 是 `make test-fast`" in agents
    assert "`make test-meta` 与 `make test-cli-smoke` 是显式 lane" in agents
    assert "`make test-full` 是 clean-clone 基线" in agents
    assert "必须与 `Makefile`、`pyproject.toml`、`README*` 与命令面测试保持一致" in agents


def test_verify_script_wraps_canonical_make_lanes() -> None:
    verify_script = _read("scripts/verify.sh")

    assert "make test-fast" in verify_script
    assert "make test-meta" in verify_script
    assert "make test-cli-smoke" in verify_script
    assert "make test-full" in verify_script


def test_docs_index_publishes_core_maintainer_working_set() -> None:
    docs_readme = _read("docs/README.md")
    docs_readme_zh = _read("docs/README.zh-CN.md")

    for text in (docs_readme, docs_readme_zh):
        assert "project.md" in text
        assert "status.md" in text
        assert "architecture.md" in text
        assert "invariants.md" in text
        assert "decisions.md" in text
