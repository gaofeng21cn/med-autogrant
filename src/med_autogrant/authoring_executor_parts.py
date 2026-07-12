from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from med_autogrant.domain_executor_client import (
    ExecutorRunner,
    run_domain_executor,
)
from opl_framework.schema_validation import SchemaSubsetValidator as _SchemaSubsetValidator
from med_autogrant.workspace import (
    materialize_workspace_surfaces,
)
from med_autogrant.workspace_reference_validation import _collect_known_ids
from med_autogrant.workspace_types import WorkspaceStateError
from med_autogrant.workspace_validation import validate_workspace_document
from med_autogrant.schema_loader import SchemaStore

def _build_direction_screening_prompt(*, input_path: str | Path, known_ids: list[str]) -> str:
    direction_schema = (SchemaStore().root / "direction-hypothesis.schema.json").resolve()
    return _build_prompt(
        route_id="direction_screening",
        input_path=input_path,
        schema_paths=[direction_schema],
        output_contract_lines=[
            'domain_output must contain exactly the keys "selected_direction_index" and "direction_hypotheses".',
            '"selected_direction_index" must be a zero-based integer pointing at the chosen mainline direction.',
            '"direction_hypotheses" must be a non-empty list; use multiple candidates only when comparison improves the decision.',
            "Each direction object must include: title, rationale, knowledge_gap_summary, applicant_fit_summary, novelty_angle, risk_summary, required_evidence_ids.",
        ],
        hard_constraints=[
            f"required_evidence_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "Choose one direction with the strongest continuity from existing outputs, active projects, and preliminary evidence.",
            "Novelty must follow from the call, evidence, and applicant advantage instead of packaging buzzwords.",
            "Prefer concrete clinical problems over broad slogans.",
        ],
        quality_goals=[
            "Select a direction with real continuity, not a temporary splice.",
            "Make the selected direction specific enough to support a mechanism-level question next.",
        ],
    )


def _build_strategy_authoring_prompt(*, input_path: str | Path, known_ids: list[str]) -> str:
    schema_root = SchemaStore().root
    return _build_prompt(
        route_id="strategy_authoring",
        input_path=input_path,
        schema_paths=[
            (schema_root / name).resolve()
            for name in (
                "direction-hypothesis.schema.json",
                "scientific-question-card.schema.json",
                "argument-chain.schema.json",
                "applicant-fit-mapping.schema.json",
                "application-draft.schema.json",
            )
        ],
        output_contract_lines=[
            "domain_output must contain selected_direction_index, direction_hypotheses, scientific_question_card, argument_chain, applicant_fit_mapping, and application_draft.",
            "application_draft must contain a non-empty outline and non-empty sections; the other objects follow their attached schemas.",
        ],
        hard_constraints=[
            f"All evidence and linked object refs may use only source ids already known at intake: {json.dumps(known_ids, ensure_ascii=False)}",
            "Keep the locked funding call, eligibility, source facts, and applicant evidence unchanged.",
            "Return one mutually coherent strategy and reviewable draft; do not fabricate evidence, citations, capacity, or results.",
        ],
        quality_goals=[
            "Let direction, scientific question, argument, applicant fit, outline, and draft converge together instead of treating route labels as a fixed reasoning sequence.",
            "Use an outline as a strong planning default while revising it inside this call when drafting exposes a real structural defect.",
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
        route_id="question_refinement",
        input_path=input_path,
        schema_paths=[question_schema],
        output_contract_lines=[
            'domain_output must contain exactly the key "scientific_question_card".',
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
        route_id="argument_building",
        input_path=input_path,
        schema_paths=[argument_schema],
        output_contract_lines=[
            'domain_output must contain exactly the key "argument_chain".',
            "The chain must include: background_claim, field_gap, necessity_claim, uniqueness_claim, route_justification, if_not_done_loss.",
            "Optional fields: non_arbitrary_route_reason, linked_evidence_ids.",
        ],
        hard_constraints=[
            f"selected direction: {selected_direction['title']}",
            f"selected question: {selected_question['core_question']}",
            f"linked_evidence_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "Route justification must explain why the validation loop is not arbitrary.",
        ],
        quality_goals=[
            "Make necessity and scientific value clear enough to guide the draft.",
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
        route_id="fit_alignment",
        input_path=input_path,
        schema_paths=[fit_schema],
        output_contract_lines=[
            'domain_output must contain exactly the key "applicant_fit_mapping".',
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
        route_id="outline",
        input_path=input_path,
        schema_paths=[draft_schema],
        output_contract_lines=[
            'domain_output must contain exactly the key "application_draft".',
            'The draft must include "project_title" and a non-empty "outline" list.',
            "Each outline item must include: section_key, section_title, core_claim, linked_object_ids.",
        ],
        hard_constraints=[
            f"selected question: {selected_question['core_question']}",
            f"necessity claim: {active_argument_chain['necessity_claim']}",
            f"applicant fit anchor: {active_fit_mapping['applicant_fit_summary']}",
            f"linked_object_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "Choose and order sections from the locked call and argument needs; do not impose one global section order.",
            "The outline should make later background, pre-experiment, progress, and figure writing straightforward.",
        ],
        quality_goals=[
            "Produce an outline that follows the human writing workflow instead of padding every section up front.",
            "Keep every section explicitly tied to the converged question, argument chain, and applicant fit.",
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
        route_id="drafting",
        input_path=input_path,
        schema_paths=[draft_schema],
        output_contract_lines=[
            'domain_output must contain exactly the key "application_draft".',
            'The draft must include "project_title" and a non-empty "sections" list.',
            "Each section must include: section_key, section_title, text, linked_object_ids.",
        ],
        hard_constraints=[
            f"outline section keys: {json.dumps([item.get('section_key') for item in active_draft.get('outline', []) if isinstance(item, dict)], ensure_ascii=False)}",
            f"selected question: {selected_question['core_question']}",
            f"necessity claim: {active_argument_chain['necessity_claim']}",
            f"applicant fit anchor: {active_fit_mapping['applicant_fit_summary']}",
            f"linked_object_ids may use only these known ids: {json.dumps(known_ids, ensure_ascii=False)}",
            "Use the current outline as the strong default. Revise it when drafting exposes a real structural defect, unless human approval has frozen it.",
            "Background, preliminary evidence, technical route, expected outcomes, progress, and figure-facing cues should all serve the same mainline.",
        ],
        quality_goals=[
            "Expand the outline into a proposal-facing draft while preserving evidence and explaining any necessary upstream adjustment.",
            "Keep the section texts concrete, evidence-linked, and ready for critique/revision.",
        ],
    )

def _build_prompt(
    *,
    route_id: str,
    input_path: str | Path,
    schema_paths: list[Path],
    output_contract_lines: list[str],
    hard_constraints: list[str],
    quality_goals: list[str],
) -> str:
    input_file = Path(input_path).expanduser().resolve()
    lines = [
        "You are executing one part of a MedAutoGrant authoring stage.",
        "Read the workspace JSON and the referenced schema files from disk before you answer.",
        "Do not modify any files. Return JSON only, with no markdown fences.",
        "Direction, question, argument, and applicant fit are interdependent professional judgments. Reconcile them together and surface a route-back when the current upstream choice no longer holds; route labels do not prescribe your reasoning order or number of iterations.",
        "",
        f"Workspace file: {input_file}",
    ]
    for schema_path in schema_paths:
        lines.append(f"Schema file: {schema_path}")
    lines.extend(
        [
            "",
            "Output contract:",
            (
                '- Return exactly one object shaped as '
                '{"surface_kind":"domain_stage_closeout_packet",'
                f'"route_id":"{route_id}","domain_output_kind":"mag_authoring_output",'
                '"domain_output":{...}}.'
            ),
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

def _run_executor_generation(
    *,
    prompt: str,
    input_path: str | Path,
    route_id: str,
    executor_runner: ExecutorRunner,
) -> tuple[dict[str, Any], dict[str, Any]]:
    return run_domain_executor(
        prompt=prompt,
        input_path=input_path,
        executor_kind="codex_cli",
        route_id=route_id,
        closeout_surface_kind="domain_stage_closeout_packet",
        domain_output_kind="mag_authoring_output",
        executor_runner=executor_runner,
    )

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

def _finalize_execution_workspace(workspace: dict[str, Any]) -> dict[str, Any]:
    _prune_invalid_preliminary_supports(workspace)
    materialized_workspace = materialize_workspace_surfaces(workspace)
    _validate_workspace_or_raise(materialized_workspace)
    return materialized_workspace

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
