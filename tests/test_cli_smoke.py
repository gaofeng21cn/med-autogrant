from __future__ import annotations

import json
import os
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

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
def test_public_cli_help_renders_group_index() -> None:
    exit_code, stdout, stderr = _run_cli("--help")

    assert exit_code == 0
    assert stderr == ""
    assert "Public command groups:" in stdout
    assert "workspace" in stdout
    assert "product" in stdout
    assert "runtime" in stdout


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
def test_product_status_dispatches_current_product_entry_surface_contract() -> None:
    payload = _run_json_cli(
        "product",
        "status",
        "--input",
        str(CRITIQUE_EXAMPLE_PATH),
        "--format",
        "json",
    )

    assert payload["command"] == "product-status"
    status = payload["product_status"]
    assert status["surface_kind"] == "product_status"
    assert status["operator_loop_surface"]["shell_key"] == "grant_user_loop"


@pytest.mark.smoke
def test_product_direct_entry_projects_workspace_cockpit_and_entry_envelopes() -> None:
    payload = _run_json_cli(
        "product",
        "direct-entry",
        "--input",
        str(CRITIQUE_EXAMPLE_PATH),
        "--task-intent",
        "smoke-entry-health",
        "--format",
        "json",
    )

    assert payload["command"] == "grant-direct-entry"
    direct_entry = payload["grant_direct_entry"]
    assert direct_entry["entry_kind"] == "grant_direct_entry"
    assert direct_entry["task_intent"] == "smoke-entry-health"
    assert direct_entry["progress_projection"]["projection_kind"] == "grant_progress"
    assert direct_entry["direct_entry"]["entry_mode"] == "direct"


@pytest.mark.smoke
def test_product_skill_catalog_exposes_single_mag_skill() -> None:
    payload = _run_json_cli(
        "product",
        "skill-catalog",
        "--input",
        str(CRITIQUE_EXAMPLE_PATH),
        "--format",
        "json",
    )

    assert payload["command"] == "skill-catalog"
    skill = payload["skill_catalog"]["skills"][0]
    assert skill["skill_id"] == "med-autogrant"
    assert skill["domain_projection"]["recommended_shell"] == "product_status"


@pytest.mark.smoke
def test_mainline_status_projects_current_program_pointer() -> None:
    payload = _run_json_cli("mainline", "status", "--format", "json")

    assert payload["program_id"] == "med-autogrant-mainline"
    assert "current_owner_line" in payload["current_line"]
    assert payload["current_focus"]["summary"]


@pytest.mark.proof
def test_runtime_run_writes_session_journal_under_runtime_state_root() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        codex_home = Path(tmp_dir) / "codex-home"
        expected_journal_path = (
            codex_home
            / "projects"
            / "med-autogrant"
            / "runtime-state"
            / "sessions"
            / "grant-run-nsfc-demo-001-baseline-001.json"
        )
        with patch.dict(
            os.environ,
            {
                "CODEX_HOME": str(codex_home),
                "MED_AUTOGRANT_RUNTIME_STATE_ROOT": "",
            },
            clear=False,
        ):
            payload = _run_json_cli(
                "runtime",
                "run",
                "--input",
                str(REVISION_EXAMPLE_PATH),
                "--format",
                "json",
            )
            journal_exists = expected_journal_path.exists()

    assert payload["command"] == "runtime-run"
    assert payload["ok"] is True
    assert payload["journal_path"] == str(expected_journal_path.resolve())
    assert journal_exists


@pytest.mark.proof
def test_domain_entry_probe_smoke_dispatches_without_workspace() -> None:
    payload = _run_json_cli("runtime", "probe-hermes", "--format", "json")

    assert payload["command"] == "probe-upstream-hermes"
    assert "ok" in payload
