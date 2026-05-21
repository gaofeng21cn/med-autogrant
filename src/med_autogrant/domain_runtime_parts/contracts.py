from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.control_plane import (
    CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH,
    read_current_program_contract as _read_current_program_contract_from_contract,
    read_program_id as _read_program_id_from_contract,
    resolve_current_program_contract_path,
    runtime_state_display_path,
)
from med_autogrant.domain_entry_contract import (
    SERVICE_SAFE_ENTRY_ADAPTER,
    SERVICE_SAFE_ENTRY_SURFACE_KIND,
    build_domain_entry_contract,
)
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.schema_subset_validator import SchemaSubsetValidator
from med_autogrant.runtime_defaults import (
    DEFAULT_EXECUTOR_OWNER,
    DEFAULT_RUNTIME_OWNER,
    DEFAULT_RUNTIME_SUBSTRATE,
    DEFAULT_TASK_RUNTIME_OWNER,
)
from med_autogrant.workspace_types import WorkspaceStateError

from .shared import (
    AUTHOR_SIDE_ROUTE_IDS,
    CURRENT_PROGRAM_RELATIVE_PATH,
    GENERATED_SESSION_RESUME_SURFACE_REF,
    GENERATED_SESSION_SURFACE_REF,
    EXECUTOR_ROUTE_OWNER,
    EXECUTOR_ROUTING_CONTRACT_SCHEMA_FILE,
    EXECUTOR_ROUTING_CONTRACT_VERSION,
    HOSTED_CONTRACT_BUNDLE_SCHEMA_FILE,
    HOSTED_CONTRACT_SCHEMA_FILES,
    SCHEMA_INDEX_RELATIVE_PATH,
)


def read_program_id(*, repo_root: Path | None = None) -> str:
    return _read_program_id_from_contract(repo_root=repo_root)


def read_current_program_contract(*, repo_root: Path | None = None) -> dict[str, Any]:
    return _read_current_program_contract_from_contract(repo_root=repo_root)


def validate_contract_schema(
    payload: dict[str, Any],
    *,
    schema_file: str,
    context: str,
    grant_run_id: str | None = None,
    workspace_id: str | None = None,
    lifecycle_stage: str | None = None,
) -> None:
    issues = SchemaSubsetValidator(SchemaStore()).validate(payload, schema_file)
    if not issues:
        return
    detail = "; ".join(f"{issue.path}: {issue.message}" for issue in issues[:5])
    if len(issues) > 5:
        detail = f"{detail}; 其余 {len(issues) - 5} 项略"
    raise WorkspaceStateError(
        f"{context} schema 校验失败: {detail}",
        errors=issues,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )


def validate_schema_payload(
    payload: dict[str, Any],
    *,
    schema_file: str,
    context: str,
) -> None:
    validate_contract_schema(
        payload,
        schema_file=schema_file,
        context=context,
    )


def validate_executor_routing_contract(
    contract: dict[str, Any],
    *,
    current_stage: str,
    recommended_next_stage: str,
    include_route_catalog: bool,
    grant_run_id: str | None = None,
    workspace_id: str | None = None,
    lifecycle_stage: str | None = None,
) -> None:
    validate_contract_schema(
        contract,
        schema_file=EXECUTOR_ROUTING_CONTRACT_SCHEMA_FILE,
        context="executor_routing_contract",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )

    expected_current_stage_route = build_stage_route_contract(
        current_stage,
        source_stage=current_stage,
    )
    if contract.get("current_stage_route") != expected_current_stage_route:
        raise WorkspaceStateError(
            "executor_routing_contract.current_stage_route 与当前冻结 route truth 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    expected_recommended_route = build_stage_route_contract(
        recommended_next_stage,
        source_stage=current_stage,
    )
    if contract.get("recommended_executor_route") != expected_recommended_route:
        raise WorkspaceStateError(
            "executor_routing_contract.recommended_executor_route 与当前冻结 route truth 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )

    if not include_route_catalog:
        if "author_side_route_catalog" in contract:
            raise WorkspaceStateError(
                "executor_routing_contract 不允许在当前 surface 携带 author_side_route_catalog。",
                errors=[],
                grant_run_id=grant_run_id,
                workspace_id=workspace_id,
                lifecycle_stage=lifecycle_stage,
            )
        return

    expected_route_catalog = [
        build_author_side_route_contract(route_id, source_stage=route_id)
        for route_id in AUTHOR_SIDE_ROUTE_IDS
    ]
    if contract.get("author_side_route_catalog") != expected_route_catalog:
        raise WorkspaceStateError(
            "executor_routing_contract.author_side_route_catalog 与当前冻结 route matrix 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def validate_hosted_contract_bundle(
    bundle: dict[str, Any],
    *,
    grant_run_id: str,
    workspace_id: str,
    lifecycle_stage: str | None,
) -> None:
    validate_contract_schema(
        bundle,
        schema_file=HOSTED_CONTRACT_BUNDLE_SCHEMA_FILE,
        context="hosted_contract_bundle",
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        lifecycle_stage=lifecycle_stage,
    )
    if bundle.get("domain_entry_contract") != build_domain_entry_contract():
        raise WorkspaceStateError(
            "hosted_contract_bundle.domain_entry_contract 与当前冻结 entry contract 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if bundle.get("schema_contract") != build_schema_contract():
        raise WorkspaceStateError(
            "hosted_contract_bundle.schema_contract 与当前冻结 schema registry 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )
    if bundle.get("authoring_contract") != build_hosted_authoring_contract():
        raise WorkspaceStateError(
            "hosted_contract_bundle.authoring_contract 与当前冻结 author-side route matrix 不一致。",
            errors=[],
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            lifecycle_stage=lifecycle_stage,
        )


def build_executor_routing_contract(
    *,
    current_stage: str,
    recommended_next_stage: str,
    include_route_catalog: bool = False,
) -> dict[str, Any]:
    contract = {
        "contract_version": EXECUTOR_ROUTING_CONTRACT_VERSION,
        "current_stage_route": build_stage_route_contract(
            current_stage,
            source_stage=current_stage,
        ),
        "recommended_executor_route": build_stage_route_contract(
            recommended_next_stage,
            source_stage=current_stage,
        ),
    }
    if include_route_catalog:
        contract["author_side_route_catalog"] = [
            build_author_side_route_contract(route_id, source_stage=route_id)
            for route_id in AUTHOR_SIDE_ROUTE_IDS
        ]
    return contract


def build_stage_route_contract(stage: str, *, source_stage: str) -> dict[str, Any]:
    resolved_stage = require_known_route_id(stage, context="executor routing stage")
    return build_author_side_route_contract(resolved_stage, source_stage=source_stage)


def build_author_side_route_contract(route_id: str, *, source_stage: str) -> dict[str, Any]:
    resolved_route_id = require_known_route_id(route_id, context="executor routing route")
    execution_command = {
        "direction_screening": "execute-direction-screening-pass",
        "question_refinement": "execute-question-refinement-pass",
        "argument_building": "execute-argument-building-pass",
        "fit_alignment": "execute-fit-alignment-pass",
        "outline": "execute-outline-pass",
        "drafting": "execute-drafting-pass",
        "critique": "execute-critique-pass",
        "revision": "execute-revision-pass",
        "frozen": "execute-freeze-pass",
        "artifact_bundle": "build-artifact-bundle",
        "final_package": "build-final-package",
        "hosted_contract_bundle": "build-hosted-contract-bundle",
    }.get(resolved_route_id)
    if execution_command is None:
        raise WorkspaceStateError(
            f"未找到已 landed 的 author-side route command: {resolved_route_id}",
            lifecycle_stage=source_stage,
        )
    return {
        "route_id": resolved_route_id,
        "route_status": "landed",
        "executor_owner": EXECUTOR_ROUTE_OWNER,
        "execution_surface": {
            "surface_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
            "entry_adapter": SERVICE_SAFE_ENTRY_ADAPTER,
            "command": execution_command,
        },
        "handoff_contract_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
    }


def build_service_safe_domain_surface(command: str) -> dict[str, str]:
    resolved_command = require_nonempty_route_id(command, context="service-safe domain surface command")
    return {
        "surface_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
        "entry_adapter": SERVICE_SAFE_ENTRY_ADAPTER,
        "command": resolved_command,
    }


def build_runtime_substrate_contract(*, current_program_contract: dict[str, Any]) -> dict[str, Any]:
    runtime_owner = current_program_contract.get("runtime_owner")
    if not isinstance(runtime_owner, dict):
        raise WorkspaceStateError("CURRENT_PROGRAM contract 缺少字段: runtime_owner")

    return {
        "runtime_owner": DEFAULT_RUNTIME_OWNER,
        "task_runtime_owner": DEFAULT_TASK_RUNTIME_OWNER,
        "runtime_substrate": DEFAULT_RUNTIME_SUBSTRATE,
        "stage_executor_owner": DEFAULT_EXECUTOR_OWNER,
        "current_owner_line": require_nonempty_string(
            runtime_owner,
            "current_owner_line",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "active_phase": require_nonempty_string(
            runtime_owner,
            "active_phase",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "active_tranche": require_nonempty_string(
            runtime_owner,
            "active_tranche",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "provenance_oracle": require_nonempty_string(
            runtime_owner,
            "provenance_oracle",
            context="CURRENT_PROGRAM contract runtime_owner",
        ),
        "repo_tracked_current_program_contract": CURRENT_PROGRAM_RELATIVE_PATH.as_posix(),
    }


def build_runtime_state_contract() -> dict[str, Any]:
    return {
        "root": runtime_state_display_path(),
        "session_state_owner": "one-person-lab",
        "generated_session_surface_ref": GENERATED_SESSION_SURFACE_REF,
        "generated_resume_surface_ref": GENERATED_SESSION_RESUME_SURFACE_REF,
        "logs_root": directory_display_path("logs"),
        "reports_root": directory_display_path("reports", "<program_id>"),
        "prompts_root": directory_display_path("prompts"),
        "handoff_state_root": directory_display_path("handoff_state"),
        "non_repo_tracked": True,
    }


def build_operator_contract() -> dict[str, Any]:
    return {
        "canonical_audit_surfaces": [
            "validate-workspace",
            "summarize-workspace",
            "grant-intake-audit",
            "grant-evidence-grounding",
            "grant-quality-scorecard",
            "grant-quality-closure-dossier",
            "grant-quality-diff",
            "next-step",
            "critique-summary",
            "stage-route-report",
        ],
        "canonical_export_surfaces": [
            "execute-direction-screening-pass",
            "execute-question-refinement-pass",
            "execute-argument-building-pass",
            "execute-fit-alignment-pass",
            "execute-outline-pass",
            "execute-drafting-pass",
            "execute-critique-pass",
            "execute-revision-pass",
            "execute-freeze-pass",
            "build-artifact-bundle",
            "build-final-package",
            "build-hosted-contract-bundle",
            "build-submission-ready-package",
        ],
        "checkpoint_aggregation_surface": "stage-route-report",
    }


def build_schema_contract() -> dict[str, Any]:
    schema_index = SchemaStore().load_schema_index()
    return {
        "schema_version": schema_index["schema_version"],
        "schema_index_path": SCHEMA_INDEX_RELATIVE_PATH,
        "aggregate_root_schema": schema_index["aggregate_root"],
        "contract_schema_files": list(HOSTED_CONTRACT_SCHEMA_FILES),
    }


def build_hosted_authoring_contract() -> dict[str, Any]:
    return {
        "route_contract_version": EXECUTOR_ROUTING_CONTRACT_VERSION,
        "route_catalog_kind": "author_side_route_catalog",
        "author_side_route_catalog": [
            build_author_side_route_contract(route_id, source_stage=route_id)
            for route_id in AUTHOR_SIDE_ROUTE_IDS
        ],
    }


def require_nonempty_string(payload: dict[str, Any], field: str, *, context: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field}")
    return value


def require_nonempty_route_id(value: Any, *, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少合法 route_id")
    return value.strip()


def require_known_route_id(value: Any, *, context: str) -> str:
    resolved_value = require_nonempty_route_id(value, context=context)
    if resolved_value not in AUTHOR_SIDE_ROUTE_IDS:
        raise WorkspaceStateError(f"{context} 不支持 route_id: {resolved_value}")
    return resolved_value


def directory_display_path(*segments: str) -> str:
    return runtime_state_display_path(*segments).rstrip("/") + "/"


def resolve_control_plane_current_program_path(
    *,
    repo_root: Path | None = None,
    worktree_list_text: str | None = None,
) -> Path:
    del worktree_list_text
    return resolve_current_program_contract_path(repo_root=repo_root)


def read_git_worktree_list(*, repo_root: Path) -> str:
    del repo_root
    raise WorkspaceStateError("项目级 .runtime-program 已退役；不再通过 git worktree 列表解析 control-plane root。")


def select_control_plane_current_program_path(
    *,
    repo_root: Path,
    worktree_list_text: str,
) -> Path:
    del repo_root
    del worktree_list_text
    raise WorkspaceStateError("项目级 .runtime-program 已退役；不再通过 main worktree 回退解析 CURRENT_PROGRAM。")


def parse_git_worktree_list_porcelain(worktree_list_text: str) -> list[dict[str, str]]:
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


CURRENT_PROGRAM_RELATIVE_PATH = CURRENT_PROGRAM_CONTRACT_RELATIVE_PATH
