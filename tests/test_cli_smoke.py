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
import med_autogrant.foundry_series_cli as foundry_series_cli
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
    assert "Series: OPL Foundry Agent" in stdout
    assert "Agent id: medautogrant" in stdout
    assert "Ordinary path: workspace/work/stage/run/vault/handoff/connect" in stdout
    assert "Executable command surface: medautogrant" in stdout
    assert "Authority boundary:" in stdout
    assert "Public command groups:" in stdout
    assert "foundry" in stdout
    assert "medautogrant foundry status --format json" in stdout
    assert "<med-autogrant-repo>/scripts/run-python-clean.sh -m med_autogrant.cli foundry status --json" in stdout
    assert "workspace" in stdout
    assert "authority" in stdout
    assert "product" not in stdout
    assert "runtime" not in stdout


@pytest.mark.smoke
def test_foundry_group_exposes_series_operations() -> None:
    exit_code, stdout, stderr = _run_cli("foundry", "--help")

    assert exit_code == 0
    assert stderr == ""
    for operation in ("status", "inspect", "interfaces", "validate", "doctor", "peers"):
        assert operation in stdout


@pytest.mark.smoke
def test_foundry_status_projects_mag_series_identity() -> None:
    payload = _run_json_cli("foundry", "status", "--json")
    direct_payload = foundry_series_cli.build_foundry_series_status()

    assert payload["ok"] is True
    assert payload == direct_payload
    assert payload["command"] == "foundry-status"
    assert payload["foundry_agent_series"]["version"] == "foundry-agent-series.v1"
    assert payload["foundry_agent_series"]["foundry_agent_id"] == "medautogrant"
    assert payload["status"]["series_label"] == "OPL Foundry Agent"
    assert payload["status"]["ordinary_path"] == "workspace/work/stage/run/vault/handoff/connect"
    assert payload["status"]["executable_command_surfaces"] == ["medautogrant"]
    assert payload["status"]["brand_shorthand"] == "mag"
    assert payload["status"]["brand_shorthand_path_safe"] is False
    assert "executable_frontdoors" not in payload["status"]


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
            "foundry",
            "status",
            "--json",
        ],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["command"] == "foundry-status"
    assert payload["status"]["executable_command_surfaces"] == ["medautogrant"]


@pytest.mark.smoke
def test_foundry_interfaces_exposes_canonical_grouped_cli() -> None:
    payload = _run_json_cli("foundry", "interfaces", "--json")

    assert payload["command"] == "foundry-interfaces"
    assert payload["interfaces"]["ordinary_series_spine"] == [
        "workspace",
        "work",
        "stage",
        "run",
        "vault",
        "handoff",
        "connect",
    ]
    assert payload["interfaces"]["ordinary_command_spine"] == [
        "workspace",
        "work",
        "stage",
        "run",
        "vault",
        "handoff",
        "connect",
    ]
    assert "ordinary_public_frontdoor_spine" not in payload["interfaces"]
    assert "validate" in payload["interfaces"]["commands_by_group"]["workspace"]
    assert "revision" in payload["interfaces"]["commands_by_group"]["pass"]


@pytest.mark.smoke
def test_pass_group_help_renders_canonical_commands() -> None:
    exit_code, stdout, stderr = _run_cli("pass", "--help")
    assert exit_code == 0
    assert stderr == ""
    assert "revision" in stdout
    assert "mainline-loop" in stdout


@pytest.mark.smoke
def test_foundry_validate_checks_command_surface_contract() -> None:
    payload = _run_json_cli("foundry", "validate", "--format", "json")

    assert payload["command"] == "foundry-validate"
    assert payload["validation"]["ok"] is True
    assert payload["validation"]["checked_command_surface_operations"] == [
        "status",
        "inspect",
        "interfaces",
        "validate",
        "doctor",
        "peers",
    ]
    assert "checked_frontdoor_operations" not in payload["validation"]
    assert payload["validation"]["problems"] == []


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
def test_product_group_is_not_a_public_default_shell() -> None:
    exit_code, stdout, stderr = _run_cli(
        "product",
        "status",
        "--input",
        str(CRITIQUE_EXAMPLE_PATH),
        "--format",
        "json",
    )

    assert exit_code == 2
    assert stdout == ""
    assert "invalid choice: 'product'" in stderr


@pytest.mark.smoke
def test_mainline_status_projects_current_program_pointer() -> None:
    payload = _run_json_cli("mainline", "status", "--format", "json")

    assert payload["program_id"] == "med-autogrant-mainline"
    assert "current_owner_line" in payload["current_line"]
    assert payload["current_focus"]["summary"]
