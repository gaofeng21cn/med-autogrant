from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry import MedAutoGrantProductEntry
from med_autogrant.product_entry_parts.domain_agent_projection_surfaces import (
    OPL_LEDGER_ARTIFACT_REGISTRATION_CONTRACT_REF,
    OPL_LEDGER_ARTIFACT_REGISTRATION_KIND,
)
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = REPO_ROOT / OPL_LEDGER_ARTIFACT_REGISTRATION_CONTRACT_REF
REQUIRED_REGISTRATION_FIELDS = {
    "domain_id",
    "artifact_class",
    "artifact_ref",
    "artifact_hash",
    "index_ref",
    "review_ref",
    "receipt_ref",
}
FORBIDDEN_REGISTRATION_PAYLOAD_KEYS = {
    "grant_body",
    "artifact_body",
    "package_body",
    "memory_body",
    "fundability_verdict",
    "authoring_quality_verdict",
    "submission_ready_export_verdict",
    "owner_receipt",
    "typed_blocker",
    "runtime_queue_record",
    "provider_attempt_record",
}


def _read_contract() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def test_opl_ledger_artifact_registration_contract_is_refs_only() -> None:
    contract = _read_contract()

    assert contract["surface_kind"] == "opl_ledger_artifact_registration_contract"
    assert contract["domain_id"] == "med-autogrant"
    assert contract["target_ledger_owner"] == "one-person-lab"
    assert contract["refs_only"] is True
    assert set(contract["required_registration_fields"]) == REQUIRED_REGISTRATION_FIELDS
    assert set(contract["allowed_ref_fields"]) >= {
        "artifact_ref",
        "index_ref",
        "review_ref",
        "receipt_ref",
    }
    assert contract["hash_policy"] == {
        "required": True,
        "algorithm": "sha256",
        "field": "artifact_hash",
        "value_format": "sha256:<hex>",
    }

    forbidden_payloads = set(contract["forbidden_payload_fields"])
    assert {
        "grant_body",
        "artifact_body",
        "package_body",
        "fundability_verdict_body",
        "authoring_quality_verdict_body",
        "submission_ready_export_verdict_body",
        "owner_receipt_body",
        "typed_blocker_body",
        "runtime_queue_record_body",
        "provider_attempt_body",
    } <= forbidden_payloads
    assert {
        "fundability_verdict",
        "authoring_quality_verdict",
        "submission_ready_export_verdict",
        "package_export_authority_verdict",
        "owner_receipt",
        "typed_blocker",
        "runtime_queue_record",
        "provider_attempt_record",
    } <= set(contract["forbidden_authority_fields"])

    boundary = contract["authority_boundary"]
    assert boundary["mag_can_write_opl_ledger"] is False
    assert boundary["mag_can_emit_registration_projection"] is True
    assert boundary["opl_ledger_can_register_refs"] is True
    assert boundary["opl_ledger_can_read_artifact_body"] is False
    assert boundary["opl_ledger_can_write_grant_truth"] is False
    assert boundary["opl_ledger_can_create_owner_receipt"] is False
    assert boundary["opl_ledger_can_create_typed_blocker"] is False
    assert boundary["opl_ledger_can_authorize_quality_or_export"] is False
    assert boundary["opl_ledger_can_declare_submission_ready"] is False

    assert not any(contract["claim_boundary"].values())
    for artifact_class in contract["artifact_classes"]:
        assert set(artifact_class["required_fields"]) == REQUIRED_REGISTRATION_FIELDS


def test_opl_ledger_registration_projection_is_discoverable_from_manifest_readback() -> None:
    manifest = MedAutoGrantProductEntry().build_product_entry_manifest(
        input_path=str(CRITIQUE_EXAMPLE_PATH),
    )["product_entry_manifest"]
    projection = manifest["artifact_locator_contract"]["opl_ledger_artifact_registration"]
    contract = _read_contract()

    assert projection["surface_kind"] == OPL_LEDGER_ARTIFACT_REGISTRATION_KIND
    assert projection["contract_ref"] == OPL_LEDGER_ARTIFACT_REGISTRATION_CONTRACT_REF
    assert projection["domain_id"] == contract["domain_id"]
    assert projection["refs_only"] is True
    assert set(projection["required_registration_fields"]) == REQUIRED_REGISTRATION_FIELDS
    assert set(projection["required_registration_fields"]) == set(
        contract["required_registration_fields"]
    )
    assert projection["source_surface_refs"] == [
        "/product_entry_manifest/artifact_locator_contract",
        "/product_entry_manifest/artifact_inventory",
        "/product_entry_manifest/controlled_stage_attempt_projection",
    ]

    template = projection["registration_record_template"]
    assert set(template) == REQUIRED_REGISTRATION_FIELDS
    assert not (set(template) & FORBIDDEN_REGISTRATION_PAYLOAD_KEYS)
    assert template["artifact_hash"] == "sha256:<hex>"

    assert set(projection["forbidden_registration_fields"]) >= FORBIDDEN_REGISTRATION_PAYLOAD_KEYS
    assert projection["opl_ledger_command_refs"] == contract["opl_ledger_command_refs"]
    assert _false_claims(projection["claim_boundary"])
    assert _false_authority_transfers(projection["authority_boundary"])


def _false_claims(claim_boundary: Mapping[str, object]) -> bool:
    return all(value is False for value in claim_boundary.values())


def _false_authority_transfers(authority_boundary: Mapping[str, object]) -> bool:
    forbidden_transfer_fields = [
        "mag_can_write_opl_ledger",
        "opl_ledger_can_read_artifact_body",
        "opl_ledger_can_write_grant_truth",
        "opl_ledger_can_create_owner_receipt",
        "opl_ledger_can_create_typed_blocker",
        "opl_ledger_can_authorize_quality_or_export",
        "opl_ledger_can_declare_submission_ready",
    ]
    return all(authority_boundary[field] is False for field in forbidden_transfer_fields)
