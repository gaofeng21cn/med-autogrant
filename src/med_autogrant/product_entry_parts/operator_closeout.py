from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_nonempty_string
from med_autogrant.workspace_types import WorkspaceStateError


MAG_OPERATOR_CLOSEOUT_PROJECTION_KIND = "mag_operator_closeout_readiness_projection"

_PRODUCTION_ACCEPTANCE_KIND = "mag_production_acceptance_evidence.v1"
_EXTERNAL_EVIDENCE_LEDGER_KIND = "mag_external_evidence_receipt_ledger.v1"
_RECEIPT_READINESS_KIND = "mag_receipt_readiness_projection"

_FORBIDDEN_BODY_KEYS = frozenset(
    {
        "artifact_body",
        "artifact_content",
        "app_workbench_state_body",
        "fundability_verdict_body",
        "grant_artifact_body",
        "grant_artifact_content",
        "grant_truth_body",
        "memory_body",
        "opl_runtime_state_body",
        "package_archive_body",
        "package_body",
        "proposal_text",
        "proposal_text_body",
        "review_artifact_body",
    }
)
_FORBIDDEN_READY_CLAIM_KEYS = frozenset(
    {
        "claims_app_workbench_consumption_complete",
        "claims_direct_hosted_parity_passed",
        "claims_external_default_caller_consumption_complete",
        "claims_fundability_ready",
        "claims_grant_ready",
        "claims_grant_or_fundability_ready",
        "claims_production_long_run_soak_complete",
        "claims_submission_ready_export",
        "fundability_ready",
        "quality_ready",
        "submission_ready",
        "submission_ready_export",
    }
)


def build_operator_closeout_readiness_projection(
    *,
    production_acceptance: Mapping[str, Any],
    external_evidence_receipt_ledger: Mapping[str, Any],
    receipt_readiness_projection: Mapping[str, Any],
) -> dict[str, Any]:
    _assert_mapping_kind(
        production_acceptance,
        expected_kind=_PRODUCTION_ACCEPTANCE_KIND,
        context="production_acceptance",
    )
    _assert_mapping_kind(
        external_evidence_receipt_ledger,
        expected_kind=_EXTERNAL_EVIDENCE_LEDGER_KIND,
        context="external_evidence_receipt_ledger",
    )
    _assert_mapping_kind(
        receipt_readiness_projection,
        expected_kind=_RECEIPT_READINESS_KIND,
        context="receipt_readiness_projection",
    )
    _assert_body_free(production_acceptance, path="production_acceptance")
    _assert_body_free(external_evidence_receipt_ledger, path="external_evidence_receipt_ledger")
    _assert_body_free(receipt_readiness_projection, path="receipt_readiness_projection")

    production_tail = _production_tail_summary(production_acceptance)
    evidence_summary = _external_evidence_summary(external_evidence_receipt_ledger)
    receipt_summary = _receipt_readiness_summary(receipt_readiness_projection)

    state = _projection_state(
        production_tail_closed=production_tail["closed"],
        accounting_open_count=evidence_summary["remaining_open_request_count"],
        real_gap_count=evidence_summary["remaining_real_evidence_gap_count"],
        missing_receipt_category_count=receipt_summary["missing_category_count"],
    )

    return {
        "surface_kind": MAG_OPERATOR_CLOSEOUT_PROJECTION_KIND,
        "version": "v1",
        "state": state,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "production_acceptance_tail": production_tail,
        "external_evidence_accounting": evidence_summary,
        "receipt_readiness": receipt_summary,
        "operator_attention": _operator_attention_items(
            production_tail=production_tail,
            evidence_summary=evidence_summary,
            receipt_summary=receipt_summary,
        ),
        "authority_boundary": {
            "projection_scope": "operator_closeout_readiness_only",
            "mag_implements_opl_runtime": False,
            "mag_implements_app_workbench": False,
            "can_declare_fundability_ready": False,
            "can_declare_quality_ready": False,
            "can_declare_export_ready": False,
            "can_declare_submission_ready": False,
            "request_accounting_closure_equals_real_evidence": False,
            "receipt_refs_ready_equals_quality_ready": False,
            "production_tail_closure_equals_grant_ready": False,
        },
        "projection_policy": (
            "read_existing_refs_only_distinguish_accounting_closure_from_real_evidence_"
            "and_receipt_coverage_from_quality_readiness"
        ),
    }


def _assert_mapping_kind(value: Any, *, expected_kind: str, context: str) -> None:
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 JSON object。")
    if value.get("surface_kind") != expected_kind:
        raise WorkspaceStateError(f"{context}.surface_kind 必须是 {expected_kind}。")


def _production_tail_summary(production_acceptance: Mapping[str, Any]) -> dict[str, Any]:
    closure = _require_mapping(production_acceptance, "closure_evidence", context="production_acceptance")
    evidence_tail_status = _require_nonempty_string(
        production_acceptance.get("evidence_tail_status"),
        field_name="evidence_tail_status",
        context="production_acceptance",
    )
    owner_receipt_ref = _require_nonempty_string(
        closure.get("owner_receipt_ref"),
        field_name="owner_receipt_ref",
        context="production_acceptance.closure_evidence",
    )
    accepted_return_shape = _require_nonempty_string(
        closure.get("accepted_return_shape"),
        field_name="accepted_return_shape",
        context="production_acceptance.closure_evidence",
    )
    return {
        "state": evidence_tail_status,
        "closed": evidence_tail_status == "closed_by_domain_owned_acceptance_receipt",
        "accepted_return_shape": accepted_return_shape,
        "owner_receipt_ref": owner_receipt_ref,
        "scope": "production_acceptance_tail_only",
        "can_declare_grant_ready": False,
    }


def _external_evidence_summary(ledger: Mapping[str, Any]) -> dict[str, Any]:
    summary = _require_mapping(ledger, "summary", context="external_evidence_receipt_ledger")
    remaining_open_request_count = _require_nonnegative_int(
        summary.get("remaining_open_request_count"),
        field_name="remaining_open_request_count",
        context="external_evidence_receipt_ledger.summary",
    )
    closed_request_count = _require_nonnegative_int(
        summary.get("closed_request_count"),
        field_name="closed_request_count",
        context="external_evidence_receipt_ledger.summary",
    )
    domain_owned_typed_blocker_count = _require_nonnegative_int(
        summary.get("domain_owned_typed_blocker_count"),
        field_name="domain_owned_typed_blocker_count",
        context="external_evidence_receipt_ledger.summary",
    )
    remaining_real_evidence_gap_ids = _require_string_list(
        ledger.get("remaining_real_evidence_gap_ids", []),
        field_name="remaining_real_evidence_gap_ids",
        context="external_evidence_receipt_ledger",
    )
    return {
        "state": _require_nonempty_string(
            ledger.get("state"),
            field_name="state",
            context="external_evidence_receipt_ledger",
        ),
        "closed_request_count": closed_request_count,
        "remaining_open_request_count": remaining_open_request_count,
        "domain_owned_typed_blocker_count": domain_owned_typed_blocker_count,
        "request_accounting_closed": remaining_open_request_count == 0,
        "remaining_real_evidence_gap_count": len(remaining_real_evidence_gap_ids),
        "remaining_real_evidence_gap_ids": remaining_real_evidence_gap_ids,
        "real_external_evidence_complete": False if remaining_real_evidence_gap_ids else True,
        "request_accounting_closure_equals_real_evidence": False,
    }


def _receipt_readiness_summary(projection: Mapping[str, Any]) -> dict[str, Any]:
    summary = _require_mapping(projection, "summary", context="receipt_readiness_projection")
    missing_categories = _require_string_list(
        projection.get("missing_categories", []),
        field_name="missing_categories",
        context="receipt_readiness_projection",
    )
    return {
        "state": _require_nonempty_string(
            projection.get("state"),
            field_name="state",
            context="receipt_readiness_projection",
        ),
        "covered_category_count": _require_nonnegative_int(
            summary.get("covered_category_count"),
            field_name="covered_category_count",
            context="receipt_readiness_projection.summary",
        ),
        "missing_category_count": len(missing_categories),
        "missing_categories": missing_categories,
        "receipt_refs_ready": not missing_categories,
        "quality_ready": False,
        "submission_ready": False,
    }


def _operator_attention_items(
    *,
    production_tail: Mapping[str, Any],
    evidence_summary: Mapping[str, Any],
    receipt_summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if not production_tail["closed"]:
        items.append(
            {
                "attention_id": "production_acceptance_tail_open",
                "state": "typed_blocker_required",
                "owner": TARGET_DOMAIN_ID,
            }
        )
    if evidence_summary["remaining_open_request_count"]:
        items.append(
            {
                "attention_id": "external_request_accounting_open",
                "state": "external_receipt_or_typed_blocker_required",
                "owner": TARGET_DOMAIN_ID,
            }
        )
    if evidence_summary["remaining_real_evidence_gap_count"]:
        items.append(
            {
                "attention_id": "real_external_evidence_missing",
                "state": "external_caller_app_parity_or_soak_receipt_required",
                "owner": "one-person-lab",
                "gap_ids": list(evidence_summary["remaining_real_evidence_gap_ids"]),
            }
        )
    if receipt_summary["missing_category_count"]:
        items.append(
            {
                "attention_id": "receipt_coverage_incomplete",
                "state": "workspace_receipt_refs_required",
                "owner": TARGET_DOMAIN_ID,
                "missing_categories": list(receipt_summary["missing_categories"]),
            }
        )
    if not items:
        items.append(
            {
                "attention_id": "quality_verdict_still_domain_owned",
                "state": "refs_ready_not_quality_ready",
                "owner": TARGET_DOMAIN_ID,
            }
        )
    return items


def _projection_state(
    *,
    production_tail_closed: bool,
    accounting_open_count: int,
    real_gap_count: int,
    missing_receipt_category_count: int,
) -> str:
    if not production_tail_closed:
        return "production_acceptance_tail_open"
    if accounting_open_count:
        return "external_request_accounting_open"
    if real_gap_count:
        return "real_external_evidence_missing"
    if missing_receipt_category_count:
        return "receipt_coverage_incomplete"
    return "operator_closeout_refs_ready_not_quality_ready"


def _assert_body_free(value: Any, *, path: str) -> None:
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = _require_nonempty_string(raw_key, field_name="key", context=path)
            normalized_key = _normalize_key(key)
            if normalized_key in _FORBIDDEN_BODY_KEYS:
                raise WorkspaceStateError(f"operator closeout projection 禁止包含 body 字段: {path}.{key}")
            if normalized_key in _FORBIDDEN_READY_CLAIM_KEYS and bool(item):
                raise WorkspaceStateError(
                    f"operator closeout projection 禁止包含 ready/completion claim: {path}.{key}"
                )
            _assert_body_free(item, path=f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_body_free(item, path=f"{path}[{index}]")


def _require_mapping(value: Mapping[str, Any], key: str, *, context: str) -> Mapping[str, Any]:
    item = value.get(key)
    if not isinstance(item, Mapping):
        raise WorkspaceStateError(f"{context}.{key} 必须是 object。")
    return item


def _require_nonnegative_int(value: Any, *, field_name: str, context: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise WorkspaceStateError(f"{context}.{field_name} 必须是非负整数。")
    return value


def _require_string_list(value: Any, *, field_name: str, context: str) -> list[str]:
    if not isinstance(value, list):
        raise WorkspaceStateError(f"{context}.{field_name} 必须是 string list。")
    return [
        _require_nonempty_string(item, field_name=field_name, context=context)
        for item in value
    ]


def _normalize_key(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


__all__ = [
    "MAG_OPERATOR_CLOSEOUT_PROJECTION_KIND",
    "build_operator_closeout_readiness_projection",
]
