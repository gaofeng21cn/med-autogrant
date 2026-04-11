from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from med_autogrant.workspace import WorkspaceFileError, WorkspaceStateError


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
            "start_entry": "run-local",
            "resume_entry": "resume-local",
            "required_local_surfaces": [
                "run-local",
                "resume-local",
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
    }


def build_hosted_contract_bundle_payload(
    *,
    final_package_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    from med_autogrant.hermes_runtime import HermesRuntimeSubstrate

    return HermesRuntimeSubstrate().build_hosted_contract_bundle(
        final_package_path=final_package_path,
        output_path=output_path,
    )


def _read_final_package(final_package_path: str | Path) -> dict[str, Any]:
    from med_autogrant.hermes_runtime import _read_final_package as _hermes_read_final_package

    return _hermes_read_final_package(final_package_path)


def _validate_required_final_package_fields(final_package: dict[str, Any]) -> None:
    package_version = final_package.get("package_version")
    if not isinstance(package_version, int) or package_version != SUPPORTED_FINAL_PACKAGE_VERSION:
        raise WorkspaceStateError("final package 缺少字段: package_version")

    for field in REQUIRED_FINAL_PACKAGE_STRING_FIELDS:
        value = final_package.get(field)
        if not isinstance(value, str) or not value:
            raise WorkspaceStateError(f"final package 缺少字段: {field}")

    for field in REQUIRED_FINAL_PACKAGE_OBJECT_FIELDS:
        if not isinstance(final_package.get(field), dict):
            raise WorkspaceStateError(f"final package 缺少字段: {field}")

    freeze_manifest = final_package["freeze_manifest"]
    for field in REQUIRED_FREEZE_MANIFEST_FIELDS:
        if field not in freeze_manifest:
            raise WorkspaceStateError(f"final package freeze_manifest 缺少字段: {field}")
    for field in ("draft_version_label", "active_revision_plan_id", "critique_id"):
        value = freeze_manifest.get(field)
        if not isinstance(value, str) or not value:
            raise WorkspaceStateError(f"final package freeze_manifest.{field} 非法: {value}")
    presubmission_frozen = freeze_manifest.get("presubmission_frozen")
    if not isinstance(presubmission_frozen, bool):
        raise WorkspaceStateError(f"final package freeze_manifest.presubmission_frozen 非法: {presubmission_frozen}")

    checkpoint_summary = final_package["checkpoint_summary"]
    verification_checkpoint = checkpoint_summary.get("verification_checkpoint")
    if not isinstance(verification_checkpoint, dict):
        raise WorkspaceStateError("final package checkpoint_summary 缺少字段: verification_checkpoint")
    if "checkpoint_status" not in checkpoint_summary:
        raise WorkspaceStateError("final package checkpoint_summary 缺少字段: checkpoint_status")

    lineage = final_package["lineage"]
    for field in REQUIRED_LINEAGE_FIELDS:
        if field not in lineage:
            raise WorkspaceStateError(f"final package lineage 缺少字段: {field}")
        value = lineage.get(field)
        if not isinstance(value, str) or not value:
            raise WorkspaceStateError(f"final package lineage.{field} 非法: {value}")

    draft_status = freeze_manifest.get("draft_status")
    if draft_status not in ALLOWED_FINAL_PACKAGE_DRAFT_STATUSES:
        raise WorkspaceStateError(f"final package freeze_manifest.draft_status 非法: {draft_status}")

    freeze_manifest_checkpoint_status = freeze_manifest.get("checkpoint_status")
    if freeze_manifest_checkpoint_status not in ALLOWED_FINAL_PACKAGE_CHECKPOINT_STATUSES:
        raise WorkspaceStateError(
            f"final package freeze_manifest.checkpoint_status 非法: {freeze_manifest_checkpoint_status}"
        )

    checkpoint_summary_status = checkpoint_summary.get("checkpoint_status")
    if checkpoint_summary_status not in ALLOWED_FINAL_PACKAGE_CHECKPOINT_STATUSES:
        raise WorkspaceStateError(
            f"final package checkpoint_summary.checkpoint_status 非法: {checkpoint_summary_status}"
        )

    verification_checkpoint_status = verification_checkpoint.get("checkpoint_status")
    if verification_checkpoint_status not in ALLOWED_FINAL_PACKAGE_CHECKPOINT_STATUSES:
        raise WorkspaceStateError(
            f"final package verification_checkpoint.checkpoint_status 非法: {verification_checkpoint_status}"
        )

    if (
        freeze_manifest_checkpoint_status != checkpoint_summary_status
        or freeze_manifest_checkpoint_status != verification_checkpoint_status
    ):
        raise WorkspaceStateError("final package checkpoint_status 不一致。")


def _read_program_id(*, repo_root: Path | None = None) -> str:
    from med_autogrant.hermes_runtime import _read_program_id as _hermes_read_program_id

    return _hermes_read_program_id(repo_root=repo_root)


def _resolve_control_plane_current_program_path(
    *,
    repo_root: Path | None = None,
    worktree_list_text: str | None = None,
) -> Path:
    from med_autogrant.hermes_runtime import (
        _resolve_control_plane_current_program_path as _hermes_resolve_control_plane_current_program_path,
    )

    return _hermes_resolve_control_plane_current_program_path(
        repo_root=repo_root,
        worktree_list_text=worktree_list_text,
    )


def _read_git_worktree_list(*, repo_root: Path) -> str:
    from med_autogrant.hermes_runtime import _read_git_worktree_list as _hermes_read_git_worktree_list

    return _hermes_read_git_worktree_list(repo_root=repo_root)


def _select_control_plane_current_program_path(
    *,
    repo_root: Path,
    worktree_list_text: str,
) -> Path:
    from med_autogrant.hermes_runtime import (
        _select_control_plane_current_program_path as _hermes_select_control_plane_current_program_path,
    )

    return _hermes_select_control_plane_current_program_path(
        repo_root=repo_root,
        worktree_list_text=worktree_list_text,
    )


def _parse_git_worktree_list_porcelain(worktree_list_text: str) -> list[dict[str, str]]:
    from med_autogrant.hermes_runtime import (
        _parse_git_worktree_list_porcelain as _hermes_parse_git_worktree_list_porcelain,
    )

    return _hermes_parse_git_worktree_list_porcelain(worktree_list_text)


def _guard_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    program_id: str,
) -> None:
    from med_autogrant.hermes_runtime import (
        _guard_hosted_contract_output_identity as _hermes_guard_hosted_contract_output_identity,
    )

    _hermes_guard_hosted_contract_output_identity(
        output_path,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        draft_id=draft_id,
        program_id=program_id,
    )


def _write_hosted_contract_bundle(output_path: Path, hosted_contract_bundle: dict[str, Any]) -> None:
    from med_autogrant.hermes_runtime import (
        _write_hosted_contract_bundle_output as _hermes_write_hosted_contract_bundle_output,
    )

    _hermes_write_hosted_contract_bundle_output(output_path, hosted_contract_bundle)
