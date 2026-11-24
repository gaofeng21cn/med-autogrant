from __future__ import annotations

from typing import Any

from med_autogrant.domain_entry_contract import (
    SERVICE_SAFE_ENTRY_ADAPTER,
    SERVICE_SAFE_ENTRY_SURFACE_KIND,
)
from med_autogrant.workspace_types import WorkspaceStateError

from ..shared import (
    AUTHOR_SIDE_ROUTE_IDS,
    EXECUTOR_ROUTE_OWNER,
    EXECUTOR_ROUTING_CONTRACT_SCHEMA_FILE,
    EXECUTOR_ROUTING_CONTRACT_VERSION,
)
from .schema_validation import validate_contract_schema


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


AUTHOR_SIDE_ROUTE_COMMANDS = {
    "direction_screening": "execute-strategy-authoring-pass",
    "question_refinement": "execute-strategy-authoring-pass",
    "argument_building": "execute-strategy-authoring-pass",
    "fit_alignment": "execute-strategy-authoring-pass",
    "outline": "execute-strategy-authoring-pass",
    "drafting": "execute-strategy-authoring-pass",
    "critique": "execute-critique-pass",
    "revision": "execute-revision-pass",
    "frozen": "execute-freeze-pass",
    "artifact_bundle": "build-artifact-bundle",
    "final_package": "build-final-package",
    "hosted_contract_bundle": "build-hosted-contract-bundle",
}


def build_author_side_route_command(route_id: str, *, source_stage: str) -> str:
    resolved_route_id = require_known_route_id(route_id, context="executor routing route")
    execution_command = AUTHOR_SIDE_ROUTE_COMMANDS.get(resolved_route_id)
    if execution_command is None:
        raise WorkspaceStateError(
            f"未找到已 landed 的 author-side route command: {resolved_route_id}",
            lifecycle_stage=source_stage,
        )
    return execution_command


def build_author_side_route_contract(route_id: str, *, source_stage: str) -> dict[str, Any]:
    resolved_route_id = require_known_route_id(route_id, context="executor routing route")
    return {
        "route_id": resolved_route_id,
        "route_status": "landed",
        "executor_owner": EXECUTOR_ROUTE_OWNER,
        "execution_surface": {
            "surface_kind": SERVICE_SAFE_ENTRY_SURFACE_KIND,
            "entry_adapter": SERVICE_SAFE_ENTRY_ADAPTER,
            "command": build_author_side_route_command(resolved_route_id, source_stage=source_stage),
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


def require_nonempty_route_id(value: Any, *, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"{context} 缺少合法 route_id")
    return value.strip()


def require_known_route_id(value: Any, *, context: str) -> str:
    resolved_value = require_nonempty_route_id(value, context=context)
    if resolved_value not in AUTHOR_SIDE_ROUTE_IDS:
        raise WorkspaceStateError(f"{context} 不支持 route_id: {resolved_value}")
    return resolved_value
