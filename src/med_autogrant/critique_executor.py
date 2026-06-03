from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable

from med_autogrant.codex_cli import (
    read_codex_cli_contract,
    run_codex_exec,
)
from med_autogrant.critique_policy import (
    build_policy_prompt_lines,
    build_weight_contract,
    resolve_critique_policy_from_document,
)
from med_autogrant.opl_executor_adapter import run_opl_agent_executor
from med_autogrant.runtime_defaults import (
    NON_DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE,
    OPL_AGENT_EXECUTION_RECEIPT_CONTRACT,
    OPL_AGENT_EXECUTION_REQUEST_CONTRACT,
    OPL_EXECUTOR_ADAPTER_CONTRACT_REF,
    OPL_EXECUTOR_ADAPTER_OWNER,
)
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.schema_subset_validator import SchemaSubsetValidator as _SchemaSubsetValidator
from med_autogrant.workspace_projection_parts import _build_workspace_state
from med_autogrant.workspace_reference_validation import _collect_known_ids
from med_autogrant.workspace_types import WorkspaceStateError
from med_autogrant.workspace_validation import validate_workspace_document


CodexRunner = Callable[[str], dict[str, Any]]
OplExecutorRunner = Callable[..., dict[str, Any]]

DEFAULT_CRITIQUE_EXECUTOR_KIND = "codex_cli"
HERMES_AGENT_EXECUTOR_KIND = "hermes_agent"
SUPPORTED_CRITIQUE_EXECUTOR_KINDS = (
    DEFAULT_CRITIQUE_EXECUTOR_KIND,
    HERMES_AGENT_EXECUTOR_KIND,
)

EXECUTABLE_REVISION_ACTION_TYPES = (
    "rebuild_argument",
    "add_evidence",
    "rewrite_section",
    "tighten_fit",
)


def build_critique_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    executor_kind: str | None = None,
    codex_runner: Callable[..., dict[str, Any]] = run_codex_exec,
    opl_executor_runner: Callable[..., dict[str, Any]] = run_opl_agent_executor,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    critique_context = _build_critique_context(document=document, state=state)
    critique_policy = resolve_critique_policy_from_document(document)
    prompt = _build_critique_prompt(context=critique_context, input_path=input_path)
    payload, executor_payload = _run_critique_generation(
        prompt=prompt,
        input_path=input_path,
        executor_kind=executor_kind,
        codex_runner=codex_runner,
        opl_executor_runner=opl_executor_runner,
    )
    critique = _normalize_mentor_critique(
        critique_context=critique_context,
        critique_policy=critique_policy,
        executor_payload=executor_payload,
        payload=_require_object(payload, "mentor_critique"),
    )
    revision_plan = _normalize_revision_plan(
        critique_context=critique_context,
        critique=critique,
        payload=_require_object(payload, "revision_plan"),
    )

    critique_workspace = deepcopy(document)
    critique_workspace["lifecycle_stage"] = "critique"
    critique_workspace.setdefault("mentor_critiques", []).append(critique)
    critique_workspace.setdefault("revision_plans", []).append(revision_plan)
    current_selection = critique_workspace.setdefault("current_selection", {})
    current_selection["active_revision_plan_id"] = revision_plan["revision_plan_id"]

    validation = validate_workspace_document(critique_workspace)
    if not validation.ok:
        first_issue = validation.errors[0]
        raise WorkspaceStateError(
            f"{first_issue.path}: {first_issue.message}",
            errors=validation.errors,
            grant_run_id=critique_workspace.get("grant_run_id"),
            workspace_id=critique_workspace.get("workspace_id"),
            lifecycle_stage=critique_workspace.get("lifecycle_stage"),
        )

    return {
        "grant_run_id": critique_workspace["grant_run_id"],
        "workspace_id": critique_workspace["workspace_id"],
        "draft_id": critique_context["draft_id"],
        "active_revision_plan_id": revision_plan["revision_plan_id"],
        "lifecycle_stage": critique_workspace["lifecycle_stage"],
        "critique_execution": {
            "executor": executor_payload,
            "critique_id": critique["critique_id"],
            "active_revision_plan_id": revision_plan["revision_plan_id"],
            "reviewed_revision_plan_id": critique.get("reviewed_revision_plan_id"),
            "verdict": critique["verdict"],
        },
        "critique_workspace": critique_workspace,
    }


def _run_critique_generation(
    *,
    prompt: str,
    input_path: str | Path,
    executor_kind: str | None,
    codex_runner: Callable[..., dict[str, Any]],
    opl_executor_runner: Callable[..., dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    resolved_executor_kind = _resolve_critique_executor_kind(executor_kind)
    resolved_cwd = Path(input_path).expanduser().resolve().parent

    if resolved_executor_kind == DEFAULT_CRITIQUE_EXECUTOR_KIND:
        codex_contract = read_codex_cli_contract()
        payload = codex_runner(
            prompt,
            cwd=resolved_cwd,
        )
        if not isinstance(payload, dict):
            raise WorkspaceStateError("Codex critique pass 返回值必须是 object。")
        return payload, _build_codex_executor_payload(codex_contract)

    receipt = opl_executor_runner(
        {
            "executor_kind": resolved_executor_kind,
            "mode": "agent_loop",
            "prompt": prompt,
            "cwd": str(resolved_cwd),
            "json": True,
            "domain_payload": {
                "domain_id": "med-autogrant",
                "route_id": "critique",
                "input_path": str(Path(input_path).expanduser().resolve()),
            },
        },
        cwd=resolved_cwd,
    )
    if not isinstance(receipt, dict):
        raise WorkspaceStateError("OPL executor adapter 返回的 receipt 必须是 object。")
    hermes_proof = _require_object(receipt, "proof")
    hermes_contract = _require_object(receipt, "executor_contract")
    hermes_payload = _require_domain_closeout_payload(receipt)
    receipt = _require_agent_execution_receipt(receipt, hermes_proof)
    return hermes_payload, _build_hermes_executor_payload(hermes_contract, hermes_proof, receipt)


def _resolve_critique_executor_kind(executor_kind: str | None) -> str:
    if executor_kind is None:
        return DEFAULT_CRITIQUE_EXECUTOR_KIND
    normalized = str(executor_kind).strip()
    if normalized in SUPPORTED_CRITIQUE_EXECUTOR_KINDS:
        return normalized
    raise WorkspaceStateError(
        "execute-critique-pass 不支持该 executor_kind："
        f"{normalized}。当前只允许 {', '.join(SUPPORTED_CRITIQUE_EXECUTOR_KINDS)}。"
    )


def _build_codex_executor_payload(codex_contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "codex_cli",
        "model": codex_contract["model_selection"],
        "reasoning_effort": codex_contract["reasoning_selection"],
    }


def _build_hermes_executor_payload(
    hermes_contract: dict[str, Any],
    hermes_proof: dict[str, Any],
    receipt: dict[str, Any],
) -> dict[str, Any]:
    return {
        "kind": "hermes_agent",
        "mode": "agent_loop",
        "adapter_owner": OPL_EXECUTOR_ADAPTER_OWNER,
        "adapter_contract_ref": OPL_EXECUTOR_ADAPTER_CONTRACT_REF,
        "request_contract": OPL_AGENT_EXECUTION_REQUEST_CONTRACT,
        "receipt_contract": OPL_AGENT_EXECUTION_RECEIPT_CONTRACT,
        "fallback_allowed": False,
        "non_equivalence_notice": NON_DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE,
        "entrypoint": _require_string(hermes_contract, "entrypoint", context="Hermes contract"),
        "model": _require_string(hermes_contract, "model", context="Hermes contract"),
        "provider": hermes_contract.get("provider"),
        "api_mode": hermes_contract.get("api_mode"),
        "reasoning_effort": hermes_contract.get("reasoning_effort"),
        "full_agent_loop_proved": _require_bool(hermes_proof, "full_agent_loop_proved", context="Hermes proof"),
        "session_id": hermes_proof.get("session_id"),
        "api_calls": _require_nonnegative_int(hermes_proof, "api_calls", context="Hermes proof"),
        "tool_call_count": _require_nonnegative_int(hermes_proof, "tool_call_count", context="Hermes proof"),
        "event_count": _require_nonnegative_int(hermes_proof, "event_count", context="Hermes proof"),
        "reasoning_semantics_status": _require_string(
            hermes_proof,
            "provider_reasoning_status",
            context="Hermes proof",
        ),
        "event_stream": _require_object_list(
            hermes_proof,
            "event_stream",
            context="Hermes proof",
        ),
        "agent_execution_receipt": dict(receipt),
    }


def _require_agent_execution_receipt(
    receipt: dict[str, Any],
    hermes_proof: dict[str, Any],
) -> dict[str, Any]:
    context = "OPL non-default AgentExecutionReceipt"
    surface_kind = _require_string(receipt, "surface_kind", context=context)
    if surface_kind != "opl_agent_execution_receipt":
        raise WorkspaceStateError(f"{context} surface_kind 必须是 opl_agent_execution_receipt。")
    executor_kind = _require_string(receipt, "executor_kind", context=context)
    if executor_kind != HERMES_AGENT_EXECUTOR_KIND:
        raise WorkspaceStateError(f"{context} executor_kind 必须是 hermes_agent。")
    mode = _require_string(receipt, "mode", context=context)
    if mode != "agent_loop":
        raise WorkspaceStateError(f"{context} mode 必须是 agent_loop。")
    notice = _require_string(receipt, "non_equivalence_notice", context=context)
    if notice != NON_DEFAULT_EXECUTOR_EQUIVALENCE_NOTICE:
        raise WorkspaceStateError(f"{context} non_equivalence_notice 不符合 OPL non-default executor 合同。")
    if not _require_object_list(receipt, "event_summary", context=context):
        raise WorkspaceStateError(f"{context} event_summary 必须包含 agent loop 事件。")
    if _require_nonnegative_int(receipt, "exit_code", context=context) != 0:
        raise WorkspaceStateError(f"{context} exit_code 必须为 0。")
    receipt_proof = _require_object(receipt, "proof")
    if receipt_proof.get("full_agent_loop_proved") is not True:
        raise WorkspaceStateError(f"{context} proof 必须证明 full_agent_loop_proved。")
    if _require_nonnegative_int(receipt_proof, "tool_call_count", context=context) <= 0:
        raise WorkspaceStateError(f"{context} proof 必须包含至少一个 tool call。")
    if receipt_proof.get("session_id") != hermes_proof.get("session_id"):
        raise WorkspaceStateError(f"{context} proof.session_id 必须与 Hermes proof 对齐。")
    if receipt_proof.get("tool_call_count") != hermes_proof.get("tool_call_count"):
        raise WorkspaceStateError(f"{context} proof.tool_call_count 必须与 Hermes proof 对齐。")
    return receipt


def _require_domain_closeout_payload(receipt: dict[str, Any]) -> dict[str, Any]:
    closeout = _require_object(receipt, "closeout_packet")
    context = "OPL non-default domain closeout packet"
    surface_kind = _require_string(closeout, "surface_kind", context=context)
    if surface_kind != "mag_critique_closeout_packet":
        raise WorkspaceStateError(f"{context} surface_kind 必须是 mag_critique_closeout_packet。")
    return {
        "mentor_critique": _require_object(closeout, "mentor_critique"),
        "revision_plan": _require_object(closeout, "revision_plan"),
    }


def _build_critique_context(
    *,
    document: dict[str, Any],
    state: Any,
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
    known_ids = sorted(_collect_known_ids(document))
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
        "next_critique_id": _next_versioned_id("critique", existing_critique_ids),
        "next_revision_plan_id": _next_versioned_id("revision", existing_revision_plan_ids),
    }


def _build_critique_prompt(*, context: dict[str, Any], input_path: str | Path) -> str:
    input_file = Path(input_path).expanduser().resolve()
    mentor_schema = (SchemaStore().root / "mentor-critique.schema.json").resolve()
    revision_schema = (SchemaStore().root / "revision-plan.schema.json").resolve()
    critique_policy = resolve_critique_policy_from_document(_require_object(context, "document"))
    policy_lines = build_policy_prompt_lines(critique_policy)
    weight_contract = build_weight_contract(critique_policy)
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
            'Return exactly one JSON object with keys "mentor_critique" and "revision_plan".',
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
            "- use only executable revision actions: rebuild_argument, add_evidence, rewrite_section, tighten_fit",
            "- every revision item must target an existing section via target_ref=section:<section_key>",
            "- every revision item must include mutation_payload.operation=replace_draft_section",
            "- every mutation_payload.linked_object_ids must cover required_input_ids and use only known ids",
            f"- mentor critique weights must be {weight_split}",
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
            "- produce a mentor-style critique that sharpens necessity/scientific value, applicant fit, and feasibility",
            "- produce a revision plan that is directly executable by the deterministic section-level revision pass",
        ]
    )


def _normalize_mentor_critique(
    *,
    critique_context: dict[str, Any],
    critique_policy: dict[str, Any],
    executor_payload: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    critique = deepcopy(payload)
    metadata = dict(critique.get("metadata") or {})
    executor_kind = str(executor_payload.get("kind") or "").strip()
    critique["critique_id"] = critique_context["next_critique_id"]
    if executor_kind == "hermes_agent":
        metadata["owner"] = "OPL executor adapter critique receipt owner"
    else:
        metadata["owner"] = "Codex CLI critique executor"
    metadata["independent_review_evidence"] = _build_independent_review_evidence(
        critique_context=critique_context,
        critique_id=critique["critique_id"],
        executor_payload=executor_payload,
        owner=metadata["owner"],
    )
    critique["metadata"] = metadata
    critique["draft_id"] = critique_context["draft_id"]
    critique["current_scientific_question"] = critique_context["selected_question"]["core_question"]
    if critique_context["lifecycle_stage"] == "revision":
        critique["reviewed_revision_plan_id"] = critique_context["active_revision_plan"]["revision_plan_id"]
    else:
        critique.pop("reviewed_revision_plan_id", None)
    for field_name, expected_weight in build_weight_contract(critique_policy).items():
        criterion = _require_object(critique, field_name)
        criterion["weight"] = expected_weight
    _validate_schema_payload(
        critique,
        schema_file="mentor-critique.schema.json",
        grant_run_id=critique_context["grant_run_id"],
        workspace_id=critique_context["workspace_id"],
        lifecycle_stage=critique_context["lifecycle_stage"],
    )
    return critique


def _build_independent_review_evidence(
    *,
    critique_context: dict[str, Any],
    critique_id: str,
    executor_payload: dict[str, Any],
    owner: str,
) -> dict[str, Any]:
    executor_kind = str(executor_payload.get("kind") or "").strip()
    session_id = executor_payload.get("session_id")
    execution_attempt_ref = (
        f"draft_artifact::{critique_context['grant_run_id']}::{critique_context['draft_id']}"
    )
    if executor_kind == "hermes_agent" and isinstance(session_id, str) and session_id.strip():
        review_receipt_ref = f"opl_agent_execution_receipt::{session_id.strip()}"
        reviewer_agent_ref = f"hermes_agent::{session_id.strip()}"
    else:
        review_receipt_ref = f"mentor_critiques::{critique_id}::metadata.independent_review_evidence"
        reviewer_agent_ref = "codex_cli::critique_executor"
    return {
        "execution_attempt_ref": execution_attempt_ref,
        "review_attempt_ref": f"mentor_critiques::{critique_id}",
        "review_receipt_ref": review_receipt_ref,
        "no_shared_context_verified": True,
        "reviewer_owner": owner,
        "reviewer_agent_ref": reviewer_agent_ref,
    }


def _normalize_revision_plan(
    *,
    critique_context: dict[str, Any],
    critique: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    revision_plan = deepcopy(payload)
    revision_plan["revision_plan_id"] = critique_context["next_revision_plan_id"]
    revision_plan["draft_id"] = critique_context["draft_id"]
    revision_plan["critique_id"] = critique["critique_id"]
    revision_plan["execution_status"] = "planned"
    revision_plan["pre_revision_version_label"] = critique_context["draft_version_label"]
    revision_plan.pop("comparison_summary", None)
    post_revision_version_label = revision_plan.get("post_revision_version_label")
    if (
        not isinstance(post_revision_version_label, str)
        or not post_revision_version_label.strip()
        or post_revision_version_label == critique_context["draft_version_label"]
    ):
        raise WorkspaceStateError(
            "critique pass 生成的 post_revision_version_label 必须为新的非空版本号。",
            errors=[],
            grant_run_id=critique_context["grant_run_id"],
            workspace_id=critique_context["workspace_id"],
            lifecycle_stage=critique_context["lifecycle_stage"],
        )
    items = revision_plan.get("items")
    if not isinstance(items, list) or not items:
        raise WorkspaceStateError(
            "critique pass 生成的 RevisionPlan.items 必须为非空列表。",
            errors=[],
            grant_run_id=critique_context["grant_run_id"],
            workspace_id=critique_context["workspace_id"],
            lifecycle_stage=critique_context["lifecycle_stage"],
        )
    for item in items:
        _validate_revision_item(
            item,
            section_keys=set(critique_context["section_keys"]),
            known_ids=set(critique_context["known_ids"]),
            grant_run_id=critique_context["grant_run_id"],
            workspace_id=critique_context["workspace_id"],
            lifecycle_stage=critique_context["lifecycle_stage"],
        )
    _validate_schema_payload(
        revision_plan,
        schema_file="revision-plan.schema.json",
        grant_run_id=critique_context["grant_run_id"],
        workspace_id=critique_context["workspace_id"],
        lifecycle_stage=critique_context["lifecycle_stage"],
    )
    return revision_plan


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


def _validate_revision_item(
    item: Any,
    *,
    section_keys: set[str],
    known_ids: set[str],
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    if not isinstance(item, dict):
        raise WorkspaceStateError(
            "critique pass 生成的 RevisionPlan.items[] 必须都是 object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    action_type = item.get("action_type")
    if action_type not in EXECUTABLE_REVISION_ACTION_TYPES:
        raise WorkspaceStateError(
            f"critique pass 只允许输出可执行 revision action_type，收到 {action_type!r}。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    target_ref = item.get("target_ref")
    if not isinstance(target_ref, str) or not target_ref.startswith("section:"):
        raise WorkspaceStateError(
            "critique pass 的 revision item.target_ref 必须形如 section:<section_key>。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    section_key = target_ref.split(":", 1)[1]
    if section_key not in section_keys:
        raise WorkspaceStateError(
            f"critique pass 不能把 revision item 指向不存在的 section: {section_key}",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    mutation_payload = item.get("mutation_payload")
    if not isinstance(mutation_payload, dict):
        raise WorkspaceStateError(
            "critique pass 的 revision item 必须包含 mutation_payload。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if mutation_payload.get("operation") != "replace_draft_section":
        raise WorkspaceStateError(
            "critique pass 的 mutation_payload.operation 必须为 replace_draft_section。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if mutation_payload.get("target_section_key") != section_key:
        raise WorkspaceStateError(
            "critique pass 的 mutation_payload.target_section_key 必须与 target_ref 一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    linked_object_ids = mutation_payload.get("linked_object_ids")
    required_input_ids = item.get("required_input_ids")
    if not isinstance(linked_object_ids, list) or not isinstance(required_input_ids, list):
        raise WorkspaceStateError(
            "critique pass 的 linked_object_ids / required_input_ids 必须为列表。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    unknown_ids = [
        ref_id
        for ref_id in linked_object_ids
        if not isinstance(ref_id, str) or not ref_id or ref_id not in known_ids
    ]
    if unknown_ids:
        raise WorkspaceStateError(
            f"critique pass 的 linked_object_ids 引用了未知对象: {unknown_ids}",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    missing_required_inputs = [
        ref_id for ref_id in required_input_ids if ref_id not in linked_object_ids
    ]
    if missing_required_inputs:
        raise WorkspaceStateError(
            "critique pass 的 linked_object_ids 必须覆盖 required_input_ids。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def _require_object(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise WorkspaceStateError(f"critique executor 输出缺少 object 字段: {key}")
    return value


def _require_object_list(payload: dict[str, Any], key: str, *, context: str) -> list[dict[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise WorkspaceStateError(f"{context} 缺少合法的 `{key}` object list。")
    return value


def _require_string(payload: dict[str, Any], key: str, *, context: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少合法的 `{key}`。")
    return value


def _require_bool(payload: dict[str, Any], key: str, *, context: str) -> bool:
    value = payload.get(key)
    if not isinstance(value, bool):
        raise WorkspaceStateError(f"{context} 缺少合法的 `{key}`。")
    return value


def _require_nonnegative_int(payload: dict[str, Any], key: str, *, context: str) -> int:
    value = payload.get(key)
    if not isinstance(value, int) or value < 0:
        raise WorkspaceStateError(f"{context} 缺少合法的 `{key}`。")
    return value


def _next_versioned_id(prefix: str, existing_ids: list[str]) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}-v(\d+)$")
    max_index = 0
    for value in existing_ids:
        match = pattern.match(value)
        if match:
            max_index = max(max_index, int(match.group(1)))
    return f"{prefix}-v{max_index + 1}"
