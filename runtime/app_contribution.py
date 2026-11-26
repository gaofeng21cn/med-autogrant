#!/usr/bin/env python3
"""Thin contribution handler for MAG's shared owner entry."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))


def _bootstrap_opl_client() -> None:
    try:
        import opl_client.helpers  # noqa: F401
        return
    except ImportError:
        pass

    candidates: list[Path] = []
    py_client_dir = os.environ.get("OPL_PYTHON_CLIENT_DIR", "").strip()
    if py_client_dir:
        base = Path(py_client_dir).expanduser()
        candidates.extend([base / "src", base])

    fw_root = os.environ.get("OPL_FRAMEWORK_ROOT", "").strip() or os.environ.get("OPL_OWNER_REPO_ROOT", "").strip()
    if fw_root:
        candidates.append(Path(fw_root).expanduser() / "sdks" / "python-client" / "src")

    opl_bin = os.environ.get("OPL_BIN", "").strip() or shutil.which("opl") or ""
    if opl_bin:
        try:
            resolved_bin = Path(opl_bin).expanduser().resolve()
            for parent in resolved_bin.parents:
                sdk_src = parent / "sdks" / "python-client" / "src"
                if (sdk_src / "opl_client" / "__init__.py").is_file():
                    candidates.append(sdk_src)
                    break
        except OSError:
            pass

    candidates.extend([
        _REPO_ROOT.parent / "one-person-lab" / "sdks" / "python-client" / "src",
        _REPO_ROOT.parent / ".worktrees" / "opl-v2" / "sdks" / "python-client" / "src",
    ])

    for candidate in candidates:
        if (candidate / "opl_client" / "__init__.py").is_file():
            resolved = str(candidate.resolve())
            if resolved not in sys.path:
                sys.path.insert(0, resolved)
            return


_bootstrap_opl_client()

try:
    from opl_client.helpers import read_stdin_json, write_json_stdout  # noqa: E402
except ImportError:
    def read_stdin_json() -> dict[str, object]:
        raw = sys.stdin.read().strip()
        if not raw:
            return {}
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise ValueError("Expected JSON object on stdin")
        return parsed

    def write_json_stdout(payload: dict[str, object]) -> None:
        sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")
        sys.stdout.flush()

from med_autogrant._opl_helpers.app_contribution import (  # noqa: E402
    AppContributionError,
    resolve_workspace_root,
)
from med_autogrant.app_contribution import (  # noqa: E402
    NOTE_ACTION,
    _selected_source,
    read_contribution,
    record_review,
)
from med_autogrant.workspace_types import WorkspaceError  # noqa: E402

_READ_REF_TO_VIEW = {
    "mag.workspace.v1#route": "route",
    "mag.workspace.v1#quality": "quality",
}


def main() -> int:
    cli_operation = sys.argv[1] if len(sys.argv) > 1 else None
    is_execute = cli_operation == "note"
    try:
        payload = read_stdin_json()
        is_envelope = (
            cli_operation is None
            and (
                payload.get("schema_version") == "opl-package-app-contribution-request.v1"
                or payload.get("operation") in ("read", "execute")
            )
        )
        if is_envelope and payload.get("operation") == "execute":
            is_execute = True

        try:
            root = resolve_workspace_root()
        except OSError as error:
            raise ValueError("请先选择已登记基金工作区。") from error
        if root is None:
            raise ValueError("请先选择已登记基金工作区。")

        if is_envelope:
            envelope_op = payload.get("operation")
            if envelope_op == "execute":
                action_id = payload.get("action_id") or payload.get("ref")
                if action_id != NOTE_ACTION:
                    raise ValueError(f"未知 MAG 审阅动作: {action_id!r}")
                raw_input = payload.get("payload")
                if not isinstance(raw_input, dict):
                    raw_input = payload.get("input") if isinstance(payload.get("input"), dict) else {}
                source = _selected_source(root, raw_input, "route")
                result = {
                    "state": "ready",
                    "result": record_review(
                        input_path=source,
                        **{
                            key: raw_input.get(key)
                            for key in ("workspace_id", "grant_run_id", "revision", "request_id", "note")
                        },
                    ),
                }
            elif envelope_op == "read":
                ref = payload.get("ref")
                view = _READ_REF_TO_VIEW.get(ref) if isinstance(ref, str) else None
                if view is None:
                    raise ValueError(f"未知 MAG 审阅视图: {ref!r}")
                raw_input = payload.get("input") if isinstance(payload.get("input"), dict) else {}
                result = read_contribution(root, raw_input, view)
            else:
                raise ValueError("未知 MAG 审阅操作。")
        else:
            operation = cli_operation or "route"
            if operation == "note":
                source = _selected_source(root, payload, "route")
                result = {
                    "state": "ready",
                    "result": record_review(
                        input_path=source,
                        **{
                            key: payload.get(key)
                            for key in ("workspace_id", "grant_run_id", "revision", "request_id", "note")
                        },
                    ),
                }
            elif operation in ("route", "quality"):
                result = read_contribution(root, payload, operation)
            else:
                raise ValueError("未知 MAG 审阅操作。")
    except (AppContributionError, WorkspaceError, OSError, ValueError, TypeError, KeyError) as error:
        if is_execute:
            result = {
                "schema_version": "opl-package-app-contribution-response.v1",
                "ok": False,
                "operation": "execute",
                "ref": NOTE_ACTION,
                "error": {"message": str(error)},
            }
        else:
            result = {"state": "unavailable", "reason": str(error)}
    write_json_stdout(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
