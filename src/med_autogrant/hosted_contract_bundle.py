from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from med_autogrant.workspace import WorkspaceFileError, WorkspaceStateError


HOSTED_CONTRACT_VERSION = 1
HOSTED_CONTRACT_KIND = "hosted_contract_bundle"
CURRENT_PROGRAM_RELATIVE_PATH = Path(".omx") / "context" / "CURRENT_PROGRAM.md"
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


def build_hosted_contract_bundle_payload(
    *,
    final_package_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    final_package = _read_final_package(final_package_path)
    program_id = _read_program_id()

    hosted_contract_bundle = {
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

    for field in ("package_version", "grant_run_id", "workspace_id", "draft_id", "lifecycle_stage", "freeze_manifest", "lineage", "checkpoint_summary"):
        if field not in final_package:
            raise WorkspaceStateError(f"final package 缺少字段: {field}")

    _validate_required_final_package_fields(final_package)

    return final_package


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


def _read_program_id() -> str:
    current_program_path = _resolve_control_plane_current_program_path()
    try:
        text = current_program_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"读取 CURRENT_PROGRAM 失败: {current_program_path}") from exc

    match = re.search(r"- program_id:\s*`([^`]+)`", text)
    if match is None:
        raise WorkspaceStateError(f"CURRENT_PROGRAM 缺少可解析的 program_id: {current_program_path}")
    return match.group(1)


def _resolve_control_plane_current_program_path(
    *,
    repo_root: Path | None = None,
    worktree_list_text: str | None = None,
) -> Path:
    resolved_repo_root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    local_current_program = resolved_repo_root / CURRENT_PROGRAM_RELATIVE_PATH
    if local_current_program.exists():
        return local_current_program

    if worktree_list_text is None:
        worktree_list_text = _read_git_worktree_list(repo_root=resolved_repo_root)
    return _select_control_plane_current_program_path(
        repo_root=resolved_repo_root,
        worktree_list_text=worktree_list_text,
    )


def _read_git_worktree_list(*, repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            check=True,
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise WorkspaceFileError("未找到 git，可用性不足，无法解析 control-plane root checkout。") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        message = "读取 git worktree 列表失败，无法解析 control-plane root checkout。"
        if stderr:
            message = f"{message} {stderr}"
        raise WorkspaceFileError(message) from exc
    return result.stdout


def _select_control_plane_current_program_path(
    *,
    repo_root: Path,
    worktree_list_text: str,
) -> Path:
    entries = _parse_git_worktree_list_porcelain(worktree_list_text)
    main_entries = [entry for entry in entries if entry.get("branch") == "refs/heads/main"]
    if not main_entries:
        raise WorkspaceFileError("git worktree 列表中未找到 `refs/heads/main`，无法解析 control-plane root checkout。")
    if len(main_entries) > 1:
        raise WorkspaceStateError("检测到多个 `refs/heads/main` worktree，无法唯一确定 control-plane root checkout。")

    main_worktree_path = Path(main_entries[0]["worktree"]).expanduser().resolve()
    current_program_path = main_worktree_path / CURRENT_PROGRAM_RELATIVE_PATH
    if not current_program_path.exists():
        raise WorkspaceFileError(f"root main worktree 缺少 CURRENT_PROGRAM.md: {current_program_path}")
    return current_program_path


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


def _guard_output_identity(
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


def _write_hosted_contract_bundle(output_path: Path, hosted_contract_bundle: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(hosted_contract_bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 hosted contract output 失败: {output_path}") from exc
