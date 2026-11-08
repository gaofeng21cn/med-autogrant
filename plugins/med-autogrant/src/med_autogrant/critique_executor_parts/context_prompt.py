from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from med_autogrant.critique_policy import (
    build_policy_prompt_lines,
    build_weight_contract,
    resolve_critique_policy_from_document,
)
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.workspace_types import WorkspaceStateError


def build_critique_context(
    *,
    document: dict[str, Any],
    state: Any,
    collect_known_ids: Callable[[dict[str, Any]], set[str]],
    next_versioned_id: Callable[[str, list[str]], str],
) -> dict[str, Any]:
    lifecycle_stage = str(document.get("lifecycle_stage") or "").strip()
    if lifecycle_stage not in {"drafting", "revision"}:
        raise WorkspaceStateError(
            f"execute-critique-pass 只允许从 drafting 或 revision 进入，当前为 {lifecycle_stage or 'unknown'}。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    if state.selected_question is None or state.active_argument_chain is None or state.active_fit_mapping is None:
        raise WorkspaceStateError(
            "critique pass 缺少 question / argument / fit 上下文。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )
    if state.active_draft is None:
        raise WorkspaceStateError(
            "critique pass 缺少 active draft。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )
    if lifecycle_stage == "revision":
        if state.active_revision_plan is None or state.active_critique is None:
            raise WorkspaceStateError(
                "revision -> critique re-review 缺少 active revision / critique 上下文。",
                errors=[],
                grant_run_id=document.get("grant_run_id"),
                workspace_id=document.get("workspace_id"),
                lifecycle_stage=document.get("lifecycle_stage"),
            )
        if state.active_revision_plan.get("execution_status") != "completed":
            raise WorkspaceStateError(
                "revision -> critique re-review 要求当前 active RevisionPlan.execution_status=completed。",
                errors=[],
                grant_run_id=document.get("grant_run_id"),
                workspace_id=document.get("workspace_id"),
                lifecycle_stage=document.get("lifecycle_stage"),
            )
        if state.active_draft.get("status") != "revised":
            raise WorkspaceStateError(
                "revision -> critique re-review 要求当前 active draft.status=revised。",
                errors=[],
                grant_run_id=document.get("grant_run_id"),
                workspace_id=document.get("workspace_id"),
                lifecycle_stage=document.get("lifecycle_stage"),
            )

    existing_critique_ids = [
        item.get("critique_id")
        for item in document.get("mentor_critiques", [])
        if isinstance(item, dict) and isinstance(item.get("critique_id"), str)
    ]
    existing_revision_plan_ids = [
        item.get("revision_plan_id")
        for item in document.get("revision_plans", [])
        if isinstance(item, dict) and isinstance(item.get("revision_plan_id"), str)
    ]
    section_keys = [
        section.get("section_key")
        for section in state.active_draft.get("sections", [])
        if isinstance(section, dict) and isinstance(section.get("section_key"), str)
    ]
    known_ids = sorted(collect_known_ids(document))
    return {
        "document": document,
        "lifecycle_stage": lifecycle_stage,
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "draft_id": state.active_draft["draft_id"],
        "draft_version_label": state.active_draft["version_label"],
        "selected_question": state.selected_question,
        "active_argument_chain": state.active_argument_chain,
        "active_fit_mapping": state.active_fit_mapping,
        "active_draft": state.active_draft,
        "active_revision_plan": state.active_revision_plan,
        "active_critique": state.active_critique,
        "existing_critique_ids": existing_critique_ids,
        "existing_revision_plan_ids": existing_revision_plan_ids,
        "section_keys": section_keys,
        "known_ids": known_ids,
        "next_critique_id": next_versioned_id("critique", existing_critique_ids),
        "next_revision_plan_id": next_versioned_id("revision", existing_revision_plan_ids),
    }


def build_critique_prompt(
    *,
    context: dict[str, Any],
    input_path: str | Path,
    require_object: Callable[[dict[str, Any], str], dict[str, Any]],
    resolve_policy: Callable[[dict[str, Any]], dict[str, Any]] = resolve_critique_policy_from_document,
    build_policy_lines: Callable[[dict[str, Any]], list[str]] = build_policy_prompt_lines,
    build_weights: Callable[[dict[str, Any]], dict[str, int]] = build_weight_contract,
    schema_store_factory: type[SchemaStore] = SchemaStore,
) -> str:
    input_file = Path(input_path).expanduser().resolve()
    mentor_schema = (schema_store_factory().root / "mentor-critique.schema.json").resolve()
    revision_schema = (schema_store_factory().root / "revision-plan.schema.json").resolve()
    critique_policy = resolve_policy(require_object(context, "document"))
    policy_lines = build_policy_lines(critique_policy)
    weight_contract = build_weights(critique_policy)
    weight_split = ", ".join(f"{field}={weight}" for field, weight in weight_contract.items())
    weighted_score_fields = " / ".join(weight_contract)
    reviewed_revision_id = None
    if isinstance(context["active_revision_plan"], dict) and context["lifecycle_stage"] == "revision":
        reviewed_revision_id = context["active_revision_plan"]["revision_plan_id"]

    return "\n".join(
        [
            "You are executing the MedAutoGrant critique pass.",
            "Read the workspace JSON and the two schema files from disk before you answer.",
            "Do not modify any files. Return JSON only, with no markdown fences.",
            "",
            f"Workspace file: {input_file}",
            f"MentorCritique schema: {mentor_schema}",
            f"RevisionPlan schema: {revision_schema}",
            "",
            "Output contract:",
            (
                'Return exactly one JSON object shaped as '
                '{"surface_kind":"domain_stage_closeout_packet",'
                '"route_id":"critique","domain_output_kind":"mag_critique_output",'
                '"domain_output":{...}}.'
            ),
            'domain_output must contain exactly the keys "mentor_critique" and "revision_plan".',
            "",
            "Critique policy/persona contract:",
            *policy_lines,
            "",
            "Hard constraints:",
            f"- lifecycle stage entering critique pass: {context['lifecycle_stage']}",
            f"- draft_id must be {context['draft_id']}",
            f"- next critique_id should be {context['next_critique_id']}",
            f"- next revision_plan_id should be {context['next_revision_plan_id']}",
            f"- current scientific question must stay exactly: {context['selected_question']['core_question']}",
            f"- current draft version_label is {context['draft_version_label']}",
            f"- allowed draft section keys: {json.dumps(context['section_keys'], ensure_ascii=False)}",
            f"- known object ids for required_input_ids / linked_object_ids: {json.dumps(context['known_ids'], ensure_ascii=False)}",
            "- choose repair actions and scope from the actual diagnosis; cross-section restructuring and upstream route-back are allowed when the argument cannot be repaired locally",
            "- target_ref and required_input_ids must make every proposed repair traceable to the affected artifact and known evidence",
            "- every planned repair needs a directly applicable mutation_payload; choose section scope or whole-draft sections scope from the diagnosis and attached schema",
            f"- preserve these profile reporting weights in the schema fields: {weight_split}",
            (
                f"- mentor_critique.{weighted_score_fields} must each be "
                "an object with exactly weight, score, judgment"
            ),
            "- do not emit rationale or verdict inside these weighted score blocks",
            "- do not invent comparison_summary for a planned revision plan",
            "- set revision_plan.execution_status to planned",
            "- revision_plan.pre_revision_version_label must equal the current draft version_label",
            "- revision_plan.post_revision_version_label must be a new non-empty version label different from the current one",
            (
                f"- mentor_critique.reviewed_revision_plan_id must be {reviewed_revision_id}"
                if reviewed_revision_id is not None
                else "- omit mentor_critique.reviewed_revision_plan_id for the first critique pass"
            ),
            "",
            "Quality goal:",
            "- produce an independent reviewer judgment over the whole proposal, not a weighted checklist traversal",
            "- produce the smallest coherent repair plan; prefer cross-section coherence over a fixed mutation taxonomy",
        ]
    )
