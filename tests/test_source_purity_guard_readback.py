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
    assert repo_shell_guard["authority_boundary"] == {
        "can_authorize_physical_delete": False,
        "can_claim_grant_readiness": False,
        "can_claim_production_long_run_soak": False,
        "can_own_generated_wrapper": False,
        "can_own_generic_runtime": False,
    }
    assert repo_shell_guard["retirement_gate"]["compatibility_alias_allowed"] is False
    assert repo_shell_guard["false_ready_guard"] == {
        "repo_shell_guard_can_claim_runtime_owner": False,
        "repo_shell_guard_can_claim_generated_wrapper_owner": False,
        "repo_shell_guard_can_authorize_physical_delete": False,
        "repo_shell_guard_can_claim_grant_ready": False,
        "repo_shell_guard_can_claim_production_ready": False,
    }
    summary = payload["compact_cleanup_readiness_summary"]
    assert summary["summary_id"] == (
        "mag.physical_morphology.compact_cleanup_readiness_summary.v1"
    )
    assert summary["state"] == "compact_cleanup_worklist_empty_current_thin_surfaces_retained"
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
    owner_decision_gate = summary["retained_surface_owner_decision_gate"]
    assert owner_decision_gate["gate_id"] == (
        "mag.physical_morphology.retained_surface_owner_decision_gate.v1"
    )
    assert owner_decision_gate["state"] == (
        "retained_surfaces_require_owner_decision_before_delete_or_tombstone"
    )
    assert owner_decision_gate["applies_to_surface_ids"] == (
        summary["retained_current_thin_surface_ids"]
    )
    assert owner_decision_gate["required_before_delete_or_tombstone"] == (
        summary["missing_evidence_refs"]
    )
    assert "tombstone_or_provenance_pointer" in owner_decision_gate["required_proofs"]
    assert "delete_from_cleanup_candidate_count_zero" in (
        owner_decision_gate["forbidden_terminal_decisions"]
    )
    assert owner_decision_gate["authority_boundary"] == {
        "gate_can_write_grant_truth": False,
        "gate_can_sign_owner_receipt": False,
        "gate_can_create_typed_blocker_instance": False,
        "gate_can_authorize_physical_delete": False,
        "gate_can_claim_default_caller_cutover": False,
        "gate_can_claim_app_operator_consumption": False,
        "gate_can_claim_grant_ready": False,
        "gate_can_claim_submission_ready": False,
        "gate_can_claim_domain_ready": False,
        "gate_can_claim_production_ready": False,
    }
    assert summary["non_candidate_surface_ids"] == [
        "grouped_cli_wrapper",
        "product_entry",
        "status",
        "user_loop",
        "domain_handler",
        "control_plane",
        "lifecycle",
    ]
    grouped_cli = summary["non_candidate_surface_statuses"]["grouped_cli_wrapper"]
    assert grouped_cli["state"] == "migrated_no_active_compat_alias_or_facade"
    assert grouped_cli["delete_path"] == []
    for surface_id in summary["retained_current_thin_surface_ids"]:
        status = summary["non_candidate_surface_statuses"][surface_id]
        assert status["state"] == "retained_current_thin_surface"
        assert status["cleanup_candidate"] is False
        assert status["delete_path"]
        assert status["retirement_guard"] == (
            "owner_receipt_or_domain_typed_blocker_required_before_delete"
        )
        assert status["owner_decision_gate_ref"].endswith(
            "/retained_surface_owner_decision_gate"
        )
    assert summary["can_apply_cleanup"] is False
    assert summary["can_authorize_physical_delete"] is False
    assert summary["can_claim_default_caller_cutover_complete"] is False
    assert summary["can_claim_app_operator_consumption"] is False
    assert summary["can_claim_grant_ready"] is False
    assert summary["can_claim_submission_ready"] is False
    assert summary["can_claim_domain_ready"] is False
    assert summary["can_claim_production_ready"] is False
    assert "owner_receipt://mag/physical_delete_or_tombstone_authorization" in (
        summary["missing_evidence_refs"]
    )
    work_order = payload["owner_delta_work_order_pack"]
    assert work_order == summary["owner_delta_work_order_pack"]
    assert work_order["surface_kind"] == "mag_cleanup_owner_delta_work_order_pack"
    assert work_order["state"] == "no_cleanup_candidates_current_thin_surfaces_retained"
    assert work_order["cleanup_candidate_count"] == 0
    assert work_order["owner_delta_route_count"] == 0
    assert work_order["owner_delta_routes"] == []
    for route in work_order["owner_delta_routes"]:
        assert route["next_owner"] == "med-autogrant_owner_receipt_or_typed_blocker_surface"
        assert route["owner_receipt_ref_shape"].startswith("owner_receipt://mag/")
        assert route["owner_receipt_ref_shape"].endswith(
            "/physical_delete_or_tombstone_authorization"
        )
        assert route["typed_blocker_ref_shape"].startswith(
            "typed_blocker://mag/physical_morphology_cleanup/"
        )
        assert route["typed_blocker_ref_shape"].endswith(
            "/requires-owner-receipt-or-evidence"
        )
        assert route["required_evidence_refs"] == summary["missing_evidence_refs"]
    assert work_order["authority_boundary"] == {
        "work_order_can_write_grant_truth": False,
        "work_order_can_sign_owner_receipt": False,
        "work_order_can_create_typed_blocker_instance": False,
        "work_order_can_authorize_physical_delete": False,
        "work_order_can_claim_default_caller_cutover": False,
        "work_order_can_claim_app_operator_consumption": False,
        "work_order_can_claim_grant_ready": False,
        "work_order_can_claim_submission_ready": False,
        "work_order_can_claim_domain_ready": False,
        "work_order_can_claim_production_ready": False,
    }
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
    assert (
        payload["repo_shell_verification_wrapper_guard"]["state"]
        == "passed_repo_native_verification_wrapper_classified"
    )
    assert payload["repo_shell_verification_wrapper_guard"]["unclassified_script_refs"] == []
    assert payload["compact_cleanup_readiness_summary"]["can_apply_cleanup"] is False
    assert (
        payload["owner_delta_work_order_pack"]["owner_delta_route_count"]
        == payload["compact_cleanup_readiness_summary"]["cleanup_candidate_count"]
    )


def test_source_purity_guard_public_cli_emits_same_guard_readback() -> None:
    result = subprocess.run(
        [
            str(REPO_ROOT / "scripts" / "run-python-clean.sh"),
            "-m",
            "med_autogrant.cli",
            "authority",
            "source-purity",
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
    assert payload["failed_checks"] == []
    assert payload["repo_shell_verification_wrapper_guard"]["classification"] == (
        "repo_native_verification_wrapper"
    )
    assert payload["repo_shell_verification_wrapper_guard"]["false_ready_guard"][
        "repo_shell_guard_can_claim_generated_wrapper_owner"
    ] is False
    assert payload["authority_boundary"]["readback_can_authorize_physical_delete"] is False
    assert payload["authority_boundary"]["readback_can_claim_grant_readiness"] is False
    assert payload["owner_delta_work_order_pack"]["authority_boundary"][
        "work_order_can_create_typed_blocker_instance"
    ] is False
