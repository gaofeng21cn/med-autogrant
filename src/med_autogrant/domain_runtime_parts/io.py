from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from med_autogrant.artifact_bundle_validation import _validate_required_artifact_bundle_fields
from med_autogrant.control_plane import resolve_runtime_state_root
from med_autogrant.final_package_validation import SUPPORTED_FINAL_PACKAGE_VERSION
from med_autogrant.workspace import materialize_workspace_surfaces
from med_autogrant.workspace_types import WorkspaceFileError, WorkspaceStateError

from .contracts import validate_schema_payload as _validate_schema_payload
from .shared import (
    FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE,
)

def _read_active_draft_id(document: dict[str, Any]) -> str | None:
    selection = document.get("current_selection") or {}
    draft_id = selection.get("active_draft_id")
    return draft_id if isinstance(draft_id, str) and draft_id.strip() else None

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
    return final_package

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
