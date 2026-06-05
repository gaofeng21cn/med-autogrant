from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


def _source_item(
    *,
    module_id: str = "product_entry",
    path: str = "src/med_autogrant/product_entry_parts/entry.py",
    declared_role: str = "domain_handler_target",
    evidence_refs: list[str] | None = None,
    forbidden_role_flags: dict[str, bool] | None = None,
) -> dict[str, object]:
    return {
        "path": path,
        "module_id": module_id,
        "declared_role": declared_role,
        "evidence_refs": evidence_refs
        if evidence_refs is not None
        else [f"/product_entry_manifest/physical_morphology/{module_id}"],
        "forbidden_role_flags": forbidden_role_flags
        if forbidden_role_flags is not None
        else {
            "scheduler_daemon_owner": False,
            "attempt_ledger_owner": False,
            "local_journal_owner": False,
            "generic_runtime_owner": False,
            "app_workbench_owner": False,
            "compatibility_alias_owner": False,
        },
    }


class ProductEntryPhysicalMorphologyGuardTest(unittest.TestCase):
    def test_allowed_items_remain_evidence_gated_without_external_refs(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        projection = MedAutoGrantProductEntry().build_physical_morphology_guard_projection(
            source_items=[
                _source_item(),
                _source_item(
                    module_id="domain_handler",
                    path="src/med_autogrant/product_entry_parts/domain_handler.py",
                    declared_role="refs_only_adapter",
                ),
                _source_item(
                    module_id="owner_receipt",
                    path="src/med_autogrant/product_entry_parts/owner_receipt_writers.py",
                    declared_role="minimal_authority_function",
                ),
                _source_item(
                    module_id="workbench_metadata",
                    path="src/med_autogrant/product_entry_parts/progress.py",
                    declared_role="diagnostic",
                ),
                _source_item(
                    module_id="legacy_runtime_residue",
                    path="docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md",
                    declared_role="legacy_proof_tombstone",
                ),
            ],
        )

        self.assertEqual(projection["surface_kind"], "mag_physical_morphology_guard_projection")
        self.assertEqual(projection["state"], "allowed_evidence_gated")
        self.assertEqual(projection["allowed_count"], 5)
        self.assertEqual(projection["blocked_count"], 0)
        self.assertEqual(projection["blocked_items"], [])
        self.assertEqual(projection["summary"]["external_evidence_ref_count"], 0)
        self.assertIn(
            "external_evidence://physical_morphology_hygiene/active_caller_migration_receipt",
            projection["required_next_evidence_refs"],
        )
        self.assertIn(
            "external_evidence://physical_morphology_hygiene/owner_receipt_or_typed_blocker_roundtrip",
            projection["required_next_evidence_refs"],
        )
        product_entry_deletion_readiness = projection["allowed_items"][0]["deletion_readiness"]
        self.assertEqual(product_entry_deletion_readiness["surface_id"], "product_entry")
        self.assertEqual(
            product_entry_deletion_readiness["state"],
            "blocked_by_surface_evidence_or_owner_receipt",
        )
        self.assertFalse(product_entry_deletion_readiness["physical_delete_authorized"])
        self.assertEqual(
            product_entry_deletion_readiness["owner_receipt_required_ref"],
            "owner_receipt://mag/physical_delete_or_tombstone_authorization",
        )
        self.assertEqual(
            product_entry_deletion_readiness["typed_blocker_allowed_ref"],
            "typed_blocker://mag/physical_delete_or_tombstone/product_entry",
        )
        self.assertIn(
            "owner_receipt://mag/physical_delete_or_tombstone_authorization",
            product_entry_deletion_readiness["missing_retirement_evidence_refs"],
        )
        self.assertIn(
            "external_evidence://physical_morphology_hygiene/continuous_no_forbidden_write",
            product_entry_deletion_readiness["missing_retirement_evidence_refs"],
        )
        self.assertEqual(
            product_entry_deletion_readiness["next_owner_delta_required"],
            "mag_owner_physical_delete_receipt_or_domain_owned_typed_blocker_required",
        )
        self.assertTrue(product_entry_deletion_readiness["delete_or_tombstone_only_after_gate"])
        self.assertFalse(product_entry_deletion_readiness["blocked_by_surface_gate"])
        self.assertFalse(product_entry_deletion_readiness["claims_grant_ready"])
        self.assertFalse(product_entry_deletion_readiness["claims_submission_ready"])
        self.assertFalse(product_entry_deletion_readiness["claims_production_ready"])
        self.assertEqual(
            projection["retirement_gate"]["state"],
            "active_caller_migration_evidence_required",
        )
        self.assertFalse(projection["retirement_gate"]["compatibility_alias_allowed"])
        self.assertTrue(
            projection["retirement_gate"]["owner_receipt_or_typed_blocker_roundtrip_required"]
        )
        self.assertFalse(
            projection["no_resurrection_policy"]["generic_runtime_owner_allowed"]
        )
        self.assertFalse(
            projection["no_resurrection_policy"]["facade_reexport_allowed"]
        )
        self.assertFalse(
            projection["claims"]["claims_physical_morphology_cleanup_complete"]
        )
        self.assertFalse(
            projection["claims"]["claims_ready_for_owner_receipted_cleanup"]
        )
        self.assertFalse(projection["authority_boundary"]["mag_implements_opl_runtime"])
        self.assertFalse(projection["authority_boundary"]["mag_implements_app_workbench"])
        self.assertFalse(
            projection["authority_boundary"]["can_declare_physical_cleanup_complete"]
        )
        self.assertFalse(
            projection["authority_boundary"]["can_declare_ready_for_owner_receipted_cleanup"]
        )

    def test_forbidden_true_flags_fail_closed(self) -> None:
        from med_autogrant.product_entry_parts.physical_morphology_guard import (
            build_physical_morphology_guard_projection,
        )

        projection = build_physical_morphology_guard_projection(
            source_items=[
                _source_item(),
                _source_item(
                    module_id="scheduler",
                    path="src/med_autogrant/grant_autonomy_controller.py",
                    declared_role="minimal_authority_function",
                    forbidden_role_flags={
                        "scheduler_daemon_owner": True,
                        "attempt_ledger_owner": True,
                        "local_journal_owner": False,
                        "generic_runtime_owner": False,
                        "app_workbench_owner": False,
                        "compatibility_alias_owner": False,
                    },
                ),
            ],
            external_evidence_refs=[
                "opl://receipts/mag/physical-morphology/parity.json",
            ],
        )

        self.assertEqual(projection["state"], "blocked_fail_closed")
        self.assertEqual(projection["allowed_count"], 1)
        self.assertEqual(projection["blocked_count"], 1)
        self.assertEqual(projection["blocked_items"][0]["module_id"], "scheduler")
        self.assertEqual(
            projection["blocked_items"][0]["true_forbidden_flags"],
            ["scheduler_daemon_owner", "attempt_ledger_owner"],
        )
        self.assertEqual(
            projection["blocked_items"][0]["blocker_reasons"][0]["reason"],
            "forbidden_role_flag_true",
        )
        self.assertTrue(
            projection["blocked_items"][0]["deletion_readiness"]["blocked_by_surface_gate"]
        )
        self.assertFalse(
            projection["blocked_items"][0]["deletion_readiness"]["physical_delete_authorized"]
        )
        self.assertIn(
            "physical_morphology://items/scheduler/no_forbidden_role_write_proof",
            projection["blocked_items"][0]["deletion_readiness"]["missing_retirement_evidence_refs"],
        )
        self.assertFalse(
            projection["claims"]["claims_physical_morphology_cleanup_complete"]
        )
        self.assertFalse(
            projection["claims"]["claims_ready_for_owner_receipted_cleanup"]
        )

    def test_unclassified_runtime_owner_role_is_blocked(self) -> None:
        from med_autogrant.product_entry_parts.physical_morphology_guard import (
            build_physical_morphology_guard_projection,
        )

        projection = build_physical_morphology_guard_projection(
            source_items=[
                _source_item(
                    module_id="runtime_owner",
                    declared_role="generic_runtime_owner",
                    forbidden_role_flags={"generic_runtime_owner": True},
                )
            ],
        )

        self.assertEqual(projection["state"], "blocked_fail_closed")
        self.assertEqual(projection["blocked_count"], 1)
        reasons = projection["blocked_items"][0]["blocker_reasons"]
        self.assertEqual(
            [reason["reason"] for reason in reasons],
            ["declared_role_not_allowed", "forbidden_role_flag_true"],
        )
        self.assertIn(
            "physical_morphology://items/runtime_owner/role_classification_receipt",
            projection["required_next_evidence_refs"],
        )
        self.assertIn(
            "physical_morphology://items/runtime_owner/no_forbidden_role_write_proof",
            projection["required_next_evidence_refs"],
        )
        self.assertIn(
            "owner_receipt://mag/physical_delete_or_tombstone_authorization",
            projection["blocked_items"][0]["deletion_readiness"]["missing_retirement_evidence_refs"],
        )

    def test_all_allowed_with_external_evidence_refs_can_mark_ready_for_owner_receipted_cleanup(self) -> None:
        from med_autogrant.product_entry_parts.physical_morphology_guard import (
            build_physical_morphology_guard_projection,
        )

        projection = build_physical_morphology_guard_projection(
            source_items=[
                _source_item(
                    module_id="agent_pack",
                    path="agent/prompts/proposal_authoring.md",
                    declared_role="declarative_pack_surface",
                ),
                _source_item(
                    module_id="native_helper",
                    path="src/med_autogrant/final_package_validation.py",
                    declared_role="native_helper",
                ),
            ],
            external_evidence_refs=[
                "opl://receipts/mag/physical-morphology/active-caller-migration.json",
                "opl://receipts/mag/physical-morphology/direct-hosted-parity.json",
                "receipt:mag/physical-morphology/owner-receipt-roundtrip.json",
                "opl://receipts/mag/physical-morphology/no-forbidden-write.json",
            ],
        )

        self.assertEqual(projection["state"], "allowed_external_evidence_present")
        self.assertEqual(projection["blocked_items"], [])
        self.assertEqual(projection["required_next_evidence_refs"], [])
        self.assertFalse(projection["allowed_items"][0]["deletion_readiness"]["physical_delete_authorized"])
        self.assertIn(
            "owner_receipt://mag/physical_delete_or_tombstone_authorization",
            projection["allowed_items"][0]["deletion_readiness"]["missing_retirement_evidence_refs"],
        )
        self.assertEqual(
            projection["retirement_gate"]["state"],
            "eligible_for_owner_receipted_cleanup",
        )
        self.assertFalse(
            projection["claims"]["claims_physical_morphology_cleanup_complete"]
        )
        self.assertTrue(
            projection["claims"]["claims_ready_for_owner_receipted_cleanup"]
        )
        self.assertFalse(
            projection["authority_boundary"]["can_declare_physical_cleanup_complete"]
        )
        self.assertTrue(
            projection["authority_boundary"]["can_declare_ready_for_owner_receipted_cleanup"]
        )

    def test_invalid_flags_and_missing_evidence_shape_fail_closed(self) -> None:
        from med_autogrant.product_entry_parts.physical_morphology_guard import (
            build_physical_morphology_guard_projection,
        )

        with self.assertRaises(WorkspaceStateError):
            build_physical_morphology_guard_projection(
                source_items=[
                    _source_item(
                        evidence_refs=[],
                        forbidden_role_flags={"generic_runtime_owner": "false"},
                    )
                ],
            )

        with self.assertRaises(WorkspaceStateError):
            build_physical_morphology_guard_projection(
                source_items=[
                    _source_item(evidence_refs="not-a-list"),  # type: ignore[arg-type]
                ],
            )
