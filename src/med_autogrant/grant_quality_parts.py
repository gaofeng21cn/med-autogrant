from __future__ import annotations

import hashlib
from typing import Any, Iterable, Mapping

from med_autogrant.workspace import WorkspaceStateError, build_critique_summary

_QUALITY_CONTROLLER_ACTIONS = {
    "continue_mainline",
    "rollback_upstream",
    "reselect_project_profile",
    "fail_closed",
}
REVIEW_CONTEXT_STAGES = {"critique", "revision", "frozen"}

def _build_evidence_supply_queue(tracked_issues: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped_issues: dict[str, list[dict[str, Any]]] = {}
    ordered_gap_ids: list[str] = []
    for tracked_issue in tracked_issues:
        issue = dict(tracked_issue)
        gap_id = _nonempty_string(issue.get("lineage_id")) or _nonempty_string(issue.get("issue_id"))
        if gap_id is None:
            continue
        if gap_id not in grouped_issues:
            grouped_issues[gap_id] = []
            ordered_gap_ids.append(gap_id)
        grouped_issues[gap_id].append(issue)
    return [
        _build_evidence_supply_queue_item(
            gap_id=gap_id,
            issues=grouped_issues[gap_id],
        )
        for gap_id in ordered_gap_ids
    ]

def _build_funding_profile_mismatch_gap(document: dict[str, Any]) -> dict[str, Any] | None:
    project_profile = _ensure_mapping(document.get("project_profile"))
    if project_profile is None:
        return None
    funding_brief = _ensure_mapping(document.get("funding_opportunity_brief"))
    if funding_brief is None:
        return None
    family_grammar = _ensure_mapping(project_profile.get("grant_family_grammar"))
    if family_grammar is None:
        family_grammar = _ensure_mapping(project_profile.get("family_grammar_trace"))
    if family_grammar is None:
        return None
    compatibility_hooks = family_grammar.get("family_compatibility_hooks")
    if not isinstance(compatibility_hooks, list) or not compatibility_hooks:
        return None

    mismatch_reasons: list[str] = []
    linked_issue_ids: list[str] = []
    for item in compatibility_hooks:
        hook = _ensure_mapping(item)
        if hook is None:
            continue
        mismatch_reason = _evaluate_family_compatibility_mismatch_reason(
            funding_brief=funding_brief,
            hook=hook,
        )
        if mismatch_reason is None:
            continue
        mismatch_reasons.append(mismatch_reason)
        rule_id = _nonempty_string(hook.get("rule_id"))
        if rule_id is not None:
            linked_issue_ids.append(f"funding_profile_mismatch:{rule_id}")

    if not mismatch_reasons:
        return None

    workspace_id = _nonempty_string(document.get("workspace_id")) or "workspace"
    family_id = _nonempty_string(family_grammar.get("family_id")) or "family"
    profile_id = _nonempty_string(project_profile.get("profile_id"))
    brief_id = _nonempty_string(funding_brief.get("brief_id"))
    required_input_ids = _dedupe_preserve_order(
        item
        for item in (profile_id, brief_id, workspace_id)
        if item is not None
    )
    return {
        "gap_id": f"funding_profile_mismatch:{workspace_id}:{family_id}",
        "gap_kind": "funding_profile_mismatch",
        "gap_summary": "当前 funding opportunity 与已选 family 不兼容。",
        "supply_status": "reselection_required",
        "controller_action_hint": {
            "action": "reselect_project_profile",
            "summary": "重选兼容的 funding / family 组合。",
            "target_stage": None,
            "source_surface": "grant_quality",
        },
        "required_input_ids": required_input_ids,
        "linked_issue_ids": _dedupe_preserve_order(linked_issue_ids),
        "linked_issue_summaries": _dedupe_preserve_order(mismatch_reasons),
        "blocking_reasons": _dedupe_preserve_order(mismatch_reasons),
        "supply_actions": [],
        "evidence_refs": [],
        "source_surfaces": ["grant_quality"],
    }

def _evaluate_family_compatibility_mismatch_reason(
    *,
    funding_brief: dict[str, Any],
    hook: dict[str, Any],
) -> str | None:
    field = _nonempty_string(hook.get("opportunity_field"))
    rule_id = _nonempty_string(hook.get("rule_id")) or "unknown_rule"
    allowed_values = _read_nonempty_string_list(hook.get("allowed_values"))
    if field is None or not allowed_values:
        return None
    observed = funding_brief.get(field)
    if isinstance(observed, list):
        normalized_observed = [item for item in (_nonempty_string(value) for value in observed) if item is not None]
        matched = any(item in allowed_values for item in normalized_observed)
        observed_payload = ", ".join(normalized_observed) if normalized_observed else "missing"
    else:
        observed_value = _nonempty_string(observed)
        matched = observed_value in allowed_values
        observed_payload = observed_value or "missing"
    if matched:
        return None
    expected_payload = ", ".join(allowed_values)
    return f"{rule_id}: funding_opportunity_brief.{field}={observed_payload}，不满足 family 允许值 {expected_payload}。"

def _build_evidence_supply_queue_item(*, gap_id: str, issues: list[dict[str, Any]]) -> dict[str, Any]:
    severities = _dedupe_preserve_order(
        severity
        for issue in issues
        for severity in [_nonempty_string(issue.get("severity"))]
        if severity is not None
    )
    if severities == ["hard"]:
        gap_kind = "hard_blocker"
    elif severities == ["gap"]:
        gap_kind = "evidence_gap"
    else:
        gap_kind = "mixed_gap"

    issue_summaries = _dedupe_preserve_order(
        summary
        for issue in issues
        for summary in [_nonempty_string(issue.get("summary"))]
        if summary is not None
    )
    linked_issue_ids = _dedupe_preserve_order(
        issue_id
        for issue in issues
        for issue_id in [_nonempty_string(issue.get("issue_id"))]
        if issue_id is not None
    )
    blocking_reasons = _dedupe_preserve_order(
        reason
        for issue in issues
        for reason in [_nonempty_string(issue.get("blocking_reason"))]
        if reason is not None
    )
    source_surfaces = _dedupe_preserve_order(
        source_surface
        for issue in issues
        for source_surface in [_nonempty_string(issue.get("source_surface"))]
        if source_surface is not None
    )
    closure_statuses = _dedupe_preserve_order(
        closure_status
        for issue in issues
        for closure_status in [_nonempty_string(issue.get("closure_status"))]
        if closure_status is not None
    )
    if closure_statuses == ["blocked"]:
        supply_status = "blocked"
    elif closure_statuses == ["evidence_required"]:
        supply_status = "evidence_required"
    else:
        supply_status = "mixed"

    required_input_ids: list[str] = []
    evidence_refs: list[str] = []
    supply_actions = _collect_supply_actions(
        issues=issues,
        required_input_ids=required_input_ids,
        evidence_refs=evidence_refs,
    )
    required_input_ids = _dedupe_preserve_order(required_input_ids)
    evidence_refs = _dedupe_preserve_order(evidence_refs)
    controller_action_hint = _resolve_controller_action_hint(issues)
    if not supply_actions:
        supply_actions = [
            {
                "obligation_id": f"{gap_id}:fallback-action",
                "summary": controller_action_hint["summary"],
                "required_input_ids": list(required_input_ids),
                "evidence_refs": list(evidence_refs),
                "satisfaction_criteria": None,
                "source_surface": controller_action_hint["source_surface"],
            }
        ]

    return {
        "gap_id": gap_id,
        "gap_kind": gap_kind,
        "gap_summary": issue_summaries[0] if issue_summaries else gap_id,
        "supply_status": supply_status,
        "controller_action_hint": controller_action_hint,
        "required_input_ids": required_input_ids,
        "linked_issue_ids": linked_issue_ids,
        "linked_issue_summaries": issue_summaries,
        "blocking_reasons": blocking_reasons,
        "supply_actions": supply_actions,
        "evidence_refs": evidence_refs,
        "source_surfaces": source_surfaces,
    }

def _collect_supply_actions(
    *,
    issues: list[dict[str, Any]],
    required_input_ids: list[str],
    evidence_refs: list[str],
) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    seen_action_ids: set[str] = set()
    for issue in issues:
        lineage_basis = _ensure_mapping(issue.get("lineage_basis")) or {}
        required_input_ids.extend(_read_nonempty_string_list(lineage_basis.get("required_input_ids")))
        obligations = issue.get("evidence_obligations")
        if not isinstance(obligations, list):
            continue
        for obligation in obligations:
            obligation_payload = _ensure_mapping(obligation)
            if obligation_payload is None:
                continue
            obligation_id = _nonempty_string(obligation_payload.get("obligation_id"))
            if obligation_id is None or obligation_id in seen_action_ids:
                continue
            seen_action_ids.add(obligation_id)
            obligation_required_inputs = _read_nonempty_string_list(obligation_payload.get("required_input_ids"))
            obligation_evidence_refs = _read_nonempty_string_list(obligation_payload.get("evidence_refs"))
            required_input_ids.extend(obligation_required_inputs)
            evidence_refs.extend(obligation_evidence_refs)
            actions.append(
                {
                    "obligation_id": obligation_id,
                    "summary": _nonempty_string(obligation_payload.get("summary")) or obligation_id,
                    "required_input_ids": obligation_required_inputs,
                    "evidence_refs": obligation_evidence_refs,
                    "satisfaction_criteria": _nonempty_string(obligation_payload.get("satisfaction_criteria")),
                    "source_surface": _nonempty_string(obligation_payload.get("source_surface")) or "grant_quality",
                }
            )
    return actions

def _resolve_controller_action_hint(issues: list[dict[str, Any]]) -> dict[str, Any]:
    prioritized_issues = sorted(
        issues,
        key=lambda item: 0 if _nonempty_string(item.get("severity")) == "hard" else 1,
    )
    for issue in prioritized_issues:
        action_hint = _ensure_mapping(issue.get("recommended_closure_action"))
        if action_hint is None:
            continue
        summary = _nonempty_string(action_hint.get("summary")) or _nonempty_string(issue.get("summary"))
        source_surface = _nonempty_string(action_hint.get("source_surface")) or _nonempty_string(issue.get("source_surface"))
        action = _normalize_quality_controller_action(
            action_hint.get("action"),
            fallback_action="rollback_upstream" if _nonempty_string(issue.get("severity")) == "hard" else "continue_mainline",
        )
        if summary is None or source_surface is None:
            continue
        return {
            "action": action,
            "summary": summary,
            "target_stage": _nonempty_string(action_hint.get("target_stage")),
            "source_surface": source_surface,
        }
    fallback_issue = prioritized_issues[0] if prioritized_issues else {}
    return {
        "action": "continue_mainline",
        "summary": _nonempty_string(fallback_issue.get("summary")) or "补齐证据供给项。",
        "target_stage": _nonempty_string(fallback_issue.get("rollback_stage")),
        "source_surface": _nonempty_string(fallback_issue.get("source_surface")) or "grant_quality",
    }

def _normalize_quality_controller_action(value: Any, *, fallback_action: str) -> str:
    action = _nonempty_string(value)
    if action in _QUALITY_CONTROLLER_ACTIONS:
        return action
    return fallback_action

def _build_evidence_supply_progress(
    *,
    previous_queue: list[dict[str, Any]],
    current_queue: list[dict[str, Any]],
) -> dict[str, Any]:
    previous_gap_map = _build_evidence_supply_map(previous_queue)
    current_gap_map = _build_evidence_supply_map(current_queue)
    closed_gap_ids = [gap_id for gap_id in previous_gap_map if gap_id not in current_gap_map]
    remaining_gap_ids = [gap_id for gap_id in previous_gap_map if gap_id in current_gap_map]
    new_gap_ids = [gap_id for gap_id in current_gap_map if gap_id not in previous_gap_map]
    ordered_gap_ids = list(previous_gap_map.keys())
    ordered_gap_ids.extend(gap_id for gap_id in current_gap_map if gap_id not in previous_gap_map)
    return {
        "closed_gaps": closed_gap_ids,
        "remaining_open_gaps": remaining_gap_ids,
        "newly_opened_gaps": new_gap_ids,
        "gap_progress": [
            _build_evidence_supply_gap_progress_entry(
                gap_id=gap_id,
                previous_gap=previous_gap_map.get(gap_id),
                current_gap=current_gap_map.get(gap_id),
            )
            for gap_id in ordered_gap_ids
        ],
    }

def _build_evidence_supply_map(queue: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        gap_id: dict(item)
        for item in queue
        for gap_id in [_nonempty_string(item.get("gap_id"))]
        if gap_id is not None
    }

def _build_evidence_supply_gap_progress_entry(
    *,
    gap_id: str,
    previous_gap: dict[str, Any] | None,
    current_gap: dict[str, Any] | None,
) -> dict[str, Any]:
    if previous_gap is not None and current_gap is None:
        transition = "closed"
        supply_delta = "supply_closed"
    elif previous_gap is None and current_gap is not None:
        transition = "newly_opened"
        supply_delta = "new_gap_opened"
    else:
        transition = "still_open"
        supply_delta = _resolve_supply_delta(
            previous_supply_status=_nonempty_string((previous_gap or {}).get("supply_status")),
            current_supply_status=_nonempty_string((current_gap or {}).get("supply_status")),
            previous_required_input_ids=_read_nonempty_string_list((previous_gap or {}).get("required_input_ids")),
            current_required_input_ids=_read_nonempty_string_list((current_gap or {}).get("required_input_ids")),
        )

    return {
        "gap_id": gap_id,
        "transition": transition,
        "previous_gap_kind": _nonempty_string((previous_gap or {}).get("gap_kind")),
        "current_gap_kind": _nonempty_string((current_gap or {}).get("gap_kind")),
        "previous_supply_status": _nonempty_string((previous_gap or {}).get("supply_status")),
        "current_supply_status": _nonempty_string((current_gap or {}).get("supply_status")),
        "previous_required_input_ids": _read_nonempty_string_list((previous_gap or {}).get("required_input_ids")),
        "current_required_input_ids": _read_nonempty_string_list((current_gap or {}).get("required_input_ids")),
        "previous_linked_issue_ids": _read_nonempty_string_list((previous_gap or {}).get("linked_issue_ids")),
        "current_linked_issue_ids": _read_nonempty_string_list((current_gap or {}).get("linked_issue_ids")),
        "previous_controller_action_hint": _optional_action_hint((previous_gap or {}).get("controller_action_hint")),
        "current_controller_action_hint": _optional_action_hint((current_gap or {}).get("controller_action_hint")),
        "supply_delta": supply_delta,
    }

def _optional_action_hint(value: Any) -> dict[str, Any] | None:
    action_hint = _ensure_mapping(value)
    if action_hint is None:
        return None
    action = _normalize_quality_controller_action(action_hint.get("action"), fallback_action="continue_mainline")
    summary = _nonempty_string(action_hint.get("summary"))
    source_surface = _nonempty_string(action_hint.get("source_surface"))
    if summary is None or source_surface is None:
        return None
    return {
        "action": action,
        "summary": summary,
        "target_stage": _nonempty_string(action_hint.get("target_stage")),
        "source_surface": source_surface,
    }

def _resolve_supply_delta(
    *,
    previous_supply_status: str | None,
    current_supply_status: str | None,
    previous_required_input_ids: list[str],
    current_required_input_ids: list[str],
) -> str:
    rank = {
        "reselection_required": 2,
        "blocked": 2,
        "mixed": 2,
        "evidence_required": 1,
    }
    previous_rank = rank.get(previous_supply_status or "")
    current_rank = rank.get(current_supply_status or "")
    if previous_rank is not None and current_rank is not None:
        if current_rank < previous_rank:
            return "progressed"
        if current_rank > previous_rank:
            return "regressed"

    previous_inputs = set(previous_required_input_ids)
    current_inputs = set(current_required_input_ids)
    if current_inputs < previous_inputs:
        return "progressed"
    if previous_inputs < current_inputs:
        return "regressed"
    return "unchanged"

def _open_issue_lineage_map(tracked_issues: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in tracked_issues:
        if _nonempty_string(item.get("status")) != "open":
            continue
        lineage_id = _nonempty_string(item.get("lineage_id"))
        if lineage_id is None:
            continue
        result[lineage_id] = dict(item)
    return result

def _build_issue_closure_progress_entries(
    *,
    previous_open_issues: Mapping[str, dict[str, Any]],
    current_open_issues: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    ordered_issue_ids = list(previous_open_issues.keys())
    ordered_issue_ids.extend(issue_id for issue_id in current_open_issues if issue_id not in previous_open_issues)
    return [
        _build_issue_closure_progress_entry(
            lineage_id=issue_id,
            previous_issue=previous_open_issues.get(issue_id),
            current_issue=current_open_issues.get(issue_id),
        )
        for issue_id in ordered_issue_ids
    ]

def _build_issue_closure_progress_entry(
    *,
    lineage_id: str,
    previous_issue: dict[str, Any] | None,
    current_issue: dict[str, Any] | None,
) -> dict[str, Any]:
    issue = current_issue or previous_issue or {}
    previous_issue_id = _nonempty_string(previous_issue.get("issue_id")) if previous_issue else None
    current_issue_id = _nonempty_string(current_issue.get("issue_id")) if current_issue else None
    previous_summary = _nonempty_string(previous_issue.get("summary")) if previous_issue else None
    current_summary = _nonempty_string(current_issue.get("summary")) if current_issue else None
    previous_closure_status = _nonempty_string(previous_issue.get("closure_status")) if previous_issue else None
    current_closure_status = _nonempty_string(current_issue.get("closure_status")) if current_issue else None
    if previous_issue is not None and current_issue is None:
        transition = "closed"
        closure_delta = "issue_closed"
    elif previous_issue is None and current_issue is not None:
        transition = "newly_opened"
        closure_delta = "new_blocker_opened" if current_issue.get("severity") == "hard" else "new_gap_opened"
    else:
        transition = "still_open"
        closure_delta = _resolve_issue_closure_delta(
            previous_closure_status=previous_closure_status,
            current_closure_status=current_closure_status,
        )
    return {
        "issue_id": current_issue_id or previous_issue_id,
        "lineage_id": lineage_id,
        "lineage_basis": dict(issue.get("lineage_basis") or {}),
        "previous_issue_id": previous_issue_id,
        "current_issue_id": current_issue_id,
        "previous_summary": previous_summary,
        "current_summary": current_summary,
        "dimension_id": issue.get("dimension_id"),
        "summary": current_summary or previous_summary,
        "severity": issue.get("severity"),
        "transition": transition,
        "previous_closure_status": previous_closure_status,
        "current_closure_status": current_closure_status,
        "blocking_reason": (
            _nonempty_string(current_issue.get("blocking_reason")) if current_issue else None
        ) or (
            _nonempty_string(previous_issue.get("blocking_reason")) if previous_issue else None
        ),
        "closure_delta": closure_delta,
    }

def _resolve_issue_closure_delta(
    *,
    previous_closure_status: str | None,
    current_closure_status: str | None,
) -> str:
    rank = {
        "blocked": 2,
        "evidence_required": 1,
    }
    previous_rank = rank.get(previous_closure_status or "")
    current_rank = rank.get(current_closure_status or "")
    if previous_rank is None or current_rank is None or previous_rank == current_rank:
        return "unchanged"
    if current_rank < previous_rank:
        return "progressed"
    return "regressed"

def _read_critique_summary(document: dict[str, Any]) -> dict[str, Any] | None:
    lifecycle_stage = _nonempty_string(document.get("lifecycle_stage"))
    if lifecycle_stage not in REVIEW_CONTEXT_STAGES:
        return None
    try:
        return build_critique_summary(document)
    except WorkspaceStateError:
        return None

def _read_active_draft_id(document: Mapping[str, Any]) -> str | None:
    selection = _ensure_mapping(document.get("current_selection")) or {}
    return _nonempty_string(selection.get("active_draft_id"))

def _ensure_mapping(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None

def _safe_int(value: Any) -> int | None:
    return value if isinstance(value, int) else None

def _nonempty_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None

def _read_nonempty_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = _nonempty_string(item)
        if text is not None:
            result.append(text)
    return result

def _read_nested_string_list(payload: Mapping[str, Any], parent_key: str, child_key: str) -> list[str]:
    parent = _ensure_mapping(payload.get(parent_key))
    if parent is None:
        return []
    return _read_nonempty_string_list(parent.get(child_key))

def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in values:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered

def _flatten_to_strings(values: Iterable[Any]) -> list[str]:
    result: list[str] = []
    for item in values:
        if isinstance(item, list):
            result.extend(_flatten_to_strings(item))
            continue
        text = _nonempty_string(item)
        if text is not None:
            result.append(text)
    return result

__all__ = [name for name in globals() if name.startswith("_") and not name.startswith("__")]
