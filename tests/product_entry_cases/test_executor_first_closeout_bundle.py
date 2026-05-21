from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


def _execution_attempt() -> dict[str, object]:
    return {
        "attempt_id": "attempt-critique-001",
        "executor": "codex_cli",
        "invocation_ref": "codex://invocations/critique-001",
        "task_record_ref": "runtime://opl/stage-attempts/critique-001.json",
        "receipt_ref": "runtime://mag/receipts/stage/critique-001.json",
        "output_artifact_ref": "runtime://mag/artifacts/critique-001.json",
    }


def _review_attempt() -> dict[str, object]:
    return {
        "review_attempt_id": "review-critique-001",
        "reviewer_executor": "codex_cli",
        "review_invocation_ref": "codex://invocations/review-critique-001",
        "review_task_record_ref": "runtime://opl/stage-attempts/review-critique-001.json",
        "review_receipt_ref": "runtime://mag/receipts/review/review-critique-001.json",
        "review_artifact_ref": "runtime://mag/artifacts/review-critique-001.json",
        "review_target_attempt_id": "attempt-critique-001",
        "independent_context": True,
        "shared_context_with_execution": False,
    }


def _codex_receipt_bundle(*, reviewed: bool = True) -> dict[str, object]:
    from med_autogrant.product_entry_parts.codex_stage_receipts import (
        build_codex_stage_execution_receipt_bundle,
    )

    return build_codex_stage_execution_receipt_bundle(
        stage_id="review_and_rebuttal",
        execution_attempts=[_execution_attempt()],
        review_attempts=[_review_attempt()] if reviewed else [],
    )


def _production_acceptance() -> dict[str, object]:
    return {
        "surface_kind": "mag_production_acceptance_evidence.v1",
        "evidence_tail_status": "closed_by_domain_owned_acceptance_receipt",
        "closure_evidence": {
            "accepted_return_shape": "domain_owner_receipt_ref",
            "owner_receipt_ref": "receipt:mag/production-live-acceptance/2026-05-20",
        },
        "patch_loop_refs": {
            "blocked_suite_result_ref": "agent-lab-suite-result:oma/mag/blocked-suite",
            "developer_patch_work_order_ref": "developer-work-order:oma/mag/ai-first-mag-patch-smoke",
            "patch_traceability_matrix_ref": "patch-traceability:oma/mag/ai-first-mag-patch-smoke",
            "target_repo_verification_refs": [
                "rtk ./scripts/run-pytest-clean.sh tests/product_entry_cases/test_executor_first_closeout_bundle.py -q",
                "rtk ./scripts/verify.sh",
                "rtk git diff --check",
            ],
            "target_runtime_read_model_consumption_ref": "/product_entry_manifest/production_live_acceptance_receipt",
            "workspace_environment_proof_ref": (
                "workspace-proof:med-autogrant/.worktrees/ai-first-mag-patch-smoke"
            ),
            "no_forbidden_write_proof_ref": (
                "contracts/agent_lab_handoff.json#/authority_boundary/oma_consumes_mag_refs_only"
            ),
            "target_owner_receipt_or_typed_blocker_ref": (
                "receipt:mag/production-live-acceptance/2026-05-20"
            ),
            "patch_absorption_ref": "git-commit:pending/codex/ai-first-mag-patch-smoke",
            "worktree_cleanup_ref": "worktree-cleanup:pending/ai-first-mag-patch-smoke",
            "agent_lab_re_evaluation_ref": (
                "agent-lab-run:oma/mag/ai-first-mag-patch-smoke/re-evaluation"
            ),
        },
    }


def _operator_evidence_ledger(*, real_gap: bool = False) -> dict[str, object]:
    return {
        "surface_kind": "mag_external_evidence_receipt_ledger.v1",
        "state": "request_pack_closed_by_receipt_or_domain_owned_typed_blockers",
        "summary": {
            "closed_request_count": 7,
            "remaining_open_request_count": 0,
            "domain_owned_typed_blocker_count": 0,
            "claims_external_runtime_evidence_received": False,
            "claims_grant_or_fundability_ready": False,
        },
        "remaining_real_evidence_gap_ids": (
            ["codex_app_workbench_package_ref_consumption_receipt"] if real_gap else []
        ),
    }


def _receipt_readiness(*, missing: list[str] | None = None) -> dict[str, object]:
    missing_categories = missing if missing is not None else []
    return {
        "surface_kind": "mag_receipt_readiness_projection",
        "state": (
            "receipt_refs_ready_not_quality_ready"
            if not missing_categories
            else "partial_receipt_coverage"
        ),
        "missing_categories": missing_categories,
        "summary": {
            "covered_category_count": 4 - len(missing_categories),
            "missing_category_count": len(missing_categories),
            "total_receipt_ref_count": 8,
        },
    }


def _operator_closeout(*, real_gap: bool = False) -> dict[str, object]:
    from med_autogrant.product_entry_parts.operator_closeout import (
        build_operator_closeout_readiness_projection,
    )

    return build_operator_closeout_readiness_projection(
        production_acceptance=_production_acceptance(),
        external_evidence_receipt_ledger=_operator_evidence_ledger(real_gap=real_gap),
        receipt_readiness_projection=_receipt_readiness(),
    )


def _source_item(
    *,
    module_id: str = "product_entry",
    declared_role: str = "domain_handler_target",
    forbidden_role_flags: dict[str, bool] | None = None,
) -> dict[str, object]:
    return {
        "path": f"src/med_autogrant/product_entry_parts/{module_id}.py",
        "module_id": module_id,
        "declared_role": declared_role,
        "evidence_refs": [f"/product_entry_manifest/physical_morphology/{module_id}"],
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


def _physical_guard(*, blocked: bool = False, evidence_gated: bool = False) -> dict[str, object]:
    from med_autogrant.product_entry_parts.physical_morphology_guard import (
        build_physical_morphology_guard_projection,
    )

    return build_physical_morphology_guard_projection(
        source_items=[
            _source_item(),
            _source_item(
                module_id="runtime_owner" if blocked else "owner_receipt",
                declared_role="generic_runtime_owner" if blocked else "minimal_authority_function",
                forbidden_role_flags={"generic_runtime_owner": True} if blocked else None,
            ),
        ],
        external_evidence_refs=[]
        if evidence_gated or blocked
        else [
            "opl://receipts/mag/physical-morphology/active-caller-migration.json",
            "opl://receipts/mag/physical-morphology/direct-hosted-parity.json",
            "receipt:mag/physical-morphology/owner-receipt-roundtrip.json",
            "opl://receipts/mag/physical-morphology/no-forbidden-write.json",
        ],
    )


def _external_consumption_ledger(*, complete: bool = True) -> dict[str, object]:
    return {
        "surface_kind": "mag_external_evidence_consumption_ledger",
        "state": "consumed_complete" if complete else "partial_consumption_evidence",
        "summary": {
            "required_request_count": 2,
            "satisfied_request_count": 2 if complete else 1,
            "missing_request_count": 0 if complete else 1,
            "accepted_receipt_count": 2 if complete else 1,
        },
        "missing_request_ids": [] if complete else ["direct_hosted_parity_receipt"],
        "claims": {
            "mag_claims_external_evidence_exists": complete,
            "mag_authorizes_fundability_ready": False,
            "mag_authorizes_quality_ready": False,
            "mag_authorizes_export_ready": False,
            "mag_authorizes_submission_ready": False,
        },
    }


class ProductEntryExecutorFirstCloseoutBundleTest(unittest.TestCase):
    def test_refs_ready_bundle_still_cannot_declare_grant_readiness(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        bundle = MedAutoGrantProductEntry().build_executor_first_closeout_bundle(
            codex_stage_execution_receipt_bundle=_codex_receipt_bundle(),
            operator_closeout_readiness_projection=_operator_closeout(),
            physical_morphology_guard_projection=_physical_guard(),
            external_evidence_consumption_ledger=_external_consumption_ledger(),
            receipt_readiness_projection=_receipt_readiness(),
        )

        self.assertEqual(bundle["surface_kind"], "mag_executor_first_closeout_bundle")
        self.assertEqual(bundle["state"], "refs_ready_not_quality_ready")
        self.assertTrue(bundle["refs_closeout"]["refs_ready"])
        self.assertFalse(bundle["refs_closeout"]["quality_ready"])
        self.assertFalse(bundle["can_declare_fundability_ready"])
        self.assertFalse(bundle["can_declare_quality_ready"])
        self.assertFalse(bundle["can_declare_export_ready"])
        self.assertFalse(bundle["can_declare_submission_ready"])
        self.assertFalse(bundle["bundle_ready_equals_grant_ready"])
        self.assertFalse(bundle["authority_boundary"]["can_declare_fundability_ready"])
        self.assertFalse(bundle["authority_boundary"]["bundle_ready_equals_grant_ready"])

    def test_refs_ready_bundle_projects_target_smoke_patch_loop_closeout_refs(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        bundle = MedAutoGrantProductEntry().build_executor_first_closeout_bundle(
            codex_stage_execution_receipt_bundle=_codex_receipt_bundle(),
            operator_closeout_readiness_projection=_operator_closeout(),
            physical_morphology_guard_projection=_physical_guard(),
            external_evidence_consumption_ledger=_external_consumption_ledger(),
            receipt_readiness_projection=_receipt_readiness(),
        )

        closeout = bundle["target_smoke_patch_loop_closeout"]

        self.assertEqual(closeout["closeout_type"], "refs_only_target_smoke_patch_loop")
        self.assertEqual(closeout["suite_result"], "blocked_suite")
        self.assertEqual(
            closeout["developer_work_order_ref"],
            "developer-work-order:oma/mag/ai-first-mag-patch-smoke",
        )
        self.assertEqual(
            closeout["patch_traceability_ref"],
            "patch-traceability:oma/mag/ai-first-mag-patch-smoke",
        )
        self.assertIn("rtk ./scripts/verify.sh", closeout["target_verification_refs"])
        self.assertEqual(
            closeout["runtime_read_model_consumption_ref"],
            "/product_entry_manifest/production_live_acceptance_receipt",
        )
        self.assertEqual(
            closeout["workspace_proof_ref"],
            "workspace-proof:med-autogrant/.worktrees/ai-first-mag-patch-smoke",
        )
        self.assertTrue(closeout["no_forbidden_write"]["proven"])
        self.assertEqual(closeout["owner_receipt_or_typed_blocker"]["return_shape"], "owner_receipt_ref")
        self.assertEqual(
            closeout["patch_absorption_ref"],
            "git-commit:pending/codex/ai-first-mag-patch-smoke",
        )
        self.assertEqual(
            closeout["worktree_cleanup_ref"],
            "worktree-cleanup:pending/ai-first-mag-patch-smoke",
        )
        self.assertEqual(
            closeout["agent_lab_re_evaluation_ref"],
            "agent-lab-run:oma/mag/ai-first-mag-patch-smoke/re-evaluation",
        )
        self.assertFalse(closeout["suite_pass_equals_closeout"])
        self.assertFalse(closeout["can_declare_quality_ready"])
        self.assertFalse(bundle["authority_boundary"]["mag_writes_grant_body"])
        self.assertFalse(bundle["authority_boundary"]["mag_writes_memory_body"])
        self.assertFalse(bundle["authority_boundary"]["mag_writes_package_body"])

    def test_missing_codex_review_receipt_blocks_executor_first_bundle(self) -> None:
        from med_autogrant.product_entry_parts.executor_first_closeout_bundle import (
            build_executor_first_closeout_bundle,
        )

        bundle = build_executor_first_closeout_bundle(
            codex_stage_execution_receipt_bundle=_codex_receipt_bundle(reviewed=False),
            operator_closeout_readiness_projection=_operator_closeout(),
            physical_morphology_guard_projection=_physical_guard(),
        )

        self.assertEqual(bundle["state"], "missing_codex_review_receipt")
        self.assertEqual(bundle["blockers"][0]["blocker_id"], "missing_codex_review_receipt")
        self.assertFalse(bundle["refs_closeout"]["refs_ready"])
        self.assertFalse(bundle["authority_boundary"]["can_declare_submission_ready"])

    def test_operator_real_evidence_gap_blocks_bundle(self) -> None:
        from med_autogrant.product_entry_parts.executor_first_closeout_bundle import (
            build_executor_first_closeout_bundle,
        )

        bundle = build_executor_first_closeout_bundle(
            codex_stage_execution_receipt_bundle=_codex_receipt_bundle(),
            operator_closeout_readiness_projection=_operator_closeout(real_gap=True),
            physical_morphology_guard_projection=_physical_guard(),
            external_evidence_consumption_ledger=_external_consumption_ledger(complete=False),
        )

        self.assertEqual(bundle["state"], "operator_real_evidence_gap")
        self.assertEqual(bundle["blockers"][0]["owner"], "one-person-lab")
        self.assertIn(
            "codex_app_workbench_package_ref_consumption_receipt",
            bundle["blockers"][0]["gap_ids"],
        )
        self.assertFalse(bundle["refs_closeout"]["refs_ready"])

    def test_physical_morphology_blocked_and_evidence_gated_are_distinct(self) -> None:
        from med_autogrant.product_entry_parts.executor_first_closeout_bundle import (
            build_executor_first_closeout_bundle,
        )

        blocked = build_executor_first_closeout_bundle(
            codex_stage_execution_receipt_bundle=_codex_receipt_bundle(),
            operator_closeout_readiness_projection=_operator_closeout(),
            physical_morphology_guard_projection=_physical_guard(blocked=True),
        )
        evidence_gated = build_executor_first_closeout_bundle(
            codex_stage_execution_receipt_bundle=_codex_receipt_bundle(),
            operator_closeout_readiness_projection=_operator_closeout(),
            physical_morphology_guard_projection=_physical_guard(evidence_gated=True),
        )

        self.assertEqual(blocked["state"], "physical_morphology_blocked")
        self.assertEqual(evidence_gated["state"], "physical_morphology_evidence_gated")
        self.assertNotEqual(blocked["state"], evidence_gated["state"])

    def test_bundle_rejects_wrong_surface_body_and_true_ready_claims(self) -> None:
        from med_autogrant.product_entry_parts.executor_first_closeout_bundle import (
            build_executor_first_closeout_bundle,
        )

        wrong_kind = _codex_receipt_bundle()
        wrong_kind["surface_kind"] = "wrong"
        with self.assertRaises(WorkspaceStateError):
            build_executor_first_closeout_bundle(
                codex_stage_execution_receipt_bundle=wrong_kind,
                operator_closeout_readiness_projection=_operator_closeout(),
                physical_morphology_guard_projection=_physical_guard(),
            )

        body_input = _operator_closeout()
        body_input["grant_artifact_body"] = "PRIVATE_BODY_TOKEN"
        with self.assertRaises(WorkspaceStateError):
            build_executor_first_closeout_bundle(
                codex_stage_execution_receipt_bundle=_codex_receipt_bundle(),
                operator_closeout_readiness_projection=body_input,
                physical_morphology_guard_projection=_physical_guard(),
            )

        ready_claim = _receipt_readiness()
        ready_claim["can_declare_quality_ready"] = True
        with self.assertRaises(WorkspaceStateError):
            build_executor_first_closeout_bundle(
                codex_stage_execution_receipt_bundle=_codex_receipt_bundle(),
                operator_closeout_readiness_projection=_operator_closeout(),
                physical_morphology_guard_projection=_physical_guard(),
                receipt_readiness_projection=ready_claim,
            )
