from __future__ import annotations

from typing import Any, Mapping


_DEFAULT_EXECUTOR_KIND = "codex_cli"
_OPL_OWNER = "one-person-lab"


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
    has_lease_or_receipt = any(
        _read_string(payload, key)
        for key in (
            "attempt_lease_ref",
            "lease_ref",
            "receipt_ref",
            "stage_attempt_receipt_ref",
        )
    )

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

    return {
        "ok": True,
        "execution_boundary": {
            "surface_kind": "mag_opl_execution_boundary",
            "controller_id": controller_id,
            "runtime_owner": _OPL_OWNER,
            "required_default_executor_kind": _DEFAULT_EXECUTOR_KIND,
            "attempt_lease_or_receipt_observed": True,
            "mag_owns_durable_loop": False,
            "mag_owns_attempt_ledger": False,
            "allowed_return_shapes": [
                "domain_owner_receipt",
                "typed_blocker",
                "no_regression_evidence",
            ],
        },
    }


def _build_typed_blocker(*, controller_id: str, reason: str) -> dict[str, Any]:
    return {
        "surface_kind": "mag_opl_execution_boundary_typed_blocker",
        "controller_id": controller_id,
        "blocker_kind": reason,
        "typed_blocker_ref": f"typed-blocker:mag/{controller_id}/opl-default-stage-attempt-required",
        "required_runtime_owner": _OPL_OWNER,
        "required_default_executor_kind": _DEFAULT_EXECUTOR_KIND,
        "required_evidence": "OPL stage attempt lease or default executor receipt",
        "mag_owns_durable_loop": False,
        "mag_owns_attempt_ledger": False,
        "hermes_agent_boundary": "explicit_non_default_opl_executor_adapter_receipt_lane_only",
    }


def _read_string(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None


__all__ = ["require_opl_default_stage_attempt"]
