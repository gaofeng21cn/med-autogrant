from __future__ import annotations

from typing import Any

from med_autogrant.schema_loader import SchemaStore
from med_autogrant.workspace_types import WorkspaceStateError
from opl_framework.schema_validation import SchemaSubsetValidator


def validate_contract_schema(
    payload: dict[str, Any],
    *,
    schema_file: str,
    context: str,
    grant_run_id: str | None = None,
    workspace_id: str | None = None,
    lifecycle_stage: str | None = None,
) -> None:
    issues = SchemaSubsetValidator(SchemaStore()).validate(payload, schema_file)
    if not issues:
        return
    detail = "; ".join(f"{issue.path}: {issue.message}" for issue in issues[:5])
    if len(issues) > 5:
        detail = f"{detail}; 其余 {len(issues) - 5} 项略"
    raise WorkspaceStateError(
        f"{context} schema 校验失败: {detail}",
        errors=issues,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def validate_schema_payload(
    payload: dict[str, Any],
    *,
    schema_file: str,
    context: str,
) -> None:
    validate_contract_schema(
        payload,
        schema_file=schema_file,
        context=context,
    )
