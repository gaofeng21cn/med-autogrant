from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta
REPO_ROOT = Path(__file__).resolve().parents[1]


def test_opl_agent_lab_longline_carries_mag_migration_guard() -> None:
    completed = subprocess.run(
        [os.environ.get("OPL_BIN", "/Users/gaofeng/workspace/one-person-lab/bin/opl"), "agent-lab", "longline", "--json"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    suite = payload["agent_lab_longline"]["suite_result"]
    summary = suite["longline_summary"]
    mag_runs = [run for run in suite["runs"] if run["domain_id"] == "med-autogrant"]
    assert len(mag_runs) == 1
    mag_run = mag_runs[0]

    assert suite["status"] == "passed"
    assert summary["ready_to_reduce_domain_longline_tests"] is True
    dispositions = {item["domain_id"]: item for item in summary["recommended_repo_test_disposition"]}
    assert dispositions["med-autogrant"]["move_to_opl_agent_lab"] == [
        "controlled grant-stage soak orchestration",
        "receipt reconciliation projection",
        "no-forbidden-write cross-domain regression",
    ]
    assert dispositions["med-autogrant"]["keep_in_domain_repo"] == [
        "fundability scorer",
        "grant owner receipt fixture",
        "proposal artifact authority checks",
    ]
    assert mag_run["status"] == "passed"
    assert mag_run["scorecard"]["domain_owned"] is True
    assert suite["refs"]["forbidden_authority_flags"] == []
    for boundary in (
        suite["authority_boundary"],
        summary["authority_boundary"],
        payload["agent_lab_longline"]["authority_boundary"],
        mag_run["authority_boundary"],
        mag_run["trajectory"]["authority_boundary"],
        mag_run["scorecard"]["authority_boundary"],
        mag_run["promotion_gate"]["authority_boundary"],
    ):
        assert boundary["can_write_domain_truth"] is False
        assert boundary["can_write_memory_body"] is False
        assert boundary["can_accept_or_reject_memory_writeback"] is False
        assert boundary["can_authorize_quality_verdict"] is False
