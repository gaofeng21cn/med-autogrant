from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from med_autogrant.product_entry_parts.source_purity_guard_readback import (
    build_source_purity_guard_readback,
)


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def _all_false(mapping: dict[str, object]) -> None:
    assert mapping
    assert all(value is False for value in mapping.values())


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

    repo_shell_guard = payload["repo_shell_verification_wrapper_guard"]
    assert repo_shell_guard["surface_kind"] == "mag_repo_shell_verification_wrapper_guard"
    assert repo_shell_guard["state"] == "passed_repo_native_verification_wrapper_classified"
    assert repo_shell_guard["classification"] == "repo_native_verification_wrapper"
    assert repo_shell_guard["active_caller_status"] == "active_repo_verification_entry"
    assert repo_shell_guard["unclassified_script_refs"] == []
    assert repo_shell_guard["stale_classified_script_refs"] == []
    assert repo_shell_guard["checked_script_refs"] == repo_shell_guard["classified_script_refs"]
    assert "scripts/check_source_purity_guard.py" in repo_shell_guard["checked_script_refs"]
    assert "scripts/verify.sh" in repo_shell_guard["checked_script_refs"]
    assert repo_shell_guard["retirement_gate"]["compatibility_alias_allowed"] is False
    _all_false(repo_shell_guard["authority_boundary"])
    _all_false(repo_shell_guard["false_ready_guard"])

    summary = payload["compact_cleanup_readiness_summary"]
    assert summary["summary_id"] == (
        "mag.physical_morphology.compact_cleanup_readiness_summary.v1"
    )
    assert summary["cleanup_candidate_count"] == 0
    assert summary["cleanup_candidate_surface_ids"] == []
    assert summary["owner_delta_required"] is False
    assert summary["migrated_surface_ids"] == ["grouped_cli_wrapper"]
    assert summary["retained_current_thin_surface_ids"] == [
        "product_entry",
        "status",
        "user_loop",
        "domain_handler",
        "control_plane",
        "lifecycle",
    ]
    for key in [
        "can_apply_cleanup",
        "can_authorize_physical_delete",
        "can_claim_default_caller_cutover_complete",
        "can_claim_app_operator_consumption",
        "can_claim_grant_ready",
        "can_claim_submission_ready",
        "can_claim_domain_ready",
        "can_claim_production_ready",
    ]:
        assert summary[key] is False

    work_order = payload["owner_delta_work_order_pack"]
    assert work_order == summary["owner_delta_work_order_pack"]
    assert work_order["surface_kind"] == "mag_cleanup_owner_delta_work_order_pack"
    assert work_order["owner_delta_route_count"] == summary["cleanup_candidate_count"]
    _all_false(work_order["authority_boundary"])
    assert "missing_evidence_worklist" in payload["allowed_outputs"]
    assert "physical_delete_operation" in payload["forbidden_outputs"]
    _all_false(payload["authority_boundary"])


def _run_json_readback(command: list[str]) -> dict[str, object]:
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    return json.loads(result.stdout)


def test_source_purity_guard_script_and_public_cli_emit_same_guard_readback() -> None:
    script_payload = _run_json_readback(
        [
            str(REPO_ROOT / "scripts" / "run-python-clean.sh"),
            "scripts/check_source_purity_guard.py",
            "--format",
            "json",
        ]
    )
    cli_payload = _run_json_readback(
        [
            str(REPO_ROOT / "scripts" / "run-python-clean.sh"),
            "-m",
            "med_autogrant.cli",
            "authority",
            "source-purity",
            "--format",
            "json",
        ]
    )

    assert script_payload == cli_payload
    assert cli_payload["surface_kind"] == "mag_strict_source_purity_guard_readback"
    assert cli_payload["state"] == "passed_repo_source_guard_only"
    assert cli_payload["failed_checks"] == []
    assert cli_payload["repo_shell_verification_wrapper_guard"]["state"] == (
        "passed_repo_native_verification_wrapper_classified"
    )
