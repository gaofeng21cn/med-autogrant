from __future__ import annotations

import json
from pathlib import Path


SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"


def load_schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def _properties(schema: dict[str, object], *path: str) -> dict[str, object]:
    node: object = schema
    for key in path:
        node = node[key]  # type: ignore[index]
    assert isinstance(node, dict)
    return node


def _false_consts(properties: dict[str, object], names: set[str]) -> None:
    for name in names:
        assert properties[name]["const"] is False  # type: ignore[index]


def test_product_surface_schemas_keep_manifest_companions_and_status_refs() -> None:
    manifest_schema = load_schema("product-entry-manifest.schema.json")
    status_schema = load_schema("product-status.schema.json")

    for schema_file in (
        "grant-progress.schema.json",
        "grant-cockpit.schema.json",
        "grant-direct-entry.schema.json",
        "grant-user-loop.schema.json",
    ):
        assert "family_orchestration" in load_schema(schema_file)["required"]

    manifest_required = set(manifest_schema["$defs"]["productEntryManifest"]["required"])
    assert {
        "opl_provider_runtime_contract",
        "runtime_control",
        "family_orchestration",
        "product_entry_start",
        "product_entry_overview",
        "product_entry_preflight",
        "product_entry_readiness",
        "grant_authoring_readiness",
        "owner_payload_response",
        "workspace_receipt_scaleout_evidence",
        "manifest_sustained_consumption_evidence",
        "mag_consumer_thinning_contract",
        "temporal_stage_run_consumption_policy",
    } <= manifest_required

    status_props = status_schema["$defs"]["productStatus"]["properties"]
    assert status_props["product_entry_start"]["$ref"] == (
        "product-entry-manifest.schema.json#/$defs/productEntryStart"
    )
    assert status_props["product_entry_readiness"]["$ref"] == (
        "product-entry-manifest.schema.json#/$defs/productEntryReadiness"
    )
    assert status_props["grant_authoring_readiness"]["$ref"] == (
        "product-entry-manifest.schema.json#/$defs/grantAuthoringReadiness"
    )


def test_manifest_schema_keeps_runtime_and_owner_authority_fail_closed() -> None:
    manifest_schema = load_schema("product-entry-manifest.schema.json")
    provider_runtime = manifest_schema["$defs"]["oplProviderRuntimeContractSurface"]
    runtime_control = manifest_schema["$defs"]["runtimeControlSurface"]
    policy = manifest_schema["$defs"]["temporalStageRunConsumptionPolicy"]
    owner_payload = manifest_schema["$defs"]["magOplOwnerPayloadResponse"]

    assert provider_runtime["properties"]["shared_contract_ref"]["const"] == (
        "contracts/opl-framework/managed-runtime-three-layer-contract.json"
    )
    assert provider_runtime["properties"]["runtime_owner"]["const"] == (
        "configured_family_runtime_provider"
    )
    assert runtime_control["properties"]["temporal_stage_run_consumption_policy"]["$ref"] == (
        "#/$defs/temporalStageRunConsumptionPolicy"
    )
    assert policy["properties"]["contract_ref"]["const"] == (
        "contracts/temporal_stage_run_consumption_policy.json"
    )
    _false_consts(
        policy["properties"],
        {
            "provider_completion_is_domain_completion",
            "domain_repo_can_own_temporal_runtime",
            "domain_repo_can_write_opl_stage_attempts",
            "domain_repo_can_own_stage_run_substrate",
            "generated_surface_ready_can_claim_domain_ready",
        },
    )
    _false_consts(
        policy["properties"]["authority_boundary"]["properties"],
        {
            "provider_completion_counts_as_domain_completion",
            "generated_surface_ready_counts_as_domain_ready",
            "mag_can_write_opl_stage_attempts",
            "mag_can_own_temporal_runtime",
        },
    )
    _false_consts(
        owner_payload["properties"],
        {
            "body_included",
            "grant_ready_claimed",
            "quality_ready_claimed",
            "export_ready_claimed",
            "submission_ready_claimed",
        },
    )
    _false_consts(
        owner_payload["properties"]["authority_boundary"]["properties"],
        {
            "opl_writes_grant_truth",
            "opl_reads_memory_body",
            "opl_reads_artifact_body",
            "opl_authorizes_quality_or_export",
            "can_declare_submission_ready",
        },
    )


def test_manifest_schema_keeps_consumer_thinning_request_only_boundary() -> None:
    manifest_schema = load_schema("product-entry-manifest.schema.json")
    thinning = manifest_schema["$defs"]["magConsumerThinningContract"]
    evidence_pack = thinning["properties"]["external_evidence_request_pack"]

    assert thinning["properties"]["minimal_authority_functions"]["$ref"] == (
        "#/$defs/ownerReceiptContract/properties/minimal_authority_functions"
    )
    assert evidence_pack["properties"]["state"]["const"] == (
        "request_pack_declared_external_evidence_not_claimed"
    )
    assert evidence_pack["properties"]["policy"]["const"] == (
        "request_refs_receipt_shapes_and_parity_only_no_runtime_implementation"
    )
    _false_consts(
        evidence_pack["properties"]["forbidden_completion_claims"]["properties"],
        {
            "provider_completion_is_fundability_ready",
            "provider_completion_is_quality_ready",
            "provider_completion_is_export_ready",
            "claims_opl_replacement_exists",
            "claims_all_bridge_exits_complete",
            "claims_production_long_run_soak_complete",
        },
    )
    _false_consts(
        evidence_pack["properties"]["authority_boundary"]["properties"],
        {
            "mag_implements_opl_runtime",
            "mag_implements_app_workbench",
            "mag_claims_external_evidence_exists",
            "mag_claims_direct_hosted_parity_passed",
            "mag_claims_long_soak_complete",
        },
    )
    assert (
        thinning["properties"]["functional_harness_consumer_coverage"]
        ["properties"]["claims_grant_ready"]["const"]
        is False
    )
    assert (
        thinning["properties"]["functional_followthrough_gap_classification"]
        ["properties"]["mag_functional_structure_gap_count"]["const"]
        == 0
    )
