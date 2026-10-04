from __future__ import annotations

from copy import deepcopy
from typing import Any

from med_autogrant.authoring_executor_parts import (
    _finalize_execution_workspace,
    _fresh_metadata,
)
from med_autogrant.workspace_projection_parts import _build_workspace_state
from med_autogrant.workspace_types import WorkspaceStateError
from med_autogrant.workspace_validation import validate_workspace_document


def build_freeze_execution_document(
    *,
    document: dict[str, Any],
) -> dict[str, Any]:
    validation = validate_workspace_document(document)
    if not validation.ok:
        first_issue = validation.errors[0]
        raise WorkspaceStateError(
            f"{first_issue.path}: {first_issue.message}",
            errors=validation.errors,
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    state = _build_workspace_state(document)
    active_critique = state.active_critique
    active_revision_plan = state.active_revision_plan
    active_draft = state.active_draft
    if active_critique is None or active_revision_plan is None or active_draft is None:
        raise WorkspaceStateError("freeze pass 需要 critique / revision / draft 上下文。")
    if active_critique.get("verdict") != "ready_for_submission":
        raise WorkspaceStateError("freeze pass 只允许从 verdict=ready_for_submission 的 workspace 进入。")
    if active_revision_plan.get("execution_status") != "completed":
        raise WorkspaceStateError("freeze pass 要求 active RevisionPlan.execution_status=completed。")
    if active_draft.get("status") not in {"revised", "frozen"}:
        raise WorkspaceStateError("freeze pass 要求激活草稿已处于 revised 或 frozen。")

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "frozen"
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": True,
        "fit_alignment_frozen": True,
        "outline_frozen": True,
        "presubmission_frozen": True,
    }
    for draft in next_workspace.get("application_drafts", []):
        if isinstance(draft, dict) and draft.get("draft_id") == active_draft["draft_id"]:
            draft["metadata"] = _fresh_metadata(document)
            draft["status"] = "frozen"
    next_workspace = _finalize_execution_workspace(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": active_draft["draft_id"],
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "freeze_execution": {
            "executor": {
                "kind": "deterministic_domain_logic",
                "model": None,
                "reasoning_effort": None,
            },
            "draft_id": active_draft["draft_id"],
            "revision_plan_id": active_revision_plan["revision_plan_id"],
            "critique_id": active_critique["critique_id"],
        },
        "frozen_workspace": next_workspace,
    }
