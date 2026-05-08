from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


PRODUCT_ENTRY_VERSION = 1
PRODUCT_ENTRY_KIND = "med_auto_grant_product_entry"
PRODUCT_ENTRY_MANIFEST_KIND = "med_auto_grant_product_entry_manifest"
PRODUCT_STATUS_KIND = "product_status"
TARGET_DOMAIN_ID = "med-autogrant"
SUPPORTED_ENTRY_MODES = ("direct", "opl-handoff")
GRANT_PROGRESS_PROJECTION_VERSION = 1
GRANT_PROGRESS_PROJECTION_KIND = "grant_progress"
GRANT_COCKPIT_KIND = "grant_cockpit"
GRANT_DIRECT_ENTRY_VERSION = 1
GRANT_DIRECT_ENTRY_KIND = "grant_direct_entry"
GRANT_USER_LOOP_VERSION = 1
GRANT_USER_LOOP_KIND = "grant_user_loop"
REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}


def _read_funding_call_from_summary(summary: Mapping[str, Any]) -> str:
    intake_snapshot = _require_mapping(summary, "intake_snapshot", context="summarize-workspace")
    return _require_nonempty_string_from_mapping(
        intake_snapshot,
        "funding_program",
        context="summarize-workspace.intake_snapshot",
    )


def _require_entry_mode(entry_mode: str) -> str:
    resolved_entry_mode = _require_nonempty_string(entry_mode, field_name="entry_mode")
    if resolved_entry_mode not in SUPPORTED_ENTRY_MODES:
        raise WorkspaceStateError(
            f"entry_mode 不支持: {resolved_entry_mode}。只允许 {', '.join(SUPPORTED_ENTRY_MODES)}。"
        )
    return resolved_entry_mode


def _require_mapping(payload: Mapping[str, Any], field_name: str, *, context: str) -> Mapping[str, Any]:
    value = payload.get(field_name)
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field_name}")
    return value


def _require_nonempty_string_from_mapping(payload: Mapping[str, Any], field_name: str, *, context: str) -> str:
    value = payload.get(field_name)
    return _require_nonempty_string(value, field_name=field_name, context=context)


def _require_nonempty_string(
    value: Any,
    *,
    field_name: str,
    context: str = "product entry",
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field_name}")
    return value.strip()


def _require_optional_string(value: Any, *, field_name: str) -> str | None:
    if value is None:
        return None
    return _require_nonempty_string(value, field_name=field_name)


def _optional_mapping(payload: Mapping[str, Any], field_name: str) -> Mapping[str, Any] | None:
    value = payload.get(field_name)
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"product entry 缺少合法字段: {field_name}")
    return value


def _optional_string_from_mapping(payload: Mapping[str, Any] | None, field_name: str) -> str | None:
    if not isinstance(payload, Mapping):
        return None
    value = payload.get(field_name)
    if value is None:
        return None
    return _require_nonempty_string(value, field_name=field_name)


def _read_nonempty_string_list(value: Any, *, context: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise WorkspaceStateError(f"{context} 缺少合法字段: workspace_alerts")
    return [item for item in value if isinstance(item, str) and item.strip()]


def _write_product_entry_output(output_path: Path, product_entry: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(product_entry, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 product entry 输出失败: {output_path}") from exc


def _require_matching_top_level_identity(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    *,
    context: str,
) -> None:
    for field_name in ("grant_run_id", "workspace_id", "draft_id", "lifecycle_stage", "input_path"):
        if left.get(field_name) != right.get(field_name):
            raise WorkspaceStateError(f"{context} 与当前 direct entry identity 不一致: {field_name}")


def _assert_entry_mode(
    payload: Mapping[str, Any],
    *,
    expected_entry_mode: str,
    context: str,
) -> None:
    resolved_entry_mode = _require_nonempty_string_from_mapping(
        payload,
        "entry_mode",
        context=context,
    )
    if resolved_entry_mode != expected_entry_mode:
        raise WorkspaceStateError(f"{context}.entry_mode 必须为 {expected_entry_mode}。")


__all__ = [name for name in globals() if not name.startswith("__")]
