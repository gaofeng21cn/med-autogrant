from __future__ import annotations

import copy
from typing import Any

from med_autogrant.workspace_types import ValidationIssue, WorkspaceContext, WorkspaceState, WorkspaceStateError

_EVIDENCE_TRUST_LEVELS: tuple[str, ...] = (
    "trusted",
    "usable_with_verification",
    "reference_only",
    "stale_or_conflicting",
    "missing_context",
)
_EVIDENCE_TRUST_RANK: dict[str, int] = {
    trust_level: index + 1 for index, trust_level in enumerate(_EVIDENCE_TRUST_LEVELS)
}

def _build_workspace_state(document: dict[str, Any]) -> WorkspaceState:
    from med_autogrant.workspace_validation import validate_workspace_document

    result = validate_workspace_document(document)
    if not result.ok:
        first = result.errors[0]
        raise WorkspaceStateError(
            f"{first.path}: {first.message}",
            errors=result.errors,
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    selection = document["current_selection"]
    direction_by_id = {item["direction_id"]: item for item in document.get("direction_hypotheses", []) if isinstance(item, dict)}
    question_by_id = {item["question_id"]: item for item in document.get("scientific_question_cards", []) if isinstance(item, dict)}
    fit_mapping_by_id = {
        item["fit_mapping_id"]: item for item in document.get("applicant_fit_mappings", []) if isinstance(item, dict)
    }
    draft_by_id = {item["draft_id"]: item for item in document.get("application_drafts", []) if isinstance(item, dict)}
    critique_by_id = {item["critique_id"]: item for item in document.get("mentor_critiques", []) if isinstance(item, dict)}
    revision_plan_by_id = {item["revision_plan_id"]: item for item in document.get("revision_plans", []) if isinstance(item, dict)}

    selected_direction = direction_by_id.get(selection.get("selected_direction_id"))
    selected_question = question_by_id.get(selection.get("selected_question_id"))
    active_fit_mapping = fit_mapping_by_id.get(selection.get("active_fit_mapping_id"))
    active_draft = draft_by_id.get(selection.get("active_draft_id"))
    active_revision_plan = revision_plan_by_id.get(selection.get("active_revision_plan_id"))
    active_critique = None
    reviewed_revision_plan = None
    if active_revision_plan is not None:
        active_critique = critique_by_id.get(active_revision_plan.get("critique_id"))
        if active_critique is not None:
            reviewed_revision_plan = revision_plan_by_id.get(active_critique.get("reviewed_revision_plan_id"))

    active_argument_chain = None
    if selected_question is not None:
        active_argument_chain = next(
            (
                item
                for item in document.get("argument_chains", [])
                if isinstance(item, dict) and item.get("scientific_question_id") == selected_question["question_id"]
            ),
            None,
        )

    return WorkspaceState(
        document=document,
        current_selection=selection,
        selected_direction=selected_direction,
        selected_question=selected_question,
        active_argument_chain=active_argument_chain,
        active_fit_mapping=active_fit_mapping,
        active_draft=active_draft,
        active_revision_plan=active_revision_plan,
        active_critique=active_critique,
        reviewed_revision_plan=reviewed_revision_plan,
    )

def _serialize_direction(direction: dict[str, Any] | None) -> dict[str, Any] | None:
    if direction is None:
        return None
    return {
        "id": direction["direction_id"],
        "title": direction["title"],
        "decision_status": direction["decision_status"],
    }

def _serialize_question(question: dict[str, Any] | None) -> dict[str, Any] | None:
    if question is None:
        return None
    return {
        "id": question["question_id"],
        "core_question": question["core_question"],
        "knowledge_boundary": question["knowledge_boundary"],
    }

def _serialize_argument_chain(argument_chain: dict[str, Any] | None) -> dict[str, Any] | None:
    if argument_chain is None:
        return None
    return {
        "id": argument_chain["argument_chain_id"],
        "necessity_claim": argument_chain["necessity_claim"],
    }

def _serialize_fit_mapping(fit_mapping: dict[str, Any] | None) -> dict[str, Any] | None:
    if fit_mapping is None:
        return None
    return {
        "id": fit_mapping["fit_mapping_id"],
        "argument_chain_id": fit_mapping["argument_chain_id"],
        "applicant_fit_summary": fit_mapping["applicant_fit_summary"],
        "unique_advantage": fit_mapping["unique_advantage"],
    }

def _serialize_draft(draft: dict[str, Any] | None) -> dict[str, Any] | None:
    if draft is None:
        return None
    return {
        "id": draft["draft_id"],
        "version_label": draft["version_label"],
        "status": draft["status"],
        "project_title": draft["project_title"],
        "outline_count": len(draft.get("outline", [])),
        "section_count": len(draft.get("sections", [])),
    }

def _serialize_revision_plan(revision_plan: dict[str, Any] | None) -> dict[str, Any] | None:
    if revision_plan is None:
        return None
    return {
        "id": revision_plan["revision_plan_id"],
        "item_count": len(revision_plan["items"]),
        "execution_status": revision_plan.get("execution_status", "planned"),
        "pre_revision_version_label": revision_plan.get("pre_revision_version_label"),
        "post_revision_version_label": revision_plan.get("post_revision_version_label"),
        "comparison_summary": revision_plan.get("comparison_summary"),
        "next_review_focus_count": len(revision_plan.get("next_review_focus", [])),
    }

def _serialize_critique(critique: dict[str, Any] | None) -> dict[str, Any] | None:
    if critique is None:
        return None
    return {
        "id": critique["critique_id"],
        "verdict": critique["verdict"],
        "reviewed_revision_plan_id": critique.get("reviewed_revision_plan_id"),
        "forced_rollback_stage": critique.get("forced_rollback_stage"),
        "forced_rollback_reason": critique.get("forced_rollback_reason"),
        "blocking_issue_count": len(critique.get("blocking_issues", [])),
    }

def _serialize_reviewed_revision_evidence(revision_plan: dict[str, Any] | None) -> dict[str, Any] | None:
    if revision_plan is None:
        return None
    return {
        "revision_plan_id": revision_plan["revision_plan_id"],
        "source_critique_id": revision_plan["critique_id"],
        "execution_status": revision_plan.get("execution_status", "planned"),
        "pre_revision_version_label": revision_plan.get("pre_revision_version_label"),
        "post_revision_version_label": revision_plan.get("post_revision_version_label"),
        "comparison_summary": revision_plan.get("comparison_summary"),
    }

def _build_intake_section(
    *,
    workspace_id: str,
    section_id: str,
    status: str,
    trust_level: str,
    summary: str,
    missing_items: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "section_id": section_id,
        "status": status,
        "trust_level": trust_level,
        "summary": summary,
        "linked_refs": [
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::{section_id}",
                "label": section_id,
            }
        ],
        "missing_items": list(missing_items or []),
    }

def _selection_context(document: dict[str, Any]) -> dict[str, Any]:
    selection = document.get("current_selection")
    if not isinstance(selection, dict):
        selection = {}
    return {
        "selected_direction_id": selection.get("selected_direction_id"),
        "selected_question_id": selection.get("selected_question_id"),
        "active_fit_mapping_id": selection.get("active_fit_mapping_id"),
        "active_draft_id": selection.get("active_draft_id"),
        "active_revision_plan_id": selection.get("active_revision_plan_id"),
    }

def _track_record_evidence_ids(document: dict[str, Any]) -> list[str]:
    evidence_ids: set[str] = set()
    for output in document.get("track_record", {}).get("representative_outputs", []):
        if not isinstance(output, dict):
            continue
        evidence = output.get("evidence")
        evidence_id = evidence.get("evidence_id") if isinstance(evidence, dict) else None
        if isinstance(evidence_id, str) and evidence_id.strip():
            evidence_ids.add(evidence_id.strip())
    return sorted(evidence_ids)

def _active_project_evidence_ids(document: dict[str, Any]) -> list[str]:
    evidence_ids: set[str] = set()
    for project in document.get("active_project_set", {}).get("projects", []):
        if not isinstance(project, dict):
            continue
        for evidence in project.get("linked_evidence", []):
            if not isinstance(evidence, dict):
                continue
            evidence_id = evidence.get("evidence_id")
            if isinstance(evidence_id, str) and evidence_id.strip():
                evidence_ids.add(evidence_id.strip())
    return sorted(evidence_ids)

def _preliminary_evidence_ids(document: dict[str, Any]) -> list[str]:
    evidence_ids: set[str] = set()
    for item in document.get("preliminary_evidence_pack", {}).get("evidence_items", []):
        if not isinstance(item, dict):
            continue
        evidence = item.get("evidence")
        evidence_id = evidence.get("evidence_id") if isinstance(evidence, dict) else None
        if isinstance(evidence_id, str) and evidence_id.strip():
            evidence_ids.add(evidence_id.strip())
    return sorted(evidence_ids)

def _preliminary_evidence_item_ids(document: dict[str, Any]) -> list[str]:
    item_ids: set[str] = set()
    for item in document.get("preliminary_evidence_pack", {}).get("evidence_items", []):
        if not isinstance(item, dict):
            continue
        item_id = item.get("item_id")
        if isinstance(item_id, str) and item_id.strip():
            item_ids.add(item_id.strip())
    return sorted(item_ids)

def _collect_primary_evidence_ids(document: dict[str, Any]) -> list[str]:
    return sorted(
        set(
            _track_record_evidence_ids(document)
            + _active_project_evidence_ids(document)
            + _preliminary_evidence_ids(document)
        )
    )

def _selected_direction_evidence_ids(document: dict[str, Any], selection_context: dict[str, Any]) -> list[str]:
    selected_direction_id = selection_context.get("selected_direction_id")
    if not isinstance(selected_direction_id, str) or not selected_direction_id.strip():
        return []
    for item in document.get("direction_hypotheses", []):
        if isinstance(item, dict) and item.get("direction_id") == selected_direction_id:
            return _string_list(item.get("required_evidence_ids"))
    return []

def _selected_question_evidence_ids(document: dict[str, Any], selection_context: dict[str, Any]) -> list[str]:
    selected_question_id = selection_context.get("selected_question_id")
    if not isinstance(selected_question_id, str) or not selected_question_id.strip():
        return []
    for item in document.get("scientific_question_cards", []):
        if isinstance(item, dict) and item.get("question_id") == selected_question_id:
            return _string_list(item.get("linked_evidence_ids"))
    return []

def _active_argument_chain_evidence_ids(document: dict[str, Any], selection_context: dict[str, Any]) -> list[str]:
    selected_question_id = selection_context.get("selected_question_id")
    if not isinstance(selected_question_id, str) or not selected_question_id.strip():
        return []
    for item in document.get("argument_chains", []):
        if isinstance(item, dict) and item.get("scientific_question_id") == selected_question_id:
            return _string_list(item.get("linked_evidence_ids"))
    return []

def _active_fit_mapping_evidence_ids(document: dict[str, Any], selection_context: dict[str, Any]) -> list[str]:
    active_fit_mapping_id = selection_context.get("active_fit_mapping_id")
    if not isinstance(active_fit_mapping_id, str) or not active_fit_mapping_id.strip():
        return []
    for item in document.get("applicant_fit_mappings", []):
        if isinstance(item, dict) and item.get("fit_mapping_id") == active_fit_mapping_id:
            return _string_list(item.get("linked_evidence_ids"))
    return []

def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return sorted({item.strip() for item in value if isinstance(item, str) and item.strip()})

def _collect_trust_ranked_evidence(document: dict[str, Any]) -> list[dict[str, Any]]:
    workspace_id = document["workspace_id"]
    entries: list[dict[str, Any]] = []

    for output in document["track_record"].get("representative_outputs", []):
        output_id = output.get("output_id")
        if not isinstance(output_id, str) or not output_id.strip():
            continue
        evidence = output.get("evidence")
        trust_level = "trusted" if isinstance(evidence, dict) else "missing_context"
        entries.append(
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::track_record.representative_outputs::{output_id}",
                "label": output.get("title") or output_id,
                "trust_level": trust_level,
                "trust_rank": _EVIDENCE_TRUST_RANK[trust_level],
                "trust_note": (
                    "代表性成果可直接回指申请人既有积累。"
                    if isinstance(evidence, dict)
                    else "代表性成果缺少结构化 evidence 指针。"
                ),
                "source_type": (evidence or {}).get("source_type", "publication") if isinstance(evidence, dict) else "publication",
                "supports": ["applicant_fit", "scientific_question", "technical_route"],
                "_source_priority": 1,
            }
        )

    for project in document["active_project_set"].get("projects", []):
        project_id = project.get("project_id")
        if not isinstance(project_id, str) or not project_id.strip():
            continue
        linked_evidence = project.get("linked_evidence")
        has_linked_evidence = isinstance(linked_evidence, list) and bool(linked_evidence)
        trust_level = "trusted" if has_linked_evidence else "missing_context"
        entries.append(
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::active_project_set.projects::{project_id}",
                "label": project.get("title") or project_id,
                "trust_level": trust_level,
                "trust_rank": _EVIDENCE_TRUST_RANK[trust_level],
                "trust_note": (
                    "在研项目可直接约束技术路线与资源可用性。"
                    if has_linked_evidence
                    else "在研项目缺少结构化 linked_evidence。"
                ),
                "source_type": "project",
                "supports": ["applicant_fit", "technical_route"],
                "_source_priority": 2,
            }
        )

    for item in document["preliminary_evidence_pack"].get("evidence_items", []):
        item_id = item.get("item_id")
        if not isinstance(item_id, str) or not item_id.strip():
            continue
        trust_level = _trust_level_from_preliminary_item(item)
        entries.append(
            {
                "ref_kind": "workspace_locator",
                "ref": f"grant_workspace::{workspace_id}::preliminary_evidence_pack.evidence_items::{item_id}",
                "label": item.get("title") or item_id,
                "trust_level": trust_level,
                "trust_rank": _EVIDENCE_TRUST_RANK[trust_level],
                "trust_note": _trust_note_from_preliminary_item(item),
                "source_type": "preliminary_result",
                "supports": ["scientific_question", "technical_route"],
                "_source_priority": 3,
            }
        )

    ordered_entries = sorted(
        entries,
        key=lambda item: (
            int(item["trust_rank"]),
            int(item["_source_priority"]),
            str(item["ref"]),
        ),
    )
    for item in ordered_entries:
        item.pop("_source_priority", None)
    return ordered_entries

def _trust_level_from_preliminary_item(item: dict[str, Any]) -> str:
    strength = item.get("strength")
    if strength == "strong":
        return "trusted"
    if strength == "moderate":
        return "usable_with_verification"
    if strength == "weak":
        return "reference_only"
    return "missing_context"

def _trust_note_from_preliminary_item(item: dict[str, Any]) -> str:
    trust_level = _trust_level_from_preliminary_item(item)
    if trust_level == "trusted":
        return "前期结果强度足够，可直接进入 route grounding。"
    if trust_level == "usable_with_verification":
        return "前期结果可用，但仍需在后续论证中显式补足功能验证。"
    if trust_level == "reference_only":
        return "前期结果强度偏弱，仅适合作为方向线索。"
    return "前期结果缺少可判定的强度信息。"

def _index_objects(
    items: Any,
    key_name: str,
    scope_name: str,
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    if not isinstance(items, list):
        return indexed
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        key = item.get(key_name)
        if not isinstance(key, str) or not key:
            continue
        if key in indexed:
            issues.append(
                ValidationIssue(
                    path=f"{scope_name}[{index}].{key_name}",
                    message=f"{key_name} 不能重复。",
                )
            )
            continue
        indexed[key] = item
    return indexed

def _require_workspace_context(document: dict[str, Any]) -> WorkspaceContext:
    state = _build_workspace_state(document)
    if (
        state.selected_direction is None
        or state.selected_question is None
        or state.active_argument_chain is None
        or state.active_fit_mapping is None
        or state.active_draft is None
        or state.active_revision_plan is None
        or state.active_critique is None
    ):
        issue = ValidationIssue(
            path="lifecycle_stage",
            message="当前 workspace 尚未具备 critique/revision 所需的完整下游上下文。",
        )
        raise WorkspaceStateError(
            f"{issue.path}: {issue.message}",
            errors=[issue],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )
    return WorkspaceContext(
        document=document,
        selected_direction=state.selected_direction,
        selected_question=state.selected_question,
        active_argument_chain=state.active_argument_chain,
        active_fit_mapping=state.active_fit_mapping,
        active_draft=state.active_draft,
        active_revision_plan=state.active_revision_plan,
        active_critique=state.active_critique,
        reviewed_revision_plan=state.reviewed_revision_plan,
    )
