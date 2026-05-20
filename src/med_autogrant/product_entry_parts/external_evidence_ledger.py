from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_nonempty_string,
)
from med_autogrant.workspace_types import WorkspaceStateError


EXTERNAL_EVIDENCE_CONSUMPTION_LEDGER_KIND = "mag_external_evidence_consumption_ledger"

_REQUEST_PACK_KIND = "mag_external_evidence_request_pack"
_NO_EVIDENCE_STATE = "request_pack_declared_external_evidence_not_claimed"
_PARTIAL_STATE = "partial_consumption_evidence"
_COMPLETE_STATE = "consumed_complete"

_REQUIRED_RECEIPT_FIELDS = (
    "request_id",
    "receipt_shape",
    "receipt_ref",
    "producer_owner",
)
_FORBIDDEN_BODY_KEYS = frozenset(
    {
        "memory_body",
        "grant_artifact_body",
        "grant_artifact_content",
        "workspace_private_evidence_body",
        "private_evidence_body",
        "opl_runtime_state_body",
        "app_workbench_state_body",
        "artifact_body",
        "artifact_content",
        "package_body",
        "package_content",
    }
)
_FORBIDDEN_READY_CLAIM_KEYS = frozenset(
    {
        "fundability_ready",
        "quality_ready",
        "export_ready",
        "submission_ready",
        "submission_ready_export",
        "provider_completion_is_fundability_ready",
        "provider_completion_is_quality_ready",
        "provider_completion_is_export_ready",
        "provider_completion_is_submission_ready",
        "can_authorize_fundability_ready",
        "can_authorize_export_ready",
        "can_authorize_submission_ready",
        "can_declare_fundability_ready",
        "can_declare_export_ready",
        "can_declare_submission_ready",
        "can_declare_submission_ready_export",
        "claims_fundability_ready",
        "claims_export_ready",
        "claims_submission_ready",
        "claims_submission_ready_export",
    }
)
_REF_METADATA_KEYS = frozenset(
    {
        "receipt_ref",
        "typed_blocker_ref",
        "no_regression_evidence_ref",
        "parity_receipt_ref",
        "parity_evidence_ref",
        "producer_receipt_ref",
        "provider_receipt_ref",
        "source_ref",
        "source_surface_ref",
        "request_ref",
        "no_forbidden_write_evidence_ref",
        "long_soak_receipt_ref",
    }
)


def build_external_evidence_consumption_ledger(
    *,
    external_evidence_request_pack: Mapping[str, Any],
    evidence_receipts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    request_index = _request_index(external_evidence_request_pack)
    required_request_ids = _required_request_ids(external_evidence_request_pack, request_index)
    receipts = _validated_receipts(evidence_receipts, request_index=request_index)
    satisfied_request_ids = [
        request_id
        for request_id in required_request_ids
        if any(receipt["request_id"] == request_id for receipt in receipts)
    ]
    missing_request_ids = [
        request_id for request_id in required_request_ids if request_id not in satisfied_request_ids
    ]
    state = _state_for(satisfied_count=len(satisfied_request_ids), required_count=len(required_request_ids))
    claims_external_evidence_exists = state == _COMPLETE_STATE

    return {
        "surface_kind": EXTERNAL_EVIDENCE_CONSUMPTION_LEDGER_KIND,
        "version": "v1",
        "state": state,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "request_pack": {
            "surface_kind": _REQUEST_PACK_KIND,
            "request_pack_id": _require_nonempty_string(
                external_evidence_request_pack.get("request_pack_id"),
                field_name="request_pack_id",
                context="external_evidence_request_pack",
            ),
            "request_pack_ref": (
                "/product_entry_manifest/mag_consumer_thinning_contract/"
                "external_evidence_request_pack"
            ),
        },
        "summary": {
            "required_request_count": len(required_request_ids),
            "satisfied_request_count": len(satisfied_request_ids),
            "missing_request_count": len(missing_request_ids),
            "accepted_receipt_count": len(receipts),
        },
        "required_request_ids": required_request_ids,
        "satisfied_request_ids": satisfied_request_ids,
        "missing_request_ids": missing_request_ids,
        "request_status": [
            _project_request_status(
                request_id,
                request_index=request_index,
                receipts=receipts,
            )
            for request_id in required_request_ids
        ],
        "accepted_receipts": receipts,
        "claims": {
            "mag_claims_external_evidence_exists": claims_external_evidence_exists,
            "mag_authorizes_fundability_ready": False,
            "mag_authorizes_quality_ready": False,
            "mag_authorizes_export_ready": False,
            "mag_authorizes_submission_ready": False,
        },
        "authority_boundary": {
            "mag_role": "external_evidence_consumer_read_projection",
            "mag_consumes_external_evidence_refs": True,
            "mag_implements_opl_runtime": False,
            "mag_implements_app_workbench": False,
            "mag_claims_external_evidence_exists": claims_external_evidence_exists,
            "mag_can_authorize_fundability_ready": False,
            "mag_can_authorize_quality_ready": False,
            "mag_can_authorize_export_ready": False,
            "mag_can_authorize_submission_ready": False,
            "opl_runtime_owner": "one-person-lab",
            "app_workbench_owner": "codex_app",
            "projection_scope": "refs_shapes_and_request_coverage_only",
        },
        "projection_policy": "refs_only_no_payload_bodies_no_runtime_or_workbench_implementation",
    }


def _request_index(
    external_evidence_request_pack: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    if not isinstance(external_evidence_request_pack, Mapping):
        raise WorkspaceStateError("external_evidence_request_pack 必须是 JSON object。")
    if external_evidence_request_pack.get("surface_kind") != _REQUEST_PACK_KIND:
        raise WorkspaceStateError(
            f"external_evidence_request_pack.surface_kind 必须是 {_REQUEST_PACK_KIND}。"
        )
    raw_requests = external_evidence_request_pack.get("requests")
    if not isinstance(raw_requests, list) or not raw_requests:
        raise WorkspaceStateError("external_evidence_request_pack.requests 至少需要一条 request。")
    index: dict[str, Mapping[str, Any]] = {}
    for item in raw_requests:
        if not isinstance(item, Mapping):
            raise WorkspaceStateError("external_evidence_request_pack.requests 必须只包含 JSON object。")
        request_id = _require_nonempty_string(
            item.get("request_id"),
            field_name="request_id",
            context="external_evidence_request_pack.requests",
        )
        if request_id in index:
            raise WorkspaceStateError(f"external_evidence_request_pack request_id 重复: {request_id}")
        shapes = _required_receipt_shapes(item, request_id=request_id)
        if not shapes:
            raise WorkspaceStateError(
                f"external_evidence_request_pack.requests.{request_id} 缺少 required_receipt_shapes。"
            )
        index[request_id] = item
    return index


def _required_request_ids(
    external_evidence_request_pack: Mapping[str, Any],
    request_index: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    raw_ids = external_evidence_request_pack.get("required_request_ids")
    if not isinstance(raw_ids, list) or not raw_ids:
        raise WorkspaceStateError("external_evidence_request_pack.required_request_ids 至少需要一条 id。")
    required_ids: list[str] = []
    for item in raw_ids:
        request_id = _require_nonempty_string(
            item,
            field_name="required_request_ids",
            context="external_evidence_request_pack",
        )
        if request_id in required_ids:
            raise WorkspaceStateError(f"external_evidence_request_pack.required_request_ids 重复: {request_id}")
        if request_id not in request_index:
            raise WorkspaceStateError(
                f"external_evidence_request_pack.required_request_ids 未在 requests 中声明: {request_id}"
            )
        required_ids.append(request_id)
    return required_ids


def _validated_receipts(
    evidence_receipts: Sequence[Mapping[str, Any]],
    *,
    request_index: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(evidence_receipts, Sequence) or isinstance(evidence_receipts, (str, bytes)):
        raise WorkspaceStateError("evidence_receipts 必须是 list。")

    receipts: list[dict[str, Any]] = []
    for index, receipt in enumerate(evidence_receipts):
        if not isinstance(receipt, Mapping):
            raise WorkspaceStateError("evidence_receipts 必须只包含 JSON object。")
        _assert_refs_only_receipt(receipt, path=f"evidence_receipts[{index}]")
        for field_name in _REQUIRED_RECEIPT_FIELDS:
            _require_nonempty_string(
                receipt.get(field_name),
                field_name=field_name,
                context=f"evidence_receipts[{index}]",
            )
        request_id = _require_nonempty_string(
            receipt.get("request_id"),
            field_name="request_id",
            context=f"evidence_receipts[{index}]",
        )
        request = request_index.get(request_id)
        if request is None:
            raise WorkspaceStateError(f"external evidence receipt request_id 未声明: {request_id}")
        receipt_shape = _require_nonempty_string(
            receipt.get("receipt_shape"),
            field_name="receipt_shape",
            context=f"evidence_receipts[{index}]",
        )
        allowed_shapes = _required_receipt_shapes(request, request_id=request_id)
        if receipt_shape not in allowed_shapes:
            raise WorkspaceStateError(
                f"external evidence receipt_shape 不匹配 request_id={request_id}: {receipt_shape}"
            )
        producer_owner = _require_nonempty_string(
            receipt.get("producer_owner"),
            field_name="producer_owner",
            context=f"evidence_receipts[{index}]",
        )
        requested_from = _require_nonempty_string(
            request.get("requested_from"),
            field_name="requested_from",
            context=f"external_evidence_request_pack.requests.{request_id}",
        )
        if producer_owner != requested_from:
            raise WorkspaceStateError(
                f"external evidence producer_owner 不匹配 request_id={request_id}: {producer_owner}"
            )
        receipts.append(_project_receipt(receipt, index=index))
    return receipts


def _required_receipt_shapes(request: Mapping[str, Any], *, request_id: str) -> list[str]:
    raw_shapes = request.get("required_receipt_shapes")
    if not isinstance(raw_shapes, list):
        raise WorkspaceStateError(f"external_evidence_request_pack.requests.{request_id}.required_receipt_shapes 必须是 list。")
    shapes: list[str] = []
    for item in raw_shapes:
        shape = _require_nonempty_string(
            item,
            field_name="required_receipt_shapes",
            context=f"external_evidence_request_pack.requests.{request_id}",
        )
        if shape not in shapes:
            shapes.append(shape)
    return shapes


def _assert_refs_only_receipt(value: Any, *, path: str) -> None:
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = _require_nonempty_string(raw_key, field_name="key", context=path)
            normalized_key = _normalize_key(key)
            if _is_forbidden_body_key(normalized_key):
                raise WorkspaceStateError(f"external evidence receipt 禁止包含 body 字段: {path}.{key}")
            if normalized_key in _FORBIDDEN_READY_CLAIM_KEYS and bool(item):
                raise WorkspaceStateError(f"external evidence receipt 不能授权 ready/export claim: {path}.{key}")
            _assert_refs_only_receipt(item, path=f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_refs_only_receipt(item, path=f"{path}[{index}]")


def _project_receipt(receipt: Mapping[str, Any], *, index: int) -> dict[str, Any]:
    projected = {
        "request_id": _require_nonempty_string(
            receipt.get("request_id"),
            field_name="request_id",
            context=f"evidence_receipts[{index}]",
        ),
        "receipt_shape": _require_nonempty_string(
            receipt.get("receipt_shape"),
            field_name="receipt_shape",
            context=f"evidence_receipts[{index}]",
        ),
        "producer_owner": _require_nonempty_string(
            receipt.get("producer_owner"),
            field_name="producer_owner",
            context=f"evidence_receipts[{index}]",
        ),
    }
    receipt_id = receipt.get("receipt_id")
    if receipt_id is not None:
        projected["receipt_id"] = _require_nonempty_string(
            receipt_id,
            field_name="receipt_id",
            context=f"evidence_receipts[{index}]",
        )
    projected["refs"] = _project_refs(receipt, context=f"evidence_receipts[{index}]")
    return projected


def _project_refs(receipt: Mapping[str, Any], *, context: str) -> dict[str, Any]:
    refs: dict[str, Any] = {}
    for raw_key, value in receipt.items():
        key = _require_nonempty_string(raw_key, field_name="key", context=context)
        normalized_key = _normalize_key(key)
        if normalized_key in _REF_METADATA_KEYS or normalized_key.endswith("_ref"):
            refs[key] = _require_nonempty_string(value, field_name=key, context=context)
            continue
        if normalized_key.endswith("_refs"):
            refs[key] = _read_ref_list(value, field_name=key, context=context)
    if "receipt_ref" not in refs:
        raise WorkspaceStateError(f"{context} 缺少 receipt_ref。")
    return refs


def _read_ref_list(value: Any, *, field_name: str, context: str) -> list[str]:
    if not isinstance(value, list):
        raise WorkspaceStateError(f"{context}.{field_name} 必须是 ref string list。")
    refs: list[str] = []
    for item in value:
        ref = _require_nonempty_string(item, field_name=field_name, context=context)
        if ref not in refs:
            refs.append(ref)
    return refs


def _project_request_status(
    request_id: str,
    *,
    request_index: Mapping[str, Mapping[str, Any]],
    receipts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    request_receipts = [receipt for receipt in receipts if receipt["request_id"] == request_id]
    return {
        "request_id": request_id,
        "state": "consumed" if request_receipts else "missing_external_receipt",
        "required_receipt_shapes": _required_receipt_shapes(
            request_index[request_id],
            request_id=request_id,
        ),
        "accepted_receipt_refs": [
            receipt["refs"]["receipt_ref"]
            for receipt in request_receipts
        ],
    }


def _state_for(*, satisfied_count: int, required_count: int) -> str:
    if satisfied_count == 0:
        return _NO_EVIDENCE_STATE
    if satisfied_count == required_count:
        return _COMPLETE_STATE
    return _PARTIAL_STATE


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _is_forbidden_body_key(normalized_key: str) -> bool:
    if normalized_key in _FORBIDDEN_BODY_KEYS:
        return True
    if normalized_key.endswith("_ref") or normalized_key.endswith("_refs"):
        return False
    return (
        normalized_key == "body"
        or normalized_key.endswith("_body")
        or normalized_key.endswith("_content")
        or normalized_key.endswith("_payload")
    )


__all__ = [
    "EXTERNAL_EVIDENCE_CONSUMPTION_LEDGER_KIND",
    "build_external_evidence_consumption_ledger",
]
