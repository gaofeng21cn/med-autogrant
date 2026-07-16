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
PRIMARY_SKILL_PATH = REPO_ROOT / "agent" / "primary_skill" / "SKILL.md"
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
PACKAGE_MANIFEST_PATH = REPO_ROOT / "contracts" / "opl_agent_package_manifest.json"
REPO_LOCAL_INSTALLER_PATHS = (
    REPO_ROOT / "scripts" / "install-codex-plugin.sh",
    REPO_ROOT / "src" / "med_autogrant" / "codex_plugin_installer.py",
)


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


def test_package_version_matches_python_plugin_and_owner_manifest() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    plugin_manifest = json.loads(PLUGIN_MANIFEST_PATH.read_text(encoding="utf-8"))
    package_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    init_text = (REPO_ROOT / "src" / "med_autogrant" / "__init__.py").read_text(
        encoding="utf-8"
    )
    version = pyproject_data["project"]["version"]

    assert version == "0.3.3"
    assert f'__version__ = "{version}"' in init_text
    assert plugin_manifest["version"] == version
    assert package_manifest["version"] == version
    assert "distribution_payload" not in package_manifest


def test_repo_does_not_track_repo_local_codex_marketplace() -> None:
    assert not MARKETPLACE_PATH.exists()


def test_agent_package_lifecycle_is_owned_by_opl_packages() -> None:
    package_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    lifecycle = package_manifest["lifecycle"]

    assert lifecycle == {
        "owner": "opl_packages",
        "module_id": "medautogrant",
        "commands": {
            "install": "opl packages install mag",
            "update": "opl packages update mag",
            "uninstall": "opl packages uninstall mag",
        },
        "repo_local_installer_allowed": False,
        "repo_local_marketplace_mutation_allowed": False,
        "repo_local_user_symlink_mutation_allowed": False,
    }
    assert all(not path.exists() for path in REPO_LOCAL_INSTALLER_PATHS)


def test_agent_package_uses_mag_identity_without_relabeling_carriers() -> None:
    pyproject_data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package_manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))

    assert package_manifest["agent_id"] == "mag"
    assert package_manifest["package_id"] == "mag"
    assert package_manifest["version"] == pyproject_data["project"]["version"]
    assert package_manifest["codex_surface"]["plugin_id"] == "med-autogrant"
    assert package_manifest["lifecycle"]["module_id"] == "medautogrant"
    assert "distribution_payload" not in package_manifest
    assert "opl-agent-med-autogrant" not in json.dumps(package_manifest)


def test_mag_skill_metadata_declares_app_skill_and_contract_surfaces() -> None:
    skill_text = PLUGIN_SKILL_PATH.read_text(encoding="utf-8")
    metadata_text = PLUGIN_SKILL_UI_METADATA_PATH.read_text(encoding="utf-8")
    pack_input = json.loads((REPO_ROOT / "contracts/pack_compiler_input.json").read_text())
    capability_map = json.loads((REPO_ROOT / "contracts/capability_map.json").read_text())
    action_catalog = json.loads((REPO_ROOT / "contracts/action_catalog.json").read_text())
    frontmatter_match = re.match(r"---\n(?P<frontmatter>.*?)\n---", skill_text, re.DOTALL)

    assert frontmatter_match is not None
    frontmatter = frontmatter_match.group("frontmatter")
    assert re.search(r"^name:\s*med-autogrant$", frontmatter, re.MULTILINE)
    assert pack_input["canonical_agent_id"] == "mag"

    primary_skill = next(
        capability
        for capability in capability_map["capabilities"]
        if capability["surface_role"] == "primary_skill"
    )
    carrier = primary_skill["carrier_projection_contract"]
    assert carrier["canonical_source"] == "agent/primary_skill/SKILL.md"
    assert carrier["carrier_skill_ref"] == "plugins/med-autogrant/skills/med-autogrant/SKILL.md"
    assert PRIMARY_SKILL_PATH.read_bytes() == PLUGIN_SKILL_PATH.read_bytes()

    for action in action_catalog["actions"]:
        assert action["execution_binding"] == {
            "kind": "stage_binding",
            "stage_manifest_ref": "agent/stages/manifest.json",
        }
        assert action["authority_boundary"]["domain_truth_owner"] == "med-autogrant"
        assert action["authority_boundary"]["opl_role"] == "projection_consumer_only"
        assert action["authority_boundary"]["write_policy"] == "no_domain_truth_writes"
        assert action["authority_boundary"]["opl_can_write_domain_truth"] is False
        assert action["supported_surfaces"]["mcp"]["descriptor_only"] is True
        assert action["supported_surfaces"]["mcp"]["public_runtime"] is False

    assert 'display_name: "Med Auto Grant"' in metadata_text
    assert "$med-autogrant" in metadata_text
