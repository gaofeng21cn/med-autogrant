from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta
CONTRACT_PATH = Path(__file__).resolve().parents[2] / "contracts" / "runtime-program" / "opl-family-contract-adoption.json"


def test_consumer_thinning_keeps_only_mag_authority_and_request_sentinels() -> None:
    thinning = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))["mag_consumer_thinning_contract"]

    assert thinning["consumes_opl_family_primitive"] == "family_scheduler_replacement"
    assert thinning["adapter_role"] == "domain_authority_pack_with_thin_program_surface"
    assert thinning["mag_owned_outputs"] == [
        "grant_owned_refs",
        "owner_receipt",
        "typed_blocker",
        "verdict_refs",
        "domain_action_metadata",
    ]
    assert "generic_scheduler_owner" in thinning["forbidden_mag_generic_owner_roles"]
    assert "generic_attempt_ledger_owner" in thinning["forbidden_mag_generic_owner_roles"]

    followthrough = thinning["functional_followthrough_gap_classification"]
    assert followthrough["mag_functional_structure_gap_count"] == 0
    assert followthrough["remaining_mag_functional_structure_gap_ids"] == []
    assert followthrough["authority_boundary"]["claims_domain_repo_physical_delete_authorized"] is False
    assert followthrough["authority_boundary"]["claims_production_long_run_soak_complete"] is False

    evidence_pack = thinning["external_evidence_request_pack"]
    assert evidence_pack["state"] == "request_pack_declared_external_evidence_not_claimed"
    assert evidence_pack["authority_boundary"]["mag_request_pack_only"] is True
    assert evidence_pack["authority_boundary"]["mag_implements_opl_runtime"] is False
    assert evidence_pack["authority_boundary"]["mag_implements_app_workbench"] is False
    assert evidence_pack["authority_boundary"]["mag_claims_external_evidence_exists"] is False

    boundary = thinning["authority_boundary"]
    assert boundary["grant_truth_owner"] == "med-autogrant"
    assert boundary["quality_verdict_owner"] == "med-autogrant"
    assert boundary["export_authority_owner"] == "med-autogrant"
    assert boundary["owner_receipt_authority"] == "med-autogrant"
    assert boundary["mag_implements_generic_scheduler"] is False
    assert boundary["mag_implements_generic_runner"] is False
    assert boundary["mag_can_emit_private_functional_state"] is False
    assert thinning["claims_domain_repo_physical_delete_authorized"] is False
    assert thinning["claims_production_long_run_soak_complete"] is False
