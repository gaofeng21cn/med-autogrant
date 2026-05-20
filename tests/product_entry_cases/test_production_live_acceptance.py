from __future__ import annotations

import tempfile

from product_entry_cases.support import *  # noqa: F401,F403


def _agent_lab_suite_result() -> dict[str, object]:
    return {
        "surface_kind": "opl_agent_lab_suite_result",
        "suite_id": "target-agent-handoff:med-autogrant:production-live-acceptance-owner-receipt-scaleout",
        "suite_kind": "agent_production_evidence_suite",
        "result_id": "oals_mag_live_acceptance",
        "status": "passed",
        "summary": {
            "forbidden_authority_flag_count": 0,
            "owner_or_human_gate_required_count": 1,
            "promotable_candidate_count": 0,
        },
        "domain_summary": [{"domain_id": "med-autogrant"}],
        "authority_boundary": {
            "can_write_domain_truth": False,
            "can_write_memory_body": False,
            "can_authorize_quality_verdict": False,
            "can_write_owner_receipt": False,
        },
        "refs": {
            "receipt_refs": [
                "receipt:mag/production-live-acceptance/2026-05-20",
                "receipt-projection:mag/production-live-acceptance-owner-receipt",
            ],
            "artifact_refs": [
                "contract-ref:mag/contracts/production_acceptance/mag-production-acceptance.json",
            ],
        },
    }


def _meta_agent_coordination_result() -> dict[str, object]:
    return {
        "surface_kind": "opl_meta_agent_external_suite_self_evolution_result",
        "status": "passed",
        "target_agent": {"domain_id": "med-autogrant"},
        "authority_boundary": {
            "can_write_target_domain_truth": False,
            "can_write_target_domain_memory_body": False,
            "can_mutate_target_domain_artifact_body": False,
            "can_authorize_target_domain_quality_or_export": False,
        },
        "learning_loop": {
            "developer_patch_work_order": {
                "status": "no_patch_required",
                "source_agent_lab_result_ref": "oals_mag_live_acceptance",
            },
        },
    }


class ProductEntryProductionLiveAcceptanceTest(unittest.TestCase):
    def test_manifest_exposes_mag_live_acceptance_receipt_surface(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        surface = payload["product_entry_manifest"]["production_live_acceptance_receipt"]
        self.assertEqual(surface["surface_kind"], "mag_production_live_acceptance_receipt_surface")
        self.assertEqual(surface["accepted_owner_receipt_shape"], "domain_owner_receipt")
        self.assertIn("production-live-acceptance-receipt", surface["command"])
        self.assertTrue(surface["authority_boundary"]["opl_agent_lab_ref_consumer_only"])
        self.assertTrue(surface["authority_boundary"]["meta_agent_work_order_consumer_only"])
        self.assertFalse(surface["authority_boundary"]["can_declare_fundability_ready"])
        self.assertFalse(surface["authority_boundary"]["can_declare_submission_ready_export"])

    def test_live_acceptance_receipt_projection_closes_domain_owner_blocker_refs_only(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="domain_owner_receipt",
                stage_id="package_and_submit_ready",
                source_ref="opl-agent-lab://mag/live-acceptance-owner-receipt",
                closeout_summary="MAG owner accepted live production acceptance receipt scaleout refs.",
                runtime_root=runtime_root,
                receipt_id="production-live-acceptance-2026-05-20",
                closeout_refs={
                    "agent_lab_suite_result_ref": "suite-result:mag/live-acceptance",
                    "meta_agent_coordination_ref": "meta-agent:mag/live-acceptance",
                },
            )["owner_receipt_evidence"]
            payload = entry.build_production_live_acceptance_receipt_projection(
                owner_receipt_evidence=receipt,
                agent_lab_suite_result=_agent_lab_suite_result(),
                meta_agent_coordination_result=_meta_agent_coordination_result(),
            )

        projection = payload["production_live_acceptance_receipt"]
        self.assertEqual(
            projection["surface_kind"],
            "mag_production_live_acceptance_receipt_projection",
        )
        self.assertEqual(
            projection["state"],
            "closed_by_mag_domain_owner_live_acceptance_receipt",
        )
        self.assertEqual(projection["receipt"]["receipt_shape"], "domain_owner_receipt")
        self.assertEqual(projection["agent_lab_coordination"]["status"], "passed")
        self.assertFalse(projection["agent_lab_coordination"]["agent_lab_can_issue_mag_owner_receipt"])
        self.assertEqual(projection["meta_agent_coordination"]["status"], "passed")
        self.assertEqual(
            projection["meta_agent_coordination"]["developer_work_order_status"],
            "no_patch_required",
        )
        self.assertFalse(projection["meta_agent_coordination"]["meta_agent_can_write_mag_truth"])
        self.assertEqual(
            projection["production_acceptance"]["accepted_return_shape"],
            "domain_owner_receipt_ref",
        )
        self.assertEqual(
            projection["production_acceptance"]["closed_typed_blocker_kind"],
            "domain_owner_live_acceptance_receipt_scaleout_required",
        )
        self.assertFalse(projection["authority_boundary"]["agent_lab_pass_equals_fundability_ready"])
        self.assertFalse(projection["authority_boundary"]["meta_agent_pass_equals_fundability_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_submission_ready_export"])
        self.assertFalse(projection["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(projection["forbidden_write_proof"]["fundability_verdict_written"])

    def test_live_acceptance_receipt_projection_rejects_typed_blocker_closeout(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.workspace_types import WorkspaceStateError

        with tempfile.TemporaryDirectory() as tmp_dir:
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="typed_blocker",
                stage_id="package_and_submit_ready",
                source_ref="opl-agent-lab://mag/live-acceptance-blocked",
                closeout_summary="MAG owner still blocked.",
                runtime_root=Path(tmp_dir) / "runtime-state",
                receipt_id="production-live-acceptance-blocked",
            )["owner_receipt_evidence"]
            with self.assertRaises(WorkspaceStateError):
                entry.build_production_live_acceptance_receipt_projection(
                    owner_receipt_evidence=receipt,
                    agent_lab_suite_result=_agent_lab_suite_result(),
                    meta_agent_coordination_result=_meta_agent_coordination_result(),
                )

    def test_live_acceptance_receipt_projection_rejects_non_mag_owner_receipt(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.workspace_types import WorkspaceStateError

        with tempfile.TemporaryDirectory() as tmp_dir:
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="domain_owner_receipt",
                stage_id="package_and_submit_ready",
                source_ref="opl-agent-lab://mag/live-acceptance-owner-receipt",
                closeout_summary="MAG owner accepted live production acceptance receipt scaleout refs.",
                runtime_root=Path(tmp_dir) / "runtime-state",
                receipt_id="production-live-acceptance-non-mag-owner",
            )["owner_receipt_evidence"]
            receipt = deepcopy(receipt)
            receipt["owner"] = "other-agent"
            receipt["target_domain_id"] = "other-agent"

            with self.assertRaises(WorkspaceStateError):
                entry.build_production_live_acceptance_receipt_projection(
                    owner_receipt_evidence=receipt,
                    agent_lab_suite_result=_agent_lab_suite_result(),
                    meta_agent_coordination_result=_meta_agent_coordination_result(),
                )

    def test_live_acceptance_receipt_projection_binds_meta_agent_to_same_agent_lab_result(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.workspace_types import WorkspaceStateError

        with tempfile.TemporaryDirectory() as tmp_dir:
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="domain_owner_receipt",
                stage_id="package_and_submit_ready",
                source_ref="opl-agent-lab://mag/live-acceptance-owner-receipt",
                closeout_summary="MAG owner accepted live production acceptance receipt scaleout refs.",
                runtime_root=Path(tmp_dir) / "runtime-state",
                receipt_id="production-live-acceptance-meta-mismatch",
            )["owner_receipt_evidence"]
            meta_result = deepcopy(_meta_agent_coordination_result())
            meta_result["learning_loop"]["developer_patch_work_order"][
                "source_agent_lab_result_ref"
            ] = "different-result-id"

            with self.assertRaises(WorkspaceStateError):
                entry.build_production_live_acceptance_receipt_projection(
                    owner_receipt_evidence=receipt,
                    agent_lab_suite_result=_agent_lab_suite_result(),
                    meta_agent_coordination_result=meta_result,
                )

    def test_live_acceptance_receipt_projection_requires_complete_agent_lab_summary(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.workspace_types import WorkspaceStateError

        with tempfile.TemporaryDirectory() as tmp_dir:
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="domain_owner_receipt",
                stage_id="package_and_submit_ready",
                source_ref="opl-agent-lab://mag/live-acceptance-owner-receipt",
                closeout_summary="MAG owner accepted live production acceptance receipt scaleout refs.",
                runtime_root=Path(tmp_dir) / "runtime-state",
                receipt_id="production-live-acceptance-incomplete-agent-lab",
            )["owner_receipt_evidence"]
            suite_result = deepcopy(_agent_lab_suite_result())
            suite_result["summary"].pop("forbidden_authority_flag_count")

            with self.assertRaises(WorkspaceStateError):
                entry.build_production_live_acceptance_receipt_projection(
                    owner_receipt_evidence=receipt,
                    agent_lab_suite_result=suite_result,
                    meta_agent_coordination_result=_meta_agent_coordination_result(),
                )

    def test_live_acceptance_receipt_projection_rejects_mag_specific_agent_lab_wrapper(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry
        from med_autogrant.workspace_types import WorkspaceStateError

        with tempfile.TemporaryDirectory() as tmp_dir:
            entry = MedAutoGrantProductEntry()
            receipt = entry.write_owner_receipt_evidence(
                input_path=CRITIQUE_EXAMPLE_PATH,
                receipt_shape="domain_owner_receipt",
                stage_id="package_and_submit_ready",
                source_ref="opl-agent-lab://standard/live-acceptance-owner-receipt",
                closeout_summary="MAG owner accepted standard Agent Lab result refs.",
                runtime_root=Path(tmp_dir) / "runtime-state",
                receipt_id="production-live-acceptance-mag-wrapper",
            )["owner_receipt_evidence"]
            suite_result = deepcopy(_agent_lab_suite_result())

            with self.assertRaises(WorkspaceStateError):
                entry.build_production_live_acceptance_receipt_projection(
                    owner_receipt_evidence=receipt,
                    agent_lab_suite_result={
                        "agent_lab_mag_live_acceptance": {
                            "suite_result": suite_result,
                        },
                    },
                    meta_agent_coordination_result=_meta_agent_coordination_result(),
                )

            suite_result["suite_kind"] = "agent_lab_mag_live_acceptance_suite"
            with self.assertRaises(WorkspaceStateError):
                entry.build_production_live_acceptance_receipt_projection(
                    owner_receipt_evidence=receipt,
                    agent_lab_suite_result=suite_result,
                    meta_agent_coordination_result=_meta_agent_coordination_result(),
                )
