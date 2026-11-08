from __future__ import annotations

from pathlib import Path
from typing import Any

from med_autogrant.control_plane import (
    read_current_program_contract as _read_current_program_contract_from_contract,
    read_program_id as _read_program_id_from_contract,
    runtime_state_display_path,
)
from med_autogrant.domain_entry_contract import build_domain_entry_contract
from med_autogrant.schema_loader import SchemaStore
from med_autogrant.workspace_types import WorkspaceStateError

from ..shared import (
    AUTHOR_SIDE_ROUTE_IDS,
    CURRENT_PROGRAM_RELATIVE_PATH,
    EXECUTOR_ROUTING_CONTRACT_VERSION,
    GENERATED_SESSION_RESUME_SURFACE_REF,
    GENERATED_SESSION_SURFACE_REF,
    HOSTED_CONTRACT_BUNDLE_SCHEMA_FILE,
    HOSTED_CONTRACT_SCHEMA_FILES,
    SCHEMA_INDEX_RELATIVE_PATH,
)
from . import scholar_binding
from .route_contracts import build_author_side_route_contract
from .schema_validation import validate_contract_schema


def read_program_id(*, repo_root: Path | None = None) -> str:
    return _read_program_id_from_contract(repo_root=repo_root)


def read_current_program_contract(*, repo_root: Path | None = None) -> dict[str, Any]:
    return _read_current_program_contract_from_contract(repo_root=repo_root)


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


def build_runtime_substrate_contract(*, current_program_contract: dict[str, Any]) -> dict[str, Any]:
    runtime_binding = current_program_contract.get("runtime_binding")
    if not isinstance(runtime_binding, dict):
        raise WorkspaceStateError("CURRENT_PROGRAM contract 缺少字段: runtime_binding")

    return {
        "runtime_owner": require_nonempty_string(
            runtime_binding,
            "runtime_provider_owner",
            context="CURRENT_PROGRAM contract runtime_binding",
        ),
        "task_runtime_owner": require_nonempty_string(
            runtime_binding,
            "task_runtime_owner",
            context="CURRENT_PROGRAM contract runtime_binding",
        ),
        "runtime_substrate": require_nonempty_string(
            runtime_binding,
            "runtime_substrate",
            context="CURRENT_PROGRAM contract runtime_binding",
        ),
        "stage_executor_owner": require_nonempty_string(
            runtime_binding,
            "stage_executor",
            context="CURRENT_PROGRAM contract runtime_binding",
        ),
        "current_owner_line": require_nonempty_string(
            runtime_binding,
            "current_owner_line",
            context="CURRENT_PROGRAM contract runtime_binding",
        ),
        "active_phase": require_nonempty_string(
            runtime_binding,
            "active_phase",
            context="CURRENT_PROGRAM contract runtime_binding",
        ),
        "active_tranche": require_nonempty_string(
            runtime_binding,
            "active_tranche",
            context="CURRENT_PROGRAM contract runtime_binding",
        ),
        "provenance_oracle": require_nonempty_string(
            runtime_binding,
            "provenance_oracle",
            context="CURRENT_PROGRAM contract runtime_binding",
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
            "execute-strategy-authoring-pass",
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
        "scholar_skill_binding_contract": scholar_binding.read_scholar_skill_binding_contract(),
    }


def require_nonempty_string(payload: dict[str, Any], field: str, *, context: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise WorkspaceStateError(f"{context} 缺少合法字段: {field}")
    return value


def directory_display_path(*segments: str) -> str:
    return runtime_state_display_path(*segments).rstrip("/") + "/"
