from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Mapping

from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_nonempty_string
from med_autogrant.workspace_types import WorkspaceStateError


MAG_CODEX_STAGE_EXECUTION_RECEIPT_BUNDLE_KIND = "mag_codex_stage_execution_receipt_bundle"

_DEFAULT_EXECUTOR = "codex_cli"
_READY_STATE = "codex_stage_receipts_ready_not_quality_ready"
_EXECUTION_MISSING_STATE = "stage_execution_receipt_missing"
_REVIEW_MISSING_STATE = "independent_review_receipt_missing"

_EXECUTION_REQUIRED_FIELDS = (
    "attempt_id",
    "executor",
    "invocation_ref",
    "task_record_ref",
    "receipt_ref",
)
_REVIEW_REQUIRED_FIELDS = (
    "review_attempt_id",
    "reviewer_executor",
    "review_invocation_ref",
    "review_task_record_ref",
    "review_receipt_ref",
    "review_artifact_ref",
    "review_target_attempt_id",
)
_FORBIDDEN_BODY_KEYS = frozenset(
    {
        "app_workbench_state_body",
        "artifact_body",
        "artifact_content",
        "authoring_quality_verdict_body",
        "canonical_grant_artifact_content",
        "export_verdict_body",
        "fundability_verdict_body",
        "grant_artifact_body",
        "grant_artifact_content",
        "grant_truth_body",
        "memory_body",
        "opl_runtime_state_body",
        "package_archive_body",
        "package_body",
        "proposal_body",
        "proposal_text",
        "proposal_text_body",
        "review_artifact_body",
        "runtime_state_body",
    }
)
_FORBIDDEN_READY_CLAIM_KEYS = frozenset(
    {
        "can_declare_export_ready",
        "can_declare_fundability_ready",
        "can_declare_quality_ready",
        "can_declare_submission_ready",
        "claims_export_ready",
        "claims_fundability_ready",
        "claims_grant_ready",
        "claims_independent_review_gate_passed",
        "claims_quality_ready",
        "claims_submission_ready",
        "export_ready",
        "fundability_ready",
        "grant_ready",
        "quality_ready",
        "submission_ready",
        "submission_ready_export",
    }
)
_REF_FIELDS = frozenset(
    {
        "invocation_ref",
        "task_record_ref",
        "receipt_ref",
        "stage_pack_ref",
        "output_artifact_ref",
        "typed_blocker_ref",
        "no_regression_evidence_ref",
        "review_invocation_ref",
        "review_task_record_ref",
        "review_receipt_ref",
        "review_artifact_ref",
    }
)
_REVIEW_GATED_CLAIMS = (
    "fundability_ready",
    "quality_ready",
    "export_ready",
    "submission_ready",
    "memory_accept_reject_ready",
)


def build_codex_stage_execution_receipt_bundle(
    *,
    stage_id: str,
    execution_attempts: Sequence[Mapping[str, Any]],
    review_attempts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    resolved_stage_id = _require_nonempty_string(stage_id, field_name="stage_id")
    executions = _project_execution_attempts(execution_attempts)
    reviews = _project_review_attempts(review_attempts, execution_attempts=executions)

    state = _bundle_state(executions=executions, reviews=reviews)
    return {
        "surface_kind": MAG_CODEX_STAGE_EXECUTION_RECEIPT_BUNDLE_KIND,
        "version": "v1",
        "state": state,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "stage_id": resolved_stage_id,
        "executor_policy": {
            "default_executor": _DEFAULT_EXECUTOR,
            "executor_first": True,
            "contract_light": True,
            "review_must_be_independent_attempt": True,
            "review_must_have_separate_invocation": True,
            "review_must_have_separate_task_record": True,
        },
        "execution_attempts": executions,
        "review_attempts": reviews,
        "summary": {
            "execution_attempt_count": len(executions),
            "independent_review_attempt_count": len(reviews),
            "reviewed_execution_attempt_count": len(_reviewed_attempt_ids(reviews)),
        },
        "quality_gate_effect": _quality_gate_effect(state),
        "authority_boundary": {
            "projection_scope": "codex_stage_execution_and_review_receipt_refs_only",
            "codex_cli_is_default_executor": True,
            "mag_implements_opl_runtime": False,
            "mag_implements_app_workbench": False,
            "execution_receipt_refs_equal_quality_ready": False,
            "review_receipt_refs_equal_quality_ready": False,
            "can_declare_fundability_ready": False,
            "can_declare_quality_ready": False,
            "can_declare_export_ready": False,
            "can_declare_submission_ready": False,
            "can_write_grant_truth_body": False,
            "can_write_memory_body": False,
        },
        "projection_policy": (
            "refs_only_execution_and_independent_review_receipts_no_artifact_body_"
            "no_memory_body_no_proposal_text_no_runtime_state"
        ),
    }


def _project_execution_attempts(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    _require_sequence(attempts, context="execution_attempts")
    projected: list[dict[str, Any]] = []
    seen_attempt_ids: set[str] = set()
    for index, attempt in enumerate(attempts):
        if not isinstance(attempt, Mapping):
            raise WorkspaceStateError(f"execution_attempts[{index}] 必须是 object。")
        context = f"execution_attempts[{index}]"
        _assert_refs_only(attempt, path=context)
        values = {
            field_name: _require_nonempty_string(
                attempt.get(field_name),
                field_name=field_name,
                context=context,
            )
            for field_name in _EXECUTION_REQUIRED_FIELDS
        }
        if values["attempt_id"] in seen_attempt_ids:
            raise WorkspaceStateError(f"execution_attempts attempt_id 重复: {values['attempt_id']}")
        seen_attempt_ids.add(values["attempt_id"])
        if values["executor"] != _DEFAULT_EXECUTOR:
            raise WorkspaceStateError(f"{context}.executor 必须是 {_DEFAULT_EXECUTOR}。")
        projected.append(
            {
                "attempt_id": values["attempt_id"],
                "executor": values["executor"],
                "refs": _project_refs(attempt, context=context),
            }
        )
    return projected


def _project_review_attempts(
    attempts: Sequence[Mapping[str, Any]],
    *,
    execution_attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    _require_sequence(attempts, context="review_attempts")
    execution_index = {
        _require_nonempty_string(item.get("attempt_id"), field_name="attempt_id", context="execution_attempts"):
        item
        for item in execution_attempts
    }
    projected: list[dict[str, Any]] = []
    seen_attempt_ids: set[str] = set()
    for index, attempt in enumerate(attempts):
        if not isinstance(attempt, Mapping):
            raise WorkspaceStateError(f"review_attempts[{index}] 必须是 object。")
        context = f"review_attempts[{index}]"
        _assert_refs_only(attempt, path=context)
        values = {
            field_name: _require_nonempty_string(
                attempt.get(field_name),
                field_name=field_name,
                context=context,
            )
            for field_name in _REVIEW_REQUIRED_FIELDS
        }
        if values["review_attempt_id"] in seen_attempt_ids:
            raise WorkspaceStateError(
                f"review_attempts review_attempt_id 重复: {values['review_attempt_id']}"
            )
        seen_attempt_ids.add(values["review_attempt_id"])
        if values["reviewer_executor"] != _DEFAULT_EXECUTOR:
            raise WorkspaceStateError(f"{context}.reviewer_executor 必须是 {_DEFAULT_EXECUTOR}。")
        target = execution_index.get(values["review_target_attempt_id"])
        if target is None:
            raise WorkspaceStateError(
                f"{context}.review_target_attempt_id 未匹配 execution attempt: "
                f"{values['review_target_attempt_id']}"
            )
        target_refs = _require_mapping(target.get("refs"), context=f"{context}.target.refs")
        if values["review_invocation_ref"] == target_refs["invocation_ref"]:
            raise WorkspaceStateError(f"{context}.review_invocation_ref 必须独立于 execution invocation。")
        if values["review_task_record_ref"] == target_refs["task_record_ref"]:
            raise WorkspaceStateError(f"{context}.review_task_record_ref 必须独立于 execution task record。")
        if attempt.get("shared_context_with_execution") is True:
            raise WorkspaceStateError(f"{context}.shared_context_with_execution 必须为 false。")
        if attempt.get("independent_context") is not True:
            raise WorkspaceStateError(f"{context}.independent_context 必须为 true。")
        projected.append(
            {
                "review_attempt_id": values["review_attempt_id"],
                "reviewer_executor": values["reviewer_executor"],
                "review_target_attempt_id": values["review_target_attempt_id"],
                "independent_context": True,
                "shared_context_with_execution": False,
                "refs": _project_refs(attempt, context=context),
            }
        )
    return projected


def _project_refs(attempt: Mapping[str, Any], *, context: str) -> dict[str, str]:
    refs: dict[str, str] = {}
    for raw_key, value in attempt.items():
        key = _require_nonempty_string(raw_key, field_name="key", context=context)
        normalized_key = _normalize_key(key)
        if normalized_key in _REF_FIELDS or normalized_key.endswith("_ref"):
            refs[key] = _require_nonempty_string(value, field_name=key, context=context)
    required_ref_fields = (
        ("invocation_ref", "task_record_ref", "receipt_ref")
        if context.startswith("execution_attempts")
        else ("review_invocation_ref", "review_task_record_ref", "review_receipt_ref", "review_artifact_ref")
    )
    for field_name in required_ref_fields:
        if field_name not in refs:
            raise WorkspaceStateError(f"{context} 缺少 {field_name}。")
    return refs


def _bundle_state(
    *,
    executions: Sequence[Mapping[str, Any]],
    reviews: Sequence[Mapping[str, Any]],
) -> str:
    if not executions:
        return _EXECUTION_MISSING_STATE
    if not reviews:
        return _REVIEW_MISSING_STATE
    reviewed_attempt_ids = _reviewed_attempt_ids(reviews)
    execution_attempt_ids = {
        _require_nonempty_string(item.get("attempt_id"), field_name="attempt_id", context="execution_attempts")
        for item in executions
    }
    if not execution_attempt_ids.issubset(reviewed_attempt_ids):
        return _REVIEW_MISSING_STATE
    return _READY_STATE


def _quality_gate_effect(state: str) -> dict[str, Any]:
    if state == _READY_STATE:
        return {
            "state": "independent_review_receipt_refs_ready_not_quality_ready",
            "gated_claims": list(_REVIEW_GATED_CLAIMS),
            "typed_blocker_required": False,
            "domain_verdict_required": True,
            "ready_verdict_authorized": False,
        }
    return {
        "state": "fail_closed_typed_blocker_required",
        "blocker_id": "independent_review_receipt_required",
        "gated_claims": list(_REVIEW_GATED_CLAIMS),
        "typed_blocker_required": True,
        "domain_verdict_required": True,
        "ready_verdict_authorized": False,
    }


def _reviewed_attempt_ids(reviews: Sequence[Mapping[str, Any]]) -> set[str]:
    return {
        _require_nonempty_string(
            review.get("review_target_attempt_id"),
            field_name="review_target_attempt_id",
            context="review_attempts",
        )
        for review in reviews
    }


def _require_sequence(value: Any, *, context: str) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise WorkspaceStateError(f"{context} 必须是 list。")


def _require_mapping(value: Any, *, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 object。")
    return value


def _assert_refs_only(value: Any, *, path: str) -> None:
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = _require_nonempty_string(raw_key, field_name="key", context=path)
            normalized_key = _normalize_key(key)
            if _is_forbidden_body_key(normalized_key):
                raise WorkspaceStateError(f"codex stage receipt ABI 禁止包含 body 字段: {path}.{key}")
            if normalized_key in _FORBIDDEN_READY_CLAIM_KEYS and bool(item):
                raise WorkspaceStateError(f"codex stage receipt ABI 禁止包含 ready claim: {path}.{key}")
            _assert_refs_only(item, path=f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_refs_only(item, path=f"{path}[{index}]")


def _is_forbidden_body_key(normalized_key: str) -> bool:
    if normalized_key in _FORBIDDEN_BODY_KEYS:
        return True
    if normalized_key.endswith("_ref") or normalized_key.endswith("_refs"):
        return False
    return (
        normalized_key == "body"
        or normalized_key.endswith("_body")
        or normalized_key.endswith("_content")
        or normalized_key.endswith("_payload")
    )


def _normalize_key(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


__all__ = [
    "MAG_CODEX_STAGE_EXECUTION_RECEIPT_BUNDLE_KIND",
    "build_codex_stage_execution_receipt_bundle",
]
