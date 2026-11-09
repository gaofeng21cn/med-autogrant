from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"


def test_repo_marketplace_exposes_the_existing_codex_plugin_carrier() -> None:
    marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))

    assert marketplace["name"] == "med-autogrant"
    assert marketplace["interface"] == {"displayName": "Med Auto Grant"}
    assert marketplace["plugins"] == [
        {
            "name": "med-autogrant",
            "source": {
                "source": "local",
                "path": "./plugins/med-autogrant",
            },
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Research",
        }
    ]

    plugin_root = REPO_ROOT / marketplace["plugins"][0]["source"]["path"]
    plugin_manifest = json.loads(
        (plugin_root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    assert plugin_root.is_dir()
    assert plugin_manifest["name"] == "med-autogrant"
    assert plugin_manifest["interface"]["category"] == "Research"
    assert plugin_manifest["skills"] == "./skills/"
    carrier_descriptor = json.loads(
        (plugin_root / "opl-package.json").read_text(encoding="utf-8")
    )
    owner_descriptor = json.loads(
        (REPO_ROOT / "contracts/opl_agent_package_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert carrier_descriptor["package_id"] == owner_descriptor["package_id"]
    assert carrier_descriptor["version"] == owner_descriptor["version"]
    assert (
        carrier_descriptor["capability_dependencies"]
        == owner_descriptor["capability_dependencies"]
    )
    assert carrier_descriptor["app_contributions"] == owner_descriptor["app_contributions"]
    assert (
        carrier_descriptor["codex_surface"]["app_contribution_adapter"]
        == owner_descriptor["codex_surface"]["app_contribution_adapter"]
    )
    owner_adapter = json.loads(
        (REPO_ROOT / "app-contribution-adapter.json").read_text(encoding="utf-8")
    )
    carrier_adapter = json.loads(
        (plugin_root / "app-contribution-adapter.json").read_text(encoding="utf-8")
    )
    assert carrier_adapter == owner_adapter
    assert {
        entry["kind"] for entry in owner_adapter["reads"].values()
    } == {"command"}
    for entry in owner_adapter["reads"].values():
        assert entry["argv"][:2] == ["python3", "runtime/app_contribution.py"]
        assert "transform" not in entry
    assert set(owner_adapter["actions"]) == {"mag.workspace.v1#review.note"}
