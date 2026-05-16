from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_nonempty_string
from med_autogrant.workspace_types import WorkspaceStateError


MAG_MEMORY_RECEIPT_READ_PROJECTION_KIND = "mag_memory_receipt_read_projection"
MAG_MEMORY_RECEIPT_READ_PROJECTION_STATE = "body_free_receipt_refs_ready_for_opl_consumption"

_OUTER_RECEIPT_FIELD = "domain_memory_receipt_evidence"
_FORBIDDEN_BODY_KEYS = frozenset(
    {
        "memory_body",
        "artifact_body",
        "artifact_content",
        "grant_artifact",
        "grant_artifact_body",
        "grant_artifact_content",
        "canonical_grant_artifact_content",
    }
)
_FORBIDDEN_CLAIM_KEYS = frozenset(
    {
        "fundability_ready",
        "quality_ready",
        "export_ready",
        "fundability_verdict",
        "quality_verdict",
        "export_verdict",
        "fundability_verdict_ref",
        "quality_verdict_ref",
        "export_verdict_ref",
        "authoring_quality_verdict",
        "authoring_quality_verdict_ref",
        "submission_ready_export_verdict",
        "submission_ready_export_verdict_ref",
        "verdict_refs",
    }
)
_FORBIDDEN_BOOLEAN_CLAIM_KEYS = frozenset(
    {
        "contains_memory_body",
        "contains_grant_artifact_content",
        "contains_canonical_grant_artifact_content",
        "contains_fundability_verdict",
        "contains_authoring_quality_verdict",
        "contains_submission_ready_export_verdict",
        "contains_quality_or_export_verdict",
    }
)


def build_memory_receipt_read_projection(
    receipt_items: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    receipt_refs: list[dict[str, str]] = []
    proposal_refs: list[dict[str, str]] = []
    memory_refs: list[dict[str, str]] = []
    accepted_count = 0
    rejected_count = 0

    for index, item in enumerate(receipt_items):
        if not isinstance(item, Mapping):
            raise WorkspaceStateError("memory receipt projection item 必须是 object。")
        _assert_body_free(item, path=f"receipt_items[{index}]")
        receipt = _coerce_receipt(item)
        decision = _require_decision(receipt, index=index)
        proposal_id = _require_nonempty_string(
            receipt.get("proposal_id"),
            field_name="proposal_id",
            context=f"memory receipt projection item[{index}]",
        )
        _assert_mag_decision_owner(receipt, index=index)

        if decision == "accepted":
            accepted_count += 1
            memory_ref_kind = "accepted_memory_ref"
        else:
            rejected_count += 1
            memory_ref_kind = "rejected_memory_ref"

        receipt_refs.append(_project_receipt_ref(receipt, decision=decision, proposal_id=proposal_id))
        proposal_refs.append(_project_proposal_ref(receipt, decision=decision, proposal_id=proposal_id))
        memory_refs.append(
            {
                "decision": decision,
                "proposal_id": proposal_id,
                "memory_ref_kind": memory_ref_kind,
                "memory_ref": _require_nonempty_string(
                    receipt.get(memory_ref_kind),
                    field_name=memory_ref_kind,
                    context=f"memory receipt projection item[{index}]",
                ),
            }
        )

    return {
        "surface_kind": MAG_MEMORY_RECEIPT_READ_PROJECTION_KIND,
        "version": "v1",
        "state": MAG_MEMORY_RECEIPT_READ_PROJECTION_STATE,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "receipt_refs": receipt_refs,
        "proposal_refs": proposal_refs,
        "memory_refs": memory_refs,
        "projection_policy": "refs_only_no_memory_body_no_grant_artifact_no_ready_or_verdict_claims",
        "authority_boundary": _authority_boundary(),
    }


def _coerce_receipt(item: Mapping[str, Any]) -> Mapping[str, Any]:
    inner = item.get(_OUTER_RECEIPT_FIELD)
    if inner is None:
        return item
    if not isinstance(inner, Mapping):
        raise WorkspaceStateError("domain_memory_receipt_evidence 必须是 object。")
    return inner


def _require_decision(receipt: Mapping[str, Any], *, index: int) -> str:
    decision = _require_nonempty_string(
        receipt.get("decision"),
        field_name="decision",
        context=f"memory receipt projection item[{index}]",
    )
    if decision not in {"accepted", "rejected"}:
        raise WorkspaceStateError(f"memory receipt projection decision 不允许: {decision}")
    return decision


def _assert_mag_decision_owner(receipt: Mapping[str, Any], *, index: int) -> None:
    owner = receipt.get("decision_owner", TARGET_DOMAIN_ID)
    resolved_owner = _require_nonempty_string(
        owner,
        field_name="decision_owner",
        context=f"memory receipt projection item[{index}]",
    )
    if resolved_owner != TARGET_DOMAIN_ID:
        raise WorkspaceStateError("memory receipt projection 只接受 MAG-owned decision receipt。")


def _project_receipt_ref(
    receipt: Mapping[str, Any],
    *,
    decision: str,
    proposal_id: str,
) -> dict[str, str]:
    projected = {
        "decision": decision,
        "proposal_id": proposal_id,
    }
    _copy_optional_ref(receipt, projected, "receipt_id")
    _copy_optional_ref(receipt, projected, "receipt_ref")
    _copy_optional_ref(receipt, projected, "receipt_instance_ref")
    if "receipt_ref" not in projected and "receipt_instance_ref" not in projected:
        raise WorkspaceStateError("memory receipt projection item 缺少 receipt_ref 或 receipt_instance_ref。")
    return projected


def _project_proposal_ref(
    receipt: Mapping[str, Any],
    *,
    decision: str,
    proposal_id: str,
) -> dict[str, str]:
    projected = {
        "decision": decision,
        "proposal_id": proposal_id,
    }
    _copy_optional_ref(receipt, projected, "proposal_ref")
    return projected


def _copy_optional_ref(source: Mapping[str, Any], target: dict[str, str], field_name: str) -> None:
    value = source.get(field_name)
    if value is None:
        return
    target[field_name] = _require_nonempty_string(
        value,
        field_name=field_name,
        context="memory receipt projection",
    )


def _assert_body_free(value: Any, *, path: str) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise WorkspaceStateError(f"{path} key 必须是 string。")
            if key in _FORBIDDEN_BODY_KEYS:
                raise WorkspaceStateError(f"memory receipt projection 禁止包含 body 字段: {path}.{key}")
            if key in _FORBIDDEN_CLAIM_KEYS:
                raise WorkspaceStateError(f"memory receipt projection 禁止包含 ready/verdict claim: {path}.{key}")
            if key in _FORBIDDEN_BOOLEAN_CLAIM_KEYS and item is True:
                raise WorkspaceStateError(f"memory receipt projection 禁止包含 body/verdict claim: {path}.{key}")
            _assert_body_free(item, path=f"{path}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _assert_body_free(item, path=f"{path}[{index}]")


def _authority_boundary() -> dict[str, bool | str]:
    return {
        "mag_owns_memory_body": True,
        "mag_owns_accept_reject": True,
        "mag_owns_grant_strategy_memory_accept_reject": True,
        "mag_owns_receipt_projection": True,
        "opl_consumes_refs_only": True,
        "opl_consumes_receipt_refs_only": True,
        "opl_can_hold_memory_body": False,
        "opl_can_write_memory_body": False,
        "opl_can_write_grant_artifact": False,
        "opl_can_accept_or_reject_memory": False,
        "opl_can_issue_fundability_verdict": False,
        "opl_can_issue_quality_verdict": False,
        "opl_can_issue_export_verdict": False,
    }


__all__ = [
    "MAG_MEMORY_RECEIPT_READ_PROJECTION_KIND",
    "MAG_MEMORY_RECEIPT_READ_PROJECTION_STATE",
    "build_memory_receipt_read_projection",
]
