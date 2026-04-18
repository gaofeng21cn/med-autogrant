from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from med_autogrant.hermes_runtime import HermesRuntimeSubstrate
from med_autogrant.upstream_hermes import probe_upstream_hermes
from med_autogrant.workspace import WorkspaceStateError


@dataclass(frozen=True)
class DomainEntryCommandSpec:
    runtime_method: str
    required_fields: tuple[str, ...]
    optional_fields: tuple[str, ...] = ()


SERVICE_SAFE_DOMAIN_COMMANDS: dict[str, DomainEntryCommandSpec] = {
    "validate-workspace": DomainEntryCommandSpec("validate_workspace", ("input_path",)),
    "summarize-workspace": DomainEntryCommandSpec("summarize_workspace", ("input_path",)),
    "next-step": DomainEntryCommandSpec("next_step", ("input_path",)),
    "critique-summary": DomainEntryCommandSpec("critique_summary", ("input_path",)),
    "stage-route-report": DomainEntryCommandSpec("stage_route_report", ("input_path",)),
    "runtime-run": DomainEntryCommandSpec("run_local", ("input_path",), ("journal_path",)),
    "runtime-resume": DomainEntryCommandSpec("resume_local", ("journal_path",)),
    "execute-direction-screening-pass": DomainEntryCommandSpec(
        "execute_direction_screening_pass",
        ("input_path", "output_path"),
    ),
    "execute-question-refinement-pass": DomainEntryCommandSpec(
        "execute_question_refinement_pass",
        ("input_path", "output_path"),
    ),
    "execute-argument-building-pass": DomainEntryCommandSpec(
        "execute_argument_building_pass",
        ("input_path", "output_path"),
    ),
    "execute-fit-alignment-pass": DomainEntryCommandSpec(
        "execute_fit_alignment_pass",
        ("input_path", "output_path"),
    ),
    "execute-outline-pass": DomainEntryCommandSpec(
        "execute_outline_pass",
        ("input_path", "output_path"),
    ),
    "execute-drafting-pass": DomainEntryCommandSpec(
        "execute_drafting_pass",
        ("input_path", "output_path"),
    ),
    "build-artifact-bundle": DomainEntryCommandSpec("build_artifact_bundle", ("input_path", "output_path")),
    "execute-critique-pass": DomainEntryCommandSpec(
        "execute_critique_pass",
        ("input_path", "output_path"),
        ("executor_kind",),
    ),
    "execute-revision-pass": DomainEntryCommandSpec("execute_revision_pass", ("input_path", "output_path")),
    "execute-freeze-pass": DomainEntryCommandSpec("execute_freeze_pass", ("input_path", "output_path")),
    "build-final-package": DomainEntryCommandSpec(
        "build_final_package",
        ("input_path", "artifact_bundle_path", "output_path"),
    ),
    "build-hosted-contract-bundle": DomainEntryCommandSpec(
        "build_hosted_contract_bundle",
        ("final_package_path", "output_path"),
    ),
    "build-submission-ready-package": DomainEntryCommandSpec(
        "build_submission_ready_package",
        ("input_path", "output_dir"),
    ),
}

COMPATIBILITY_COMMAND_ALIASES: dict[str, str] = {
    "run-local": "runtime-run",
    "resume-local": "runtime-resume",
}


class MedAutoGrantDomainEntry:
    """给 CLI 与未来 service caller 共用的结构化 domain entry。"""

    def __init__(
        self,
        *,
        runtime: HermesRuntimeSubstrate | None = None,
        probe: Callable[[], dict[str, Any]] | None = None,
    ) -> None:
        self._runtime = runtime or HermesRuntimeSubstrate()
        self._probe = probe or probe_upstream_hermes

    def dispatch(self, request: Mapping[str, Any]) -> dict[str, Any]:
        command = _normalize_command(_require_command(request))
        if command == "probe-upstream-hermes":
            return self._probe()

        spec = SERVICE_SAFE_DOMAIN_COMMANDS.get(command)
        if spec is None:
            raise WorkspaceStateError(f"不支持的 domain entry command: {command}")

        missing_fields = [
            field_name for field_name in spec.required_fields if not _has_structured_value(request.get(field_name))
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

        runtime_method = getattr(self._runtime, spec.runtime_method)
        payload = runtime_method(**runtime_kwargs)
        if not isinstance(payload, dict):
            raise WorkspaceStateError(f"domain entry `{command}` 返回值必须是 object。")
        if "command" not in payload:
            return {"command": command, **payload}
        return payload


def _normalize_command(command: str) -> str:
    return COMPATIBILITY_COMMAND_ALIASES.get(command, command)


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
