from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_nonempty_string
from med_autogrant.workspace_types import WorkspaceStateError


MAG_MANIFEST_SUSTAINED_CONSUMPTION_PAYLOAD_RESPONSE_KIND = (
    "mag_manifest_sustained_consumption_payload_response"
)
_OWNER_PAYLOAD_RESPONSE_KIND = "mag_opl_owner_payload_response"
_WORKSPACE_RECEIPT_SCALEOUT_KIND = "mag_workspace_receipt_scaleout_evidence.v1"
_REQUIRED_SUCCESS_REFS = (
    "app_operator_consumption_ref",
    "default_caller_consumption_ref",
    "owner_payload_response_ref",
    "workspace_receipt_scaleout_evidence_ref",
    "no_forbidden_write_ref",
    "long_soak_or_typed_blocker_ref",
)
_TYPED_BLOCKER_REFS_FIELD = "typed_blocker_refs"
_ALLOWED_OPERATOR_PAYLOAD_FIELDS = (*_REQUIRED_SUCCESS_REFS, _TYPED_BLOCKER_REFS_FIELD)
_ALLOWED_OPERATOR_PAYLOAD_FIELD_SET = frozenset(_ALLOWED_OPERATOR_PAYLOAD_FIELDS)
_FORBIDDEN_BODY_KEYS = frozenset(
    {
        "artifact_body",
        "artifact_content",
        "fundability_verdict_body",
        "grant_artifact_body",
        "grant_artifact_content",
        "grant_truth_body",
        "memory_body",
        "package_archive_body",
        "package_body",
        "proposal_text",
        "proposal_text_body",
        "submission_ready_export_verdict_body",
    }
)
_FORBIDDEN_READY_CLAIM_KEYS = frozenset(
    {
        "claims_app_sustained_consumption_complete",
        "claims_export_ready",
        "claims_grant_ready",
        "claims_human_approval_obtained",
        "claims_provider_long_soak_complete",
        "claims_quality_ready",
        "claims_submission_ready",
        "claims_submission_ready_export",
        "export_ready",
        "grant_ready",
        "provider_long_soak_complete",
        "quality_ready",
        "submission_ready",
    }
)


def build_manifest_sustained_consumption_payload_response(
    *,
    owner_payload_response: Mapping[str, Any],
    workspace_receipt_scaleout_evidence: Mapping[str, Any],
    operator_payload: Mapping[str, Any],
) -> dict[str, Any]:
    _assert_mapping_kind(
        owner_payload_response,
        expected_kind=_OWNER_PAYLOAD_RESPONSE_KIND,
        context="owner_payload_response",
    )
    _assert_mapping_kind(
        workspace_receipt_scaleout_evidence,
        expected_kind=_WORKSPACE_RECEIPT_SCALEOUT_KIND,
        context="workspace_receipt_scaleout_evidence",
    )
    if not isinstance(operator_payload, Mapping) or not operator_payload:
        raise WorkspaceStateError("manifest sustained consumption payload 必须是非空 JSON object。")
    _assert_body_free(operator_payload, path="operator_payload")
    _assert_known_operator_payload_fields(operator_payload)

    typed_blocker_refs = _read_ref_list(operator_payload, _TYPED_BLOCKER_REFS_FIELD)
    success_payload = {
        field_name: _read_ref_list(operator_payload, field_name)
        for field_name in _REQUIRED_SUCCESS_REFS
    }
    has_complete_success_payload = all(success_payload[field_name] for field_name in _REQUIRED_SUCCESS_REFS)
    if typed_blocker_refs and has_complete_success_payload:
        raise WorkspaceStateError(
            "manifest sustained consumption payload 只能选择 success refs path 或 typed blocker path。"
        )
    if not typed_blocker_refs and not has_complete_success_payload:
        raise WorkspaceStateError(
            "manifest sustained consumption payload 缺少 success refs path 或 typed blocker refs。"
        )
    if typed_blocker_refs:
        return _build_typed_blocker_response(
            owner_payload_response=owner_payload_response,
            workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
            typed_blocker_refs=typed_blocker_refs,
        )
    return _build_success_ref_response(
        owner_payload_response=owner_payload_response,
        workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
        success_payload=success_payload,
    )


def _build_success_ref_response(
    *,
    owner_payload_response: Mapping[str, Any],
    workspace_receipt_scaleout_evidence: Mapping[str, Any],
    success_payload: Mapping[str, list[str]],
) -> dict[str, Any]:
    record_payload = {
        "app_operator_consumption_refs": list(success_payload["app_operator_consumption_ref"]),
        "default_caller_consumption_refs": list(success_payload["default_caller_consumption_ref"]),
        "owner_payload_response_refs": list(success_payload["owner_payload_response_ref"]),
        "workspace_receipt_scaleout_evidence_refs": list(
            success_payload["workspace_receipt_scaleout_evidence_ref"]
        ),
        "no_forbidden_write_refs": list(success_payload["no_forbidden_write_ref"]),
        "long_soak_or_typed_blocker_refs": list(success_payload["long_soak_or_typed_blocker_ref"]),
    }
    provider_long_soak_followthrough = _provider_long_soak_followthrough_from_refs(
        success_payload["long_soak_or_typed_blocker_ref"]
    )
    return _base_response(
        owner_payload_response=owner_payload_response,
        workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
        status="sustained_consumption_payload_refs_ready",
        recommended_payload_path="sustained_consumption_refs_path",
        operator_payload_submitted=True,
        record_payload=record_payload,
        provider_long_soak_followthrough=provider_long_soak_followthrough,
    )


def _build_typed_blocker_response(
    *,
    owner_payload_response: Mapping[str, Any],
    workspace_receipt_scaleout_evidence: Mapping[str, Any],
    typed_blocker_refs: list[str],
) -> dict[str, Any]:
    return _base_response(
        owner_payload_response=owner_payload_response,
        workspace_receipt_scaleout_evidence=workspace_receipt_scaleout_evidence,
        status="blocked_by_app_operator_typed_blocker",
        recommended_payload_path="typed_blocker_path",
        operator_payload_submitted=True,
        record_payload={
            "typed_blocker_refs": list(typed_blocker_refs),
        },
        provider_long_soak_followthrough=_provider_long_soak_followthrough_from_typed_blocker_path(
            typed_blocker_refs
        ),
    )


def _base_response(
    *,
    owner_payload_response: Mapping[str, Any],
    workspace_receipt_scaleout_evidence: Mapping[str, Any],
    status: str,
    recommended_payload_path: str,
    operator_payload_submitted: bool,
    record_payload: Mapping[str, Any],
    provider_long_soak_followthrough: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "surface_kind": MAG_MANIFEST_SUSTAINED_CONSUMPTION_PAYLOAD_RESPONSE_KIND,
        "version": "v1",
        "status": status,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "payload_kind": "manifest_sustained_consumption_refs_or_typed_blocker",
        "recommended_payload_path": recommended_payload_path,
        "record_payload": dict(record_payload),
        "opl_runtime_action_execute_payload": dict(record_payload),
        "source_surface_refs": {
            "owner_payload_response_ref": "/product_entry_manifest/owner_payload_response",
            "workspace_receipt_scaleout_evidence_ref": (
                "/product_entry_manifest/workspace_receipt_scaleout_evidence"
            ),
            "manifest_workorder_ref": (
                "/product_entry_manifest/owner_payload_response/"
                "manifest_consumer_evidence/sustained_consumption_followthrough_workorder"
            ),
        },
        "provider_long_soak_followthrough": dict(provider_long_soak_followthrough),
        "observed_counts": {
            "domain_owner_receipt_ref_count": len(
                _read_ref_list(owner_payload_response, "domain_owner_receipt_refs")
            ),
            "owner_chain_ref_count": len(_read_ref_list(owner_payload_response, "owner_chain_refs")),
            "typed_blocker_ref_count": len(_read_ref_list(owner_payload_response, "typed_blocker_refs")),
            "no_regression_evidence_ref_count": len(
                _read_ref_list(owner_payload_response, "no_regression_evidence_refs")
            ),
            "workspace_count": _workspace_count(workspace_receipt_scaleout_evidence),
        },
        "accepted_payload_paths": _accepted_payload_paths(),
        "allowed_operator_payload_fields": list(_ALLOWED_OPERATOR_PAYLOAD_FIELDS),
        "rejects_unknown_operator_payload_fields": True,
        "operator_payload_submitted": operator_payload_submitted,
        "body_included": False,
        "claims_sustained_app_consumption_complete": False,
        "claims_grant_ready": False,
        "claims_quality_ready": False,
        "claims_export_ready": False,
        "claims_submission_ready": False,
        "claims_provider_long_soak_complete": False,
        "authority_boundary": _authority_boundary(),
        "forbidden_payload_fields": sorted(_FORBIDDEN_BODY_KEYS),
    }


def _provider_long_soak_followthrough_from_refs(refs: list[str]) -> dict[str, Any]:
    typed_blocker_refs = [ref for ref in refs if _is_typed_blocker_ref(ref)]
    long_soak_evidence_refs = [ref for ref in refs if not _is_typed_blocker_ref(ref)]
    status = (
        "blocked_by_provider_long_soak_typed_blocker"
        if typed_blocker_refs
        else "provider_long_soak_evidence_refs_observed_not_mag_closeout"
    )
    return {
        "surface_kind": "mag_manifest_provider_long_soak_followthrough",
        "version": "v1",
        "status": status,
        "evidence_owner": "one-person-lab",
        "long_soak_or_typed_blocker_refs": list(refs),
        "typed_blocker_refs": typed_blocker_refs,
        "long_soak_evidence_refs": long_soak_evidence_refs,
        "requires_temporal_provider_long_soak_window_evidence": bool(
            typed_blocker_refs or not long_soak_evidence_refs
        ),
        "typed_blocker_is_provider_long_soak_completion": False,
        "claims_provider_long_soak_complete": False,
        "closes_provider_long_soak": False,
        "can_declare_provider_long_soak_complete": False,
    }


def _provider_long_soak_followthrough_from_typed_blocker_path(
    typed_blocker_refs: list[str],
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_manifest_provider_long_soak_followthrough",
        "version": "v1",
        "status": "blocked_by_app_operator_typed_blocker_path",
        "evidence_owner": "one-person-lab",
        "long_soak_or_typed_blocker_refs": [],
        "typed_blocker_refs": list(typed_blocker_refs),
        "long_soak_evidence_refs": [],
        "requires_temporal_provider_long_soak_window_evidence": True,
        "typed_blocker_is_provider_long_soak_completion": False,
        "claims_provider_long_soak_complete": False,
        "closes_provider_long_soak": False,
        "can_declare_provider_long_soak_complete": False,
    }


def _is_typed_blocker_ref(ref: str) -> bool:
    return ref.startswith("typed-blocker:")


def _accepted_payload_paths() -> dict[str, dict[str, Any]]:
    return {
        "sustained_consumption_refs_path": {
            "required_operator_payload_refs": list(_REQUIRED_SUCCESS_REFS),
            "typed_blocker_refs_must_be_absent": True,
            "requires_long_soak_or_typed_blocker_ref": True,
            "success_claimed": False,
            "closes_app_sustained_consumption": False,
            "closes_grant_ready": False,
            "closes_submission_ready": False,
            "closes_provider_long_soak": False,
        },
        "typed_blocker_path": {
            "required_operator_payload_refs": ["typed_blocker_refs"],
            "success_claimed": False,
            "closes_app_sustained_consumption": False,
            "closes_grant_ready": False,
            "closes_submission_ready": False,
            "closes_provider_long_soak": False,
        },
    }


def _authority_boundary() -> dict[str, bool | str]:
    return {
        "owner": TARGET_DOMAIN_ID,
        "refs_only": True,
        "mag_validates_payload_shape": True,
        "payload_owner": "app_operator_or_release_default_caller",
        "can_write_grant_truth": False,
        "can_read_memory_body": False,
        "can_read_artifact_body": False,
        "can_create_owner_receipt": False,
        "can_submit_operator_payload": False,
        "can_satisfy_provider_long_soak": False,
        "can_declare_app_sustained_consumption_complete": False,
        "can_declare_submission_ready": False,
        "can_declare_provider_long_soak_complete": False,
    }


def _assert_mapping_kind(value: Any, *, expected_kind: str, context: str) -> None:
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 JSON object。")
    if value.get("surface_kind") != expected_kind:
        raise WorkspaceStateError(f"{context}.surface_kind 必须是 {expected_kind}。")


def _workspace_count(workspace_receipt_scaleout_evidence: Mapping[str, Any]) -> int | None:
    scaleout = workspace_receipt_scaleout_evidence.get("workspace_receipt_scaleout")
    if not isinstance(scaleout, Mapping):
        return None
    value = scaleout.get("workspace_count")
    return value if isinstance(value, int) else None


def _read_ref_list(value: Mapping[str, Any], field_name: str) -> list[str]:
    raw_refs = value.get(field_name, [])
    if raw_refs is None:
        return []
    if not isinstance(raw_refs, list):
        raise WorkspaceStateError(f"{field_name} 必须是 string list。")
    return [
        _require_nonempty_string(ref, field_name=field_name)
        for ref in raw_refs
    ]


def _assert_body_free(value: Any, *, path: str) -> None:
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = _require_nonempty_string(raw_key, field_name="key", context=path)
            normalized_key = _normalize_key(key)
            if normalized_key in _FORBIDDEN_BODY_KEYS:
                raise WorkspaceStateError(f"manifest sustained consumption payload 禁止包含 body 字段: {path}.{key}")
            if normalized_key in _FORBIDDEN_READY_CLAIM_KEYS and bool(item):
                raise WorkspaceStateError(
                    f"manifest sustained consumption payload 禁止包含 ready/soak claim: {path}.{key}"
                )
            _assert_body_free(item, path=f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_body_free(item, path=f"{path}[{index}]")


def _normalize_key(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _assert_known_operator_payload_fields(operator_payload: Mapping[str, Any]) -> None:
    unknown_fields = [
        _require_nonempty_string(raw_key, field_name="key", context="operator_payload")
        for raw_key in operator_payload
        if raw_key not in _ALLOWED_OPERATOR_PAYLOAD_FIELD_SET
    ]
    if unknown_fields:
        joined = ", ".join(sorted(unknown_fields))
        raise WorkspaceStateError(
            "manifest sustained consumption payload 包含未声明字段: " + joined
        )


__all__ = [
    "MAG_MANIFEST_SUSTAINED_CONSUMPTION_PAYLOAD_RESPONSE_KIND",
    "build_manifest_sustained_consumption_payload_response",
]
