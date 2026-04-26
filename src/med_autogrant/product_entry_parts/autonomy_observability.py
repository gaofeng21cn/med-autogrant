from __future__ import annotations

from typing import Any, Mapping


def _text(value: object) -> str | None:
    text = str(value or "").strip()
    return text or None


def _mapping(value: object) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _bool(value: object) -> bool:
    return bool(value)


def _list(value: object) -> list[object]:
    return list(value) if isinstance(value, list | tuple) else []


def build_grant_autonomy_observability(
    *,
    task_lifecycle: Mapping[str, Any],
    runtime_inventory: Mapping[str, Any],
    grant_authoring_readiness: Mapping[str, Any],
    runtime_control: Mapping[str, Any],
    remaining_gaps: list[object],
) -> dict[str, Any]:
    checkpoint_summary = _mapping(task_lifecycle.get("checkpoint_summary"))
    runtime_binding = _mapping(runtime_inventory.get("workspace_binding"))
    semantic_closure = _mapping(runtime_control.get("semantic_closure"))
    task_status = _text(task_lifecycle.get("status")) or "unknown"
    runtime_health = _text(runtime_inventory.get("health_status")) or "unknown"
    blocking_gaps = _list(grant_authoring_readiness.get("blocking_gaps"))
    remaining_gap_count = len(remaining_gaps)
    observability = {
        "surface_kind": "grant_autonomy_observability",
        "schema_version": 1,
        "owner": "med-autogrant",
        "sli_summary": {
            "task_status": task_status,
            "runtime_health_status": runtime_health,
            "task_resumable": task_status in {"forward_progress", "resumable"},
            "workspace_bound": _text(runtime_binding.get("workspace_path")) is not None,
            "same_funding_call_locked": _text(semantic_closure.get("funding_call_lock")) is not None,
            "quality_closure_surface_ready": _text(semantic_closure.get("quality_closure_surface")) is not None,
            "submission_ready_gate_open": _bool(grant_authoring_readiness.get("fully_automatic")),
            "operator_assisted_ready": _bool(grant_authoring_readiness.get("usable_now")),
            "remaining_gaps_count": remaining_gap_count,
            "blocking_gaps_count": len(blocking_gaps),
        },
        "checkpoint_ref": {
            "status": _text(checkpoint_summary.get("status")) or task_status,
            "checkpoint_id": _text(checkpoint_summary.get("checkpoint_id")),
        },
        "attention_candidates": [],
    }
    attention_candidates: list[dict[str, Any]] = []
    if task_status == "blocked":
        attention_candidates.append(
            {
                "attention_type": "authoring_checkpoint_blocked",
                "severity": "high",
                "recommended_surface": "grant_user_loop",
            }
        )
    if runtime_health != "healthy":
        attention_candidates.append(
            {
                "attention_type": "managed_runtime_attention_required",
                "severity": "medium",
                "recommended_surface": "runtime_control",
            }
        )
    if remaining_gap_count or blocking_gaps:
        attention_candidates.append(
            {
                "attention_type": "open_authoring_or_export_gaps",
                "severity": "medium",
                "recommended_surface": "grant_authoring_readiness",
            }
        )
    observability["attention_candidates"] = attention_candidates
    return observability
