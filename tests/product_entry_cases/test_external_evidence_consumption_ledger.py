from __future__ import annotations

from product_entry_cases.support import *  # noqa: F401,F403


def _request_pack() -> dict[str, object]:
    from med_autogrant.product_entry_parts.consumer_thinning_pack import (
        build_external_evidence_request_pack,
    )

    return build_external_evidence_request_pack()


def _receipt_for(request: dict[str, object], *, receipt_shape: str | None = None) -> dict[str, object]:
    request_id = str(request["request_id"])
    shapes = request["required_receipt_shapes"]
    assert isinstance(shapes, list)
    shape = receipt_shape or str(shapes[0])
    return {
        "request_id": request_id,
        "receipt_shape": shape,
        "receipt_id": f"receipt-{request_id}",
        "receipt_ref": f"opl://receipts/mag/external-evidence/{request_id}.json",
        "producer_owner": str(request["requested_from"]),
        "source_ref": f"opl://external-evidence/{request_id}",
        "typed_blocker_ref": f"opl://typed-blockers/{request_id}",
        "no_regression_evidence_ref": f"opl://no-regression/{request_id}",
        "parity_receipt_ref": f"opl://parity/{request_id}",
    }


def _receipts_for_request_ids(request_pack: dict[str, object], request_ids: list[str]) -> list[dict[str, object]]:
    requests = request_pack["requests"]
    assert isinstance(requests, list)
    request_by_id = {str(item["request_id"]): item for item in requests}
    return [_receipt_for(request_by_id[request_id]) for request_id in request_ids]


def _first_live_receipts(request_pack: dict[str, object]) -> list[dict[str, object]]:
    requests = request_pack["requests"]
    assert isinstance(requests, list)
    by_id = {str(item["request_id"]): item for item in requests}
    return [
        _receipt_for(
            by_id["opl_generated_hosted_caller_pack_consumption"],
            receipt_shape="opl_hosted_domain_handler_call_receipt",
        ),
        _receipt_for(
            by_id["app_workbench_package_ref_consumption"],
            receipt_shape="app_consumed_package_ref_receipt",
        ),
        _receipt_for(
            by_id["production_default_caller_release_dist_consumption"],
            receipt_shape="production_default_caller_receipt",
        ),
        _receipt_for(
            by_id["owner_receipt_typed_blocker_ref_roundtrip"],
            receipt_shape="domain_owner_receipt",
        ),
        _receipt_for(
            by_id["continuous_no_forbidden_write_guard"],
            receipt_shape="continuous_guard_snapshot_receipt",
        ),
        _receipt_for(
            by_id["direct_hosted_parity_no_regression"],
            receipt_shape="direct_hosted_parity_receipt",
        ),
        _receipt_for(
            by_id["temporal_provider_long_soak_receipt_reconciliation"],
            receipt_shape="temporal_provider_long_soak_receipt",
        ),
    ]


class ProductEntryExternalEvidenceConsumptionLedgerTest(unittest.TestCase):
    def test_empty_receipts_keep_request_pack_declared_without_claiming_evidence(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        request_pack = _request_pack()
        ledger = MedAutoGrantProductEntry().build_external_evidence_consumption_ledger(
            external_evidence_request_pack=request_pack,
            evidence_receipts=[],
        )

        self.assertEqual(ledger["surface_kind"], "mag_external_evidence_consumption_ledger")
        self.assertEqual(ledger["state"], "request_pack_declared_external_evidence_not_claimed")
        self.assertEqual(ledger["summary"]["accepted_receipt_count"], 0)
        self.assertEqual(ledger["satisfied_request_ids"], [])
        self.assertEqual(ledger["missing_request_ids"], request_pack["required_request_ids"])
        self.assertFalse(ledger["claims"]["mag_claims_external_evidence_exists"])
        self.assertFalse(ledger["authority_boundary"]["mag_implements_opl_runtime"])
        self.assertFalse(ledger["authority_boundary"]["mag_implements_app_workbench"])
        self.assertFalse(ledger["authority_boundary"]["mag_can_authorize_fundability_ready"])
        self.assertFalse(ledger["authority_boundary"]["mag_can_authorize_export_ready"])
        self.assertFalse(ledger["authority_boundary"]["mag_can_authorize_submission_ready"])

    def test_partial_receipts_project_partial_consumption_without_ready_authority(self) -> None:
        from med_autogrant.product_entry_parts.external_evidence_ledger import (
            build_external_evidence_consumption_ledger,
        )

        request_pack = _request_pack()
        partial_request_ids = list(request_pack["required_request_ids"][:2])
        ledger = build_external_evidence_consumption_ledger(
            external_evidence_request_pack=request_pack,
            evidence_receipts=_receipts_for_request_ids(request_pack, partial_request_ids),
        )

        self.assertEqual(ledger["state"], "partial_consumption_evidence")
        self.assertEqual(ledger["satisfied_request_ids"], partial_request_ids)
        self.assertEqual(ledger["summary"]["satisfied_request_count"], 2)
        self.assertEqual(
            ledger["summary"]["missing_request_count"],
            len(request_pack["required_request_ids"]) - 2,
        )
        self.assertFalse(ledger["claims"]["mag_claims_external_evidence_exists"])
        self.assertFalse(ledger["claims"]["mag_authorizes_fundability_ready"])
        self.assertFalse(ledger["claims"]["mag_authorizes_export_ready"])
        self.assertFalse(ledger["claims"]["mag_authorizes_submission_ready"])

    def test_all_receipts_mark_consumed_complete_refs_only(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        request_pack = _request_pack()
        required_request_ids = list(request_pack["required_request_ids"])
        ledger = MedAutoGrantProductEntry().build_external_evidence_consumption_ledger(
            external_evidence_request_pack=request_pack,
            evidence_receipts=_receipts_for_request_ids(request_pack, required_request_ids),
        )

        self.assertEqual(ledger["state"], "consumed_complete")
        self.assertEqual(ledger["satisfied_request_ids"], required_request_ids)
        self.assertEqual(ledger["missing_request_ids"], [])
        self.assertTrue(ledger["claims"]["mag_claims_external_evidence_exists"])
        self.assertTrue(ledger["authority_boundary"]["mag_claims_external_evidence_exists"])
        self.assertFalse(ledger["authority_boundary"]["mag_implements_opl_runtime"])
        self.assertFalse(ledger["authority_boundary"]["mag_implements_app_workbench"])
        self.assertFalse(ledger["authority_boundary"]["mag_can_authorize_fundability_ready"])
        self.assertFalse(ledger["authority_boundary"]["mag_can_authorize_export_ready"])
        self.assertFalse(ledger["authority_boundary"]["mag_can_authorize_submission_ready"])

        encoded = json.dumps(ledger, ensure_ascii=False, sort_keys=True)
        self.assertNotIn("PRIVATE_BODY_TOKEN", encoded)
        for receipt in ledger["accepted_receipts"]:
            self.assertEqual(
                set(receipt),
                {"request_id", "receipt_shape", "producer_owner", "receipt_id", "refs"},
            )
            self.assertIn("receipt_ref", receipt["refs"])

    def test_first_live_production_receipts_cover_all_requested_evidence_without_ready_authority(self) -> None:
        from med_autogrant.product_entry import MedAutoGrantProductEntry

        request_pack = _request_pack()
        ledger = MedAutoGrantProductEntry().build_external_evidence_consumption_ledger(
            external_evidence_request_pack=request_pack,
            evidence_receipts=_first_live_receipts(request_pack),
        )

        self.assertEqual(ledger["state"], "consumed_complete")
        self.assertEqual(ledger["summary"]["required_request_count"], 7)
        self.assertEqual(ledger["summary"]["satisfied_request_count"], 7)
        self.assertEqual(ledger["summary"]["missing_request_count"], 0)
        self.assertEqual(ledger["missing_request_ids"], [])
        self.assertTrue(ledger["claims"]["mag_claims_external_evidence_exists"])
        self.assertFalse(ledger["claims"]["mag_authorizes_fundability_ready"])
        self.assertFalse(ledger["claims"]["mag_authorizes_quality_ready"])
        self.assertFalse(ledger["claims"]["mag_authorizes_export_ready"])
        self.assertFalse(ledger["claims"]["mag_authorizes_submission_ready"])
        self.assertFalse(ledger["authority_boundary"]["mag_implements_opl_runtime"])
        self.assertFalse(ledger["authority_boundary"]["mag_implements_app_workbench"])
        self.assertEqual(
            {receipt["request_id"] for receipt in ledger["accepted_receipts"]},
            set(request_pack["required_request_ids"]),
        )

    def test_illegal_request_id_fails_closed(self) -> None:
        from med_autogrant.product_entry_parts.external_evidence_ledger import (
            build_external_evidence_consumption_ledger,
        )

        request_pack = _request_pack()
        receipt = _receipts_for_request_ids(
            request_pack,
            [request_pack["required_request_ids"][0]],
        )[0]
        receipt["request_id"] = "not_declared_by_request_pack"

        with self.assertRaises(WorkspaceStateError):
            build_external_evidence_consumption_ledger(
                external_evidence_request_pack=request_pack,
                evidence_receipts=[receipt],
            )

    def test_receipt_shape_mismatch_fails_closed(self) -> None:
        from med_autogrant.product_entry_parts.external_evidence_ledger import (
            build_external_evidence_consumption_ledger,
        )

        request_pack = _request_pack()
        receipt = _receipts_for_request_ids(
            request_pack,
            [request_pack["required_request_ids"][0]],
        )[0]
        receipt["receipt_shape"] = "wrong_external_receipt_shape"

        with self.assertRaises(WorkspaceStateError):
            build_external_evidence_consumption_ledger(
                external_evidence_request_pack=request_pack,
                evidence_receipts=[receipt],
            )

    def test_producer_owner_mismatch_fails_closed(self) -> None:
        from med_autogrant.product_entry_parts.external_evidence_ledger import (
            build_external_evidence_consumption_ledger,
        )

        request_pack = _request_pack()
        receipt = _receipts_for_request_ids(
            request_pack,
            [request_pack["required_request_ids"][0]],
        )[0]
        receipt["producer_owner"] = "wrong-owner"

        with self.assertRaises(WorkspaceStateError):
            build_external_evidence_consumption_ledger(
                external_evidence_request_pack=request_pack,
                evidence_receipts=[receipt],
            )

    def test_forbidden_body_payload_fails_closed(self) -> None:
        from med_autogrant.product_entry_parts.external_evidence_ledger import (
            build_external_evidence_consumption_ledger,
        )

        request_pack = _request_pack()
        base_receipt = _receipts_for_request_ids(
            request_pack,
            [request_pack["required_request_ids"][0]],
        )[0]
        forbidden_body_fields = [
            "memory_body",
            "grant_artifact_body",
            "opl_runtime_state_body",
            "app_workbench_state_body",
        ]

        for field_name in forbidden_body_fields:
            receipt = dict(base_receipt)
            receipt[field_name] = "PRIVATE_BODY_TOKEN_DO_NOT_CONSUME"
            with self.subTest(field_name=field_name):
                with self.assertRaises(WorkspaceStateError):
                    build_external_evidence_consumption_ledger(
                        external_evidence_request_pack=request_pack,
                        evidence_receipts=[receipt],
                    )
