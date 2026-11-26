from __future__ import annotations

import json
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Annotated, Any, Literal

from jsonschema import Draft202012Validator, FormatChecker
from med_autogrant._opl_helpers.json_io import (
    ExistingJsonIdentityMismatch,
    JsonObjectReadError,
    guard_existing_json_identity,
    read_json_object,
    write_json_object_atomic,
)
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from med_autogrant.artifact_bundle_validation import (
    _validate_required_artifact_bundle_fields,
)
from med_autogrant.control_plane import resolve_runtime_state_root
from med_autogrant.final_package_validation import SUPPORTED_FINAL_PACKAGE_VERSION
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.workspace import materialize_workspace_surfaces
from med_autogrant.workspace_types import (
    ValidationIssue,
    WorkspaceFileError,
    WorkspaceStateError,
)

from .shared import FUNDING_LANDSCAPE_CACHE_SCHEMA_FILE


class _ArtifactBundleEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow", strict=True)

    bundle_kind: Literal["artifact_bundle"]
    grant_run_id: Any = None
    workspace_id: Any = None
    draft_id: Any = None


class _FinalPackageEnvelope(BaseModel):
    model_config = ConfigDict(extra="allow", strict=True)

    package_kind: Literal["final_package"]
    package_version: Annotated[
        int,
        Field(
            strict=True,
            ge=SUPPORTED_FINAL_PACKAGE_VERSION,
            le=SUPPORTED_FINAL_PACKAGE_VERSION,
        ),
    ]
    grant_run_id: Any
    workspace_id: Any
    draft_id: Any
    lifecycle_stage: Any
    freeze_manifest: Any
    lineage: Any
    checkpoint_summary: Any


_JSON_SCHEMA_FORMAT_CHECKER = FormatChecker()


@_JSON_SCHEMA_FORMAT_CHECKER.checks("date-time", ValueError)
def _check_iso8601_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if "T" not in value and "t" not in value:
        raise ValueError("must be an ISO-8601 date-time string")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("date-time must include timezone offset")
    return True


@lru_cache(maxsize=4)
def _schema_registry(schema_root: Path) -> Registry[Any]:
    resources: list[tuple[str, Resource[Any]]] = []
    for schema_path in sorted(schema_root.glob("*.schema.json")):
        contents = json.loads(schema_path.read_text(encoding="utf-8"))
        resource = Resource.from_contents(contents, default_specification=DRAFT202012)
        schema_id = contents.get("$id")
        if isinstance(schema_id, str) and schema_id:
            resources.append((schema_id, resource))
        resources.append((schema_path.name, resource))
    return Registry().with_resources(resources)


def _validate_json_schema_payload(
    payload: dict[str, Any],
    *,
    schema_file: str,
    context: str,
) -> None:
    store = SchemaStore()
    schema = store.load_json(schema_file)
    validator = Draft202012Validator(
        schema,
        registry=_schema_registry(store.root.resolve()),
        format_checker=_JSON_SCHEMA_FORMAT_CHECKER,
    )
    raw_errors = sorted(validator.iter_errors(payload), key=lambda item: [str(part) for part in item.path])
    if not raw_errors:
        return
    issues = [
        ValidationIssue(
            path=".".join(str(part) for part in err.path) or "$",
            message=err.message,
        )
        for err in raw_errors
    ]
    detail = "; ".join(f"{issue.path}: {issue.message}" for issue in issues[:5])
    if len(issues) > 5:
        detail = f"{detail}; 其余 {len(issues) - 5} 项略"
    raise WorkspaceStateError(f"{context} schema 校验失败: {detail}", errors=issues)


def _read_active_draft_id(document: dict[str, Any]) -> str | None:
    selection = document.get("current_selection") or {}
    draft_id = selection.get("active_draft_id")
    return draft_id if isinstance(draft_id, str) and draft_id.strip() else None


def _nested_value(payload: dict[str, Any], *path: str) -> Any:
    value: Any = payload
    for key in path:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _first_value(payload: dict[str, Any], *paths: tuple[str, ...]) -> Any:
    for path in paths:
        value = _nested_value(payload, *path)
        if value is not None:
            return value
    return None


def _guard_output_identity(
    output_path: Path,
    *,
    label: str,
    expected: dict[str, Any],
    project_identity: Any = None,
    grant_run_id: str | None = None,
    workspace_id: str | None = None,
    lifecycle_stage: str | None = None,
) -> None:
    try:
        guard_existing_json_identity(
            output_path,
            expected,
            project_identity=project_identity,
        )
    except JsonObjectReadError as exc:
        if exc.reason == "read_error":
            raise WorkspaceFileError(f"读取 {label} output 失败: {output_path}") from exc
        shape = (
            "顶层不是 JSON object"
            if exc.reason == "top_level_not_object"
            else "不是可校验的 JSON object"
        )
        raise WorkspaceStateError(
            f"{label} output identity 不匹配: {output_path} 已存在且{shape}。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc
    except ExistingJsonIdentityMismatch as exc:
        raise WorkspaceStateError(
            (
                f"{label} output identity 不匹配: {output_path} -> "
                f"{exc.observed} != {exc.expected}"
            ),
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc


def _guard_artifact_bundle_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    lifecycle_stage: str,
) -> None:
    _guard_output_identity(
        output_path,
        label="bundle",
        expected={
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
        },
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
    _guard_output_identity(
        output_path,
        label="revision",
        expected={
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "active_revision_plan_id": active_revision_plan_id,
        },
        project_identity=lambda payload: {
            "grant_run_id": payload.get("grant_run_id"),
            "workspace_id": payload.get("workspace_id"),
            "draft_id": _first_value(
                payload,
                ("draft_id",),
                ("current_selection", "active_draft_id"),
            ),
            "active_revision_plan_id": _first_value(
                payload,
                ("current_selection", "active_revision_plan_id"),
                ("revision_execution", "active_revision_plan_id"),
            ),
        },
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
    grant_run_id = workspace_document.get("grant_run_id")
    workspace_id = workspace_document.get("workspace_id")
    lifecycle_stage = workspace_document.get("lifecycle_stage")
    expected_selection = workspace_document.get("current_selection")
    if not isinstance(expected_selection, dict):
        expected_selection = {}
    expected_draft_id = draft_id if draft_id is not None else expected_selection.get("active_draft_id")
    _guard_output_identity(
        output_path,
        label="workspace",
        expected={
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "lifecycle_stage": lifecycle_stage,
            "draft_id": expected_draft_id,
            "current_selection": expected_selection,
        },
        project_identity=lambda payload: {
            "grant_run_id": payload.get("grant_run_id"),
            "workspace_id": payload.get("workspace_id"),
            "lifecycle_stage": payload.get("lifecycle_stage"),
            "draft_id": _first_value(
                payload,
                ("draft_id",),
                ("current_selection", "active_draft_id"),
            ),
            "current_selection": (
                payload.get("current_selection")
                if isinstance(payload.get("current_selection"), dict)
                else {}
            ),
        },
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

    try:
        envelope = _ArtifactBundleEnvelope.model_validate(artifact_bundle)
    except ValidationError as exc:
        raise WorkspaceStateError(
            f"artifact bundle kind 非法: {artifact_bundle.get('bundle_kind')}",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        ) from exc

    if (envelope.grant_run_id, envelope.workspace_id, envelope.draft_id) != (
        grant_run_id,
        workspace_id,
        draft_id,
    ):
        raise WorkspaceStateError(
            (
                "artifact bundle identity 不匹配: "
                f"{envelope.grant_run_id}/{envelope.workspace_id}/{envelope.draft_id} "
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

    try:
        envelope = _FinalPackageEnvelope.model_validate(final_package)
    except ValidationError as exc:
        first_loc = exc.errors()[0].get("loc", ())
        first_field = str(first_loc[0]) if first_loc else "package_kind"
        if first_field == "package_kind":
            raise WorkspaceStateError(f"final package kind 非法: {final_package.get('package_kind')}") from exc
        raise WorkspaceStateError(f"final package 缺少字段: {first_field}") from exc

    if envelope.package_version != SUPPORTED_FINAL_PACKAGE_VERSION:
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
    _guard_output_identity(
        output_path,
        label="final package",
        expected={
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
        },
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
    _guard_output_identity(
        output_path,
        label="hosted contract",
        expected={
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "program_id": program_id,
        },
        project_identity=lambda payload: {
            key: _first_value(payload, ("execution_identity", key), (key,))
            for key in ("grant_run_id", "workspace_id", "draft_id", "program_id")
        },
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
    )


def _guard_submission_ready_package_output_identity(
    output_path: Path,
    *,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str,
    program_id: str,
) -> None:
    _guard_output_identity(
        output_path,
        label="submission ready package",
        expected={
            "package_kind": "submission_ready_package",
            "grant_run_id": grant_run_id,
            "workspace_id": workspace_id,
            "draft_id": draft_id,
            "program_id": program_id,
        },
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
    )


def _write_hosted_contract_bundle_output(output_path: Path, hosted_contract_bundle: dict[str, Any]) -> None:
    _write_json_output(output_path, hosted_contract_bundle, label="hosted contract output")


def _write_artifact_bundle_output(output_path: Path, bundle: dict[str, Any]) -> None:
    _write_json_output(output_path, bundle, label="bundle output")


def _write_revised_workspace_output(output_path: Path, revised_workspace: dict[str, Any]) -> None:
    materialized_workspace = materialize_workspace_surfaces(revised_workspace)
    _write_json_output(output_path, materialized_workspace, label="revised workspace output")


def _write_final_package_output(output_path: Path, final_package: dict[str, Any]) -> None:
    _write_json_output(output_path, final_package, label="final package output")


def _write_submission_ready_package_output(
    output_path: Path,
    submission_ready_package: dict[str, Any],
) -> None:
    _write_json_output(
        output_path,
        submission_ready_package,
        label="submission ready package output",
    )


def _write_json_output(output_path: Path, payload: dict[str, Any], *, label: str) -> None:
    try:
        write_json_object_atomic(output_path, payload, ensure_ascii=False, indent=2)
    except OSError as exc:
        raise WorkspaceFileError(f"写入 {label} 失败: {output_path}") from exc


def _load_json_object(input_path: str | Path, *, context: str) -> dict[str, Any]:
    resolved_input_path = Path(input_path).expanduser().resolve()
    try:
        return read_json_object(resolved_input_path)
    except JsonObjectReadError as exc:
        if isinstance(exc.__cause__, FileNotFoundError):
            raise WorkspaceFileError(f"未找到 {context} 文件: {resolved_input_path}") from exc
        if exc.reason == "invalid_json":
            raise WorkspaceFileError(f"{context} JSON 解析失败: {resolved_input_path}") from exc
        if exc.reason == "top_level_not_object":
            raise WorkspaceFileError(f"{context} 顶层必须是 JSON object。") from exc
        raise WorkspaceFileError(f"读取 {context} 失败: {resolved_input_path}") from exc


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
    _validate_json_schema_payload(
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
