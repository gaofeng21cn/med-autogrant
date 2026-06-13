from __future__ import annotations

import unittest

from med_autogrant.product_entry_parts import manifest_builder as manifest_builder_module
from med_autogrant.product_entry_parts.manifest_shell.shell_assembly import (
    build_manifest_shell_assembly,
)
from med_autogrant.public_cli import public_cli_command

from product_entry_cases.executor_defaults_assertions import assert_executor_defaults
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH
from product_entry_cases.test_manifest_and_status_cases.context import ManifestStatusContext


def assert_manifest_shell(
    test_case: unittest.TestCase,
    context: ManifestStatusContext,
) -> None:
    payload = context.payload
    manifest = context.manifest

    test_case.assertEqual(payload["command"], "product-entry-manifest")
    test_case.assertEqual(payload["grant_run_id"], "grant-run-nsfc-demo-001-baseline-001")
    test_case.assertEqual(payload["workspace_id"], "nsfc-demo-001")
    test_case.assertEqual(manifest["surface_kind"], "product_entry_manifest")
    test_case.assertEqual(manifest["manifest_version"], 2)
    test_case.assertEqual(manifest["manifest_kind"], "med_auto_grant_product_entry_manifest")
    test_case.assertEqual(manifest["target_domain_id"], "med-autogrant")
    test_case.assertEqual(manifest["formal_entry"]["default"], "CLI")
    test_case.assertEqual(manifest["formal_entry"]["supported_protocols"], ["MCP"])
    test_case.assertEqual(
        manifest["workspace_locator"]["workspace_root"],
        str(CRITIQUE_EXAMPLE_PATH.resolve()),
    )
    test_case.assertEqual(
        manifest["workspace_locator"]["workspace_path"],
        str(CRITIQUE_EXAMPLE_PATH.resolve()),
    )
    test_case.assertEqual(manifest["recommended_shell"], "grant_user_loop")
    test_case.assertEqual(
        manifest["recommended_command"],
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
    test_case.assertEqual(manifest["product_entry_surface"]["shell_key"], "product_status")
    test_case.assertEqual(
        manifest["product_entry_surface"]["command"],
        public_cli_command(
            "product-status", "--input", str(CRITIQUE_EXAMPLE_PATH.resolve()), "--format", "json"
        ),
    )
    test_case.assertIs(
        manifest_builder_module.build_manifest_shell_assembly,
        build_manifest_shell_assembly,
    )
    test_case.assertEqual(manifest["product_entry_surface"]["surface_kind"], "product_status")
    test_case.assertIn(
        "OPL generated/hosted status caller",
        manifest["product_entry_surface"]["summary"],
    )
    test_case.assertEqual(manifest["progress_projection"]["surface_kind"], "progress_projection")
    test_case.assertEqual(
        manifest["progress_projection"]["workspace_path"],
        str(CRITIQUE_EXAMPLE_PATH.resolve()),
    )
    test_case.assertEqual(
        manifest["progress_projection"]["projection"]["projection_kind"],
        "grant_progress",
    )
    test_case.assertEqual(manifest["artifact_inventory"]["surface_kind"], "artifact_inventory")
    test_case.assertEqual(
        manifest["artifact_inventory"]["workspace_path"],
        str(CRITIQUE_EXAMPLE_PATH.resolve()),
    )
    test_case.assertEqual(
        manifest["artifact_inventory"]["artifacts"][0]["artifact_kind"],
        "workspace_document",
    )
    test_case.assertEqual(manifest["skill_catalog"]["surface_kind"], "skill_catalog")
    test_case.assertEqual(len(manifest["skill_catalog"]["skills"]), 1)
    assert_executor_defaults(test_case, manifest["executor_defaults"])
    skill = manifest["skill_catalog"]["skills"][0]
    test_case.assertEqual(skill["skill_id"], "med-autogrant")
    test_case.assertEqual(skill["title"], "Med Auto Grant")
    test_case.assertEqual(skill["domain_projection"]["plugin_name"], "med-autogrant")
    test_case.assertEqual(skill["domain_projection"]["skill_entry"], "med-autogrant")
    test_case.assertEqual(skill["domain_projection"]["recommended_shell"], "product_status")
    test_case.assertEqual(
        skill["domain_projection"]["runtime_continuity"]["surface_kind"],
        "skill_runtime_continuity",
    )
    test_case.assertIn("validate-workspace", manifest["skill_catalog"]["supported_commands"])
    test_case.assertTrue(manifest["skill_catalog"]["command_contracts"])
    test_case.assertEqual(manifest["automation"]["surface_kind"], "automation")
    test_case.assertEqual(
        [item["automation_id"] for item in manifest["automation"]["automations"]],
        ["mag.submission_ready_export", "mag.authoring_loop_continuation"],
    )
