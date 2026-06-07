from __future__ import annotations

import unittest

from med_autogrant.public_cli import public_cli_command

from product_entry_cases.support import (
    _assert_family_orchestration_companion,
    CRITIQUE_EXAMPLE_PATH,
)
from product_entry_cases.test_manifest_and_status_cases.context import ManifestStatusContext


def assert_start_surfaces(
    test_case: unittest.TestCase,
    context: ManifestStatusContext,
) -> None:
    manifest = context.manifest

    test_case.assertEqual(
        manifest["product_entry_shell"]["grant_progress"]["command"],
        public_cli_command(
            "grant-progress", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertEqual(
        manifest["product_entry_shell"]["grant_user_loop"]["command"],
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
        manifest["product_entry_shell"]["product_status"]["command"],
        public_cli_command(
            "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertEqual(
        manifest["shared_handoff"]["direct_entry_builder"]["command"],
        public_cli_command(
            "build-product-entry",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH.resolve()),
            "--entry-mode",
            "direct",
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
    )
    test_case.assertEqual(
        manifest["shared_handoff"]["opl_handoff_builder"]["command"],
        public_cli_command(
            "build-product-entry",
            "--input",
            str(CRITIQUE_EXAMPLE_PATH.resolve()),
            "--entry-mode",
            "opl-handoff",
            "--task-intent",
            "<describe-task-intent>",
            "--format",
            "json",
        ),
    )
    _assert_family_orchestration_companion(
        test_case,
        manifest.get("family_orchestration"),
        expected_resume_surface="grant_user_loop",
    )
    test_case.assertEqual(
        manifest["family_orchestration"]["human_gates"][0]["gate_id"],
        "mag_route_gate_revision",
    )
    test_case.assertEqual(
        manifest["family_orchestration"]["event_envelope_surface"]["ref"],
        "/product_entry_manifest/recommended_command",
    )
    test_case.assertEqual(
        manifest["family_orchestration"]["checkpoint_lineage_surface"]["ref"],
        "/product_entry_manifest/repo_mainline/active_phase",
    )
    test_case.assertEqual(manifest["product_entry_quickstart"]["surface_kind"], "product_entry_quickstart")
    test_case.assertEqual(
        manifest["product_entry_quickstart"]["recommended_step_id"],
        "open_product_entry",
    )
    test_case.assertEqual(
        [step["step_id"] for step in manifest["product_entry_quickstart"]["steps"]],
        [
            "open_product_entry",
            "continue_grant_loop",
            "inspect_progress",
            "inspect_cockpit",
            "build_submission_ready_package",
        ],
    )
    test_case.assertEqual(
        manifest["product_entry_quickstart"]["steps"][0]["command"],
        public_cli_command(
            "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertEqual(
        manifest["product_entry_quickstart"]["steps"][1]["requires"],
        ["task_intent"],
    )
    test_case.assertEqual(
        manifest["product_entry_quickstart"]["steps"][4]["requires"],
        ["output_dir"],
    )
    test_case.assertEqual(
        manifest["product_entry_quickstart"]["resume_contract"],
        manifest["family_orchestration"]["resume_contract"],
    )
    test_case.assertEqual(
        manifest["product_entry_quickstart"]["human_gate_ids"],
        ["mag_route_gate_revision"],
    )
    product_start = manifest["product_entry_start"]
    test_case.assertEqual(product_start["surface_kind"], "product_entry_start")
    test_case.assertEqual(product_start["recommended_mode_id"], "open_product_entry")
    test_case.assertEqual(
        [mode["mode_id"] for mode in product_start["modes"]],
        ["open_product_entry", "continue_grant_loop", "build_direct_entry"],
    )
    test_case.assertEqual(
        product_start["modes"][0]["command"],
        public_cli_command(
            "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertEqual(product_start["modes"][1]["requires"], ["task_intent"])
    test_case.assertEqual(product_start["modes"][2]["surface_kind"], "grant_direct_entry")
    test_case.assertEqual(
        product_start["resume_surface"],
        manifest["family_orchestration"]["resume_contract"],
    )
    test_case.assertEqual(product_start["human_gate_ids"], ["mag_route_gate_revision"])
