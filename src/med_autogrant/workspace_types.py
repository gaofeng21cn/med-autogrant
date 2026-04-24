from __future__ import annotations

from dataclasses import dataclass
from typing import Any



class WorkspaceError(Exception):
    """Workspace 相关错误。"""


class WorkspaceFileError(WorkspaceError):
    """Workspace 文件读写错误。"""


class WorkspaceStateError(WorkspaceError):
    """Workspace 状态不满足运行时约束。"""

    def __init__(
        self,
        message: str,
        *,
        errors: list[ValidationIssue] | None = None,
        grant_run_id: str | None = None,
        workspace_id: str | None = None,
        lifecycle_stage: str | None = None,
    ) -> None:
        super().__init__(message)
        self.errors = list(errors or [])
        self.grant_run_id = grant_run_id
        self.workspace_id = workspace_id
        self.lifecycle_stage = lifecycle_stage


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    errors: list[ValidationIssue]

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def error_count(self) -> int:
        return len(self.errors)

    def to_dict(self, document: dict[str, Any] | None = None) -> dict[str, Any]:
        grant_run_id = None
        workspace_id = None
        lifecycle_stage = None
        if isinstance(document, dict):
            grant_run_id = document.get("grant_run_id")
            workspace_id = document.get("workspace_id")
            lifecycle_stage = document.get("lifecycle_stage")
        return {
            "ok": self.ok,
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
            "error_count": self.error_count,
            "errors": [
                {
                    "path": issue.path,
                    "message": issue.message,
                }
                for issue in self.errors
            ],
        }


@dataclass(frozen=True)
class WorkspaceContext:
    document: dict[str, Any]
    selected_direction: dict[str, Any]
    selected_question: dict[str, Any]
    active_argument_chain: dict[str, Any]
    active_fit_mapping: dict[str, Any]
    active_draft: dict[str, Any]
    active_revision_plan: dict[str, Any]
    active_critique: dict[str, Any]
    reviewed_revision_plan: dict[str, Any] | None


@dataclass(frozen=True)
class WorkspaceState:
    document: dict[str, Any]
    current_selection: dict[str, Any]
    selected_direction: dict[str, Any] | None
    selected_question: dict[str, Any] | None
    active_argument_chain: dict[str, Any] | None
    active_fit_mapping: dict[str, Any] | None
    active_draft: dict[str, Any] | None
    active_revision_plan: dict[str, Any] | None
    active_critique: dict[str, Any] | None
    reviewed_revision_plan: dict[str, Any] | None
