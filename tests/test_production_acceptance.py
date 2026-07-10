from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta
REPO_ROOT = Path(__file__).resolve().parents[1]
ACCEPTANCE_PATH = (
    REPO_ROOT / "contracts" / "production_acceptance" / "mag-production-acceptance.json"
)


def _acceptance() -> dict[str, object]:
    return json.loads(ACCEPTANCE_PATH.read_text(encoding="utf-8"))


def test_production_acceptance_is_provenance_only_with_open_typed_blocker() -> None:
    surface = _acceptance()

    assert surface["surface_kind"] == "mag_production_acceptance_evidence.v1"
    assert surface["surface_id"] == "mag.production_acceptance.provenance"
    assert surface["state"] == "provenance_only_not_live_progress_or_readiness"
    assert surface["domain_id"] == "med-autogrant"
    assert surface["acceptance_owner"] == "med-autogrant"
    assert surface["refs"] == {
        "current_program_ref": "contracts/runtime-program/current-program.json",
        "live_stage_run_progress_ref": "contracts/live_stage_run_progress_evidence.json",
        "owner_receipt_contract_ref": "contracts/owner_receipt_contract.json",
        "external_evidence_ledger_ref": (
            "contracts/external_evidence/mag-evidence-receipt-ledger.json"
        ),
    }

    closure = surface["closure_evidence"]
    assert closure["state"] == "typed_blocker_open"
    assert closure["domain_owned_closing_ref"] is None
    assert closure["typed_blocker_ref"].startswith("typed-blocker:mag/")
    assert closure["counts_as_live_progress"] is False
    assert closure["counts_as_readiness"] is False

    tail = surface["live_stage_run_progress_tail_policy"]
    assert tail["role"] == "provenance_only_not_live_owner_closing_ref"
    assert tail["live_progress_source_ref"] == surface["refs"]["live_stage_run_progress_ref"]
    assert tail["domain_owned_closing_ref"] is None


def test_production_acceptance_keeps_return_and_readiness_authority_closed() -> None:
    surface = _acceptance()
    receipt_chain = surface["grant_receipt_chain"]

    assert receipt_chain["accepted_return_shapes"] == [
        "domain_owner_receipt_ref",
        "typed_blocker_ref",
        "no_regression_evidence_ref",
    ]
    assert receipt_chain["owner_receipt_contract_ref"] == surface["refs"][
        "owner_receipt_contract_ref"
    ]
    assert receipt_chain["provider_completion_counts_as_domain_completion"] is False

    authority = surface["authority_boundary"]
    assert set(authority) == {
        "opl_can_authorize_grant_domain_ready",
        "opl_can_authorize_fundability_ready",
        "opl_can_authorize_review_ready",
        "opl_can_authorize_submission_ready",
        "provider_completion_equals_domain_ready",
        "structural_conformance_equals_domain_ready",
    }
    assert all(value is False for value in authority.values())
    assert surface["forbidden_claims"] == [
        "grant_ready",
        "fundability_ready",
        "quality_ready",
        "export_ready",
        "submission_ready",
        "production_ready",
    ]
