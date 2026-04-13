from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from med_autogrant.codex_cli import read_codex_cli_contract, run_codex_exec
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.workspace import (
    WorkspaceStateError,
    _SchemaSubsetValidator,
    _build_workspace_state,
    _collect_known_ids,
    validate_workspace_document,
)


CodexRunner = Callable[..., dict[str, Any]]


def build_direction_screening_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    codex_runner: CodexRunner = run_codex_exec,
) -> dict[str, Any]:
    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_direction_screening_prompt(
        input_path=input_path,
        known_ids=known_ids,
    )
    codex_payload, codex_contract = _run_codex_generation(
        prompt=prompt,
        input_path=input_path,
        codex_runner=codex_runner,
    )
    selected_direction_index = _require_nonnegative_int(
        codex_payload,
        "selected_direction_index",
        context="direction screening payload",
    )
    raw_directions = _require_object_list(
        codex_payload,
        "direction_hypotheses",
        context="direction screening payload",
    )
    if not 2 <= len(raw_directions) <= 5:
        raise WorkspaceStateError("direction screening 必须输出 2 到 5 个方向候选。")
    if selected_direction_index >= len(raw_directions):
        raise WorkspaceStateError("selected_direction_index 超出 direction_hypotheses 范围。")

    existing_direction_ids = [
        item.get("direction_id")
        for item in document.get("direction_hypotheses", [])
        if isinstance(item, dict) and isinstance(item.get("direction_id"), str)
    ]
    direction_ids = _allocate_sequence_ids("direction", len(raw_directions), existing_direction_ids)
    normalized_directions: list[dict[str, Any]] = []
    selected_direction_id = direction_ids[selected_direction_index]
    for index, raw_direction in enumerate(raw_directions):
        direction = {
            "metadata": _fresh_metadata(document),
            "direction_id": direction_ids[index],
            "title": _require_nonempty_string(raw_direction, "title", context="direction hypothesis"),
            "rationale": _require_nonempty_string(raw_direction, "rationale", context="direction hypothesis"),
            "knowledge_gap_summary": _require_nonempty_string(
                raw_direction,
                "knowledge_gap_summary",
                context="direction hypothesis",
            ),
            "applicant_fit_summary": _require_nonempty_string(
                raw_direction,
                "applicant_fit_summary",
                context="direction hypothesis",
            ),
            "novelty_angle": _optional_string(raw_direction, "novelty_angle"),
            "risk_summary": _optional_string(raw_direction, "risk_summary"),
            "required_evidence_ids": _require_known_string_list(
                raw_direction,
                "required_evidence_ids",
                known_ids=set(known_ids),
                context="direction hypothesis",
            ),
            "decision_status": "selected" if index == selected_direction_index else _normalize_direction_status(raw_direction),
        }
        _validate_schema_payload(
            direction,
            schema_file="direction-hypothesis.schema.json",
            grant_run_id=document["grant_run_id"],
            workspace_id=document["workspace_id"],
            lifecycle_stage="direction_screening",
        )
        normalized_directions.append(direction)

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "direction_screening"
    next_workspace["direction_hypotheses"] = normalized_directions
    next_workspace["scientific_question_cards"] = []
    next_workspace["argument_chains"] = []
    next_workspace["applicant_fit_mappings"] = []
    next_workspace["application_drafts"] = []
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction_id,
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": False,
        "argument_chain_frozen": False,
        "fit_alignment_frozen": False,
        "outline_frozen": False,
        "presubmission_frozen": False,
    }
    _prune_invalid_preliminary_supports(next_workspace)
    _validate_workspace_or_raise(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": None,
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "direction_screening_execution": {
            "executor": _build_codex_executor_payload(codex_contract),
            "selected_direction_id": selected_direction_id,
            "direction_count": len(normalized_directions),
        },
        "direction_screening_workspace": next_workspace,
    }


def build_question_refinement_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    codex_runner: CodexRunner = run_codex_exec,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    selected_direction = state.selected_direction
    if selected_direction is None:
        raise WorkspaceStateError("question refinement 需要当前 workspace 已绑定 selected direction。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_question_refinement_prompt(
        input_path=input_path,
        selected_direction=selected_direction,
        known_ids=known_ids,
    )
    codex_payload, codex_contract = _run_codex_generation(
        prompt=prompt,
        input_path=input_path,
        codex_runner=codex_runner,
    )
    raw_question = _require_mapping(
        codex_payload,
        "scientific_question_card",
        context="question refinement payload",
    )
    existing_question_ids = [
        item.get("question_id")
        for item in document.get("scientific_question_cards", [])
        if isinstance(item, dict) and isinstance(item.get("question_id"), str)
    ]
    question_id = _next_versioned_id("question", existing_question_ids)
    question = {
        "metadata": _fresh_metadata(document),
        "question_id": question_id,
        "parent_direction_id": selected_direction["direction_id"],
        "phenomenon": _optional_string(raw_question, "phenomenon"),
        "knowledge_boundary": _require_nonempty_string(
            raw_question,
            "knowledge_boundary",
            context="scientific question card",
        ),
        "unknown_mechanism": _require_nonempty_string(
            raw_question,
            "unknown_mechanism",
            context="scientific question card",
        ),
        "core_question": _require_nonempty_string(raw_question, "core_question", context="scientific question card"),
        "subquestions": _optional_string_list(raw_question, "subquestions"),
        "falsifiable_statement": _require_nonempty_string(
            raw_question,
            "falsifiable_statement",
            context="scientific question card",
        ),
        "proposed_breakthrough_angle": _require_nonempty_string(
            raw_question,
            "proposed_breakthrough_angle",
            context="scientific question card",
        ),
        "why_not_engineering": _require_nonempty_string(
            raw_question,
            "why_not_engineering",
            context="scientific question card",
        ),
        "why_now": _optional_string(raw_question, "why_now"),
        "linked_evidence_ids": _require_known_string_list(
            raw_question,
            "linked_evidence_ids",
            known_ids=set(known_ids),
            context="scientific question card",
        ),
    }
    _validate_schema_payload(
        question,
        schema_file="scientific-question-card.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="question_refinement",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "question_refinement"
    next_workspace["scientific_question_cards"] = [question]
    next_workspace["argument_chains"] = []
    next_workspace["applicant_fit_mappings"] = []
    next_workspace["application_drafts"] = []
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": question_id,
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": False,
        "fit_alignment_frozen": False,
        "outline_frozen": False,
        "presubmission_frozen": False,
    }
    _prune_invalid_preliminary_supports(next_workspace)
    _validate_workspace_or_raise(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": None,
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "question_refinement_execution": {
            "executor": _build_codex_executor_payload(codex_contract),
            "selected_direction_id": selected_direction["direction_id"],
            "selected_question_id": question_id,
        },
        "question_refinement_workspace": next_workspace,
    }


def build_argument_building_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    codex_runner: CodexRunner = run_codex_exec,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    selected_direction = state.selected_direction
    selected_question = state.selected_question
    if selected_direction is None or selected_question is None:
        raise WorkspaceStateError("argument building 需要当前 workspace 已绑定 direction 与 question。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_argument_building_prompt(
        input_path=input_path,
        selected_direction=selected_direction,
        selected_question=selected_question,
        known_ids=known_ids,
    )
    codex_payload, codex_contract = _run_codex_generation(
        prompt=prompt,
        input_path=input_path,
        codex_runner=codex_runner,
    )
    raw_argument = _require_mapping(
        codex_payload,
        "argument_chain",
        context="argument building payload",
    )
    existing_argument_ids = [
        item.get("argument_chain_id")
        for item in document.get("argument_chains", [])
        if isinstance(item, dict) and isinstance(item.get("argument_chain_id"), str)
    ]
    argument_chain_id = _next_versioned_id("argument", existing_argument_ids)
    argument_chain = {
        "metadata": _fresh_metadata(document),
        "argument_chain_id": argument_chain_id,
        "scientific_question_id": selected_question["question_id"],
        "background_claim": _require_nonempty_string(raw_argument, "background_claim", context="argument chain"),
        "field_gap": _require_nonempty_string(raw_argument, "field_gap", context="argument chain"),
        "necessity_claim": _require_nonempty_string(raw_argument, "necessity_claim", context="argument chain"),
        "uniqueness_claim": _require_nonempty_string(raw_argument, "uniqueness_claim", context="argument chain"),
        "route_justification": _require_nonempty_string(raw_argument, "route_justification", context="argument chain"),
        "non_arbitrary_route_reason": _optional_string(raw_argument, "non_arbitrary_route_reason"),
        "if_not_done_loss": _require_nonempty_string(raw_argument, "if_not_done_loss", context="argument chain"),
        "linked_evidence_ids": _require_known_string_list(
            raw_argument,
            "linked_evidence_ids",
            known_ids=set(known_ids),
            context="argument chain",
        ),
    }
    _validate_schema_payload(
        argument_chain,
        schema_file="argument-chain.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="argument_building",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "argument_building"
    next_workspace["argument_chains"] = [argument_chain]
    next_workspace["applicant_fit_mappings"] = []
    next_workspace["application_drafts"] = []
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": selected_question["question_id"],
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": True,
        "fit_alignment_frozen": False,
        "outline_frozen": False,
        "presubmission_frozen": False,
    }
    _prune_invalid_preliminary_supports(next_workspace)
    _validate_workspace_or_raise(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": None,
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "argument_building_execution": {
            "executor": _build_codex_executor_payload(codex_contract),
            "selected_question_id": selected_question["question_id"],
            "argument_chain_id": argument_chain_id,
        },
        "argument_building_workspace": next_workspace,
    }


def build_fit_alignment_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    codex_runner: CodexRunner = run_codex_exec,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    selected_direction = state.selected_direction
    selected_question = state.selected_question
    active_argument_chain = state.active_argument_chain
    if selected_direction is None or selected_question is None or active_argument_chain is None:
        raise WorkspaceStateError("fit alignment 需要当前 workspace 已具备 direction / question / argument。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_fit_alignment_prompt(
        input_path=input_path,
        selected_question=selected_question,
        active_argument_chain=active_argument_chain,
        known_ids=known_ids,
    )
    codex_payload, codex_contract = _run_codex_generation(
        prompt=prompt,
        input_path=input_path,
        codex_runner=codex_runner,
    )
    raw_fit_mapping = _require_mapping(
        codex_payload,
        "applicant_fit_mapping",
        context="fit alignment payload",
    )
    existing_fit_ids = [
        item.get("fit_mapping_id")
        for item in document.get("applicant_fit_mappings", [])
        if isinstance(item, dict) and isinstance(item.get("fit_mapping_id"), str)
    ]
    fit_mapping_id = _next_versioned_id("fit", existing_fit_ids)
    fit_mapping = {
        "metadata": _fresh_metadata(document),
        "fit_mapping_id": fit_mapping_id,
        "scientific_question_id": selected_question["question_id"],
        "argument_chain_id": active_argument_chain["argument_chain_id"],
        "applicant_fit_summary": _require_nonempty_string(
            raw_fit_mapping,
            "applicant_fit_summary",
            context="applicant fit mapping",
        ),
        "unique_advantage": _require_nonempty_string(
            raw_fit_mapping,
            "unique_advantage",
            context="applicant fit mapping",
        ),
        "methods_readiness": _require_nonempty_string(
            raw_fit_mapping,
            "methods_readiness",
            context="applicant fit mapping",
        ),
        "resource_readiness": _require_nonempty_string(
            raw_fit_mapping,
            "resource_readiness",
            context="applicant fit mapping",
        ),
        "risk_mitigation": _require_nonempty_string(
            raw_fit_mapping,
            "risk_mitigation",
            context="applicant fit mapping",
        ),
        "linked_evidence_ids": _require_known_string_list(
            raw_fit_mapping,
            "linked_evidence_ids",
            known_ids=set(known_ids),
            context="applicant fit mapping",
        ),
    }
    _validate_schema_payload(
        fit_mapping,
        schema_file="applicant-fit-mapping.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="fit_alignment",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "fit_alignment"
    next_workspace["applicant_fit_mappings"] = [fit_mapping]
    next_workspace["application_drafts"] = []
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": selected_question["question_id"],
        "active_fit_mapping_id": fit_mapping_id,
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": True,
        "fit_alignment_frozen": True,
        "outline_frozen": False,
        "presubmission_frozen": False,
    }
    _prune_invalid_preliminary_supports(next_workspace)
    _validate_workspace_or_raise(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": None,
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "fit_alignment_execution": {
            "executor": _build_codex_executor_payload(codex_contract),
            "selected_question_id": selected_question["question_id"],
            "active_fit_mapping_id": fit_mapping_id,
        },
        "fit_alignment_workspace": next_workspace,
    }


def build_outline_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    codex_runner: CodexRunner = run_codex_exec,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    selected_direction = state.selected_direction
    selected_question = state.selected_question
    active_argument_chain = state.active_argument_chain
    active_fit_mapping = state.active_fit_mapping
    if (
        selected_direction is None
        or selected_question is None
        or active_argument_chain is None
        or active_fit_mapping is None
    ):
        raise WorkspaceStateError("outline 需要当前 workspace 已具备 direction / question / argument / fit。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_outline_prompt(
        input_path=input_path,
        selected_question=selected_question,
        active_argument_chain=active_argument_chain,
        active_fit_mapping=active_fit_mapping,
        known_ids=known_ids,
    )
    codex_payload, codex_contract = _run_codex_generation(
        prompt=prompt,
        input_path=input_path,
        codex_runner=codex_runner,
    )
    raw_draft = _require_mapping(codex_payload, "application_draft", context="outline payload")
    raw_outline = _require_object_list(raw_draft, "outline", context="outline payload.application_draft")
    if not raw_outline:
        raise WorkspaceStateError("outline 需要输出非空提纲。")

    existing_draft_ids = [
        item.get("draft_id")
        for item in document.get("application_drafts", [])
        if isinstance(item, dict) and isinstance(item.get("draft_id"), str)
    ]
    draft_id = state.active_draft["draft_id"] if isinstance(state.active_draft, dict) else _next_versioned_id("draft", existing_draft_ids)
    outline = []
    for raw_section in raw_outline:
        section = {
            "section_key": _require_nonempty_string(raw_section, "section_key", context="draft outline item"),
            "section_title": _require_nonempty_string(raw_section, "section_title", context="draft outline item"),
            "core_claim": _require_nonempty_string(raw_section, "core_claim", context="draft outline item"),
            "linked_object_ids": _require_known_string_list(
                raw_section,
                "linked_object_ids",
                known_ids=set(known_ids),
                context="draft outline item",
            ),
        }
        outline.append(section)

    draft = {
        "metadata": _fresh_metadata(document),
        "draft_id": draft_id,
        "version_label": "v0.1",
        "project_title": _require_nonempty_string(raw_draft, "project_title", context="application draft"),
        "status": "outline",
        "frozen_question_id": selected_question["question_id"],
        "outline": outline,
        "sections": [],
    }
    _validate_schema_payload(
        draft,
        schema_file="application-draft.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="outline",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "outline"
    next_workspace["application_drafts"] = [draft]
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": selected_question["question_id"],
        "active_fit_mapping_id": active_fit_mapping["fit_mapping_id"],
        "active_draft_id": draft_id,
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": True,
        "fit_alignment_frozen": True,
        "outline_frozen": True,
        "presubmission_frozen": False,
    }
    _prune_invalid_preliminary_supports(next_workspace)
    _validate_workspace_or_raise(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": draft_id,
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "outline_execution": {
            "executor": _build_codex_executor_payload(codex_contract),
            "active_fit_mapping_id": active_fit_mapping["fit_mapping_id"],
            "draft_id": draft_id,
            "outline_count": len(outline),
        },
        "outline_workspace": next_workspace,
    }


def build_drafting_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    codex_runner: CodexRunner = run_codex_exec,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    selected_direction = state.selected_direction
    selected_question = state.selected_question
    active_argument_chain = state.active_argument_chain
    active_fit_mapping = state.active_fit_mapping
    active_draft = state.active_draft
    if (
        selected_direction is None
        or selected_question is None
        or active_argument_chain is None
        or active_fit_mapping is None
        or active_draft is None
    ):
        raise WorkspaceStateError("drafting 需要当前 workspace 已具备 direction / question / argument / fit / draft。")

    known_ids = sorted(_collect_known_ids(document))
    prompt = _build_drafting_prompt(
        input_path=input_path,
        active_draft=active_draft,
        selected_question=selected_question,
        active_argument_chain=active_argument_chain,
        active_fit_mapping=active_fit_mapping,
        known_ids=known_ids,
    )
    codex_payload, codex_contract = _run_codex_generation(
        prompt=prompt,
        input_path=input_path,
        codex_runner=codex_runner,
    )
    raw_draft = _require_mapping(codex_payload, "application_draft", context="drafting payload")
    raw_sections = _require_object_list(raw_draft, "sections", context="drafting payload.application_draft")
    if not raw_sections:
        raise WorkspaceStateError("drafting 需要输出非空正文 sections。")

    sections = []
    for raw_section in raw_sections:
        section = {
            "section_key": _require_nonempty_string(raw_section, "section_key", context="draft section"),
            "section_title": _require_nonempty_string(raw_section, "section_title", context="draft section"),
            "text": _require_nonempty_string(raw_section, "text", context="draft section"),
            "linked_object_ids": _require_known_string_list(
                raw_section,
                "linked_object_ids",
                known_ids=set(known_ids),
                context="draft section",
            ),
        }
        sections.append(section)

    draft = deepcopy(active_draft)
    draft["metadata"] = _fresh_metadata(document)
    draft["project_title"] = _require_nonempty_string(raw_draft, "project_title", context="application draft")
    draft["version_label"] = _bump_version_label(str(active_draft.get("version_label") or "v0.1"))
    draft["status"] = "draft"
    draft["sections"] = sections
    _validate_schema_payload(
        draft,
        schema_file="application-draft.schema.json",
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        lifecycle_stage="drafting",
    )

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "drafting"
    next_workspace["application_drafts"] = [draft]
    next_workspace["mentor_critiques"] = []
    next_workspace["revision_plans"] = []
    next_workspace["current_selection"] = {
        "selected_direction_id": selected_direction["direction_id"],
        "selected_question_id": selected_question["question_id"],
        "active_fit_mapping_id": active_fit_mapping["fit_mapping_id"],
        "active_draft_id": draft["draft_id"],
    }
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": True,
        "fit_alignment_frozen": True,
        "outline_frozen": True,
        "presubmission_frozen": False,
    }
    _prune_invalid_preliminary_supports(next_workspace)
    _validate_workspace_or_raise(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": draft["draft_id"],
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "drafting_execution": {
            "executor": _build_codex_executor_payload(codex_contract),
            "draft_id": draft["draft_id"],
            "version_label": draft["version_label"],
            "section_count": len(sections),
        },
        "drafting_workspace": next_workspace,
    }


def build_freeze_execution_document(
    *,
    document: dict[str, Any],
) -> dict[str, Any]:
    validation = validate_workspace_document(document)
    if not validation.ok:
        first_issue = validation.errors[0]
        raise WorkspaceStateError(
            f"{first_issue.path}: {first_issue.message}",
            errors=validation.errors,
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    state = _build_workspace_state(document)
    active_critique = state.active_critique
    active_revision_plan = state.active_revision_plan
    active_draft = state.active_draft
    if active_critique is None or active_revision_plan is None or active_draft is None:
        raise WorkspaceStateError("freeze pass 需要 critique / revision / draft 上下文。")
    if active_critique.get("verdict") != "ready_for_submission":
        raise WorkspaceStateError("freeze pass 只允许从 verdict=ready_for_submission 的 workspace 进入。")
    if active_revision_plan.get("execution_status") != "completed":
        raise WorkspaceStateError("freeze pass 要求 active RevisionPlan.execution_status=completed。")
    if active_draft.get("status") not in {"revised", "frozen"}:
        raise WorkspaceStateError("freeze pass 要求激活草稿已处于 revised 或 frozen。")

    next_workspace = deepcopy(document)
    next_workspace["metadata"] = _fresh_metadata(document)
    next_workspace["lifecycle_stage"] = "frozen"
    next_workspace["gates"] = {
        "direction_frozen": True,
        "scientific_question_frozen": True,
        "argument_chain_frozen": True,
        "fit_alignment_frozen": True,
        "outline_frozen": True,
        "presubmission_frozen": True,
    }
    for draft in next_workspace.get("application_drafts", []):
        if isinstance(draft, dict) and draft.get("draft_id") == active_draft["draft_id"]:
            draft["metadata"] = _fresh_metadata(document)
            draft["status"] = "frozen"
    _prune_invalid_preliminary_supports(next_workspace)
    _validate_workspace_or_raise(next_workspace)

    return {
        "grant_run_id": next_workspace["grant_run_id"],
        "workspace_id": next_workspace["workspace_id"],
        "draft_id": active_draft["draft_id"],
        "lifecycle_stage": next_workspace["lifecycle_stage"],
        "freeze_execution": {
            "executor": {
                "kind": "deterministic_domain_logic",
                "model": None,
                "reasoning_effort": None,
            },
            "draft_id": active_draft["draft_id"],
            "revision_plan_id": active_revision_plan["revision_plan_id"],
            "critique_id": active_critique["critique_id"],
        },
        "frozen_workspace": next_workspace,
    }


def _build_direction_screening_prompt(*, input_path: str | Path, known_ids: list[str]) -> str:
    direction_schema = (SchemaStore().root / "direction-hypothesis.schema.json").resolve()
    return _build_prompt(
        input_path=input_path,
        schema_paths=[direction_schema],
        output_contract_lines=[
            'Return exactly one JSON object with keys "selected_direction_index" and "direction_hypotheses".',
            '"selected_direction_index" must be a zero-based integer pointing at the chosen mainline direction.',
            '"direction_hypotheses" must be a list of 2 to 5 objects.',
            "Each direction object must include: title, rationale, knowledge_gap_summary, applicant_fit_summary, novelty_angle, risk_summary, required_evidence_ids.",
        ],
        hard_constraints=[
            f"required_evidence_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "Choose one direction with the strongest continuity from existing outputs, active projects, and preliminary evidence.",
            "Novelty must absorb 1-2 hotspots naturally into the mainline instead of packaging buzzwords.",
            "Prefer concrete clinical problems over broad slogans.",
        ],
        quality_goals=[
            "Select a direction with real continuity, not a temporary splice.",
            "Make the selected direction specific enough to support a mechanism-level question next.",
        ],
    )


def _build_question_refinement_prompt(
    *,
    input_path: str | Path,
    selected_direction: dict[str, Any],
    known_ids: list[str],
) -> str:
    question_schema = (SchemaStore().root / "scientific-question-card.schema.json").resolve()
    return _build_prompt(
        input_path=input_path,
        schema_paths=[question_schema],
        output_contract_lines=[
            'Return exactly one JSON object with key "scientific_question_card".',
            "The card must include: knowledge_boundary, unknown_mechanism, core_question, falsifiable_statement, proposed_breakthrough_angle, why_not_engineering.",
            "Optional fields: phenomenon, subquestions, why_now, linked_evidence_ids.",
        ],
        hard_constraints=[
            f"parent direction title: {selected_direction['title']}",
            f"linked_evidence_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "The question must be specific, clinically anchored, and answerable.",
            "The question must close onto one concrete mechanism rather than a broad theme.",
        ],
        quality_goals=[
            "Turn the selected direction into a precise, falsifiable scientific question.",
            "Explain clearly why this is a mechanism question rather than an engineering task.",
        ],
    )


def _build_argument_building_prompt(
    *,
    input_path: str | Path,
    selected_direction: dict[str, Any],
    selected_question: dict[str, Any],
    known_ids: list[str],
) -> str:
    argument_schema = (SchemaStore().root / "argument-chain.schema.json").resolve()
    return _build_prompt(
        input_path=input_path,
        schema_paths=[argument_schema],
        output_contract_lines=[
            'Return exactly one JSON object with key "argument_chain".',
            "The chain must include: background_claim, field_gap, necessity_claim, uniqueness_claim, route_justification, if_not_done_loss.",
            "Optional fields: non_arbitrary_route_reason, linked_evidence_ids.",
        ],
        hard_constraints=[
            f"selected direction: {selected_direction['title']}",
            f"selected question: {selected_question['core_question']}",
            f"linked_evidence_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "The argument chain must support a 'write significance first, background later' authoring order.",
            "Route justification must explain why the validation loop is not arbitrary.",
        ],
        quality_goals=[
            "Close the necessity/scientific value mainline before the draft expands.",
            "Tie the background, evidence gap, and route design into one coherent chain.",
        ],
    )


def _build_fit_alignment_prompt(
    *,
    input_path: str | Path,
    selected_question: dict[str, Any],
    active_argument_chain: dict[str, Any],
    known_ids: list[str],
) -> str:
    fit_schema = (SchemaStore().root / "applicant-fit-mapping.schema.json").resolve()
    return _build_prompt(
        input_path=input_path,
        schema_paths=[fit_schema],
        output_contract_lines=[
            'Return exactly one JSON object with key "applicant_fit_mapping".',
            "The mapping must include: applicant_fit_summary, unique_advantage, methods_readiness, resource_readiness, risk_mitigation.",
            "Optional field: linked_evidence_ids.",
        ],
        hard_constraints=[
            f"selected question: {selected_question['core_question']}",
            f"necessity claim anchor: {active_argument_chain['necessity_claim']}",
            f"linked_evidence_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "Fit must be evidence-backed and explicit about why this applicant is the right person to do this problem now.",
        ],
        quality_goals=[
            "Bind applicant, methods, resources, and risk control to the exact scientific question.",
            "Avoid resume-stacking; explain irreplaceable fit instead.",
        ],
    )


def _build_outline_prompt(
    *,
    input_path: str | Path,
    selected_question: dict[str, Any],
    active_argument_chain: dict[str, Any],
    active_fit_mapping: dict[str, Any],
    known_ids: list[str],
) -> str:
    draft_schema = (SchemaStore().root / "application-draft.schema.json").resolve()
    return _build_prompt(
        input_path=input_path,
        schema_paths=[draft_schema],
        output_contract_lines=[
            'Return exactly one JSON object with key "application_draft".',
            'The draft must include "project_title" and a non-empty "outline" list.',
            "Each outline item must include: section_key, section_title, core_claim, linked_object_ids.",
        ],
        hard_constraints=[
            f"selected question: {selected_question['core_question']}",
            f"necessity claim: {active_argument_chain['necessity_claim']}",
            f"applicant fit anchor: {active_fit_mapping['applicant_fit_summary']}",
            f"linked_object_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "Order the outline around the mainline: significance / background / preliminary support / research content / technical route / innovation / expected outcomes / timeline as needed.",
            "The outline should make later background, pre-experiment, progress, and figure writing straightforward.",
        ],
        quality_goals=[
            "Produce an outline that follows the human writing workflow instead of padding every section up front.",
            "Keep every section explicitly tied to the frozen question, argument chain, and applicant fit.",
        ],
    )


def _build_drafting_prompt(
    *,
    input_path: str | Path,
    active_draft: dict[str, Any],
    selected_question: dict[str, Any],
    active_argument_chain: dict[str, Any],
    active_fit_mapping: dict[str, Any],
    known_ids: list[str],
) -> str:
    draft_schema = (SchemaStore().root / "application-draft.schema.json").resolve()
    return _build_prompt(
        input_path=input_path,
        schema_paths=[draft_schema],
        output_contract_lines=[
            'Return exactly one JSON object with key "application_draft".',
            'The draft must include "project_title" and a non-empty "sections" list.',
            "Each section must include: section_key, section_title, text, linked_object_ids.",
        ],
        hard_constraints=[
            f"outline section keys: {json.dumps([item.get('section_key') for item in active_draft.get('outline', []) if isinstance(item, dict)], ensure_ascii=False)}",
            f"selected question: {selected_question['core_question']}",
            f"necessity claim: {active_argument_chain['necessity_claim']}",
            f"applicant fit anchor: {active_fit_mapping['applicant_fit_summary']}",
            f"linked_object_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "Draft the sections faithfully from the frozen outline instead of introducing a new structure.",
            "Background, preliminary evidence, technical route, expected outcomes, progress, and figure-facing cues should all serve the same mainline.",
        ],
        quality_goals=[
            "Expand the outline into a proposal-facing draft without breaking the frozen question and upstream logic.",
            "Keep the section texts concrete, evidence-linked, and ready for critique/revision.",
        ],
    )


def _build_prompt(
    *,
    input_path: str | Path,
    schema_paths: list[Path],
    output_contract_lines: list[str],
    hard_constraints: list[str],
    quality_goals: list[str],
) -> str:
    input_file = Path(input_path).expanduser().resolve()
    lines = [
        "You are executing a MedAutoGrant authoring pass.",
        "Read the workspace JSON and the referenced schema files from disk before you answer.",
        "Do not modify any files. Return JSON only, with no markdown fences.",
        "",
        f"Workspace file: {input_file}",
    ]
    for schema_path in schema_paths:
        lines.append(f"Schema file: {schema_path}")
    lines.extend(
        [
            "",
            "Output contract:",
            *[f"- {line}" for line in output_contract_lines],
            "",
            "Hard constraints:",
            *[f"- {line}" for line in hard_constraints],
            "",
            "Quality goal:",
            *[f"- {line}" for line in quality_goals],
        ]
    )
    return "\n".join(lines)


def _run_codex_generation(
    *,
    prompt: str,
    input_path: str | Path,
    codex_runner: CodexRunner,
) -> tuple[dict[str, Any], dict[str, Any]]:
    codex_contract = read_codex_cli_contract()
    payload = codex_runner(
        prompt,
        cwd=Path(input_path).expanduser().resolve().parent,
    )
    if not isinstance(payload, dict):
        raise WorkspaceStateError("Codex authoring pass 返回值必须是 object。")
    return payload, codex_contract


def _build_codex_executor_payload(codex_contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "codex_cli",
        "model": codex_contract["model_selection"],
        "reasoning_effort": codex_contract["reasoning_selection"],
    }


def _fresh_metadata(document: dict[str, Any]) -> dict[str, Any]:
    source_mode = document.get("mode")
    return {
        "schema_version": "v1",
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
        "source_mode": source_mode if isinstance(source_mode, str) and source_mode else "auto",
        "owner": "Med Auto Grant authoring executor",
    }


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _allocate_sequence_ids(prefix: str, count: int, existing_ids: list[str]) -> list[str]:
    used = set(existing_ids)
    allocated: list[str] = []
    index = 1
    while len(allocated) < count:
        candidate = f"{prefix}-v{index}"
        if candidate not in used:
            used.add(candidate)
            allocated.append(candidate)
        index += 1
    return allocated


def _next_versioned_id(prefix: str, existing_ids: list[str]) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}-v(\d+)$")
    max_index = 0
    for value in existing_ids:
        match = pattern.match(value)
        if match:
            max_index = max(max_index, int(match.group(1)))
    return f"{prefix}-v{max_index + 1}"


def _bump_version_label(value: str) -> str:
    match = re.match(r"^v(\d+)\.(\d+)$", value.strip())
    if not match:
        return "v0.2"
    major = int(match.group(1))
    minor = int(match.group(2))
    return f"v{major}.{minor + 1}"


def _normalize_direction_status(payload: dict[str, Any]) -> str:
    status = payload.get("decision_status")
    if status in {"candidate", "rejected", "deferred"}:
        return str(status)
    return "deferred"


def _prune_invalid_preliminary_supports(document: dict[str, Any]) -> None:
    known_ids = _collect_known_ids(document)
    evidence_items = document.get("preliminary_evidence_pack", {}).get("evidence_items", [])
    for item in evidence_items:
        if not isinstance(item, dict):
            continue
        supports = item.get("supports")
        if not isinstance(supports, list):
            continue
        item["supports"] = [value for value in supports if isinstance(value, str) and value in known_ids]


def _validate_workspace_or_raise(document: dict[str, Any]) -> None:
    validation = validate_workspace_document(document)
    if validation.ok:
        return
    first_issue = validation.errors[0]
    raise WorkspaceStateError(
        f"{first_issue.path}: {first_issue.message}",
        errors=validation.errors,
        grant_run_id=document.get("grant_run_id"),
        workspace_id=document.get("workspace_id"),
        lifecycle_stage=document.get("lifecycle_stage"),
    )


def _validate_schema_payload(
    payload: dict[str, Any],
    *,
    schema_file: str,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    issues = _SchemaSubsetValidator(SchemaStore()).validate(payload, schema_file)
    if not issues:
        return
    detail = "; ".join(f"{issue.path}: {issue.message}" for issue in issues[:5])
    raise WorkspaceStateError(
        f"{schema_file} 校验失败: {detail}",
        errors=issues,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _require_mapping(payload: dict[str, Any], key: str, *, context: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise WorkspaceStateError(f"{context} 缺少 object 字段: {key}")
    return value


def _require_object_list(payload: dict[str, Any], key: str, *, context: str) -> list[dict[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise WorkspaceStateError(f"{context} 缺少 object list 字段: {key}")
    return list(value)


def _require_nonnegative_int(payload: dict[str, Any], key: str, *, context: str) -> int:
    value = payload.get(key)
    if not isinstance(value, int) or value < 0:
        raise WorkspaceStateError(f"{context} 缺少非负整数字段: {key}")
    return value


def _require_nonempty_string(payload: dict[str, Any], key: str, *, context: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少非空字符串字段: {key}")
    return value.strip()


def _optional_string(payload: dict[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"字段 {key} 必须为非空字符串或省略。")
    return value.strip()


def _optional_string_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise WorkspaceStateError(f"字段 {key} 必须为字符串列表或省略。")
    return [item.strip() for item in value]


def _require_known_string_list(
    payload: dict[str, Any],
    key: str,
    *,
    known_ids: set[str],
    context: str,
) -> list[str]:
    values = _optional_string_list(payload, key)
    unknown_ids = [value for value in values if value not in known_ids]
    if unknown_ids:
        raise WorkspaceStateError(f"{context}.{key} 引用了未知对象: {unknown_ids}")
    return values
