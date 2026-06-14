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
)
from med_autogrant.artifact_bundle import build_artifact_bundle_document
from med_autogrant.critique_executor import build_critique_execution_document
from med_autogrant.revision_executor import build_revision_execution_document

from med_autogrant.domain_runtime_parts.io import (
    _guard_artifact_bundle_output_identity,
    _guard_critique_output_identity,
    _guard_revision_output_identity,
    _write_artifact_bundle_output,
    _write_revised_workspace_output,
)


class DomainRuntimeHandoffSurfaceMixin:
    def execute_direction_screening_pass(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        execution_document = build_direction_screening_execution_document(
            document=self._load_workspace(input_path),
            input_path=input_path,
        )
        return self._write_authoring_execution_output(
            command="execute-direction-screening-pass",
            output_path=output_path,
            execution_document=execution_document,
            execution_key="direction_screening_execution",
            workspace_key="direction_screening_workspace",
        )

    def execute_question_refinement_pass(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        execution_document = build_question_refinement_execution_document(
            document=self._load_workspace(input_path),
            input_path=input_path,
        )
        return self._write_authoring_execution_output(
            command="execute-question-refinement-pass",
            output_path=output_path,
            execution_document=execution_document,
            execution_key="question_refinement_execution",
            workspace_key="question_refinement_workspace",
        )

    def execute_argument_building_pass(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        execution_document = build_argument_building_execution_document(
            document=self._load_workspace(input_path),
            input_path=input_path,
        )
        return self._write_authoring_execution_output(
            command="execute-argument-building-pass",
            output_path=output_path,
            execution_document=execution_document,
            execution_key="argument_building_execution",
            workspace_key="argument_building_workspace",
        )

    def execute_fit_alignment_pass(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        execution_document = build_fit_alignment_execution_document(
            document=self._load_workspace(input_path),
            input_path=input_path,
        )
        return self._write_authoring_execution_output(
            command="execute-fit-alignment-pass",
            output_path=output_path,
            execution_document=execution_document,
            execution_key="fit_alignment_execution",
            workspace_key="fit_alignment_workspace",
        )

    def execute_outline_pass(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        execution_document = build_outline_execution_document(
            document=self._load_workspace(input_path),
            input_path=input_path,
        )
        return self._write_authoring_execution_output(
            command="execute-outline-pass",
            output_path=output_path,
            execution_document=execution_document,
            execution_key="outline_execution",
            workspace_key="outline_workspace",
        )

    def execute_drafting_pass(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        execution_document = build_drafting_execution_document(
            document=self._load_workspace(input_path),
            input_path=input_path,
        )
        return self._write_authoring_execution_output(
            command="execute-drafting-pass",
            output_path=output_path,
            execution_document=execution_document,
            execution_key="drafting_execution",
            workspace_key="drafting_workspace",
        )

    def build_artifact_bundle(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        bundle = build_artifact_bundle_document(document=document)
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
        revision_document = build_revision_execution_document(document=document)
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
        critique_document = build_critique_execution_document(
            document=self._load_workspace(input_path),
            input_path=input_path,
            executor_kind=executor_kind,
        )
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
