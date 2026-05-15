from __future__ import annotations

import tempfile
from pathlib import Path

from product_entry_cases.support import *  # noqa: F401,F403


class ProductEntryFunctionalClosureTest(unittest.TestCase):
    def test_manifest_exposes_mag_owner_receipt_contract_for_opl_ref_only_consumption(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]

        contract = manifest["owner_receipt_contract"]
        self.assertEqual(contract["surface_kind"], "mag_owner_receipt_contract")
        self.assertEqual(contract["contract_id"], "mag.owner_receipt.contract.v1")
        self.assertEqual(contract["target_domain_id"], "med-autogrant")
        self.assertEqual(contract["receipt_owner"], "med-autogrant")
        self.assertEqual(contract["maps_to_opl_contract"], "opl_domain_owner_receipt_envelope.v1")
        self.assertEqual(
            contract["allowed_return_shapes"],
            ["domain_owner_receipt", "typed_blocker", "no_regression_evidence"],
        )
        self.assertEqual(
            contract["receipt_ref_templates"]["stage_attempt_receipt_ref"],
            manifest["controlled_stage_attempt_projection"]["receipt_refs"]["stage_attempt_receipt_ref"],
        )
        self.assertFalse(contract["forbidden_write_proof"]["opl_can_write_grant_truth"])
        self.assertFalse(contract["forbidden_write_proof"]["opl_can_write_grant_artifacts"])
        self.assertFalse(contract["forbidden_write_proof"]["opl_can_hold_fundability_verdict"])
        self.assertIn(
            "/product_entry_manifest/owner_receipt_contract",
            manifest["controlled_stage_attempt_projection"]["owner_receipt_contract_ref"],
        )
        self.assertEqual(
            manifest["controlled_soak_no_regression_attempt"]["owner_receipt_contract_ref"],
            "/product_entry_manifest/owner_receipt_contract",
        )

    def test_manifest_exposes_accept_reject_domain_memory_receipt_fixtures_without_memory_body(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        proof = payload["product_entry_manifest"]["controlled_domain_memory_apply_proof"]

        fixtures = proof["controlled_receipt_instances"]
        self.assertEqual(fixtures["surface_kind"], "mag_domain_memory_controlled_receipt_instances")
        self.assertEqual(fixtures["state"], "runtime_receipt_evidence_path_verified")
        self.assertFalse(fixtures["repo_tracked_real_receipt_instance"])
        self.assertTrue(fixtures["runtime_receipt_instance_writable"])
        self.assertFalse(fixtures["contains_memory_body"])
        self.assertFalse(fixtures["contains_quality_or_export_verdict"])
        self.assertEqual(fixtures["accepted_receipt"]["decision"], "accepted")
        self.assertEqual(fixtures["rejected_receipt"]["decision"], "rejected")
        self.assertIsNotNone(fixtures["accepted_receipt"]["accepted_memory_ref"])
        self.assertIn("domain-memory/accepted-strategy-context-fixture.json", fixtures["accepted_receipt_instance_ref"])
        self.assertIsNone(fixtures["accepted_receipt"]["rejected_memory_ref"])
        self.assertIsNone(fixtures["rejected_receipt"]["accepted_memory_ref"])
        self.assertIsNotNone(fixtures["rejected_receipt"]["rejected_memory_ref"])
        self.assertIn("domain-memory/rejected-strategy-context-fixture.json", fixtures["rejected_receipt_instance_ref"])
        self.assertEqual(
            fixtures["missing_receipt_blocker"]["blocker_kind"],
            "domain_memory_owner_receipt_required",
        )
        self.assertEqual(fixtures["missing_receipt_blocker"]["owner"], "med-autogrant")
        self.assertFalse(fixtures["missing_receipt_blocker"]["opl_can_synthesize_receipt"])

    def test_manifest_exposes_lifecycle_guarded_apply_proof_for_cleanup_restore_retention(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]
        proof = manifest["lifecycle_guarded_apply_proof"]

        self.assertEqual(proof["surface_kind"], "mag_lifecycle_guarded_apply_proof")
        self.assertEqual(proof["proof_id"], "mag.lifecycle.guarded_apply.proof.v1")
        self.assertEqual(proof["target_domain_id"], "med-autogrant")
        self.assertEqual(proof["owner_receipt_contract_ref"], "/product_entry_manifest/owner_receipt_contract")
        self.assertEqual(
            [operation["operation"] for operation in proof["operations"]],
            ["cleanup", "restore", "retention"],
        )
        for operation in proof["operations"]:
            with self.subTest(operation=operation["operation"]):
                self.assertEqual(operation["opl_apply_scope"], "opl_owned_ledger_and_locator_only")
                self.assertEqual(operation["domain_mutation_policy"], "requires_mag_owner_receipt")
                self.assertEqual(operation["artifact_mutation_authority"], "med-autogrant")
                self.assertEqual(
                    operation["typed_blocker"]["blocker_kind"],
                    "mag_domain_artifact_owner_receipt_required",
                )
                self.assertFalse(operation["typed_blocker"]["opl_can_execute_domain_artifact_mutation"])
        self.assertFalse(proof["authority_boundary"]["opl_can_delete_grant_artifacts"])
        self.assertFalse(proof["authority_boundary"]["opl_can_restore_grant_artifacts"])
        self.assertFalse(proof["authority_boundary"]["opl_can_set_retention_for_grant_truth"])

    def test_owner_receipt_evidence_writer_persists_no_regression_receipt_without_domain_writes(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            payload = MedAutoGrantProductEntry().write_owner_receipt_evidence(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                receipt_shape="no_regression_evidence",
                stage_id="review_and_rebuttal",
                source_ref="opl-stage-attempt://attempt-1",
                closeout_summary="Controlled OPL-hosted attempt reused MAG refs without mutating grant truth.",
                runtime_root=tmp_dir,
                receipt_id="attempt-1",
            )
            receipt = payload["owner_receipt_evidence"]
            receipt_path = Path(receipt["receipt_instance_ref"])
            receipt_exists = receipt_path.exists()

        self.assertEqual(payload["command"], "owner-receipt-evidence")
        self.assertEqual(receipt["surface_kind"], "mag_owner_receipt_evidence")
        self.assertEqual(receipt["state"], "runtime_receipt_instance_written")
        self.assertEqual(receipt["receipt_shape"], "no_regression_evidence")
        self.assertEqual(receipt["stage_id"], "review_and_rebuttal")
        self.assertTrue(receipt_exists)
        self.assertFalse(receipt["repo_tracked"])
        self.assertFalse(receipt["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(receipt["forbidden_write_proof"]["memory_body_written"])
        self.assertFalse(receipt["forbidden_write_proof"]["submission_ready_export_verdict_written"])
        self.assertTrue(receipt["opl_consumption"]["consumes_receipt_ref_only"])
        self.assertIn(
            "/product_entry_manifest/controlled_stage_attempt_projection",
            receipt["source_refs"],
        )

    def test_lifecycle_receipt_evidence_writer_persists_guarded_apply_receipt_without_artifact_mutation(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            payload = MedAutoGrantProductEntry().write_lifecycle_receipt_evidence(
                input_path=str(CRITIQUE_EXAMPLE_PATH),
                operation="cleanup",
                receipt_shape="typed_blocker",
                source_ref="opl-lifecycle://cleanup/attempt-1",
                closeout_summary="Cleanup request requires MAG owner receipt before artifact mutation.",
                runtime_root=tmp_dir,
                receipt_id="cleanup-blocker-1",
            )
            receipt = payload["lifecycle_receipt_evidence"]
            receipt_path = Path(receipt["receipt_instance_ref"])
            receipt_exists = receipt_path.exists()

        self.assertEqual(payload["command"], "lifecycle-receipt-evidence")
        self.assertEqual(receipt["surface_kind"], "mag_lifecycle_receipt_evidence")
        self.assertEqual(receipt["state"], "runtime_receipt_instance_written")
        self.assertEqual(receipt["operation"], "cleanup")
        self.assertEqual(receipt["receipt_shape"], "typed_blocker")
        self.assertTrue(receipt_exists)
        self.assertFalse(receipt["repo_tracked"])
        self.assertEqual(receipt["artifact_mutation"], "none")
        self.assertEqual(receipt["lifecycle_mutation"], "receipt_metadata_only")
        self.assertFalse(receipt["forbidden_write_proof"]["grant_artifact_written"])
        self.assertFalse(receipt["forbidden_write_proof"]["memory_body_written"])
        self.assertTrue(receipt["opl_consumption"]["consumes_receipt_ref_only"])

    def test_manifest_exposes_physical_skeleton_follow_through_with_repo_source_anchors(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]
        follow_through = manifest["physical_skeleton_follow_through"]
        audit = manifest["controlled_domain_memory_apply_proof"]["repo_source_layout_audit"]

        self.assertEqual(follow_through["surface_kind"], "mag_physical_skeleton_follow_through")
        self.assertEqual(follow_through["state"], "minimum_repo_source_anchors_landed")
        self.assertEqual(audit["layout_state"], "physical_skeleton_follow_through_landed_minimum_anchors")
        self.assertFalse(follow_through["moves_workspace_artifacts"])
        self.assertFalse(follow_through["moves_runtime_receipt_instances"])
        self.assertEqual(follow_through["legacy_active_path_policy"], "physically_removed_or_history_tombstone_only")
        self.assertEqual(audit["retired_active_path_policy"], "physically_removed_or_history_tombstone_only")
        self.assertEqual(audit["forbidden_active_path_residue"], [])
        residue_states = {entry["path_family"]: entry["state"] for entry in audit["legacy_active_path_residue"]}
        self.assertEqual(residue_states["default Hermes active path"], "tombstone_only")
        self.assertEqual(residue_states["default Gateway active path"], "physically_removed_from_active_source")
        self.assertEqual(residue_states["default local-manager active path"], "physically_removed_from_active_source")
        for root_key, root in follow_through["roots"].items():
            with self.subTest(root=root_key):
                self.assertTrue((REPO_ROOT / root["anchor_ref"]).exists())
                self.assertEqual(root["owner"], "med-autogrant")
        for ref_status in audit["source_ref_status"]:
            with self.subTest(source_ref=ref_status["path"]):
                self.assertTrue(ref_status["exists"])
                self.assertTrue((REPO_ROOT / ref_status["path"]).exists())

    def test_manifest_exposes_ideal_state_closure_status_without_claiming_live_soak(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )
        manifest = payload["product_entry_manifest"]

        closure_status = manifest["ideal_state_closure_status"]
        self.assertEqual(closure_status["surface_kind"], "mag_ideal_state_closure_status")
        self.assertEqual(closure_status["state"], "repo_closure_landed_external_evidence_gated")
        self.assertEqual(closure_status["plan_ref"], "docs/active/mag-ideal-state-cross-repo-gap-plan.md")
        self.assertEqual(closure_status["owner"], "med-autogrant")
        self.assertFalse(closure_status["claims_production_long_run_soak_complete"])
        self.assertFalse(closure_status["authority_boundary"]["opl_can_write_domain_truth"])
        self.assertFalse(closure_status["authority_boundary"]["opl_can_write_memory_body"])
        self.assertFalse(closure_status["authority_boundary"]["opl_can_declare_export_ready"])
        phase_states = {phase["phase_id"]: phase["state"] for phase in closure_status["phases"]}
        self.assertEqual(
            phase_states,
            {
                "P0": "landed",
                "P1": "external_evidence_gate",
                "P2": "external_opl_primitive_gate",
                "P3": "runtime_workspace_evidence_gate",
                "P4": "runtime_workspace_evidence_gate",
                "P5": "landed_with_external_delete_audit_gate",
            },
        )
        p1 = next(phase for phase in closure_status["phases"] if phase["phase_id"] == "P1")
        self.assertEqual(
            p1["required_evidence_refs"],
            [
                "opl_runtime_ledger_mag_controlled_stage_attempt_ref",
                "mag_runtime_owner_receipt_instance_ref",
                "mag_no_regression_evidence_or_typed_blocker_ref",
            ],
        )
        self.assertIn(
            "/product_entry_manifest/owner_receipt_contract",
            p1["mag_surface_refs"],
        )
        p3 = next(phase for phase in closure_status["phases"] if phase["phase_id"] == "P3")
        self.assertIn(
            "mag_runtime_memory_body_migration_ref",
            p3["required_evidence_refs"],
        )
        self.assertTrue(closure_status["repo_source_exclusions"]["memory_body"])
        self.assertTrue(closure_status["repo_source_exclusions"]["runtime_receipt_instances"])
