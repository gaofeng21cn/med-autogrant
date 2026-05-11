from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant import final_package_validation as _final_package_validation
from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.domain_runtime_parts.contracts import (
    build_hosted_authoring_contract as _build_hosted_authoring_contract,
    build_operator_contract as _build_operator_contract,
    build_runtime_state_contract as _build_runtime_state_contract,
    build_runtime_substrate_contract as _build_runtime_substrate_contract,
    build_schema_contract as _build_schema_contract,
    parse_git_worktree_list_porcelain,
    read_current_program_contract as _read_current_program_contract,
    read_git_worktree_list,
    read_program_id as _read_program_id_from_contract,
    resolve_control_plane_current_program_path,
    select_control_plane_current_program_path,
    validate_hosted_contract_bundle as _validate_hosted_contract_bundle,
)
from med_autogrant.domain_runtime_parts.io import (
    _guard_hosted_contract_output_identity,
    _read_final_package as _read_final_package_from_runtime_parts,
    _write_hosted_contract_bundle_output,
)
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError


HOSTED_CONTRACT_VERSION = 1
HOSTED_CONTRACT_KIND = "hosted_contract_bundle"
SUPPORTED_FINAL_PACKAGE_VERSION = 1
REQUIRED_FINAL_PACKAGE_OBJECT_FIELDS = (
    "freeze_manifest",
    "lineage",
    "checkpoint_summary",
)
REQUIRED_FINAL_PACKAGE_STRING_FIELDS = (
    "grant_run_id",
    "workspace_id",
    "draft_id",
    "lifecycle_stage",
)
REQUIRED_FREEZE_MANIFEST_FIELDS = (
    "draft_version_label",
    "draft_status",
    "active_revision_plan_id",
    "critique_id",
    "checkpoint_status",
    "presubmission_frozen",
)
REQUIRED_LINEAGE_FIELDS = (
    "frozen_question_id",
    "selected_direction_id",
    "selected_question_id",
    "active_fit_mapping_id",
    "draft_id",
    "revision_plan_id",
)
ALLOWED_FINAL_PACKAGE_DRAFT_STATUSES = {"revised", "frozen"}
ALLOWED_FINAL_PACKAGE_CHECKPOINT_STATUSES = {"freeze_ready", "submission_frozen"}


def build_hosted_contract_bundle_document(
    *,
    final_package: dict[str, Any],
    program_id: str,
    runtime_substrate_contract: dict[str, Any],
    runtime_state_contract: dict[str, Any],
    operator_contract: dict[str, Any],
    domain_entry_contract: dict[str, Any],
    schema_contract: dict[str, Any],
    authoring_contract: dict[str, Any],
) -> dict[str, Any]:
    return {
        "contract_version": HOSTED_CONTRACT_VERSION,
        "bundle_kind": HOSTED_CONTRACT_KIND,
        "formal_entry_matrix": {
            "default_formal_entry": "CLI",
            "supported_protocol_layer": "MCP",
            "internal_controller_surface": "controller",
        },
        "execution_identity": {
            "grant_run_id": final_package["grant_run_id"],
            "workspace_id": final_package["workspace_id"],
            "draft_id": final_package["draft_id"],
            "program_id": program_id,
        },
        "runtime_substrate_contract": runtime_substrate_contract,
        "runtime_state_contract": runtime_state_contract,
        "session_contract": {
            "session_handle_kind": "grant_run_id",
            "start_entry": "runtime-run",
            "resume_entry": "runtime-resume",
            "required_local_surfaces": [
                "runtime-run",
                "runtime-resume",
                "build-artifact-bundle",
                "build-final-package",
                "run_journal",
                "stage_action_envelope",
            ],
        },
        "operator_contract": operator_contract,
        "state_contract": {
            "workspace_surface_kind": "nsfc_workspace",
            "run_journal_kind": "local_run_journal",
            "stage_action_envelope_kind": "stage_action_envelope",
            "artifact_bundle_kind": "artifact_bundle",
            "final_package_kind": "final_package",
        },
        "artifact_contract": {
            "artifact_bundle_manifest_kind": "artifact_bundle_manifest",
            "final_package_manifest_kind": "freeze_manifest",
            "lineage_fields": list(final_package["lineage"].keys()),
        },
        "audit_contract": {
            "verification_checkpoint_kind": "verification_checkpoint",
            "checkpoint_status_kind": "checkpoint_status",
            "reviewed_revision_evidence_kind": "reviewed_revision_evidence",
        },
        "domain_entry_contract": domain_entry_contract,
        "schema_contract": schema_contract,
        "authoring_contract": authoring_contract,
    }


def build_hosted_contract_bundle_payload(
    *,
    final_package_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    final_package = _read_final_package(final_package_path)
    _validate_required_final_package_fields(final_package)
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
    _guard_output_identity(
        resolved_output_path,
        grant_run_id=final_package["grant_run_id"],
        workspace_id=final_package["workspace_id"],
        draft_id=final_package["draft_id"],
        program_id=program_id,
    )
    _write_hosted_contract_bundle(resolved_output_path, hosted_contract_bundle)
    return {
        "ok": True,
        "command": "build-hosted-contract-bundle",
        "grant_run_id": final_package["grant_run_id"],
        "workspace_id": final_package["workspace_id"],
        "draft_id": final_package["draft_id"],
        "output_path": str(resolved_output_path),
        "hosted_contract_bundle": hosted_contract_bundle,
    }


def _read_final_package(final_package_path: str | Path) -> dict[str, Any]:
    return _read_final_package_from_runtime_parts(final_package_path)


def _validate_required_final_package_fields(final_package: dict[str, Any]) -> None:
    _final_package_validation._validate_required_final_package_fields(final_package)


def _read_program_id(*, repo_root: Path | None = None) -> str:
    return _read_program_id_from_contract(repo_root=repo_root)


def _resolve_control_plane_current_program_path(
    *,
    repo_root: Path | None = None,
    worktree_list_text: str | None = None,
) -> Path:
    return resolve_control_plane_current_program_path(
        repo_root=repo_root,
        worktree_list_text=worktree_list_text,
    )


def _read_git_worktree_list(*, repo_root: Path) -> str:
    return read_git_worktree_list(repo_root=repo_root)


def _select_control_plane_current_program_path(
    *,
    repo_root: Path,
    worktree_list_text: str,
) -> Path:
    return select_control_plane_current_program_path(
        repo_root=repo_root,
        worktree_list_text=worktree_list_text,
    )


def _parse_git_worktree_list_porcelain(worktree_list_text: str) -> list[dict[str, str]]:
    return parse_git_worktree_list_porcelain(worktree_list_text)


def _guard_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    program_id: str,
) -> None:
    _guard_hosted_contract_output_identity(
        output_path,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        draft_id=draft_id,
        program_id=program_id,
    )


def _write_hosted_contract_bundle(output_path: Path, hosted_contract_bundle: dict[str, Any]) -> None:
    _write_hosted_contract_bundle_output(output_path, hosted_contract_bundle)
