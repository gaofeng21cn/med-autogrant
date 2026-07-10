from __future__ import annotations

import json
from pathlib import Path


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"


def _load(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def _assert_false(properties: dict[str, object], *names: str) -> None:
    assert all(properties[name]["const"] is False for name in names)


def test_product_schemas_keep_companions_and_owner_authority_fail_closed() -> None:
    manifest_schema = _load("product-entry-manifest.schema.json")
    manifest = manifest_schema["$defs"]["productEntryManifest"]
    status = _load("product-status.schema.json")["$defs"]["productStatus"]

    assert {
        "opl_provider_runtime_contract",
        "runtime_control",
        "product_entry_start",
        "product_entry_readiness",
        "grant_authoring_readiness",
        "owner_payload_response",
        "mag_consumer_thinning_contract",
        "temporal_stage_run_consumption_policy",
    } <= set(manifest["required"])
    assert manifest["properties"]["owner_payload_response"]["$ref"] == "#/$defs/magOplOwnerPayloadResponse"
    assert status["properties"]["product_entry_readiness"]["$ref"].endswith("#/$defs/productEntryReadiness")

    owner_payload = manifest_schema["$defs"]["magOplOwnerPayloadResponse"]
    _assert_false(
        owner_payload["properties"],
        "body_included",
        "grant_ready_claimed",
        "quality_ready_claimed",
        "export_ready_claimed",
        "submission_ready_claimed",
    )
    _assert_false(
        owner_payload["properties"]["authority_boundary"]["properties"],
        "opl_writes_grant_truth",
        "opl_reads_memory_body",
        "opl_reads_artifact_body",
        "opl_authorizes_quality_or_export",
        "can_declare_submission_ready",
    )

    policy = manifest_schema["$defs"]["temporalStageRunConsumptionPolicy"]
    _assert_false(
        policy["properties"],
        "provider_completion_is_domain_completion",
        "domain_repo_can_own_temporal_runtime",
        "domain_repo_can_write_opl_stage_attempts",
        "generated_surface_ready_can_claim_domain_ready",
    )


def test_consumer_thinning_schema_remains_request_only() -> None:
    thinning = _load("product-entry-manifest.schema.json")["$defs"]["magConsumerThinningContract"]
    evidence_pack = thinning["properties"]["external_evidence_request_pack"]

    assert thinning["properties"]["minimal_authority_functions"]["$ref"] == (
        "#/$defs/ownerReceiptContract/properties/minimal_authority_functions"
    )
    assert evidence_pack["properties"]["state"]["const"] == (
        "request_pack_declared_external_evidence_not_claimed"
    )
    _assert_false(
        evidence_pack["properties"]["forbidden_completion_claims"]["properties"],
        "provider_completion_is_fundability_ready",
        "provider_completion_is_quality_ready",
        "provider_completion_is_export_ready",
        "claims_opl_replacement_exists",
        "claims_production_long_run_soak_complete",
    )
    _assert_false(
        evidence_pack["properties"]["authority_boundary"]["properties"],
        "mag_implements_opl_runtime",
        "mag_implements_app_workbench",
        "mag_claims_external_evidence_exists",
        "mag_claims_long_soak_complete",
    )
