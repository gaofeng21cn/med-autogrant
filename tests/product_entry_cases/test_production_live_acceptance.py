from __future__ import annotations

import tempfile

from copy import deepcopy
import unittest
from pathlib import Path

from med_autogrant.product_entry import MedAutoGrantProductEntry
from med_autogrant.product_entry_parts.owner_receipt_common import (
    PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_PROJECTION_KIND,
)
from med_autogrant.product_entry_parts.manifest_owner_receipt_surfaces import (
    build_production_live_acceptance_receipt_surface,
)
from med_autogrant.product_entry_parts.production_live_acceptance import (
    build_production_live_acceptance_receipt_projection,
)
from med_autogrant.product_entry_parts.owner_receipt_writers import (
    write_owner_receipt_evidence,
)
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import CRITIQUE_EXAMPLE_PATH


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


def _meta_agent_patch_work_order_result() -> dict[str, object]:
    result = deepcopy(_meta_agent_coordination_result())
    result["learning_loop"]["developer_patch_work_order"] = {
        "status": "patch_smoke_closed",
        "source_agent_lab_result_ref": "oals_mag_live_acceptance",
        "blocked_suite_result_ref": "agent-lab-suite-result:oma/mag/blocked-suite",
        "developer_patch_work_order_ref": "developer-work-order:oma/mag/ai-first-mag-patch-smoke",
        "patch_traceability_matrix_ref": "patch-traceability:oma/mag/ai-first-mag-patch-smoke",
        "target_repo_verification_refs": [
            "rtk ./scripts/run-pytest-clean.sh tests/product_entry_cases/test_production_live_acceptance.py tests/test_production_acceptance.py -q",
            "rtk ./scripts/verify.sh",
            "rtk git diff --check",
        ],
        "target_runtime_read_model_consumption_ref": (
            "/product_entry_manifest/production_live_acceptance_receipt"
        ),
        "workspace_environment_proof_ref": (
            "workspace-proof:med-autogrant/.worktrees/ai-first-mag-patch-smoke"
        ),
        "no_forbidden_write_proof_ref": (
            "contracts/agent_lab_handoff.json#/authority_boundary/oma_consumes_mag_refs_only"
        ),
        "target_owner_receipt_or_typed_blocker_ref": "typed-blocker:mag/ai-first-mag-patch-smoke",
        "patch_absorption_ref": "git-commit:pending/codex/ai-first-mag-patch-smoke",
        "worktree_cleanup_ref": "worktree-cleanup:pending/ai-first-mag-patch-smoke",
        "agent_lab_re_evaluation_ref": "agent-lab-run:oma/mag/ai-first-mag-patch-smoke/re-evaluation",
    }
    return result


def _owner_receipt(
    runtime_root: Path,
    *,
    receipt_shape: str,
    source_ref: str,
    receipt_id: str,
    closeout_summary: str,
    closeout_refs: dict[str, object] | None = None,
) -> dict[str, object]:
    return write_owner_receipt_evidence(
        input_path=CRITIQUE_EXAMPLE_PATH,
        receipt_shape=receipt_shape,
        stage_id="package_and_submit_ready",
        source_ref=source_ref,
        closeout_summary=closeout_summary,
        runtime_root=runtime_root,
        receipt_id=receipt_id,
        closeout_refs=closeout_refs,
    )["owner_receipt_evidence"]


class ProductEntryProductionLiveAcceptanceTest(unittest.TestCase):
    def test_manifest_exposes_mag_live_acceptance_receipt_surface(self) -> None:
        payload = MedAutoGrantProductEntry().build_product_entry_manifest(
            input_path=str(CRITIQUE_EXAMPLE_PATH),
        )

        surface = payload["product_entry_manifest"]["production_live_acceptance_receipt"]
        self.assertEqual(surface, build_production_live_acceptance_receipt_surface())
        self.assertEqual(surface["surface_kind"], "mag_production_live_acceptance_receipt_surface")
        self.assertEqual(surface["accepted_owner_receipt_shape"], "domain_owner_receipt")
        self.assertEqual(
            surface["accepted_closeout_shapes"],
            ["domain_owner_receipt", "typed_blocker"],
        )
        self.assertIn("authority production-acceptance", surface["command"])
        self.assertEqual(
            set(surface["required_patch_loop_refs"]),
            {
                "blocked_suite_result_ref",
                "developer_patch_work_order_ref",
                "patch_traceability_matrix_ref",
                "target_repo_verification_refs",
                "target_runtime_read_model_consumption_ref",
                "workspace_environment_proof_ref",
                "no_forbidden_write_proof_ref",
                "target_owner_receipt_or_typed_blocker_ref",
                "patch_absorption_ref",
                "worktree_cleanup_ref",
                "agent_lab_re_evaluation_ref",
            },
        )
        self.assertTrue(surface["authority_boundary"]["opl_agent_lab_ref_consumer_only"])
        self.assertTrue(surface["authority_boundary"]["meta_agent_work_order_consumer_only"])
        self.assertFalse(surface["authority_boundary"]["can_declare_fundability_ready"])
        self.assertFalse(surface["authority_boundary"]["can_declare_submission_ready_export"])

    def test_live_acceptance_receipt_projection_closes_domain_owner_blocker_refs_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            runtime_root = Path(tmp_dir) / "runtime-state"
            receipt = _owner_receipt(
                runtime_root,
                receipt_shape="domain_owner_receipt",
                source_ref="opl-agent-lab://mag/live-acceptance-owner-receipt",
                closeout_summary="MAG owner accepted live production acceptance receipt scaleout refs.",
                receipt_id="production-live-acceptance-2026-05-20",
                closeout_refs={
                    "agent_lab_suite_result_ref": "suite-result:mag/live-acceptance",
                    "meta_agent_coordination_ref": "meta-agent:mag/live-acceptance",
                },
            )
            payload = build_production_live_acceptance_receipt_projection(
                owner_receipt_evidence=receipt,
                agent_lab_suite_result=_agent_lab_suite_result(),
                meta_agent_coordination_result=_meta_agent_coordination_result(),
            )

        projection = payload["production_live_acceptance_receipt"]
        self.assertEqual(
            projection["surface_kind"],
            PRODUCTION_LIVE_ACCEPTANCE_RECEIPT_PROJECTION_KIND,
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

    def test_live_acceptance_receipt_projection_accepts_typed_blocker_patch_smoke_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt = _owner_receipt(
                Path(tmp_dir) / "runtime-state",
                receipt_shape="typed_blocker",
                source_ref="opl-agent-lab://mag/live-acceptance-blocked",
                closeout_summary="MAG owner still blocked.",
                receipt_id="production-live-acceptance-blocked",
            )
            payload = build_production_live_acceptance_receipt_projection(
                owner_receipt_evidence=receipt,
                agent_lab_suite_result=_agent_lab_suite_result(),
                meta_agent_coordination_result=_meta_agent_patch_work_order_result(),
            )

        projection = payload["production_live_acceptance_receipt"]
        self.assertEqual(projection["state"], "typed_blocker_closeout_refs_ready")
        self.assertEqual(projection["receipt"]["receipt_shape"], "typed_blocker")
        self.assertEqual(
            projection["production_acceptance"]["accepted_return_shape"],
            "typed_blocker_ref",
        )
        self.assertEqual(
            projection["production_acceptance"]["closed_typed_blocker_kind"],
            "domain_owner_live_acceptance_receipt_scaleout_required",
        )
        self.assertFalse(projection["authority_boundary"]["can_declare_fundability_ready"])
        self.assertFalse(projection["authority_boundary"]["can_declare_submission_ready_export"])
        self.assertFalse(projection["forbidden_write_proof"]["grant_truth_written"])
        self.assertFalse(projection["forbidden_write_proof"]["memory_body_written"])

    def test_live_acceptance_receipt_projection_rejects_non_mag_owner_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt = _owner_receipt(
                Path(tmp_dir) / "runtime-state",
                receipt_shape="domain_owner_receipt",
                source_ref="opl-agent-lab://mag/live-acceptance-owner-receipt",
                closeout_summary="MAG owner accepted live production acceptance receipt scaleout refs.",
                receipt_id="production-live-acceptance-non-mag-owner",
            )
            receipt = deepcopy(receipt)
            receipt["owner"] = "other-agent"
            receipt["target_domain_id"] = "other-agent"

            with self.assertRaises(WorkspaceStateError):
                build_production_live_acceptance_receipt_projection(
                    owner_receipt_evidence=receipt,
                    agent_lab_suite_result=_agent_lab_suite_result(),
                    meta_agent_coordination_result=_meta_agent_coordination_result(),
                )

    def test_live_acceptance_receipt_projection_binds_meta_agent_to_same_agent_lab_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt = _owner_receipt(
                Path(tmp_dir) / "runtime-state",
                receipt_shape="domain_owner_receipt",
                source_ref="opl-agent-lab://mag/live-acceptance-owner-receipt",
                closeout_summary="MAG owner accepted live production acceptance receipt scaleout refs.",
                receipt_id="production-live-acceptance-meta-mismatch",
            )
            meta_result = deepcopy(_meta_agent_coordination_result())
            meta_result["learning_loop"]["developer_patch_work_order"][
                "source_agent_lab_result_ref"
            ] = "different-result-id"

            with self.assertRaises(WorkspaceStateError):
                build_production_live_acceptance_receipt_projection(
                    owner_receipt_evidence=receipt,
                    agent_lab_suite_result=_agent_lab_suite_result(),
                    meta_agent_coordination_result=meta_result,
                )

    def test_live_acceptance_receipt_projection_requires_complete_agent_lab_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            receipt = _owner_receipt(
                Path(tmp_dir) / "runtime-state",
                receipt_shape="domain_owner_receipt",
                source_ref="opl-agent-lab://mag/live-acceptance-owner-receipt",
                closeout_summary="MAG owner accepted live production acceptance receipt scaleout refs.",
                receipt_id="production-live-acceptance-incomplete-agent-lab",
            )
            suite_result = deepcopy(_agent_lab_suite_result())
            suite_result["summary"].pop("forbidden_authority_flag_count")

            with self.assertRaises(WorkspaceStateError):
                build_production_live_acceptance_receipt_projection(
                    owner_receipt_evidence=receipt,
                    agent_lab_suite_result=suite_result,
                    meta_agent_coordination_result=_meta_agent_coordination_result(),
                )
