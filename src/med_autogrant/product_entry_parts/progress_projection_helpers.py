from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import (
    _optional_mapping,
    _optional_string_from_mapping,
    _read_nonempty_string_list,
    _require_mapping,
    _require_nonempty_string_from_mapping,
)


def _read_blocking_issues(critique_summary: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(critique_summary, Mapping):
        return []
    blocking_issues = critique_summary.get("blocking_issues")
    if not isinstance(blocking_issues, list):
        return []
    return [item for item in blocking_issues if isinstance(item, str) and item.strip()]


def _read_projection_blockers(
    *,
    workspace_summary: Mapping[str, Any],
    critique_summary: Mapping[str, Any] | None,
) -> list[str]:
    critique_blockers = _read_blocking_issues(critique_summary)
    if critique_blockers:
        return critique_blockers

    blockers: list[str] = []
    intake_audit = _optional_mapping(workspace_summary, "grant_intake_audit")
    evidence_grounding = _optional_mapping(workspace_summary, "grant_evidence_grounding")
    if isinstance(intake_audit, Mapping):
        blockers.extend(_read_nonempty_string_list(intake_audit.get("blocking_gaps"), context="grant_intake_audit"))
    if isinstance(evidence_grounding, Mapping):
        blockers.extend(
            _read_nonempty_string_list(
                evidence_grounding.get("evidence_gaps"),
                context="grant_evidence_grounding",
            )
        )
    seen: set[str] = set()
    ordered: list[str] = []
    for blocker in blockers:
        if blocker not in seen:
            seen.add(blocker)
            ordered.append(blocker)
    return ordered


def _read_next_system_action(next_step: Mapping[str, Any]) -> str:
    actions = next_step.get("actions")
    if isinstance(actions, list):
        for item in actions:
            if isinstance(item, str) and item.strip():
                return item.strip()
    return _require_nonempty_string_from_mapping(
        next_step,
        "reason",
        context="stage-route-report.route.next_step",
    )


def _build_current_stage_summary(
    *,
    lifecycle_stage: str,
    checkpoint_status: str,
    next_step: Mapping[str, Any],
) -> str:
    if lifecycle_stage == "frozen" and checkpoint_status == "submission_frozen":
        reason = "送审前冻结 gate 已闭合，可保持当前阶段继续推进。"
    else:
        reason = _require_nonempty_string_from_mapping(
            next_step,
            "reason",
            context="stage-route-report.route.next_step",
        )
    return f"当前 grant 已进入 {lifecycle_stage} 阶段；{reason}"


def _build_author_decision_summary(next_step: Mapping[str, Any]) -> str | None:
    if not bool(next_step.get("requires_human_confirmation")):
        return None
    return _require_nonempty_string_from_mapping(
        next_step,
        "reason",
        context="stage-route-report.route.next_step",
    )


def _build_focus_payload(
    *,
    workspace_summary: Mapping[str, Any],
    critique_summary: Mapping[str, Any] | None,
) -> dict[str, Any]:
    intake_snapshot = _require_mapping(
        workspace_summary,
        "intake_snapshot",
        context="summarize-workspace",
    )
    project_profile = _require_mapping(
        workspace_summary,
        "project_profile",
        context="summarize-workspace",
    )
    selected_direction = _optional_mapping(workspace_summary, "selected_direction")
    selected_question = _optional_mapping(workspace_summary, "selected_question")
    active_draft = _optional_mapping(workspace_summary, "active_draft")
    active_critique = _optional_mapping(workspace_summary, "active_critique")
    critique_verdict = _optional_string_from_mapping(active_critique, "verdict")
    if isinstance(critique_summary, Mapping):
        critique_verdict = _optional_string_from_mapping(critique_summary, "verdict") or critique_verdict
    return {
        "applicant_name": _require_nonempty_string_from_mapping(
            intake_snapshot,
            "applicant_name",
            context="summarize-workspace.intake_snapshot",
        ),
        "funding_program": _require_nonempty_string_from_mapping(
            intake_snapshot,
            "funding_program",
            context="summarize-workspace.intake_snapshot",
        ),
        "project_profile_label": _require_nonempty_string_from_mapping(
            project_profile,
            "profile_label",
            context="summarize-workspace.project_profile",
        ),
        "template_label": _require_nonempty_string_from_mapping(
            project_profile,
            "template_label",
            context="summarize-workspace.project_profile",
        ),
        "critique_policy_id": _require_nonempty_string_from_mapping(
            project_profile,
            "critique_policy_id",
            context="summarize-workspace.project_profile",
        ),
        "selected_direction_title": _optional_string_from_mapping(selected_direction, "title"),
        "selected_question": _optional_string_from_mapping(selected_question, "core_question"),
        "active_draft_title": _optional_string_from_mapping(active_draft, "project_title"),
        "critique_verdict": critique_verdict,
    }


def _build_workspace_overview(
    *,
    workspace_summary: Mapping[str, Any],
    progress_projection: Mapping[str, Any],
    critique_summary: Mapping[str, Any] | None,
) -> dict[str, Any]:
    focus = _build_focus_payload(
        workspace_summary=workspace_summary,
        critique_summary=critique_summary,
    )
    return {
        "applicant_name": focus["applicant_name"],
        "funding_program": focus["funding_program"],
        "project_profile_label": focus["project_profile_label"],
        "template_label": focus["template_label"],
        "critique_policy_id": focus["critique_policy_id"],
        "lifecycle_stage": _require_nonempty_string_from_mapping(
            progress_projection,
            "current_stage",
            context="grant-progress.progress_projection",
        ),
        "checkpoint_status": _require_nonempty_string_from_mapping(
            progress_projection,
            "checkpoint_status",
            context="grant-progress.progress_projection",
        ),
        "selected_direction_title": focus["selected_direction_title"],
        "selected_question": focus["selected_question"],
        "active_draft_title": focus["active_draft_title"],
        "critique_verdict": focus["critique_verdict"],
    }


def _build_workspace_status(*, blockers: list[str], needs_author_decision: bool) -> str:
    if blockers or needs_author_decision:
        return "attention_required"
    return "on_track"


__all__ = [name for name in globals() if not name.startswith("__")]
