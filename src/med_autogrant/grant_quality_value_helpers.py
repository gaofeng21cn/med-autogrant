from __future__ import annotations

import hashlib

from typing import Any, Iterable, Mapping


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
    seen: set[str] = set()
    ordered: list[str] = []
    for item in values:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


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
