#!/usr/bin/env python3
"""Thin carrier adapter for MAG's shared owner entry."""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from opl_framework.app_contribution import (
    AppContributionError,
    read_stdin_json,
    resolve_workspace_root,
    write_json_stdout,
)
from med_autogrant.app_contribution import NOTE_ACTION, _selected_source, read_contribution, record_review
from med_autogrant.workspace_types import WorkspaceError


def main() -> int:
    operation = sys.argv[1] if len(sys.argv) > 1 else "route"
    try:
        try:
            root = resolve_workspace_root()
        except OSError as error:
            raise ValueError("请先选择已登记基金工作区。") from error
        if root is None:
            raise ValueError("请先选择已登记基金工作区。")
        value = read_stdin_json()
        if operation == "note":
            source = _selected_source(root, value, "route")
            result = {"state": "ready", "result": record_review(input_path=source, **{
                key: value.get(key) for key in ("workspace_id", "grant_run_id", "revision", "request_id", "note")})}
        elif operation in ("route", "quality"):
            result = read_contribution(root, value, operation)
        else:
            raise ValueError("未知 MAG 审阅操作。")
    except (AppContributionError, WorkspaceError, OSError, ValueError, TypeError, KeyError) as error:
        result = {"state": "unavailable", "reason": str(error)}
        if operation == "note":
            result = {"schema_version": "opl-package-app-contribution-response.v1", "ok": False,
                      "operation": "execute", "ref": NOTE_ACTION, "error": {"message": str(error)}}
    write_json_stdout(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
