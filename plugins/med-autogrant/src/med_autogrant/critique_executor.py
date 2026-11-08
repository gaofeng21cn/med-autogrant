from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from med_autogrant.critique_policy import (
    build_policy_prompt_lines,
    build_weight_contract,
    resolve_critique_policy_from_document,
)
from med_autogrant.domain_executor_client import ExecutorRunner, run_domain_executor
from med_autogrant.domain_runtime_parts.contracts import validate_contract_schema
from med_autogrant.schema_loader import SchemaStore
from opl_framework.executor_client import run_agent_execution_request
from med_autogrant.workspace_projection_parts import _build_workspace_state
from med_autogrant.workspace_reference_validation import _collect_known_ids
from med_autogrant.workspace_types import WorkspaceStateError
from med_autogrant.workspace_validation import validate_workspace_document
from med_autogrant.critique_executor_parts.context_prompt import (
    build_critique_context as _build_critique_context_impl,
    build_critique_prompt as _build_critique_prompt_impl,
)
from med_autogrant.critique_executor_parts.mentor_evidence import (
    build_independent_review_evidence as _build_independent_review_evidence_impl,
    normalize_mentor_critique as _normalize_mentor_critique_impl,
)
from med_autogrant.critique_executor_parts.revision_plan import (
    EXECUTABLE_REVISION_OPERATIONS,
    normalize_revision_plan as _normalize_revision_plan_impl,
    validate_revision_item as _validate_revision_item_impl,
)


DEFAULT_CRITIQUE_EXECUTOR_KIND = "codex_cli"
HERMES_AGENT_EXECUTOR_KIND = "hermes_agent"
SUPPORTED_CRITIQUE_EXECUTOR_KINDS = (
    DEFAULT_CRITIQUE_EXECUTOR_KIND,
    HERMES_AGENT_EXECUTOR_KIND,
)

def build_critique_execution_document(
    *,
    document: dict[str, Any],
    input_path: str | Path,
    executor_kind: str | None = None,
    executor_runner: ExecutorRunner = run_agent_execution_request,
) -> dict[str, Any]:
    state = _build_workspace_state(document)
    critique_context = _build_critique_context(document=document, state=state)
    critique_policy = resolve_critique_policy_from_document(document)
    prompt = _build_critique_prompt(context=critique_context, input_path=input_path)
    payload, executor_payload = _run_critique_generation(
        prompt=prompt,
        input_path=input_path,
        executor_kind=executor_kind,
        executor_runner=executor_runner,
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
    executor_runner: ExecutorRunner,
) -> tuple[dict[str, Any], dict[str, Any]]:
    resolved_executor_kind = _resolve_critique_executor_kind(executor_kind)
    return run_domain_executor(
        prompt=prompt,
        input_path=input_path,
        executor_kind=resolved_executor_kind,
        route_id="critique",
        closeout_surface_kind="domain_stage_closeout_packet",
        domain_output_kind="mag_critique_output",
        executor_runner=executor_runner,
    )


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


def _build_critique_context(
    *,
    document: dict[str, Any],
    state: Any,
) -> dict[str, Any]:
    return _build_critique_context_impl(
        document=document,
        state=state,
        collect_known_ids=_collect_known_ids,
        next_versioned_id=_next_versioned_id,
    )


def _build_critique_prompt(*, context: dict[str, Any], input_path: str | Path) -> str:
    return _build_critique_prompt_impl(
        context=context,
        input_path=input_path,
        require_object=_require_object,
        resolve_policy=resolve_critique_policy_from_document,
        build_policy_lines=build_policy_prompt_lines,
        build_weights=build_weight_contract,
        schema_store_factory=SchemaStore,
    )


def _normalize_mentor_critique(
    *,
    critique_context: dict[str, Any],
    critique_policy: dict[str, Any],
    executor_payload: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    return _normalize_mentor_critique_impl(
        critique_context=critique_context,
        critique_policy=critique_policy,
        executor_payload=executor_payload,
        payload=payload,
        build_weights=build_weight_contract,
        require_object=_require_object,
        validate_schema_payload=_validate_schema_payload,
        build_independent_review_evidence=_build_independent_review_evidence,
    )


def _build_independent_review_evidence(
    *,
    critique_context: dict[str, Any],
    critique_id: str,
    executor_payload: dict[str, Any],
    owner: str,
) -> dict[str, Any]:
    return _build_independent_review_evidence_impl(
        critique_context=critique_context,
        critique_id=critique_id,
        executor_payload=executor_payload,
        owner=owner,
    )


def _normalize_revision_plan(
    *,
    critique_context: dict[str, Any],
    critique: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    return _normalize_revision_plan_impl(
        critique_context=critique_context,
        critique=critique,
        payload=payload,
        validate_revision_item=_validate_revision_item,
        validate_schema_payload=_validate_schema_payload,
    )


def _validate_schema_payload(
    payload: dict[str, Any],
    *,
    schema_file: str,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str,
) -> None:
    validate_contract_schema(
        payload,
        schema_file=schema_file,
        context=schema_file,
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
    return _validate_revision_item_impl(
        item,
        section_keys=section_keys,
        known_ids=known_ids,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
        executable_revision_operations=EXECUTABLE_REVISION_OPERATIONS,
    )


def _require_object(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise WorkspaceStateError(f"critique executor 输出缺少 object 字段: {key}")
    return value


def _next_versioned_id(prefix: str, existing_ids: list[str]) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}-v(\d+)$")
    max_index = 0
    for value in existing_ids:
        match = pattern.match(value)
        if match:
            max_index = max(max_index, int(match.group(1)))
    return f"{prefix}-v{max_index + 1}"
