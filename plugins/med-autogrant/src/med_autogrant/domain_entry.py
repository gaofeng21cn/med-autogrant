from __future__ import annotations

from typing import Any, Mapping

from med_autogrant.domain_entry_catalog import SERVICE_SAFE_DOMAIN_COMMANDS
from med_autogrant.domain_runtime_parts.authoring_surface import execute_freeze_pass
from med_autogrant.domain_runtime_parts.handoff_surfaces import (
    build_artifact_bundle,
    execute_argument_building_pass,
    execute_critique_pass,
    execute_direction_screening_pass,
    execute_drafting_pass,
    execute_fit_alignment_pass,
    execute_outline_pass,
    execute_question_refinement_pass,
    execute_revision_pass,
    execute_strategy_authoring_pass,
)
from med_autogrant.domain_runtime_parts.package_surface import (
    build_final_package,
    build_hosted_contract_bundle,
    build_submission_ready_package,
)
from med_autogrant.domain_runtime_parts.quality_surface import (
    grant_quality_closure_dossier,
    grant_quality_diff,
    grant_quality_scorecard,
)
from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime
from med_autogrant.workspace_types import WorkspaceStateError


class MedAutoGrantDomainEntry:
    """给 CLI 与未来 service caller 共用的结构化 domain entry。"""

    def __init__(
        self,
        *,
        runtime: MagDomainRuntime | None = None,
    ) -> None:
        self._runtime = runtime or MagDomainRuntime()

    def dispatch(self, request: Mapping[str, Any]) -> dict[str, Any]:
        return dispatch_domain_request(request, runtime=self._runtime)


def dispatch_domain_request(
    request: Mapping[str, Any],
    *,
    runtime: MagDomainRuntime | None = None,
) -> dict[str, Any]:
    command = _require_command(request)

    spec = SERVICE_SAFE_DOMAIN_COMMANDS.get(command)
    if spec is None:
        raise WorkspaceStateError(f"不支持的 domain entry command: {command}")

    missing_fields = [
        field_name
        for field_name in spec.required_fields
        if not _has_structured_value(request.get(field_name))
    ]
    if missing_fields:
        raise WorkspaceStateError(
            f"domain entry `{command}` 缺少必填字段: {', '.join(missing_fields)}"
        )

    runtime_kwargs: dict[str, Any] = {}
    for field_name in spec.required_fields + spec.optional_fields:
        field_value = request.get(field_name)
        if field_value is not None:
            runtime_kwargs[field_name] = field_value

    payload = _dispatch_runtime_command(
        runtime or MagDomainRuntime(),
        command=command,
        runtime_kwargs=runtime_kwargs,
    )
    if not isinstance(payload, dict):
        raise WorkspaceStateError(f"domain entry `{command}` 返回值必须是 object。")
    if "command" not in payload:
        return {"command": command, **payload}
    return payload


def _dispatch_runtime_command(
    runtime: MagDomainRuntime,
    *,
    command: str,
    runtime_kwargs: dict[str, Any],
) -> dict[str, Any]:
    if command == "validate-workspace":
        return MagDomainRuntime.validate_workspace(runtime, **runtime_kwargs)
    if command == "summarize-workspace":
        return MagDomainRuntime.summarize_workspace(runtime, **runtime_kwargs)
    if command == "grant-intake-audit":
        return MagDomainRuntime.grant_intake_audit(runtime, **runtime_kwargs)
    if command == "grant-evidence-grounding":
        return MagDomainRuntime.grant_evidence_grounding(runtime, **runtime_kwargs)
    if command == "grant-quality-scorecard":
        return grant_quality_scorecard(runtime, **runtime_kwargs)
    if command == "grant-quality-closure-dossier":
        return grant_quality_closure_dossier(runtime, **runtime_kwargs)
    if command == "grant-quality-diff":
        return grant_quality_diff(runtime, **runtime_kwargs)
    if command == "discover-funding-opportunities":
        return MagDomainRuntime.discover_funding_opportunities(runtime, **runtime_kwargs)
    if command == "refresh-funding-opportunities-cache":
        return MagDomainRuntime.refresh_funding_opportunities_cache(runtime, **runtime_kwargs)
    if command == "select-project-profile":
        return MagDomainRuntime.select_project_profile(runtime, **runtime_kwargs)
    if command == "initialize-intake-workspace":
        return MagDomainRuntime.initialize_intake_workspace(runtime, **runtime_kwargs)
    if command == "next-step":
        return MagDomainRuntime.next_step(runtime, **runtime_kwargs)
    if command == "critique-summary":
        return MagDomainRuntime.critique_summary(runtime, **runtime_kwargs)
    if command == "stage-route-report":
        return MagDomainRuntime.stage_route_report(runtime, **runtime_kwargs)
    if command == "execute-strategy-authoring-pass":
        return execute_strategy_authoring_pass(runtime, **runtime_kwargs)
    if command == "execute-direction-screening-pass":
        return execute_direction_screening_pass(runtime, **runtime_kwargs)
    if command == "execute-question-refinement-pass":
        return execute_question_refinement_pass(runtime, **runtime_kwargs)
    if command == "execute-argument-building-pass":
        return execute_argument_building_pass(runtime, **runtime_kwargs)
    if command == "execute-fit-alignment-pass":
        return execute_fit_alignment_pass(runtime, **runtime_kwargs)
    if command == "execute-outline-pass":
        return execute_outline_pass(runtime, **runtime_kwargs)
    if command == "execute-drafting-pass":
        return execute_drafting_pass(runtime, **runtime_kwargs)
    if command == "build-artifact-bundle":
        return build_artifact_bundle(runtime, **runtime_kwargs)
    if command == "execute-critique-pass":
        return execute_critique_pass(runtime, **runtime_kwargs)
    if command == "execute-revision-pass":
        return execute_revision_pass(runtime, **runtime_kwargs)
    if command == "execute-freeze-pass":
        return execute_freeze_pass(runtime, **runtime_kwargs)
    if command == "build-final-package":
        return build_final_package(runtime, **runtime_kwargs)
    if command == "build-hosted-contract-bundle":
        return build_hosted_contract_bundle(runtime, **runtime_kwargs)
    if command == "build-submission-ready-package":
        return build_submission_ready_package(runtime, **runtime_kwargs)
    raise WorkspaceStateError(f"不支持的 domain entry command: {command}")


def _require_command(request: Mapping[str, Any]) -> str:
    if not isinstance(request, Mapping):
        raise WorkspaceStateError("domain entry request 必须是 mapping。")

    command = request.get("command")
    if not isinstance(command, str) or not command.strip():
        raise WorkspaceStateError("domain entry request 缺少 command。")
    return command


def _has_structured_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True
