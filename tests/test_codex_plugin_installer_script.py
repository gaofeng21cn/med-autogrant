from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import sys
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = REPO_ROOT / "scripts" / "install-codex-plugin.sh"


def test_codex_plugin_installer_script_keeps_codex_paths_repo_local(tmp_path: Path) -> None:
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
    assert payload["plugin_root"] == str(REPO_ROOT / "plugins" / "mag")
    assert not (home_dir / "plugins" / "mag").exists()
    assert not (home_dir / ".agents" / "skills" / "mag").exists()
    assert not (home_dir / ".agents" / "plugins" / "marketplace.json").exists()
    assert (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").exists()


def test_codex_plugin_installer_script_skip_tools_does_not_require_shared_runtime_dependency(
    tmp_path: Path,
) -> None:
    home_dir = tmp_path / "home"
    repo_copy = tmp_path / "repo"
    temp_bin = tmp_path / "bin"
    home_dir.mkdir()
    temp_bin.mkdir()

    shutil.copytree(REPO_ROOT / "src" / "med_autogrant", repo_copy / "src" / "med_autogrant")
    shutil.copytree(REPO_ROOT / "plugins" / "mag", repo_copy / "plugins" / "mag")

    python_wrapper = temp_bin / "python3"
    python_wrapper.write_text(
        "#!/bin/sh\n"
        f"exec {sys.executable!r} -S \"$@\"\n",
        encoding="utf-8",
    )
    python_wrapper.chmod(0o755)

    env = os.environ.copy()
    env["HOME"] = str(home_dir)
    env["PATH"] = f"{temp_bin}:/bin:/usr/bin:/usr/sbin:/sbin"
    env["PYTHONNOUSERSITE"] = "1"
    env.pop("PYTHONPATH", None)
    env.pop("VIRTUAL_ENV", None)

    result = subprocess.run(
        [
            "bash",
            str(INSTALLER_PATH),
            "--home",
            str(home_dir),
            "--repo-root",
            str(repo_copy),
            "--skip-tools",
        ],
        cwd=repo_copy,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["plugin_root"] == str(repo_copy / "plugins" / "mag")
    assert (repo_copy / ".agents" / "plugins" / "marketplace.json").exists()
