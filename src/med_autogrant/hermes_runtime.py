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

_editable_shared_bootstrap.ensure_editable_dependency_paths()


JOURNAL_VERSION = 1
CURRENT_PROGRAM_RELATIVE_PATH = CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH
EXECUTOR_ROUTING_CONTRACT_VERSION = 1
EXECUTOR_ROUTING_CONTRACT_SCHEMA_FILE = "executor-routing-contract.schema.json"
PRODUCT_ENTRY_SCHEMA_FILE = "product-entry.schema.json"
GRANT_PROGRESS_SCHEMA_FILE = "grant-progress.schema.json"
GRANT_COCKPIT_SCHEMA_FILE = "grant-cockpit.schema.json"
GRANT_DIRECT_ENTRY_SCHEMA_FILE = "grant-direct-entry.schema.json"
GRANT_USER_LOOP_SCHEMA_FILE = "grant-user-loop.schema.json"
PRODUCT_ENTRY_MANIFEST_SCHEMA_FILE = "product-entry-manifest.schema.json"
PRODUCT_FRONTDESK_SCHEMA_FILE = "product-frontdesk.schema.json"
GRANT_INTAKE_AUDIT_SCHEMA_FILE = "grant-intake-audit.schema.json"
GRANT_EVIDENCE_GROUNDING_SCHEMA_FILE = "grant-evidence-grounding.schema.json"
GRANT_QUALITY_SCORECARD_SCHEMA_FILE = "grant-quality-scorecard.schema.json"
GRANT_QUALITY_DIFF_SCHEMA_FILE = "grant-quality-diff.schema.json"
GRANT_QUALITY_CLOSURE_DOSSIER_SCHEMA_FILE = "grant-quality-closure-dossier.schema.json"
GRANT_AUTONOMY_CONTROLLER_INPUT_SCHEMA_FILE = "grant-autonomy-controller-input.schema.json"
GRANT_AUTONOMY_CONTROLLER_REPORT_SCHEMA_FILE = "grant-autonomy-controller-report.schema.json"
HOSTED_CONTRACT_BUNDLE_SCHEMA_FILE = "hosted-contract-bundle.schema.json"
SUBMISSION_READY_PACKAGE_SCHEMA_FILE = "submission-ready-package.schema.json"
PROJECT_PROFILE_SELECTION_INPUT_SCHEMA_FILE = "project-profile-selection-input.schema.json"
PROJECT_PROFILE_SELECTION_SCHEMA_FILE = "project-profile-selection.schema.json"
CRITIQUE_LOOP_REPORT_SCHEMA_FILE = "critique-loop-report.schema.json"
FUNDING_LANDSCAPE_DISCOVERY_INPUT_SCHEMA_FILE = "funding-landscape-discovery-input.schema.json"
FUNDING_LANDSCAPE_DISCOVERY_SCHEMA_FILE = "funding-landscape-discovery.schema.json"
FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE = "funding-landscape-cache.schema.json"
FUNDING_LANDSCAPE_DIFF_REPORT_SCHEMA_FILE = "funding-landscape-diff-report.schema.json"
AUTHORING_MAINLINE_LOOP_REPORT_SCHEMA_FILE = "authoring-mainline-loop-report.schema.json"
SCHEMA_INDEX_RELATIVE_PATH = "schemas/v1/schema-index.json"
PRODUCT_ENTRY_KIND = "med_auto_grant_product_entry"
HOSTED_CONTRACT_SCHEMA_FILES = (
    "service-safe-domain-surface.schema.json",
    "executor-routing-contract.schema.json",
    "product-entry.schema.json",
    "grant-intake-audit.schema.json",
    "grant-evidence-grounding.schema.json",
    "grant-quality-scorecard.schema.json",
    "grant-quality-closure-dossier.schema.json",
    "grant-quality-diff.schema.json",
    "grant-autonomy-controller-input.schema.json",
    "grant-autonomy-controller-report.schema.json",
    "funding-landscape-discovery-input.schema.json",
    "funding-landscape-discovery.schema.json",
    "funding-landscape-cache.schema.json",
    "funding-landscape-diff-report.schema.json",
    "project-profile-selection-input.schema.json",
    "project-profile-selection.schema.json",
    "critique-loop-report.schema.json",
    "authoring-mainline-loop-report.schema.json",
    "hosted-contract-bundle.schema.json",
    "submission-ready-package.schema.json",
)
AUTHOR_SIDE_ROUTE_IDS = (
    "direction_screening",
    "question_refinement",
    "argument_building",
    "fit_alignment",
    "outline",
    "drafting",
    "critique",
    "revision",
    "frozen",
    "artifact_bundle",
    "final_package",
    "hosted_contract_bundle",
)
EXECUTOR_ROUTE_OWNER = "med-autogrant"


class LocalRuntimeStateError(WorkspaceError):
    """Local runtime journal/state mismatch。"""


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


def build_validation_failed_route_report(
    *,
    document: dict[str, Any],
    validation: Any,
) -> dict[str, Any]:
    lifecycle_stage = document.get("lifecycle_stage")
    validation_payload = validation.to_dict(document)
    reason = validation.errors[0].message if validation.errors else "workspace validation failed"
    checkpoint_status = None
    return {
        "ok": False,
        "grant_run_id": document.get("grant_run_id"),
        "workspace_id": document.get("workspace_id"),
        "lifecycle_stage": lifecycle_stage,
        "route": {
            "validate_workspace": validation_payload,
            "summarize_workspace": None,
            "next_step": {
                "grant_run_id": document.get("grant_run_id"),
                "workspace_id": document.get("workspace_id"),
                "presubmission_frozen": bool(document.get("gates", {}).get("presubmission_frozen")),
                "current_stage": lifecycle_stage,
                "recommended_stage": lifecycle_stage,
                "reason": reason,
                "actions": [],
                "requires_human_confirmation": False,
            },
            "critique_summary": None,
        },
        "checkpoint_status": checkpoint_status,
        "verification_checkpoint": {
            "checkpoint_status": checkpoint_status,
            "validation_ok": False,
            "identity": {
                "grant_run_id": document.get("grant_run_id"),
                "workspace_id": document.get("workspace_id"),
                "draft_id": None,
                "active_revision_plan_id": None,
                "reviewed_revision_plan_id": None,
            },
            "route_alignment": {
                "lifecycle_stage": lifecycle_stage,
                "recommended_next_stage": lifecycle_stage,
                "forced_rollback_stage": None,
                "forced_rollback_reason": None,
                "presubmission_frozen": bool(document.get("gates", {}).get("presubmission_frozen")),
            },
            "review_checkpoint": {
                "critique_id": None,
                "reviewed_revision_evidence": None,
                "blocking_issue_count": None,
            },
        },
    }


def derive_stop_reason(route_report: dict[str, Any]) -> dict[str, Any]:
    next_step = route_report["route"]["next_step"]
    checkpoint = route_report["verification_checkpoint"]
    checkpoint_status = checkpoint["checkpoint_status"]
    route_alignment = checkpoint["route_alignment"]
    forced_rollback_stage = route_alignment.get("forced_rollback_stage")
    forced_rollback_reason = route_alignment.get("forced_rollback_reason")
    requires_human_confirmation = bool(next_step.get("requires_human_confirmation"))

    if checkpoint_status == "submission_frozen":
        code = "presubmission_frozen"
    elif forced_rollback_stage or checkpoint_status == "rollback_required":
        code = "rollback_required"
    elif checkpoint_status == "freeze_ready":
        code = "freeze_ready"
    elif requires_human_confirmation:
        code = "human_confirmation_required"
    else:
        code = "stage_action_required"

    return {
        "code": code,
        "reason": next_step["reason"],
        "current_stage": next_step["current_stage"],
        "recommended_next_stage": next_step["recommended_stage"],
        "checkpoint_status": checkpoint_status,
        "requires_human_confirmation": requires_human_confirmation,
        "forced_rollback_stage": forced_rollback_stage,
        "forced_rollback_reason": forced_rollback_reason,
    }


def derive_stage_action_envelope(
    *,
    route_report: dict[str, Any],
    stop_reason: dict[str, Any],
    journal_path: Path,
) -> dict[str, Any] | None:
    if stop_reason.get("code") != "stage_action_required":
        return None

    summary = route_report["route"]["summarize_workspace"]
    next_step = route_report["route"]["next_step"]
    checkpoint = route_report["verification_checkpoint"]
    selection = summary.get("current_selection") or {}
    actions = next_step.get("actions") or []
    executor_routing_contract = _build_executor_routing_contract(
        current_stage=next_step["current_stage"],
        recommended_next_stage=next_step["recommended_stage"],
    )
    _validate_executor_routing_contract(
        executor_routing_contract,
        current_stage=next_step["current_stage"],
        recommended_next_stage=next_step["recommended_stage"],
        include_route_catalog=False,
        grant_run_id=route_report["grant_run_id"],
        workspace_id=route_report["workspace_id"],
        lifecycle_stage=next_step["current_stage"],
    )

    return {
        "envelope_version": 1,
        "status": "action_required",
        "grant_run_id": route_report["grant_run_id"],
        "workspace_id": route_report["workspace_id"],
        "draft_id": checkpoint["identity"]["draft_id"],
        "current_stage": next_step["current_stage"],
        "recommended_next_stage": next_step["recommended_stage"],
        "checkpoint_status": checkpoint["checkpoint_status"],
        "requires_human_confirmation": bool(next_step.get("requires_human_confirmation")),
        "selection": {
            "selected_direction_id": selection.get("selected_direction_id"),
            "selected_question_id": selection.get("selected_question_id"),
            "active_fit_mapping_id": selection.get("active_fit_mapping_id"),
            "active_draft_id": selection.get("active_draft_id"),
            "active_revision_plan_id": selection.get("active_revision_plan_id"),
        },
        "action_items": [
            {
                "index": index,
                "instruction": instruction,
            }
            for index, instruction in enumerate(actions, start=1)
        ],
        "route_reason": next_step["reason"],
        "executor_routing_contract": executor_routing_contract,
        "resume_decision": {
            "command": "runtime-resume",
            "journal_path": str(journal_path),
            "append_attempt": True,
            "reuse_grant_run_id": True,
        },
    }


def _resolve_journal_path(*, document: dict[str, Any], journal_path: str | Path | None) -> Path:
    if journal_path is not None:
        return Path(journal_path).expanduser().resolve()
    grant_run_id = document.get("grant_run_id")
    if not isinstance(grant_run_id, str) or not grant_run_id:
        raise LocalRuntimeStateError("workspace 缺少 grant_run_id，无法推导默认 journal 路径。")
    return (_default_journal_root() / f"{grant_run_id}.json").resolve()


def _default_journal_root() -> Path:
    return resolve_runtime_state_root() / "sessions"


def _apply_quality_gate_to_route(
    *,
    route: dict[str, Any],
    quality_scorecard: dict[str, Any] | None,
) -> dict[str, Any]:
    resolved_route = dict(route)
    quality_payload = quality_scorecard if isinstance(quality_scorecard, dict) else {}
    quality_gate = quality_payload.get("loop_gate")
    if not isinstance(quality_gate, dict):
        return resolved_route

    resolved_route["quality_gate"] = dict(quality_gate)
    gate_action = str(quality_gate.get("action") or "").strip()
    gate_reason = str(quality_gate.get("reason") or "").strip()
    gate_stage = str(quality_gate.get("recommended_stage") or "").strip()
    route_stage = str(resolved_route.get("recommended_stage") or "").strip()

    if gate_action == "rollback_required" and gate_stage and gate_stage != route_stage:
        resolved_route["recommended_stage"] = gate_stage
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} 质量 gate 要求回退：{gate_reason}".strip()
        resolved_route["actions"] = _build_forced_rollback_actions(gate_stage)
        resolved_route["requires_human_confirmation"] = gate_stage in {
            "direction_screening",
            "question_refinement",
        }
        return resolved_route

    if gate_action == "continue" and route_stage in {"frozen", "ready_for_submission"} and gate_stage:
        resolved_route["recommended_stage"] = gate_stage
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} 质量 gate 暂不允许停止：{gate_reason}".strip()
        return resolved_route

    if gate_action == "ready_for_submission" and gate_reason:
        resolved_route["reason"] = f"{resolved_route.get('reason') or ''} {gate_reason}".strip()
    return resolved_route


def _build_autonomy_quality_evaluator_output(workspace: dict[str, Any]) -> dict[str, Any]:
    scorecard = build_grant_quality_scorecard(workspace)
    overall_status = str(scorecard.get("overall_status") or "")
    quality_status = overall_status if overall_status in {
        "submission_grade_candidate",
        "near_submission_candidate",
    } else "not_ready"
    tracked_issues = scorecard.get("tracked_issues") if isinstance(scorecard.get("tracked_issues"), list) else []
    evidence_supply_queue = scorecard.get("evidence_supply_queue") if isinstance(scorecard.get("evidence_supply_queue"), list) else []
    unresolved_blockers = list(scorecard.get("unresolved_hard_issues") or [])
    unresolved_blockers.extend(
        str(issue.get("summary") or "")
        for issue in tracked_issues
        if isinstance(issue, dict)
        and issue.get("status") == "open"
        and issue.get("severity") == "hard"
    )
    dimensions = scorecard.get("dimensions") if isinstance(scorecard.get("dimensions"), list) else []
    evidence_gaps: list[str] = []
    for dimension in dimensions:
        if not isinstance(dimension, dict):
            continue
        for gap in dimension.get("evidence_gaps") or []:
            if isinstance(gap, str) and gap.strip():
                evidence_gaps.append(gap.strip())
    for item in evidence_supply_queue:
        if not isinstance(item, dict):
            continue
        gap_summary = str(item.get("gap_summary") or "").strip()
        supply_status = str(item.get("supply_status") or "").strip()
        if not gap_summary:
            continue
        if supply_status in {"blocked", "reselection_required"}:
            unresolved_blockers.append(gap_summary)
        else:
            evidence_gaps.append(gap_summary)

    return {
        "quality_status": quality_status,
        "blocker_report": scorecard,
        "unresolved_blockers": _dedupe_strings(unresolved_blockers),
        "evidence_gaps": _dedupe_strings(evidence_gaps),
        "evidence_supply_queue": evidence_supply_queue,
    }


def _dedupe_strings(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text or text in seen:
            continue
        seen.add(text)
        deduped.append(text)
    return deduped


def _looks_like_workspace(payload: dict[str, Any]) -> bool:
    return all(isinstance(payload.get(field), str) and payload[field] for field in (
        "grant_run_id",
        "workspace_id",
        "lifecycle_stage",
    ))


def _read_journal(journal_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(journal_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 journal 文件: {journal_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"journal JSON 解析失败: {journal_path}") from exc
    if not isinstance(payload, dict):
        raise WorkspaceFileError(f"journal 顶层必须是 JSON object: {journal_path}")
    return payload


def _read_active_draft_id(document: dict[str, Any]) -> str | None:
    selection = document.get("current_selection") or {}
    draft_id = selection.get("active_draft_id")
    return draft_id if isinstance(draft_id, str) and draft_id.strip() else None


def _load_or_initialize_journal(
    *,
    journal_path: Path,
    document: dict[str, Any],
    input_path: Path,
) -> dict[str, Any]:
    if not journal_path.exists():
        return {
            "journal_version": JOURNAL_VERSION,
            "grant_run_id": document.get("grant_run_id"),
            "workspace_id": document.get("workspace_id"),
            "input_path": str(input_path),
            "latest_stop_reason": None,
            "latest_stage_action_envelope": None,
            "latest_route_report": None,
            "attempts": [],
        }

    journal = _read_journal(journal_path)
    if journal.get("grant_run_id") != document.get("grant_run_id"):
        raise LocalRuntimeStateError(
            f"journal grant_run_id 不匹配: {journal_path} -> {journal.get('grant_run_id')} != {document.get('grant_run_id')}"
        )
    if journal.get("workspace_id") != document.get("workspace_id"):
        raise LocalRuntimeStateError(
            f"journal workspace_id 不匹配: {journal_path} -> {journal.get('workspace_id')} != {document.get('workspace_id')}"
        )
    if journal.get("input_path") != str(input_path):
        raise LocalRuntimeStateError(
            f"journal input_path 不匹配: {journal_path} -> {journal.get('input_path')} != {input_path}"
        )
    attempts = journal.get("attempts")
    if not isinstance(attempts, list):
        raise LocalRuntimeStateError(f"journal attempts 不是 list: {journal_path}")
    return journal


def _append_attempt(
    *,
    journal: dict[str, Any],
    attempt_index: int,
    trigger: str,
    lifecycle_stage: str | None,
    route_report: dict[str, Any],
    stop_reason: dict[str, Any],
    stage_action_envelope: dict[str, Any] | None,
) -> dict[str, Any]:
    attempts = journal.setdefault("attempts", [])
    checkpoint_status = stop_reason.get("checkpoint_status")
    attempts.append(
        {
            "attempt_index": attempt_index,
            "trigger": trigger,
            "timestamp": datetime.now(UTC).isoformat(),
            "lifecycle_stage": lifecycle_stage,
            "checkpoint_status": checkpoint_status,
            "stop_reason": stop_reason,
            "stage_action_envelope": stage_action_envelope,
        }
    )
    journal["latest_stop_reason"] = stop_reason
    journal["latest_stage_action_envelope"] = stage_action_envelope
    journal["latest_route_report"] = route_report
    return journal


def _write_journal(journal_path: Path, journal: dict[str, Any]) -> None:
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    journal_path.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")


def _guard_artifact_bundle_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    lifecycle_stage: str,
) -> None:
    if not output_path.exists():
        return

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"bundle output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 bundle output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"bundle output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    same_identity = (
        existing_payload.get("grant_run_id") == grant_run_id
        and existing_payload.get("workspace_id") == workspace_id
        and existing_payload.get("draft_id") == draft_id
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "bundle output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_payload.get('grant_run_id')}/{existing_payload.get('workspace_id')}/{existing_payload.get('draft_id')} "
            f"!= {grant_run_id}/{workspace_id}/{draft_id}"
        ),
        errors=[],
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _guard_revision_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    active_revision_plan_id: str,
    lifecycle_stage: str | None,
) -> None:
    if not output_path.exists():
        return

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"revision output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 revised workspace output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"revision output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    existing_grant_run_id = existing_payload.get("grant_run_id")
    existing_workspace_id = existing_payload.get("workspace_id")
    existing_draft_id = existing_payload.get("draft_id")
    if existing_draft_id is None:
        current_selection = existing_payload.get("current_selection")
        if isinstance(current_selection, dict):
            existing_draft_id = current_selection.get("active_draft_id")

    existing_active_revision_plan_id = None
    current_selection = existing_payload.get("current_selection")
    if isinstance(current_selection, dict):
        existing_active_revision_plan_id = current_selection.get("active_revision_plan_id")
    if existing_active_revision_plan_id is None:
        revision_execution = existing_payload.get("revision_execution")
        if isinstance(revision_execution, dict):
            existing_active_revision_plan_id = revision_execution.get("active_revision_plan_id")

    same_identity = (
        existing_grant_run_id == grant_run_id
        and existing_workspace_id == workspace_id
        and existing_draft_id == draft_id
        and existing_active_revision_plan_id == active_revision_plan_id
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "revision output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_grant_run_id}/{existing_workspace_id}/{existing_draft_id}/{existing_active_revision_plan_id} "
            f"!= {grant_run_id}/{workspace_id}/{draft_id}/{active_revision_plan_id}"
        ),
        errors=[],
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _guard_critique_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    active_revision_plan_id: str,
    lifecycle_stage: str | None,
) -> None:
    _guard_revision_output_identity(
        output_path,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        draft_id=draft_id,
        active_revision_plan_id=active_revision_plan_id,
        lifecycle_stage=lifecycle_stage,
    )


def _guard_workspace_output_identity(
    output_path: Path,
    *,
    workspace_document: dict[str, Any],
    draft_id: str | None,
) -> None:
    if not output_path.exists():
        return

    grant_run_id = workspace_document.get("grant_run_id")
    workspace_id = workspace_document.get("workspace_id")
    lifecycle_stage = workspace_document.get("lifecycle_stage")
    expected_selection = workspace_document.get("current_selection")
    if not isinstance(expected_selection, dict):
        expected_selection = {}

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"workspace output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 workspace output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"workspace output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    existing_selection = existing_payload.get("current_selection")
    if not isinstance(existing_selection, dict):
        existing_selection = {}
    existing_draft_id = existing_payload.get("draft_id")
    if existing_draft_id is None:
        existing_draft_id = existing_selection.get("active_draft_id")
    expected_draft_id = draft_id if draft_id is not None else expected_selection.get("active_draft_id")

    same_identity = (
        existing_payload.get("grant_run_id") == grant_run_id
        and existing_payload.get("workspace_id") == workspace_id
        and existing_payload.get("lifecycle_stage") == lifecycle_stage
        and existing_draft_id == expected_draft_id
        and existing_selection == expected_selection
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "workspace output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_payload.get('grant_run_id')}/{existing_payload.get('workspace_id')}/{existing_payload.get('lifecycle_stage')} "
            f"selection={existing_selection} draft_id={existing_draft_id} "
            f"!= {grant_run_id}/{workspace_id}/{lifecycle_stage} "
            f"selection={expected_selection} draft_id={expected_draft_id}"
        ),
        errors=[],
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _read_artifact_bundle(
    artifact_bundle_path: str | Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    lifecycle_stage: str | None,
) -> dict[str, Any]:
    resolved_bundle_path = Path(artifact_bundle_path).expanduser().resolve()
    try:
        artifact_bundle = json.loads(resolved_bundle_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 artifact bundle 文件: {resolved_bundle_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"artifact bundle JSON 解析失败: {resolved_bundle_path}") from exc

    if not isinstance(artifact_bundle, dict):
        raise WorkspaceStateError(
            f"artifact bundle 顶层必须是 JSON object: {resolved_bundle_path}",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    if artifact_bundle.get("bundle_kind") != "artifact_bundle":
        raise WorkspaceStateError(
            f"artifact bundle kind 非法: {artifact_bundle.get('bundle_kind')}",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    if (
        artifact_bundle.get("grant_run_id") != grant_run_id
        or artifact_bundle.get("workspace_id") != workspace_id
        or artifact_bundle.get("draft_id") != draft_id
    ):
        raise WorkspaceStateError(
            (
                "artifact bundle identity 不匹配: "
                f"{artifact_bundle.get('grant_run_id')}/{artifact_bundle.get('workspace_id')}/{artifact_bundle.get('draft_id')} "
                f"!= {grant_run_id}/{workspace_id}/{draft_id}"
            ),
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    _validate_required_artifact_bundle_fields(
        artifact_bundle,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    return artifact_bundle


def _read_final_package(final_package_path: str | Path) -> dict[str, Any]:
    resolved_final_package_path = Path(final_package_path).expanduser().resolve()
    try:
        final_package = json.loads(resolved_final_package_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 final package 文件: {resolved_final_package_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"final package JSON 解析失败: {resolved_final_package_path}") from exc

    if not isinstance(final_package, dict):
        raise WorkspaceStateError(f"final package 顶层必须是 JSON object: {resolved_final_package_path}")

    if final_package.get("package_kind") != "final_package":
        raise WorkspaceStateError(f"final package kind 非法: {final_package.get('package_kind')}")

    required_fields = (
        "package_version",
        "grant_run_id",
        "workspace_id",
        "draft_id",
        "lifecycle_stage",
        "freeze_manifest",
        "lineage",
        "checkpoint_summary",
    )
    for field in required_fields:
        if field not in final_package:
            raise WorkspaceStateError(f"final package 缺少字段: {field}")

    package_version = final_package.get("package_version")
    if not isinstance(package_version, int) or package_version != SUPPORTED_FINAL_PACKAGE_VERSION:
        raise WorkspaceStateError("final package 缺少字段: package_version")

    _validate_required_final_package_fields(final_package)
    return final_package


def _read_program_id(*, repo_root: Path | None = None) -> str:
    return _read_program_id_from_contract(repo_root=repo_root)


def _read_current_program_contract(*, repo_root: Path | None = None) -> dict[str, Any]:
    return _read_current_program_contract_from_contract(repo_root=repo_root)


def _validate_contract_schema(
    payload: dict[str, Any],
    *,
    schema_file: str,
    context: str,
    grant_run_id: str | None = None,
    workspace_id: str | None = None,
    lifecycle_stage: str | None = None,
) -> None:
    issues = _SchemaSubsetValidator(SchemaStore()).validate(payload, schema_file)
    if not issues:
        return
    detail = "; ".join(f"{issue.path}: {issue.message}" for issue in issues[:5])
    if len(issues) > 5:
        detail = f"{detail}; 其余 {len(issues) - 5} 项略"
    raise WorkspaceStateError(
        f"{context} schema 校验失败: {detail}",
        errors=issues,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _validate_schema_payload(
    payload: dict[str, Any],
    *,
    schema_file: str,
    context: str,
) -> None:
    _validate_contract_schema(
        payload,
        schema_file=schema_file,
        context=context,
    )


def _validate_executor_routing_contract(
    contract: dict[str, Any],
    *,
    current_stage: str,
    recommended_next_stage: str,
    include_route_catalog: bool,
    grant_run_id: str | None = None,
    workspace_id: str | None = None,
    lifecycle_stage: str | None = None,
) -> None:
    _validate_contract_schema(
        contract,
        schema_file=EXECUTOR_ROUTING_CONTRACT_SCHEMA_FILE,
        context="executor_routing_contract",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )

    expected_current_stage_route = _build_stage_route_contract(
        current_stage,
        source_stage=current_stage,
    )
    if contract.get("current_stage_route") != expected_current_stage_route:
        raise WorkspaceStateError(
            "executor_routing_contract.current_stage_route 与当前冻结 route truth 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    expected_recommended_route = _build_stage_route_contract(
        recommended_next_stage,
        source_stage=current_stage,
    )
    if contract.get("recommended_executor_route") != expected_recommended_route:
        raise WorkspaceStateError(
            "executor_routing_contract.recommended_executor_route 与当前冻结 route truth 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    if not include_route_catalog:
        if "author_side_route_catalog" in contract:
            raise WorkspaceStateError(
                "executor_routing_contract 不允许在当前 surface 携带 author_side_route_catalog。",
                errors=[],
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )
        return

    expected_route_catalog = [
        _build_author_side_route_contract(route_id, source_stage=route_id)
        for route_id in AUTHOR_SIDE_ROUTE_IDS
    ]
    if contract.get("author_side_route_catalog") != expected_route_catalog:
        raise WorkspaceStateError(
            "executor_routing_contract.author_side_route_catalog 与当前冻结 route matrix 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def _validate_hosted_contract_bundle(
    bundle: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str | None,
) -> None:
    _validate_contract_schema(
        bundle,
        schema_file=HOSTED_CONTRACT_BUNDLE_SCHEMA_FILE,
        context="hosted_contract_bundle",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    if bundle.get("domain_entry_contract") != build_domain_entry_contract():
        raise WorkspaceStateError(
            "hosted_contract_bundle.domain_entry_contract 与当前冻结 entry contract 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if bundle.get("schema_contract") != _build_schema_contract():
        raise WorkspaceStateError(
            "hosted_contract_bundle.schema_contract 与当前冻结 schema registry 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if bundle.get("authoring_contract") != _build_hosted_authoring_contract():
        raise WorkspaceStateError(
            "hosted_contract_bundle.authoring_contract 与当前冻结 author-side route matrix 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def _build_executor_routing_contract(
    *,
    current_stage: str,
    recommended_next_stage: str,
    include_route_catalog: bool = False,
) -> dict[str, Any]:
    contract = {
        "contract_version": EXECUTOR_ROUTING_CONTRACT_VERSION,
        "current_stage_route": _build_stage_route_contract(
            current_stage,
            source_stage=current_stage,
        ),
        "recommended_executor_route": _build_stage_route_contract(
            recommended_next_stage,
            source_stage=current_stage,
        ),
    }
    if include_route_catalog:
        contract["author_side_route_catalog"] = [
            _build_author_side_route_contract(route_id, source_stage=route_id)
            for route_id in AUTHOR_SIDE_ROUTE_IDS
        ]
    return contract


def _build_stage_route_contract(stage: str, *, source_stage: str) -> dict[str, Any]:
    resolved_stage = _require_known_route_id(stage, context="executor routing stage")
    return _build_author_side_route_contract(resolved_stage, source_stage=source_stage)


def _build_author_side_route_contract(route_id: str, *, source_stage: str) -> dict[str, Any]:
    resolved_route_id = _require_known_route_id(route_id, context="executor routing route")
    execution_command = {
        "direction_screening": "execute-direction-screening-pass",
        "question_refinement": "execute-question-refinement-pass",
        "argument_building": "execute-argument-building-pass",
        "fit_alignment": "execute-fit-alignment-pass",
        "outline": "execute-outline-pass",
        "drafting": "execute-drafting-pass",
        "critique": "execute-critique-pass",
        "revision": "execute-revision-pass",
        "frozen": "execute-freeze-pass",
        "artifact_bundle": "build-artifact-bundle",
        "final_package": "build-final-package",
        "hosted_contract_bundle": "build-hosted-contract-bundle",
    }.get(resolved_route_id)
    if execution_command is None:
        raise WorkspaceStateError(
            f"未找到已 landed 的 author-side route command: {resolved_route_id}",
            lifecycle_stage=source_stage,
        )
    return {
        "route_id": resolved_route_id,
        "route_status": "landed",
        "executor_owner": EXECUTOR_ROUTE_OWNER,
        "execution_surface": {
            "surface_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
            "entry_adapter": SERVICE_SAFE_ENTRY_ADAPTER,
            "command": execution_command,
        },
        "handoff_contract_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
    }


def _build_service_safe_domain_surface(command: str) -> dict[str, str]:
    resolved_command = _require_nonempty_route_id(command, context="service-safe domain surface command")
    return {
        "surface_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
        "entry_adapter": SERVICE_SAFE_ENTRY_ADAPTER,
        "command": resolved_command,
    }


def _build_runtime_substrate_contract(*, current_program_contract: dict[str, Any]) -> dict[str, Any]:
    runtime_owner = current_program_contract.get("runtime_owner")
    if not isinstance(runtime_owner, dict):
        raise WorkspaceStateError("CURRENT_PROGRAM contract 缺少字段: runtime_owner")

    return {
        "runtime_owner": "Hermes",
        "current_owner_line": _require_nonempty_string(
            runtime_owner,
            "current_owner_line",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "active_phase": _require_nonempty_string(
            runtime_owner,
            "active_phase",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "active_tranche": _require_nonempty_string(
            runtime_owner,
            "active_tranche",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "compatibility_bridge": _require_nonempty_string(
            runtime_owner,
            "compatibility_bridge",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "repo_tracked_current_program_contract": CURRENT_PROGRAM_RELATIVE_PATH.as_posix(),
    }


def _build_runtime_state_contract() -> dict[str, Any]:
    return {
        "root": runtime_state_display_path(),
        "session_journal_root": _directory_display_path("sessions"),
        "logs_root": _directory_display_path("logs"),
        "reports_root": _directory_display_path("reports", "<program_id>"),
        "prompts_root": _directory_display_path("prompts"),
        "handoff_state_root": _directory_display_path("handoff_state"),
        "non_repo_tracked": True,
    }


def _build_operator_contract() -> dict[str, Any]:
        return {
            "canonical_audit_surfaces": [
                "validate-workspace",
                "summarize-workspace",
                "grant-intake-audit",
                "grant-evidence-grounding",
                "grant-quality-scorecard",
                "grant-quality-closure-dossier",
                "grant-quality-diff",
                "next-step",
                "critique-summary",
                "stage-route-report",
            ],
        "canonical_export_surfaces": [
            "execute-direction-screening-pass",
            "execute-question-refinement-pass",
            "execute-argument-building-pass",
            "execute-fit-alignment-pass",
            "execute-outline-pass",
            "execute-drafting-pass",
            "execute-critique-pass",
            "execute-revision-pass",
            "execute-freeze-pass",
            "build-artifact-bundle",
            "build-final-package",
            "build-hosted-contract-bundle",
            "build-submission-ready-package",
        ],
        "checkpoint_aggregation_surface": "stage-route-report",
    }
def _build_schema_contract() -> dict[str, Any]:
    return {
        "schema_version": SchemaStore().load_schema_index()["schema_version"],
        "schema_index_path": SCHEMA_INDEX_RELATIVE_PATH,
        "aggregate_root_schema": SchemaStore().load_schema_index()["aggregate_root"],
        "contract_schema_files": list(HOSTED_CONTRACT_SCHEMA_FILES),
    }


def _build_hosted_authoring_contract() -> dict[str, Any]:
    return {
        "route_contract_version": EXECUTOR_ROUTING_CONTRACT_VERSION,
        "route_catalog_kind": "author_side_route_catalog",
        "author_side_route_catalog": [
            _build_author_side_route_contract(route_id, source_stage=route_id)
            for route_id in AUTHOR_SIDE_ROUTE_IDS
        ],
    }


def _require_nonempty_string(payload: dict[str, Any], field: str, *, context: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field}")
    return value


def _require_nonempty_route_id(value: Any, *, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少合法 route_id")
    return value.strip()


def _require_known_route_id(value: Any, *, context: str) -> str:
    resolved_value = _require_nonempty_route_id(value, context=context)
    if resolved_value not in AUTHOR_SIDE_ROUTE_IDS:
        raise WorkspaceStateError(f"{context} 不支持 route_id: {resolved_value}")
    return resolved_value


def _directory_display_path(*segments: str) -> str:
    return runtime_state_display_path(*segments).rstrip("/") + "/"


def _resolve_control_plane_current_program_path(
    *,
    repo_root: Path | None = None,
    worktree_list_text: str | None = None,
) -> Path:
    del worktree_list_text
    return resolve_current_program_contract_path(repo_root=repo_root)


def _read_git_worktree_list(*, repo_root: Path) -> str:
    del repo_root
    raise WorkspaceStateError("项目级 .runtime-program 已退役；不再通过 git worktree 列表解析 control-plane root。")


def _select_control_plane_current_program_path(
    *,
    repo_root: Path,
    worktree_list_text: str,
) -> Path:
    del repo_root
    del worktree_list_text
    raise WorkspaceStateError("项目级 .runtime-program 已退役；不再通过 main worktree 回退解析 CURRENT_PROGRAM。")


def _parse_git_worktree_list_porcelain(worktree_list_text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw_line in worktree_list_text.splitlines():
        if not raw_line:
            continue
        key, _, value = raw_line.partition(" ")
        if key == "worktree":
            if current is not None:
                entries.append(current)
            current = {"worktree": value}
            continue
        if current is None:
            continue
        if key in {"branch", "HEAD"}:
            current[key] = value

    if current is not None:
        entries.append(current)
    return entries


def _guard_final_package_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    lifecycle_stage: str | None,
) -> None:
    if not output_path.exists():
        return

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"final package output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 final package output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"final package output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    same_identity = (
        existing_payload.get("grant_run_id") == grant_run_id
        and existing_payload.get("workspace_id") == workspace_id
        and existing_payload.get("draft_id") == draft_id
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "final package output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_payload.get('grant_run_id')}/{existing_payload.get('workspace_id')}/{existing_payload.get('draft_id')} "
            f"!= {grant_run_id}/{workspace_id}/{draft_id}"
        ),
        errors=[],
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def _guard_hosted_contract_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    program_id: str,
) -> None:
    if not output_path.exists():
        return

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"hosted contract output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。"
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 hosted contract output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"hosted contract output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。"
        )

    existing_execution_identity = existing_payload.get("execution_identity")
    if isinstance(existing_execution_identity, dict):
        existing_grant_run_id = existing_execution_identity.get("grant_run_id")
        existing_workspace_id = existing_execution_identity.get("workspace_id")
        existing_draft_id = existing_execution_identity.get("draft_id")
        existing_program_id = existing_execution_identity.get("program_id")
    else:
        existing_grant_run_id = existing_payload.get("grant_run_id")
        existing_workspace_id = existing_payload.get("workspace_id")
        existing_draft_id = existing_payload.get("draft_id")
        existing_program_id = existing_payload.get("program_id")

    same_identity = (
        existing_grant_run_id == grant_run_id
        and existing_workspace_id == workspace_id
        and existing_draft_id == draft_id
        and existing_program_id == program_id
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "hosted contract output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_grant_run_id}/{existing_workspace_id}/{existing_draft_id}/{existing_program_id} "
            f"!= {grant_run_id}/{workspace_id}/{draft_id}/{program_id}"
        )
    )


def _guard_submission_ready_package_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    program_id: str,
) -> None:
    if not output_path.exists():
        return

    try:
        existing_payload = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError(
            f"submission ready package output identity 不匹配: {output_path} 已存在且不是可校验的 JSON object。"
        ) from exc
    except OSError as exc:
        raise WorkspaceFileError(f"读取 submission ready package output 失败: {output_path}") from exc

    if not isinstance(existing_payload, dict):
        raise WorkspaceStateError(
            f"submission ready package output identity 不匹配: {output_path} 已存在且顶层不是 JSON object。"
        )

    same_identity = (
        existing_payload.get("package_kind") == "submission_ready_package"
        and existing_payload.get("grant_run_id") == grant_run_id
        and existing_payload.get("workspace_id") == workspace_id
        and existing_payload.get("draft_id") == draft_id
        and existing_payload.get("program_id") == program_id
    )
    if same_identity:
        return

    raise WorkspaceStateError(
        (
            "submission ready package output identity 不匹配: "
            f"{output_path} -> "
            f"{existing_payload.get('grant_run_id')}/{existing_payload.get('workspace_id')}/"
            f"{existing_payload.get('draft_id')}/{existing_payload.get('program_id')} "
            f"!= {grant_run_id}/{workspace_id}/{draft_id}/{program_id}"
        )
    )


def _write_hosted_contract_bundle_output(output_path: Path, hosted_contract_bundle: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(hosted_contract_bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 hosted contract output 失败: {output_path}") from exc


def _write_artifact_bundle_output(output_path: Path, bundle: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 bundle output 失败: {output_path}") from exc


def _write_revised_workspace_output(output_path: Path, revised_workspace: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    materialized_workspace = materialize_workspace_surfaces(revised_workspace)
    try:
        output_path.write_text(json.dumps(materialized_workspace, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 revised workspace output 失败: {output_path}") from exc


def _write_final_package_output(output_path: Path, final_package: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 final package output 失败: {output_path}") from exc


def _write_submission_ready_package_output(
    output_path: Path,
    submission_ready_package: dict[str, Any],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(
            json.dumps(submission_ready_package, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError as exc:
        raise WorkspaceFileError(f"写入 submission ready package output 失败: {output_path}") from exc


def _write_json_output(output_path: Path, payload: dict[str, Any], *, label: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 {label} 失败: {output_path}") from exc


def _load_json_object(input_path: str | Path, *, context: str) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    try:
        payload = json.loads(resolved_input_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise WorkspaceFileError(f"未找到 {context} 文件: {resolved_input_path}") from exc
    except json.JSONDecodeError as exc:
        raise WorkspaceFileError(f"{context} JSON 解析失败: {resolved_input_path}") from exc
    if not isinstance(payload, dict):
        raise WorkspaceFileError(f"{context} 顶层必须是 JSON object。")
    return payload


def _default_funding_landscape_cache_path() -> Path:
    return resolve_runtime_state_root() / "funding-landscape" / "cache" / "latest.json"


def _derive_funding_landscape_diff_report_path(cache_path: Path) -> Path:
    return cache_path.with_name(f"{cache_path.stem}.diff.json")


def _load_existing_cache_snapshot(cache_path: Path) -> dict[str, Any] | None:
    if not cache_path.exists():
        return None
    return _load_json_object(cache_path, context="funding landscape cache")


def _load_funding_landscape_cache_if_needed(discovery_input: dict[str, Any]) -> dict[str, Any] | None:
    if discovery_input.get("discovery_source") != "official_cached":
        return None
    cache_path_value = discovery_input.get("cache_path")
    cache_path = (
        Path(str(cache_path_value)).expanduser().resolve()
        if isinstance(cache_path_value, str) and cache_path_value.strip()
        else _default_funding_landscape_cache_path()
    )
    if not cache_path.exists():
        raise WorkspaceFileError(f"official_cached 模式缺少 funding cache: {cache_path}")
    snapshot = _load_json_object(cache_path, context="funding landscape cache")
    _validate_schema_payload(
        snapshot,
        schema_file=FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE,
        context="funding_landscape_cache",
    )
    return snapshot


def _build_selection_input_from_discovery(
    *,
    discovery_input: dict[str, Any],
    funding_opportunity_pool: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "metadata": dict(discovery_input["metadata"]),
        "selection_input_id": discovery_input["discovery_input_id"],
        "mode": discovery_input.get("mode", "auto"),
        "rough_direction_hint": discovery_input.get("rough_direction_hint"),
        "applicant_profile": dict(discovery_input["applicant_profile"]),
        "track_record": dict(discovery_input["track_record"]),
        "active_project_set": dict(
            discovery_input.get("active_project_set")
            or {
                "metadata": dict(discovery_input["metadata"]),
                "project_set_id": f"{discovery_input['discovery_input_id']}-projects",
                "projects": [],
            }
        ),
        "preliminary_evidence_pack": dict(
            discovery_input.get("preliminary_evidence_pack")
            or {
                "metadata": dict(discovery_input["metadata"]),
                "evidence_pack_id": f"{discovery_input['discovery_input_id']}-prelim",
                "evidence_items": [],
            }
        ),
        "funding_opportunity_pool": [dict(item) for item in funding_opportunity_pool],
    }
