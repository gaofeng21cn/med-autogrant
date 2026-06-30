from __future__ import annotations

import unittest
from typing import Any


OPL_STAGE_ATTEMPT = {
    "runtime_owner": "one-person-lab",
    "executor_kind": "codex_cli",
    "attempt_lease_ref": "lease:opl/stage-run/mag/test/owner-chain-default-caller",
}


def assert_no_stage_transition_authority(
    test_case: unittest.TestCase,
    boundary: dict[str, Any],
) -> None:
    test_case.assertFalse(
        any(
            boundary[key]
            for key in (
                "mag_writes_stage_current_pointer",
                "mag_writes_stage_terminal_state",
                "mag_selects_next_opl_stage",
            )
        )
    )
    test_case.assertTrue(boundary["requires_opl_stage_transition_authority"])


def selection_start_request() -> dict[str, Any]:
    return {
        "request_id": "autonomy-req-001",
        "opl_stage_attempt": dict(OPL_STAGE_ATTEMPT),
        "start": {
            "mode": "selection_input",
            "selection_input": {
                "selection_input_id": "sel-001",
                "funding_opportunity_pool": [{"brief_id": "nsfc-2026-general"}],
            },
        },
        "goal": {
            "target_status": "submission_grade_candidate",
            "summary": "进入可提交态",
        },
        "max_rounds_or_cycles": 3,
        "budget": {"max_total_steps": 20},
        "stop_conditions": {
            "require_zero_blockers": True,
            "require_zero_evidence_gaps": True,
        },
        "blocker_queue": ["初始 blocker"],
        "evidence_gap_queue": ["初始证据缺口"],
        "reselection_policy": {
            "enabled": True,
            "max_reselections": 1,
        },
        "rollback_policy": {
            "enabled": True,
            "max_rollbacks": 1,
        },
    }


def workspace_start_request() -> dict[str, Any]:
    return {
        "request_id": "autonomy-req-002",
        "opl_stage_attempt": dict(OPL_STAGE_ATTEMPT),
        "start": {
            "mode": "workspace",
            "workspace": {
                "workspace_id": "ws-001",
                "lifecycle_stage": "critique",
            },
        },
        "goal": {
            "target_status": "near_submission_candidate",
            "summary": "先达到 near submission",
        },
        "max_rounds_or_cycles": 2,
        "budget": {"max_total_steps": 10},
        "stop_conditions": {
            "require_zero_blockers": True,
            "require_zero_evidence_gaps": True,
        },
        "blocker_queue": [],
        "evidence_gap_queue": [],
        "reselection_policy": {
            "enabled": False,
            "max_reselections": 0,
        },
        "rollback_policy": {
            "enabled": False,
            "max_rollbacks": 0,
        },
    }


def closure_package(
    *,
    closure_id: str,
    summary: str,
    severity: str = "hard",
    action: str = "continue_mainline",
    target_stage: str | None = None,
    required_input_ids: list[str] | None = None,
    linked_issue_ids: list[str] | None = None,
    blocking_reasons: list[str] | None = None,
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "closure_id": closure_id,
        "summary": summary,
        "severity": severity,
        "target_stage": target_stage,
        "action": action,
        "required_input_ids": list(required_input_ids or []),
        "evidence_refs": list(evidence_refs or []),
        "linked_issue_ids": list(linked_issue_ids or []),
        "blocking_reasons": list(blocking_reasons or []),
        "evidence_obligations": [],
        "acceptance_signals": [
            {
                "signal_id": f"signal:{closure_id}",
                "signal_kind": "controller_action",
                "summary": summary,
                "source_surface": "grant_quality",
                "required_input_ids": list(required_input_ids or []),
                "evidence_refs": list(evidence_refs or []),
            }
        ],
    }


def _resolved_overall_status(quality_status: str, overall_status: str | None) -> str:
    if overall_status is not None:
        return overall_status
    if quality_status == "not_ready":
        return "blocked"
    return quality_status


def _resolved_score(quality_status: str, overall_score: int | None) -> int:
    if overall_score is not None:
        return overall_score
    if quality_status == "submission_grade_candidate":
        return 90
    if quality_status == "near_submission_candidate":
        return 78
    return 55


def _resolved_loop_gate_action(quality_status: str, loop_gate_action: str | None) -> str:
    if loop_gate_action is not None:
        return loop_gate_action
    if quality_status == "not_ready":
        return "rollback_required"
    return "continue"


def _evidence_supply_queue_summary(supply_queue: list[dict[str, Any]]) -> dict[str, Any]:
    gap_ids = [
        str(item.get("gap_id") or "").strip()
        for item in supply_queue
        if str(item.get("gap_id") or "").strip()
    ]
    status_counts: dict[str, list[str]] = {}
    kind_counts: dict[str, list[str]] = {}
    for item in supply_queue:
        gap_id = str(item.get("gap_id") or "").strip()
        supply_status = str(item.get("supply_status") or "").strip()
        gap_kind = str(item.get("gap_kind") or "").strip()
        if gap_id and supply_status:
            status_counts.setdefault(supply_status, []).append(gap_id)
        if gap_id and gap_kind:
            kind_counts.setdefault(gap_kind, []).append(gap_id)

    return {
        "total_gap_count": len(gap_ids),
        "outstanding_gap_ids": gap_ids,
        "status_counts": [
            {
                "supply_status": status,
                "count": len(ids),
                "gap_ids": ids,
            }
            for status, ids in status_counts.items()
        ],
        "kind_counts": [
            {
                "gap_kind": gap_kind,
                "count": len(ids),
                "gap_ids": ids,
            }
            for gap_kind, ids in kind_counts.items()
        ],
    }


def quality_result(
    *,
    quality_status: str,
    unresolved_blockers: list[str] | None = None,
    evidence_gaps: list[str] | None = None,
    closure_packages: list[dict[str, Any]] | None = None,
    evidence_supply_queue: list[dict[str, Any]] | None = None,
    workspace_id: str = "ws-001",
    lifecycle_stage: str = "critique",
    draft_id: str | None = "draft-001",
    grant_run_id: str = "grant-001",
    overall_score: int | None = None,
    overall_status: str | None = None,
    summary: str | None = None,
    loop_gate_action: str | None = None,
    loop_gate_stage: str | None = None,
    loop_gate_reason: str | None = None,
) -> dict[str, Any]:
    unresolved = list(unresolved_blockers or [])
    gaps = list(evidence_gaps or [])
    packages = [dict(item) for item in (closure_packages or [])]
    supply_queue = [dict(item) for item in (evidence_supply_queue or [])]
    resolved_overall_status = _resolved_overall_status(quality_status, overall_status)
    resolved_score = _resolved_score(quality_status, overall_score)
    resolved_summary = summary or f"quality:{resolved_overall_status}"
    resolved_loop_gate_action = _resolved_loop_gate_action(quality_status, loop_gate_action)
    resolved_loop_gate_reason = loop_gate_reason or (unresolved[0] if unresolved else resolved_summary)

    return {
        "quality_status": quality_status,
        "blocker_report": {
            "surface_kind": "grant_quality_scorecard",
            "overall_status": resolved_overall_status,
            "overall_score": resolved_score,
        },
        "unresolved_blockers": unresolved,
        "evidence_gaps": gaps,
        "evidence_supply_queue": supply_queue,
        "quality_closure_dossier": {
            "surface_kind": "grant_quality_closure_dossier",
            "dossier_version": 1,
            "workspace_surface_kind": "nsfc_workspace",
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
            "draft_id": draft_id,
            "quality_summary": {
                "overall_status": resolved_overall_status,
                "overall_score": resolved_score,
                "summary": resolved_summary,
                "loop_gate": {
                    "action": resolved_loop_gate_action,
                    "recommended_stage": loop_gate_stage,
                    "reason": resolved_loop_gate_reason,
                },
            },
            "unclosed_hard_issues": unresolved,
            "evidence_supply_queue_summary": _evidence_supply_queue_summary(supply_queue),
            "closure_packages": packages,
        },
    }
