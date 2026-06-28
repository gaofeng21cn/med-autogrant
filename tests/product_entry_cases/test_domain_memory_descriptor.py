from __future__ import annotations

import unittest
from product_entry_cases.support import (
    CRITIQUE_EXAMPLE_PATH,
    REPO_ROOT,
)


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

    def test_manifest_exposes_controlled_grant_stage_domain_memory_apply_proof(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]
        proof = manifest["controlled_domain_memory_apply_proof"]

        self.assertEqual(proof["surface_kind"], "controlled_grant_stage_domain_memory_apply_proof")
        self.assertEqual(proof["proof_id"], "mag.domain_memory.controlled_grant_stage_apply.proof.v1")
        self.assertEqual(proof["target_domain_id"], "med-autogrant")
        self.assertEqual(proof["proof_state"], "repo_source_audit_landed_no_runtime_artifact_write")
        self.assertEqual(
            proof["consumed_grant_strategy_memory_refs"],
            [
                {
                    "stage_id": stage["stage_id"],
                    "stage_descriptor_ref": f"/product_entry_manifest/family_stage_control_plane/stages/{index}",
                    "accepted_memory_ref_template": (
                        "$CODEX_HOME/projects/med-autogrant/runtime-state/domain-memory/"
                        "accepted/<memory_id>.json"
                    ),
                    "consumption_policy": "stage_context_ref_only_no_memory_body_in_repo",
                }
                for index, stage in enumerate(manifest["family_stage_control_plane"]["stages"])
            ],
        )
        self.assertEqual(
            proof["writeback_proposal_projection"]["surface_kind"],
            "domain_memory_writeback_proposal_generator",
        )
        self.assertEqual(
            proof["writeback_proposal_projection"]["proposal_ref_template"],
            manifest["domain_memory_descriptor_locator"]["memory_locator"]["writeback_proposal_ref_template"],
        )
        self.assertEqual(
            proof["accept_reject_decision_projection"]["surface_kind"],
            "domain_memory_accept_reject_command",
        )
        self.assertTrue(proof["accept_reject_decision_projection"]["requires_mag_decision_before_store_mutation"])
        self.assertEqual(
            proof["runtime_receipt_evidence_projection"]["surface_kind"],
            "domain_memory_runtime_receipt_evidence_projection",
        )
        self.assertEqual(
            proof["runtime_receipt_evidence_projection"]["output_surface_kind"],
            "mag_domain_memory_runtime_receipt_evidence",
        )
        self.assertEqual(
            proof["runtime_receipt_evidence_projection"]["write_policy"],
            "runtime_receipt_instance_only_no_repo_write",
        )
        self.assertEqual(
            proof["operator_receipt_projection"],
            manifest["domain_memory_descriptor_locator"]["operator_receipt_projection"],
        )
        self.assertFalse(proof["authority_boundary"]["can_write_fundability_verdict"])
        self.assertFalse(proof["authority_boundary"]["can_write_authoring_quality_verdict"])
        self.assertFalse(proof["authority_boundary"]["can_write_submission_ready_export_verdict"])
        self.assertFalse(proof["authority_boundary"]["can_write_grant_artifact"])
        self.assertFalse(proof["repo_payload_policy"]["repo_tracked_real_memory_body"])
        self.assertFalse(proof["repo_payload_policy"]["repo_tracked_real_receipt_instance"])
        self.assertFalse(proof["repo_payload_policy"]["repo_tracked_real_grant_artifact"])

        layout_audit = proof["repo_source_layout_audit"]
        self.assertEqual(layout_audit["surface_kind"], "mag_repo_source_layout_audit")
        self.assertEqual(layout_audit["layout_state"], "declarative_grant_pack_follow_through_landed")
        self.assertEqual(layout_audit["boundary_keys"], ["agent", "contracts", "runtime", "docs"])
        self.assertEqual(
            layout_audit["active_path_current_role_policy"],
            "current_role_guard_and_history_index_only",
        )
        self.assertEqual(layout_audit["forbidden_active_path_residue"], [])
        closed_history = layout_audit["closed_default_path_history_summary"]
        self.assertEqual(closed_history["state"], "closed_history_index_only")
        self.assertEqual(closed_history["closed_path_family_count"], 3)
        self.assertEqual(closed_history["active_source_residue_count"], 0)
        self.assertFalse(closed_history["stores_closed_path_names"])
        for ref_status in layout_audit["source_ref_status"]:
            with self.subTest(source_ref=ref_status["path"]):
                self.assertTrue(ref_status["exists"])
                self.assertTrue((REPO_ROOT / ref_status["path"]).exists())
