from __future__ import annotations

import unittest
from med_autogrant.workspace import WorkspaceStateError
from product_entry_cases.support import (
    assert_false_keys,
    codex_execution_attempt,
    codex_review_attempt,
    production_acceptance_evidence,
    receipt_readiness_projection,
)


def _codex_receipt_bundle(*, reviewed: bool = True) -> dict[str, object]:
    from med_autogrant.product_entry_parts.codex_stage_receipts import (
        build_codex_stage_execution_receipt_bundle,
    )

    return build_codex_stage_execution_receipt_bundle(
        stage_id="review_and_rebuttal",
        execution_attempts=[codex_execution_attempt()],
        review_attempts=[codex_review_attempt()] if reviewed else [],
    )


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


def _operator_closeout(*, real_gap: bool = False) -> dict[str, object]:
    from med_autogrant.product_entry_parts.operator_closeout import (
        build_operator_closeout_readiness_projection,
    )

    return build_operator_closeout_readiness_projection(
        production_acceptance=production_acceptance_evidence(include_patch_loop_refs=True),
        external_evidence_receipt_ledger=_operator_evidence_ledger(real_gap=real_gap),
        receipt_readiness_projection=receipt_readiness_projection(total_ref_count=8),
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


def _build_bundle(**overrides: object) -> dict[str, object]:
    from med_autogrant.product_entry_parts.executor_first_closeout_bundle import (
        build_executor_first_closeout_bundle,
    )

    args: dict[str, object] = {
        "codex_stage_execution_receipt_bundle": _codex_receipt_bundle(),
        "operator_closeout_readiness_projection": _operator_closeout(),
        "physical_morphology_guard_projection": _physical_guard(),
        "external_evidence_consumption_ledger": _external_consumption_ledger(),
        "receipt_readiness_projection": receipt_readiness_projection(total_ref_count=8),
    }
    args.update(overrides)
    return build_executor_first_closeout_bundle(**args)  # type: ignore[arg-type]


class ProductEntryExecutorFirstCloseoutBundleTest(unittest.TestCase):
    def test_refs_ready_bundle_still_cannot_declare_grant_readiness(self) -> None:
        bundle = _build_bundle()

        self.assertEqual(bundle["surface_kind"], "mag_executor_first_closeout_bundle")
        self.assertEqual(bundle["state"], "refs_ready_not_quality_ready")
        self.assertTrue(bundle["refs_closeout"]["refs_ready"])
        assert_false_keys(
            self,
            bundle,
            (
                "can_declare_fundability_ready",
                "can_declare_quality_ready",
                "can_declare_export_ready",
                "can_declare_submission_ready",
                "bundle_ready_equals_grant_ready",
            ),
        )
        assert_false_keys(
            self,
            bundle["authority_boundary"],
            ("can_declare_fundability_ready", "bundle_ready_equals_grant_ready"),
        )

    def test_missing_codex_review_receipt_blocks_executor_first_bundle(self) -> None:
        bundle = _build_bundle(
            codex_stage_execution_receipt_bundle=_codex_receipt_bundle(reviewed=False),
        )

        self.assertEqual(bundle["state"], "missing_codex_review_receipt")
        self.assertEqual(bundle["blockers"][0]["blocker_id"], "missing_codex_review_receipt")
        self.assertFalse(bundle["refs_closeout"]["refs_ready"])
        self.assertFalse(bundle["authority_boundary"]["can_declare_submission_ready"])

    def test_operator_real_evidence_gap_blocks_bundle(self) -> None:
        bundle = _build_bundle(
            operator_closeout_readiness_projection=_operator_closeout(real_gap=True),
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
        blocked = _build_bundle(
            physical_morphology_guard_projection=_physical_guard(blocked=True),
        )
        evidence_gated = _build_bundle(
            physical_morphology_guard_projection=_physical_guard(evidence_gated=True),
        )

        self.assertEqual(blocked["state"], "physical_morphology_blocked")
        self.assertEqual(evidence_gated["state"], "physical_morphology_evidence_gated")
        self.assertNotEqual(blocked["state"], evidence_gated["state"])

    def test_bundle_rejects_wrong_surface_body_and_true_ready_claims(self) -> None:
        wrong_kind = _codex_receipt_bundle()
        wrong_kind["surface_kind"] = "wrong"
        with self.assertRaises(WorkspaceStateError):
            _build_bundle(
                codex_stage_execution_receipt_bundle=wrong_kind,
            )

        body_input = _operator_closeout()
        body_input["grant_artifact_body"] = "PRIVATE_BODY_TOKEN"
        with self.assertRaises(WorkspaceStateError):
            _build_bundle(
                operator_closeout_readiness_projection=body_input,
            )

        ready_claim = receipt_readiness_projection(total_ref_count=8)
        ready_claim["can_declare_quality_ready"] = True
        with self.assertRaises(WorkspaceStateError):
            _build_bundle(
                receipt_readiness_projection=ready_claim,
            )
