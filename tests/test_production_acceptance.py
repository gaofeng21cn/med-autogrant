from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_PATH = REPO_ROOT / "contracts" / "production_acceptance" / "mag-production-acceptance.json"
LEDGER_PATH = REPO_ROOT / "contracts" / "external_evidence" / "mag-evidence-receipt-ledger.json"


def _acceptance() -> dict[str, object]:
    return json.loads(ACCEPTANCE_PATH.read_text(encoding="utf-8"))


def _ledger() -> dict[str, object]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


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
    assert summary["claims_temporal_provider_long_soak_complete"] is True
    assert summary["claims_grant_or_fundability_ready"] is False
    assert ledger["domain_owned_typed_blocker_request_ids"] == []
    assert ledger["remaining_real_evidence_gap_ids"] == []

    assert first_live["state"] == "consumed_complete_refs_only"
    for key in (
        "external_default_caller_release_dist_consumed",
        "app_workbench_package_refs_consumed",
        "owner_receipt_typed_blocker_roundtrip_verified",
        "continuous_no_forbidden_write_guard_verified",
        "direct_hosted_parity_no_regression_verified",
        "temporal_soak_reconciliation_verified",
    ):
        assert first_live[key] is True

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
