from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "med-autogrant"
PLUGIN_MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
PLUGIN_ICON_PATH = PLUGIN_ROOT / "assets" / "icon.png"
PLUGIN_ICON_SOURCE_PATH = PLUGIN_ROOT / "assets" / "icon.svg"
PLUGIN_SKILL_PATH = PLUGIN_ROOT / "skills" / "med-autogrant" / "SKILL.md"
PLUGIN_SKILL_UI_METADATA_PATH = PLUGIN_ROOT / "skills" / "med-autogrant" / "agents" / "openai.yaml"
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"


def test_codex_plugin_manifest_tracks_repo_metadata_and_skill_layout() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    manifest = json.loads(PLUGIN_MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["name"] == "med-autogrant"
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
    icon_source = PLUGIN_ICON_SOURCE_PATH.read_text(encoding="utf-8")
    assert '<rect width="512" height="512" rx="112"' in icon_source
    assert 'stroke-width="42"' in icon_source
    assert 'stroke="#FFE08A"' in icon_source
    assert PLUGIN_SKILL_PATH.is_file()
    assert PLUGIN_SKILL_UI_METADATA_PATH.is_file()


def test_repo_does_not_track_repo_local_codex_marketplace() -> None:
    assert not MARKETPLACE_PATH.exists()


def test_mag_skill_metadata_declares_app_skill_and_contract_surfaces() -> None:
    skill_text = PLUGIN_SKILL_PATH.read_text(encoding="utf-8")
    metadata_text = PLUGIN_SKILL_UI_METADATA_PATH.read_text(encoding="utf-8")
    frontmatter_match = re.match(r"---\n(?P<frontmatter>.*?)\n---", skill_text, re.DOTALL)

    assert frontmatter_match is not None
    frontmatter = frontmatter_match.group("frontmatter")
    assert re.search(r"^name:\s*med-autogrant$", frontmatter, re.MULTILINE)
    assert "domain entry" in frontmatter
    assert "authority targets" in frontmatter
    assert "schema-backed contracts" in frontmatter
    for command_surface in (
        "workspace route-report",
        "workspace quality-scorecard",
        "pass revision",
        "package submission-ready",
        "authority memory-proposal",
        "authority memory-decision",
        "authority source-purity",
    ):
        assert (
            f"<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli {command_surface}"
            in skill_text
        )
    assert "descriptor_only=true" in skill_text
    assert "public_runtime=false" in skill_text
    assert 'display_name: "Med Auto Grant"' in metadata_text
    assert 'default_prompt: "Use $med-autogrant' in metadata_text
    assert "$mag alias remains supported" in metadata_text
