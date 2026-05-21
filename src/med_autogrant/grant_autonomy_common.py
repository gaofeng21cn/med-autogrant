from __future__ import annotations

from copy import deepcopy
from typing import Any

_CONTROLLER_STATUSES = {
    "submission_grade_candidate",
    "near_submission_candidate",
    "failed_closed",
}
_QUALITY_STATUSES = {
    "submission_grade_candidate",
    "near_submission_candidate",
    "not_ready",
}
_CONTROLLER_ACTIONS = {
    "continue_mainline",
    "stop_success",
    "rollback_upstream",
    "reselect_project_profile",
    "fail_closed",
}
_GATE_STATUSES = {
    "open",
    "passed",
    "blocked",
    "failed_closed",
}


def _normalized_string(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def _string_list(value: Any) -> list[str] | None:
    if not isinstance(value, list):
        return None
    normalized: list[str] = []
    for item in value:
        item_text = _normalized_string(item)
        if not item_text:
            return None
        normalized.append(item_text)
    return normalized


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for item in values:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _extract_mapping(payload: Any, *, preferred_keys: tuple[str, ...]) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    for key in preferred_keys:
        if key in payload:
            value = payload[key]
            if isinstance(value, dict):
                return deepcopy(value)
            return None
    return deepcopy(payload)
