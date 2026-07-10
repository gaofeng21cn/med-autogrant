from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from med_autogrant.authoring_executor import (
    build_argument_building_execution_document,
    build_direction_screening_execution_document,
    build_drafting_execution_document,
    build_fit_alignment_execution_document,
    build_freeze_execution_document,
    build_outline_execution_document,
    build_question_refinement_execution_document,
)
from med_autogrant.control_plane import (
    resolve_runtime_state_root,
    runtime_state_display_path,
)
from med_autogrant.critique_executor import build_critique_execution_document
from med_autogrant.critique_loop_controller import run_critique_revision_closed_loop
from med_autogrant.authoring_mainline_controller import run_authoring_mainline_controller
from med_autogrant.grant_quality import (
    build_grant_quality_closure_dossier,
    build_grant_quality_diff,
    build_grant_quality_scorecard,
)
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.revision_executor import build_revision_execution_document
from med_autogrant.route_report import build_stage_route_report
from med_autogrant.stage_router import determine_next_step
from med_autogrant.domain_runtime_parts.package_surface import DomainRuntimePackageSurfaceMixin
from med_autogrant.workspace import (
    load_workspace_document,
)
from med_autogrant.workspace_projection_parts import _require_workspace_context
from med_autogrant.workspace_types import WorkspaceStateError
from med_autogrant.domain_runtime_parts.shared import (
    CRITIQUE_LOOP_REPORT_SCHEMA_FILE,
)
from med_autogrant.domain_runtime_parts.io import (
    _guard_critique_output_identity,
    _guard_revision_output_identity,
    _guard_workspace_output_identity,
    _write_json_output,
    _write_revised_workspace_output,
)
from med_autogrant.domain_runtime_parts.contracts import validate_schema_payload as _validate_schema_payload
from med_autogrant.domain_runtime_parts.authoring_mainline import build_authoring_mainline_payload


class DomainRuntimeAuthoringSurfaceMixin(DomainRuntimePackageSurfaceMixin):
    def execute_critique_revision_loop(
        self,
        *,
        input_path: str | Path,
        output_dir: str | Path,
        max_rounds: int = 3,
        executor_kind: str | None = None,
        opl_stage_attempt: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        starting_document = self._load_workspace(resolved_input_path)
        starting_stage = str(starting_document.get("lifecycle_stage") or "").strip()
        if starting_stage not in {"drafting", "revision"}:
            raise WorkspaceStateError("execute-critique-revision-loop 只允许从 drafting 或 revision 进入。")
        resolved_output_dir = Path(output_dir).expanduser().resolve()
        resolved_output_dir.mkdir(parents=True, exist_ok=True)

        current_round = {"index": 0}

        def critique_runner(document: dict[str, Any]) -> dict[str, Any]:
            current_round["index"] += 1
            critique_document = build_critique_execution_document(
                document=document,
                input_path=resolved_input_path,
                executor_kind=executor_kind,
            )
            critique_path = resolved_output_dir / f"round-{current_round['index']:02d}-critique-workspace.json"
            _guard_critique_output_identity(
                critique_path,
                grant_run_id=critique_document["grant_run_id"],
                workspace_id=critique_document["workspace_id"],
                draft_id=critique_document["draft_id"],
                active_revision_plan_id=critique_document["active_revision_plan_id"],
                lifecycle_stage=critique_document["lifecycle_stage"],
            )
            _write_revised_workspace_output(critique_path, critique_document["critique_workspace"])
            return {
                "critique_workspace": critique_document["critique_workspace"],
            }

        def revision_runner(document: dict[str, Any]) -> dict[str, Any]:
            revision_document = build_revision_execution_document(document=document)
            revision_path = resolved_output_dir / f"round-{current_round['index']:02d}-revision-workspace.json"
            _guard_revision_output_identity(
                revision_path,
                grant_run_id=revision_document["grant_run_id"],
                workspace_id=revision_document["workspace_id"],
                draft_id=revision_document["draft_id"],
                active_revision_plan_id=revision_document["active_revision_plan_id"],
                lifecycle_stage=revision_document["lifecycle_stage"],
            )
            _write_revised_workspace_output(revision_path, revision_document["revised_workspace"])
            return {
                "revised_workspace": revision_document["revised_workspace"],
            }

        loop = run_critique_revision_closed_loop(
            current_document=starting_document,
            max_rounds=max_rounds,
            critique_runner=critique_runner,
            revision_runner=revision_runner,
            route_resolver=determine_next_step,
            opl_stage_attempt=opl_stage_attempt,
        )
        final_workspace = loop["final_workspace"]
        final_route = loop["final_route"]
        final_workspace_path = resolved_output_dir / "critique-loop-final-workspace.json"
        _guard_workspace_output_identity(
            final_workspace_path,
            workspace_document=final_workspace,
            draft_id=_require_workspace_context(final_workspace).active_draft["draft_id"]
            if final_workspace.get("lifecycle_stage") in {"outline", "drafting", "critique", "revision", "frozen"}
            and final_workspace.get("current_selection", {}).get("active_draft_id")
            else None,
        )
        _write_revised_workspace_output(final_workspace_path, final_workspace)
        quality_scorecard = build_grant_quality_scorecard(final_workspace)
        quality_closure_dossier = build_grant_quality_closure_dossier(final_workspace)
        loop_report = {
            "surface_kind": "critique_loop_report",
            "loop_version": 1,
            "loop_status": loop["loop_status"],
            "loop_status_role": loop["loop_status_role"],
            "stage_transition_authority": loop["stage_transition_authority"],
            "authority_boundary": loop["authority_boundary"],
            "stage_transition_intent": loop["stage_transition_intent"],
            "authority_return": loop["authority_return"],
            "started_from_stage": starting_stage,
            "completed_rounds": len(loop["rounds"]),
            "max_rounds": max_rounds,
            "termination_reason": loop["termination_reason"],
            "final_stage": final_workspace["lifecycle_stage"],
            "final_recommended_stage": final_route.get("recommended_stage"),
            "rounds": [
                {
                    "round": item["round"],
                    "decision": item["decision"],
                    "critique_stage": item["critique_workspace"]["lifecycle_stage"],
                    "revision_stage": (
                        item["revision_workspace"]["lifecycle_stage"]
                        if isinstance(item.get("revision_workspace"), dict)
                        else None
                    ),
                    "recommended_stage": item["route"].get("recommended_stage"),
                    "route_reason": item["route"].get("reason") or "unknown",
                }
                for item in loop["rounds"]
            ],
            "grant_quality_scorecard": quality_scorecard,
            "grant_quality_closure_dossier": quality_closure_dossier,
        }
        if isinstance(loop.get("typed_blocker"), dict):
            loop_report["typed_blocker"] = loop["typed_blocker"]
        _validate_schema_payload(
            loop_report,
            schema_file=CRITIQUE_LOOP_REPORT_SCHEMA_FILE,
            context="critique_loop_report",
        )
        loop_report_path = resolved_output_dir / "critique-loop-report.json"
        _write_json_output(loop_report_path, loop_report, label="critique loop report")
        return {
            "ok": True,
            "command": "execute-critique-revision-loop",
            "grant_run_id": final_workspace["grant_run_id"],
            "workspace_id": final_workspace["workspace_id"],
            "draft_id": (
                _require_workspace_context(final_workspace).active_draft["draft_id"]
                if final_workspace.get("current_selection", {}).get("active_draft_id")
                else None
            ),
            "lifecycle_stage": final_workspace["lifecycle_stage"],
            "output_dir": str(resolved_output_dir),
            "loop_report_path": str(loop_report_path),
            "final_workspace_path": str(final_workspace_path),
            "loop_report": loop_report,
            "final_workspace": final_workspace,
        }

    def execute_authoring_mainline_loop(
        self,
        *,
        input_path: str | Path,
        output_dir: str | Path,
        max_cycles: int = 8,
        executor_kind: str | None = None,
        opl_stage_attempt: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        starting_workspace = self._load_workspace(resolved_input_path)
        resolved_output_dir = Path(output_dir).expanduser().resolve()
        resolved_output_dir.mkdir(parents=True, exist_ok=True)

        return build_authoring_mainline_payload(
            runtime=self,
            input_path=resolved_input_path,
            output_dir=resolved_output_dir,
            starting_workspace=starting_workspace,
            max_cycles=max_cycles,
            executor_kind=executor_kind,
            opl_stage_attempt=opl_stage_attempt,
            run_authoring_mainline_controller=run_authoring_mainline_controller,
        )

    def execute_freeze_pass(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        execution_document = build_freeze_execution_document(
            document=self._load_workspace(input_path),
        )
        return self._write_authoring_execution_output(
            command="execute-freeze-pass",
            output_path=output_path,
            execution_document=execution_document,
            execution_key="freeze_execution",
            workspace_key="frozen_workspace",
        )

    def _write_authoring_execution_output(
        self,
        *,
        command: str,
        output_path: str | Path,
        execution_document: dict[str, Any],
        execution_key: str,
        workspace_key: str,
    ) -> dict[str, Any]:
        resolved_output_path = Path(output_path).expanduser().resolve()
        workspace_document = execution_document[workspace_key]
        _guard_workspace_output_identity(
            resolved_output_path,
            workspace_document=workspace_document,
            draft_id=execution_document.get("draft_id"),
        )
        _write_revised_workspace_output(resolved_output_path, workspace_document)
        return {
            "ok": True,
            "command": command,
            "grant_run_id": execution_document["grant_run_id"],
            "workspace_id": execution_document["workspace_id"],
            "draft_id": execution_document.get("draft_id"),
            "lifecycle_stage": execution_document["lifecycle_stage"],
            "output_path": str(resolved_output_path),
            execution_key: execution_document[execution_key],
            workspace_key: workspace_document,
        }
