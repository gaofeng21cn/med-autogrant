from __future__ import annotations

import unittest

from med_autogrant.product_entry_parts import manifest_builder as manifest_builder_module
from med_autogrant.product_entry_parts.manifest_shell.runtime_task_shell import (
    build_manifest_runtime_task_shell,
)
from product_entry_cases.test_manifest_and_status_cases.context import ManifestStatusContext


def assert_runtime_control(
    test_case: unittest.TestCase,
    context: ManifestStatusContext,
) -> None:
    payload = context.payload
    manifest = context.manifest

    test_case.assertIs(
        manifest_builder_module.build_manifest_runtime_task_shell,
        build_manifest_runtime_task_shell,
    )
    test_case.assertEqual(
        manifest["opl_provider_runtime_contract"],
        {
            "shared_contract_ref": "contracts/opl-framework/managed-runtime-three-layer-contract.json",
            "runtime_owner": "configured_family_runtime_provider",
            "domain_owner": "med-autogrant",
            "executor_owner": "codex_cli",
            "supervision_status_surface": {
                "surface_kind": "grant_progress",
                "owner": "med-autogrant",
            },
            "attention_queue_surface": {
                "surface_kind": "grant_user_loop",
                "owner": "med-autogrant",
            },
            "recovery_contract_surface": {
                "surface_kind": "grant_user_loop",
                "owner": "med-autogrant",
            },
            "fail_closed_rules": [
                "domain_supervision_cannot_bypass_runtime",
                "executor_cannot_declare_global_gate_clear",
                "runtime_cannot_invent_domain_publishability_truth",
            ],
        },
    )
    test_case.assertEqual(manifest["runtime_inventory"]["surface_kind"], "runtime_inventory")
    test_case.assertEqual(
        manifest["runtime_inventory"]["runtime_owner"],
        "configured_family_runtime_provider",
    )
    test_case.assertEqual(
        manifest["runtime_inventory"]["domain_owner"],
        manifest["opl_provider_runtime_contract"]["domain_owner"],
    )
    test_case.assertEqual(manifest["task_lifecycle"]["surface_kind"], "task_lifecycle")
    test_case.assertEqual(
        manifest["task_lifecycle"]["status"],
        "forward_progress",
    )
    test_case.assertEqual(
        manifest["task_lifecycle"]["progress_surface"]["surface_kind"],
        "grant_progress",
    )
    test_case.assertEqual(manifest["persistence_policy"]["surface_kind"], "family_persistence_policy")
    test_case.assertEqual(
        manifest["persistence_policy"]["authority_surfaces"][0]["owner"],
        "med-autogrant",
    )
    test_case.assertEqual(manifest["lifecycle_ledger"]["surface_kind"], "family_lifecycle_ledger")
    test_case.assertEqual(
        manifest["lifecycle_ledger"]["actions"][0]["safety_gate"],
        "schema_and_shared_family_validator",
    )
    test_case.assertRegex(manifest["lifecycle_ledger"]["actions"][0]["sha256"], r"^[0-9a-f]{64}$")
    test_case.assertEqual(manifest["owner_route"]["surface_kind"], "family_owner_route")
    test_case.assertEqual(manifest["owner_route"]["next_owner"], "med-autogrant")
    test_case.assertIn("open_product_entry", manifest["owner_route"]["allowed_actions"])
    test_case.assertEqual(manifest["session_continuity"]["surface_kind"], "session_continuity")
    test_case.assertEqual(manifest["session_continuity"]["session_locator_field"], "grant_run_id")
    test_case.assertEqual(manifest["session_continuity"]["session_handle_kind"], "grant_run_id")
    test_case.assertEqual(manifest["session_continuity"]["session_id"], payload["grant_run_id"])
    test_case.assertEqual(manifest["session_continuity"]["session_owner"], "one-person-lab")
    test_case.assertEqual(
        manifest["session_continuity"]["generated_session_surface_ref"],
        "opl://generated-surfaces/mag/product-entry-session",
    )
    test_case.assertEqual(
        manifest["session_continuity"]["generated_resume_surface_ref"],
        "opl://generated-surfaces/mag/product-entry-session#resume",
    )
    test_case.assertEqual(
        manifest["session_continuity"]["domain_authority_surface_ref"],
        "/product_entry_manifest/owner_receipt_contract",
    )
    runtime_control = manifest["runtime_control"]
    test_case.assertEqual(runtime_control["surface_kind"], "runtime_control")
    test_case.assertEqual(runtime_control["runtime_owner"], "one-person-lab")
    test_case.assertEqual(runtime_control["domain_owner"], "med-autogrant")
    test_case.assertEqual(runtime_control["executor_owner"], "codex_cli")
    test_case.assertEqual(runtime_control["session_locator"]["locator_field"], "grant_run_id")
    test_case.assertEqual(runtime_control["session_locator"]["locator_value"], payload["grant_run_id"])
    test_case.assertEqual(runtime_control["restore_point"]["session_id"], payload["grant_run_id"])
    test_case.assertEqual(runtime_control["restore_point"]["lifecycle_stage"], payload["lifecycle_stage"])
    test_case.assertEqual(runtime_control["restore_point"]["session_owner"], "one-person-lab")
    test_case.assertEqual(
        runtime_control["restore_point"]["resume_surface_ref"],
        "opl://generated-surfaces/mag/product-entry-session#resume",
    )
    test_case.assertEqual(
        runtime_control["restore_point"]["domain_authority_surface_ref"],
        "/product_entry_manifest/owner_receipt_contract",
    )
    semantic_closure = runtime_control["semantic_closure"]
    test_case.assertEqual(semantic_closure["surface_kind"], "runtime_control_semantic_closure")
    test_case.assertEqual(semantic_closure["authoring_continuity"], "same_funding_call_task")
    test_case.assertEqual(semantic_closure["funding_call_lock"], "nsfc-2026-general")
    test_case.assertEqual(semantic_closure["quality_closure_surface"], "grant-quality-closure-dossier")
    test_case.assertEqual(
        semantic_closure["submission_ready_gate"],
        "package_submission_ready_strict_export_gate",
    )
    test_case.assertEqual(
        semantic_closure["closure_ref"],
        "/product_entry_manifest/grant_authoring_readiness",
    )
    test_case.assertEqual(runtime_control["progress_surface"]["surface_kind"], "grant_progress")
    test_case.assertEqual(runtime_control["artifact_pickup_surface"]["surface_kind"], "artifact_inventory")
    test_case.assertEqual(runtime_control["approval_control_surface"]["surface_kind"], "grant_user_loop")
    test_case.assertEqual(runtime_control["direct_entry"]["surface_kind"], "grant_direct_entry")
    test_case.assertIn("direct-entry", runtime_control["direct_entry"]["command"])
    observability = manifest["autonomy_observability"]
    test_case.assertEqual(observability["surface_kind"], "grant_autonomy_observability")
    test_case.assertEqual(observability["owner"], "med-autogrant")
    test_case.assertEqual(
        observability["sli_summary"]["task_status"],
        manifest["task_lifecycle"]["status"],
    )
    test_case.assertEqual(
        observability["sli_summary"]["runtime_health_status"],
        manifest["runtime_inventory"]["health_status"],
    )
    test_case.assertTrue(observability["sli_summary"]["same_funding_call_locked"])
    test_case.assertEqual(
        observability["sli_summary"]["remaining_gaps_count"],
        len(manifest["remaining_gaps"]),
    )
