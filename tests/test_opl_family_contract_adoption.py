from __future__ import annotations

import json
from pathlib import Path

import pytest


pytestmark = pytest.mark.meta

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = "contracts/runtime-program/opl-family-contract-adoption.json"
DOC_PATH = "docs/references/opl_family_contract_adoption.md"


def _read(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def _contract() -> dict[str, object]:
    return json.loads(_read(CONTRACT_PATH))


def test_mag_declares_thin_opl_family_contract_adoption() -> None:
    contract = _contract()
    doc = _read(DOC_PATH)

    assert contract["contract_kind"] == "mag_opl_family_contract_adoption.v1"
    assert contract["domain_id"] == "med-autogrant"
    assert contract["opl_role"] == "family-level projection consumer only"
    assert "不把 `OPL` 变成 grant authoring owner" in doc


def test_mag_runtime_projection_maps_to_grant_runtime_truth_surfaces() -> None:
    contract = _contract()
    doc = _read(DOC_PATH)
    attempt = contract["attempt_projection"]

    for surface in (
        "runtime_control",
        "runtime_continuity",
        "grant-autonomy-controller-report",
        "workspace progress",
    ):
        assert surface in attempt["source_surfaces"]
        assert surface in doc
    assert attempt["maps_to_opl_contract"] == "opl_family_runtime_attempt_contract.v1"
    assert "MAG owns grant authoring runtime" in attempt["owner_boundary"]


def test_mag_quality_projection_keeps_grant_quality_owner_and_excludes_other_domain_gates() -> None:
    contract = _contract()
    doc = _read(DOC_PATH)
    quality = contract["quality_projection"]

    for surface in (
        "grant_quality_scorecard",
        "grant_quality_closure_dossier",
        "grant review",
        "fundability gate",
        "submission-ready export gate",
    ):
        assert surface in quality["source_surfaces"]
        assert surface in doc
    assert quality["maps_to_opl_contract"] == "opl_family_domain_quality_projection_contract.v1"
    assert quality["claim_only_ready_forbidden"] is True
    for forbidden in (
        "claim-only ready",
        "generic persona QA",
        "medical publication gate",
        "visual render/export proof gate",
        "OPL projection-only",
    ):
        assert forbidden in doc


def test_mag_operator_and_incident_projection_require_source_refs_and_mag_closure() -> None:
    contract = _contract()
    doc = _read(DOC_PATH)
    incident = contract["incident_projection"]
    operator = contract["operator_projection"]

    assert incident["maps_to_opl_contract"] == "opl_family_incident_learning_loop.v1"
    assert "MAG-owned closure ref" in incident["closure_rule"]
    for field in ("source_refs", "freshness", "owner_split", "next_surface_ref", "human_gate_reason"):
        assert field in operator["required_fields"]
        assert field.replace("_", " ") in doc or field in doc
    for non_goal in (
        "OPL owns grant truth",
        "OPL bypasses submission-ready export gate",
        "medical publication gate",
        "visual render/export proof gate",
    ):
        assert non_goal in contract["non_goals"]

