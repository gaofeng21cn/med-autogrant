from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_nonempty_string
from med_autogrant.workspace_types import WorkspaceStateError


OPL_CONFLICT_OR_BLOCKER_ENVELOPE_KIND = "opl_conflict_or_blocker.v1"
MAG_CONFLICT_OR_BLOCKER_SURFACE_KIND = "mag_opl_conflict_or_blocker_envelope"

ALLOWED_CLASSIFICATIONS = (
    "authority_conflict",
    "evidence_blocker",
    "quality_blocker",
    "human_gate",
    "receipt_conflict",
)

FORBIDDEN_CLAIMS = (
    "provider_completion_is_domain_ready",
    "descriptor_resolved_is_grant_ready",
    "receipt_reconciled_is_grant_ready",
    "fallback_complete",
    "grant_ready",
    "quality_ready",
    "export_ready",
    "production_soak_complete",
    "opl_can_write_domain_truth",
    "opl_can_declare_fundability_ready",
    "opl_can_declare_export_ready",
)


def build_opl_conflict_or_blocker_envelope(
    payload: Mapping[str, Any] | None = None,
    *,
    classification: str | None = None,
    severity: str | None = None,
    owner_receipt: Mapping[str, Any] | None = None,
    typed_blocker: Mapping[str, Any] | None = None,
    no_regression_evidence: Mapping[str, Any] | None = None,
    source_refs: list[str] | tuple[str, ...] | None = None,
    receipt_refs: Mapping[str, Any] | None = None,
    verdict_refs: Mapping[str, Any] | None = None,
    safe_action_refs: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    body = _optional_payload(payload)
    resolved_classification = _require_classification(
        classification if classification is not None else body.get("classification")
    )
    resolved_severity = _require_nonempty_string(
        severity if severity is not None else body.get("severity", "blocking"),
        field_name="severity",
        context="conflict envelope",
    )
    resolved_owner_receipt = _optional_mapping(
        owner_receipt if owner_receipt is not None else body.get("owner_receipt"),
        field_name="owner_receipt",
    )
    resolved_typed_blocker = _optional_mapping(
        typed_blocker if typed_blocker is not None else body.get("typed_blocker"),
        field_name="typed_blocker",
    )
    resolved_no_regression_evidence = _optional_mapping(
        (
            no_regression_evidence
            if no_regression_evidence is not None
            else body.get("no_regression_evidence")
        ),
        field_name="no_regression_evidence",
    )
    resolved_source_refs = _read_refs(
        source_refs if source_refs is not None else body.get("source_refs"),
        field_name="source_refs",
    )
    receipt_ref_projection = _build_receipt_refs(
        explicit_refs=receipt_refs if receipt_refs is not None else body.get("receipt_refs"),
        owner_receipt=resolved_owner_receipt,
    )
    typed_blocker_refs = _build_typed_blocker_refs(resolved_typed_blocker)
    no_regression_evidence_refs = _build_no_regression_evidence_refs(resolved_no_regression_evidence)
    combined_source_refs = _combine_source_refs(
        resolved_source_refs,
        _optional_ref(resolved_owner_receipt, "source_ref"),
        _optional_ref(resolved_typed_blocker, "source_ref"),
        _optional_ref(resolved_no_regression_evidence, "source_ref"),
    )
    return {
        "surface_kind": MAG_CONFLICT_OR_BLOCKER_SURFACE_KIND,
        "envelope_kind": OPL_CONFLICT_OR_BLOCKER_ENVELOPE_KIND,
        "version": "v1",
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "classification": resolved_classification,
        "severity": resolved_severity,
        "source_refs": combined_source_refs,
        "receipt_refs": receipt_ref_projection,
        "typed_blocker_refs": typed_blocker_refs,
        "no_regression_evidence_refs": no_regression_evidence_refs,
        "verdict_refs": _read_ref_mapping(
            verdict_refs if verdict_refs is not None else body.get("verdict_refs"),
            field_name="verdict_refs",
        ),
        "safe_action_refs": _read_ref_mapping(
            safe_action_refs if safe_action_refs is not None else body.get("safe_action_refs"),
            field_name="safe_action_refs",
        ),
        "authority_boundary": _authority_boundary(),
        "forbidden_claims": list(FORBIDDEN_CLAIMS),
        "projection_policy": "refs_only_no_artifact_or_memory_body_no_fallback_completion",
    }


def _optional_payload(payload: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if payload is None:
        return {}
    if not isinstance(payload, Mapping):
        raise WorkspaceStateError("conflict envelope payload 必须是 object。")
    return payload


def _require_classification(value: Any) -> str:
    resolved = _require_nonempty_string(
        value,
        field_name="classification",
        context="conflict envelope",
    )
    if resolved not in ALLOWED_CLASSIFICATIONS:
        raise WorkspaceStateError(
            "conflict envelope classification 不支持: "
            f"{resolved}。只允许 {', '.join(ALLOWED_CLASSIFICATIONS)}。"
        )
    return resolved


def _optional_mapping(value: Any, *, field_name: str) -> Mapping[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"conflict envelope {field_name} 必须是 object。")
    return value


def _build_receipt_refs(
    *,
    explicit_refs: Any,
    owner_receipt: Mapping[str, Any] | None,
) -> dict[str, str]:
    refs = _read_ref_mapping(explicit_refs, field_name="receipt_refs")
    if owner_receipt is None:
        return refs
    projected = dict(refs)
    _copy_optional_string(
        owner_receipt,
        projected,
        source_key="receipt_instance_ref",
        target_key="owner_receipt_ref",
    )
    _copy_optional_string(owner_receipt, projected, source_key="receipt_id", target_key="receipt_id")
    _copy_optional_string(owner_receipt, projected, source_key="receipt_shape", target_key="receipt_shape")
    _copy_optional_string(owner_receipt, projected, source_key="source_ref", target_key="source_ref")
    return projected


def _build_typed_blocker_refs(typed_blocker: Mapping[str, Any] | None) -> dict[str, str]:
    if typed_blocker is None:
        return {}
    projected: dict[str, str] = {}
    for key in ("blocker_ref", "blocker_id", "blocker_kind", "source_ref"):
        _copy_optional_string(typed_blocker, projected, source_key=key, target_key=key)
    return projected


def _build_no_regression_evidence_refs(no_regression_evidence: Mapping[str, Any] | None) -> dict[str, Any]:
    if no_regression_evidence is None:
        return {}
    projected: dict[str, Any] = {}
    evidence_refs = _read_refs(
        no_regression_evidence.get("evidence_refs"),
        field_name="no_regression_evidence.evidence_refs",
    )
    if evidence_refs:
        projected["evidence_refs"] = evidence_refs
    for key in ("evidence_ref", "source_ref"):
        _copy_optional_string(no_regression_evidence, projected, source_key=key, target_key=key)
    return projected


def _read_ref_mapping(value: Any, *, field_name: str) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"conflict envelope {field_name} 必须是 object。")
    refs: dict[str, str] = {}
    for key, ref in value.items():
        if not isinstance(key, str) or not key.strip():
            raise WorkspaceStateError(f"conflict envelope {field_name} key 必须是非空字符串。")
        if not isinstance(ref, str) or not ref.strip():
            raise WorkspaceStateError(f"conflict envelope {field_name}.{key} 必须是非空字符串。")
        refs[key.strip()] = ref.strip()
    return refs


def _read_refs(value: Any, *, field_name: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise WorkspaceStateError(f"conflict envelope {field_name} 必须是 string list。")
    refs: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise WorkspaceStateError(f"conflict envelope {field_name} 必须只包含非空字符串。")
        refs.append(item.strip())
    return refs


def _copy_optional_string(
    source: Mapping[str, Any],
    target: dict[str, str],
    *,
    source_key: str,
    target_key: str,
) -> None:
    value = source.get(source_key)
    if value is None:
        return
    target[target_key] = _require_nonempty_string(
        value,
        field_name=source_key,
        context="conflict envelope",
    )


def _optional_ref(payload: Mapping[str, Any] | None, key: str) -> str | None:
    if payload is None or payload.get(key) is None:
        return None
    return _require_nonempty_string(payload.get(key), field_name=key, context="conflict envelope")


def _combine_source_refs(source_refs: list[str], *extra_refs: str | None) -> list[str]:
    combined: list[str] = []
    for ref in [*source_refs, *[item for item in extra_refs if item is not None]]:
        if ref not in combined:
            combined.append(ref)
    return combined


def _authority_boundary() -> dict[str, bool | str]:
    return {
        "mag_owns_domain_truth": True,
        "mag_owns_grant_truth": True,
        "mag_owns_verdicts": True,
        "mag_owns_fundability_verdict": True,
        "mag_owns_quality_verdict": True,
        "mag_owns_export_verdict": True,
        "mag_owns_owner_receipt": True,
        "mag_owns_package_authority": True,
        "mag_owns_safe_action_refs": True,
        "opl_ref_consumer_only": True,
        "opl_can_write_domain_truth": False,
        "opl_can_write_memory_body": False,
        "opl_can_mutate_grant_artifacts": False,
        "opl_can_declare_fundability_ready": False,
        "opl_can_declare_quality_ready": False,
        "opl_can_declare_export_ready": False,
        "provider_completion_is_domain_ready": False,
        "provider_completion_is_grant_ready": False,
        "descriptor_resolved_is_grant_ready": False,
        "receipt_reconciled_is_grant_ready": False,
        "fallback_complete": False,
        "grant_ready": False,
        "quality_ready": False,
        "export_ready": False,
        "production_soak_complete": False,
    }


__all__ = [
    "ALLOWED_CLASSIFICATIONS",
    "FORBIDDEN_CLAIMS",
    "MAG_CONFLICT_OR_BLOCKER_SURFACE_KIND",
    "OPL_CONFLICT_OR_BLOCKER_ENVELOPE_KIND",
    "build_opl_conflict_or_blocker_envelope",
]
