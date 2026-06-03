from __future__ import annotations

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
from med_autogrant.critique_executor import build_critique_execution_document
from med_autogrant.grant_quality import (
    build_grant_quality_closure_dossier,
    build_grant_quality_scorecard,
)
from med_autogrant.revision_executor import build_revision_execution_document
from med_autogrant.stage_router import determine_next_step
from med_autogrant.workspace_projection_parts import _require_workspace_context
from med_autogrant.workspace_types import WorkspaceStateError

from med_autogrant.domain_runtime_parts.io import (
    _guard_workspace_output_identity,
    _write_json_output,
    _write_revised_workspace_output,
)
from med_autogrant.domain_runtime_parts.runtime_ops import _apply_quality_gate_to_route
from med_autogrant.domain_runtime_parts.shared import AUTHORING_MAINLINE_LOOP_REPORT_SCHEMA_FILE
from med_autogrant.domain_runtime_parts.contracts import validate_schema_payload as _validate_schema_payload


AUTHORING_MAINLINE_STAGE_NAMES = (
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
)


class AuthoringMainlineRuntime:
    def __init__(
        self,
        *,
        runtime: Any,
        input_path: Path,
        output_dir: Path,
        executor_kind: str | None,
    ) -> None:
        self._runtime = runtime
        self._input_path = input_path
        self._output_dir = output_dir
        self._executor_kind = executor_kind
        self._cycle = 0

    def build_stage_runners(self) -> dict[str, Any]:
        return {stage_name: self._stage_runner(stage_name) for stage_name in AUTHORING_MAINLINE_STAGE_NAMES}

    def quality_aware_route_resolver(self, workspace: dict[str, Any]) -> dict[str, Any]:
        route = determine_next_step(workspace)
        quality_scorecard = build_grant_quality_scorecard(workspace)
        return _apply_quality_gate_to_route(route=route, quality_scorecard=quality_scorecard)

    def write_final_workspace(self, workspace: dict[str, Any]) -> Path:
        final_workspace_path = self._output_dir / "authoring-mainline-final-workspace.json"
        self._write_cycle_workspace(final_workspace_path, workspace)
        return final_workspace_path

    def build_loop_report(
        self,
        *,
        starting_workspace: dict[str, Any],
        final_workspace: dict[str, Any],
        final_route: dict[str, Any],
        loop: dict[str, Any],
        max_cycles: int,
    ) -> dict[str, Any]:
        quality_scorecard = build_grant_quality_scorecard(final_workspace)
        quality_closure_dossier = build_grant_quality_closure_dossier(final_workspace)
        mainline_loop_report = {
            "surface_kind": "authoring_mainline_loop_report",
            "loop_version": 1,
            "loop_status": loop["loop_status"],
            "started_from_stage": starting_workspace["lifecycle_stage"],
            "completed_cycles": len(loop["cycles"]),
            "max_cycles": max_cycles,
            "termination_reason": loop["termination_reason"],
            "final_stage": final_workspace["lifecycle_stage"],
            "final_recommended_stage": final_route.get("recommended_stage"),
            "cycles": [
                {
                    "cycle": item["cycle"],
                    "decision": item["decision"],
                    "input_stage": item["input_workspace"]["lifecycle_stage"],
                    "recommended_stage": item["route"].get("recommended_stage"),
                    "route_reason": item["route"].get("reason") or "unknown",
                    "output_stage": (
                        item["output_workspace"]["lifecycle_stage"]
                        if isinstance(item.get("output_workspace"), dict)
                        else None
                    ),
                }
                for item in loop["cycles"]
            ],
            "grant_quality_scorecard": quality_scorecard,
            "grant_quality_closure_dossier": quality_closure_dossier,
        }
        if isinstance(loop.get("typed_blocker"), dict):
            mainline_loop_report["typed_blocker"] = loop["typed_blocker"]
        _validate_schema_payload(
            mainline_loop_report,
            schema_file=AUTHORING_MAINLINE_LOOP_REPORT_SCHEMA_FILE,
            context="authoring_mainline_loop_report",
        )
        return mainline_loop_report

    def write_loop_report(self, mainline_loop_report: dict[str, Any]) -> Path:
        report_path = self._output_dir / "authoring-mainline-loop-report.json"
        _write_json_output(report_path, mainline_loop_report, label="authoring mainline loop report")
        return report_path

    def extract_draft_id(self, workspace: dict[str, Any]) -> str | None:
        selection = workspace.get("current_selection") or {}
        draft_id = selection.get("active_draft_id")
        if isinstance(draft_id, str) and draft_id.strip():
            return draft_id
        return None

    def _materialize_loop_input(self, workspace: dict[str, Any]) -> Path:
        input_path_for_cycle = self._output_dir / f"cycle-{self._cycle + 1:02d}-input-workspace.json"
        _write_revised_workspace_output(input_path_for_cycle, workspace)
        return input_path_for_cycle

    def _write_cycle_workspace(self, path: Path, workspace: dict[str, Any]) -> None:
        _guard_workspace_output_identity(
            path,
            workspace_document=workspace,
            draft_id=self.extract_draft_id(workspace),
        )
        _write_revised_workspace_output(path, workspace)

    def _stage_runner(self, stage_name: str):
        def _runner(workspace: dict[str, Any]) -> dict[str, Any]:
            self._cycle += 1
            current_input_path = self._materialize_loop_input(workspace)
            next_workspace = self._build_stage_workspace(
                stage_name=stage_name,
                workspace=workspace,
                current_input_path=current_input_path,
            )
            output_path_for_cycle = self._output_dir / f"cycle-{self._cycle:02d}-{stage_name}-workspace.json"
            self._write_cycle_workspace(output_path_for_cycle, next_workspace)
            return {
                "workspace": next_workspace,
            }

        return _runner

    def _build_stage_workspace(
        self,
        *,
        stage_name: str,
        workspace: dict[str, Any],
        current_input_path: Path,
    ) -> dict[str, Any]:
        if stage_name == "direction_screening":
            return build_direction_screening_execution_document(
                document=workspace,
                input_path=current_input_path,
            )["direction_screening_workspace"]
        if stage_name == "question_refinement":
            return build_question_refinement_execution_document(
                document=workspace,
                input_path=current_input_path,
            )["question_refinement_workspace"]
        if stage_name == "argument_building":
            return build_argument_building_execution_document(
                document=workspace,
                input_path=current_input_path,
            )["argument_building_workspace"]
        if stage_name == "fit_alignment":
            return build_fit_alignment_execution_document(
                document=workspace,
                input_path=current_input_path,
            )["fit_alignment_workspace"]
        if stage_name == "outline":
            return build_outline_execution_document(
                document=workspace,
                input_path=current_input_path,
            )["outline_workspace"]
        if stage_name == "drafting":
            return build_drafting_execution_document(
                document=workspace,
                input_path=current_input_path,
            )["drafting_workspace"]
        if stage_name == "critique":
            return build_critique_execution_document(
                document=workspace,
                input_path=current_input_path,
                executor_kind=self._executor_kind,
            )["critique_workspace"]
        if stage_name == "revision":
            return build_revision_execution_document(document=workspace)["revised_workspace"]
        if stage_name == "frozen":
            return build_freeze_execution_document(document=workspace)["frozen_workspace"]
        raise WorkspaceStateError(f"execute-authoring-mainline-loop 不支持 stage runner: {stage_name}")


def build_authoring_mainline_payload(
    *,
    runtime: Any,
    input_path: Path,
    output_dir: Path,
    starting_workspace: dict[str, Any],
    max_cycles: int,
    executor_kind: str | None,
    opl_stage_attempt: dict[str, Any] | None,
    run_authoring_mainline_controller: Any,
) -> dict[str, Any]:
    authoring_runtime = AuthoringMainlineRuntime(
        runtime=runtime,
        input_path=input_path,
        output_dir=output_dir,
        executor_kind=executor_kind,
    )
    loop = run_authoring_mainline_controller(
        current_workspace=starting_workspace,
        max_cycles=max_cycles,
        route_resolver=authoring_runtime.quality_aware_route_resolver,
        stage_runners=authoring_runtime.build_stage_runners(),
        opl_stage_attempt=opl_stage_attempt,
    )
    final_workspace = loop["final_workspace"]
    final_route = loop["final_route"]
    final_workspace_path = authoring_runtime.write_final_workspace(final_workspace)
    mainline_loop_report = authoring_runtime.build_loop_report(
        starting_workspace=starting_workspace,
        final_workspace=final_workspace,
        final_route=final_route,
        loop=loop,
        max_cycles=max_cycles,
    )
    report_path = authoring_runtime.write_loop_report(mainline_loop_report)
    return {
        "ok": True,
        "command": "execute-authoring-mainline-loop",
        "grant_run_id": final_workspace["grant_run_id"],
        "workspace_id": final_workspace["workspace_id"],
        "draft_id": authoring_runtime.extract_draft_id(final_workspace),
        "lifecycle_stage": final_workspace["lifecycle_stage"],
        "output_dir": str(output_dir),
        "mainline_loop_report_path": str(report_path),
        "final_workspace_path": str(final_workspace_path),
        "mainline_loop_report": mainline_loop_report,
        "final_workspace": final_workspace,
    }


__all__ = [
    "AUTHORING_MAINLINE_STAGE_NAMES",
    "AuthoringMainlineRuntime",
    "build_authoring_mainline_payload",
    "_require_workspace_context",
]
