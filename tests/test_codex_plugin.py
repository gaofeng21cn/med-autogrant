from __future__ import annotations

import json
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "mag"
PLUGIN_MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
PLUGIN_SKILL_PATH = PLUGIN_ROOT / "skills" / "mag" / "SKILL.md"


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
