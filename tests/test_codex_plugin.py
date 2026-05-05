from __future__ import annotations

import json
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "mag"
PLUGIN_MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
PLUGIN_ICON_PATH = PLUGIN_ROOT / "assets" / "icon.png"
PLUGIN_ICON_SOURCE_PATH = PLUGIN_ROOT / "assets" / "icon.svg"
PLUGIN_SKILL_PATH = PLUGIN_ROOT / "skills" / "mag" / "SKILL.md"
PLUGIN_SKILL_UI_METADATA_PATH = PLUGIN_ROOT / "skills" / "mag" / "agents" / "openai.yaml"
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"


def test_codex_plugin_manifest_tracks_repo_metadata_and_skill_layout() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    manifest = json.loads(PLUGIN_MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["name"] == "mag"
    assert manifest["version"] == pyproject_data["project"]["version"]
    assert manifest["repository"] == "https://github.com/gaofeng21cn/med-autogrant"
    assert manifest["skills"] == "./skills/"
    assert manifest["interface"]["displayName"] == "Med Auto Grant"
    assert manifest["interface"]["category"] == "Research"
    assert manifest["interface"]["composerIcon"] == "./assets/icon.png"
    assert manifest["interface"]["logo"] == "./assets/icon.png"
    assert "domain app" in manifest["description"].lower()
    assert PLUGIN_ICON_PATH.is_file()
    assert PLUGIN_ICON_SOURCE_PATH.is_file()
    assert PLUGIN_SKILL_PATH.is_file()
    assert PLUGIN_SKILL_UI_METADATA_PATH.is_file()


def test_codex_plugin_marketplace_uses_full_display_name() -> None:
    marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
    plugin_entry = next(item for item in marketplace["plugins"] if item["name"] == "mag")

    assert marketplace["interface"]["displayName"] == "Med Auto Grant Local"
    assert plugin_entry["source"] == {
        "source": "local",
        "path": "./plugins/mag",
    }
    assert plugin_entry["category"] == "Research"


def test_mag_skill_pins_domain_runtime_guardrails() -> None:
    skill_text = PLUGIN_SKILL_PATH.read_text(encoding="utf-8")
    metadata_text = PLUGIN_SKILL_UI_METADATA_PATH.read_text(encoding="utf-8")

    assert "Domain runtime 护栏" in skill_text
    assert "必须通过 MAG product-entry、user-loop、direct-entry 或 schema-backed authoring contract 推进" in skill_text
    assert "不得用通用 `documents` / Office skill、直接编辑 `.docx`" in skill_text
    assert "ad-hoc 脚本、手写导出包或 prompt-only 文档路径" in skill_text
    assert "回到 repo 层补最小 callable/product-entry surface" in skill_text
    assert "不能成为绕开 runtime 的替代执行路径" in skill_text
    assert 'display_name: "Med Auto Grant"' in metadata_text
    assert 'default_prompt: "Use $mag' in metadata_text
