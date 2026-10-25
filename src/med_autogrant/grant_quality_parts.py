from __future__ import annotations

# Keep the historical module-level names importable. Consumers currently bind
# private helpers from this facade, including during test monkeypatch setup.
import hashlib
from typing import Any, Iterable, Mapping

from med_autogrant.workspace_surface_builders import build_critique_summary
from med_autogrant.workspace_types import WorkspaceStateError

from med_autogrant.grant_quality_support.evidence_supply import (
    _build_evidence_supply_queue,
    _build_evidence_supply_queue_item,
    _build_evidence_supply_progress,
    _build_evidence_supply_gap_progress_entry,
    _build_evidence_supply_map,
    _build_funding_profile_mismatch_gap,
    _collect_supply_actions,
    _evaluate_family_compatibility_mismatch_reason,
    _resolve_controller_action_hint,
    _resolve_supply_delta,
)
from med_autogrant.grant_quality_support.issue_closure import (
    _build_issue_closure_progress_entries,
    _build_issue_closure_progress_entry,
    _open_issue_lineage_map,
    _resolve_issue_closure_delta,
)
from med_autogrant.grant_quality_support.primitives import (
    REVIEW_CONTEXT_STAGES,
    _QUALITY_CONTROLLER_ACTIONS,
    _dedupe_preserve_order,
    _ensure_mapping,
    _flatten_to_strings,
    _nonempty_string,
    _normalize_quality_controller_action,
    _optional_action_hint,
    _read_active_draft_id,
    _read_nested_string_list,
    _read_nonempty_string_list,
    _safe_int,
    _stable_digest,
)


def _read_critique_summary(document: dict[str, Any]) -> dict[str, Any] | None:
    lifecycle_stage = _nonempty_string(document.get("lifecycle_stage"))
    if lifecycle_stage not in REVIEW_CONTEXT_STAGES:
        return None
    try:
        return build_critique_summary(document)
    except WorkspaceStateError:
        return None
