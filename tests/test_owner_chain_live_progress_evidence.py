from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta
LEDGER_PATH = (
    Path(__file__).resolve().parents[1]
    / "contracts"
    / "external_evidence"
    / "mag-evidence-receipt-ledger.json"
)


def test_external_evidence_ledger_keeps_owner_refs_open_and_body_free() -> None:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    assert ledger["surface_kind"] == "mag_external_evidence_receipt_ledger.v1"
    assert ledger["state"] == "refs_only_provenance_with_open_live_evidence_gates"
    assert ledger["domain_id"] == "med-autogrant"
    assert ledger["owner"] == "med-autogrant"

    owner_refs = ledger["first_live_production_evidence"]
    assert owner_refs["state"] == "provenance_only_not_currentness_or_readiness"
    assert owner_refs["owner_receipt_ref"].startswith("receipt:mag/")
    assert owner_refs["typed_blocker_ref"].startswith("typed-blocker:mag/")
    assert owner_refs["no_regression_ref"].startswith("no-regression:mag/")

    owner_lane = ledger["owner_chain_live_progress_evidence_lane"]
    assert owner_lane["state"] == "owner_refs_recorded_with_open_gates"
    assert owner_lane["evidence_ref"] == (
        "contracts/live_stage_run_progress_evidence.json#/domain_owner_chain_scaleout"
    )
    assert owner_lane["typed_blocker_ref"] == owner_refs["typed_blocker_ref"]
    assert owner_lane["counts_as_domain_ready"] is False
    assert owner_lane["counts_as_production_ready"] is False

    assert all(value is False for value in ledger["authority_boundary"].values())
