from __future__ import annotations

import json
import os
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import pytest

import med_autogrant.__main__ as main_module
import med_autogrant.cli as cli_module
from med_autogrant.cli import main


REPO_ROOT = Path(__file__).resolve().parents[1]
CRITIQUE_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_critique.json"
REVISION_EXAMPLE_PATH = REPO_ROOT / "examples" / "nsfc_workspace_p2c_revision.json"


def _run_cli(*args: str) -> tuple[int, str, str]:
    stdout = StringIO()
    stderr = StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            exit_code = main(list(args))
        except SystemExit as exc:
            exit_code = int(exc.code)
    return exit_code, stdout.getvalue(), stderr.getvalue()


def _run_json_cli(*args: str) -> dict[str, object]:
    exit_code, stdout, stderr = _run_cli(*args)
    assert exit_code == 0
    assert stderr == ""
    return json.loads(stdout)


@pytest.mark.smoke
def test_module_entrypoint_reuses_cli_entrypoint() -> None:
    assert main_module.entrypoint is cli_module.entrypoint


@pytest.mark.smoke
def test_public_cli_help_renders_group_index() -> None:
    exit_code, stdout, stderr = _run_cli("--help")

    assert exit_code == 0
    assert stderr == ""
    assert "Med Auto Grant domain authority CLI" in stdout
    assert "Agent id: mag" in stdout
    assert "OPL public inspection: opl foundry agents inspect mag --json" in stdout
    assert "Authority boundary:" in stdout
    assert "Public command groups:" in stdout
    assert "\n  foundry" not in stdout
    assert "workspace" in stdout
    assert "authority" in stdout
    assert "product" not in stdout
    assert "\n  mainline        " not in stdout
    assert "runtime" not in stdout


@pytest.mark.smoke
def test_repo_local_clean_runner_is_cwd_independent(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["MAG_CLEAN_RUNNER_SKIP_SYNC"] = "1"
    env.setdefault("UV_PROJECT_ENVIRONMENT", sys.prefix)

    result = subprocess.run(
        [
            str(REPO_ROOT / "scripts" / "run-python-clean.sh"),
            "-m",
            "med_autogrant.cli",
            "workspace",
            "validate",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH),
            "--format",
            "json",
        ],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["command"] == "validate-workspace"
    assert payload["workspace_id"] == "nsfc-demo-001"


@pytest.mark.smoke
def test_pass_group_help_renders_canonical_commands() -> None:
    exit_code, stdout, stderr = _run_cli("pass", "--help")
    assert exit_code == 0
    assert stderr == ""
    assert "\n  revision\n" in stdout
    assert "\n  critique\n" in stdout
    assert "\n  freeze\n" in stdout
    assert "critique-loop" not in stdout
    assert "mainline-loop" not in stdout


@pytest.mark.smoke
def test_workspace_validate_accepts_canonical_critique_workspace() -> None:
    payload = _run_json_cli(
        "workspace",
        "validate",
        "--input",
        str(CRITIQUE_EXAMPLE_PATH),
        "--format",
        "json",
    )

    assert payload["ok"] is True
    assert payload["command"] == "validate-workspace"
    assert payload["grant_run_id"] == "grant-run-nsfc-demo-001-baseline-001"
    assert payload["workspace_id"] == "nsfc-demo-001"
    assert payload["lifecycle_stage"] == "critique"


@pytest.mark.smoke
@pytest.mark.parametrize("group", ["foundry", "product", "mainline"])
def test_generic_shell_group_is_not_a_public_default(group: str) -> None:
    exit_code, stdout, stderr = _run_cli(
        group,
        "status",
        "--input",
        str(CRITIQUE_EXAMPLE_PATH),
        "--format",
        "json",
    )

    assert exit_code == 2
    assert stdout == ""
    assert f"invalid choice: '{group}'" in stderr
