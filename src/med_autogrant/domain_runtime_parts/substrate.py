from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from med_autogrant.control_plane import (
    CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH,
    read_current_program_contract as _read_current_program_contract_from_contract,
    read_program_id as _read_program_id_from_contract,
    resolve_current_program_contract_path,
    resolve_runtime_state_root,
    runtime_state_display_path,
)
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
from med_autogrant.upstream_hermes import MagGrantRunLedger
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
from med_autogrant.schema_subset_validator import SchemaSubsetValidator as _SchemaSubsetValidator
from med_autogrant.workspace import (
    build_grant_evidence_grounding,
    build_grant_intake_audit,
    build_critique_summary,
    load_workspace_document,
    materialize_workspace_surfaces,
    summarize_workspace_document,
)
from med_autogrant.workspace_projection_parts import _require_workspace_context
from med_autogrant.workspace_scaffold import (
    materialize_mag_directory_workspace,
    resolve_mag_directory_workspace_document_path,
)
from med_autogrant.workspace_types import WorkspaceError, WorkspaceFileError, WorkspaceStateError
from med_autogrant.workspace_validation import validate_workspace_document
from med_autogrant import editable_shared_bootstrap as _editable_shared_bootstrap
from med_autogrant.domain_runtime_parts.shared import (
    FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE,
    FUNDING_LANDSCAPE_DIFF_REPORT_SCHEMA_FILE,
    FUNDING_LANDSCAPE_DISCOVERY_INPUT_SCHEMA_FILE,
    FUNDING_LANDSCAPE_DISCOVERY_SCHEMA_FILE,
    GRANT_EVIDENCE_GROUNDING_SCHEMA_FILE,
    GRANT_INTAKE_AUDIT_SCHEMA_FILE,
    GRANT_QUALITY_CLOSURE_DOSSIER_SCHEMA_FILE,
    GRANT_QUALITY_DIFF_SCHEMA_FILE,
    GRANT_QUALITY_SCORECARD_SCHEMA_FILE,
    LocalRuntimeStateError,
    PROJECT_PROFILE_SELECTION_INPUT_SCHEMA_FILE,
    PROJECT_PROFILE_SELECTION_SCHEMA_FILE,
)
from med_autogrant.domain_runtime_parts.authoring_surface import DomainRuntimeAuthoringSurfaceMixin
from med_autogrant.domain_runtime_parts.handoff_surfaces import DomainRuntimeHandoffSurfaceMixin


_editable_shared_bootstrap.ensure_editable_dependency_paths()


class MagDomainRuntime(DomainRuntimeAuthoringSurfaceMixin, DomainRuntimeHandoffSurfaceMixin):
    """MAG-owned domain runtime surface for grant authoring, quality, and export."""

    runtime_owner = "Med Auto Grant"

    def describe_topology(self) -> dict[str, Any]:
        return {
            "runtime_owner": self.runtime_owner,
            "domain_agent": "Med Auto Grant",
            "authoring_truth_owner": "Med Auto Grant",
            "quality_gate_owner": "Med Auto Grant",
            "export_authority": "Med Auto Grant",
            "default_formal_entry": "CLI",
            "default_stage_attempt_executor": "Codex CLI",
            "supported_protocol_layer": "MCP",
            "internal_controller_surface": "controller",
            "optional_proof_executor": "Hermes-Agent",
            "optional_proof_executor_boundary": "explicit opt-in only",
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
        output_path: str | Path | None = None,
        workspace_root: str | Path | None = None,
        initialize_git: bool = True,
    ) -> dict[str, Any]:
        if output_path is None and workspace_root is None:
            raise WorkspaceStateError("initialize-intake-workspace 需要 --output 或 --workspace-root。")
        if output_path is not None and workspace_root is not None:
            raise WorkspaceStateError("initialize-intake-workspace 只能指定 --output 或 --workspace-root 其中一个。")

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

        if workspace_root is not None:
            resolved_workspace_root = Path(workspace_root).expanduser().resolve()
            resolved_output_path = resolve_mag_directory_workspace_document_path(resolved_workspace_root)
            _guard_workspace_output_identity(
                resolved_output_path,
                workspace_document=workspace,
                draft_id=None,
            )
            scaffold = materialize_mag_directory_workspace(
                workspace_root=resolved_workspace_root,
                workspace_document=workspace,
                initialize_git=initialize_git,
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
                "workspace_root": str(resolved_workspace_root),
                "workspace_path": str(resolved_output_path),
                "workspace_git": scaffold["workspace_git"],
                "workspace_scaffold": scaffold,
                "project_profile_selection": selection,
                "initialized_workspace": workspace,
            }

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

        attempt_index = MagGrantRunLedger().record_attempt(
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

    def _load_workspace(self, input_path: str | Path) -> dict[str, Any]:
        return load_workspace_document(Path(input_path).expanduser().resolve())

from med_autogrant.domain_runtime_parts.contracts import (
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
from med_autogrant.domain_runtime_parts.io import (
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
from med_autogrant.domain_runtime_parts.runtime_ops import (
    _apply_quality_gate_to_route,
    _build_autonomy_quality_evaluator_output,
    _looks_like_workspace,
    _resolve_journal_path,
    build_validation_failed_route_report,
    derive_stage_action_envelope,
    derive_stop_reason,
)

__all__ = [name for name in globals() if not name.startswith("__")]
