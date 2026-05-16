from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    TARGET_DOMAIN_ID,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.workspace_types import WorkspaceStateError


HOSTED_RECEIPT_VERIFICATION_KIND = "mag_focused_hosted_receipt_verification"
OPL_HOSTED_ATTEMPT_EVIDENCE_KIND = "opl_hosted_stage_attempt_evidence"
OWNER_RECEIPT_EVIDENCE_KIND = "mag_owner_receipt_evidence"

_READY_CLAIM_KEYS = (
    "grant_ready",
    "fundability_ready",
    "quality_ready",
    "export_ready",
    "submission_ready_export",
    "production_soak_complete",
    "claims_grant_ready",
    "claims_fundability_ready",
    "claims_authoring_quality_ready",
    "claims_submission_ready_export",
)
_FORBIDDEN_WRITE_KEYS = (
    "repo_receipt_instance_written",
    "grant_truth_written",
    "grant_artifact_written",
    "memory_body_written",
    "fundability_verdict_written",
    "authoring_quality_verdict_written",
    "submission_ready_export_verdict_written",
)


def build_focused_hosted_receipt_verification(
    *,
    owner_receipt_evidence: Mapping[str, Any],
    opl_attempt_evidence: Mapping[str, Any],
    sidecar_closeout_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    receipt = _require_owner_receipt_evidence(owner_receipt_evidence)
    attempt = _require_opl_attempt_evidence(opl_attempt_evidence)
    closeout = dict(sidecar_closeout_result or {})
    breakdown = _require_mapping(
        attempt,
        "domain_breakdown",
        context="opl_hosted_stage_attempt_evidence",
    )
    receipt_ref = _require_nonempty_string_from_mapping(
        receipt,
        "receipt_instance_ref",
        context="owner_receipt_evidence",
    )
    receipt_shape = _require_nonempty_string_from_mapping(
        receipt,
        "receipt_shape",
        context="owner_receipt_evidence",
    )
    stage_id = _require_nonempty_string_from_mapping(receipt, "stage_id", context="owner_receipt_evidence")
    ledger_ref = _require_nonempty_string_from_mapping(attempt, "ledger_ref", context="opl_attempt_evidence")
    if stage_id != _require_nonempty_string_from_mapping(attempt, "stage_id", context="opl_attempt_evidence"):
        raise WorkspaceStateError("OPL attempt stage_id 与 MAG owner receipt stage_id 不一致。")

    typed_blocker_refs = _read_ref_list(breakdown.get("typed_blocker_refs"), field_name="typed_blocker_refs")
    no_regression_refs = _read_ref_list(
        breakdown.get("no_regression_evidence_refs"),
        field_name="no_regression_evidence_refs",
    )
    owner_receipt_ref = _require_nonempty_string_from_mapping(
        breakdown,
        "owner_receipt_ref",
        context="opl_attempt_evidence.domain_breakdown",
    )
    matches = {
        "owner_receipt_ref_matches_opl": owner_receipt_ref == receipt_ref,
        "ledger_ref_matches_receipt_source": ledger_ref
        == _require_nonempty_string_from_mapping(receipt, "source_ref", context="owner_receipt_evidence"),
        "receipt_ref_matches_sidecar": _receipt_ref_matches_sidecar(receipt_ref, closeout),
    }
    allowed_result = _allowed_result(
        receipt_shape=receipt_shape,
        receipt_ref=receipt_ref,
        typed_blocker_refs=typed_blocker_refs,
        no_regression_refs=no_regression_refs,
    )
    payload = {
        "surface_kind": HOSTED_RECEIPT_VERIFICATION_KIND,
        "version": "v1",
        "state": "focused_hosted_receipt_refs_verified_not_live_soak",
        "focused_status": _focused_status(allowed_result["result_shape"]),
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "stage_id": stage_id,
        "opl_attempt": {
            "attempt_ref": _require_nonempty_string_from_mapping(
                attempt,
                "attempt_ref",
                context="opl_attempt_evidence",
            ),
            "ledger_ref": ledger_ref,
            "provider_completion_ref": _provider_completion_ref(attempt),
            "provider_completion_consumed_as_readiness": False,
        },
        "mag_owner_receipt": {
            "receipt_ref": receipt_ref,
            "receipt_id": _require_nonempty_string_from_mapping(
                receipt,
                "receipt_id",
                context="owner_receipt_evidence",
            ),
            "receipt_shape": receipt_shape,
            "source_ref": _require_nonempty_string_from_mapping(
                receipt,
                "source_ref",
                context="owner_receipt_evidence",
            ),
        },
        "matches": matches,
        "allowed_result": allowed_result,
        "claims": {
            "claims_opl_provider_completion": bool(
                _require_mapping(
                    attempt,
                    "provider_completion",
                    context="opl_attempt_evidence",
                    allow_missing=True,
                ).get("completed", False)
            ),
            "claims_production_long_run_soak_complete": False,
            "claims_grant_fundability_ready": False,
            "claims_authoring_quality_ready": False,
            "claims_submission_ready_export": False,
        },
        "authority_boundary": {
            "mag_owner_receipt_authority": True,
            "opl_attempt_owner": "one-person-lab",
            "mag_implements_opl_provider": False,
            "mag_writes_opl_ledger": False,
            "opl_can_write_grant_truth": False,
            "opl_can_write_memory_body": False,
            "provider_completion_can_declare_grant_ready": False,
            "provider_completion_can_declare_export_ready": False,
        },
        "forbidden_write_proof": _forbidden_write_proof(receipt),
    }
    return {
        "ok": True,
        "command": "focused-hosted-receipt-verification",
        "focused_hosted_receipt_verification": payload,
    }


def _require_owner_receipt_evidence(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    if receipt.get("surface_kind") != OWNER_RECEIPT_EVIDENCE_KIND:
        raise WorkspaceStateError("owner_receipt_evidence.surface_kind 必须是 mag_owner_receipt_evidence。")
    proof = _require_mapping(receipt, "forbidden_write_proof", context="owner_receipt_evidence")
    if any(bool(proof.get(key)) for key in _FORBIDDEN_WRITE_KEYS):
        raise WorkspaceStateError("owner_receipt_evidence 不能包含 forbidden write。")
    return receipt


def _require_opl_attempt_evidence(attempt: Mapping[str, Any]) -> Mapping[str, Any]:
    if attempt.get("surface_kind") != OPL_HOSTED_ATTEMPT_EVIDENCE_KIND:
        raise WorkspaceStateError(
            "opl_attempt_evidence.surface_kind 必须是 opl_hosted_stage_attempt_evidence。"
        )
    breakdown = _require_mapping(attempt, "domain_breakdown", context="opl_attempt_evidence")
    if breakdown.get("target_domain_id") != TARGET_DOMAIN_ID:
        raise WorkspaceStateError("opl_attempt_evidence.domain_breakdown.target_domain_id 必须是 med-autogrant。")
    provider_completion = _require_mapping(
        attempt,
        "provider_completion",
        context="opl_attempt_evidence",
        allow_missing=True,
    )
    if any(bool(provider_completion.get(key)) for key in _READY_CLAIM_KEYS):
        raise WorkspaceStateError("OPL provider completion 不能声明 MAG grant readiness。")
    if any(bool(attempt.get(key)) for key in _READY_CLAIM_KEYS):
        raise WorkspaceStateError("OPL attempt evidence 不能声明 MAG grant readiness。")
    return attempt


def _allowed_result(
    *,
    receipt_shape: str,
    receipt_ref: str,
    typed_blocker_refs: list[str],
    no_regression_refs: list[str],
) -> dict[str, Any]:
    if receipt_shape == "typed_blocker":
        if receipt_ref not in typed_blocker_refs:
            raise WorkspaceStateError("typed_blocker receipt ref 必须出现在 OPL typed_blocker_refs 中。")
        return {
            "result_shape": "typed_blocker",
            "owner_receipt_ref": receipt_ref,
            "typed_blocker_refs": typed_blocker_refs,
            "no_regression_evidence_refs": [],
        }
    if receipt_shape == "no_regression_evidence":
        if receipt_ref not in no_regression_refs:
            raise WorkspaceStateError(
                "no_regression_evidence receipt ref 必须出现在 OPL no_regression_evidence_refs 中。"
            )
        return {
            "result_shape": "no_regression_evidence",
            "owner_receipt_ref": receipt_ref,
            "typed_blocker_refs": [],
            "no_regression_evidence_refs": no_regression_refs,
        }
    if receipt_shape == "domain_owner_receipt":
        return {
            "result_shape": "domain_owner_receipt",
            "owner_receipt_ref": receipt_ref,
            "typed_blocker_refs": [],
            "no_regression_evidence_refs": [],
        }
    raise WorkspaceStateError(f"receipt_shape 不支持: {receipt_shape}")


def _focused_status(result_shape: str) -> str:
    if result_shape == "typed_blocker":
        return "focused_typed_blocker_verified"
    if result_shape == "no_regression_evidence":
        return "focused_no_regression_evidence_verified"
    return "focused_domain_owner_receipt_verified"


def _provider_completion_ref(attempt: Mapping[str, Any]) -> str | None:
    provider_completion = _require_mapping(
        attempt,
        "provider_completion",
        context="opl_attempt_evidence",
        allow_missing=True,
    )
    ref = provider_completion.get("completion_ref")
    if ref is None:
        return None
    return _require_nonempty_string(ref, field_name="provider_completion.completion_ref")


def _receipt_ref_matches_sidecar(receipt_ref: str, closeout: Mapping[str, Any]) -> bool | None:
    if not closeout:
        return None
    return closeout.get("receipt_ref") == receipt_ref


def _read_ref_list(value: Any, *, field_name: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise WorkspaceStateError(f"opl_attempt_evidence.domain_breakdown.{field_name} 必须是 list。")
    refs: list[str] = []
    for ref in value:
        resolved = _require_nonempty_string(ref, field_name=field_name)
        if resolved not in refs:
            refs.append(resolved)
    return refs


def _forbidden_write_proof(receipt: Mapping[str, Any]) -> dict[str, bool]:
    proof = _require_mapping(receipt, "forbidden_write_proof", context="owner_receipt_evidence")
    return {key: bool(proof.get(key)) for key in _FORBIDDEN_WRITE_KEYS}


def _require_mapping(
    payload: Mapping[str, Any],
    field_name: str,
    *,
    context: str,
    allow_missing: bool = False,
) -> Mapping[str, Any]:
    value = payload.get(field_name)
    if value is None and allow_missing:
        return {}
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field_name}")
    return value
