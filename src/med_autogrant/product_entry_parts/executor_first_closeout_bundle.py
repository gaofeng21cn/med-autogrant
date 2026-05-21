from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.product_entry_parts.codex_stage_receipts import (
    MAG_CODEX_STAGE_EXECUTION_RECEIPT_BUNDLE_KIND,
)
from med_autogrant.product_entry_parts.external_evidence_ledger import (
    EXTERNAL_EVIDENCE_CONSUMPTION_LEDGER_KIND,
)
from med_autogrant.product_entry_parts.operator_closeout import (
    MAG_OPERATOR_CLOSEOUT_PROJECTION_KIND,
)
from med_autogrant.product_entry_parts.physical_morphology_guard import (
    PHYSICAL_MORPHOLOGY_GUARD_PROJECTION_KIND,
)
from med_autogrant.product_entry_parts.primitives import TARGET_DOMAIN_ID, _require_nonempty_string
from med_autogrant.product_entry_parts.receipt_readiness import (
    MAG_RECEIPT_READINESS_PROJECTION_KIND,
)
from med_autogrant.workspace_types import WorkspaceStateError


MAG_EXECUTOR_FIRST_CLOSEOUT_BUNDLE_KIND = "mag_executor_first_closeout_bundle"

_CODEX_REFS_READY_STATE = "codex_stage_receipts_ready_not_quality_ready"
_OPERATOR_REFS_READY_STATE = "operator_closeout_refs_ready_not_quality_ready"
_PHYSICAL_READY_STATE = "allowed_external_evidence_present"
_EXTERNAL_EVIDENCE_READY_STATE = "consumed_complete"
_RECEIPT_REFS_READY_STATE = "receipt_refs_ready_not_quality_ready"

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
        "package_content",
        "package_payload",
        "private_evidence_body",
        "proposal_body",
        "proposal_text",
        "proposal_text_body",
        "review_artifact_body",
        "runtime_state_body",
        "runtime_state_payload",
        "workspace_private_evidence_body",
    }
)
_FORBIDDEN_READY_CLAIM_KEYS = frozenset(
    {
        "bundle_ready_equals_grant_ready",
        "can_authorize_export_ready",
        "can_authorize_fundability_ready",
        "can_authorize_quality_ready",
        "can_authorize_submission_ready",
        "can_declare_export_ready",
        "can_declare_fundability_ready",
        "can_declare_quality_ready",
        "can_declare_submission_ready",
        "claims_export_ready",
        "claims_fundability_ready",
        "claims_grant_or_fundability_ready",
        "claims_grant_ready",
        "claims_quality_ready",
        "claims_submission_ready",
        "claims_submission_ready_export",
        "export_ready",
        "fundability_ready",
        "grant_ready",
        "mag_authorizes_export_ready",
        "mag_authorizes_fundability_ready",
        "mag_authorizes_quality_ready",
        "mag_authorizes_submission_ready",
        "mag_can_authorize_export_ready",
        "mag_can_authorize_fundability_ready",
        "mag_can_authorize_quality_ready",
        "mag_can_authorize_submission_ready",
        "provider_completion_is_export_ready",
        "provider_completion_is_fundability_ready",
        "provider_completion_is_quality_ready",
        "provider_completion_is_submission_ready",
        "quality_ready",
        "submission_ready",
        "submission_ready_export",
    }
)
_NEGATED_BODY_CAPABILITY_KEYS = frozenset(
    {
        "can_write_grant_truth_body",
        "can_write_memory_body",
        "can_write_package_body",
        "mag_writes_grant_body",
        "mag_writes_memory_body",
        "mag_writes_package_body",
    }
)


def build_executor_first_closeout_bundle(
    *,
    codex_stage_execution_receipt_bundle: Mapping[str, Any],
    operator_closeout_readiness_projection: Mapping[str, Any],
    physical_morphology_guard_projection: Mapping[str, Any],
    external_evidence_consumption_ledger: Mapping[str, Any] | None = None,
    receipt_readiness_projection: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    codex_bundle = _require_input_surface(
        codex_stage_execution_receipt_bundle,
        expected_kind=MAG_CODEX_STAGE_EXECUTION_RECEIPT_BUNDLE_KIND,
        context="codex_stage_execution_receipt_bundle",
    )
    operator_projection = _require_input_surface(
        operator_closeout_readiness_projection,
        expected_kind=MAG_OPERATOR_CLOSEOUT_PROJECTION_KIND,
        context="operator_closeout_readiness_projection",
    )
    physical_projection = _require_input_surface(
        physical_morphology_guard_projection,
        expected_kind=PHYSICAL_MORPHOLOGY_GUARD_PROJECTION_KIND,
        context="physical_morphology_guard_projection",
    )
    evidence_ledger = (
        _require_input_surface(
            external_evidence_consumption_ledger,
            expected_kind=EXTERNAL_EVIDENCE_CONSUMPTION_LEDGER_KIND,
            context="external_evidence_consumption_ledger",
        )
        if external_evidence_consumption_ledger is not None
        else None
    )
    receipt_projection = (
        _require_input_surface(
            receipt_readiness_projection,
            expected_kind=MAG_RECEIPT_READINESS_PROJECTION_KIND,
            context="receipt_readiness_projection",
        )
        if receipt_readiness_projection is not None
        else None
    )

    blockers = _blockers(
        codex_bundle=codex_bundle,
        operator_projection=operator_projection,
        physical_projection=physical_projection,
        evidence_ledger=evidence_ledger,
        receipt_projection=receipt_projection,
    )
    state = _bundle_state(blockers)
    refs_ready = state == "refs_ready_not_quality_ready"

    return {
        "surface_kind": MAG_EXECUTOR_FIRST_CLOSEOUT_BUNDLE_KIND,
        "version": "v1",
        "state": state,
        "owner": TARGET_DOMAIN_ID,
        "target_domain_id": TARGET_DOMAIN_ID,
        "executor_policy": {
            "default_executor": "codex_cli",
            "executor_first": True,
            "contract_light": True,
            "requires_independent_codex_review_receipt": True,
        },
        "input_surfaces": _input_surface_summaries(
            codex_bundle=codex_bundle,
            operator_projection=operator_projection,
            physical_projection=physical_projection,
            evidence_ledger=evidence_ledger,
            receipt_projection=receipt_projection,
        ),
        "refs_closeout": {
            "refs_ready": refs_ready,
            "quality_ready": False,
            "fundability_ready": False,
            "export_ready": False,
            "submission_ready": False,
            "bundle_ready_equals_grant_ready": False,
        },
        "target_smoke_patch_loop_closeout": _target_smoke_patch_loop_closeout(
            operator_projection=operator_projection,
        ),
        "blockers": blockers,
        "operator_next_attention": _operator_next_attention(state, blockers),
        "can_declare_fundability_ready": False,
        "can_declare_quality_ready": False,
        "can_declare_export_ready": False,
        "can_declare_submission_ready": False,
        "bundle_ready_equals_grant_ready": False,
        "authority_boundary": {
            "projection_scope": "executor_first_closeout_refs_bundle_only",
            "refs_only_projection": True,
            "mag_implements_opl_runtime": False,
            "mag_implements_app_workbench": False,
            "mag_writes_grant_body": False,
            "mag_writes_memory_body": False,
            "mag_writes_package_body": False,
            "bundle_ready_equals_grant_ready": False,
            "can_declare_fundability_ready": False,
            "can_declare_quality_ready": False,
            "can_declare_export_ready": False,
            "can_declare_submission_ready": False,
        },
        "projection_policy": (
            "compose_existing_refs_only_surfaces_no_proposal_body_no_grant_body_"
            "no_memory_body_no_package_body_no_runtime_state_no_app_workbench_body_"
            "no_ready_verdict_claims"
        ),
    }


def _require_input_surface(value: Any, *, expected_kind: str, context: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise WorkspaceStateError(f"{context} 必须是 JSON object。")
    if value.get("surface_kind") != expected_kind:
        raise WorkspaceStateError(f"{context}.surface_kind 必须是 {expected_kind}。")
    _assert_refs_body_free(value, path=context)
    return value


def _blockers(
    *,
    codex_bundle: Mapping[str, Any],
    operator_projection: Mapping[str, Any],
    physical_projection: Mapping[str, Any],
    evidence_ledger: Mapping[str, Any] | None,
    receipt_projection: Mapping[str, Any] | None,
) -> list[dict[str, Any]]:
    blockers: list[dict[str, Any]] = []
    codex_state = _surface_state(codex_bundle, context="codex_stage_execution_receipt_bundle")
    if codex_state != _CODEX_REFS_READY_STATE:
        blockers.append(
            {
                "blocker_id": "missing_codex_review_receipt",
                "state": codex_state,
                "owner": TARGET_DOMAIN_ID,
                "source_surface_kind": MAG_CODEX_STAGE_EXECUTION_RECEIPT_BUNDLE_KIND,
                "required_next_evidence_ref": (
                    "runtime://mag/receipts/review/independent-codex-review-receipt"
                ),
            }
        )

    operator_state = _surface_state(
        operator_projection,
        context="operator_closeout_readiness_projection",
    )
    evidence_gap_ids = _operator_real_evidence_gap_ids(operator_projection)
    if evidence_ledger is not None:
        evidence_gap_ids.extend(_external_evidence_missing_ids(evidence_ledger))
    if operator_state == "real_external_evidence_missing" or evidence_gap_ids:
        blockers.append(
            {
                "blocker_id": "operator_real_evidence_gap",
                "state": operator_state,
                "owner": "one-person-lab",
                "source_surface_kind": MAG_OPERATOR_CLOSEOUT_PROJECTION_KIND,
                "gap_ids": _dedupe(evidence_gap_ids),
            }
        )

    physical_state = _surface_state(
        physical_projection,
        context="physical_morphology_guard_projection",
    )
    if physical_state == "blocked_fail_closed":
        blockers.append(
            {
                "blocker_id": "physical_morphology_blocked",
                "state": physical_state,
                "owner": TARGET_DOMAIN_ID,
                "source_surface_kind": PHYSICAL_MORPHOLOGY_GUARD_PROJECTION_KIND,
                "blocked_count": _nonnegative_int_from_path(
                    physical_projection,
                    ("summary", "blocked_count"),
                    context="physical_morphology_guard_projection.summary.blocked_count",
                ),
                "required_next_evidence_refs": _string_list_from_path(
                    physical_projection,
                    ("required_next_evidence_refs",),
                    context="physical_morphology_guard_projection.required_next_evidence_refs",
                ),
            }
        )
    elif physical_state != _PHYSICAL_READY_STATE:
        blockers.append(
            {
                "blocker_id": "physical_morphology_evidence_gated",
                "state": physical_state,
                "owner": TARGET_DOMAIN_ID,
                "source_surface_kind": PHYSICAL_MORPHOLOGY_GUARD_PROJECTION_KIND,
                "required_next_evidence_refs": _string_list_from_path(
                    physical_projection,
                    ("required_next_evidence_refs",),
                    context="physical_morphology_guard_projection.required_next_evidence_refs",
                ),
            }
        )

    if operator_state != _OPERATOR_REFS_READY_STATE and not any(
        blocker["blocker_id"] == "operator_real_evidence_gap" for blocker in blockers
    ):
        blockers.append(
            {
                "blocker_id": "operator_closeout_refs_incomplete",
                "state": operator_state,
                "owner": TARGET_DOMAIN_ID,
                "source_surface_kind": MAG_OPERATOR_CLOSEOUT_PROJECTION_KIND,
            }
        )

    if receipt_projection is not None:
        receipt_state = _surface_state(
            receipt_projection,
            context="receipt_readiness_projection",
        )
        if receipt_state != _RECEIPT_REFS_READY_STATE:
            blockers.append(
                {
                    "blocker_id": "receipt_refs_incomplete",
                    "state": receipt_state,
                    "owner": TARGET_DOMAIN_ID,
                    "source_surface_kind": MAG_RECEIPT_READINESS_PROJECTION_KIND,
                    "missing_categories": _string_list_from_path(
                        receipt_projection,
                        ("missing_categories",),
                        context="receipt_readiness_projection.missing_categories",
                    ),
                }
            )

    return blockers


def _bundle_state(blockers: list[Mapping[str, Any]]) -> str:
    if not blockers:
        return "refs_ready_not_quality_ready"
    blocker_ids = [
        _require_nonempty_string(
            blocker.get("blocker_id"),
            field_name="blocker_id",
            context="blockers",
        )
        for blocker in blockers
    ]
    for state in (
        "missing_codex_review_receipt",
        "operator_real_evidence_gap",
        "physical_morphology_blocked",
        "physical_morphology_evidence_gated",
        "operator_closeout_refs_incomplete",
        "receipt_refs_incomplete",
    ):
        if state in blocker_ids:
            return state
    return blocker_ids[0]


def _input_surface_summaries(
    *,
    codex_bundle: Mapping[str, Any],
    operator_projection: Mapping[str, Any],
    physical_projection: Mapping[str, Any],
    evidence_ledger: Mapping[str, Any] | None,
    receipt_projection: Mapping[str, Any] | None,
) -> dict[str, dict[str, Any] | None]:
    return {
        "codex_stage_execution_receipt_bundle": _surface_summary(codex_bundle),
        "operator_closeout_readiness_projection": _surface_summary(operator_projection),
        "physical_morphology_guard_projection": _surface_summary(physical_projection),
        "external_evidence_consumption_ledger": (
            _surface_summary(evidence_ledger) if evidence_ledger is not None else None
        ),
        "receipt_readiness_projection": (
            _surface_summary(receipt_projection) if receipt_projection is not None else None
        ),
    }


def _target_smoke_patch_loop_closeout(
    *,
    operator_projection: Mapping[str, Any],
) -> dict[str, Any]:
    production_tail = _mapping_from_path(
        operator_projection,
        ("production_acceptance_tail",),
        context="operator_closeout_readiness_projection.production_acceptance_tail",
    )
    raw_patch_refs = production_tail.get("patch_loop_refs")
    if raw_patch_refs is None:
        return _blocked_target_smoke_patch_loop_closeout(
            blocker_ref="typed-blocker:mag/target-smoke-patch-loop/patch-loop-refs-missing",
        )
    if not isinstance(raw_patch_refs, Mapping):
        raise WorkspaceStateError(
            "operator_closeout_readiness_projection.production_acceptance_tail.patch_loop_refs "
            "必须是 object。"
        )
    _assert_refs_body_free(raw_patch_refs, path="patch_loop_refs")

    owner_ref = _require_nonempty_string(
        raw_patch_refs.get("target_owner_receipt_or_typed_blocker_ref"),
        field_name="target_owner_receipt_or_typed_blocker_ref",
        context="patch_loop_refs",
    )
    no_forbidden_write_ref = _require_nonempty_string(
        raw_patch_refs.get("no_forbidden_write_proof_ref"),
        field_name="no_forbidden_write_proof_ref",
        context="patch_loop_refs",
    )
    return {
        "closeout_type": "refs_only_target_smoke_patch_loop",
        "suite_result": "blocked_suite",
        "blocked_suite_result_ref": _require_nonempty_string(
            raw_patch_refs.get("blocked_suite_result_ref"),
            field_name="blocked_suite_result_ref",
            context="patch_loop_refs",
        ),
        "developer_work_order_ref": _require_nonempty_string(
            raw_patch_refs.get("developer_patch_work_order_ref"),
            field_name="developer_patch_work_order_ref",
            context="patch_loop_refs",
        ),
        "patch_traceability_ref": _require_nonempty_string(
            raw_patch_refs.get("patch_traceability_matrix_ref"),
            field_name="patch_traceability_matrix_ref",
            context="patch_loop_refs",
        ),
        "target_verification_refs": _string_list_from_path(
            raw_patch_refs,
            ("target_repo_verification_refs",),
            context="patch_loop_refs.target_repo_verification_refs",
        ),
        "runtime_read_model_consumption_ref": _require_nonempty_string(
            raw_patch_refs.get("target_runtime_read_model_consumption_ref"),
            field_name="target_runtime_read_model_consumption_ref",
            context="patch_loop_refs",
        ),
        "workspace_proof_ref": _require_nonempty_string(
            raw_patch_refs.get("workspace_environment_proof_ref"),
            field_name="workspace_environment_proof_ref",
            context="patch_loop_refs",
        ),
        "no_forbidden_write": {
            "proven": True,
            "proof_ref": no_forbidden_write_ref,
            "grant_truth_written": False,
            "artifact_body_written": False,
            "memory_body_written": False,
            "fundability_verdict_written": False,
            "quality_verdict_written": False,
            "export_verdict_written": False,
            "owner_receipt_authority_overwritten": False,
        },
        "owner_receipt_or_typed_blocker": {
            "required": True,
            "return_shape": _owner_receipt_or_blocker_shape(owner_ref),
            "ref": owner_ref,
        },
        "patch_absorption_ref": _require_nonempty_string(
            raw_patch_refs.get("patch_absorption_ref"),
            field_name="patch_absorption_ref",
            context="patch_loop_refs",
        ),
        "worktree_cleanup_ref": _require_nonempty_string(
            raw_patch_refs.get("worktree_cleanup_ref"),
            field_name="worktree_cleanup_ref",
            context="patch_loop_refs",
        ),
        "agent_lab_re_evaluation_ref": _require_nonempty_string(
            raw_patch_refs.get("agent_lab_re_evaluation_ref"),
            field_name="agent_lab_re_evaluation_ref",
            context="patch_loop_refs",
        ),
        "suite_pass_equals_closeout": False,
        "can_declare_fundability_ready": False,
        "can_declare_quality_ready": False,
        "can_declare_export_ready": False,
        "can_declare_submission_ready": False,
        "projection_policy": (
            "target_smoke_closeout_consumes_refs_only_blocked_suite_requires_owner_receipt_"
            "or_typed_blocker_no_forbidden_write_cleanup_and_agent_lab_re_evaluation_refs"
        ),
    }


def _blocked_target_smoke_patch_loop_closeout(*, blocker_ref: str) -> dict[str, Any]:
    return {
        "closeout_type": "refs_only_target_smoke_patch_loop",
        "suite_result": "blocked_suite",
        "typed_blocker_ref": blocker_ref,
        "owner_receipt_or_typed_blocker": {
            "required": True,
            "return_shape": "typed_blocker_ref",
            "ref": blocker_ref,
        },
        "suite_pass_equals_closeout": False,
        "can_declare_fundability_ready": False,
        "can_declare_quality_ready": False,
        "can_declare_export_ready": False,
        "can_declare_submission_ready": False,
    }


def _owner_receipt_or_blocker_shape(ref: str) -> str:
    normalized = ref.strip().lower()
    if "typed-blocker" in normalized or "typed_blocker" in normalized:
        return "typed_blocker_ref"
    if "no-regression" in normalized or "no_regression" in normalized:
        return "no_regression_evidence_ref"
    return "owner_receipt_ref"


def _surface_summary(surface: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "surface_kind": _require_nonempty_string(
            surface.get("surface_kind"),
            field_name="surface_kind",
            context="input_surface",
        ),
        "state": _surface_state(surface, context="input_surface"),
        "owner": _require_nonempty_string(
            surface.get("owner", TARGET_DOMAIN_ID),
            field_name="owner",
            context="input_surface",
        ),
    }


def _operator_next_attention(state: str, blockers: list[Mapping[str, Any]]) -> dict[str, Any]:
    if not blockers:
        return {
            "attention_id": "quality_verdict_still_domain_owned",
            "state": state,
            "owner": TARGET_DOMAIN_ID,
        }
    first_blocker = blockers[0]
    return {
        "attention_id": _require_nonempty_string(
            first_blocker.get("blocker_id"),
            field_name="blocker_id",
            context="blockers[0]",
        ),
        "state": state,
        "owner": _require_nonempty_string(
            first_blocker.get("owner"),
            field_name="owner",
            context="blockers[0]",
        ),
    }


def _operator_real_evidence_gap_ids(operator_projection: Mapping[str, Any]) -> list[str]:
    accounting = _mapping_from_path(
        operator_projection,
        ("external_evidence_accounting",),
        context="operator_closeout_readiness_projection.external_evidence_accounting",
    )
    return _string_list_from_path(
        accounting,
        ("remaining_real_evidence_gap_ids",),
        context=(
            "operator_closeout_readiness_projection.external_evidence_accounting."
            "remaining_real_evidence_gap_ids"
        ),
    )


def _external_evidence_missing_ids(ledger: Mapping[str, Any]) -> list[str]:
    state = _surface_state(ledger, context="external_evidence_consumption_ledger")
    missing_ids = _string_list_from_path(
        ledger,
        ("missing_request_ids",),
        context="external_evidence_consumption_ledger.missing_request_ids",
    )
    if state != _EXTERNAL_EVIDENCE_READY_STATE and not missing_ids:
        return [state]
    return missing_ids


def _surface_state(surface: Mapping[str, Any], *, context: str) -> str:
    return _require_nonempty_string(surface.get("state"), field_name="state", context=context)


def _mapping_from_path(
    value: Mapping[str, Any],
    path: tuple[str, ...],
    *,
    context: str,
) -> Mapping[str, Any]:
    item: Any = value
    for key in path:
        if not isinstance(item, Mapping) or not isinstance(item.get(key), Mapping):
            raise WorkspaceStateError(f"{context} 必须是 object。")
        item = item[key]
    return item


def _string_list_from_path(
    value: Mapping[str, Any],
    path: tuple[str, ...],
    *,
    context: str,
) -> list[str]:
    item: Any = value
    for key in path:
        if not isinstance(item, Mapping):
            raise WorkspaceStateError(f"{context} 必须是 string list。")
        item = item.get(key)
    if not isinstance(item, list):
        raise WorkspaceStateError(f"{context} 必须是 string list。")
    return [
        _require_nonempty_string(entry, field_name="ref", context=context)
        for entry in item
    ]


def _nonnegative_int_from_path(
    value: Mapping[str, Any],
    path: tuple[str, ...],
    *,
    context: str,
) -> int:
    item: Any = value
    for key in path:
        if not isinstance(item, Mapping):
            raise WorkspaceStateError(f"{context} 必须是非负整数。")
        item = item.get(key)
    if not isinstance(item, int) or item < 0:
        raise WorkspaceStateError(f"{context} 必须是非负整数。")
    return item


def _assert_refs_body_free(value: Any, *, path: str) -> None:
    if isinstance(value, Mapping):
        for raw_key, item in value.items():
            key = _require_nonempty_string(raw_key, field_name="key", context=path)
            normalized_key = _normalize_key(key)
            if _is_forbidden_body_key(normalized_key) and not (
                normalized_key in _NEGATED_BODY_CAPABILITY_KEYS and item is False
            ):
                raise WorkspaceStateError(f"executor-first closeout bundle 禁止包含 body 字段: {path}.{key}")
            if normalized_key in _FORBIDDEN_READY_CLAIM_KEYS and bool(item):
                raise WorkspaceStateError(
                    f"executor-first closeout bundle 禁止包含 ready claim: {path}.{key}"
                )
            _assert_refs_body_free(item, path=f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _assert_refs_body_free(item, path=f"{path}[{index}]")


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


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped


__all__ = [
    "MAG_EXECUTOR_FIRST_CLOSEOUT_BUNDLE_KIND",
    "build_executor_first_closeout_bundle",
]
