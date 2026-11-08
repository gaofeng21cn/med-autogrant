from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.authoring_executor import build_freeze_execution_document
from med_autogrant.domain_runtime_parts.io import (
    _guard_workspace_output_identity,
    _write_revised_workspace_output,
)


def execute_freeze_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    execution_document = build_freeze_execution_document(
        document=self._load_workspace(input_path),
    )
    return self._write_authoring_execution_output(
        command="execute-freeze-pass",
        output_path=output_path,
        execution_document=execution_document,
        execution_key="freeze_execution",
        workspace_key="frozen_workspace",
    )


def _write_authoring_execution_output(
    self,
    *,
    command: str,
    output_path: str | Path,
    execution_document: dict[str, Any],
    execution_key: str,
    workspace_key: str,
) -> dict[str, Any]:
    resolved_output_path = Path(output_path).expanduser().resolve()
    workspace_document = execution_document[workspace_key]
    _guard_workspace_output_identity(
        resolved_output_path,
        workspace_document=workspace_document,
        draft_id=execution_document.get("draft_id"),
    )
    _write_revised_workspace_output(resolved_output_path, workspace_document)
    return {
        "ok": True,
        "command": command,
        "grant_run_id": execution_document["grant_run_id"],
        "workspace_id": execution_document["workspace_id"],
        "draft_id": execution_document.get("draft_id"),
        "lifecycle_stage": execution_document["lifecycle_stage"],
        "output_path": str(resolved_output_path),
        execution_key: execution_document[execution_key],
        workspace_key: workspace_document,
    }
