from __future__ import annotations

from pathlib import Path
from typing import Any

from opl_framework.workspace_boundary import (
    DEFAULT_WORKSPACE_DOCUMENT,
    WorkspaceScaffoldFile,
    materialize_directory_workspace,
)

from med_autogrant.domain_runtime_parts import (
    authoring_surface,
    handoff_surfaces,
    package_surface,
    quality_surface,
)
from med_autogrant.domain_runtime_parts.contracts import (
    validate_contract_schema as _validate_contract_schema,
    validate_schema_payload as _validate_schema_payload,
)
from med_autogrant.domain_runtime_parts.io import (
    _build_selection_input_from_discovery,
    _default_funding_landscape_cache_path,
    _derive_funding_landscape_diff_report_path,
    _guard_workspace_output_identity,
    _load_existing_cache_snapshot,
    _load_funding_landscape_cache_if_needed,
    _load_json_object,
    _write_json_output,
    _write_revised_workspace_output,
)
from med_autogrant.domain_runtime_parts.shared import (
    FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE,
    FUNDING_LANDSCAPE_DIFF_REPORT_SCHEMA_FILE,
    FUNDING_LANDSCAPE_DISCOVERY_INPUT_SCHEMA_FILE,
    FUNDING_LANDSCAPE_DISCOVERY_SCHEMA_FILE,
    GRANT_EVIDENCE_GROUNDING_SCHEMA_FILE,
    GRANT_INTAKE_AUDIT_SCHEMA_FILE,
    PROJECT_PROFILE_SELECTION_INPUT_SCHEMA_FILE,
    PROJECT_PROFILE_SELECTION_SCHEMA_FILE,
)
from med_autogrant.funding_landscape_discovery import (
    build_funding_landscape_cache,
    build_funding_landscape_diff_report,
    discover_funding_landscape,
)
from med_autogrant.project_profile_selector import (
    build_initialized_intake_workspace,
    select_project_profile,
)
from med_autogrant.route_report import build_stage_route_report
from med_autogrant.stage_router import determine_next_step
from med_autogrant.workspace import (
    build_grant_evidence_grounding,
    build_grant_intake_audit,
    build_critique_summary,
    load_workspace_document,
    summarize_workspace_document,
)
from med_autogrant.workspace_profile import (
    MAG_WORKSPACE_GITIGNORE_ENTRIES,
    MAG_WORKSPACE_DIRECTORIES,
    render_mag_workspace_readme,
)
from med_autogrant.workspace_types import WorkspaceStateError
from med_autogrant.workspace_validation import validate_workspace_document


class MagDomainRuntime:
    """Repo-side domain adapter and regression oracle for grant authoring, quality, and export."""

    runtime_owner = "one-person-lab"

    # Keep the implementation split by responsibility without a single-implementation hierarchy.
    grant_quality_scorecard = quality_surface.grant_quality_scorecard
    grant_quality_diff = quality_surface.grant_quality_diff
    grant_quality_closure_dossier = quality_surface.grant_quality_closure_dossier
    build_final_package = package_surface.build_final_package
    build_hosted_contract_bundle = package_surface.build_hosted_contract_bundle
    build_submission_ready_package = package_surface.build_submission_ready_package
    execute_direction_screening_pass = handoff_surfaces.execute_direction_screening_pass
    execute_question_refinement_pass = handoff_surfaces.execute_question_refinement_pass
    execute_argument_building_pass = handoff_surfaces.execute_argument_building_pass
    execute_fit_alignment_pass = handoff_surfaces.execute_fit_alignment_pass
    execute_outline_pass = handoff_surfaces.execute_outline_pass
    execute_drafting_pass = handoff_surfaces.execute_drafting_pass
    build_artifact_bundle = handoff_surfaces.build_artifact_bundle
    execute_revision_pass = handoff_surfaces.execute_revision_pass
    execute_critique_pass = handoff_surfaces.execute_critique_pass
    execute_freeze_pass = authoring_surface.execute_freeze_pass
    _write_authoring_execution_output = authoring_surface._write_authoring_execution_output

    def describe_topology(self) -> dict[str, Any]:
        return {
            "runtime_owner": self.runtime_owner,
            "runtime_surface_role": "repo_side_domain_adapter_and_regression_oracle",
            "domain_agent": "Med Auto Grant",
            "domain_surface_owner": "Med Auto Grant",
            "authoring_truth_owner": "Med Auto Grant",
            "quality_gate_owner": "Med Auto Grant",
            "export_authority": "Med Auto Grant",
            "can_claim_generic_runtime_owner": False,
            "default_formal_entry": "CLI",
            "default_stage_attempt_executor": "Codex CLI",
            "supported_protocol_layer": "MCP",
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
            resolved_output_path = resolved_workspace_root / DEFAULT_WORKSPACE_DOCUMENT
            _guard_workspace_output_identity(
                resolved_output_path,
                workspace_document=workspace,
                draft_id=None,
            )
            scaffold = materialize_directory_workspace(
                workspace_root=resolved_workspace_root,
                directories=MAG_WORKSPACE_DIRECTORIES,
                files=(
                    WorkspaceScaffoldFile(
                        "README.md",
                        render_mag_workspace_readme(workspace),
                    ),
                ),
                gitignore_entries=MAG_WORKSPACE_GITIGNORE_ENTRIES,
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

    def _load_workspace(self, input_path: str | Path) -> dict[str, Any]:
        return load_workspace_document(Path(input_path).expanduser().resolve())

__all__ = ["MagDomainRuntime"]
