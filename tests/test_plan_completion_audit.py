from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_PROGRAM_CONTRACT = REPO_ROOT / "contracts" / "runtime-program" / "current-program.json"


def test_historical_plan_audit_is_not_a_machine_truth_gate() -> None:
    contract = json.loads(CURRENT_PROGRAM_CONTRACT.read_text(encoding="utf-8"))

    assert all(
        not surface_ref.startswith("docs/history/")
        for surface_ref in contract["repo_tracked_truth_surfaces"]
    )
