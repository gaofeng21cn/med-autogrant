from __future__ import annotations

from med_autogrant.grant_autonomy_quality_payload import _normalize_quality_output


def _closure_package(
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
) -> dict[str, object]:
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


def _quality_result(
    *,
    quality_status: str,
    unresolved_blockers: list[str] | None = None,
    evidence_gaps: list[str] | None = None,
    closure_packages: list[dict[str, object]] | None = None,
    workspace_id: str = "ws-001",
    lifecycle_stage: str = "critique",
    draft_id: str | None = "draft-001",
    grant_run_id: str = "grant-001",
    overall_score: int | None = None,
    overall_status: str | None = None,
    summary: str | None = None,
) -> dict[str, object]:
    unresolved = list(unresolved_blockers or [])
    gaps = list(evidence_gaps or [])
    packages = [dict(item) for item in (closure_packages or [])]
    resolved_overall_status = overall_status
    if resolved_overall_status is None:
        resolved_overall_status = quality_status if quality_status != "not_ready" else "blocked"
    resolved_score = overall_score
    if resolved_score is None:
        resolved_score = 90 if quality_status == "submission_grade_candidate" else 78
    resolved_summary = summary or f"quality:{resolved_overall_status}"
    return {
        "quality_status": quality_status,
        "blocker_report": {
            "surface_kind": "grant_quality_scorecard",
            "overall_status": resolved_overall_status,
            "overall_score": resolved_score,
        },
        "unresolved_blockers": unresolved,
        "evidence_gaps": gaps,
        "evidence_supply_queue": [],
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
                    "action": "continue",
                    "recommended_stage": None,
                    "reason": resolved_summary,
                },
            },
            "unclosed_hard_issues": unresolved,
            "evidence_supply_queue_summary": {
                "total_gap_count": 0,
                "outstanding_gap_ids": [],
                "status_counts": [],
                "kind_counts": [],
            },
            "closure_packages": packages,
        },
    }


def test_normalize_quality_output_accepts_controller_quality_fixture() -> None:
    quality_output = _quality_result(
        quality_status="near_submission_candidate",
        unresolved_blockers=[],
        evidence_gaps=["secondary evidence gap"],
        closure_packages=[
            _closure_package(
                closure_id="secondary-evidence",
                summary="Secondary evidence remains.",
                severity="gap",
                action="continue_mainline",
                target_stage="revision",
                evidence_refs=["evidence://secondary"],
            )
        ],
    )

    normalized = _normalize_quality_output(quality_output)

    assert normalized is not None
    assert normalized["quality_status"] == "near_submission_candidate"
    assert normalized["evidence_gaps"] == ["secondary evidence gap"]
    closure_package = normalized["quality_closure_dossier"]["closure_packages"][0]
    assert closure_package["closure_id"] == "secondary-evidence"
    assert closure_package["evidence_refs"] == ["evidence://secondary"]
    quality_output["blocker_report"]["overall_status"] = "mutated-after-normalize"
    assert normalized["blocker_report"]["overall_status"] == "near_submission_candidate"
    assert _normalize_quality_output({"quality_status": "bad-status"}) is None
