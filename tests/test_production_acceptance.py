from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_PATH = REPO_ROOT / "contracts" / "production_acceptance" / "mag-production-acceptance.json"
LEDGER_PATH = REPO_ROOT / "contracts" / "external_evidence" / "mag-evidence-receipt-ledger.json"
STAGE_CONTROL_PLANE_PATH = REPO_ROOT / "contracts" / "stage_control_plane.json"


def _acceptance() -> dict[str, object]:
    return json.loads(ACCEPTANCE_PATH.read_text(encoding="utf-8"))


def _ledger() -> dict[str, object]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def _stage_control_plane() -> dict[str, object]:
    return json.loads(STAGE_CONTROL_PLANE_PATH.read_text(encoding="utf-8"))


def _assert_ref_list(values: object) -> None:
    assert isinstance(values, list)
    assert values
    for value in values:
        assert isinstance(value, str)
        assert value
        assert (
            value.startswith("/")
            or value.startswith("contracts/")
            or value.startswith("docs/")
            or value.startswith("tests/")
            or value.startswith("agent/")
            or value.startswith("rtk ")
            or value.startswith("receipt:")
            or value.startswith("receipt-projection:")
            or value.startswith("typed-blocker:")
            or value.startswith("human_gate:")
            or "::" in value
        ), value


def test_mag_production_acceptance_surface_exists_with_domain_owned_tail_state() -> None:
    assert ACCEPTANCE_PATH.exists()
    surface = _acceptance()

    assert surface["surface_kind"] == "mag_production_acceptance_evidence.v1"
    assert surface["domain_id"] == "med-autogrant"
    assert surface["acceptance_owner"] == "med-autogrant"
    assert surface["evidence_tail_status"] in {
        "closed_by_domain_owned_acceptance_receipt",
        "domain_owned_typed_blocker_with_next_verification_ref",
    }
    assert surface["conformance_status"] == {
        "structural_conformance": "passed",
        "physical_conformance": "passed",
        "conformance_can_claim_domain_ready": False,
        "conformance_can_claim_fundability_ready": False,
    }
    assert surface["grant_receipt_chain"]["production_like_grant_receipt_chain_present"] is True
    assert surface["domain_readiness_policy"]["domain_readiness_owner"] == "med-autogrant"
    assert surface["domain_readiness_policy"]["fundability_readiness_owner"] == "med-autogrant"


def test_mag_production_acceptance_is_refs_only_and_contains_required_refs() -> None:
    surface = _acceptance()

    refs = surface["refs"]
    for key in (
        "grant_owner_receipt_refs",
        "fundability_review_gate_refs",
        "package_proposal_lifecycle_refs",
        "typed_blocker_refs",
        "next_verification_command_refs",
    ):
        _assert_ref_list(refs[key])

    forbidden_payloads = surface["refs_only_policy"]["forbidden_payload_classes"]
    for forbidden in (
        "grant_artifact_body",
        "memory_body",
        "opl_runtime_state_body",
        "fundability_verdict_body",
        "proposal_text_body",
    ):
        assert forbidden in forbidden_payloads

    assert surface["refs_only_policy"]["repo_tracks_receipt_instance_body"] is False
    assert surface["refs_only_policy"]["repo_tracks_grant_artifact_body"] is False


def test_opl_provider_completion_cannot_authorize_mag_grant_readiness() -> None:
    surface = _acceptance()
    authority = surface["authority_boundary"]

    assert authority["opl_can_authorize_grant_domain_ready"] is False
    assert authority["opl_can_authorize_fundability_ready"] is False
    assert authority["provider_completion_equals_fundability_ready"] is False
    assert authority["provider_completion_equals_domain_ready"] is False
    assert authority["provider_completion_equals_submission_ready"] is False
    assert authority["structural_conformance_equals_domain_ready"] is False


def test_external_evidence_ledger_records_first_live_production_refs_without_ready_authority() -> None:
    ledger = _ledger()
    summary = ledger["summary"]
    first_live = ledger["first_live_production_evidence"]

    assert ledger["state"] == "first_live_production_evidence_consumed_refs_only"
    assert summary["closed_request_count"] == 7
    assert summary["receipt_ref_count"] == 7
    assert summary["domain_owned_typed_blocker_count"] == 0
    assert summary["claims_external_runtime_evidence_received"] is True
    assert summary["claims_direct_hosted_parity_passed"] is True
    assert summary["claims_temporal_provider_long_soak_complete"] is False
    assert summary["temporal_provider_reconciliation_ref_recorded"] is True
    assert summary["claims_grant_or_fundability_ready"] is False
    assert ledger["domain_owned_typed_blocker_request_ids"] == []
    assert ledger["remaining_real_evidence_gap_ids"] == [
        "temporal_provider_long_soak_window_evidence"
    ]

    assert first_live["state"] == "consumed_complete_refs_only"
    for key in (
        "external_default_caller_release_dist_consumed",
        "app_workbench_package_refs_consumed",
        "owner_receipt_typed_blocker_roundtrip_verified",
        "continuous_no_forbidden_write_guard_verified",
        "direct_hosted_parity_no_regression_verified",
    ):
        assert first_live[key] is True
    assert first_live["temporal_soak_reconciliation_verified"] is False
    assert first_live["temporal_provider_reconciliation_ref_recorded"] is True

    boundary = first_live["authority_boundary"]
    assert boundary["mag_records_domain_owned_owner_receipt"] is True
    assert boundary["mag_records_external_receipt_refs"] is True
    for claim in (
        "mag_declares_opl_provider_domain_ready",
        "mag_declares_grant_ready",
        "mag_declares_fundability_ready",
        "mag_declares_submission_ready_export",
        "mag_implements_opl_runtime",
        "mag_implements_app_workbench",
    ):
        assert boundary[claim] is False


def test_mag_production_acceptance_requires_owner_receipt_or_typed_blocker() -> None:
    surface = _acceptance()
    closure = surface["closure_evidence"]
    refs = surface["refs"]

    assert closure["required_return_shapes"] == [
        "domain_owner_receipt_ref",
        "typed_blocker_ref",
        "no_regression_evidence_ref",
    ]
    assert closure["accepted_return_shape"] in closure["required_return_shapes"]
    if surface["evidence_tail_status"] == "closed_by_domain_owned_acceptance_receipt":
        assert closure["accepted_return_shape"] == "domain_owner_receipt_ref"
        assert closure["owner_receipt_ref"] in refs["owner_receipt_refs"]
        _assert_ref_list(refs["grant_owner_receipt_refs"])
        _assert_ref_list(refs["acceptance_receipt_refs"])
        assert "tests/product_entry_cases/test_production_live_acceptance.py" in refs["next_verification_command_refs"]
    else:
        assert closure["accepted_return_shape"] == "typed_blocker_ref"
        _assert_ref_list(refs["typed_blocker_refs"])
        assert closure["next_verification_ref"] in refs["next_verification_command_refs"]


def test_production_acceptance_tail_is_not_w7_live_owner_closing_ref() -> None:
    surface = _acceptance()
    policy = surface["live_stage_run_progress_tail_policy"]

    assert policy["surface_kind"] == "mag_live_stage_run_progress_tail_policy.v1"
    assert policy["owner"] == "med-autogrant"
    assert policy["w7_owner_evidence_tail_role"] == (
        "provenance_input_not_domain_owned_closing_ref"
    )
    assert policy["live_stage_run_progress_source_of_truth"] == (
        "contracts/live_stage_run_progress_evidence.json"
    )
    assert policy["production_acceptance_tail_counts_as_live_owner_closing_ref"] is False
    assert policy["domain_owned_closing_ref"] is None
    assert policy["required_live_closing_shapes"] == [
        "real_submission_ready_human_gate_receipt_ref",
        "real_quality_or_export_receipt_ref",
        "temporal_provider_long_soak_window_evidence_ref",
        "owner_acceptance_or_success_rate_evidence_ref",
    ]
    assert policy["current_blocked_gate_categories"] == [
        "human_gate",
        "quality_or_export",
        "long_soak",
        "owner_acceptance",
    ]
    for claim_name, value in policy["forbidden_claims"].items():
        assert value is False, claim_name


def test_mag_production_acceptance_exposes_real_target_patch_loop_refs() -> None:
    surface = _acceptance()
    patch_loop_refs = surface["patch_loop_refs"]

    assert set(patch_loop_refs) == {
        "blocked_suite_result_ref",
        "developer_patch_work_order_ref",
        "patch_traceability_matrix_ref",
        "target_repo_verification_refs",
        "target_runtime_read_model_consumption_ref",
        "workspace_environment_proof_ref",
        "no_forbidden_write_proof_ref",
        "target_owner_receipt_or_typed_blocker_ref",
        "patch_absorption_ref",
        "worktree_cleanup_ref",
        "agent_lab_re_evaluation_ref",
    }
    assert patch_loop_refs["target_runtime_read_model_consumption_ref"] == (
        "/product_entry_manifest/production_live_acceptance_receipt"
    )
    assert patch_loop_refs["no_forbidden_write_proof_ref"] == (
        "contracts/agent_lab_handoff.json#/authority_boundary/oma_consumes_mag_refs_only"
    )
    assert patch_loop_refs["target_owner_receipt_or_typed_blocker_ref"] in (
        surface["refs"]["owner_receipt_refs"] + surface["refs"]["typed_blocker_refs"]
    )
    _assert_ref_list(patch_loop_refs["target_repo_verification_refs"])
    for key, value in patch_loop_refs.items():
        if key == "target_repo_verification_refs":
            continue
        assert isinstance(value, str)
        assert value


def test_grant_stage_controlled_attempt_closeout_covers_expected_receipts_and_monitor_freshness() -> None:
    ledger = _ledger()
    stage_plane = _stage_control_plane()
    closeout = ledger["grant_stage_controlled_attempt_closeout"]
    stage_closeouts = closeout["stage_closeout_refs"]

    assert closeout["surface_kind"] == "mag_grant_stage_controlled_attempt_body_free_closeout.v1"
    assert closeout["state"] == "closed_by_mag_owner_receipt_ref_body_free"
    assert closeout["accepted_return_shape"] == "domain_owner_receipt_ref"
    assert closeout["required_return_shapes"] == [
        "domain_owner_receipt_ref",
        "typed_blocker_ref",
        "no_regression_evidence_ref",
    ]
    assert len(stage_closeouts) == len(stage_plane["stages"]) == 6
    assert closeout["external_evidence_refs"]["release_dist_consumption_ref"].endswith(
        "/request_closures/2"
    )
    assert closeout["external_evidence_refs"]["no_forbidden_write_guard_ref"].endswith(
        "/request_closures/4"
    )
    assert closeout["external_evidence_refs"]["direct_hosted_parity_no_regression_ref"].endswith(
        "/request_closures/5"
    )
    assert closeout["external_evidence_refs"]["temporal_reconciliation_ref"].endswith(
        "/request_closures/6"
    )
    live_attempt = closeout["live_grant_stage_attempt_ref_packet"]
    assert live_attempt["surface_kind"] == "mag_live_grant_stage_attempt_ref_packet.v1"
    assert live_attempt["stage_id"] == "specific_aims_and_structure"
    assert live_attempt["attempt_kind"] == "real_grant_stage_attempt_body_free_owner_chain"
    assert live_attempt["payload_body_included"] is False
    assert live_attempt["owner_receipt_or_typed_blocker_refs"]["accepted_return_shape"] in (
        "domain_owner_receipt_ref",
        "typed_blocker_ref",
    )
    assert live_attempt["release_dist_consumption_ref"] == closeout["external_evidence_refs"][
        "release_dist_consumption_ref"
    ]
    assert live_attempt["direct_hosted_parity_no_regression_ref"] == closeout[
        "external_evidence_refs"
    ]["direct_hosted_parity_no_regression_ref"]
    assert live_attempt["no_forbidden_write_guard_ref"] == closeout["external_evidence_refs"][
        "no_forbidden_write_guard_ref"
    ]
    assert live_attempt["monitor_freshness_refs"] == stage_closeouts[2]["monitor_freshness_refs"]
    assert live_attempt["readiness_claims"] == {
        "claims_grant_ready": False,
        "claims_fundability_ready": False,
        "claims_quality_ready": False,
        "claims_submission_ready_export": False,
    }

    for index, stage in enumerate(stage_plane["stages"]):
        stage_contract = stage["stage_contract"]
        stage_closeout = stage_closeouts[index]

        assert stage_closeout["stage_id"] == stage["stage_id"], stage["stage_id"]
        assert stage_closeout["expected_receipt_ref"] == (
            f"contracts/stage_control_plane.json#/stages/{index}/"
            "stage_contract/expected_receipt_refs/0"
        )
        assert len(stage_closeout["monitor_freshness_refs"]) == 3, stage["stage_id"]
        assert stage_contract["expected_receipt_refs"][0]["required_return_shapes"] == (
            closeout["required_return_shapes"]
        )
        assert stage_contract["expected_receipt_refs"][0]["body_free_payload_required"] is True
        assert stage_contract["monitor_freshness_refs"]
        assert stage["stage_production_evidence_closeout"]["evidence_refs"][0] == (
            "contracts/external_evidence/mag-evidence-receipt-ledger.json#/"
            "grant_stage_controlled_attempt_closeout"
        )
    handoff = closeout["opl_stage_evidence_receipt_handoff"]
    assert handoff["surface_kind"] == "mag_opl_stage_evidence_receipt_handoff.v1"
    assert handoff["status"] == (
        "ready_for_opl_stage_evidence_record_verify_with_submission_human_gate_typed_blocker"
    )
    assert handoff["mode"] == (
        "refs_only_domain_owner_receipt_refs_and_domain_owned_typed_blocker_refs"
    )
    assert len(handoff["stage_owner_receipt_refs"]) == 6
    assert {
        item["stage_id"] for item in handoff["stage_owner_receipt_refs"]
    } == {stage["stage_id"] for stage in stage_plane["stages"]}
    assert all(
        item["domain_receipt_ref"].startswith("receipt:mag/grant-stage-controlled-attempt/")
        for item in handoff["stage_owner_receipt_refs"]
    )
    assert handoff["monitor_evidence_refs"] == [
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/grant_stage_controlled_attempt_closeout",
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/first_live_production_evidence",
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/request_closures/5",
        "contracts/external_evidence/mag-evidence-receipt-ledger.json#/request_closures/6",
    ]
    assert handoff["stage_typed_blocker_refs"] == [
        {
            "stage_id": "package_and_submit_ready",
            "human_gate_ref": "human_gate:submission_ready_export_gate",
            "typed_blocker_ref": (
                "typed-blocker:mag/package_and_submit_ready/submission_ready_export_gate/"
                "human-approval-required/2026-05-22"
            ),
            "blocker_kind": "submission_ready_export_gate_human_approval_required",
            "blocker_state": "human_gate_required_no_submission_ready_approval_recorded",
        }
    ]
    assert handoff["authority_boundary"] == {
        "mag_owns_domain_receipt_refs": True,
        "opl_records_refs_only": True,
        "opl_can_write_grant_truth": False,
        "opl_can_write_memory_body": False,
        "opl_can_sign_owner_receipt": False,
        "opl_can_authorize_fundability_or_export": False,
        "opl_can_record_human_gate_as_approval": False,
        "human_gate_approval_recorded": False,
        "claims_grant_ready": False,
        "claims_submission_ready_export": False,
    }
    package_closeout = stage_closeouts[5]
    assert package_closeout["stage_id"] == "package_and_submit_ready"
    assert package_closeout["submission_ready_export_gate_ref"] == (
        "human_gate:submission_ready_export_gate"
    )
    assert package_closeout["submission_ready_export_gate_typed_blocker_ref"] == (
        "typed-blocker:mag/package_and_submit_ready/submission_ready_export_gate/"
        "human-approval-required/2026-05-22"
    )

    submission_tail = closeout["submission_ready_export_gate_tail"]
    assert submission_tail == {
        "surface_kind": "mag_submission_ready_export_gate_tail.v1",
        "state": "blocked_by_domain_owned_human_gate_typed_blocker",
        "stage_id": "package_and_submit_ready",
        "human_gate_ref": "human_gate:submission_ready_export_gate",
        "typed_blocker_ref": (
            "typed-blocker:mag/package_and_submit_ready/submission_ready_export_gate/"
            "human-approval-required/2026-05-22"
        ),
        "blocker_reason": (
            "The package-and-submit stage has no real human approval receipt for "
            "submission-ready export; MAG exposes a typed blocker instead of allowing "
            "OPL to record the gate id as approval."
        ),
        "opl_recording_policy": (
            "OPL may record the typed_blocker_ref through the refs-only "
            "stage-production-evidence route; recording this blocker is not a "
            "submission-ready export approval."
        ),
        "readiness_claims": {
            "claims_grant_ready": False,
            "claims_export_ready": False,
            "claims_submission_ready_export": False,
            "claims_human_approval_obtained": False,
        },
        "authority_boundary": {
            "mag_owns_submission_ready_export_gate": True,
            "opl_records_refs_only": True,
            "opl_can_authorize_submission_ready": False,
            "opl_can_treat_human_gate_ref_as_receipt_instance": False,
            "human_gate_approval_recorded": False,
        },
    }

    source_runtime_handoff = closeout["opl_stage_source_runtime_evidence_typed_blocker_handoff"]
    assert source_runtime_handoff["surface_kind"] == (
        "mag_opl_stage_source_runtime_evidence_typed_blocker_handoff.v1"
    )
    assert source_runtime_handoff["status"] == (
        "ready_for_opl_stage_source_runtime_typed_blocker_record"
    )
    assert source_runtime_handoff["mode"] == "refs_only_domain_owned_typed_blocker_refs"
    assert source_runtime_handoff["summary"] == {
        "stage_count": 6,
        "typed_blocker_ref_count": 6,
        "blocked_source_scope_ref_count": 29,
        "blocked_runtime_event_ref_count": 6,
        "claims_source_scope_live_evidence_complete": False,
        "claims_runtime_event_live_evidence_complete": False,
        "claims_grant_ready": False,
        "claims_submission_ready_export": False,
    }
    blocker_by_stage = {
        item["stage_id"]: item
        for item in source_runtime_handoff["stage_typed_blocker_refs"]
    }
    assert set(blocker_by_stage) == {stage["stage_id"] for stage in stage_plane["stages"]}
    for stage in stage_plane["stages"]:
        stage_id = stage["stage_id"]
        stage_contract = stage["stage_contract"]
        blocker = blocker_by_stage[stage_id]
        expected_source_scope_refs = []
        for source_ref in stage_contract["source_scope_refs"]:
            value = source_ref["ref"]
            if isinstance(value, list):
                expected_source_scope_refs.extend(value)
            else:
                expected_source_scope_refs.append(value)
        assert blocker["blocked_source_scope_refs"] == expected_source_scope_refs
        assert blocker["blocked_runtime_event_refs"] == stage_contract["runtime_event_refs"]
        assert blocker["typed_blocker_ref"] == (
            f"typed-blocker:mag/stage-source-runtime-live-evidence/{stage_id}/pending"
        )
        assert blocker["next_owner"] == "med-autogrant_or_app_live_operator"
    assert source_runtime_handoff["authority_boundary"] == {
        "mag_owns_typed_blocker_refs": True,
        "opl_records_refs_only": True,
        "opl_can_write_grant_truth": False,
        "opl_can_write_memory_body": False,
        "opl_can_record_source_runtime_success_without_live_refs": False,
        "opl_can_authorize_fundability_or_export": False,
        "typed_blocker_equals_source_runtime_success": False,
        "claims_grant_ready": False,
        "claims_submission_ready_export": False,
    }

    for forbidden, value in closeout["forbidden_write_proof"].items():
        assert value is False, forbidden
    for claim, value in closeout["claims"].items():
        assert value is False, claim
    boundary = closeout["authority_boundary"]
    assert boundary["mag_owner_receipt_authority"] is True
    assert boundary["mag_fundability_export_submission_verdict_authority"] is True
    assert boundary["opl_consumes_refs_only"] is True
    for forbidden in (
        "opl_can_write_grant_truth",
        "opl_can_write_memory_body",
        "opl_can_sign_owner_receipt",
        "opl_can_declare_fundability_verdict",
        "opl_can_declare_export_verdict",
        "opl_can_declare_submission_ready",
    ):
        assert boundary[forbidden] is False
