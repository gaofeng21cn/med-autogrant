from __future__ import annotations

from pathlib import Path

import med_autogrant.codex_plugin_installer as installer


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_plugin_install_preserves_user_skill_removes_legacy_and_is_idempotent(tmp_path: Path) -> None:
    legacy_home = tmp_path / "legacy-home"
    legacy_target = tmp_path / "legacy-target"
    legacy_target.mkdir()
    for link in (
        legacy_home / "plugins" / "mag",
        legacy_home / ".agents" / "skills" / "mag",
    ):
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(legacy_target)
    stub = legacy_home / ".codex" / "skills" / "mag"
    stub.mkdir(parents=True)
    (stub / "SKILL.md").write_text(
        "---\nname: mag\ndescription: mag test skill\n---\n\n# mag\n",
        encoding="utf-8",
    )

    first = installer.install_repo_local_codex_plugin(repo_root=REPO_ROOT, home=legacy_home)
    second = installer.install_repo_local_codex_plugin(repo_root=REPO_ROOT, home=legacy_home)

    assert not (legacy_home / "plugins" / "mag").exists()
    assert not (legacy_home / ".agents" / "skills" / "mag").exists()
    assert not stub.exists()
    assert first == second
    assert first["plugin_root"] == str(REPO_ROOT / "plugins" / "med-autogrant")
    assert first["plugin_manifest_path"] == str(
        REPO_ROOT / "plugins" / "med-autogrant" / ".codex-plugin" / "plugin.json"
    )
    assert first["skill_root"] == str(
        REPO_ROOT / "plugins" / "med-autogrant" / "skills" / "med-autogrant"
    )
    assert first["repo_local_marketplace_written"] == "false"
    assert first["codex_marketplace_owner"] == "opl_owned_wrapper"
    assert not (legacy_home / "plugins" / "med-autogrant").exists()
    assert not (legacy_home / ".codex" / "skills" / "med-autogrant").exists()

    user_home = tmp_path / "user-home"
    user_skill = user_home / ".codex" / "skills" / "mag"
    user_skill.mkdir(parents=True)
    skill_text = "---\nname: mag\ndescription: custom local MAG skill\n---\n"
    (user_skill / "SKILL.md").write_text(skill_text, encoding="utf-8")

    installer.install_repo_local_codex_plugin(repo_root=REPO_ROOT, home=user_home)

    assert (user_skill / "SKILL.md").read_text(encoding="utf-8") == skill_text
    assert not (user_home / ".codex" / "skills" / "med-autogrant").exists()
