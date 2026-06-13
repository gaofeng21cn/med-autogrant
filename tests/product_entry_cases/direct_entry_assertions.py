from __future__ import annotations

import unittest
from typing import Any, Mapping

from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.domain_runtime_parts.shared import AUTHOR_SIDE_ROUTE_IDS
from product_entry_cases.support import (
    _expected_route,
    CANONICAL_EXPORT_SURFACES,
    CRITIQUE_EXAMPLE_PATH,
    PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
)


def assert_grant_direct_entry_composes_projection_and_entry_envelopes(
    test_case: unittest.TestCase,
    payload: Mapping[str, Any],
) -> None:
    _assert_direct_entry_payload_header(test_case, payload)
    _assert_runtime_control(test_case, payload)

    grant_direct_entry = payload["grant_direct_entry"]
    _assert_grant_direct_entry_header(test_case, grant_direct_entry)
    _assert_progress_projection(test_case, payload, grant_direct_entry["progress_projection"])
    test_case.assertEqual(
        grant_direct_entry["current_stage_route"],
        _expected_route("critique", source_stage="critique"),
    )
    test_case.assertEqual(
        grant_direct_entry["recommended_executor_route"],
        _expected_route("revision", source_stage="critique"),
    )

    expected_return_surface_contract = _expected_return_surface_contract(payload)
    runtime_substrate_contract = grant_direct_entry["direct_entry"]["runtime_session_contract"][
        "runtime_substrate_contract"
    ]
    _assert_runtime_substrate_contract(test_case, runtime_substrate_contract)
    for entry_key, entry_mode in (
        ("direct_entry", "direct"),
        ("opl_handoff_entry", "opl-handoff"),
    ):
        with test_case.subTest(entry_key=entry_key):
            _assert_entry_envelope(
                test_case,
                payload,
                grant_direct_entry[entry_key],
                entry_mode=entry_mode,
                expected_return_surface_contract=expected_return_surface_contract,
                runtime_substrate_contract=runtime_substrate_contract,
            )


def _assert_direct_entry_payload_header(
    test_case: unittest.TestCase,
    payload: Mapping[str, Any],
) -> None:
    test_case.assertEqual(payload["command"], "grant-direct-entry")
    test_case.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
    test_case.assertEqual(payload["workspace_id"], "nsfc-demo-001")
    test_case.assertEqual(payload["draft_id"], "draft-v1")
    test_case.assertEqual(payload["lifecycle_stage"], "critique")
    test_case.assertEqual(payload["grant_intake_audit"]["intake_status"], "ready")
    test_case.assertEqual(payload["grant_evidence_grounding"]["grounding_status"], "selection_grounded")
    test_case.assertEqual(payload["session_continuity"]["surface_kind"], "session_continuity")
    test_case.assertEqual(payload["session_continuity"]["session_id"], payload["grant_run_id"])
    test_case.assertEqual(payload["progress_projection"]["surface_kind"], "progress_projection")
    test_case.assertEqual(
        payload["progress_projection"]["projection"]["projection_kind"],
        "grant_progress",
    )
    test_case.assertEqual(payload["artifact_inventory"]["surface_kind"], "artifact_inventory")


def _assert_runtime_control(
    test_case: unittest.TestCase,
    payload: Mapping[str, Any],
) -> None:
    runtime_control = payload["runtime_control"]
    test_case.assertEqual(runtime_control["surface_kind"], "runtime_control")
    test_case.assertEqual(runtime_control["runtime_owner"], "one-person-lab")
    test_case.assertEqual(runtime_control["domain_owner"], "med-autogrant")
    test_case.assertEqual(runtime_control["executor_owner"], "codex_cli")
    test_case.assertEqual(runtime_control["session_locator"]["locator_value"], payload["grant_run_id"])
    test_case.assertEqual(runtime_control["restore_point"]["lifecycle_stage"], payload["lifecycle_stage"])
    test_case.assertIn(
        "--task-intent tighten-grant-mainline",
        runtime_control["approval_control_surface"]["command"],
    )
    test_case.assertIn(
        "--task-intent tighten-grant-mainline",
        runtime_control["direct_entry"]["command"],
    )


def _assert_grant_direct_entry_header(
    test_case: unittest.TestCase,
    grant_direct_entry: Mapping[str, Any],
) -> None:
    test_case.assertEqual(grant_direct_entry["entry_version"], 1)
    test_case.assertEqual(grant_direct_entry["entry_kind"], "grant_direct_entry")
    test_case.assertEqual(grant_direct_entry["target_domain_id"], "med-autogrant")
    test_case.assertEqual(grant_direct_entry["workspace_surface_kind"], "nsfc_workspace")
    test_case.assertEqual(grant_direct_entry["task_intent"], "tighten-grant-mainline")
    test_case.assertEqual(grant_direct_entry["workspace_status"], "attention_required")
    test_case.assertEqual(grant_direct_entry["workspace_alerts"], ["必要性表述仍略偏现象描述。"])
    test_case.assertEqual(
        grant_direct_entry["workspace_overview"]["selected_question"],
        "炎症巨噬细胞介导的跨细胞通讯机制如何在心梗后特定时间窗调控成纤维细胞致纤维化重编程？",
    )


def _assert_progress_projection(
    test_case: unittest.TestCase,
    payload: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
) -> None:
    test_case.assertEqual(progress_projection["projection_version"], 1)
    test_case.assertEqual(progress_projection["projection_kind"], "grant_progress")
    test_case.assertEqual(progress_projection["current_stage"], "critique")
    test_case.assertEqual(progress_projection["recommended_next_stage"], "revision")
    test_case.assertEqual(progress_projection["current_blockers"], ["必要性表述仍略偏现象描述。"])
    test_case.assertFalse(progress_projection["needs_author_decision"])
    test_case.assertEqual(
        progress_projection["currentness_resolver"]["authority_boundary"]["grant_truth_owner"],
        "med-autogrant",
    )
    test_case.assertFalse(
        progress_projection["currentness_resolver"]["authority_boundary"]["can_write_grant_truth"]
    )
    test_case.assertEqual(
        progress_projection["opl_progress_delta"]["progress_delta_classification"],
        "mixed",
    )
    test_case.assertEqual(
        progress_projection["status_narration_contract"]["facts"]["grant_run_id"],
        payload["grant_run_id"],
    )
    test_case.assertEqual(
        progress_projection["product_entry_surface"]["builder_command"],
        PUBLIC_PRODUCT_ENTRY_BUILDER_COMMAND,
    )


def _expected_return_surface_contract(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "entry_adapter": "MedAutoGrantDomainEntry",
        "default_formal_entry": "CLI",
        "supported_entry_modes": ["direct", "opl-handoff"],
        "domain_entry_contract": build_domain_entry_contract(),
        "checkpoint_aggregation_surface": "stage-route-report",
        "operator_contract": {
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
        "session_continuity": payload["session_continuity"],
        "progress_projection": payload["progress_projection"],
        "artifact_inventory": payload["artifact_inventory"],
        "runtime_control": payload["runtime_control"],
    }


def _assert_runtime_substrate_contract(
    test_case: unittest.TestCase,
    runtime_substrate_contract: Mapping[str, Any],
) -> None:
    test_case.assertEqual(runtime_substrate_contract["runtime_owner"], "configured_family_runtime_provider")
    test_case.assertEqual(runtime_substrate_contract["task_runtime_owner"], "one-person-lab")
    test_case.assertEqual(runtime_substrate_contract["runtime_substrate"], "temporal")
    test_case.assertEqual(runtime_substrate_contract["stage_executor_owner"], "codex_cli")


def _assert_entry_envelope(
    test_case: unittest.TestCase,
    payload: Mapping[str, Any],
    entry: Mapping[str, Any],
    *,
    entry_mode: str,
    expected_return_surface_contract: Mapping[str, Any],
    runtime_substrate_contract: Mapping[str, Any],
) -> None:
    test_case.assertEqual(entry["entry_version"], 1)
    test_case.assertEqual(entry["entry_kind"], "med_auto_grant_product_entry")
    test_case.assertEqual(entry["target_domain_id"], "med-autogrant")
    test_case.assertEqual(entry["task_intent"], "tighten-grant-mainline")
    test_case.assertEqual(entry["entry_mode"], entry_mode)
    test_case.assertEqual(
        entry["workspace_locator"],
        {
            "workspace_surface_kind": "nsfc_workspace",
            "workspace_path": str(CRITIQUE_EXAMPLE_PATH.resolve()),
        },
    )
    test_case.assertEqual(entry["return_surface_contract"], expected_return_surface_contract)
    test_case.assertEqual(
        entry["domain_payload"],
        {
            "workspace_id": "nsfc-demo-001",
            "draft_id": "draft-v1",
            "funding_call": "nsfc-2026-general",
        },
    )
    test_case.assertEqual(
        entry["stage_snapshot"],
        {
            "lifecycle_stage": "critique",
            "checkpoint_status": "forward_progress",
            "recommended_next_stage": "revision",
        },
    )
    _assert_runtime_session_contract(
        test_case,
        payload,
        entry["runtime_session_contract"],
        runtime_substrate_contract=runtime_substrate_contract,
    )
    _assert_executor_routing_contract(test_case, entry["executor_routing_contract"])


def _assert_runtime_session_contract(
    test_case: unittest.TestCase,
    payload: Mapping[str, Any],
    runtime_session_contract: Mapping[str, Any],
    *,
    runtime_substrate_contract: Mapping[str, Any],
) -> None:
    test_case.assertEqual(runtime_session_contract["grant_run_id"], payload["grant_run_id"])
    test_case.assertEqual(runtime_session_contract["session_handle_kind"], "grant_run_id")
    test_case.assertEqual(runtime_session_contract["session_owner"], "one-person-lab")
    test_case.assertEqual(
        runtime_session_contract["generated_session_surface_ref"],
        "opl://generated-surfaces/mag/product-entry-session",
    )
    test_case.assertEqual(
        runtime_session_contract["generated_resume_surface_ref"],
        "opl://generated-surfaces/mag/product-entry-session#resume",
    )
    test_case.assertEqual(
        runtime_session_contract["domain_authority_surface_ref"],
        "/product_entry_manifest/owner_receipt_contract",
    )
    test_case.assertEqual(
        runtime_session_contract["runtime_substrate_contract"],
        runtime_substrate_contract,
    )
    test_case.assertEqual(
        runtime_session_contract["runtime_state_contract"]["root"],
        "$CODEX_HOME/projects/med-autogrant/runtime-state/",
    )
    test_case.assertTrue(runtime_session_contract["runtime_state_contract"]["non_repo_tracked"])


def _assert_executor_routing_contract(
    test_case: unittest.TestCase,
    executor_routing_contract: Mapping[str, Any],
) -> None:
    test_case.assertEqual(executor_routing_contract["contract_version"], 1)
    test_case.assertEqual(
        executor_routing_contract["current_stage_route"],
        _expected_route("critique", source_stage="critique"),
    )
    test_case.assertEqual(
        executor_routing_contract["recommended_executor_route"],
        _expected_route("revision", source_stage="critique"),
    )
    test_case.assertEqual(
        executor_routing_contract["author_side_route_catalog"],
        [_expected_route(route_id, source_stage=route_id) for route_id in AUTHOR_SIDE_ROUTE_IDS],
    )
