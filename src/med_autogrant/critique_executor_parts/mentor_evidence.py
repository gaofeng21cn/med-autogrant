from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable


def normalize_mentor_critique(
    *,
    critique_context: dict[str, Any],
    critique_policy: dict[str, Any],
    executor_payload: dict[str, Any],
    payload: dict[str, Any],
    build_weights: Callable[[dict[str, Any]], dict[str, int]],
    require_object: Callable[[dict[str, Any], str], dict[str, Any]],
    validate_schema_payload: Callable[..., None],
    build_independent_review_evidence: Callable[..., dict[str, Any]],
) -> dict[str, Any]:
    critique = deepcopy(payload)
    metadata = dict(critique.get("metadata") or {})
    executor_kind = str(executor_payload.get("kind") or "").strip()
    critique["critique_id"] = critique_context["next_critique_id"]
    if executor_kind == "hermes_agent":
        metadata["owner"] = "OPL executor client critique receipt owner"
    else:
        metadata["owner"] = "Codex CLI critique executor"
    metadata["independent_review_evidence"] = build_independent_review_evidence(
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
    for field_name, expected_weight in build_weights(critique_policy).items():
        criterion = require_object(critique, field_name)
        criterion["weight"] = expected_weight
    validate_schema_payload(
        critique,
        schema_file="mentor-critique.schema.json",
        grant_run_id=critique_context["grant_run_id"],
        workspace_id=critique_context["workspace_id"],
        lifecycle_stage=critique_context["lifecycle_stage"],
    )
    return critique


def build_independent_review_evidence(
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
    if isinstance(session_id, str) and session_id.strip():
        review_receipt_ref = f"opl_agent_execution_receipt::{session_id.strip()}"
        reviewer_agent_ref = f"{executor_kind}::{session_id.strip()}"
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
