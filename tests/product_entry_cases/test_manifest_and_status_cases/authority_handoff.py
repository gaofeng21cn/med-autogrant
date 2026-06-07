from __future__ import annotations

import unittest

from product_entry_cases.domain_memory_assertions import assert_generated_surface_handoff
from product_entry_cases.support import REPO_ROOT
from product_entry_cases.test_manifest_and_status_cases.context import ManifestStatusContext


def assert_authority_handoff(
    test_case: unittest.TestCase,
    context: ManifestStatusContext,
) -> None:
    manifest = context.manifest

    default_caller_proof = manifest["mag_consumer_thinning_contract"][
        "generated_hosted_default_caller_proof"
    ]
    test_case.assertEqual(
        default_caller_proof["target_default_caller"],
        "opl_generated_or_hosted_product_shell",
    )
    test_case.assertEqual(
        default_caller_proof["repo_local_product_shell_classification"]["product_status"],
        "domain_handler_ref_only_adapter",
    )
    test_case.assertFalse(
        default_caller_proof["authority_boundary"]["mag_claims_direct_hosted_parity_passed"]
    )
    action_catalog = manifest["family_action_catalog"]
    test_case.assertEqual(action_catalog["surface_kind"], "family_action_catalog")
    test_case.assertEqual(action_catalog["catalog_id"], "med_autogrant_action_catalog")
    test_case.assertEqual(action_catalog["target_domain_id"], "med-autogrant")
    test_case.assertEqual(action_catalog["authority_boundary"]["domain_truth_owner"], "med-autogrant")
    test_case.assertIn("MCP projection is descriptor-only", action_catalog["notes"])
    user_loop_action = next(
        action for action in action_catalog["actions"] if action["action_id"] == "open_grant_user_loop"
    )
    test_case.assertEqual(user_loop_action["source_command"]["command"], manifest["recommended_command"])
    test_case.assertFalse(user_loop_action["supported_surfaces"]["mcp"]["public_runtime"])
    test_case.assertTrue(user_loop_action["supported_surfaces"]["mcp"]["descriptor_only"])
    test_case.assertEqual(
        manifest["action_catalog_projections"]["mcp"][0]["name"],
        "open_grant_user_loop",
    )
    test_case.assertFalse(manifest["action_catalog_projections"]["mcp"][0]["public_runtime"])
    test_case.assertTrue(manifest["action_catalog_projections"]["mcp"][0]["descriptor_only"])
    test_case.assertEqual(
        manifest["operator_loop_actions"]["open_loop"]["action_catalog_ref"],
        "open_grant_user_loop",
    )
    test_case.assertEqual(
        manifest["operator_loop_actions"]["open_loop"]["command"],
        user_loop_action["source_command"]["command"],
    )
    source_provenance = manifest["source_provenance"]
    test_case.assertEqual(source_provenance["surface_kind"], "source_provenance")
    test_case.assertEqual(source_provenance["capability_classification"], "source_provenance_only")
    test_case.assertEqual(source_provenance["source_provenance_ref"]["ref"], "docs/source/README.md")
    test_case.assertEqual(
        source_provenance["historical_fixture_ref"]["ref"],
        "examples/nsfc_workspace_p2c_critique.json",
    )
    test_case.assertIn(
        "workspace-initialize-intake",
        source_provenance["explicit_archive_import_ref"]["command"],
    )
    test_case.assertEqual(
        source_provenance["parity_oracle_ref"]["ref"],
        "program:mag_declared_grant_pack_source_refs",
    )
    test_case.assertIn(
        "source_refs_do_not_contain_source_body",
        source_provenance["authority_boundary"],
    )
    test_case.assertIn(
        "no_runtime_workbench_ledger_or_scheduler_authority_transferred",
        source_provenance["authority_boundary"],
    )
    thinning = manifest["mag_consumer_thinning_contract"]
    compiler_input = thinning["declarative_grant_pack_compiler_input"]
    test_case.assertEqual(
        compiler_input["surface_kind"],
        "mag_declarative_grant_pack_compiler_input",
    )
    test_case.assertEqual(compiler_input["compiler_owner"], "one-person-lab")
    test_case.assertEqual(compiler_input["pack_owner"], "med-autogrant")
    test_case.assertEqual(
        compiler_input["input_policy"],
        "declarative_refs_and_authority_manifest_only",
    )
    test_case.assertEqual(
        compiler_input["source_refs"]["stage_graph_ref"],
        "/product_entry_manifest/family_stage_control_plane",
    )
    test_case.assertEqual(
        compiler_input["source_refs"]["action_metadata_ref"],
        "/product_entry_manifest/family_action_catalog",
    )
    test_case.assertEqual(
        compiler_input["source_refs"]["transition_oracle_ref"],
        "/product_entry_manifest/grant_transition_oracle",
    )
    test_case.assertFalse(compiler_input["authority_boundary"]["opl_can_write_grant_truth"])
    test_case.assertFalse(compiler_input["authority_boundary"]["opl_can_sign_owner_receipt"])
    test_case.assertFalse(
        compiler_input["authority_boundary"]["opl_can_declare_fundability_verdict"]
    )
    assert_generated_surface_handoff(test_case, thinning, REPO_ROOT)
    test_case.assertEqual(
        thinning["minimal_authority_function_ids"],
        [
            "fundability_verdict",
            "quality_verdict",
            "export_verdict",
            "package_authority",
            "memory_accept_reject",
            "owner_receipt_signer",
            "grant_helper",
        ],
    )
    authority_functions = {
        item["function_id"]: item for item in thinning["minimal_authority_functions"]
    }
    test_case.assertEqual(set(authority_functions), set(thinning["minimal_authority_function_ids"]))
    for authority_function in authority_functions.values():
        with test_case.subTest(authority_function=authority_function["function_id"]):
            test_case.assertEqual(authority_function["owner"], "med-autogrant")
            test_case.assertEqual(
                authority_function["retention_class"],
                "mag_minimal_authority_function",
            )
            test_case.assertFalse(authority_function["generated_by_opl"])
            test_case.assertTrue(authority_function["opl_generated_wrapper_allowed"])
            test_case.assertEqual(
                authority_function["cannot_absorb_reason"],
                authority_function["cannot_generate_reason"],
            )
            test_case.assertEqual(
                authority_function["ai_first_guard_policy"],
                "stage_artifact_or_owner_receipt_required",
            )
            test_case.assertTrue(authority_function["ai_first_guard"])
            test_case.assertEqual(
                authority_function["output_boundary"]["allowed_return_shapes"],
                authority_function["allowed_return_shapes"],
            )
            test_case.assertIn("typed_blocker", authority_function["allowed_return_shapes"])
            test_case.assertIn(
                "mechanical_ready_verdict",
                authority_function["output_boundary"]["forbidden_outputs"],
            )
