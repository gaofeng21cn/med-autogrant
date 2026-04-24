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
from med_autogrant.artifact_bundle import build_artifact_bundle_document
from med_autogrant.control_plane import (
    CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH,
    read_current_program_contract as _read_current_program_contract_from_contract,
    read_program_id as _read_program_id_from_contract,
    resolve_current_program_contract_path,
    resolve_runtime_state_root,
    runtime_state_display_path,
)
from med_autogrant.critique_executor import build_critique_execution_document
from med_autogrant.critique_loop_controller import run_critique_revision_closed_loop
from med_autogrant.authoring_mainline_controller import run_authoring_mainline_controller
from med_autogrant.grant_autonomy_controller import run_grant_autonomy_controller
from med_autogrant.grant_quality import (
    build_grant_quality_closure_dossier,
    build_grant_quality_diff,
    build_grant_quality_scorecard,
)
from med_autogrant.final_package import (
    _validate_required_artifact_bundle_fields,
    build_final_package_document,
)
from med_autogrant.hosted_contract_bundle import (
    SUPPORTED_FINAL_PACKAGE_VERSION,
    _validate_required_final_package_fields,
    build_hosted_contract_bundle_document,
)
from med_autogrant.submission_ready import build_submission_ready_package_document
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.upstream_hermes import HermesGrantRunLedger
from med_autogrant.revision_executor import build_revision_execution_document
from med_autogrant.route_report import build_stage_route_report
from med_autogrant.funding_landscape_discovery import discover_funding_landscape
from med_autogrant.funding_landscape_discovery import build_funding_landscape_cache
from med_autogrant.funding_landscape_discovery import build_funding_landscape_diff_report
from med_autogrant.project_profile_selector import (
    build_initialized_intake_workspace,
    select_project_profile,
)
from med_autogrant.stage_router import _build_forced_rollback_actions, determine_next_step
from med_autogrant.domain_entry_contract import (
    SERVICE_SAFE_ENTRY_ADAPTER,
    SERVICE_SAFE_ENTRY_SURFACE_KIND,
    build_domain_entry_contract,
)
from med_autogrant.workspace import (
    WorkspaceError,
    WorkspaceFileError,
    WorkspaceStateError,
    _SchemaSubsetValidator,
    _require_workspace_context,
    build_grant_evidence_grounding,
    build_grant_intake_audit,
    build_critique_summary,
    load_workspace_document,
    materialize_workspace_surfaces,
    summarize_workspace_document,
    validate_workspace_document,
)
from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap

from med_autogrant.hermes_runtime_parts.shared import *  # noqa: F401,F403


_editable_shared_bootstrap.ensure_editable_dependency_paths()


class HermesRuntimeSubstrate:
    """Hermes owns runtime orchestration while MedAutoGrant keeps domain semantics."""

    runtime_owner = "Hermes"

    def describe_topology(self) -> dict[str, Any]:
        return {
            "runtime_owner": self.runtime_owner,
            "default_formal_entry": "CLI",
            "supported_protocol_layer": "MCP",
            "internal_controller_surface": "controller",
            "compatibility_bridge": "Codex-default host-agent runtime",
            "domain_logic_modules": [
                "workspace",
                "stage_router",
                "route_report",
                "revision_executor",
                "artifact_bundle",
                "final_package",
                "hosted_contract_bundle",
            ],
        }

    def validate_workspace(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        result = validate_workspace_document(document)
        return result.to_dict(document)

    def summarize_workspace(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        return summarize_workspace_document(document)

    def grant_intake_audit(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        payload = {
            "ok": True,
            "command": "grant-intake-audit",
            "grant_run_id": document["grant_run_id"],
            "workspace_id": document["workspace_id"],
            "draft_id": None,
            "lifecycle_stage": document["lifecycle_stage"],
            "input_path": str(Path(input_path).expanduser().resolve()),
            "grant_intake_audit": build_grant_intake_audit(document),
        }
        _validate_contract_schema(
            payload,
            schema_file=GRANT_INTAKE_AUDIT_SCHEMA_FILE,
            context="grant_intake_audit",
            grant_run_id=document["grant_run_id"],
            workspace_id=document["workspace_id"],
            lifecycle_stage=document["lifecycle_stage"],
        )
        return payload

    def grant_evidence_grounding(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        payload = {
            "ok": True,
            "command": "grant-evidence-grounding",
            "grant_run_id": document["grant_run_id"],
            "workspace_id": document["workspace_id"],
            "draft_id": None,
            "lifecycle_stage": document["lifecycle_stage"],
            "input_path": str(Path(input_path).expanduser().resolve()),
            "grant_evidence_grounding": build_grant_evidence_grounding(document),
        }
        _validate_contract_schema(
            payload,
            schema_file=GRANT_EVIDENCE_GROUNDING_SCHEMA_FILE,
            context="grant_evidence_grounding",
            grant_run_id=document["grant_run_id"],
            workspace_id=document["workspace_id"],
            lifecycle_stage=document["lifecycle_stage"],
        )
        return payload

    def grant_quality_scorecard(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        payload = {
            "ok": True,
            "command": "grant-quality-scorecard",
            "grant_run_id": document["grant_run_id"],
            "workspace_id": document["workspace_id"],
            "draft_id": _read_active_draft_id(document),
            "lifecycle_stage": document["lifecycle_stage"],
            "input_path": str(Path(input_path).expanduser().resolve()),
            "grant_quality_scorecard": build_grant_quality_scorecard(document),
        }
        _validate_contract_schema(
            payload,
            schema_file=GRANT_QUALITY_SCORECARD_SCHEMA_FILE,
            context="grant_quality_scorecard",
            grant_run_id=document["grant_run_id"],
            workspace_id=document["workspace_id"],
            lifecycle_stage=document["lifecycle_stage"],
        )
        return payload

    def grant_quality_diff(
        self,
        *,
        input_path: str | Path,
        previous_input_path: str | Path,
    ) -> dict[str, Any]:
        current_document = self._load_workspace(input_path)
        previous_document = self._load_workspace(previous_input_path)
        payload = {
            "ok": True,
            "command": "grant-quality-diff",
            "grant_run_id": current_document["grant_run_id"],
            "workspace_id": current_document["workspace_id"],
            "draft_id": _read_active_draft_id(current_document),
            "lifecycle_stage": current_document["lifecycle_stage"],
            "input_path": str(Path(input_path).expanduser().resolve()),
            "previous_input_path": str(Path(previous_input_path).expanduser().resolve()),
            "grant_quality_diff": build_grant_quality_diff(
                current_document=current_document,
                previous_document=previous_document,
            ),
        }
        _validate_contract_schema(
            payload,
            schema_file=GRANT_QUALITY_DIFF_SCHEMA_FILE,
            context="grant_quality_diff",
            grant_run_id=current_document["grant_run_id"],
            workspace_id=current_document["workspace_id"],
            lifecycle_stage=current_document["lifecycle_stage"],
        )
        return payload

    def grant_quality_closure_dossier(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        payload = {
            "ok": True,
            "command": "grant-quality-closure-dossier",
            "grant_run_id": document["grant_run_id"],
            "workspace_id": document["workspace_id"],
            "draft_id": _read_active_draft_id(document),
            "lifecycle_stage": document["lifecycle_stage"],
            "input_path": str(Path(input_path).expanduser().resolve()),
            "grant_quality_closure_dossier": build_grant_quality_closure_dossier(document),
        }
        _validate_contract_schema(
            payload,
            schema_file=GRANT_QUALITY_CLOSURE_DOSSIER_SCHEMA_FILE,
            context="grant_quality_closure_dossier",
            grant_run_id=document["grant_run_id"],
            workspace_id=document["workspace_id"],
            lifecycle_stage=document["lifecycle_stage"],
        )
        return payload

    def discover_funding_opportunities(self, *, input_path: str | Path) -> dict[str, Any]:
        discovery_input = _load_json_object(input_path, context="funding landscape discovery input")
        _validate_schema_payload(
            discovery_input,
            schema_file=FUNDING_LANDSCAPE_DISCOVERY_INPUT_SCHEMA_FILE,
            context="funding_landscape_discovery_input",
        )
        discovery = discover_funding_landscape(
            discovery_input,
            cached_snapshot=_load_funding_landscape_cache_if_needed(discovery_input),
        )
        discovery_surface = {
            "surface_kind": "funding_landscape_discovery",
            "discovery_version": 1,
            "discovery_input_id": discovery_input["discovery_input_id"],
            **discovery,
        }
        _validate_schema_payload(
            discovery_surface,
            schema_file=FUNDING_LANDSCAPE_DISCOVERY_SCHEMA_FILE,
            context="funding_landscape_discovery",
        )
        return {
            "ok": True,
            "command": "discover-funding-opportunities",
            "discovery_input_id": discovery_input["discovery_input_id"],
            "input_path": str(Path(input_path).expanduser().resolve()),
            "funding_landscape_discovery": discovery_surface,
        }

    def refresh_funding_opportunities_cache(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path | None = None,
    ) -> dict[str, Any]:
        discovery_input = _load_json_object(input_path, context="funding landscape discovery input")
        _validate_schema_payload(
            discovery_input,
            schema_file=FUNDING_LANDSCAPE_DISCOVERY_INPUT_SCHEMA_FILE,
            context="funding_landscape_discovery_input",
        )
        resolved_output_path = (
            Path(output_path).expanduser().resolve()
            if output_path is not None
            else _default_funding_landscape_cache_path()
        )
        existing_snapshot = _load_existing_cache_snapshot(resolved_output_path)
        cache_snapshot = build_funding_landscape_cache(
            discovery_input,
            existing_snapshot=existing_snapshot,
        )
        diff_report = build_funding_landscape_diff_report(
            previous_snapshot=existing_snapshot,
            current_snapshot=cache_snapshot,
        )
        _validate_schema_payload(
            cache_snapshot,
            schema_file=FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE,
            context="funding_landscape_cache",
        )
        _validate_schema_payload(
            diff_report,
            schema_file=FUNDING_LANDSCAPE_DIFF_REPORT_SCHEMA_FILE,
            context="funding_landscape_diff_report",
        )
        _write_json_output(resolved_output_path, cache_snapshot, label="funding landscape cache")
        diff_report_path = _derive_funding_landscape_diff_report_path(resolved_output_path)
        _write_json_output(diff_report_path, diff_report, label="funding landscape diff report")
        return {
            "ok": True,
            "command": "refresh-funding-opportunities-cache",
            "discovery_input_id": cache_snapshot["discovery_input_id"],
            "cache_path": str(resolved_output_path),
            "diff_report_path": str(diff_report_path),
            "cache_snapshot": cache_snapshot,
            "diff_report": diff_report,
        }

    def select_project_profile(self, *, input_path: str | Path) -> dict[str, Any]:
        selection_input = _load_json_object(input_path, context="project profile selection input")
        _validate_schema_payload(
            selection_input,
            schema_file=PROJECT_PROFILE_SELECTION_INPUT_SCHEMA_FILE,
            context="project_profile_selection_input",
        )
        selection = select_project_profile(selection_input)
        _validate_schema_payload(
            selection,
            schema_file=PROJECT_PROFILE_SELECTION_SCHEMA_FILE,
            context="project_profile_selection",
        )
        return {
            "ok": True,
            "command": "select-project-profile",
            "selection_input_id": selection_input["selection_input_id"],
            "input_path": str(Path(input_path).expanduser().resolve()),
            "project_profile_selection": selection,
        }

    def initialize_intake_workspace(
        self,
        *,
        input_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        raw_input = _load_json_object(input_path, context="intake initialization input")
        if "funding_opportunity_pool" in raw_input:
            selection_input = raw_input
            _validate_schema_payload(
                selection_input,
                schema_file=PROJECT_PROFILE_SELECTION_INPUT_SCHEMA_FILE,
                context="project_profile_selection_input",
            )
        else:
            _validate_schema_payload(
                raw_input,
                schema_file=FUNDING_LANDSCAPE_DISCOVERY_INPUT_SCHEMA_FILE,
                context="funding_landscape_discovery_input",
            )
            discovered = discover_funding_landscape(
                raw_input,
                cached_snapshot=_load_funding_landscape_cache_if_needed(raw_input),
            )
            selection_input = _build_selection_input_from_discovery(
                discovery_input=raw_input,
                funding_opportunity_pool=discovered["funding_opportunity_pool"],
            )

        workspace, selection = build_initialized_intake_workspace(selection_input)
        validation = validate_workspace_document(workspace)
        if not validation.ok:
            first_issue = validation.errors[0]
            raise WorkspaceStateError(
                f"{first_issue.path}: {first_issue.message}",
                errors=validation.errors,
                grant_run_id=workspace.get("grant_run_id"),
                workspace_id=workspace.get("workspace_id"),
                lifecycle_stage=workspace.get("lifecycle_stage"),
            )

        resolved_output_path = Path(output_path).expanduser().resolve()
        _guard_workspace_output_identity(
            resolved_output_path,
            workspace_document=workspace,
            draft_id=None,
        )
        _write_revised_workspace_output(resolved_output_path, workspace)
        return {
            "ok": True,
            "command": "initialize-intake-workspace",
            "selection_input_id": selection_input["selection_input_id"],
            "grant_run_id": workspace["grant_run_id"],
            "workspace_id": workspace["workspace_id"],
            "draft_id": None,
            "lifecycle_stage": workspace["lifecycle_stage"],
            "output_path": str(resolved_output_path),
            "project_profile_selection": selection,
            "initialized_workspace": workspace,
        }

    def next_step(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        return determine_next_step(document)

    def critique_summary(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        payload = build_critique_summary(document)
        payload["recommended_next_stage"] = determine_next_step(document)["recommended_stage"]
        return payload

    def stage_route_report(self, *, input_path: str | Path) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        return build_stage_route_report(document)

    def run_local(
        self,
        *,
        input_path: str | Path,
        journal_path: str | Path | None = None,
        trigger: str = "runtime-run",
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        document = self._load_workspace(resolved_input_path)
        validation = validate_workspace_document(document)
        resolved_journal_path = _resolve_journal_path(document=document, journal_path=journal_path)
        journal = _load_or_initialize_journal(
            journal_path=resolved_journal_path,
            document=document,
            input_path=resolved_input_path,
        )

        if validation.ok:
            route_report = build_stage_route_report(document)
            stop_reason = derive_stop_reason(route_report)
            stage_action_envelope = derive_stage_action_envelope(
                route_report=route_report,
                stop_reason=stop_reason,
                journal_path=resolved_journal_path,
            )
            draft_id = route_report["verification_checkpoint"]["identity"]["draft_id"]
            lifecycle_stage = route_report["lifecycle_stage"]
        else:
            route_report = build_validation_failed_route_report(document=document, validation=validation)
            next_step = route_report["route"]["next_step"]
            stop_reason = {
                "code": "validation_failed",
                "reason": next_step["reason"],
                "current_stage": next_step["current_stage"],
                "recommended_next_stage": next_step["recommended_stage"],
                "checkpoint_status": route_report["checkpoint_status"],
                "requires_human_confirmation": False,
                "forced_rollback_stage": None,
                "forced_rollback_reason": None,
            }
            stage_action_envelope = None
            draft_id = None
            lifecycle_stage = document.get("lifecycle_stage")

        attempt_index = HermesGrantRunLedger().record_attempt(
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            trigger=trigger,
            journal_path=resolved_journal_path,
            lifecycle_stage=lifecycle_stage,
            stop_reason=stop_reason,
            stage_action_envelope=stage_action_envelope,
            route_report=route_report,
        )
        journal = _append_attempt(
            journal=journal,
            attempt_index=attempt_index,
            trigger=trigger,
            lifecycle_stage=lifecycle_stage,
            route_report=route_report,
            stop_reason=stop_reason,
            stage_action_envelope=stage_action_envelope,
        )
        _write_journal(resolved_journal_path, journal)

        payload = {
            "ok": validation.ok,
            "command": trigger,
            "grant_run_id": document.get("grant_run_id"),
            "workspace_id": document.get("workspace_id"),
            "draft_id": draft_id,
            "lifecycle_stage": lifecycle_stage,
            "input_path": str(resolved_input_path),
            "journal_path": str(resolved_journal_path),
            "attempt_index": journal["attempts"][-1]["attempt_index"],
            "stop_reason": stop_reason,
            "stage_action_envelope": stage_action_envelope,
            "route_report": route_report,
            "resume": {
                "command": "runtime-resume",
                "journal_path": str(resolved_journal_path),
            },
        }
        if not validation.ok:
            payload["error"] = f"validation_failed: {validation.errors[0].path}: {validation.errors[0].message}"
            payload["errors"] = validation.to_dict(document)["errors"]
        return payload

    def resume_local(self, *, journal_path: str | Path) -> dict[str, Any]:
        resolved_journal_path = Path(journal_path).expanduser().resolve()
        journal = _read_journal(resolved_journal_path)
        input_path = journal.get("input_path")
        if not isinstance(input_path, str) or not input_path:
            raise LocalRuntimeStateError(f"journal 缺少 input_path: {resolved_journal_path}")
        return self.run_local(
            input_path=input_path,
            journal_path=resolved_journal_path,
            trigger="runtime-resume",
        )

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

    def execute_critique_revision_loop(
        self,
        *,
        input_path: str | Path,
        output_dir: str | Path,
        max_rounds: int = 3,
        executor_kind: str | None = None,
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
    ) -> dict[str, Any]:
        resolved_input_path = Path(input_path).expanduser().resolve()
        starting_workspace = self._load_workspace(resolved_input_path)
        resolved_output_dir = Path(output_dir).expanduser().resolve()
        resolved_output_dir.mkdir(parents=True, exist_ok=True)

        loop_state = {"cycle": 0}

        def _materialize_loop_input(workspace: dict[str, Any]) -> Path:
            input_path_for_cycle = resolved_output_dir / f"cycle-{loop_state['cycle'] + 1:02d}-input-workspace.json"
            _write_revised_workspace_output(input_path_for_cycle, workspace)
            return input_path_for_cycle

        def _extract_draft_id(workspace: dict[str, Any]) -> str | None:
            selection = workspace.get("current_selection") or {}
            draft_id = selection.get("active_draft_id")
            if isinstance(draft_id, str) and draft_id.strip():
                return draft_id
            return None

        def _write_cycle_workspace(path: Path, workspace: dict[str, Any]) -> None:
            _guard_workspace_output_identity(
                path,
                workspace_document=workspace,
                draft_id=_extract_draft_id(workspace),
            )
            _write_revised_workspace_output(path, workspace)

        def _stage_runner(stage_name: str):
            def _runner(workspace: dict[str, Any]) -> dict[str, Any]:
                loop_state["cycle"] += 1
                current_input_path = _materialize_loop_input(workspace)
                if stage_name == "direction_screening":
                    execution_document = build_direction_screening_execution_document(
                        document=workspace,
                        input_path=current_input_path,
                    )
                    next_workspace = execution_document["direction_screening_workspace"]
                elif stage_name == "question_refinement":
                    execution_document = build_question_refinement_execution_document(
                        document=workspace,
                        input_path=current_input_path,
                    )
                    next_workspace = execution_document["question_refinement_workspace"]
                elif stage_name == "argument_building":
                    execution_document = build_argument_building_execution_document(
                        document=workspace,
                        input_path=current_input_path,
                    )
                    next_workspace = execution_document["argument_building_workspace"]
                elif stage_name == "fit_alignment":
                    execution_document = build_fit_alignment_execution_document(
                        document=workspace,
                        input_path=current_input_path,
                    )
                    next_workspace = execution_document["fit_alignment_workspace"]
                elif stage_name == "outline":
                    execution_document = build_outline_execution_document(
                        document=workspace,
                        input_path=current_input_path,
                    )
                    next_workspace = execution_document["outline_workspace"]
                elif stage_name == "drafting":
                    execution_document = build_drafting_execution_document(
                        document=workspace,
                        input_path=current_input_path,
                    )
                    next_workspace = execution_document["drafting_workspace"]
                elif stage_name == "critique":
                    execution_document = build_critique_execution_document(
                        document=workspace,
                        input_path=current_input_path,
                        executor_kind=executor_kind,
                    )
                    next_workspace = execution_document["critique_workspace"]
                elif stage_name == "revision":
                    execution_document = build_revision_execution_document(document=workspace)
                    next_workspace = execution_document["revised_workspace"]
                elif stage_name == "frozen":
                    execution_document = build_freeze_execution_document(document=workspace)
                    next_workspace = execution_document["frozen_workspace"]
                else:
                    raise WorkspaceStateError(f"execute-authoring-mainline-loop 不支持 stage runner: {stage_name}")

                output_path_for_cycle = resolved_output_dir / f"cycle-{loop_state['cycle']:02d}-{stage_name}-workspace.json"
                _write_cycle_workspace(output_path_for_cycle, next_workspace)
                return {
                    "workspace": next_workspace,
                }

            return _runner

        def _quality_aware_route_resolver(workspace: dict[str, Any]) -> dict[str, Any]:
            route = determine_next_step(workspace)
            quality_scorecard = build_grant_quality_scorecard(workspace)
            return _apply_quality_gate_to_route(route=route, quality_scorecard=quality_scorecard)

        loop = run_authoring_mainline_controller(
            current_workspace=starting_workspace,
            max_cycles=max_cycles,
            route_resolver=_quality_aware_route_resolver,
            stage_runners={
                "direction_screening": _stage_runner("direction_screening"),
                "question_refinement": _stage_runner("question_refinement"),
                "argument_building": _stage_runner("argument_building"),
                "fit_alignment": _stage_runner("fit_alignment"),
                "outline": _stage_runner("outline"),
                "drafting": _stage_runner("drafting"),
                "critique": _stage_runner("critique"),
                "revision": _stage_runner("revision"),
                "frozen": _stage_runner("frozen"),
            },
        )
        final_workspace = loop["final_workspace"]
        final_route = loop["final_route"]
        final_workspace_path = resolved_output_dir / "authoring-mainline-final-workspace.json"
        _write_cycle_workspace(final_workspace_path, final_workspace)
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
        _validate_schema_payload(
            mainline_loop_report,
            schema_file=AUTHORING_MAINLINE_LOOP_REPORT_SCHEMA_FILE,
            context="authoring_mainline_loop_report",
        )
        report_path = resolved_output_dir / "authoring-mainline-loop-report.json"
        _write_json_output(report_path, mainline_loop_report, label="authoring mainline loop report")
        return {
            "ok": True,
            "command": "execute-authoring-mainline-loop",
            "grant_run_id": final_workspace["grant_run_id"],
            "workspace_id": final_workspace["workspace_id"],
            "draft_id": _extract_draft_id(final_workspace),
            "lifecycle_stage": final_workspace["lifecycle_stage"],
            "output_dir": str(resolved_output_dir),
            "mainline_loop_report_path": str(report_path),
            "final_workspace_path": str(final_workspace_path),
            "mainline_loop_report": mainline_loop_report,
            "final_workspace": final_workspace,
        }

    def execute_grant_autonomy_controller(
        self,
        *,
        input_path: str | Path,
        output_dir: str | Path,
        executor_kind: str | None = None,
    ) -> dict[str, Any]:
        request = _load_json_object(input_path, context="grant autonomy controller input")
        _validate_schema_payload(
            request,
            schema_file=GRANT_AUTONOMY_CONTROLLER_INPUT_SCHEMA_FILE,
            context="grant_autonomy_controller_input",
        )
        resolved_output_dir = Path(output_dir).expanduser().resolve()
        resolved_output_dir.mkdir(parents=True, exist_ok=True)

        def _discoverer(discovery_input: dict[str, Any]) -> dict[str, Any]:
            discovery = discover_funding_landscape(
                discovery_input,
                cached_snapshot=_load_funding_landscape_cache_if_needed(discovery_input),
            )
            selection_input = _build_selection_input_from_discovery(
                discovery_input=discovery_input,
                funding_opportunity_pool=discovery["funding_opportunity_pool"],
            )
            return {
                "selection_input": selection_input,
                "funding_landscape_discovery": discovery,
            }

        def _selector(selection_input: dict[str, Any]) -> dict[str, Any]:
            return select_project_profile(selection_input)

        def _initializer(selection_input: dict[str, Any], _selection: dict[str, Any]) -> dict[str, Any]:
            workspace, selection = build_initialized_intake_workspace(selection_input)
            validation = validate_workspace_document(workspace)
            if not validation.ok:
                first_issue = validation.errors[0]
                raise WorkspaceStateError(
                    f"{first_issue.path}: {first_issue.message}",
                    errors=validation.errors,
                    grant_run_id=workspace.get("grant_run_id"),
                    workspace_id=workspace.get("workspace_id"),
                    lifecycle_stage=workspace.get("lifecycle_stage"),
                )
            return {
                "workspace": workspace,
                "project_profile_selection": selection,
            }

        def _mainline_runner(payload: dict[str, Any]) -> dict[str, Any]:
            workspace = payload.get("workspace")
            if not isinstance(workspace, dict):
                raise WorkspaceStateError("grant autonomy mainline runner 缺少 workspace。")
            cycle = payload.get("cycle")
            cycle_index = cycle if isinstance(cycle, int) and cycle > 0 else 0
            cycle_output_dir = resolved_output_dir / f"controller-cycle-{cycle_index:02d}-mainline"
            cycle_input_path = cycle_output_dir / "mainline-input-workspace.json"
            _write_revised_workspace_output(cycle_input_path, workspace)
            mainline_payload = self.execute_authoring_mainline_loop(
                input_path=cycle_input_path,
                output_dir=cycle_output_dir,
                max_cycles=1,
                executor_kind=executor_kind,
            )
            return {
                "workspace": mainline_payload["final_workspace"],
                "final_workspace": mainline_payload["final_workspace"],
                "mainline_loop_report": mainline_payload["mainline_loop_report"],
            }

        report = run_grant_autonomy_controller(
            request=request,
            selector=_selector,
            initializer=_initializer,
            mainline_runner=_mainline_runner,
            quality_evaluator=_build_autonomy_quality_evaluator_output,
            discoverer=_discoverer,
        )
        _validate_schema_payload(
            report,
            schema_file=GRANT_AUTONOMY_CONTROLLER_REPORT_SCHEMA_FILE,
            context="grant_autonomy_controller_report",
        )

        report_path = resolved_output_dir / "grant-autonomy-controller-report.json"
        _write_json_output(report_path, report, label="grant autonomy controller report")

        final_workspace = report.get("final_workspace") if isinstance(report.get("final_workspace"), dict) else {}
        final_workspace_path: Path | None = None
        if _looks_like_workspace(final_workspace):
            final_workspace_path = resolved_output_dir / "grant-autonomy-final-workspace.json"
            _guard_workspace_output_identity(
                final_workspace_path,
                workspace_document=final_workspace,
                draft_id=_read_active_draft_id(final_workspace),
            )
            _write_revised_workspace_output(final_workspace_path, final_workspace)

        return {
            "ok": True,
            "command": "execute-grant-autonomy-controller",
            "grant_run_id": final_workspace.get("grant_run_id") if final_workspace else None,
            "workspace_id": final_workspace.get("workspace_id") if final_workspace else None,
            "draft_id": _read_active_draft_id(final_workspace) if final_workspace else None,
            "lifecycle_stage": final_workspace.get("lifecycle_stage") if final_workspace else None,
            "controller_status": report["controller_status"],
            "termination_reason": report["termination_reason"],
            "output_dir": str(resolved_output_dir),
            "grant_autonomy_controller_report_path": str(report_path),
            "final_workspace_path": str(final_workspace_path) if final_workspace_path else None,
            "grant_autonomy_controller_report": report,
            "final_workspace": final_workspace,
        }

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

    def build_final_package(
        self,
        *,
        input_path: str | Path,
        artifact_bundle_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        context = _require_workspace_context(document)
        active_draft = context.active_draft
        artifact_bundle = _read_artifact_bundle(
            artifact_bundle_path,
            grant_run_id=document["grant_run_id"],
            workspace_id=document["workspace_id"],
            draft_id=active_draft["draft_id"],
            lifecycle_stage=document.get("lifecycle_stage"),
        )
        final_package = build_final_package_document(
            document=document,
            artifact_bundle=artifact_bundle,
        )
        resolved_output_path = Path(output_path).expanduser().resolve()
        _guard_final_package_output_identity(
            resolved_output_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )
        _write_final_package_output(resolved_output_path, final_package)
        return {
            "ok": True,
            "command": "build-final-package",
            "grant_run_id": final_package["grant_run_id"],
            "workspace_id": final_package["workspace_id"],
            "draft_id": final_package["draft_id"],
            "lifecycle_stage": final_package["lifecycle_stage"],
            "output_path": str(resolved_output_path),
            "final_package": final_package,
        }

    def build_hosted_contract_bundle(
        self,
        *,
        final_package_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        final_package = _read_final_package(final_package_path)
        current_program_contract = _read_current_program_contract()
        program_id = _read_program_id()
        hosted_contract_bundle = build_hosted_contract_bundle_document(
            final_package=final_package,
            program_id=program_id,
            runtime_substrate_contract=_build_runtime_substrate_contract(
                current_program_contract=current_program_contract,
            ),
            runtime_state_contract=_build_runtime_state_contract(),
            operator_contract=_build_operator_contract(),
            domain_entry_contract=build_domain_entry_contract(),
            schema_contract=_build_schema_contract(),
            authoring_contract=_build_hosted_authoring_contract(),
        )
        _validate_hosted_contract_bundle(
            hosted_contract_bundle,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )
        resolved_output_path = Path(output_path).expanduser().resolve()
        _guard_hosted_contract_output_identity(
            resolved_output_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            program_id=program_id,
        )
        _write_hosted_contract_bundle_output(resolved_output_path, hosted_contract_bundle)
        return {
            "ok": True,
            "command": "build-hosted-contract-bundle",
            "grant_run_id": final_package["grant_run_id"],
            "workspace_id": final_package["workspace_id"],
            "draft_id": final_package["draft_id"],
            "output_path": str(resolved_output_path),
            "hosted_contract_bundle": hosted_contract_bundle,
        }

    def build_submission_ready_package(
        self,
        *,
        input_path: str | Path,
        output_dir: str | Path,
    ) -> dict[str, Any]:
        document = self._load_workspace(input_path)
        artifact_bundle = build_artifact_bundle_document(document=document)
        final_package = build_final_package_document(
            document=document,
            artifact_bundle=artifact_bundle,
        )
        current_program_contract = _read_current_program_contract()
        program_id = _read_program_id()
        hosted_contract_bundle = build_hosted_contract_bundle_document(
            final_package=final_package,
            program_id=program_id,
            runtime_substrate_contract=_build_runtime_substrate_contract(
                current_program_contract=current_program_contract,
            ),
            runtime_state_contract=_build_runtime_state_contract(),
            operator_contract=_build_operator_contract(),
            domain_entry_contract=build_domain_entry_contract(),
            schema_contract=_build_schema_contract(),
            authoring_contract=_build_hosted_authoring_contract(),
        )
        _validate_hosted_contract_bundle(
            hosted_contract_bundle,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )
        submission_ready_package = build_submission_ready_package_document(
            document=document,
            artifact_bundle=artifact_bundle,
            final_package=final_package,
            hosted_contract_bundle=hosted_contract_bundle,
            program_id=program_id,
        )
        if not submission_ready_package["submission_ready"]:
            issue_ids = [
                item["issue_id"]
                for item in submission_ready_package["blocking_issues"]
                if isinstance(item, dict) and isinstance(item.get("issue_id"), str)
            ]
            raise WorkspaceStateError(
                f"submission ready package blocked: {', '.join(issue_ids)}",
                errors=[],
                grant_run_id=final_package["grant_run_id"],
                workspace_id=final_package["workspace_id"],
                lifecycle_stage=final_package["lifecycle_stage"],
            )
        _validate_contract_schema(
            submission_ready_package,
            schema_file=SUBMISSION_READY_PACKAGE_SCHEMA_FILE,
            context="submission_ready_package",
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )

        resolved_output_dir = Path(output_dir).expanduser().resolve()
        artifact_bundle_path = resolved_output_dir / "artifact-bundle.json"
        final_package_path = resolved_output_dir / "final-package.json"
        hosted_contract_bundle_path = resolved_output_dir / "hosted-contract-bundle.json"
        submission_ready_package_path = resolved_output_dir / "submission-ready-package.json"

        _guard_artifact_bundle_output_identity(
            artifact_bundle_path,
            grant_run_id=artifact_bundle["grant_run_id"],
            workspace_id=artifact_bundle["workspace_id"],
            draft_id=artifact_bundle["draft_id"],
            lifecycle_stage=artifact_bundle["lifecycle_stage"],
        )
        _guard_final_package_output_identity(
            final_package_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            lifecycle_stage=final_package["lifecycle_stage"],
        )
        _guard_hosted_contract_output_identity(
            hosted_contract_bundle_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            program_id=program_id,
        )
        _guard_submission_ready_package_output_identity(
            submission_ready_package_path,
            grant_run_id=final_package["grant_run_id"],
            workspace_id=final_package["workspace_id"],
            draft_id=final_package["draft_id"],
            program_id=program_id,
        )

        _write_artifact_bundle_output(artifact_bundle_path, artifact_bundle)
        _write_final_package_output(final_package_path, final_package)
        _write_hosted_contract_bundle_output(hosted_contract_bundle_path, hosted_contract_bundle)
        _write_submission_ready_package_output(submission_ready_package_path, submission_ready_package)
        return {
            "ok": True,
            "command": "build-submission-ready-package",
            "grant_run_id": final_package["grant_run_id"],
            "workspace_id": final_package["workspace_id"],
            "draft_id": final_package["draft_id"],
            "lifecycle_stage": final_package["lifecycle_stage"],
            "output_dir": str(resolved_output_dir),
            "output_paths": {
                "artifact_bundle": str(artifact_bundle_path),
                "final_package": str(final_package_path),
                "hosted_contract_bundle": str(hosted_contract_bundle_path),
                "submission_ready_package": str(submission_ready_package_path),
            },
            "submission_ready_package": submission_ready_package,
        }

    def _load_workspace(self, input_path: str | Path) -> dict[str, Any]:
        return load_workspace_document(Path(input_path).expanduser().resolve())

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


from med_autogrant.hermes_runtime_parts.contracts import (
    build_author_side_route_contract as _build_author_side_route_contract,
    build_executor_routing_contract as _build_executor_routing_contract,
    build_hosted_authoring_contract as _build_hosted_authoring_contract,
    build_operator_contract as _build_operator_contract,
    build_service_safe_domain_surface as _build_service_safe_domain_surface,
    build_stage_route_contract as _build_stage_route_contract,
    build_runtime_state_contract as _build_runtime_state_contract,
    build_runtime_substrate_contract as _build_runtime_substrate_contract,
    build_schema_contract as _build_schema_contract,
    parse_git_worktree_list_porcelain as _parse_git_worktree_list_porcelain,
    read_current_program_contract as _read_current_program_contract,
    read_git_worktree_list as _read_git_worktree_list,
    read_program_id as _read_program_id,
    require_known_route_id as _require_known_route_id,
    require_nonempty_route_id as _require_nonempty_route_id,
    require_nonempty_string as _require_nonempty_string,
    resolve_control_plane_current_program_path as _resolve_control_plane_current_program_path,
    select_control_plane_current_program_path as _select_control_plane_current_program_path,
    validate_contract_schema as _validate_contract_schema,
    validate_executor_routing_contract as _validate_executor_routing_contract,
    validate_hosted_contract_bundle as _validate_hosted_contract_bundle,
    validate_schema_payload as _validate_schema_payload,
)
from med_autogrant.hermes_runtime_parts.io import (
    _append_attempt,
    _build_selection_input_from_discovery,
    _default_funding_landscape_cache_path,
    _derive_funding_landscape_diff_report_path,
    _guard_artifact_bundle_output_identity,
    _guard_critique_output_identity,
    _guard_final_package_output_identity,
    _guard_hosted_contract_output_identity,
    _guard_revision_output_identity,
    _guard_submission_ready_package_output_identity,
    _guard_workspace_output_identity,
    _load_existing_cache_snapshot,
    _load_funding_landscape_cache_if_needed,
    _load_json_object,
    _load_or_initialize_journal,
    _read_active_draft_id,
    _read_artifact_bundle,
    _read_final_package,
    _read_journal,
    _write_artifact_bundle_output,
    _write_final_package_output,
    _write_hosted_contract_bundle_output,
    _write_json_output,
    _write_journal,
    _write_revised_workspace_output,
    _write_submission_ready_package_output,
)
from med_autogrant.hermes_runtime_parts.runtime_ops import (
    _apply_quality_gate_to_route,
    _build_autonomy_quality_evaluator_output,
    _looks_like_workspace,
    _resolve_journal_path,
    build_validation_failed_route_report,
    derive_stage_action_envelope,
    derive_stop_reason,
)
