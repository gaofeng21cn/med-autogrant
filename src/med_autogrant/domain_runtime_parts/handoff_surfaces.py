from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.authoring_executor import (
    build_argument_building_execution_document,
    build_direction_screening_execution_document,
    build_drafting_execution_document,
    build_fit_alignment_execution_document,
    build_outline_execution_document,
    build_question_refinement_execution_document,
    build_strategy_authoring_execution_document,
)
from med_autogrant.artifact_bundle import build_artifact_bundle_document
from med_autogrant.critique_executor import build_critique_execution_document
from med_autogrant.revision_executor import build_revision_execution_document
from med_autogrant.workspace_types import WorkspaceStateError

from med_autogrant.domain_runtime_parts.io import (
    _guard_artifact_bundle_output_identity,
    _guard_critique_output_identity,
    _guard_revision_output_identity,
    _write_artifact_bundle_output,
    _write_revised_workspace_output,
)


def execute_strategy_authoring_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    return _execute_authoring_progress_first(
        self,
        command="execute-strategy-authoring-pass",
        input_path=input_path,
        output_path=output_path,
        builder=build_strategy_authoring_execution_document,
        execution_key="strategy_authoring_execution",
        workspace_key="strategy_authoring_workspace",
    )


def execute_direction_screening_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    return _execute_authoring_progress_first(
        self,
        command="execute-direction-screening-pass",
        input_path=input_path,
        output_path=output_path,
        builder=build_direction_screening_execution_document,
        execution_key="direction_screening_execution",
        workspace_key="direction_screening_workspace",
    )

def execute_question_refinement_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    return _execute_authoring_progress_first(
        self,
        command="execute-question-refinement-pass",
        input_path=input_path,
        output_path=output_path,
        builder=build_question_refinement_execution_document,
        execution_key="question_refinement_execution",
        workspace_key="question_refinement_workspace",
    )

def execute_argument_building_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    return _execute_authoring_progress_first(
        self,
        command="execute-argument-building-pass",
        input_path=input_path,
        output_path=output_path,
        builder=build_argument_building_execution_document,
        execution_key="argument_building_execution",
        workspace_key="argument_building_workspace",
    )

def execute_fit_alignment_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    return _execute_authoring_progress_first(
        self,
        command="execute-fit-alignment-pass",
        input_path=input_path,
        output_path=output_path,
        builder=build_fit_alignment_execution_document,
        execution_key="fit_alignment_execution",
        workspace_key="fit_alignment_workspace",
    )

def execute_outline_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    return _execute_authoring_progress_first(
        self,
        command="execute-outline-pass",
        input_path=input_path,
        output_path=output_path,
        builder=build_outline_execution_document,
        execution_key="outline_execution",
        workspace_key="outline_workspace",
    )

def execute_drafting_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    return _execute_authoring_progress_first(
        self,
        command="execute-drafting-pass",
        input_path=input_path,
        output_path=output_path,
        builder=build_drafting_execution_document,
        execution_key="drafting_execution",
        workspace_key="drafting_workspace",
    )


def _execute_authoring_progress_first(
    runtime,
    *,
    command: str,
    input_path: str | Path,
    output_path: str | Path,
    builder,
    execution_key: str,
    workspace_key: str,
) -> dict[str, Any]:
    document = runtime._load_workspace(input_path)
    try:
        execution_document = builder(document=document, input_path=input_path)
    except WorkspaceStateError as error:
        return _stage_progress_diagnostic(command=command, document=document, error=error)
    return runtime._write_authoring_execution_output(
        command=command,
        output_path=output_path,
        execution_document=execution_document,
        execution_key=execution_key,
        workspace_key=workspace_key,
    )


def _stage_progress_diagnostic(
    *,
    command: str,
    document: dict[str, Any],
    error: WorkspaceStateError,
) -> dict[str, Any]:
    return {
        "ok": True,
        "command": command,
        "status": "completed_with_quality_debt",
        "grant_run_id": document.get("grant_run_id"),
        "workspace_id": document.get("workspace_id"),
        "lifecycle_stage": document.get("lifecycle_stage"),
        "source_workspace_preserved": True,
        "output_path": None,
        "stage_attempt_diagnostic": {
            "failure_kind": "authoring_input_or_output_quality_debt",
            "detail": str(error),
        },
        "quality_debt": {
            "status": "recorded_non_blocking",
            "reasons": [str(error)],
            "blocks_stage_transition": False,
            "blocks_quality_submission_export_or_ready_claims": True,
        },
        "next_stage_may_start": True,
        "semantic_route_owner": "decisive_codex_attempt",
        "recommended_route_back_stage": document.get("lifecycle_stage"),
    }

def build_artifact_bundle(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    document = self._load_workspace(input_path)
    try:
        bundle = build_artifact_bundle_document(document=document)
    except WorkspaceStateError as error:
        return _stage_progress_diagnostic(
            command="build-artifact-bundle",
            document=document,
            error=error,
        )
    resolved_output_path = Path(output_path).expanduser().resolve()
    _guard_artifact_bundle_output_identity(
        resolved_output_path,
        grant_run_id=bundle["grant_run_id"],
        workspace_id=bundle["workspace_id"],
        draft_id=bundle["draft_id"],
        lifecycle_stage=bundle["lifecycle_stage"],
    )
    _write_artifact_bundle_output(resolved_output_path, bundle)
    return {
        "ok": True,
        "command": "build-artifact-bundle",
        "grant_run_id": bundle["grant_run_id"],
        "workspace_id": bundle["workspace_id"],
        "draft_id": bundle["draft_id"],
        "lifecycle_stage": bundle["lifecycle_stage"],
        "output_path": str(resolved_output_path),
        "bundle": bundle,
    }

def execute_revision_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    document = self._load_workspace(input_path)
    try:
        revision_document = build_revision_execution_document(document=document)
    except WorkspaceStateError as error:
        return _stage_progress_diagnostic(
            command="execute-revision-pass",
            document=document,
            error=error,
        )
    resolved_output_path = Path(output_path).expanduser().resolve()
    _guard_revision_output_identity(
        resolved_output_path,
        grant_run_id=revision_document["grant_run_id"],
        workspace_id=revision_document["workspace_id"],
        draft_id=revision_document["draft_id"],
        active_revision_plan_id=revision_document["active_revision_plan_id"],
        lifecycle_stage=revision_document["lifecycle_stage"],
    )
    _write_revised_workspace_output(
        resolved_output_path,
        revision_document["revised_workspace"],
    )
    return {
        "ok": True,
        "command": "execute-revision-pass",
        "grant_run_id": revision_document["grant_run_id"],
        "workspace_id": revision_document["workspace_id"],
        "draft_id": revision_document["draft_id"],
        "lifecycle_stage": revision_document["lifecycle_stage"],
        "output_path": str(resolved_output_path),
        "revision_execution": revision_document["revision_execution"],
        "revised_workspace": revision_document["revised_workspace"],
    }

def execute_critique_pass(
    self,
    *,
    input_path: str | Path,
    output_path: str | Path,
    executor_kind: str | None = None,
) -> dict[str, Any]:
    source_document = self._load_workspace(input_path)
    try:
        critique_document = build_critique_execution_document(
            document=source_document,
            input_path=input_path,
            executor_kind=executor_kind,
        )
    except WorkspaceStateError as error:
        return {
            "ok": True,
            "command": "execute-critique-pass",
            "status": "completed_with_quality_debt",
            "grant_run_id": source_document.get("grant_run_id"),
            "workspace_id": source_document.get("workspace_id"),
            "lifecycle_stage": source_document.get("lifecycle_stage"),
            "source_workspace_preserved": True,
            "output_path": None,
            "quality_debt": {
                "code": "critique_executor_or_output_shape_gap",
                "detail": str(error),
                "blocks_stage_transition": False,
                "blocks_quality_submission_export_or_ready_claims": True,
            },
            "next_stage_may_start": True,
            "route_back_selection_owner": "decisive_codex_attempt",
            "recommended_route_back_stage": source_document.get("lifecycle_stage"),
        }
    resolved_output_path = Path(output_path).expanduser().resolve()
    _guard_critique_output_identity(
        resolved_output_path,
        grant_run_id=critique_document["grant_run_id"],
        workspace_id=critique_document["workspace_id"],
        draft_id=critique_document["draft_id"],
        active_revision_plan_id=critique_document["active_revision_plan_id"],
        lifecycle_stage=critique_document["lifecycle_stage"],
    )
    _write_revised_workspace_output(
        resolved_output_path,
        critique_document["critique_workspace"],
    )
    return {
        "ok": True,
        "command": "execute-critique-pass",
        "grant_run_id": critique_document["grant_run_id"],
        "workspace_id": critique_document["workspace_id"],
        "draft_id": critique_document["draft_id"],
        "lifecycle_stage": critique_document["lifecycle_stage"],
        "output_path": str(resolved_output_path),
        "critique_execution": critique_document["critique_execution"],
        "critique_workspace": critique_document["critique_workspace"],
    }
