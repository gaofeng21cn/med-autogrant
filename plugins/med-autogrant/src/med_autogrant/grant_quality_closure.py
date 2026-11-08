from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.grant_quality_parts import (
    _dedupe_preserve_order,
    _ensure_mapping,
    _nonempty_string,
    _optional_action_hint,
    _read_nonempty_string_list,
    _stable_digest,
)

def _build_quality_closure_packages(
    *,
    tracked_issues: list[dict[str, Any]],
    evidence_supply_queue: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped_issues, ordered_lineage_ids = _group_tracked_issues_by_lineage(tracked_issues)
    queue_by_gap_id = {
        gap_id: dict(item)
        for item in evidence_supply_queue
        for gap_id in [_nonempty_string(item.get("gap_id"))]
        if gap_id is not None
    }
    packages = [
        _build_issue_lineage_closure_package(
            closure_id=lineage_id,
            issues=grouped_issues[lineage_id],
            gap=queue_by_gap_id.get(lineage_id),
        )
        for lineage_id in ordered_lineage_ids
    ]
    seen_closure_ids = set(ordered_lineage_ids)
    for item in evidence_supply_queue:
        gap_id = _nonempty_string(item.get("gap_id"))
        if gap_id is None or gap_id in seen_closure_ids:
            continue
        packages.append(_build_queue_only_closure_package(dict(item)))
    return packages

def _group_tracked_issues_by_lineage(
    tracked_issues: list[dict[str, Any]],
) -> tuple[dict[str, list[dict[str, Any]]], list[str]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    ordered_lineage_ids: list[str] = []
    for item in tracked_issues:
        lineage_id = _nonempty_string(item.get("lineage_id"))
        if lineage_id is None:
            continue
        if lineage_id not in grouped:
            grouped[lineage_id] = []
            ordered_lineage_ids.append(lineage_id)
        grouped[lineage_id].append(item)
    return grouped, ordered_lineage_ids

def _build_issue_lineage_closure_package(
    *,
    closure_id: str,
    issues: list[dict[str, Any]],
    gap: dict[str, Any] | None,
) -> dict[str, Any]:
    obligations = _collect_issue_lineage_obligations(issues)
    action_hint = _resolve_closure_package_action_hint(issues=issues, gap=gap)
    required_input_ids = _dedupe_preserve_order(
        input_id
        for input_id in (
            _read_nonempty_string_list((gap or {}).get("required_input_ids"))
            + _collect_issue_lineage_required_input_ids(issues)
        )
    )
    evidence_refs = _dedupe_preserve_order(
        evidence_ref
        for evidence_ref in (
            _read_nonempty_string_list((gap or {}).get("evidence_refs"))
            + _collect_issue_lineage_evidence_refs(issues)
        )
    )
    linked_issue_ids = _dedupe_preserve_order(
        issue_id
        for issue_id in (
            _read_nonempty_string_list((gap or {}).get("linked_issue_ids"))
            + _collect_issue_lineage_issue_ids(issues)
        )
    )
    blocking_reasons = _dedupe_preserve_order(
        reason
        for reason in (
            _read_nonempty_string_list((gap or {}).get("blocking_reasons"))
            + _collect_issue_lineage_blocking_reasons(issues)
        )
    )
    return {
        "closure_id": closure_id,
        "summary": _resolve_closure_package_summary(issues=issues, gap=gap, closure_id=closure_id),
        "severity": _resolve_issue_lineage_severity(issues),
        "target_stage": _nonempty_string(action_hint.get("target_stage")),
        "action": action_hint["action"],
        "required_input_ids": required_input_ids,
        "evidence_refs": evidence_refs,
        "linked_issue_ids": linked_issue_ids,
        "blocking_reasons": blocking_reasons,
        "evidence_obligations": obligations,
        "acceptance_signals": _build_closure_acceptance_signals(
            obligations=obligations,
            gap=gap,
            fallback_action_hint=action_hint,
        ),
    }

def _build_queue_only_closure_package(gap: dict[str, Any]) -> dict[str, Any]:
    action_hint = _optional_action_hint(gap.get("controller_action_hint")) or {
        "action": "continue_mainline",
        "summary": _nonempty_string(gap.get("gap_summary")) or "关闭当前 evidence gap。",
        "target_stage": None,
        "source_surface": "grant_quality",
    }
    return {
        "closure_id": _nonempty_string(gap.get("gap_id")) or "gap",
        "summary": _nonempty_string(gap.get("gap_summary")) or "关闭当前 evidence gap。",
        "severity": _severity_from_gap_kind(_nonempty_string(gap.get("gap_kind"))),
        "target_stage": _nonempty_string(action_hint.get("target_stage")),
        "action": action_hint["action"],
        "required_input_ids": _read_nonempty_string_list(gap.get("required_input_ids")),
        "evidence_refs": _read_nonempty_string_list(gap.get("evidence_refs")),
        "linked_issue_ids": _read_nonempty_string_list(gap.get("linked_issue_ids")),
        "blocking_reasons": _read_nonempty_string_list(gap.get("blocking_reasons")),
        "evidence_obligations": [],
        "acceptance_signals": _build_closure_acceptance_signals(
            obligations=[],
            gap=gap,
            fallback_action_hint=action_hint,
        ),
    }

def _resolve_issue_lineage_severity(issues: list[dict[str, Any]]) -> str:
    severities = {
        severity
        for issue in issues
        for severity in [_nonempty_string(issue.get("severity"))]
        if severity is not None
    }
    return "hard" if "hard" in severities else "gap"

def _severity_from_gap_kind(gap_kind: str | None) -> str:
    if gap_kind in {"hard_blocker", "mixed_gap", "funding_profile_mismatch"}:
        return "hard"
    return "gap"

def _resolve_closure_package_summary(
    *,
    issues: list[dict[str, Any]],
    gap: dict[str, Any] | None,
    closure_id: str,
) -> str:
    gap_summary = _nonempty_string((gap or {}).get("gap_summary"))
    if gap_summary is not None:
        return gap_summary
    for issue in issues:
        summary = _nonempty_string(issue.get("summary"))
        if summary is not None:
            return summary
    return closure_id

def _collect_issue_lineage_issue_ids(issues: list[dict[str, Any]]) -> list[str]:
    return _dedupe_preserve_order(
        issue_id
        for issue in issues
        for issue_id in [_nonempty_string(issue.get("issue_id"))]
        if issue_id is not None
    )

def _collect_issue_lineage_blocking_reasons(issues: list[dict[str, Any]]) -> list[str]:
    return _dedupe_preserve_order(
        blocking_reason
        for issue in issues
        for blocking_reason in [_nonempty_string(issue.get("blocking_reason"))]
        if blocking_reason is not None
    )

def _collect_issue_lineage_required_input_ids(issues: list[dict[str, Any]]) -> list[str]:
    return _dedupe_preserve_order(
        input_id
        for issue in issues
        for input_id in _read_nonempty_string_list(
            (_ensure_mapping(issue.get("lineage_basis")) or {}).get("required_input_ids")
        )
        + [
            item
            for obligation in _read_evidence_obligations(issue)
            for item in _read_nonempty_string_list(obligation.get("required_input_ids"))
        ]
    )

def _collect_issue_lineage_evidence_refs(issues: list[dict[str, Any]]) -> list[str]:
    return _dedupe_preserve_order(
        evidence_ref
        for issue in issues
        for obligation in _read_evidence_obligations(issue)
        for evidence_ref in _read_nonempty_string_list(obligation.get("evidence_refs"))
    )

def _collect_issue_lineage_obligations(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    obligations: list[dict[str, Any]] = []
    seen_obligation_ids: set[str] = set()
    for issue in issues:
        for obligation in _read_evidence_obligations(issue):
            obligation_id = _nonempty_string(obligation.get("obligation_id"))
            if obligation_id is None or obligation_id in seen_obligation_ids:
                continue
            seen_obligation_ids.add(obligation_id)
            obligations.append(dict(obligation))
    return obligations

def _read_evidence_obligations(issue: dict[str, Any]) -> list[dict[str, Any]]:
    obligations = issue.get("evidence_obligations")
    if not isinstance(obligations, list):
        return []
    return [
        obligation_payload
        for item in obligations
        for obligation_payload in [_ensure_mapping(item)]
        if obligation_payload is not None
    ]

def _resolve_closure_package_action_hint(
    *,
    issues: list[dict[str, Any]],
    gap: dict[str, Any] | None,
) -> dict[str, Any]:
    gap_action_hint = _optional_action_hint((gap or {}).get("controller_action_hint"))
    if gap_action_hint is not None:
        return gap_action_hint
    prioritized_issues = sorted(
        issues,
        key=lambda item: 0 if _nonempty_string(item.get("severity")) == "hard" else 1,
    )
    for issue in prioritized_issues:
        action_hint = _optional_action_hint(issue.get("recommended_closure_action"))
        if action_hint is not None:
            return action_hint
    fallback_issue = prioritized_issues[0] if prioritized_issues else {}
    return {
        "action": "continue_mainline",
        "summary": _nonempty_string(fallback_issue.get("summary")) or "继续关闭当前 closure package。",
        "target_stage": _nonempty_string(fallback_issue.get("rollback_stage")),
        "source_surface": _nonempty_string(fallback_issue.get("source_surface")) or "grant_quality",
    }

def _build_closure_acceptance_signals(
    *,
    obligations: list[dict[str, Any]],
    gap: dict[str, Any] | None,
    fallback_action_hint: Mapping[str, Any],
) -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = []
    for obligation in obligations:
        obligation_id = _nonempty_string(obligation.get("obligation_id"))
        if obligation_id is None:
            continue
        signals.append(
            {
                "signal_id": f"obligation:{obligation_id}",
                "signal_kind": "evidence_obligation",
                "summary": _nonempty_string(obligation.get("satisfaction_criteria"))
                or _nonempty_string(obligation.get("summary"))
                or obligation_id,
                "source_surface": _nonempty_string(obligation.get("source_surface")) or "grant_quality",
                "required_input_ids": _read_nonempty_string_list(obligation.get("required_input_ids")),
                "evidence_refs": _read_nonempty_string_list(obligation.get("evidence_refs")),
            }
        )
    if signals:
        return signals

    supply_actions = (gap or {}).get("supply_actions")
    if isinstance(supply_actions, list):
        for action in supply_actions:
            action_payload = _ensure_mapping(action)
            if action_payload is None:
                continue
            obligation_id = _nonempty_string(action_payload.get("obligation_id")) or "supply-action"
            signals.append(
                {
                    "signal_id": f"supply:{obligation_id}",
                    "signal_kind": "supply_action",
                    "summary": _nonempty_string(action_payload.get("satisfaction_criteria"))
                    or _nonempty_string(action_payload.get("summary"))
                    or obligation_id,
                    "source_surface": _nonempty_string(action_payload.get("source_surface")) or "grant_quality",
                    "required_input_ids": _read_nonempty_string_list(action_payload.get("required_input_ids")),
                    "evidence_refs": _read_nonempty_string_list(action_payload.get("evidence_refs")),
                }
            )
    if signals:
        return signals

    return [
        {
            "signal_id": f"controller:{_stable_digest(_nonempty_string(fallback_action_hint.get('summary')) or 'closure')}",
            "signal_kind": "controller_action",
            "summary": _nonempty_string(fallback_action_hint.get("summary")) or "关闭当前 closure package。",
            "source_surface": _nonempty_string(fallback_action_hint.get("source_surface")) or "grant_quality",
            "required_input_ids": _read_nonempty_string_list((gap or {}).get("required_input_ids")),
            "evidence_refs": _read_nonempty_string_list((gap or {}).get("evidence_refs")),
        }
    ]
