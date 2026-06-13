from __future__ import annotations

from typing import Any

from med_autogrant.grant_quality_value_helpers import (
    _dedupe_preserve_order,
    _nonempty_string,
    _read_nonempty_string_list,
    _stable_digest,
)


def _build_issue(
    *,
    dimension_id: str,
    summary: str,
    severity: str,
    source_surface: str,
    rollback_stage: str | None,
    evidence_refs: list[str],
    context: dict[str, Any],
) -> dict[str, Any]:
    digest = _stable_digest(" ".join(summary.split()).strip().lower())
    closure_status = "blocked" if severity == "hard" else "evidence_required"
    recommended_closure_action = _build_recommended_closure_action(
        dimension_id=dimension_id,
        summary=summary,
        severity=severity,
        rollback_stage=rollback_stage,
        context=context,
    )
    evidence_obligations = _build_issue_evidence_obligations(
        dimension_id=dimension_id,
        summary=summary,
        severity=severity,
        evidence_refs=evidence_refs,
        context=context,
    )
    lineage_basis = _build_issue_lineage_basis(
        dimension_id=dimension_id,
        summary=summary,
        severity=severity,
        recommended_closure_action=recommended_closure_action,
        evidence_obligations=evidence_obligations,
    )
    return {
        "issue_id": f"{dimension_id}:{digest}",
        "lineage_id": _build_issue_lineage_id(lineage_basis),
        "lineage_basis": lineage_basis,
        "dimension_id": dimension_id,
        "summary": summary,
        "status": "open",
        "severity": severity,
        "source_surface": source_surface,
        "rollback_stage": rollback_stage,
        "closure_status": closure_status,
        "blocking_reason": summary if severity == "hard" else None,
        "evidence_obligations": evidence_obligations,
        "recommended_closure_action": recommended_closure_action,
    }


def _build_recommended_closure_action(
    *,
    dimension_id: str,
    summary: str,
    severity: str,
    rollback_stage: str | None,
    context: dict[str, Any],
) -> dict[str, Any]:
    repair_summaries = _dimension_repair_summaries(dimension_id, context=context)
    revision_items = _relevant_revision_items(dimension_id, context=context)
    revision_plan = _active_revision_plan(context)
    action_summary = summary
    source_surface = dimension_id
    if repair_summaries:
        action_summary = repair_summaries[0]
        source_surface = "critique_summary"
    elif revision_items:
        action_summary = _nonempty_string(revision_items[0].get("action")) or summary
        source_surface = "revision_plan"
    elif dimension_id == "version_issue_closure" and revision_plan is not None:
        next_focus = _read_nonempty_string_list(revision_plan.get("next_review_focus"))
        if next_focus:
            action_summary = next_focus[0]
            source_surface = "revision_plan"
    target_stage = rollback_stage or _nonempty_string(context["document"].get("lifecycle_stage"))
    if severity == "gap" and target_stage is None:
        target_stage = "revision"
    return {
        "action": "rollback_upstream" if severity == "hard" else "continue_mainline",
        "summary": action_summary,
        "target_stage": target_stage,
        "source_surface": source_surface,
    }


def _build_issue_evidence_obligations(
    *,
    dimension_id: str,
    summary: str,
    severity: str,
    evidence_refs: list[str],
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    obligations: list[dict[str, Any]] = []
    for item in _relevant_revision_items(dimension_id, context=context):
        item_id = _nonempty_string(item.get("item_id")) or f"{dimension_id}-revision-item"
        obligations.append(
            {
                "obligation_id": f"{dimension_id}:{item_id}",
                "summary": _nonempty_string(item.get("action")) or summary,
                "required_input_ids": _read_nonempty_string_list(item.get("required_input_ids")),
                "evidence_refs": list(evidence_refs),
                "satisfaction_criteria": _nonempty_string(item.get("done_criteria")),
                "source_surface": "revision_plan",
            }
        )
    if obligations:
        return obligations
    repair_summaries = _dimension_repair_summaries(dimension_id, context=context)
    if repair_summaries:
        return [
            {
                "obligation_id": f"{dimension_id}:repair:{_stable_digest(repair_summaries[0])}",
                "summary": repair_summaries[0],
                "required_input_ids": _default_obligation_input_ids(dimension_id, context=context),
                "evidence_refs": list(evidence_refs),
                "satisfaction_criteria": None,
                "source_surface": "critique_summary",
            }
        ]
    return [
        {
            "obligation_id": f"{dimension_id}:issue:{_stable_digest(summary)}",
            "summary": summary,
            "required_input_ids": _default_obligation_input_ids(dimension_id, context=context),
            "evidence_refs": list(evidence_refs),
            "satisfaction_criteria": None,
            "source_surface": dimension_id if severity == "hard" else "evidence_grounding",
        }
    ]


def _build_issue_lineage_basis(
    *,
    dimension_id: str,
    summary: str,
    severity: str,
    recommended_closure_action: dict[str, Any],
    evidence_obligations: list[dict[str, Any]],
) -> dict[str, Any]:
    obligation_ids = [
        obligation_id
        for item in evidence_obligations
        if isinstance(item, dict)
        for obligation_id in [_nonempty_string(item.get("obligation_id"))]
        if obligation_id is not None
    ]
    required_input_ids = _dedupe_preserve_order(
        input_id
        for item in evidence_obligations
        if isinstance(item, dict)
        for input_id in _read_nonempty_string_list(item.get("required_input_ids"))
    )
    target_stage = _nonempty_string(recommended_closure_action.get("target_stage"))
    source_surface = _nonempty_string(recommended_closure_action.get("source_surface")) or dimension_id
    action_summary = _nonempty_string(recommended_closure_action.get("summary"))
    if obligation_ids:
        anchor_ref = obligation_ids[0]
        if ":rev-item-" in anchor_ref:
            anchor_kind = "revision_item"
        elif ":repair:" in anchor_ref:
            anchor_kind = "critique_repair"
        else:
            anchor_kind = "required_input_set"
            anchor_ref = _required_input_anchor_ref(dimension_id=dimension_id, required_input_ids=required_input_ids)
    elif required_input_ids:
        anchor_kind = "required_input_set"
        anchor_ref = _required_input_anchor_ref(dimension_id=dimension_id, required_input_ids=required_input_ids)
    elif action_summary is not None:
        anchor_kind = "closure_action"
        anchor_ref = (
            f"{dimension_id}:action:"
            f"{_stable_digest('|'.join([source_surface, target_stage or '', action_summary, severity]))}"
        )
    else:
        anchor_kind = "summary_fallback"
        anchor_ref = f"{dimension_id}:summary:{_stable_digest(summary)}"
    return {
        "anchor_kind": anchor_kind,
        "anchor_ref": anchor_ref,
        "source_surface": source_surface,
        "target_stage": target_stage,
        "required_input_ids": required_input_ids,
    }


def _build_issue_lineage_id(lineage_basis: dict[str, Any]) -> str:
    return f"{lineage_basis['anchor_kind']}:{lineage_basis['anchor_ref']}"


def _required_input_anchor_ref(*, dimension_id: str, required_input_ids: list[str]) -> str:
    return f"{dimension_id}:inputs:{_stable_digest('|'.join(required_input_ids))}"


def _relevant_revision_items(dimension_id: str, *, context: dict[str, Any]) -> list[dict[str, Any]]:
    revision_plan = _active_revision_plan(context)
    if revision_plan is None:
        return []
    items = [item for item in revision_plan.get("items") or [] if isinstance(item, dict)]
    if dimension_id in {"scientific_question_validity", "necessity_value_closure"}:
        return [
            item
            for item in items
            if _nonempty_string(item.get("action_type")) == "rebuild_argument"
            or _nonempty_string(item.get("target_ref")) == "section:basis"
        ]
    if dimension_id == "applicant_fit":
        return [
            item
            for item in items
            if _nonempty_string(item.get("action_type")) == "tighten_fit"
            or _nonempty_string(item.get("target_ref")) == "section:foundation"
        ]
    if dimension_id in {"unresolved_hard_issues", "version_issue_closure"}:
        high_priority_items = [item for item in items if _nonempty_string(item.get("priority")) == "p0"]
        return high_priority_items or items
    return []


def _dimension_repair_summaries(dimension_id: str, *, context: dict[str, Any]) -> list[str]:
    critique_summary = context["critique_summary"]
    if critique_summary is None:
        return []
    if dimension_id in {"scientific_question_validity", "necessity_value_closure"}:
        return _read_nonempty_string_list(critique_summary.get("logic_chain_repairs"))
    if dimension_id == "applicant_fit":
        return _read_nonempty_string_list(critique_summary.get("applicant_fit_repairs"))
    return []


def _default_obligation_input_ids(dimension_id: str, *, context: dict[str, Any]) -> list[str]:
    state = context["state"]
    if dimension_id == "scientific_question_validity":
        return _dedupe_preserve_order(
            _read_object_id(state.selected_question, "question_id")
            + _read_object_id(state.selected_direction, "direction_id")
        )
    if dimension_id == "necessity_value_closure":
        return _dedupe_preserve_order(
            _read_object_id(state.active_argument_chain, "argument_chain_id")
            + _read_object_id(state.selected_question, "question_id")
        )
    if dimension_id in {"applicant_fit", "technical_feasibility"}:
        return _dedupe_preserve_order(
            _read_object_id(state.active_fit_mapping, "fit_mapping_id")
            + _read_object_id(state.active_draft, "draft_id")
        )
    if dimension_id == "claim_evidence_coverage":
        return _dedupe_preserve_order(
            _read_object_id(state.active_draft, "draft_id")
            + _read_object_id(state.selected_question, "question_id")
            + _read_object_id(state.active_argument_chain, "argument_chain_id")
            + _read_object_id(state.active_fit_mapping, "fit_mapping_id")
        )
    if dimension_id in {"unresolved_hard_issues", "version_issue_closure"}:
        return _dedupe_preserve_order(
            _read_object_id(state.active_revision_plan, "revision_plan_id")
            + _read_object_id(state.active_draft, "draft_id")
        )
    return []


def _read_object_id(payload: dict[str, Any] | None, key: str) -> list[str]:
    if not isinstance(payload, dict):
        return []
    value = _nonempty_string(payload.get(key))
    return [value] if value is not None else []


def _active_revision_plan(context: dict[str, Any]) -> dict[str, Any] | None:
    revision_plan = context["state"].active_revision_plan
    return revision_plan if isinstance(revision_plan, dict) else None
