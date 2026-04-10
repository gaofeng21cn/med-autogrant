from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from med_autogrant.route_report import build_stage_route_report
from med_autogrant.workspace import WorkspaceFileError, WorkspaceStateError, _require_workspace_context


FINAL_PACKAGE_VERSION = 1
FINAL_PACKAGE_KIND = "final_package"
ALLOWED_CHECKPOINT_STATUSES = {"freeze_ready", "submission_frozen"}
REQUIRED_ARTIFACT_BUNDLE_OBJECT_FIELDS = (
    "selection",
    "manifest",
    "lineage",
    "bundle_summary",
    "artifacts",
)
REQUIRED_ARTIFACT_BUNDLE_NESTED_FIELDS = {
    "selection": (
        "selected_direction_id",
        "selected_question_id",
        "active_fit_mapping_id",
        "active_draft_id",
    ),
    "manifest": (
        "direction_id",
        "question_id",
        "argument_chain_id",
        "fit_mapping_id",
        "draft_id",
        "draft_version_label",
        "draft_status",
    ),
    "lineage": (
        "frozen_question_id",
        "argument_chain_id",
        "fit_mapping_id",
        "draft_id",
    ),
    "bundle_summary": (
        "outline_count",
        "section_count",
    ),
    "artifacts": (
        "selected_direction",
        "selected_question",
        "argument_chain",
        "fit_mapping",
        "draft_outline",
        "draft_sections",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_STRING_NESTED_FIELDS = {
    "selection": (
        "selected_direction_id",
        "selected_question_id",
        "active_fit_mapping_id",
        "active_draft_id",
    ),
    "manifest": (
        "direction_id",
        "question_id",
        "argument_chain_id",
        "fit_mapping_id",
        "draft_id",
        "draft_version_label",
        "draft_status",
    ),
    "lineage": (
        "frozen_question_id",
        "argument_chain_id",
        "fit_mapping_id",
        "draft_id",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_NONNEGATIVE_INT_NESTED_FIELDS = {
    "bundle_summary": (
        "outline_count",
        "section_count",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_LIST_NESTED_FIELDS = {
    "artifacts": (
        "draft_outline",
        "draft_sections",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_FIELDS = {
    "draft_outline": (
        "section_key",
        "section_title",
        "core_claim",
        "linked_object_ids",
    ),
    "draft_sections": (
        "section_key",
        "section_title",
        "text",
        "linked_object_ids",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_DICT_NESTED_FIELDS = {
    "artifacts": (
        "selected_direction",
        "selected_question",
        "argument_chain",
        "fit_mapping",
    ),
}
REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_PRIMARY_ID_FIELDS = {
    "selected_direction": "direction_id",
    "selected_question": "question_id",
    "argument_chain": "argument_chain_id",
    "fit_mapping": "fit_mapping_id",
}
REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_LINKAGE_ID_FIELDS = {
    "selected_question": (
        "parent_direction_id",
    ),
    "argument_chain": (
        "scientific_question_id",
    ),
    "fit_mapping": (
        "scientific_question_id",
        "argument_chain_id",
    ),
}


def build_final_package_payload(
    document: dict[str, Any],
    *,
    artifact_bundle_path: str | Path,
    output_path: str | Path,
) -> dict[str, Any]:
    context = _require_workspace_context(document)
    active_draft = context.active_draft
    active_revision_plan = context.active_revision_plan
    active_critique = context.active_critique
    route_report = build_stage_route_report(document)
    verification_checkpoint = route_report["verification_checkpoint"]
    checkpoint_status = verification_checkpoint["checkpoint_status"]
    if checkpoint_status not in ALLOWED_CHECKPOINT_STATUSES:
        raise WorkspaceStateError(
            (
                "checkpoint_status 必须为 freeze_ready 或 submission_frozen，"
                f"当前为 {checkpoint_status}。"
            ),
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    draft_status = active_draft.get("status")
    if draft_status not in {"revised", "frozen"}:
        raise WorkspaceStateError(
            "final package 只允许基于 revised / frozen 的 active draft 构建。",
            errors=[],
            grant_run_id=document.get("grant_run_id"),
            workspace_id=document.get("workspace_id"),
            lifecycle_stage=document.get("lifecycle_stage"),
        )

    artifact_bundle = _read_artifact_bundle(
        artifact_bundle_path,
        grant_run_id=document["grant_run_id"],
        workspace_id=document["workspace_id"],
        draft_id=active_draft["draft_id"],
        lifecycle_stage=document.get("lifecycle_stage"),
    )

    final_package = {
        "package_version": FINAL_PACKAGE_VERSION,
        "package_kind": FINAL_PACKAGE_KIND,
        "grant_run_id": document["grant_run_id"],
        "workspace_id": document["workspace_id"],
        "draft_id": active_draft["draft_id"],
        "lifecycle_stage": document["lifecycle_stage"],
        "freeze_manifest": {
            "draft_version_label": active_draft["version_label"],
            "draft_status": draft_status,
            "active_revision_plan_id": active_revision_plan["revision_plan_id"],
            "critique_id": active_critique["critique_id"],
            "checkpoint_status": checkpoint_status,
            "presubmission_frozen": bool(document.get("gates", {}).get("presubmission_frozen")),
        },
        "lineage": {
            "frozen_question_id": active_draft["frozen_question_id"],
            "selected_direction_id": context.selected_direction["direction_id"],
            "selected_question_id": context.selected_question["question_id"],
            "active_fit_mapping_id": context.active_fit_mapping["fit_mapping_id"],
            "draft_id": active_draft["draft_id"],
            "revision_plan_id": active_revision_plan["revision_plan_id"],
        },
        "checkpoint_summary": {
            "verification_checkpoint": verification_checkpoint,
            "checkpoint_status": checkpoint_status,
        },
        "export_summary": {
            "outline_count": len(active_draft.get("outline", [])),
            "section_count": len(active_draft.get("sections", [])),
            "artifact_count": len(artifact_bundle["artifacts"]),
        },
        "deliverables": {
            "artifact_bundle_manifest": deepcopy(artifact_bundle["manifest"]),
            "final_draft_outline": deepcopy(active_draft.get("outline", [])),
            "final_draft_sections": deepcopy(active_draft.get("sections", [])),
        },
    }

    resolved_output_path = Path(output_path).expanduser().resolve()
    _guard_output_identity(
        resolved_output_path,
        grant_run_id=final_package["grant_run_id"],
        workspace_id=final_package["workspace_id"],
        draft_id=final_package["draft_id"],
        lifecycle_stage=final_package["lifecycle_stage"],
    )
    _write_final_package(resolved_output_path, final_package)

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


def _validate_required_artifact_bundle_fields(
    artifact_bundle: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str | None,
) -> None:
    bundle_lifecycle_stage = artifact_bundle.get("lifecycle_stage")
    if not isinstance(bundle_lifecycle_stage, str) or not bundle_lifecycle_stage:
        raise WorkspaceStateError(
            "artifact bundle 缺少必填字段: lifecycle_stage",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    for field in REQUIRED_ARTIFACT_BUNDLE_OBJECT_FIELDS:
        value = artifact_bundle.get(field)
        if not isinstance(value, dict):
            raise WorkspaceStateError(
                f"artifact bundle 缺少必填字段: {field}",
                errors=[],
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            if required_field not in nested_payload:
                raise WorkspaceStateError(
                    f"artifact bundle {object_field} 缺少字段: {required_field}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_STRING_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            value = nested_payload.get(required_field)
            if not isinstance(value, str) or not value:
                raise WorkspaceStateError(
                    f"artifact bundle {object_field}.{required_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_NONNEGATIVE_INT_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            value = nested_payload.get(required_field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise WorkspaceStateError(
                    f"artifact bundle {object_field}.{required_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_LIST_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            value = nested_payload.get(required_field)
            if not isinstance(value, list):
                raise WorkspaceStateError(
                    f"artifact bundle {object_field}.{required_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    artifacts_payload = artifact_bundle["artifacts"]
    for list_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_LIST_ELEMENT_FIELDS.items():
        for index, value in enumerate(artifacts_payload[list_field]):
            if not isinstance(value, dict):
                raise WorkspaceStateError(
                    f"artifact bundle artifacts.{list_field}[{index}] 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )
            for required_field in required_fields:
                if required_field not in value:
                    raise WorkspaceStateError(
                        f"artifact bundle artifacts.{list_field}[{index}] 缺少字段: {required_field}",
                        errors=[],
                        grant_run_id=grant_run_id,
                        workspace_id=workspace_id,
                        lifecycle_stage=lifecycle_stage,
                    )

    for object_field, required_fields in REQUIRED_ARTIFACT_BUNDLE_DICT_NESTED_FIELDS.items():
        nested_payload = artifact_bundle[object_field]
        for required_field in required_fields:
            value = nested_payload.get(required_field)
            if not isinstance(value, dict):
                raise WorkspaceStateError(
                    f"artifact bundle {object_field}.{required_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )

    for object_field, nested_field in REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_PRIMARY_ID_FIELDS.items():
        value = artifacts_payload[object_field].get(nested_field)
        if not isinstance(value, str) or not value:
            raise WorkspaceStateError(
                f"artifact bundle artifacts.{object_field}.{nested_field} 非法: {value}",
                errors=[],
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )

    for object_field, nested_fields in REQUIRED_ARTIFACT_BUNDLE_ARTIFACT_OBJECT_LINKAGE_ID_FIELDS.items():
        for nested_field in nested_fields:
            value = artifacts_payload[object_field].get(nested_field)
            if not isinstance(value, str) or not value:
                raise WorkspaceStateError(
                    f"artifact bundle artifacts.{object_field}.{nested_field} 非法: {value}",
                    errors=[],
                    grant_run_id=grant_run_id,
                    workspace_id=workspace_id,
                    lifecycle_stage=lifecycle_stage,
                )


def _guard_output_identity(
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


def _write_final_package(output_path: Path, final_package: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(json.dumps(final_package, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise WorkspaceFileError(f"写入 final package output 失败: {output_path}") from exc
