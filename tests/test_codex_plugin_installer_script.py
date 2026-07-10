from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = REPO_ROOT / "scripts" / "install-codex-plugin.sh"


def test_codex_plugin_installer_wrapper_smoke(tmp_path: Path) -> None:
    home = tmp_path / "home"
    home.mkdir()
    env = dict(os.environ, HOME=str(home))

    completed = subprocess.run(
        ["bash", str(INSTALLER_PATH), "--home", str(home), "--repo-root", str(REPO_ROOT)],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["plugin_root"] == str(REPO_ROOT / "plugins" / "med-autogrant")
    assert payload["plugin_manifest_path"].endswith("/.codex-plugin/plugin.json")
    assert payload["repo_local_marketplace_written"] == "false"
    assert payload["codex_marketplace_owner"] == "opl_owned_wrapper"
    assert not (home / "plugins" / "med-autogrant").exists()
    assert not (home / ".agents" / "plugins" / "marketplace.json").exists()
