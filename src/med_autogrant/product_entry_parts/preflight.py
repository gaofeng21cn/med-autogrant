from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    REVIEW_CONTEXT_STAGES,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
    _require_optional_string,
)
from med_autogrant.public_cli import public_cli_command
from med_autogrant.workspace import load_workspace_document
from med_autogrant.workspace_validation import validate_workspace_document

from opl_harness_shared.product_entry_program_companions import (
    build_program_check,
    build_product_entry_preflight as _build_shared_product_entry_preflight,
)



class ProductEntryPreflightMixin:
    def build_product_entry_preflight(
        self,
        *,
        input_path: str | Path,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        document = load_workspace_document(resolved_input_path)
        validation = validate_workspace_document(document)
        current_selection = document.get("current_selection") if isinstance(document.get("current_selection"), Mapping) else {}
        draft_id = _require_optional_string(current_selection.get("active_draft_id"), field_name="draft_id")
        validate_command = public_cli_command(
            "validate-workspace", "--input", str(resolved_input_path), "--format", "json"
        )
        start_command = public_cli_command(
            "product-status", "--input", str(resolved_input_path), "--format", "json"
        )
        checks = [
            build_program_check(
                check_id="workspace_document_valid",
                title="Workspace Document Valid",
                status="pass" if validation.ok else "fail",
                blocking=True,
                summary=(
                    "workspace document schema 与 runtime constraints 均通过。"
                    if validation.ok
                    else "workspace document 仍有 schema 或 runtime constraint 问题。"
                ),
                command=validate_command,
            ),
            build_program_check(
                check_id="submission_ready_export_gate",
                title="Submission Ready Export Gate",
                status="pass" if document.get("lifecycle_stage") == "frozen" else "warn",
                blocking=False,
                summary=(
                    "当前 stage 已接近或进入 submission-ready export gate。"
                    if document.get("lifecycle_stage") == "frozen"
                    else "当前 stage 还未到 submission-ready export gate；这不阻止进入 product entry surface，但后续仍需继续主线推进。"
                ),
                command=public_cli_command(
                    "build-submission-ready-package",
                    "--input",
                    str(resolved_input_path),
                    "--output-dir",
                    "<output-dir>",
                    "--format",
                    "json",
                ),
            ),
        ]
        summary = (
            "当前 direct grant product entry surface 的前置检查已通过，可以先复核 workspace 与主线，再进入 OPL/App generated status target 或 domain-handler export。"
            if validation.ok
            else "当前 direct grant product entry surface 仍有 blocking preflight check；请先修复 workspace 或默认 runtime owner line，再进入 OPL/App generated status target 或 domain-handler export。"
        )
        product_entry_preflight = _build_shared_product_entry_preflight(
            summary=summary,
            recommended_check_command=validate_command,
            recommended_start_command=start_command,
            checks=checks,
        )
        return {
            "ok": True,
            "command": "product-preflight",
            "grant_run_id": _require_nonempty_string(document.get("grant_run_id"), field_name="grant_run_id"),
            "workspace_id": _require_nonempty_string(document.get("workspace_id"), field_name="workspace_id"),
            "draft_id": draft_id,
            "lifecycle_stage": _require_nonempty_string(document.get("lifecycle_stage"), field_name="lifecycle_stage"),
            "input_path": str(resolved_input_path),
            "product_entry_preflight": product_entry_preflight,
        }

    def _load_projection_context(
        self,
        *,
        input_path: str | Path,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        route_report = self._domain_entry.dispatch(
            {
                "command": "stage-route-report",
                "input_path": str(resolved_input_path),
            }
        )
        workspace_summary = self._domain_entry.dispatch(
            {
                "command": "summarize-workspace",
                "input_path": str(resolved_input_path),
            }
        )
        lifecycle_stage = _require_nonempty_string_from_mapping(
            route_report,
            "lifecycle_stage",
            context="stage-route-report",
        )
        critique_summary = None
        if lifecycle_stage in REVIEW_CONTEXT_STAGES:
            critique_summary = self._domain_entry.dispatch(
                {
                    "command": "critique-summary",
                    "input_path": str(resolved_input_path),
                }
            )
        return {
            "resolved_input_path": resolved_input_path,
            "route_report": route_report,
            "workspace_summary": workspace_summary,
            "critique_summary": critique_summary,
        }
