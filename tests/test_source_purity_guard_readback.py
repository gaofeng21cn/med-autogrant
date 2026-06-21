from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from scripts.check_source_purity_guard import build_source_purity_guard_readback


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_source_purity_guard_readback_is_repo_guard_not_readiness_claim() -> None:
    payload = build_source_purity_guard_readback()

    assert payload["surface_kind"] == "mag_strict_source_purity_guard_readback"
    assert payload["state"] == "passed_repo_source_guard_only"
    assert payload["failed_checks"] == []
    assert payload["active_path_scan"]["state"] == "passed"
    assert payload["source_ref_integrity_gate"]["checked_source_ref_count"] > 0
    assert payload["strict_source_purity_no_second_truth_guard"]["guard_id"] == (
        "mag.physical_morphology.strict_source_purity_no_second_truth_guard.v1"
    )
    assert "missing_evidence_worklist" in payload["allowed_outputs"]
    assert "physical_delete_operation" in payload["forbidden_outputs"]
    assert payload["authority_boundary"] == {
        "readback_can_write_grant_truth": False,
        "readback_can_sign_owner_receipt": False,
        "readback_can_create_typed_blocker": False,
        "readback_can_authorize_physical_delete": False,
        "readback_can_claim_default_caller_cutover": False,
        "readback_can_claim_generated_hosted_live_consumption": False,
        "readback_can_claim_grant_readiness": False,
        "readback_can_claim_submission_ready": False,
        "readback_can_claim_production_ready": False,
    }


def test_source_purity_guard_script_emits_json_readback() -> None:
    result = subprocess.run(
        [
            str(REPO_ROOT / "scripts" / "run-python-clean.sh"),
            "scripts/check_source_purity_guard.py",
            "--format",
            "json",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["surface_kind"] == "mag_strict_source_purity_guard_readback"
    assert payload["state"] == "passed_repo_source_guard_only"
