from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OPL_BIN = "/Users/gaofeng/workspace/one-person-lab/bin/opl"
MAG_DOMAIN_ID = "med-autogrant"


def _run_opl_agent_lab_longline() -> dict[str, Any]:
    opl_bin = os.environ.get("OPL_BIN", DEFAULT_OPL_BIN)
    completed = subprocess.run(
        [opl_bin, "agent-lab", "longline", "--json"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def _authority_boundary_has_no_domain_write_authority(boundary: dict[str, Any]) -> None:
    assert boundary["can_write_domain_truth"] is False
    assert boundary["can_write_memory_body"] is False
    assert boundary["can_accept_or_reject_memory_writeback"] is False
    assert boundary["can_authorize_quality_verdict"] is False


def test_opl_agent_lab_longline_carries_mag_framework_migration_guard() -> None:
    payload = _run_opl_agent_lab_longline()
    suite = payload["agent_lab_longline"]["suite_result"]
    longline_summary = suite["longline_summary"]

    assert suite["status"] == "passed"
    assert MAG_DOMAIN_ID in longline_summary["domain_ids"]
    assert longline_summary["ready_to_reduce_domain_longline_tests"] is True

    dispositions = {
        entry["domain_id"]: entry for entry in longline_summary["recommended_repo_test_disposition"]
    }
    mag_disposition = dispositions[MAG_DOMAIN_ID]
    assert mag_disposition["move_to_opl_agent_lab"] == [
        "controlled grant-stage soak orchestration",
        "receipt reconciliation projection",
        "no-forbidden-write cross-domain regression",
    ]
    assert mag_disposition["keep_in_domain_repo"] == [
        "fundability scorer",
        "grant owner receipt fixture",
        "proposal artifact authority checks",
    ]

    for boundary in (
        suite["authority_boundary"],
        longline_summary["authority_boundary"],
        payload["agent_lab_longline"]["authority_boundary"],
    ):
        _authority_boundary_has_no_domain_write_authority(boundary)

    mag_runs = [run for run in suite["runs"] if run["domain_id"] == MAG_DOMAIN_ID]
    assert len(mag_runs) == 1
    mag_run = mag_runs[0]
    assert mag_run["status"] == "passed"
    assert mag_run["scorecard"]["domain_owned"] is True
    for boundary in (
        mag_run["authority_boundary"],
        mag_run["trajectory"]["authority_boundary"],
        mag_run["scorecard"]["authority_boundary"],
        mag_run["promotion_gate"]["authority_boundary"],
    ):
        _authority_boundary_has_no_domain_write_authority(boundary)

    assert suite["refs"]["forbidden_authority_flags"] == []
