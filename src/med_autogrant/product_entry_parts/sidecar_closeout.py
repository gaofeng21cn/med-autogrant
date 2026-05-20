from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Protocol

from med_autogrant.product_entry_parts.primitives import (
    _optional_mapping,
    _require_mapping,
    _require_nonempty_string,
    _require_nonempty_string_from_mapping,
)
from med_autogrant.workspace_types import WorkspaceStateError


class DispatchPayload(Protocol):
    def __call__(
        self,
        *,
        action: str,
        task: Mapping[str, Any],
        task_path: Path,
        input_path: str,
        status: str,
        result: Mapping[str, Any],
        executed_command: str | None,
    ) -> dict[str, Any]: ...


def _dispatch_codex_stage_receipts(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
    dispatch_payload: DispatchPayload,
) -> dict[str, Any]:
    receipt_bundle = product_entry.build_codex_stage_execution_receipt_bundle(
        stage_id=_require_nonempty_string_from_mapping(task, "stage_id", context="sidecar_task"),
        execution_attempts=_required_mapping_list(task, "execution_attempts"),
        review_attempts=_optional_mapping_list(task.get("review_attempts")),
    )
    return dispatch_payload(
        action="closeout/codex-stage-receipts",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "sidecar_codex_stage_receipts_result",
            "receipt_bundle": receipt_bundle,
            "write_policy": "read_projection_only_no_domain_truth_mutation",
        },
        executed_command=None,
    )


def _dispatch_operator_readiness(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
    dispatch_payload: DispatchPayload,
) -> dict[str, Any]:
    closeout_readiness = product_entry.build_operator_closeout_readiness_projection(
        production_acceptance=_require_mapping(
            task,
            "production_acceptance",
            context="sidecar_task",
        ),
        external_evidence_receipt_ledger=_require_mapping(
            task,
            "external_evidence_receipt_ledger",
            context="sidecar_task",
        ),
        receipt_readiness_projection=_require_mapping(
            task,
            "receipt_readiness_projection",
            context="sidecar_task",
        ),
    )
    return dispatch_payload(
        action="closeout/operator-readiness",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "sidecar_operator_closeout_readiness_result",
            "operator_closeout_readiness": closeout_readiness,
            "write_policy": "read_projection_only_no_domain_truth_mutation",
        },
        executed_command=None,
    )


def _dispatch_physical_morphology_guard(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
    dispatch_payload: DispatchPayload,
) -> dict[str, Any]:
    morphology_guard = product_entry.build_physical_morphology_guard_projection(
        source_items=_required_mapping_list(task, "source_items"),
        external_evidence_refs=_optional_string_list(task.get("external_evidence_refs")),
    )
    return dispatch_payload(
        action="closeout/physical-morphology-guard",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "sidecar_physical_morphology_guard_result",
            "physical_morphology_guard": morphology_guard,
            "write_policy": "read_projection_only_no_domain_truth_mutation",
        },
        executed_command=None,
    )


def _dispatch_executor_first_bundle(
    product_entry: Any,
    *,
    task: Mapping[str, Any],
    input_path: str,
    task_path: Path,
    dispatch_payload: DispatchPayload,
) -> dict[str, Any]:
    closeout_bundle = product_entry.build_executor_first_closeout_bundle(
        codex_stage_execution_receipt_bundle=_require_mapping(
            task,
            "codex_stage_execution_receipt_bundle",
            context="sidecar_task",
        ),
        operator_closeout_readiness_projection=_require_mapping(
            task,
            "operator_closeout_readiness_projection",
            context="sidecar_task",
        ),
        physical_morphology_guard_projection=_require_mapping(
            task,
            "physical_morphology_guard_projection",
            context="sidecar_task",
        ),
        external_evidence_consumption_ledger=_optional_mapping(
            task,
            "external_evidence_consumption_ledger",
        ),
        receipt_readiness_projection=_optional_mapping(
            task,
            "receipt_readiness_projection",
        ),
    )
    return dispatch_payload(
        action="closeout/executor-first-bundle",
        task=task,
        task_path=task_path,
        input_path=input_path,
        status="completed",
        result={
            "surface_kind": "sidecar_executor_first_closeout_bundle_result",
            "executor_first_closeout_bundle": closeout_bundle,
            "write_policy": "read_projection_only_no_domain_truth_mutation",
        },
        executed_command=None,
    )


def _optional_mapping_list(value: Any) -> list[Mapping[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise WorkspaceStateError("sidecar_task refs 必须是 object list。")
    items: list[Mapping[str, Any]] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise WorkspaceStateError("sidecar_task refs 必须是 object list。")
        items.append(item)
    return items


def _required_mapping_list(task: Mapping[str, Any], field_name: str) -> list[Mapping[str, Any]]:
    items = _optional_mapping_list(task.get(field_name))
    if not items:
        raise WorkspaceStateError(f"sidecar_task.{field_name} 必须是非空 object list。")
    return items


def _optional_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise WorkspaceStateError("sidecar_task refs 必须是 string list。")
    refs: list[str] = []
    for item in value:
        refs.append(_require_nonempty_string(item, field_name="ref", context="sidecar_task"))
    return refs
