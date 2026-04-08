from __future__ import annotations

from typing import Any

from med_autogrant.stage_router import determine_next_step
from med_autogrant.workspace import (
    WorkspaceStateError,
    build_critique_summary,
    summarize_workspace_document,
    validate_workspace_document,
)


def build_stage_route_report(document: dict[str, Any]) -> dict[str, Any]:
    validation = validate_workspace_document(document)
    if not validation.ok:
        first = validation.errors[0]
        raise WorkspaceStateError(
            f"{first.path}: {first.message}",
            errors=validation.errors,
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    validation_payload = validation.to_dict(document)
    summary = summarize_workspace_document(document)
    next_step = determine_next_step(document)
    route: dict[str, Any] = {
        "validate_workspace": validation_payload,
        "summarize_workspace": summary,
        "next_step": next_step,
    }
    critique_summary: dict[str, Any] | None = None
    if document["lifecycle_stage"] in {"critique", "revision", "frozen"}:
        critique_summary = build_critique_summary(document)
        critique_summary["recommended_next_stage"] = next_step["recommended_stage"]
        route["critique_summary"] = critique_summary
    return {
        "ok": True,
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "lifecycle_stage": document["lifecycle_stage"],
        "route": route,
        "verification_checkpoint": build_verification_checkpoint(
            document=document,
            validation_payload=validation_payload,
            summary=summary,
            next_step=next_step,
            critique_summary=critique_summary,
        ),
    }


def build_verification_checkpoint(
    *,
    document: dict[str, Any],
    validation_payload: dict[str, Any],
    summary: dict[str, Any],
    next_step: dict[str, Any],
    critique_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    current_selection = summary.get("current_selection")
    active_draft = summary.get("active_draft")
    active_critique = summary.get("active_critique")
    forced_rollback_stage = next_step.get("forced_rollback_stage")
    if forced_rollback_stage is None and isinstance(critique_summary, dict):
        forced_rollback_stage = critique_summary.get("forced_rollback_stage")

    forced_rollback_reason = None
    if isinstance(critique_summary, dict):
        forced_rollback_reason = critique_summary.get("forced_rollback_reason")
    elif isinstance(active_critique, dict):
        forced_rollback_reason = active_critique.get("forced_rollback_reason")

    presubmission_frozen = bool(summary.get("gates", {}).get("presubmission_frozen"))
    if presubmission_frozen:
        checkpoint_status = "submission_frozen"
    elif forced_rollback_stage:
        checkpoint_status = "rollback_required"
    elif is_freeze_ready_checkpoint(
        summary=summary,
        next_step=next_step,
        critique_summary=critique_summary,
    ):
        checkpoint_status = "freeze_ready"
    else:
        checkpoint_status = "forward_progress"

    return {
        "checkpoint_status": checkpoint_status,
        "validation_ok": bool(validation_payload.get("ok")),
        "identity": {
            "grant_run_id": document["grant_run_id"],
            "workspace_id": document["workspace_id"],
            "draft_id": active_draft.get("id") if isinstance(active_draft, dict) else None,
            "active_revision_plan_id": (
                current_selection.get("active_revision_plan_id")
                if isinstance(current_selection, dict)
                else None
            ),
            "reviewed_revision_plan_id": (
                critique_summary.get("reviewed_revision_plan_id")
                if isinstance(critique_summary, dict)
                else None
            ),
        },
        "route_alignment": {
            "lifecycle_stage": document["lifecycle_stage"],
            "recommended_next_stage": next_step["recommended_stage"],
            "forced_rollback_stage": forced_rollback_stage,
            "forced_rollback_reason": forced_rollback_reason,
            "presubmission_frozen": presubmission_frozen,
        },
        "review_checkpoint": {
            "critique_id": critique_summary.get("critique_id") if isinstance(critique_summary, dict) else None,
            "reviewed_revision_evidence": summary.get("reviewed_revision_evidence"),
            "blocking_issue_count": (
                len(critique_summary.get("blocking_issues", []))
                if isinstance(critique_summary, dict)
                else 0
            ),
        },
    }


def is_freeze_ready_checkpoint(
    *,
    summary: dict[str, Any],
    next_step: dict[str, Any],
    critique_summary: dict[str, Any] | None,
) -> bool:
    if not isinstance(critique_summary, dict):
        return False

    if critique_summary.get("verdict") != "ready_for_submission":
        return False

    if bool(summary.get("gates", {}).get("presubmission_frozen")):
        return False

    return next_step.get("recommended_stage") == "frozen"
