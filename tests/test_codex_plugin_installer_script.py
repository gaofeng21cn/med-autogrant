from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import sys
import subprocess
import tomllib


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_PATH = REPO_ROOT / "scripts" / "install-codex-plugin.sh"
PLUGIN_DIR = "med-autogrant"


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
        ],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["plugin_root"] == str(REPO_ROOT / "plugins" / PLUGIN_DIR)
    assert not (home_dir / "plugins" / PLUGIN_DIR).exists()
    assert not (home_dir / ".agents" / "skills" / "mag").exists()
    assert not (home_dir / ".agents" / "plugins" / "marketplace.json").exists()
    assert not (REPO_ROOT / ".agents" / "plugins" / "marketplace.json").exists()
    assert payload["plugin_manifest_path"] == str(
        REPO_ROOT / "plugins" / PLUGIN_DIR / ".codex-plugin" / "plugin.json"
    )
    assert payload["repo_local_marketplace_written"] == "false"
    assert payload["codex_marketplace_owner"] == "opl_owned_wrapper"


def test_codex_plugin_installer_leaves_cli_installation_to_python_packaging(tmp_path: Path) -> None:
    home_dir = tmp_path / "home"
    fake_bin = tmp_path / "bin"
    home_dir.mkdir()
    fake_bin.mkdir()
    (fake_bin / "uv").write_text(
        "#!/usr/bin/env bash\n"
        "echo 'uv must not be invoked by wrapper-only install' >&2\n"
        "exit 99\n",
        encoding="utf-8",
    )
    (fake_bin / "uv").chmod(0o755)

    env = os.environ.copy()
    env["HOME"] = str(home_dir)
    env["PATH"] = f"{fake_bin}:{env['PATH']}"

    result = subprocess.run(
        ["bash", str(INSTALLER_PATH), "--home", str(home_dir), "--repo-root", str(REPO_ROOT)],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert pyproject["project"]["scripts"]["medautogrant"] == "med_autogrant.cli:entrypoint"
    assert not (home_dir / ".local" / "bin" / "medautogrant").exists()
    assert "uv tool install" not in INSTALLER_PATH.read_text(encoding="utf-8")
    assert "--editable" not in INSTALLER_PATH.read_text(encoding="utf-8")


def test_codex_plugin_installer_script_does_not_require_shared_runtime_dependency(
    tmp_path: Path,
) -> None:
    home_dir = tmp_path / "home"
    repo_copy = tmp_path / "repo"
    temp_bin = tmp_path / "bin"
    home_dir.mkdir()
    temp_bin.mkdir()

    shutil.copytree(REPO_ROOT / "src" / "med_autogrant", repo_copy / "src" / "med_autogrant")
    shutil.copytree(REPO_ROOT / "plugins" / PLUGIN_DIR, repo_copy / "plugins" / PLUGIN_DIR)

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
        ],
        cwd=repo_copy,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["plugin_root"] == str(repo_copy / "plugins" / PLUGIN_DIR)
    assert payload["plugin_manifest_path"] == str(
        repo_copy / "plugins" / PLUGIN_DIR / ".codex-plugin" / "plugin.json"
    )
    assert payload["repo_local_marketplace_written"] == "false"
    assert payload["codex_marketplace_owner"] == "opl_owned_wrapper"
    assert not (repo_copy / ".agents" / "plugins" / "marketplace.json").exists()
