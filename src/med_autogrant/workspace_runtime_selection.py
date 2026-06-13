from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from med_autogrant.workspace_runtime_policy import _WorkspaceRuntimeRequirements
from med_autogrant.workspace_types import ValidationIssue


@dataclass(frozen=True)
class _WorkspaceRuntimeSelection:
    selected_direction_id: Any
    selected_question_id: Any
    active_fit_mapping_id: Any
    active_draft_id: Any
    active_revision_plan_id: Any
    selected_direction: dict[str, Any] | None
    selected_question: dict[str, Any] | None


def _resolve_runtime_selection(
    document: dict[str, Any],
    *,
    stage: Any,
    requirements: _WorkspaceRuntimeRequirements,
    directions: dict[str, dict[str, Any]],
    questions: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> _WorkspaceRuntimeSelection:
    selection = document.get("current_selection", {})
    selected_direction_id = selection.get("selected_direction_id")
    selected_question_id = selection.get("selected_question_id")
    active_fit_mapping_id = selection.get("active_fit_mapping_id")
    active_draft_id = selection.get("active_draft_id")
    active_revision_plan_id = selection.get("active_revision_plan_id")

    _validate_direction_count(document, requirements=requirements, issues=issues)
    selected_direction = _resolve_selected_direction(
        stage=stage,
        requirements=requirements,
        selected_direction_id=selected_direction_id,
        directions=directions,
        selected_direction_count=_selected_direction_count(document),
        issues=issues,
    )
    selected_question = _resolve_selected_question(
        stage=stage,
        requirements=requirements,
        selected_direction=selected_direction,
        selected_question_id=selected_question_id,
        questions=questions,
        issues=issues,
    )

    return _WorkspaceRuntimeSelection(
        selected_direction_id=selected_direction_id,
        selected_question_id=selected_question_id,
        active_fit_mapping_id=active_fit_mapping_id,
        active_draft_id=active_draft_id,
        active_revision_plan_id=active_revision_plan_id,
        selected_direction=selected_direction,
        selected_question=selected_question,
    )


def _selected_direction_count(document: dict[str, Any]) -> int:
    return sum(
        1
        for item in document.get("direction_hypotheses", [])
        if isinstance(item, dict) and item.get("decision_status") == "selected"
    )


def _validate_direction_count(
    document: dict[str, Any],
    *,
    requirements: _WorkspaceRuntimeRequirements,
    issues: list[ValidationIssue],
) -> None:
    if not requirements.direction_count:
        return
    direction_count = len(document.get("direction_hypotheses", []))
    if direction_count < 2 or direction_count > 5:
        issues.append(
            ValidationIssue(
                path="direction_hypotheses",
                message="P2.A 方向阶段必须保留 2 到 5 个 DirectionHypothesis。",
            )
        )


def _resolve_selected_direction(
    *,
    stage: Any,
    requirements: _WorkspaceRuntimeRequirements,
    selected_direction_id: Any,
    directions: dict[str, dict[str, Any]],
    selected_direction_count: int,
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    if requirements.direction and selected_direction_count != 1:
        issues.append(
            ValidationIssue(
                path="direction_hypotheses",
                message="必须且只能有一个 decision_status=selected 的 DirectionHypothesis。",
            )
        )

    selected_direction = directions.get(selected_direction_id) if isinstance(selected_direction_id, str) else None
    if requirements.direction and selected_direction_id is None:
        issues.append(
            ValidationIssue(
                path="current_selection.selected_direction_id",
                message=f"{stage} 阶段必须显式绑定当前 DirectionHypothesis。",
            )
        )
    elif selected_direction_id is not None and selected_direction is None:
        issues.append(
            ValidationIssue(
                path="current_selection.selected_direction_id",
                message="未找到对应的 DirectionHypothesis。",
            )
        )
    elif selected_direction is not None and selected_direction.get("decision_status") != "selected":
        issues.append(
            ValidationIssue(
                path="current_selection.selected_direction_id",
                message="当前选中方向必须处于 selected 状态。",
            )
        )
    return selected_direction


def _resolve_selected_question(
    *,
    stage: Any,
    requirements: _WorkspaceRuntimeRequirements,
    selected_direction: dict[str, Any] | None,
    selected_question_id: Any,
    questions: dict[str, dict[str, Any]],
    issues: list[ValidationIssue],
) -> dict[str, Any] | None:
    selected_question = questions.get(selected_question_id) if isinstance(selected_question_id, str) else None
    if requirements.question and selected_question_id is None:
        issues.append(
            ValidationIssue(
                path="current_selection.selected_question_id",
                message=f"{stage} 阶段必须显式绑定当前 ScientificQuestionCard。",
            )
        )
    elif selected_question_id is not None and selected_question is None:
        issues.append(
            ValidationIssue(
                path="current_selection.selected_question_id",
                message="未找到对应的 ScientificQuestionCard。",
            )
        )
    elif (
        selected_direction is not None
        and selected_question is not None
        and selected_question.get("parent_direction_id") != selected_direction.get("direction_id")
    ):
        issues.append(
            ValidationIssue(
                path="current_selection.selected_question_id",
                message="当前选中问题不属于当前选中方向。",
            )
        )
    return selected_question


__all__ = [name for name in globals() if name.startswith("_") and not name.startswith("__")]
