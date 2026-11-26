from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_MANIFEST_PATH = REPO_ROOT / "opl-package.json"


def test_repo_uses_v2_single_manifest_without_legacy_marketplace_mirrors() -> None:
    assert not (REPO_ROOT / ".agents").exists()
    assert not (REPO_ROOT / ".codex-plugin").exists()
    assert not (REPO_ROOT / "plugins").exists()
    assert not (REPO_ROOT / "app-contribution-adapter.json").exists()
    assert not (REPO_ROOT / "contracts" / "carrier_projection.json").exists()
    assert not (REPO_ROOT / "contracts" / "opl_agent_package_manifest.json").exists()

    manifest = json.loads(PACKAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "opl.package.v2"
    identity = manifest["identity"]
    assert identity["id"] == "mag"
    assert identity["intent"] == "agent"
    assert identity["name"]["en-US"] == "Med Auto Grant"
    assert (REPO_ROOT / identity["icon"]).is_file()

    codex = manifest["host_hints"]["codex"]
    assert codex["sync_enabled"] is True
    assert codex["plugin_name"] == "med-autogrant"
    assert codex["category"] == "Research"
    assert codex["capabilities"] == ["Interactive", "Write"]

    skills = manifest["provides"]["skills"]
    assert skills == [{"id": "med-autogrant", "path": "./skills/med-autogrant", "exposure": "default"}]
    assert (REPO_ROOT / "skills" / "med-autogrant" / "SKILL.md").is_file()

    handler = manifest["provides"]["contribution_handler"]
    assert handler == {
        "kind": "cli",
        "argv": ["python3", "./runtime/app_contribution.py"],
        "transport": "stdin_json_stdout_json",
    }
    assert (REPO_ROOT / "runtime" / "app_contribution.py").is_file()

    views = manifest["ui"]["declarative"]["views"]
    assert {view["data_ref"] for view in views} == {
        "mag.workspace.v1#route",
        "mag.workspace.v1#quality",
    }
    action_refs = {
        action["action_ref"]
        for view in views
        for action in view.get("actions", [])
    }
    assert action_refs == {"mag.workspace.v1#review.note"}
