from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryDomainMemoryDescriptorTest(unittest.TestCase):
    def test_product_entry_manifest_exposes_standard_family_domain_memory_ref(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]
        descriptor = manifest["domain_memory_descriptor"]
        locator = manifest["domain_memory_descriptor_locator"]
        stage_plane = manifest["family_stage_control_plane"]

        self.assertEqual(descriptor["surface_kind"], "family_domain_memory_ref")
        self.assertEqual(descriptor["version"], "family-domain-memory-ref.v1")
        self.assertEqual(descriptor["memory_ref_id"], "mag_grant_strategy_memory")
        self.assertEqual(descriptor["target_domain_id"], "med-autogrant")
        self.assertEqual(descriptor["owner"], "Med Auto Grant")
        self.assertEqual(descriptor["memory_family"], "grant_strategy_memory")
        self.assertEqual(
            descriptor["memory_pack_ref"]["ref"],
            "docs/references/grant_strategy_memory_policy.md",
        )
        self.assertEqual(
            descriptor["stage_applicability"],
            [stage["stage_id"] for stage in stage_plane["stages"]],
        )
        self.assertEqual(
            descriptor["stage_applicability"],
            [ref["stage_id"] for ref in locator["stage_descriptor_refs"]],
        )
        self.assertEqual(
            descriptor["retrieval_contract_ref"]["ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator/memory_locator",
        )
        self.assertEqual(
            descriptor["writeback_contract_ref"]["ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator/writeback_proposal_generator",
        )
        self.assertEqual(
            descriptor["writeback_contract_ref"]["accept_reject_ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator/accept_reject_command",
        )
        self.assertEqual(
            descriptor["receipt_contract_ref"]["ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator/operator_receipt_projection",
        )
        self.assertEqual(
            descriptor["recall_projection_ref"]["ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator/stage_descriptor_refs",
        )
        self.assertEqual(
            descriptor["migration_plan_ref"]["ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator/migration_plan",
        )
        self.assertEqual(
            descriptor["seed_corpus_ref"]["ref"],
            "contracts/runtime-program/domain-memory-seed-fixture.json",
        )
        self.assertEqual(
            descriptor["writeback_receipt_locator_ref"]["ref"],
            "/product_entry_manifest/domain_memory_descriptor_locator/receipt_locator",
        )
        consumed_proof = locator["controlled_consumed_memory_proof"]
        self.assertEqual(
            consumed_proof["surface_kind"],
            "domain_memory_controlled_consumed_memory_proof",
        )
        self.assertEqual(consumed_proof["maps_to_opl_contract"], "opl_family_consumed_memory_proof.v1")
        self.assertEqual(consumed_proof["projection_policy"], "locator_and_stage_context_only_no_memory_body")
        self.assertFalse(consumed_proof["repo_tracked_real_memory_body"])
        self.assertEqual(consumed_proof["opl_role"], "consumed_memory_ref_consumer_only")
        self.assertIn("memory_body", consumed_proof["forbidden_payloads"])
        self.assertIn("fundability_verdict", consumed_proof["forbidden_payloads"])
        self.assertIn("submission_ready_export_verdict", consumed_proof["forbidden_payloads"])

        receipt_proof = locator["writeback_receipt_proof"]
        self.assertEqual(receipt_proof["surface_kind"], "domain_memory_writeback_receipt_proof")
        self.assertEqual(
            receipt_proof["maps_to_opl_contract"],
            "opl_family_memory_writeback_receipt_proof.v1",
        )
        self.assertEqual(receipt_proof["proposal_surface_kind"], "mag_domain_memory_writeback_proposal")
        self.assertEqual(receipt_proof["decision_surface_kind"], "mag_domain_memory_writeback_decision")
        self.assertEqual(
            receipt_proof["receipt_content_policy"],
            "decision_metadata_and_refs_only_no_memory_body",
        )
        self.assertTrue(receipt_proof["mag_accept_reject_required"])
        self.assertFalse(receipt_proof["receipt_instance_repo_tracked"])
        self.assertIn("memory_body", receipt_proof["forbidden_payloads"])
        self.assertIn("authoring_quality_verdict", receipt_proof["forbidden_payloads"])
        self.assertEqual(
            descriptor["freshness"]["refresh_policy"],
            "rebuild_product_entry_manifest_before_opl_discovery",
        )
        self.assertEqual(
            descriptor["migration_readiness"]["status"],
            "migration_plan_ready_descriptor_only",
        )
        self.assertEqual(
            descriptor["migration_readiness"]["memory_body_migration"],
            "domain_owned_runtime_apply_required",
        )
        self.assertFalse(descriptor["migration_readiness"]["opl_apply_allowed"])

        authority = descriptor["authority_boundary"]
        self.assertEqual(authority["opl_role"], "locator_projection_owner")
        self.assertEqual(authority["domain_memory_owner"], "med-autogrant")
        self.assertIn("memory_store_owner", authority["forbidden_opl_authority"])
        self.assertIn("fundability_verdict_owner", authority["forbidden_opl_authority"])
        self.assertIn("submission_ready_export_verdict_owner", authority["forbidden_opl_authority"])
        self.assertFalse(authority["can_write_domain_truth"])
        self.assertFalse(authority["can_authorize_quality_verdict"])
        self.assertFalse(authority["can_write_artifacts"])
        self.assertFalse(authority["can_accept_or_reject_memory_writeback"])
