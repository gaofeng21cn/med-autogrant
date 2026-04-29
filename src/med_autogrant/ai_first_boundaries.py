from __future__ import annotations

from typing import Any


AI_REVIEWER_BACKED_OWNERS = frozenset(
    {
        "Codex CLI critique executor",
        "Hermes-native critique proof executor",
    }
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
    owner = _text(metadata.get("owner"))
    ai_backed = owner in AI_REVIEWER_BACKED_OWNERS
    return {
        "assessment_owner": "ai_reviewer_backed" if ai_backed else "projection_only",
        "ai_reviewer_required": not ai_backed,
        "review_artifact_ref": f"mentor_critiques::{critique_id}" if ai_backed and critique_id is not None else None,
        "review_owner": owner,
    }


def require_active_ai_backed_critique(document: dict[str, Any]) -> dict[str, Any]:
    provenance = active_critique_ai_review_provenance(document)
    if provenance["ai_reviewer_required"]:
        from med_autogrant.workspace_types import WorkspaceStateError

        raise WorkspaceStateError(
            "AI reviewer-backed critique is required before this mechanical quality/revision surface can proceed."
        )
    return provenance
