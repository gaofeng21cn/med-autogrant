from __future__ import annotations

import json
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "mag"
PLUGIN_MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
PLUGIN_SKILL_PATH = PLUGIN_ROOT / "skills" / "mag" / "SKILL.md"
README_PATH = REPO_ROOT / "README.md"
INVARIANTS_PATH = REPO_ROOT / "docs" / "invariants.md"


def test_codex_plugin_manifest_tracks_repo_metadata_and_skill_layout() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    manifest = json.loads(PLUGIN_MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["name"] == "mag"
    assert manifest["version"] == pyproject_data["project"]["version"]
    assert manifest["repository"] == "https://github.com/gaofeng21cn/med-autogrant"
    assert manifest["skills"] == "./skills/"
    assert manifest["interface"]["displayName"] == "Med Auto Grant"
    assert manifest["interface"]["category"] == "Research"
    assert "domain app" in manifest["description"].lower()
    assert PLUGIN_SKILL_PATH.is_file()


def test_mag_skill_pins_domain_runtime_guardrails() -> None:
    skill_text = PLUGIN_SKILL_PATH.read_text(encoding="utf-8")

    assert "Domain runtime 护栏" in skill_text
    assert "必须通过 MAG product-entry、user-loop、direct-entry 或 schema-backed authoring contract 推进" in skill_text
    assert "不得用通用 `documents` / Office skill、直接编辑 `.docx`" in skill_text
    assert "ad-hoc 脚本、手写导出包或 prompt-only 文档路径" in skill_text
    assert "回到 repo 层补最小 callable/product-entry surface" in skill_text
    assert "不能成为绕开 runtime 的替代执行路径" in skill_text


def test_public_docs_pin_schema_backed_authoring_runtime_boundary() -> None:
    readme_text = README_PATH.read_text(encoding="utf-8")
    invariants_text = INVARIANTS_PATH.read_text(encoding="utf-8")

    assert "only those local scripts/contracts that are schema-backed" in readme_text
    assert "not alternate paths around the authoring runtime" in readme_text
    assert "local scripts/contracts only when schema-backed and surfaced through those runtime contracts" in readme_text
    assert "product-entry/user-loop surfaced local scripts/contracts" in invariants_text
    assert "不得作为绕开 authoring runtime 的 ad-hoc 执行路径" in invariants_text
