from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from med_autogrant.codex_cli import read_codex_cli_contract, run_codex_exec
from med_autogrant import authoring_executor_parts as _authoring_executor_parts
from med_autogrant.facade_exports import re_export_public_names
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.workspace import (
    WorkspaceStateError,
    _SchemaSubsetValidator,
    _build_workspace_state,
    _collect_known_ids,
    materialize_workspace_surfaces,
    validate_workspace_document,
)

re_export_public_names(_authoring_executor_parts, globals())


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
    next_workspace = _finalize_execution_workspace(next_workspace)

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
    next_workspace = _finalize_execution_workspace(next_workspace)

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
    next_workspace = _finalize_execution_workspace(next_workspace)

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
    next_workspace = _finalize_execution_workspace(next_workspace)

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
    next_workspace = _finalize_execution_workspace(next_workspace)

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
    next_workspace = _finalize_execution_workspace(next_workspace)

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
    next_workspace = _finalize_execution_workspace(next_workspace)

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



















































