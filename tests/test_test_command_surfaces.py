from __future__ import annotations

import os
import sys
import tomllib
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _make_dry_run(target: str) -> str:
    result = subprocess.run(
        ["make", "-n", target],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.stdout


def test_makefile_lanes_route_to_repo_native_checks() -> None:
    fast = _make_dry_run("test-fast")
    meta = _make_dry_run("test-meta")
    structure = _make_dry_run("test-structure")

    assert fast.count("run-pytest-clean.sh") == 1
    assert 'not meta and not regression' in fast
    assert "test-cli-smoke" not in fast

    assert "scripts/repo-hygiene.sh --fix" not in meta
    assert "scripts/repo-hygiene.sh" in meta
    assert "scripts/check_descriptor_contracts.py" in meta

    assert "scripts/check_descriptor_contracts.py" in structure
    assert "run-structural-quality-gate" not in structure
    assert "sentrux" not in structure.lower()


def test_clean_python_runners_route_caches_outside_checkout() -> None:
    python_runner = _read("scripts/run-python-clean.sh")

    subprocess.run(["bash", "-n", "scripts/run-python-clean.sh"], cwd=REPO_ROOT, check=True)
    subprocess.run(["bash", "-n", "scripts/run-pytest-clean.sh"], cwd=REPO_ROOT, check=True)
    assert "PYTHONDONTWRITEBYTECODE=1" in python_runner
    assert "PYTHONPYCACHEPREFIX" in python_runner
    assert 'venv_python="${repo_root}/.venv/bin/python"' not in python_runner


def test_clean_python_runner_resolves_framework_from_installed_opl(
    tmp_path: Path,
) -> None:
    framework_root = tmp_path / "framework"
    framework_package = framework_root / "python" / "opl_framework"
    framework_package.mkdir(parents=True)
    (framework_package / "__init__.py").write_text("", encoding="utf-8")
    (framework_package / "executor_client.py").write_text(
        'INSTALL_MARKER = "installed-opl-framework"\n',
        encoding="utf-8",
    )
    framework_bin = framework_root / "bin"
    framework_bin.mkdir()
    (framework_bin / "opl").write_text("#!/usr/bin/env bash\n", encoding="utf-8")

    install_root = tmp_path / "install"
    package_parent = install_root / "lib" / "node_modules"
    package_parent.mkdir(parents=True)
    (package_parent / "opl-framework").symlink_to(framework_root, target_is_directory=True)
    launcher_dir = install_root / "bin"
    launcher_dir.mkdir()
    opl_launcher = launcher_dir / "opl"
    opl_launcher.symlink_to("../lib/node_modules/opl-framework/bin/opl")

    env = os.environ.copy()
    env.pop("OPL_FRAMEWORK_ROOT", None)
    env.pop("OPL_OWNER_REPO_ROOT", None)
    env.pop("PYTHONPATH", None)
    env["OPL_BIN"] = str(opl_launcher)
    env["MAG_CLEAN_RUNNER_SKIP_SYNC"] = "1"
    env["UV_PROJECT_ENVIRONMENT"] = str(Path(sys.executable).parent.parent)
    result = subprocess.run(
        [
            "scripts/run-python-clean.sh",
            "-c",
            "from opl_framework.executor_client import INSTALL_MARKER; print(INSTALL_MARKER)",
        ],
        cwd=REPO_ROOT,
        env=env,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.stdout.strip() == "installed-opl-framework"


def test_pyproject_registers_cli_scripts_and_external_cache() -> None:
    pyproject = tomllib.loads(_read("pyproject.toml"))
    scripts = pyproject["project"]["scripts"]
    assert scripts == {"medautogrant": "med_autogrant.cli:entrypoint"}

    pytest_options = pyproject["tool"]["pytest"]["ini_options"]
    assert pytest_options["cache_dir"] == "/tmp/med-autogrant-pytest-cache"
