from __future__ import annotations

import unittest
from typing import Any, Mapping

from product_entry_cases.support import assert_contains_all, assert_false_keys


def assert_family_stage_control_plane_preserves_opl_projection_and_mag_authority(
    test_case: unittest.TestCase,
    action_catalog: Mapping[str, Any],
    stage_plane: Mapping[str, Any],
) -> None:
    _assert_plane_identity(test_case, stage_plane)

    action_ids = {action["action_id"] for action in action_catalog["actions"]}
    expected_order = [
        "call_and_candidate_intake",
        "fundability_strategy",
        "specific_aims_and_structure",
        "proposal_authoring",
        "review_and_rebuttal",
        "package_and_submit_ready",
    ]
    test_case.assertEqual([stage["stage_id"] for stage in stage_plane["stages"]], expected_order)
    test_case.assertEqual(
        [
            stage["stage_id"]
            for stage in stage_plane["stages"]
            if stage["selected_executor"]["default_executor"] is True
        ],
        ["call_and_candidate_intake"],
    )

    required_fields = set(stage_plane["discovery_smoke"]["required_stage_fields"])
    for stage in stage_plane["stages"]:
        with test_case.subTest(stage=stage["stage_id"]):
            _assert_stage_projection_shape(test_case, stage, action_ids, required_fields)
            _assert_stage_authority_boundary(test_case, stage)
            _assert_stage_artifact_and_closeout_contract(test_case, stage)

    proposal_stage = next(stage for stage in stage_plane["stages"] if stage["stage_id"] == "proposal_authoring")
    test_case.assertEqual(proposal_stage["stage_kind"], "creation")
    test_case.assertEqual(
        proposal_stage["authority_boundary"]["submission_ready_export_gate_owner"],
        "med-autogrant",
    )


def _assert_plane_identity(test_case: unittest.TestCase, stage_plane: Mapping[str, Any]) -> None:
    test_case.assertEqual(stage_plane["surface_kind"], "family_stage_control_plane")
    test_case.assertEqual(stage_plane["version"], "family-stage-control-plane.v1")
    test_case.assertEqual(stage_plane["plane_id"], "med_autogrant_stage_control_plane")
    test_case.assertEqual(stage_plane["target_domain_id"], "med-autogrant")
    test_case.assertEqual(stage_plane["authority_boundary"]["opl_role"], "projection_consumer_only")
    assert_false_keys(
        test_case,
        stage_plane["authority_boundary"],
        ("can_write_grant_truth", "can_override_fundability_judgment", "can_bypass_submission_ready_gate"),
    )
    test_case.assertEqual(stage_plane["discovery_smoke"]["status"], "ready")
    test_case.assertEqual(stage_plane["parity"]["status"], "aligned")


def _assert_stage_projection_shape(
    test_case: unittest.TestCase,
    stage: Mapping[str, Any],
    action_ids: set[str],
    required_fields: set[str],
) -> None:
    for required_field in required_fields:
        _assert_required_field_path(test_case, stage, required_field)
    test_case.assertEqual(stage["owner"], "med-autogrant")
    test_case.assertEqual(stage["stage_goal"], stage["goal"])
    test_case.assertEqual(stage["selected_executor"]["executor_kind"], "codex_cli")
    test_case.assertEqual(stage["selected_executor"]["executor_binding_ref"], "default_codex_cli")
    test_case.assertTrue(set(stage["allowed_action_refs"]) <= action_ids)
    test_case.assertTrue(stage["stage_contract"]["requires"])
    test_case.assertTrue(stage["stage_contract"]["ensures"])
    test_case.assertTrue(any(ref["role"] == "owner_receipt_gate" for ref in stage["evaluation"]))
    test_case.assertTrue(stage["trust_boundary"]["owner_receipt_required"])
    test_case.assertTrue(stage["trust_boundary"]["runtime_guard_required"])


def _assert_stage_authority_boundary(test_case: unittest.TestCase, stage: Mapping[str, Any]) -> None:
    independent_gate_stage_ids = {
        "fundability_strategy",
        "specific_aims_and_structure",
        "review_and_rebuttal",
        "package_and_submit_ready",
    }
    test_case.assertEqual(
        stage["authority_boundary"]["independent_gate_receipt_required"],
        stage["stage_id"] in independent_gate_stage_ids,
    )
    assert_false_keys(
        test_case,
        stage["authority_boundary"],
        ("can_write_grant_truth", "can_override_fundability_judgment", "can_bypass_submission_ready_gate"),
    )


def _assert_stage_artifact_and_closeout_contract(
    test_case: unittest.TestCase,
    stage: Mapping[str, Any],
) -> None:
    contract = stage["stage_contract"]
    native = contract["stage_native_artifact_contract"]
    test_case.assertEqual(native["surface_kind"], "mag_stage_native_artifact_contract")
    test_case.assertEqual(native["owner"], "med-autogrant")
    test_case.assertEqual(native["stage_id"], stage["stage_id"])
    test_case.assertTrue(native["manifest_requirements"]["body_free_projection_required"])
    test_case.assertTrue(native["stage_folder_lifecycle_contract"]["artifact_bundle_manifest_required"])
    test_case.assertTrue(native["stage_folder_lifecycle_contract"]["artifact_bundle_owner_receipt_or_typed_blocker_required"])
    test_case.assertFalse(native["stage_folder_lifecycle_contract"]["opl_can_interpret_grant_quality"])

    physical_kernel = native["physical_stage_folder_kernel"]
    test_case.assertEqual(physical_kernel["maps_to_opl_contract"], "opl_stage_artifact_runtime_contract.v1")
    assert_contains_all(
        test_case,
        physical_kernel["required_attempt_entries"],
        ("stage.json", "attempt.json", "manifest.json", "receipts/receipt.json"),
    )
    assert_false_keys(
        test_case,
        physical_kernel["authority_boundary"],
        ("opl_can_promote_canonical_pointer", "opl_can_create_mag_owner_receipt", "opl_can_interpret_grant_quality"),
    )

    verdict_policy = native["owner_verdict_signature_policy"]
    test_case.assertEqual(verdict_policy["owner"], "med-autogrant")
    assert_contains_all(
        test_case,
        verdict_policy["required_verdicts"],
        ("fundability_verdict", "authoring_quality_verdict", "export_verdict", "submission_ready_verdict"),
    )
    test_case.assertFalse(verdict_policy["opl_can_sign_or_infer_verdict"])

    closeout = stage["stage_production_evidence_closeout"]
    test_case.assertEqual(closeout["surface_kind"], "mag_stage_production_evidence_closeout_refs")
    test_case.assertEqual(closeout["stage_id"], stage["stage_id"])
    audit = closeout["grant_ready_completion_audit"]
    test_case.assertEqual(audit["state"], "blocked_without_mag_owner_closing_ref")
    assert_false_keys(
        test_case,
        audit["claim_permissions"],
        ("grant_ready", "quality_ready", "export_ready", "submission_ready"),
    )
    assert_contains_all(
        test_case,
        audit["false_completion_signals"],
        ("provider_completion", "schema_completeness", "generated_surface_ready", "focused_tests_passed"),
    )
    assert_false_keys(
        test_case,
        closeout["authority_boundary"],
        (
            "opl_can_sign_owner_receipt",
            "opl_can_write_grant_truth",
            "opl_can_declare_export_ready",
            "provider_completion_counts_as_grant_ready",
            "schema_completeness_counts_as_grant_ready",
            "generated_surface_ready_counts_as_grant_ready",
            "focused_tests_count_as_grant_ready",
        ),
    )

    classification = native["artifact_classification_boundary"]
    test_case.assertEqual(classification["artifact_body_owner"], "med-autogrant")
    assert_false_keys(
        test_case,
        classification,
        (
            "opl_can_read_artifact_body",
            "opl_can_write_artifact_body",
            "opl_can_declare_fundability_ready",
            "opl_can_declare_quality_ready",
            "opl_can_declare_export_ready",
            "opl_can_declare_submission_ready",
        ),
    )


def _assert_required_field_path(
    test_case: unittest.TestCase,
    payload: Mapping[str, Any],
    path: str,
) -> None:
    current: Any = payload
    for part in path.split("."):
        test_case.assertIsInstance(current, dict, path)
        test_case.assertIn(part, current, path)
        current = current[part]
