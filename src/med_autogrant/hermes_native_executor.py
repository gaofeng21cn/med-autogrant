from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable

from med_autogrant.workspace_types import WorkspaceStateError


ConfigLoader = Callable[[], dict[str, Any]]
AgentFactory = Callable[..., Any]


def read_hermes_agent_contract(
    env: dict[str, str] | None = None,
    *,
    config_loader: ConfigLoader | None = None,
) -> dict[str, Any]:
    resolved_env = env or os.environ
    resolved_config_loader = config_loader or _load_hermes_config
    config = resolved_config_loader() if callable(resolved_config_loader) else {}
    model_config = config.get("model", {})
    agent_config = config.get("agent", {})

    default_model = _normalize_model_default(model_config)
    default_provider = _normalize_config_string(model_config.get("provider"))
    default_base_url = _normalize_config_string(model_config.get("base_url"))
    default_api_mode = _normalize_config_string(model_config.get("api_mode"))
    default_reasoning_effort = _normalize_config_string(agent_config.get("reasoning_effort"))

    model_override = _parse_optional_override(resolved_env.get("MED_AUTOGRANT_HERMES_MODEL"))
    provider_override = _parse_optional_override(resolved_env.get("MED_AUTOGRANT_HERMES_PROVIDER"))
    base_url_override = _parse_optional_override(resolved_env.get("MED_AUTOGRANT_HERMES_BASE_URL"))
    api_mode_override = _parse_optional_override(resolved_env.get("MED_AUTOGRANT_HERMES_API_MODE"))
    reasoning_override = _parse_optional_override(resolved_env.get("MED_AUTOGRANT_HERMES_REASONING_EFFORT"))

    model = model_override or default_model
    if model is None:
        raise WorkspaceStateError(
            "Hermes-native proof 缺少可执行 model：请在 `~/.hermes/config.yaml` 里提供 `model.default`，"
            "或显式设置 `MED_AUTOGRANT_HERMES_MODEL`。"
        )

    reasoning_effort = reasoning_override or default_reasoning_effort
    return {
        "entrypoint": "run_agent.AIAgent.run_conversation",
        "full_agent_loop_required": True,
        "model": model,
        "provider": provider_override or default_provider,
        "base_url": base_url_override or default_base_url,
        "api_mode": api_mode_override or default_api_mode,
        "reasoning_effort": reasoning_effort,
        "reasoning_config": _parse_reasoning_effort(reasoning_effort or ""),
        "resolution": {
            "model": "env_override" if model_override else "local_config",
            "reasoning_effort": "env_override" if reasoning_override else "local_config",
        },
    }


def run_hermes_agent_exec(
    prompt: str,
    *,
    cwd: str | Path,
    env: dict[str, str] | None = None,
    config_loader: ConfigLoader | None = None,
    agent_factory: AgentFactory | None = None,
) -> dict[str, Any]:
    contract = read_hermes_agent_contract(env, config_loader=config_loader)
    resolved_cwd = Path(cwd).expanduser().resolve()
    if not resolved_cwd.exists():
        raise WorkspaceStateError(f"Hermes-native executor working directory 不存在: {resolved_cwd}")

    events: list[dict[str, Any]] = []

    def _append_event(event_type: str, **payload: Any) -> None:
        events.append({"type": event_type, **payload})

    resolved_agent_factory = agent_factory or _load_ai_agent_factory()
    agent = resolved_agent_factory(
        quiet_mode=True,
        model=contract["model"],
        provider=contract["provider"] or None,
        base_url=contract["base_url"] or None,
        api_mode=contract["api_mode"] or None,
        reasoning_config=contract["reasoning_config"],
        skip_context_files=True,
        skip_memory=True,
        tool_start_callback=lambda _tcid, name, args: _append_event(
            "tool_start",
            tool=name,
            args=args,
        ),
        tool_complete_callback=lambda _tcid, name, _args, result: _append_event(
            "tool_complete",
            tool=name,
            result_preview=_preview_text(result),
        ),
        step_callback=lambda step_index, previous_tools: _append_event(
            "step",
            step=step_index,
            prev_tool_count=len(previous_tools),
        ),
        status_callback=lambda event_name, message: _append_event(
            "status",
            event=event_name,
            message=_preview_text(message),
        ),
        reasoning_callback=lambda text: _append_event(
            "reasoning",
            preview=_preview_text(text),
        ),
    )

    try:
        result = agent.run_conversation(prompt)
    finally:
        close = getattr(agent, "close", None)
        if callable(close):
            close()

    if not isinstance(result, dict):
        raise WorkspaceStateError("Hermes-native executor 返回值必须是 object。")

    completed = bool(result.get("completed"))
    tool_start_events = [event for event in events if event["type"] == "tool_start"]
    tool_complete_events = [event for event in events if event["type"] == "tool_complete"]
    if not tool_start_events or not tool_complete_events:
        raise WorkspaceStateError("Hermes-native proof 未触发任何工具事件，不接受 chat-only 结果。")
    if not completed:
        raise WorkspaceStateError("Hermes-native proof 未完成完整 agent loop，不能作为 critique executor 证明。")

    payload = _parse_json_object(result.get("final_response"))
    agent_api_mode = _normalize_config_string(getattr(agent, "api_mode", None)) or contract["api_mode"]
    proof = {
        "proof_kind": "full_agent_loop_aiaagent",
        "full_agent_loop_proved": True,
        "session_id": _normalize_config_string(getattr(agent, "session_id", None)),
        "api_calls": _require_nonnegative_int(result, "api_calls", context="Hermes-native result"),
        "tool_call_count": len(tool_start_events),
        "event_count": len(events),
        "event_stream": events,
        "provider_reasoning_status": _resolve_reasoning_status(
            provider=contract["provider"],
            api_mode=agent_api_mode,
        ),
    }
    return {
        "payload": payload,
        "contract": contract,
        "proof": proof,
    }


def _normalize_model_default(payload: Any) -> str | None:
    if isinstance(payload, dict):
        value = payload.get("default")
    else:
        value = payload
    return _parse_optional_override(value)


def _normalize_config_string(value: Any) -> str | None:
    text = str(value or "").strip()
    return text or None


def _parse_optional_override(value: Any) -> str | None:
    return _normalize_config_string(value)


def _parse_json_object(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    if not isinstance(payload, str) or not payload.strip():
        raise WorkspaceStateError("Hermes-native executor 未返回 final JSON message。")

    stripped = payload.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()

    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise WorkspaceStateError("Hermes-native executor final response 不是合法 JSON object。") from exc
    if not isinstance(parsed, dict):
        raise WorkspaceStateError("Hermes-native executor final response 顶层必须是 JSON object。")
    return parsed


def _require_nonnegative_int(payload: dict[str, Any], key: str, *, context: str) -> int:
    value = payload.get(key)
    if not isinstance(value, int) or value < 0:
        raise WorkspaceStateError(f"{context} 缺少合法的 `{key}`。")
    return value


def _preview_text(value: Any, limit: int = 240) -> str:
    text = str(value)
    return text if len(text) <= limit else f"{text[:limit]}..."


def _resolve_reasoning_status(*, provider: str | None, api_mode: str | None) -> str:
    if provider == "custom" and api_mode == "chat_completions":
        return "unproven_custom_chat_completions"
    return "not_proved"


def _load_hermes_config() -> dict[str, Any]:
    from hermes_cli.config import load_config

    return load_config()


def _parse_reasoning_effort(value: str) -> dict[str, Any]:
    text = str(value or "").strip()
    try:
        from hermes_constants import parse_reasoning_effort
    except ModuleNotFoundError:
        return {
            "enabled": bool(text),
            "effort": text,
        }
    parsed = parse_reasoning_effort(value)
    if isinstance(parsed, dict) and parsed:
        return parsed
    return {
        "enabled": bool(text),
        "effort": text,
    }


def _load_ai_agent_factory() -> AgentFactory:
    from run_agent import AIAgent

    return AIAgent
