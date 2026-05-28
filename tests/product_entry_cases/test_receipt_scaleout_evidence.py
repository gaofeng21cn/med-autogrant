from __future__ import annotations

import tempfile

from product_entry_cases.support import *  # noqa: F401,F403


CONTRACT_PATH = (
    REPO_ROOT
    / "contracts"
    / "production_acceptance"
    / "mag-workspace-receipt-scaleout-evidence-20260527.json"
)
SUSTAINED_CONSUMPTION_CONTRACT_PATH = (
    REPO_ROOT
    / "contracts"
    / "production_acceptance"
    / "mag-manifest-sustained-consumption-evidence-20260528.json"
)
SUBMISSION_GATE_BLOCKER_REF = (
    "typed-blocker:mag/package_and_submit_ready/"
    "submission_ready_export_gate/human-approval-required/2026-05-22"
)


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _production_acceptance() -> dict[str, object]:
    return json.loads(
        (REPO_ROOT / "contracts" / "production_acceptance" / "mag-production-acceptance.json")
        .read_text(encoding="utf-8")
    )


def _external_evidence_ledger() -> dict[str, object]:
    return json.loads(
        (REPO_ROOT / "contracts" / "external_evidence" / "mag-evidence-receipt-ledger.json")
        .read_text(encoding="utf-8")
    )


def _workspace_samples() -> tuple[tuple[str, Path, str, str, str], ...]:
    return (
        (
            "workspace-a",
            INPUT_EXAMPLE_PATH,
            "call_and_candidate_intake",
            "domain_owner_receipt",
            "accepted",
        ),
        (
            "workspace-b",
            CRITIQUE_EXAMPLE_PATH,
            "review_and_rebuttal",
            "no_regression_evidence",
            "rejected",
        ),
        (
            "workspace-c",
            FROZEN_EXAMPLE_PATH,
            "package_and_submit_ready",
            "typed_blocker",
            "accepted",
        ),
        (
            "workspace-d",
            REVISION_EXAMPLE_PATH,
            "proposal_authoring",
            "domain_owner_receipt",
            "rejected",
        ),
    )


def _memory_receipt_for_sample(
    entry: object,
    *,
    sample_id: str,
    workspace_path: Path,
    stage_id: str,
    decision: str,
    runtime_root: Path,
) -> dict[str, object]:
    proposal = entry.build_domain_memory_writeback_proposal(
        input_path=workspace_path,
        stage_id=stage_id,
        source_ref=f"workspace-runtime-ref:mag/receipt-scaleout/{sample_id}/memory",
        lesson_summary=f"{sample_id} strategy memory receipt scaleout marker.",
        proposal_id=f"mag-receipt-scaleout-{sample_id}",
    )
    proposal_path = runtime_root / "proposals" / f"{sample_id}.json"
    proposal_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(proposal_path, proposal)
    decision_payload = entry.build_domain_memory_writeback_decision(
        proposal_path=proposal_path,
        decision=decision,
        decision_reason=f"{sample_id} receipt scaleout {decision} decision.",
        memory_id=f"mag-receipt-scaleout-{sample_id}",
    )
    return entry.write_domain_memory_receipt_evidence(
        decision_payload=decision_payload,
        runtime_root=runtime_root,
    )["domain_memory_receipt_evidence"]


def _lifecycle_bundle_for_sample(
    entry: object,
    *,
    sample_id: str,
    workspace_path: Path,
    runtime_root: Path,
) -> dict[str, object]:
    receipts = [
        entry.write_lifecycle_receipt_evidence(
            input_path=workspace_path,
            operation=operation,
            receipt_shape=receipt_shape,
            source_ref=f"opl-lifecycle://mag/receipt-scaleout/{sample_id}/{operation}",
            closeout_summary=f"{sample_id} {operation} lifecycle receipt metadata only.",
            runtime_root=runtime_root,
            receipt_id=f"mag-receipt-scaleout-{sample_id}-{operation}",
        )["lifecycle_receipt_evidence"]
        for operation, receipt_shape in (
            ("cleanup", "typed_blocker"),
            ("restore", "domain_owner_receipt"),
            ("retention", "no_regression_evidence"),
        )
    ]
    return entry.build_lifecycle_receipt_bundle(
        lifecycle_receipt_evidence_items=receipts,
    )["lifecycle_receipt_bundle"]


def _package_lifecycle_for_sample(
    entry: object,
    *,
    sample_id: str,
    owner_receipt_ref: str,
    lifecycle_bundle: dict[str, object],
) -> dict[str, object]:
    return entry.build_package_lifecycle_handoff_projection(
        package_refs={
            "artifact_bundle_ref": f"mag-package://receipt-scaleout/{sample_id}/artifact-bundle",
            "final_package_ref": f"mag-package://receipt-scaleout/{sample_id}/final-package",
            "submission_ready_package_ref": (
                f"mag-package://receipt-scaleout/{sample_id}/submission-ready-package-ref-only"
            ),
        },
        gap_report={
            "gap_report_ref": f"mag-gap://receipt-scaleout/{sample_id}/manual-portal",
            "state": "blocked_by_submission_ready_export_gate",
            "summary": "Package refs are present; MAG human gate remains the submission boundary.",
            "gap_refs": [SUBMISSION_GATE_BLOCKER_REF],
        },
        export_verdict={
            "export_verdict_ref": f"mag-verdict://receipt-scaleout/{sample_id}/export-blocked",
            "verdict_state": "blocked",
            "owner": "med-autogrant",
            "source_kind": "mag_owner_receipt",
            "provenance_ref": owner_receipt_ref,
        },
        manual_portal_boundary={
            "manual_portal_boundary_ref": f"mag-boundary://receipt-scaleout/{sample_id}/manual-portal",
            "state": "human_portal_required_for_external_submit",
            "safe_action_ref": f"mag-action://receipt-scaleout/{sample_id}/manual-portal/open",
        },
        lifecycle_receipt_refs=dict(lifecycle_bundle["receipt_refs"]),
    )


def _build_scaleout_payload() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    from med_autogrant.product_entry import MedAutoGrantProductEntry

    entry = MedAutoGrantProductEntry()
    owner_receipts = []
    memory_receipts = []
    lifecycle_bundles = []
    package_lifecycle_items = []

    with tempfile.TemporaryDirectory() as tmp_dir:
        runtime_root = Path(tmp_dir) / "runtime-state"
        for sample_id, workspace_path, stage_id, receipt_shape, decision in _workspace_samples():
            owner_receipt = entry.write_owner_receipt_evidence(
                input_path=workspace_path,
                receipt_shape=receipt_shape,
                stage_id=stage_id,
                source_ref=f"opl-stage-attempt://mag-receipt-scaleout/{sample_id}",
                closeout_summary=(
                    f"{sample_id} body-free owner receipt scaleout; no grant truth mutation."
                ),
                runtime_root=runtime_root,
                receipt_id=f"mag-receipt-scaleout-{sample_id}-owner",
                closeout_refs={
                    "no_forbidden_write_ref": (
                        f"mag-no-forbidden-write:receipt-scaleout:{sample_id}"
                    )
                },
            )["owner_receipt_evidence"]
            memory_receipt = _memory_receipt_for_sample(
                entry,
                sample_id=sample_id,
                workspace_path=workspace_path,
                stage_id=stage_id,
                decision=decision,
                runtime_root=runtime_root,
            )
            lifecycle_bundle = _lifecycle_bundle_for_sample(
                entry,
                sample_id=sample_id,
                workspace_path=workspace_path,
                runtime_root=runtime_root,
            )
            package_lifecycle = _package_lifecycle_for_sample(
                entry,
                sample_id=sample_id,
                owner_receipt_ref=owner_receipt["receipt_instance_ref"],
                lifecycle_bundle=lifecycle_bundle,
            )
            owner_receipts.append(owner_receipt)
            memory_receipts.append(memory_receipt)
            lifecycle_bundles.append(lifecycle_bundle)
            package_lifecycle_items.append(package_lifecycle)

        readiness = entry.build_receipt_readiness_projection(
            owner_receipt_evidence_items=owner_receipts,
            memory_receipt_items=memory_receipts,
            package_lifecycle_items=package_lifecycle_items,
            lifecycle_receipt_items=lifecycle_bundles,
        )
        owner_payload = entry.build_opl_owner_payload_response(
            production_acceptance=_production_acceptance(),
            external_evidence_receipt_ledger=_external_evidence_ledger(),
            receipt_readiness_projection=readiness,
        )

    scaleout_payload = {
        "readiness": readiness,
        "owner_payload": owner_payload,
        "owner_receipts": owner_receipts,
        "memory_receipts": memory_receipts,
        "package_lifecycle_items": package_lifecycle_items,
        "lifecycle_bundles": lifecycle_bundles,
    }
    return scaleout_payload, readiness, owner_payload


class ProductEntryReceiptScaleoutEvidenceTest(unittest.TestCase):
    def test_real_workspace_receipt_scaleout_reaches_owner_payload_without_body_or_ready_claim(self) -> None:
        scaleout_payload, readiness, owner_payload = _build_scaleout_payload()

        self.assertEqual(readiness["state"], "receipt_refs_ready_not_quality_ready")
        self.assertEqual(readiness["missing_categories"], [])
        self.assertEqual(readiness["summary"]["covered_category_count"], 4)
        self.assertEqual(readiness["summary"]["total_receipt_ref_count"], 36)
        for category in (
            "owner_receipt",
            "memory_accept_reject",
            "package_export_lifecycle",
            "cleanup_restore_retention_lifecycle",
        ):
            with self.subTest(category=category):
                self.assertTrue(readiness["categories"][category]["covered"])
                self.assertEqual(readiness["categories"][category]["counts"]["input_item_count"], 4)

        self.assertEqual(owner_payload["status"], "blocked_by_submission_ready_human_gate")
        self.assertIn(SUBMISSION_GATE_BLOCKER_REF, owner_payload["typed_blocker_refs"])
        self.assertGreaterEqual(len(owner_payload["domain_owner_receipt_refs"]), 11)
        self.assertGreaterEqual(len(owner_payload["owner_chain_refs"]), 45)
        self.assertFalse(owner_payload["grant_ready_claimed"])
        self.assertFalse(owner_payload["quality_ready_claimed"])
        self.assertFalse(owner_payload["export_ready_claimed"])
        self.assertFalse(owner_payload["submission_ready_claimed"])
        self.assertFalse(owner_payload["authority_boundary"]["can_declare_submission_ready"])
        self.assertFalse(owner_payload["authority_boundary"]["typed_blocker_is_submission_ready"])
        stage_summary = owner_payload["stage_expected_receipt_payload_summary"]
        self.assertEqual(stage_summary["stage_count"], 6)
        self.assertEqual(
            stage_summary["status"],
            "per_stage_expected_receipt_payload_refs_ready_with_live_evidence_typed_blockers",
        )
        self.assertFalse(stage_summary["payload_body_allowed"])
        self.assertFalse(stage_summary["operator_payload_submitted"])
        self.assertFalse(stage_summary["success_refs_visible_is_completion"])
        self.assertFalse(stage_summary["grant_ready_claimed"])
        self.assertFalse(stage_summary["quality_ready_claimed"])
        self.assertFalse(stage_summary["export_ready_claimed"])
        self.assertFalse(stage_summary["submission_ready_claimed"])
        self.assertFalse(stage_summary["production_soak_complete_claimed"])
        self.assertFalse(stage_summary["authority_boundary"]["can_create_owner_receipt"])
        self.assertFalse(stage_summary["authority_boundary"]["can_declare_submission_ready"])
        self.assertEqual(
            len(stage_summary["typed_blocker_path_payload"]["typed_blocker_refs"]),
            6,
        )
        self.assertTrue(
            all(not stage["success_refs_visible_is_completion"] for stage in stage_summary["stages"])
        )
        self.assertTrue(all(not stage["grant_ready_claimed"] for stage in stage_summary["stages"]))
        self.assertTrue(
            all(
                not stage["authority_boundary"]["can_declare_submission_ready"]
                for stage in stage_summary["stages"]
            )
        )
        self.assertEqual(
            stage_summary["stages"][0]["success_refs_path_payload"]["runtime_event_refs"],
            ["runtime_event:call_and_candidate_intake.owner_receipt_recorded"],
        )

        for sample_id, *_ in _workspace_samples():
            with self.subTest(sample_id=sample_id):
                self.assertTrue(
                    any(sample_id in ref for ref in readiness["receipt_refs"]["owner_receipt"])
                )
                self.assertTrue(
                    any(sample_id in ref for ref in readiness["receipt_refs"]["memory_accept_reject"])
                )
                self.assertTrue(
                    any(
                        sample_id in ref
                        for ref in readiness["receipt_refs"]["package_export_lifecycle"]
                    )
                )
                self.assertTrue(
                    any(
                        sample_id in ref
                        for ref in readiness["receipt_refs"]["cleanup_restore_retention_lifecycle"]
                    )
                )

        encoded = json.dumps(scaleout_payload, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("strategy memory receipt scaleout marker", encoded)
        self.assertNotIn("receipt scaleout accepted decision", encoded)
        self.assertNotIn("receipt scaleout rejected decision", encoded)
        self.assertNotIn("PRIVATE_BODY_TOKEN", encoded)
        self.assertNotIn("SECRET_", encoded)

    def test_contract_snapshot_records_scaleout_closeout_without_grant_ready_claim(self) -> None:
        snapshot = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

        self.assertEqual(snapshot["surface_kind"], "mag_workspace_receipt_scaleout_evidence.v1")
        self.assertEqual(snapshot["state"], "workspace_receipt_refs_scaleout_observed")
        self.assertEqual(snapshot["workspace_receipt_scaleout"]["workspace_count"], 4)
        self.assertEqual(snapshot["workspace_receipt_scaleout"]["total_receipt_ref_count"], 36)
        self.assertTrue(snapshot["workspace_receipt_scaleout"]["receipt_kind_coverage_ready"])
        self.assertEqual(
            snapshot["owner_payload_response"]["status"],
            "blocked_by_submission_ready_human_gate",
        )
        self.assertEqual(
            snapshot["owner_payload_response"]["typed_blocker_refs"],
            [SUBMISSION_GATE_BLOCKER_REF],
        )
        self.assertEqual(
            snapshot["owner_payload_response"]["stage_expected_receipt_payload_stage_count"],
            6,
        )
        self.assertFalse(snapshot["owner_payload_response"]["stage_payload_body_allowed"])
        self.assertFalse(snapshot["owner_payload_response"]["stage_success_refs_visible_is_completion"])
        manifest_consumer = snapshot["manifest_consumer_evidence"]
        workorder = manifest_consumer["sustained_consumption_followthrough_workorder"]
        self.assertEqual(
            workorder["status"],
            "requires_real_app_operator_or_default_caller_payload",
        )
        self.assertEqual(workorder["authority_command"], "authority manifest-consumption-payload")
        self.assertEqual(
            workorder["accepted_payload_paths"]["typed_blocker_path"][
                "required_operator_payload_refs"
            ],
            ["typed_blocker_refs"],
        )
        self.assertTrue(workorder["rejects_unknown_operator_payload_fields"])
        self.assertFalse(workorder["claims_sustained_app_consumption_complete"])
        self.assertFalse(snapshot["claims"]["claims_grant_ready"])
        self.assertFalse(snapshot["claims"]["claims_submission_ready_export"])
        self.assertFalse(snapshot["authority_boundary"]["can_write_memory_body"])
        self.assertFalse(snapshot["authority_boundary"]["can_mutate_grant_artifact"])

    def test_manifest_sustained_consumption_snapshot_records_payload_without_ready_claim(self) -> None:
        snapshot = json.loads(SUSTAINED_CONSUMPTION_CONTRACT_PATH.read_text(encoding="utf-8"))

        self.assertEqual(
            snapshot["surface_kind"],
            "mag_manifest_sustained_consumption_evidence.v1",
        )
        self.assertEqual(snapshot["state"], "app_operator_default_caller_payload_observed_refs_only")
        self.assertEqual(snapshot["operator_payload"]["owner_payload_response_ref"], [
            "/product_entry_manifest/owner_payload_response",
        ])
        response = snapshot["manifest_sustained_consumption_payload_response"]
        self.assertEqual(
            response["surface_kind"],
            "mag_manifest_sustained_consumption_payload_response",
        )
        self.assertEqual(response["status"], "sustained_consumption_payload_refs_ready")
        self.assertEqual(response["recommended_payload_path"], "sustained_consumption_refs_path")
        self.assertTrue(response["operator_payload_submitted"])
        self.assertEqual(
            response["record_payload"]["typed_blocker_refs"],
            [
                "typed-blocker:mag/manifest-sustained-consumption/"
                "provider-long-soak-window-still-open/2026-05-28"
            ],
        )
        self.assertFalse(response["body_included"])
        self.assertFalse(response["claims_sustained_app_consumption_complete"])
        self.assertFalse(response["claims_provider_long_soak_complete"])
        self.assertFalse(response["claims_grant_ready"])
        self.assertFalse(response["claims_quality_ready"])
        self.assertFalse(response["claims_export_ready"])
        self.assertFalse(response["claims_submission_ready"])
        self.assertFalse(response["authority_boundary"]["can_create_owner_receipt"])
        self.assertFalse(
            response["authority_boundary"]["can_declare_app_sustained_consumption_complete"]
        )
        self.assertFalse(snapshot["claims"]["claims_owner_receipt_created"])
        self.assertFalse(snapshot["authority_boundary"]["can_submit_operator_payload"])

        encoded = json.dumps(
            {
                "operator_payload": snapshot["operator_payload"],
                "record_payload": response["record_payload"],
                "opl_runtime_action_execute_payload": response[
                    "opl_runtime_action_execute_payload"
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        self.assertNotIn("grant_truth_body", encoded)
        self.assertNotIn("memory_body", encoded)
        self.assertNotIn("proposal_text", encoded)
