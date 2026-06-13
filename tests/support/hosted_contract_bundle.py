from __future__ import annotations

import unittest
from collections.abc import Mapping

from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.domain_runtime_parts.contracts import build_operator_contract
from med_autogrant.domain_runtime_parts.shared import AUTHOR_SIDE_ROUTE_IDS


CANONICAL_EXPORT_SURFACES = build_operator_contract()["canonical_export_surfaces"]


def assert_hosted_contract_bundle_contract(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
    *,
    current_runtime_owner: Mapping[str, str],
) -> None:
    _assert_hosted_contract_bundle_header(test_case, contract_bundle)
    _assert_hosted_runtime_contracts(
        test_case,
        contract_bundle,
        current_runtime_owner=current_runtime_owner,
    )
    _assert_hosted_domain_and_schema_contracts(test_case, contract_bundle)
    _assert_hosted_authoring_contract(test_case, contract_bundle)


def _assert_hosted_contract_bundle_header(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
) -> None:
    test_case.assertEqual(contract_bundle["contract_version"], 1)
    test_case.assertEqual(contract_bundle["bundle_kind"], "hosted_contract_bundle")
    test_case.assertEqual(
        contract_bundle["formal_entry_matrix"],
        {
            "default_formal_entry": "CLI",
            "supported_protocol_layer": "MCP",
            "internal_controller_surface": "controller",
        },
    )
    test_case.assertEqual(
        contract_bundle["execution_identity"],
        {
            "grant_run_id": "grant-run-nsfc-demo-001-baseline-001",
            "workspace_id": "nsfc-demo-001",
            "draft_id": "draft-v1",
            "program_id": "med-autogrant-mainline",
        },
    )


def _assert_hosted_runtime_contracts(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
    *,
    current_runtime_owner: Mapping[str, str],
) -> None:
    test_case.assertEqual(
        contract_bundle["runtime_substrate_contract"],
        {
            "runtime_owner": "configured_family_runtime_provider",
            "task_runtime_owner": "one-person-lab",
            "runtime_substrate": "temporal",
            "stage_executor_owner": "codex_cli",
            "current_owner_line": current_runtime_owner["current_owner_line"],
            "active_phase": current_runtime_owner["active_phase"],
            "active_tranche": current_runtime_owner["active_tranche"],
            "provenance_oracle": current_runtime_owner["provenance_oracle"],
            "repo_tracked_current_program_contract": "contracts/runtime-program/current-program.json",
        },
    )
    test_case.assertEqual(
        contract_bundle["runtime_state_contract"],
        {
            "root": "$CODEX_HOME/projects/med-autogrant/runtime-state/",
            "session_state_owner": "one-person-lab",
            "generated_session_surface_ref": "opl://generated-surfaces/mag/product-entry-session",
            "generated_resume_surface_ref": "opl://generated-surfaces/mag/product-entry-session#resume",
            "logs_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/logs/",
            "reports_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/reports/<program_id>/",
            "prompts_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/prompts/",
            "handoff_state_root": "$CODEX_HOME/projects/med-autogrant/runtime-state/handoff_state/",
            "non_repo_tracked": True,
        },
    )
    test_case.assertEqual(
        contract_bundle["session_contract"],
        {
            "session_handle_kind": "grant_run_id",
            "session_owner": "one-person-lab",
            "generated_session_surface_ref": "opl://generated-surfaces/mag/product-entry-session",
            "generated_resume_surface_ref": "opl://generated-surfaces/mag/product-entry-session#resume",
            "domain_authority_surface_ref": "/product_entry_manifest/owner_receipt_contract",
            "required_mag_authority_surfaces": [
                "build-artifact-bundle",
                "build-final-package",
                "build-submission-ready-package",
                "owner_receipt_contract",
                "grant_transition_oracle",
            ],
        },
    )
    test_case.assertEqual(
        contract_bundle["operator_contract"],
        {
            "canonical_audit_surfaces": [
                "validate-workspace",
                "summarize-workspace",
                "grant-intake-audit",
                "grant-evidence-grounding",
                "grant-quality-scorecard",
                "grant-quality-closure-dossier",
                "grant-quality-diff",
                "next-step",
                "critique-summary",
                "stage-route-report",
            ],
            "canonical_export_surfaces": CANONICAL_EXPORT_SURFACES,
            "checkpoint_aggregation_surface": "stage-route-report",
        },
    )


def _assert_hosted_domain_and_schema_contracts(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
) -> None:
    test_case.assertEqual(
        contract_bundle["state_contract"],
        {
            "workspace_surface_kind": "nsfc_workspace",
            "session_surface_kind": "opl_generated_session_surface",
            "domain_authority_surface_kind": "owner_receipt_contract",
            "artifact_bundle_kind": "artifact_bundle",
            "final_package_kind": "final_package",
        },
    )
    test_case.assertEqual(
        contract_bundle["artifact_contract"],
        {
            "artifact_bundle_manifest_kind": "artifact_bundle_manifest",
            "final_package_manifest_kind": "freeze_manifest",
            "lineage_fields": [
                "frozen_question_id",
                "selected_direction_id",
                "selected_question_id",
                "active_fit_mapping_id",
                "draft_id",
                "revision_plan_id",
            ],
        },
    )
    test_case.assertEqual(
        contract_bundle["audit_contract"],
        {
            "verification_checkpoint_kind": "verification_checkpoint",
            "checkpoint_status_kind": "checkpoint_status",
            "reviewed_revision_evidence_kind": "reviewed_revision_evidence",
        },
    )
    test_case.assertEqual(
        contract_bundle["domain_entry_contract"],
        build_domain_entry_contract(),
    )
    test_case.assertEqual(
        contract_bundle["schema_contract"],
        {
            "schema_version": "v1",
            "schema_index_path": "schemas/v1/schema-index.json",
            "aggregate_root_schema": "nsfc-workspace.schema.json",
            "contract_schema_files": [
                "service-safe-domain-surface.schema.json",
                "executor-routing-contract.schema.json",
                "product-entry.schema.json",
                "grant-intake-audit.schema.json",
                "grant-evidence-grounding.schema.json",
                "grant-quality-scorecard.schema.json",
                "grant-quality-closure-dossier.schema.json",
                "grant-quality-diff.schema.json",
                "grant-autonomy-controller-input.schema.json",
                "grant-autonomy-controller-report.schema.json",
                "funding-landscape-discovery-input.schema.json",
                "funding-landscape-discovery.schema.json",
                "funding-landscape-cache.schema.json",
                "funding-landscape-diff-report.schema.json",
                "project-profile-selection-input.schema.json",
                "project-profile-selection.schema.json",
                "critique-loop-report.schema.json",
                "authoring-mainline-loop-report.schema.json",
                "hosted-contract-bundle.schema.json",
                "submission-ready-package.schema.json",
            ],
        },
    )


def _assert_hosted_authoring_contract(
    test_case: unittest.TestCase,
    contract_bundle: dict[str, object],
) -> None:
    authoring_contract = contract_bundle["authoring_contract"]
    test_case.assertEqual(authoring_contract["route_contract_version"], 1)
    test_case.assertEqual(
        authoring_contract["route_catalog_kind"],
        "author_side_route_catalog",
    )
    test_case.assertEqual(
        [route["route_id"] for route in authoring_contract["author_side_route_catalog"]],
        list(AUTHOR_SIDE_ROUTE_IDS),
    )
    route_catalog = {route["route_id"]: route for route in authoring_contract["author_side_route_catalog"]}
    test_case.assertEqual(route_catalog["critique"]["route_status"], "landed")
    test_case.assertEqual(route_catalog["critique"]["handoff_contract_kind"], "service-safe-domain-entry-command")
    test_case.assertEqual(route_catalog["critique"]["execution_surface"]["command"], "execute-critique-pass")
    test_case.assertEqual(route_catalog["revision"]["route_status"], "landed")
    test_case.assertEqual(route_catalog["revision"]["execution_surface"]["command"], "execute-revision-pass")
    test_case.assertEqual(route_catalog["hosted_contract_bundle"]["route_status"], "landed")
    test_case.assertEqual(
        route_catalog["hosted_contract_bundle"]["execution_surface"]["command"],
        "build-hosted-contract-bundle",
    )
