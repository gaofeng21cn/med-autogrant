from __future__ import annotations

from typing import Any

from med_autogrant.workspace_types import WorkspaceStateError


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
