from __future__ import annotations

from typing import Any, Iterable, Mapping

from .primitives import _nonempty_string


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
