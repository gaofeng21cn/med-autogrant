from __future__ import annotations

import unittest

from med_autogrant.domain_entry_contract import (
    build_domain_entry_contract,
    build_user_interaction_contract,
)
from med_autogrant.product_entry_parts.domain_agent_projection_surfaces import (
    ARTIFACT_LOCATOR_KIND,
    CONTROLLED_STAGE_ATTEMPT_KIND,
    DOMAIN_MEMORY_DESCRIPTOR_LOCATOR_KIND,
)

from product_entry_cases.domain_memory_assertions import assert_domain_memory_descriptor_locator
from product_entry_cases.test_manifest_and_status_cases.context import ManifestStatusContext


def assert_standard_agent_contract(
    test_case: unittest.TestCase,
    context: ManifestStatusContext,
) -> None:
    manifest = context.manifest

    artifact_locator = manifest["artifact_locator_contract"]
    test_case.assertEqual(artifact_locator["surface_kind"], ARTIFACT_LOCATOR_KIND)
    test_case.assertEqual(artifact_locator["locator_id"], "mag.artifact_locator.v1")
    test_case.assertFalse(artifact_locator["runtime_artifact_root"]["repo_tracked"])
    test_case.assertIn(
        "$CODEX_HOME/projects/med-autogrant/runtime-state/artifacts/",
        artifact_locator["runtime_artifact_root"]["path_template"],
    )
    test_case.assertEqual(
        artifact_locator["runtime_artifact_root"]["write_policy"],
        "mag_runtime_or_export_surface_only",
    )
    test_case.assertEqual(
        artifact_locator["artifact_inventory_ref"],
        "/product_entry_manifest/artifact_inventory",
    )
    test_case.assertFalse(artifact_locator["opl_consumption"]["can_issue_fundability_verdict"])
    test_case.assertFalse(artifact_locator["opl_consumption"]["can_issue_export_verdict"])
    test_case.assertTrue(
        artifact_locator["opl_consumption"]["requires_mag_receipt_for_domain_artifact_mutation"]
    )
    controlled_attempt = manifest["controlled_stage_attempt_projection"]
    test_case.assertEqual(controlled_attempt["surface_kind"], CONTROLLED_STAGE_ATTEMPT_KIND)
    test_case.assertEqual(
        controlled_attempt["maps_to_opl_contract"],
        "opl_family_runtime_attempt_contract.v1",
    )
    test_case.assertEqual(controlled_attempt["attempt_owner"], "med-autogrant")
    test_case.assertEqual(controlled_attempt["attempt_state"], manifest["task_lifecycle"]["status"])
    test_case.assertEqual(controlled_attempt["last_observed_projection"], manifest["progress_projection"])
    test_case.assertIn(
        "$CODEX_HOME/projects/med-autogrant/runtime-state/receipts/",
        controlled_attempt["receipt_refs"]["domain_handler_dispatch_receipt_ref"],
    )
    test_case.assertFalse(
        controlled_attempt["opl_consumption_contract"]["can_hold_fundability_verdict"]
    )
    test_case.assertFalse(controlled_attempt["opl_consumption_contract"]["can_hold_export_verdict"])
    test_case.assertIn(
        "canonical_grant_artifact_content",
        controlled_attempt["opl_consumption_contract"]["does_not_consume"],
    )
    proof = controlled_attempt["proof"]
    test_case.assertEqual(proof["surface_kind"], "controlled_stage_attempt_fixture_proof")
    test_case.assertTrue(proof["direct_skill_and_opl_hosted_use_same_descriptor_domain_handler_quality_refs"])
    test_case.assertFalse(proof["opl_verdict_authority"]["fundability"])
    test_case.assertFalse(proof["opl_verdict_authority"]["submission_ready_export"])
    stage_plane = manifest["family_stage_control_plane"]
    memory_locator = manifest["domain_memory_descriptor_locator"]
    test_case.assertEqual(memory_locator["surface_kind"], DOMAIN_MEMORY_DESCRIPTOR_LOCATOR_KIND)
    assert_domain_memory_descriptor_locator(test_case, memory_locator, stage_plane)
    skeleton = manifest["standard_domain_agent_skeleton"]
    test_case.assertEqual(skeleton["surface_kind"], "standard_domain_agent_skeleton")
    test_case.assertEqual(skeleton["skeleton_id"], "mag.standard_domain_agent_skeleton.v1")
    test_case.assertEqual(skeleton["canonical_semantic_pack_root"], "agent/")
    test_case.assertEqual(
        skeleton["canonical_semantic_pack_role"],
        "repo_source_declarative_grant_pack",
    )
    test_case.assertEqual(set(skeleton["repo_source_boundary"]), {"agent", "contracts", "runtime", "docs"})
    test_case.assertNotIn("agent/README.md", skeleton["repo_source_boundary"]["agent"]["source_refs"])
    test_case.assertIn(
        "agent/README.md",
        skeleton["repo_source_boundary"]["agent"]["human_readable_provenance_refs"],
    )
    test_case.assertEqual(
        skeleton["runtime_declaration"]["runtime_only_declares"],
        ["domain_handler", "projection_builder", "lifecycle_adapter"],
    )
    test_case.assertEqual(
        skeleton["artifact_locator_ref"],
        "/product_entry_manifest/artifact_locator_contract",
    )
    test_case.assertEqual(
        skeleton["controlled_stage_attempt_ref"],
        "/product_entry_manifest/controlled_stage_attempt_projection",
    )
    test_case.assertEqual(
        skeleton["domain_memory_descriptor_locator_ref"],
        "/product_entry_manifest/domain_memory_descriptor_locator",
    )
    test_case.assertEqual(skeleton["domain_memory_descriptor_locator"], memory_locator)
    test_case.assertFalse(skeleton["authority_boundary"]["can_hold_fundability_verdict"])
    test_case.assertFalse(skeleton["authority_boundary"]["can_hold_export_verdict"])
    test_case.assertFalse(skeleton["authority_boundary"]["can_write_grant_artifacts"])
    skill = manifest["skill_catalog"]["skills"][0]
    test_case.assertEqual(
        skill["domain_projection"]["action_catalog_ref"],
        "/product_entry_manifest/family_action_catalog",
    )
    test_case.assertEqual(skill["domain_projection"]["standard_domain_agent_skeleton"], skeleton)
    test_case.assertEqual(
        skill["domain_projection"]["mcp_descriptor"],
        manifest["action_catalog_projections"]["mcp"][0],
    )
    test_case.assertEqual(manifest["domain_entry_contract"], build_domain_entry_contract())
    test_case.assertEqual(
        manifest["domain_entry_contract"]["domain_agent_entry_spec"],
        {
            "surface_kind": "domain_agent_entry_spec",
            "agent_id": "mag",
            "title": "Med Auto Grant Domain Agent",
            "description": "Grant authoring domain truth owner surface for Med Auto Grant.",
            "default_engine": "codex",
            "workspace_requirement": "required",
            "locator_schema": {
                "required_fields": ["input_path"],
                "optional_fields": ["workspace_id", "grant_run_id", "draft_id"],
                "workspace_field": "input_path",
                "workspace_kind": "nsfc_workspace",
                "workspace_id_field": "workspace_id",
                "run_id_field": "grant_run_id",
                "draft_id_field": "draft_id",
            },
            "codex_entry_strategy": "domain_agent_entry",
            "artifact_conventions": "grant_proposal_package",
            "progress_conventions": "grant_workloop_narration",
            "entry_command": "product-status",
            "manifest_command": "product-entry-manifest",
        },
    )
    test_case.assertEqual(
        manifest["user_interaction_contract"],
        build_user_interaction_contract(),
    )
