from __future__ import annotations

import json
from pathlib import Path

import med_autogrant.codex_plugin_installer as codex_plugin_installer


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_install_repo_local_codex_plugin_uses_repo_local_plugin_and_marketplace(tmp_path: Path) -> None:
    home = tmp_path / "home"
    legacy_plugin_link = home / "plugins" / "mag"
    legacy_skill_link = home / ".agents" / "skills" / "mag"
    legacy_target = tmp_path / "legacy-target"
    legacy_target.mkdir()
    legacy_plugin_link.parent.mkdir(parents=True)
    legacy_skill_link.parent.mkdir(parents=True)
    legacy_plugin_link.symlink_to(legacy_target)
    legacy_skill_link.symlink_to(legacy_target)
    legacy_marketplace_path = home / ".agents" / "plugins" / "marketplace.json"
    legacy_marketplace_path.parent.mkdir(parents=True)
    legacy_marketplace_path.write_text(
        json.dumps({"plugins": [{"name": "mag", "source": {"path": "./plugins/mag"}}]}),
        encoding="utf-8",
    )

    result = codex_plugin_installer.install_repo_local_codex_plugin(repo_root=REPO_ROOT, home=home)

    plugin_link = home / "plugins" / "med-autogrant"
    skill_link = home / ".agents" / "skills" / "med-autogrant"
    marketplace_path = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"

    assert not legacy_plugin_link.exists()
    assert not legacy_skill_link.exists()
    assert result["plugin_root"] == str(REPO_ROOT / "plugins" / "med-autogrant")
    assert result["plugin_manifest_path"] == str(
        REPO_ROOT / "plugins" / "med-autogrant" / ".codex-plugin" / "plugin.json"
    )
    assert result["skill_root"] == str(REPO_ROOT / "plugins" / "med-autogrant" / "skills" / "med-autogrant")
    assert not plugin_link.exists()
    assert not skill_link.exists()
    assert not marketplace_path.exists()
    assert result["repo_local_marketplace_written"] == "false"
    assert result["codex_marketplace_owner"] == "opl_owned_wrapper"


def test_install_repo_local_codex_plugin_keeps_skill_repo_local(tmp_path: Path) -> None:
    home = tmp_path / "home"

    result = codex_plugin_installer.install_repo_local_codex_plugin(repo_root=REPO_ROOT, home=home)

    assert not (home / ".agents" / "skills" / "med-autogrant").exists()
    assert not (home / ".codex" / "skills" / "med-autogrant").exists()
    assert result["skill_root"] == str(REPO_ROOT / "plugins" / "med-autogrant" / "skills" / "med-autogrant")


def test_install_repo_local_codex_plugin_removes_legacy_test_skill_stub(tmp_path: Path) -> None:
    home = tmp_path / "home"
    stub = home / ".codex" / "skills" / "mag"
    stub.mkdir(parents=True)
    (stub / "SKILL.md").write_text(
        "---\nname: mag\ndescription: mag test skill\n---\n\n# mag\n",
        encoding="utf-8",
    )

    codex_plugin_installer.install_repo_local_codex_plugin(repo_root=REPO_ROOT, home=home)

    assert not stub.exists()


def test_install_repo_local_codex_plugin_preserves_non_stub_user_skill(tmp_path: Path) -> None:
    home = tmp_path / "home"
    skill = home / ".codex" / "skills" / "mag"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: mag\ndescription: custom local MAG skill\n---\n\n# mag\n",
        encoding="utf-8",
    )

    codex_plugin_installer.install_repo_local_codex_plugin(repo_root=REPO_ROOT, home=home)

    assert skill.exists()
    assert "custom local MAG skill" in (skill / "SKILL.md").read_text(encoding="utf-8")


def test_install_repo_local_codex_plugin_is_idempotent(tmp_path: Path) -> None:
    home = tmp_path / "home"

    first = codex_plugin_installer.install_repo_local_codex_plugin(repo_root=REPO_ROOT, home=home)
    second = codex_plugin_installer.install_repo_local_codex_plugin(repo_root=REPO_ROOT, home=home)

    assert first["marketplace_path"] == second["marketplace_path"]
    assert first["plugin_root"] == second["plugin_root"]
    assert first["plugin_manifest_path"] == second["plugin_manifest_path"]
    assert first["skill_root"] == second["skill_root"]
