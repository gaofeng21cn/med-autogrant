from __future__ import annotations

import hashlib
from typing import Any, Iterable, Mapping


_QUALITY_CONTROLLER_ACTIONS = {
    "continue_mainline",
    "rollback_upstream",
    "reselect_project_profile",
    "fail_closed",
}
REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}


def _ensure_mapping(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def _safe_int(value: Any) -> int | None:
    return value if isinstance(value, int) else None


def _nonempty_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None


def _read_active_draft_id(document: Mapping[str, Any]) -> str | None:
    selection = _ensure_mapping(document.get("current_selection")) or {}
    return _nonempty_string(selection.get("active_draft_id"))


def _read_nonempty_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = _nonempty_string(item)
        if text is not None:
            result.append(text)
    return result


def _read_nested_string_list(payload: Mapping[str, Any], parent_key: str, child_key: str) -> list[str]:
    parent = _ensure_mapping(payload.get(parent_key))
    if parent is None:
        return []
    return _read_nonempty_string_list(parent.get(child_key))


def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _flatten_to_strings(values: Iterable[Any]) -> list[str]:
    result: list[str] = []
    for item in values:
        if isinstance(item, list):
            result.extend(_flatten_to_strings(item))
            continue
        text = _nonempty_string(item)
        if text is not None:
            result.append(text)
    return result


def _stable_digest(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:12]


def _normalize_quality_controller_action(value: Any, *, fallback_action: str) -> str:
    action = _nonempty_string(value)
    if action in _QUALITY_CONTROLLER_ACTIONS:
        return action
    return fallback_action


def _optional_action_hint(value: Any) -> dict[str, Any] | None:
    action_hint = _ensure_mapping(value)
    if action_hint is None:
        return None
    action = _normalize_quality_controller_action(action_hint.get("action"), fallback_action="continue_mainline")
    summary = _nonempty_string(action_hint.get("summary"))
    source_surface = _nonempty_string(action_hint.get("source_surface"))
    if summary is None or source_surface is None:
        return None
    return {
        "action": action,
        "summary": summary,
        "target_stage": _nonempty_string(action_hint.get("target_stage")),
        "source_surface": source_surface,
    }
