from __future__ import annotations

from pathlib import Path

from med_autogrant.control_plane import read_program_id, resolve_runtime_state_root
from med_autogrant.domain_runtime_parts.contracts import build_author_side_route_command
from med_autogrant.public_cli import public_cli_command
from med_autogrant.workspace_types import WorkspaceStateError


def _build_route_execution_command(
    *,
    route_id: str,
    input_path: Path,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> str:
    resolved_input_path = input_path.expanduser().resolve()
    command = build_author_side_route_command(route_id, source_stage=route_id)
    output_path = _build_runtime_route_output_path(
        route_id=route_id,
        grant_run_id=grant_run_id,
        workspace_id=workspace_id,
        draft_id=draft_id,
    )
    if route_id not in {"final_package", "hosted_contract_bundle"}:
        return public_cli_command(
            command,
            "--input",
            str(resolved_input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "final_package":
        artifact_bundle_path = _build_runtime_route_output_path(
            route_id="artifact_bundle",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            draft_id=draft_id,
        )
        return public_cli_command(
            command,
            "--input",
            str(resolved_input_path),
            "--artifact-bundle",
            str(artifact_bundle_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    if route_id == "hosted_contract_bundle":
        final_package_path = _build_runtime_route_output_path(
            route_id="final_package",
            grant_run_id=grant_run_id,
            workspace_id=workspace_id,
            draft_id=draft_id,
        )
        return public_cli_command(
            command,
            "--final-package",
            str(final_package_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        )
    raise WorkspaceStateError(f"grant_user_loop 不支持 landed route command: {route_id}")


def _build_runtime_route_output_path(
    *,
    route_id: str,
    grant_run_id: str,
    workspace_id: str,
    draft_id: str | None,
) -> Path:
    output_file = {
        "direction_screening": "direction-screening-workspace.json",
        "question_refinement": "question-refinement-workspace.json",
        "argument_building": "argument-building-workspace.json",
        "fit_alignment": "fit-alignment-workspace.json",
        "outline": "outline-workspace.json",
        "drafting": "drafting-workspace.json",
        "critique": "critique-workspace.json",
        "revision": "revision-workspace.json",
        "frozen": "frozen-workspace.json",
        "artifact_bundle": "artifact-bundle.json",
        "final_package": "final-package.json",
        "hosted_contract_bundle": "hosted-contract-bundle.json",
    }.get(route_id)
    if output_file is None:
        raise WorkspaceStateError(f"grant_user_loop 不支持 runtime output path route: {route_id}")

    program_id = _require_runtime_path_segment(read_program_id(), field_name="program_id")
    return (
        resolve_runtime_state_root()
        / "reports"
        / program_id
        / _require_runtime_path_segment(grant_run_id, field_name="grant_run_id")
        / _require_runtime_path_segment(workspace_id, field_name="workspace_id")
        / _require_runtime_path_segment(draft_id or "no-draft", field_name="draft_id")
        / output_file
    )


def _require_runtime_path_segment(value: str, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceStateError(f"grant_user_loop runtime output path 缺少合法字段: {field_name}")
    resolved_value = value.strip()
    if resolved_value in {".", ".."} or "/" in resolved_value or "\\" in resolved_value:
        raise WorkspaceStateError(f"grant_user_loop runtime output path 字段不能包含路径分隔符: {field_name}")
    return resolved_value
