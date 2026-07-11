from __future__ import annotations

from typing import Any


AI_REVIEWER_BACKED_OWNERS = frozenset(
    {
        "Codex CLI critique executor",
        "OPL executor client critique receipt owner",
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


def _independent_review_evidence(
    *,
    metadata: dict[str, Any],
    critique_id: str | None,
) -> dict[str, Any] | None:
    evidence = metadata.get("independent_review_evidence")
    if not isinstance(evidence, dict):
        return None
    normalized = {
        "execution_attempt_ref": _text(evidence.get("execution_attempt_ref")),
        "review_attempt_ref": _text(evidence.get("review_attempt_ref")),
        "review_receipt_ref": _text(evidence.get("review_receipt_ref")),
        "no_shared_context_verified": evidence.get("no_shared_context_verified") is True,
        "reviewer_owner": _text(evidence.get("reviewer_owner")),
        "reviewer_agent_ref": _text(evidence.get("reviewer_agent_ref")),
    }
    if normalized["review_attempt_ref"] != (
        f"mentor_critiques::{critique_id}" if critique_id is not None else None
    ):
        return None
    if not normalized["no_shared_context_verified"]:
        return None
    required_refs = (
        normalized["execution_attempt_ref"],
        normalized["review_attempt_ref"],
        normalized["review_receipt_ref"],
    )
    if any(ref is None for ref in required_refs):
        return None
    if normalized["execution_attempt_ref"] == normalized["review_attempt_ref"]:
        return None
    if normalized["reviewer_owner"] is None and normalized["reviewer_agent_ref"] is None:
        return None
    return normalized


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
    owner_known = owner in AI_REVIEWER_BACKED_OWNERS
    independent_evidence = _independent_review_evidence(metadata=metadata, critique_id=critique_id)
    reviewer_owner = (
        independent_evidence.get("reviewer_owner") if independent_evidence is not None else None
    )
    reviewer_identity_verified = (
        reviewer_owner in AI_REVIEWER_BACKED_OWNERS
        or (
            independent_evidence is not None
            and independent_evidence.get("reviewer_agent_ref") is not None
        )
    )
    ai_backed = owner_known and independent_evidence is not None and reviewer_identity_verified
    blocker_reason = None
    if not ai_backed:
        blocker_reason = "AI reviewer-backed critique with independent execution/review receipt refs is required."
    return {
        "assessment_owner": "ai_reviewer_backed" if ai_backed else "projection_only",
        "ai_reviewer_required": not ai_backed,
        "review_artifact_ref": f"mentor_critiques::{critique_id}" if ai_backed and critique_id is not None else None,
        "review_owner": owner,
        "independent_review_evidence": independent_evidence if ai_backed else None,
        "ai_reviewer_blocker_reason": blocker_reason,
    }


def require_active_ai_backed_critique(document: dict[str, Any]) -> dict[str, Any]:
    provenance = active_critique_ai_review_provenance(document)
    if provenance["ai_reviewer_required"]:
        from med_autogrant.workspace_types import WorkspaceStateError

        raise WorkspaceStateError(
            "AI reviewer-backed critique is required before this mechanical quality/revision surface can proceed."
        )
    return provenance
