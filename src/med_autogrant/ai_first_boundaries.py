from __future__ import annotations

from typing import Any

from med_autogrant._opl_helpers.review_provenance import (
    DEFAULT_AI_REVIEWER_BACKED_OWNERS as AI_REVIEWER_BACKED_OWNERS,
    evaluate_independent_review_provenance,
    validate_independent_review_evidence,
)


def _text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None


def _find_by_id(items: object, id_field: str, value: str | None) -> dict[str, Any] | None:
    if value is None or not isinstance(items, list):
        return None
    for item in items:
        if isinstance(item, dict) and item.get(id_field) == value:
            return item
    return None


def _independent_review_evidence(
    *,
    metadata: dict[str, Any],
    critique_id: str | None,
) -> dict[str, Any] | None:
    return validate_independent_review_evidence(
        metadata.get("independent_review_evidence"),
        expected_review_attempt_ref=(
            f"mentor_critiques::{critique_id}" if critique_id is not None else None
        ),
    )


def active_critique_ai_review_provenance(document: dict[str, Any]) -> dict[str, Any]:
    current_selection = document.get("current_selection")
    active_revision_plan_id = (
        _text(current_selection.get("active_revision_plan_id"))
        if isinstance(current_selection, dict)
        else None
    )
    revision_plan = _find_by_id(document.get("revision_plans"), "revision_plan_id", active_revision_plan_id)
    critique_id = _text(revision_plan.get("critique_id")) if isinstance(revision_plan, dict) else None
    critique = _find_by_id(document.get("mentor_critiques"), "critique_id", critique_id)
    metadata = dict(critique.get("metadata") or {}) if isinstance(critique, dict) else {}
    return evaluate_independent_review_provenance(
        metadata=metadata,
        review_attempt_ref=(
            f"mentor_critiques::{critique_id}" if critique_id is not None else None
        ),
        allowed_owners=AI_REVIEWER_BACKED_OWNERS,
        blocker_reason="AI reviewer-backed critique with independent execution/review receipt refs is required.",
    )


def active_ai_backed_critique_quality_context(document: dict[str, Any]) -> dict[str, Any]:
    """Return review provenance without turning missing review into a progression gate."""
    return active_critique_ai_review_provenance(document)
