from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = REPO_ROOT / "scripts" / "install-codex-plugin.sh"


def test_codex_plugin_installer_script_supports_lightweight_skip_tools_path(tmp_path: Path) -> None:
    home_dir = tmp_path / "home"
    home_dir.mkdir()

    env = os.environ.copy()
    env["HOME"] = str(home_dir)

    result = subprocess.run(
        [
            "bash",
            str(INSTALLER_PATH),
            "--home",
            str(home_dir),
            "--repo-root",
            str(REPO_ROOT),
            "--skip-tools",
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["plugin_root"] == str(home_dir / "plugins" / "med-autogrant")
    assert (home_dir / "plugins" / "med-autogrant").is_symlink()
    assert (home_dir / ".agents" / "skills" / "med-autogrant").is_symlink()
    assert (home_dir / ".agents" / "plugins" / "marketplace.json").exists()
