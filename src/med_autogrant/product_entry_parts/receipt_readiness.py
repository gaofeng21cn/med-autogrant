from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_nonempty_string
from med_autogrant.workspace_types import WorkspaceStateError


MAG_RECEIPT_READINESS_PROJECTION_KIND = "mag_receipt_readiness_projection"

_OWNER_RECEIPT_EVIDENCE_KIND = "mag_owner_receipt_evidence"
_REQUIRED_CATEGORIES = (
    "owner_receipt",
    "memory_accept_reject",
    "package_export_lifecycle",
    "cleanup_restore_retention_lifecycle",
)
_REF_FIELDS = ("receipt_ref", "receipt_instance_ref", "evidence_ref")
_NESTED_RECEIPT_PAYLOAD_KEYS = frozenset(
    {
        "owner_receipt_evidence",
        "domain_memory_receipt_evidence",
        "memory_receipt_read_projection",
        "package_lifecycle_handoff_projection",
        "lifecycle_receipt_evidence",
        "lifecycle_receipt_bundle",
        "receipt_readiness_projection",
    }
)
_RECEIPT_REF_CONTAINER_KEYS = frozenset({"receipt_refs"})
_SHAPE_FIELDS = ("receipt_shape", "decision", "operation")
_FORBIDDEN_BODY_KEYS = frozenset(
    {
        "artifact_body",
        "artifact_content",
        "canonical_grant_artifact_content",
        "grant_artifact",
        "grant_artifact_body",
        "grant_artifact_content",
        "memory_body",
        "package_archive_body",
        "package_body",
        "package_content",
        "package_payload",
        "proposal_body",
        "proposal_text",
        "proposal_text_body",
        "opl_runtime_state_body",
        "runtime_state_body",
        "runtime_state_payload",
    }
)
_FORBIDDEN_TRUE_FLAGS = frozenset(
    {
        "contains_memory_body",
        "contains_grant_artifact_content",
        "contains_canonical_grant_artifact_content",
        "contains_package_archive_body",
        "contains_opl_runtime_state_body",
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
        "can_declare_fundability_ready",
        "can_declare_quality_ready",
        "can_declare_export_ready",
        "can_declare_submission_ready",
        "claims_fundability_ready",
        "claims_quality_ready",
        "claims_export_ready",
        "claims_submission_ready",
    }
)


def build_receipt_readiness_projection(
    *,
    owner_receipt_evidence_items: list[Mapping[str, Any]],
    memory_receipt_items: list[Mapping[str, Any]],
    package_lifecycle_items: list[Mapping[str, Any]],
    lifecycle_receipt_items: list[Mapping[str, Any]],
) -> dict[str, Any]:
    categories = {
        "owner_receipt": _project_category(
            category_id="owner_receipt",
            items=owner_receipt_evidence_items,
        ),
        "memory_accept_reject": _project_category(
            category_id="memory_accept_reject",
            items=memory_receipt_items,
        ),
        "package_export_lifecycle": _project_category(
            category_id="package_export_lifecycle",
            items=package_lifecycle_items,
        ),
        "cleanup_restore_retention_lifecycle": _project_category(
            category_id="cleanup_restore_retention_lifecycle",
            items=lifecycle_receipt_items,
        ),
    }
    missing_categories = [
        category_id
        for category_id in _REQUIRED_CATEGORIES
        if not categories[category_id]["covered"]
    ]
    total_receipt_ref_count = sum(
        category["counts"]["receipt_ref_count"] for category in categories.values()
    )

    return {
        "surface_kind": MAG_RECEIPT_READINESS_PROJECTION_KIND,
        "version": "v1",
        "state": _projection_state(missing_categories),
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "required_categories": list(_REQUIRED_CATEGORIES),
        "missing_categories": missing_categories,
        "summary": {
            "required_category_count": len(_REQUIRED_CATEGORIES),
            "covered_category_count": len(_REQUIRED_CATEGORIES) - len(missing_categories),
            "missing_category_count": len(missing_categories),
            "total_receipt_ref_count": total_receipt_ref_count,
        },
        "categories": categories,
        "receipt_refs": {
            category_id: list(category["receipt_refs"])
            for category_id, category in categories.items()
        },
        "projection_policy": (
            "refs_and_shapes_only_no_grant_artifact_body_no_memory_body_"
            "no_proposal_text_no_package_archive_no_opl_runtime_state"
        ),
        "authority_boundary": _authority_boundary(),
    }


def _project_category(
    *,
    category_id: str,
    items: list[Mapping[str, Any]],
) -> dict[str, Any]:
    _require_item_list(items, context=category_id)
    receipt_refs: list[str] = []
    shapes: list[str] = []

    for index, item in enumerate(items):
        context = f"{category_id}[{index}]"
        _assert_body_free(item, path=context)
        if category_id == "owner_receipt":
            _require_owner_receipt_evidence_shape(item, context=context)
        item_refs = _collect_receipt_refs(item, context=context)
        if not item_refs:
            raise WorkspaceStateError(
                f"{context} 缺少 receipt_ref、receipt_instance_ref 或 evidence_ref。"
            )
        receipt_refs.extend(item_refs)
        shapes.extend(_collect_shapes(item))

    deduped_refs = _dedupe(receipt_refs)
    shape_counts = _count_by_value(shapes)
    covered = bool(deduped_refs)
    return {
        "category": category_id,
        "covered": covered,
        "counts": {
            "input_item_count": len(items),
            "receipt_ref_count": len(deduped_refs),
            "shape_count": sum(shape_counts.values()),
        },
        "missing_categories": [] if covered else [category_id],
        "receipt_refs": deduped_refs,
        "shape_counts": shape_counts,
    }


def _require_owner_receipt_evidence_shape(item: Mapping[str, Any], *, context: str) -> None:
    receipt = item.get("owner_receipt_evidence", item)
    if not isinstance(receipt, Mapping):
        raise WorkspaceStateError(f"{context}.owner_receipt_evidence 必须是 object。")
    if receipt.get("surface_kind") != _OWNER_RECEIPT_EVIDENCE_KIND:
        raise WorkspaceStateError(
            f"{context}.surface_kind 必须是 {_OWNER_RECEIPT_EVIDENCE_KIND}。"
        )
    _require_nonempty_string(
        receipt.get("receipt_id"),
        field_name="receipt_id",
        context=context,
    )
    _require_nonempty_string(
        receipt.get("receipt_shape"),
        field_name="receipt_shape",
        context=context,
    )


def _require_item_list(items: Any, *, context: str) -> None:
    if not isinstance(items, list):
        raise WorkspaceStateError(f"{context} 必须是 list of object。")
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise WorkspaceStateError(f"{context}[{index}] 必须是 object。")


def _collect_receipt_refs(value: Any, *, context: str) -> list[str]:
    if isinstance(value, Mapping):
        refs: list[str] = []
        for field_name in _REF_FIELDS:
            if field_name in value:
                refs.append(
                    _require_nonempty_string(
                        value.get(field_name),
                        field_name=field_name,
                        context=context,
                    )
                )
        for raw_key, item in value.items():
            key = _require_key(raw_key, context=context)
            if key in _NESTED_RECEIPT_PAYLOAD_KEYS:
                refs.extend(_collect_receipt_refs(item, context=f"{context}.{key}"))
                continue
            if key in _RECEIPT_REF_CONTAINER_KEYS:
                refs.extend(_collect_receipt_ref_container(item, context=f"{context}.{key}"))
        return refs
    if isinstance(value, list):
        refs = []
        for index, item in enumerate(value):
            refs.extend(_collect_receipt_refs(item, context=f"{context}[{index}]"))
        return refs
    return []


def _collect_receipt_ref_container(value: Any, *, context: str) -> list[str]:
    if isinstance(value, str):
        return [_require_nonempty_string(value, field_name="receipt_ref", context=context)]
    if isinstance(value, Mapping):
        refs: list[str] = []
        direct_refs = _collect_receipt_refs(value, context=context)
        refs.extend(direct_refs)
        if direct_refs:
            return refs
        for raw_key, item in value.items():
            key = _require_key(raw_key, context=context)
            if isinstance(item, str):
                refs.append(
                    _require_nonempty_string(item, field_name=key, context=context)
                )
                continue
            if isinstance(item, (Mapping, list)):
                refs.extend(_collect_receipt_ref_container(item, context=f"{context}.{key}"))
                continue
            raise WorkspaceStateError(f"{context}.{key} 必须是 receipt ref string。")
        return refs
    if isinstance(value, list):
        refs = []
        for index, item in enumerate(value):
            refs.extend(_collect_receipt_ref_container(item, context=f"{context}[{index}]"))
        return refs
    raise WorkspaceStateError(f"{context} 必须是 receipt ref object、list 或 string。")


def _collect_shapes(value: Any) -> list[str]:
    shapes: list[str] = []
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = str(raw_key)
            if key in _SHAPE_FIELDS:
                shapes.append(
                    _require_nonempty_string(
                        item,
                        field_name=key,
                        context="receipt readiness shape",
                    )
                )
                continue
            if isinstance(item, (Mapping, list)):
                shapes.extend(_collect_shapes(item))
    elif isinstance(value, list):
        for item in value:
            shapes.extend(_collect_shapes(item))
    return shapes


def _assert_body_free(value: Any, *, path: str) -> None:
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = _require_key(raw_key, context=path)
            normalized_key = _normalize_key(key)
            if normalized_key in _FORBIDDEN_BODY_KEYS:
                raise WorkspaceStateError(f"receipt readiness projection 禁止包含 body 字段: {path}.{key}")
            if normalized_key in _FORBIDDEN_TRUE_FLAGS and item is True:
                raise WorkspaceStateError(f"receipt readiness projection 禁止包含 body claim: {path}.{key}")
            if normalized_key in _FORBIDDEN_READY_CLAIM_KEYS and bool(item):
                raise WorkspaceStateError(
                    f"receipt readiness projection 禁止包含 ready/export claim: {path}.{key}"
                )
            _assert_body_free(item, path=f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_body_free(item, path=f"{path}[{index}]")


def _projection_state(missing_categories: list[str]) -> str:
    if len(missing_categories) == len(_REQUIRED_CATEGORIES):
        return "receipts_missing"
    if missing_categories:
        return "partial_receipt_coverage"
    return "receipt_refs_ready_not_quality_ready"


def _authority_boundary() -> dict[str, bool | str]:
    return {
        "mag_owns_receipt_readiness_projection": True,
        "projection_scope": "receipt_coverage_only",
        "refs_only_projection": True,
        "can_declare_fundability_ready": False,
        "can_declare_quality_ready": False,
        "can_declare_export_ready": False,
        "can_declare_submission_ready": False,
    }


def _require_key(value: Any, *, context: str) -> str:
    return _require_nonempty_string(value, field_name="key", context=context)


def _normalize_key(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped


def _count_by_value(values: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


__all__ = [
    "MAG_RECEIPT_READINESS_PROJECTION_KIND",
    "build_receipt_readiness_projection",
]
