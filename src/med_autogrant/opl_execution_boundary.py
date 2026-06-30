from __future__ import annotations

from typing import Any, Mapping


_DEFAULT_EXECUTOR_KIND = "codex_cli"
_OPL_OWNER = "one-person-lab"
_STAGE_TRANSITION_AUTHORITY = "one-person-lab"
_OWNER_CHAIN_DEFAULT_CALLER_ROLE = "opl_owner_chain_default_caller"
_ACCEPTED_STAGE_RUN_REF_FIELDS = (
    "stage_run_ref",
    "temporal_stage_run_ref",
)
_LEASE_OR_RECEIPT_REF_FIELDS = (
    "attempt_lease_ref",
    "lease_ref",
    "receipt_ref",
    "stage_attempt_receipt_ref",
)
_CALLER_ROLE_FIELD = "caller_role"
_STAGE_RUN_REF_MARKERS = (
    "stage-run",
    "stage_run",
    "temporal-stage-run",
    "temporal_stage_run",
)
_OWNER_CHAIN_DEFAULT_CALLER_REF_MARKER = "owner-chain-default-caller"
_ALLOWED_STAGE_AUTHORITY_RETURN_SHAPES = [
    "transition_intent_ref",
    "domain_owner_receipt",
    "typed_blocker",
    "no_regression_evidence",
]


def require_opl_default_stage_attempt(
    payload: Mapping[str, Any] | None,
    *,
    controller_id: str,
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        return {
            "ok": False,
            "typed_blocker": _build_typed_blocker(
                controller_id=controller_id,
                reason="missing_opl_stage_attempt",
            ),
        }

    executor_kind = _read_string(payload, "executor_kind")
    runtime_owner = _read_string(payload, "runtime_owner") or _read_string(payload, "owner")
    lease_or_receipt_refs = _read_strings(payload, _LEASE_OR_RECEIPT_REF_FIELDS)
    stage_run_ref = _read_stage_run_ref(payload, lease_or_receipt_refs)
    caller_role = _read_caller_role(payload, lease_or_receipt_refs)
    has_lease_or_receipt = bool(lease_or_receipt_refs)

    if runtime_owner != _OPL_OWNER:
        return {
            "ok": False,
            "typed_blocker": _build_typed_blocker(
                controller_id=controller_id,
                reason="opl_runtime_owner_required",
            ),
        }
    if executor_kind != _DEFAULT_EXECUTOR_KIND:
        return {
            "ok": False,
            "typed_blocker": _build_typed_blocker(
                controller_id=controller_id,
                reason="opl_default_executor_required",
            ),
        }
    if not has_lease_or_receipt:
        return {
            "ok": False,
            "typed_blocker": _build_typed_blocker(
                controller_id=controller_id,
                reason="opl_attempt_lease_or_receipt_required",
            ),
        }
    if not stage_run_ref:
        return {
            "ok": False,
            "typed_blocker": _build_typed_blocker(
                controller_id=controller_id,
                reason="opl_stage_run_ref_required",
            ),
        }
    if caller_role != _OWNER_CHAIN_DEFAULT_CALLER_ROLE:
        return {
            "ok": False,
            "typed_blocker": _build_typed_blocker(
                controller_id=controller_id,
                reason="opl_owner_chain_default_caller_required",
            ),
        }

    return {
        "ok": True,
        "execution_boundary": {
            "surface_kind": "mag_opl_execution_boundary",
            "controller_id": controller_id,
            "runtime_owner": _OPL_OWNER,
            "stage_run_ref": stage_run_ref,
            "caller_role": caller_role,
            "required_default_executor_kind": _DEFAULT_EXECUTOR_KIND,
            "required_caller_role": _OWNER_CHAIN_DEFAULT_CALLER_ROLE,
            "attempt_lease_or_receipt_observed": True,
            "owner_chain_default_caller_observed": True,
            "mag_owns_durable_loop": False,
            "mag_owns_attempt_ledger": False,
            "allowed_return_shapes": [
                "domain_owner_receipt",
                "typed_blocker",
                "no_regression_evidence",
            ],
            "stage_transition_authority": _STAGE_TRANSITION_AUTHORITY,
            "mag_writes_stage_current_pointer": False,
            "mag_writes_stage_terminal_state": False,
            "provider_completion_is_stage_transition": False,
        },
    }


def build_stage_transition_authority_boundary(
    *,
    surface_id: str,
    mag_role: str,
) -> dict[str, Any]:
    return {
        "surface_kind": "mag_stage_transition_authority_boundary",
        "surface_id": surface_id,
        "stage_transition_authority": _STAGE_TRANSITION_AUTHORITY,
        "stage_transition_authority_role": "sole_stage_current_terminal_next_writer",
        "mag_role": mag_role,
        "mag_writes_stage_current_pointer": False,
        "mag_writes_stage_terminal_state": False,
        "mag_writes_current_owner_delta": False,
        "mag_selects_next_opl_stage": False,
        "provider_completion_is_stage_transition": False,
        "workspace_lifecycle_stage_is_domain_observation": True,
        "recommendation_requires_opl_stage_transition_authority": True,
        "allowed_return_shapes": list(_ALLOWED_STAGE_AUTHORITY_RETURN_SHAPES),
    }


def _build_typed_blocker(*, controller_id: str, reason: str) -> dict[str, Any]:
    return {
        "surface_kind": "mag_opl_execution_boundary_typed_blocker",
        "controller_id": controller_id,
        "blocker_kind": reason,
        "typed_blocker_ref": f"typed-blocker:mag/{controller_id}/opl-default-stage-attempt-required",
        "required_runtime_owner": _OPL_OWNER,
        "required_default_executor_kind": _DEFAULT_EXECUTOR_KIND,
        "required_stage_run_ref_fields": list(_ACCEPTED_STAGE_RUN_REF_FIELDS),
        "required_stage_run_ref_sources": [
            *list(_ACCEPTED_STAGE_RUN_REF_FIELDS),
            *list(_LEASE_OR_RECEIPT_REF_FIELDS),
        ],
        "required_caller_role": _OWNER_CHAIN_DEFAULT_CALLER_ROLE,
        "required_owner_chain_ref_marker": _OWNER_CHAIN_DEFAULT_CALLER_REF_MARKER,
        "required_evidence": "OPL stage attempt lease or default executor receipt",
        "required_owner_chain_policy": "OPL StageRun owner-chain default caller role",
        "mag_owns_durable_loop": False,
        "mag_owns_attempt_ledger": False,
        "stage_transition_authority": _STAGE_TRANSITION_AUTHORITY,
        "mag_writes_stage_current_pointer": False,
        "mag_writes_stage_terminal_state": False,
        "hermes_agent_boundary": "explicit_non_default_opl_executor_adapter_receipt_lane_only",
    }


def _read_string(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None


def _read_first_string(payload: Mapping[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        text = _read_string(payload, key)
        if text:
            return text
    return None


def _read_strings(payload: Mapping[str, Any], keys: tuple[str, ...]) -> list[str]:
    refs: list[str] = []
    for key in keys:
        text = _read_string(payload, key)
        if text:
            refs.append(text)
    return refs


def _read_stage_run_ref(payload: Mapping[str, Any], lease_or_receipt_refs: list[str]) -> str | None:
    explicit_ref = _read_first_string(payload, _ACCEPTED_STAGE_RUN_REF_FIELDS)
    if explicit_ref:
        return explicit_ref
    for ref in lease_or_receipt_refs:
        normalized = ref.replace("_", "-").lower()
        if any(marker in normalized for marker in _STAGE_RUN_REF_MARKERS):
            return ref
    return None


def _read_caller_role(payload: Mapping[str, Any], lease_or_receipt_refs: list[str]) -> str | None:
    explicit_role = _read_string(payload, _CALLER_ROLE_FIELD)
    if explicit_role:
        return explicit_role
    for ref in lease_or_receipt_refs:
        if _OWNER_CHAIN_DEFAULT_CALLER_REF_MARKER in ref.replace("_", "-").lower():
            return _OWNER_CHAIN_DEFAULT_CALLER_ROLE
    return None


__all__ = ["build_stage_transition_authority_boundary", "require_opl_default_stage_attempt"]
