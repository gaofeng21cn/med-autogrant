from __future__ import annotations

from typing import Any

from med_autogrant.workspace_types import ValidationIssue


def _index_objects(
    items: Any,
    key_name: str,
    scope_name: str,
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    if not isinstance(items, list):
        return indexed
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        key = item.get(key_name)
        if not isinstance(key, str) or not key:
            continue
        if key in indexed:
            issues.append(
                ValidationIssue(
                    path=f"{scope_name}[{index}].{key_name}",
                    message=f"{key_name} 不能重复。",
                )
            )
            continue
        indexed[key] = item
    return indexed

