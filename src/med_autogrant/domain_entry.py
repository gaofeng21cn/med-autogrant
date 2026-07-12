from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping

from med_autogrant.domain_entry_catalog import SERVICE_SAFE_DOMAIN_COMMANDS
from med_autogrant.workspace_types import WorkspaceStateError

if TYPE_CHECKING:
    from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime


class MedAutoGrantDomainEntry:
    """给 CLI 与未来 service caller 共用的结构化 domain entry。"""

    def __init__(
        self,
        *,
        runtime: MagDomainRuntime | None = None,
    ) -> None:
        self._runtime = runtime or _build_runtime()

    def dispatch(self, request: Mapping[str, Any]) -> dict[str, Any]:
        command = _require_command(request)

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


def _require_command(request: Mapping[str, Any]) -> str:
    if not isinstance(request, Mapping):
        raise WorkspaceStateError("domain entry request 必须是 mapping。")

    command = request.get("command")
    if not isinstance(command, str) or not command.strip():
        raise WorkspaceStateError("domain entry request 缺少 command。")
    return command


def _build_runtime() -> MagDomainRuntime:
    from med_autogrant.domain_runtime_parts.substrate import MagDomainRuntime

    return MagDomainRuntime()


def _has_structured_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True
