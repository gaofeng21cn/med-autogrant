from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "schemas" / "v1"
REQUIRED_PRODUCT_ENTRY_OWNER_SURFACES = {
    "opl_provider_runtime_contract",
    "runtime_control",
    "family_orchestration",
    "family_action_catalog",
    "family_stage_control_plane",
    "controlled_stage_attempt_projection",
    "mag_consumer_thinning_contract",
    "temporal_stage_run_consumption_policy",
}
TEMPORAL_POLICY_OWNER_CONSTS = {
    "owner": "med-autogrant",
    "runtime_substrate_owner": "one-person-lab",
    "stage_run_substrate_owner": "one-person-lab",
    "domain_truth_owner": "med-autogrant",
    "temporal_attempt_ledger_owner": "one-person-lab/OPL",
}


def _load(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def _assert_false(properties: dict[str, Any], *names: str) -> None:
    assert all(properties[name]["const"] is False for name in names)


def test_product_schemas_keep_companions_and_owner_authority_fail_closed() -> None:
    manifest_schema = _load("product-entry-manifest.schema.json")
    manifest = manifest_schema["$defs"]["productEntryManifest"]
    status = _load("product-status.schema.json")["$defs"]["productStatus"]

    assert REQUIRED_PRODUCT_ENTRY_OWNER_SURFACES <= set(manifest["required"])
    manifest_refs = {
        "product_entry_start": "productEntryStart",
        "product_entry_overview": "productEntryOverview",
        "product_entry_preflight": "productEntryPreflight",
        "product_entry_readiness": "productEntryReadiness",
        "grant_authoring_readiness": "grantAuthoringReadiness",
        "owner_payload_response": "magOplOwnerPayloadResponse",
        "workspace_receipt_scaleout_evidence": "magWorkspaceReceiptScaleoutEvidence",
        "manifest_sustained_consumption_evidence": "magManifestSustainedConsumptionEvidence",
        "temporal_stage_run_consumption_policy": "temporalStageRunConsumptionPolicy",
    }
    for field, definition in manifest_refs.items():
        assert manifest["properties"][field]["$ref"] == f"#/$defs/{definition}"

    for field, definition in (
        ("product_entry_start", "productEntryStart"),
        ("product_entry_overview", "productEntryOverview"),
        ("product_entry_preflight", "productEntryPreflight"),
        ("product_entry_readiness", "productEntryReadiness"),
        ("grant_authoring_readiness", "grantAuthoringReadiness"),
    ):
        assert status["properties"][field]["$ref"] == (
            f"product-entry-manifest.schema.json#/$defs/{definition}"
        )

    for definition, surface_kind, required in (
        (
            "productEntryOverview",
            "product_entry_overview",
            {
                "surface_kind",
                "summary",
                "product_entry_command",
                "recommended_command",
                "operator_loop_command",
                "project_profile_label",
                "template_label",
                "critique_policy_id",
                "progress_surface",
                "resume_surface",
                "recommended_step_id",
                "next_focus",
                "remaining_gaps_count",
                "human_gate_ids",
            },
        ),
        (
            "productEntryPreflight",
            "product_entry_preflight",
            {
                "surface_kind",
                "summary",
                "ready_to_try_now",
                "recommended_check_command",
                "recommended_start_command",
                "blocking_check_ids",
                "checks",
            },
        ),
    ):
        surface = manifest_schema["$defs"][definition]
        assert set(surface["required"]) == required
        assert surface["properties"]["surface_kind"]["const"] == surface_kind

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
        "domain_repo_can_own_stage_run_substrate",
        "mag_can_own_status_user_loop_direct_entry_domain_handler_or_workbench_shell",
        "generated_surface_ready_can_claim_domain_ready",
        "mag_writes_opl_stage_attempt_records",
    )
    _assert_false(
        policy["properties"]["authority_boundary"]["properties"],
        "mag_can_write_opl_stage_attempts",
        "mag_can_own_temporal_runtime",
        "provider_completion_counts_as_domain_completion",
        "generated_surface_ready_counts_as_domain_ready",
    )
    assert {
        field for field in policy["required"] if field == "owner" or field.endswith("_owner")
    } == set(TEMPORAL_POLICY_OWNER_CONSTS)
    assert {
        field: policy["properties"][field]["const"]
        for field in TEMPORAL_POLICY_OWNER_CONSTS
    } == TEMPORAL_POLICY_OWNER_CONSTS


def test_receipt_and_temporal_nested_authority_remains_fail_closed() -> None:
    definitions = _load("product-entry-manifest.schema.json")["$defs"]
    workspace_receipt = definitions["magWorkspaceReceiptScaleoutEvidence"]
    sustained_receipt = definitions["magManifestSustainedConsumptionEvidence"]
    grouped_evidence = sustained_receipt["properties"]["grouped_cli_regression_evidence"]["properties"]
    temporal = definitions["temporalStageRunConsumptionPolicy"]
    stage_boundary = temporal["properties"]["stage_run_consumption_boundary"]["properties"]
    completion_audit = temporal["properties"]["grant_ready_completion_audit"]["properties"]

    false_groups = (
        (
            workspace_receipt["properties"]["owner_payload_response"]["properties"],
            ("stage_payload_body_allowed", "stage_success_refs_visible_is_completion"),
        ),
        (
            workspace_receipt["properties"]["claims"]["properties"],
            (
                "claims_grant_ready",
                "claims_quality_ready",
                "claims_export_ready",
                "claims_submission_ready_export",
                "claims_provider_long_soak_complete",
                "claims_physical_delete_authorized",
            ),
        ),
        (
            workspace_receipt["properties"]["authority_boundary"]["properties"],
            (
                "can_write_memory_body",
                "can_mutate_grant_artifact",
                "can_authorize_quality_or_export",
                "can_declare_submission_ready",
                "typed_blocker_is_submission_ready",
            ),
        ),
        (
            grouped_evidence,
            (
                "success_path_claims_provider_long_soak_complete",
                "body_included",
                "claims_sustained_app_consumption_complete",
                "claims_provider_long_soak_complete",
                "closes_provider_long_soak",
            ),
        ),
        (
            grouped_evidence["authority_boundary"]["properties"],
            (
                "can_write_grant_truth",
                "can_read_memory_body",
                "can_read_artifact_body",
                "can_create_owner_receipt",
                "can_submit_operator_payload",
                "can_declare_app_sustained_consumption_complete",
                "can_declare_submission_ready",
                "can_declare_provider_long_soak_complete",
            ),
        ),
        (
            sustained_receipt["properties"]["claims"]["properties"],
            (
                "claims_sustained_app_consumption_complete",
                "claims_grant_ready",
                "claims_quality_ready",
                "claims_export_ready",
                "claims_submission_ready",
                "claims_provider_long_soak_complete",
                "claims_owner_receipt_created",
            ),
        ),
        (
            sustained_receipt["properties"]["authority_boundary"]["properties"],
            (
                "can_write_grant_truth",
                "can_read_memory_body",
                "can_read_artifact_body",
                "can_create_owner_receipt",
                "can_submit_operator_payload",
                "can_declare_app_sustained_consumption_complete",
                "can_declare_submission_ready",
                "can_declare_provider_long_soak_complete",
            ),
        ),
        (
            stage_boundary,
            ("payload_body_allowed", "mag_runtime_state_write_allowed"),
        ),
        (
            stage_boundary["authority_boundary"]["properties"],
            (
                "mag_can_start_temporal_worker",
                "mag_can_schedule_stage_run",
                "mag_can_write_attempt_ledger",
                "mag_can_own_generated_shell",
                "opl_can_write_grant_truth",
                "opl_can_sign_mag_owner_receipt",
                "provider_completion_counts_as_domain_completion",
            ),
        ),
        (
            completion_audit["claim_permissions"]["properties"],
            (
                "domain_ready",
                "grant_ready",
                "fundability_ready",
                "quality_ready",
                "export_ready",
                "submission_ready",
                "production_ready",
            ),
        ),
        (
            completion_audit["authority_boundary"]["properties"],
            (
                "provider_completion_counts_as_grant_ready",
                "schema_completeness_counts_as_grant_ready",
                "generated_surface_ready_counts_as_grant_ready",
                "focused_tests_count_as_grant_ready",
                "stage_replay_counts_as_submission_ready",
                "package_existence_counts_as_submission_ready",
                "quality_scorecard_counts_as_quality_ready",
            ),
        ),
    )
    for properties, fields in false_groups:
        _assert_false(properties, *fields)


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
