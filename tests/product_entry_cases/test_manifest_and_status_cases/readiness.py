from __future__ import annotations

import unittest

from med_autogrant.public_cli import public_cli_command

from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH
from product_entry_cases.test_manifest_and_status_cases.context import ManifestStatusContext


def assert_readiness_surfaces(
    test_case: unittest.TestCase,
    context: ManifestStatusContext,
) -> None:
    manifest = context.manifest

    test_case.assertEqual(manifest["product_entry_overview"]["surface_kind"], "product_entry_overview")
    test_case.assertEqual(
        manifest["product_entry_overview"]["summary"],
        manifest["product_entry_status"]["summary"],
    )
    test_case.assertEqual(
        manifest["product_entry_overview"]["product_entry_command"],
        public_cli_command(
            "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertEqual(
        manifest["product_entry_overview"]["recommended_command"],
        public_cli_command(
            "grant-user-loop",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH.resolve()),
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
    )
    test_case.assertEqual(
        manifest["product_entry_overview"]["progress_surface"],
        {
            "surface_kind": "grant_progress",
            "command": public_cli_command(
                "grant-progress", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
            ),
            "step_id": "inspect_progress",
        },
    )
    test_case.assertEqual(
        manifest["product_entry_overview"]["resume_surface"],
        {
            "surface_kind": "grant_user_loop",
            "command": public_cli_command(
                "grant-user-loop",
                "--input",
                str(CRITIQUE_EXAMPLE_PATH.resolve()),
                "--task-intent",
                "<describe-task-intent>",
                "--format",
                "json",
            ),
            "session_locator_field": "grant_run_id",
            "checkpoint_locator_field": "lifecycle_stage",
        },
    )
    test_case.assertEqual(manifest["product_entry_overview"]["recommended_step_id"], "open_product_entry")
    test_case.assertEqual(
        manifest["product_entry_overview"]["next_focus"],
        manifest["product_entry_status"]["next_focus"],
    )
    test_case.assertEqual(
        manifest["product_entry_overview"]["remaining_gaps_count"],
        manifest["product_entry_status"]["remaining_gaps_count"],
    )
    test_case.assertEqual(
        manifest["product_entry_overview"]["human_gate_ids"],
        ["mag_route_gate_revision"],
    )
    preflight = manifest["product_entry_preflight"]
    test_case.assertEqual(preflight["surface_kind"], "product_entry_preflight")
    test_case.assertEqual(
        preflight["summary"],
        "当前 direct grant product entry surface 的前置检查已通过，可以先复核 workspace 与主线，再进入 OPL/App generated status target 或 domain-handler export。",
    )
    test_case.assertTrue(preflight["ready_to_try_now"])
    test_case.assertEqual(
        preflight["recommended_check_command"],
        public_cli_command(
            "validate-workspace", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertEqual(
        preflight["recommended_start_command"],
        public_cli_command(
            "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertEqual(preflight["blocking_check_ids"], [])
    test_case.assertEqual(
        [check["check_id"] for check in preflight["checks"]],
        [
            "workspace_document_valid",
            "default_runtime_owner_line",
            "direct_product entry surface_contract_landed",
            "submission_ready_export_gate",
        ],
    )
    test_case.assertEqual(preflight["checks"][0]["status"], "pass")
    test_case.assertEqual(preflight["checks"][0]["blocking"], True)
    test_case.assertEqual(preflight["checks"][1]["status"], "pass")
    test_case.assertEqual(preflight["checks"][2]["status"], "pass")
    test_case.assertEqual(preflight["checks"][3]["status"], "warn")
    product_readiness = manifest["product_entry_readiness"]
    test_case.assertEqual(product_readiness["surface_kind"], "product_entry_readiness")
    test_case.assertEqual(product_readiness["verdict"], "agent_assisted_ready_not_product_grade")
    test_case.assertTrue(product_readiness["usable_now"])
    test_case.assertFalse(product_readiness["good_to_use_now"])
    test_case.assertFalse(product_readiness["fully_automatic"])
    test_case.assertEqual(product_readiness["recommended_start_surface"], "product_status")
    test_case.assertEqual(
        product_readiness["recommended_start_command"],
        public_cli_command(
            "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertEqual(product_readiness["recommended_loop_surface"], "grant_user_loop")
    test_case.assertEqual(
        product_readiness["recommended_loop_command"],
        public_cli_command(
            "grant-user-loop",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH.resolve()),
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
    )
    test_case.assertIn("还不是 mature direct grant Web UI / hosted runtime。", product_readiness["blocking_gaps"])
    readiness = manifest["grant_authoring_readiness"]
    test_case.assertEqual(readiness["surface_kind"], "grant_authoring_readiness")
    test_case.assertEqual(readiness["verdict"], "agent_assisted_cli_ready_not_full_autopilot")
    test_case.assertFalse(readiness["fully_automatic"])
    test_case.assertTrue(readiness["usable_now"])
    test_case.assertFalse(readiness["good_to_use_now"])
    test_case.assertEqual(readiness["recommended_start_surface"], "product_status")
    test_case.assertEqual(
        readiness["recommended_start_command"],
        public_cli_command(
            "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertEqual(readiness["recommended_loop_surface"], "grant_user_loop")
    test_case.assertEqual(
        [item["step_id"] for item in readiness["workflow_coverage"]],
        [
            "accumulation_direction_screening",
            "hotspot_literature_fit",
            "clinical_question_refinement",
            "innovation_framework",
            "mainline_closure",
            "significance_background_drafting",
            "preliminary_evidence_and_basis",
            "expected_results_timeline",
            "final_review_figures_package",
        ],
    )
    test_case.assertEqual(readiness["workflow_coverage"][0]["coverage_status"], "landed_route")
    test_case.assertEqual(readiness["workflow_coverage"][1]["coverage_status"], "partially_supported")
    test_case.assertIn("还不是 mature direct grant Web UI / hosted runtime。", readiness["blocking_gaps"])
