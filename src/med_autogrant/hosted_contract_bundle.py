from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from med_autogrant.workspace import WorkspaceFileError, WorkspaceStateError


HOSTED_CONTRACT_VERSION = 1
HOSTED_CONTRACT_KIND = "hosted_contract_bundle"
# Post-R5A control-plane truth is anchored to the root checkout because `.omx/`
# is local state and is not copied into isolated implementation worktrees.
CONTROL_PLANE_ROOT = Path("/Users/gaofeng/workspace/med-autogrant")
CURRENT_PROGRAM_PATH = CONTROL_PLANE_ROOT / ".omx" / "context" / "CURRENT_PROGRAM.md"


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
            "lineage_fields": list(final_package.get("lineage", {}).keys()),
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

    for field in ("grant_run_id", "workspace_id", "draft_id", "freeze_manifest", "lineage", "checkpoint_summary"):
        if field not in final_package:
            raise WorkspaceStateError(f"final package 缺少字段: {field}")

    return final_package


def _read_program_id() -> str:
    try:
        text = CURRENT_PROGRAM_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"读取 CURRENT_PROGRAM 失败: {CURRENT_PROGRAM_PATH}") from exc

    match = re.search(r"- program_id:\s*`([^`]+)`", text)
    if match is None:
        raise WorkspaceStateError(f"CURRENT_PROGRAM 缺少可解析的 program_id: {CURRENT_PROGRAM_PATH}")
    return match.group(1)


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
