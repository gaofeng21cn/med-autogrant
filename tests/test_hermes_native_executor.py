from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


class HermesNativeExecutorContractTest(unittest.TestCase):
    def test_read_hermes_agent_contract_resolves_local_config_defaults(self) -> None:
        from med_autogrant.hermes_native_executor import read_hermes_agent_contract

        contract = read_hermes_agent_contract(
            env={},
            config_loader=lambda: {
                "model": {
                    "default": "gpt-5.4",
                    "provider": "custom",
                    "base_url": "https://gflabtoken.cn/v1",
                    "api_mode": "chat_completions",
                },
                "agent": {
                    "reasoning_effort": "xhigh",
                },
            },
        )

        self.assertEqual(contract["entrypoint"], "run_agent.AIAgent.run_conversation")
        self.assertTrue(contract["full_agent_loop_required"])
        self.assertEqual(contract["model"], "gpt-5.4")
        self.assertEqual(contract["provider"], "custom")
        self.assertEqual(contract["base_url"], "https://gflabtoken.cn/v1")
        self.assertEqual(contract["api_mode"], "chat_completions")
        self.assertEqual(contract["reasoning_effort"], "xhigh")
        self.assertEqual(contract["reasoning_config"], {"enabled": True, "effort": "xhigh"})
        self.assertEqual(contract["resolution"], {"model": "local_config", "reasoning_effort": "local_config"})

    def test_read_hermes_agent_contract_keeps_explicit_env_overrides(self) -> None:
        from med_autogrant.hermes_native_executor import read_hermes_agent_contract

        contract = read_hermes_agent_contract(
            env={
                "MED_AUTOGRANT_HERMES_MODEL": "gpt-5.5",
                "MED_AUTOGRANT_HERMES_PROVIDER": "openai-codex",
                "MED_AUTOGRANT_HERMES_BASE_URL": "https://api.example.test/v1",
                "MED_AUTOGRANT_HERMES_API_MODE": "codex_responses",
                "MED_AUTOGRANT_HERMES_REASONING_EFFORT": "high",
            },
            config_loader=lambda: {
                "model": {
                    "default": "gpt-5.4",
                    "provider": "custom",
                    "base_url": "https://gflabtoken.cn/v1",
                    "api_mode": "chat_completions",
                },
                "agent": {
                    "reasoning_effort": "xhigh",
                },
            },
        )

        self.assertEqual(contract["model"], "gpt-5.5")
        self.assertEqual(contract["provider"], "openai-codex")
        self.assertEqual(contract["base_url"], "https://api.example.test/v1")
        self.assertEqual(contract["api_mode"], "codex_responses")
        self.assertEqual(contract["reasoning_effort"], "high")
        self.assertEqual(contract["reasoning_config"], {"enabled": True, "effort": "high"})
        self.assertEqual(contract["resolution"], {"model": "env_override", "reasoning_effort": "env_override"})


class HermesNativeExecutorRunTest(unittest.TestCase):
    def test_run_hermes_agent_exec_requires_full_agent_loop_with_tool_events(self) -> None:
        from med_autogrant.hermes_native_executor import run_hermes_agent_exec

        class FakeAgent:
            init_kwargs: dict[str, object] | None = None

            def __init__(self, **kwargs) -> None:
                type(self).init_kwargs = kwargs
                self.session_id = "hermes-session-test"
                self.api_mode = kwargs.get("api_mode")

            def run_conversation(self, user_message: str) -> dict[str, object]:
                self.init_kwargs["step_callback"](1, [])
                self.init_kwargs["tool_start_callback"]("tool-1", "read_file", {"path": "/tmp/workspace.json"})
                self.init_kwargs["tool_complete_callback"](
                    "tool-1",
                    "read_file",
                    {"path": "/tmp/workspace.json"},
                    {"content": '{"grant_run_id":"grant-run-test"}'},
                )
                self.init_kwargs["step_callback"](2, [{"name": "read_file", "result": "ok"}])
                return {
                    "completed": True,
                    "api_calls": 2,
                    "final_response": '{"mentor_critique": {}, "revision_plan": {}}',
                    "provider": self.init_kwargs.get("provider"),
                    "model": self.init_kwargs.get("model"),
                }

            def close(self) -> None:
                return None

        result = run_hermes_agent_exec(
            "{}",
            cwd=REPO_ROOT,
            config_loader=lambda: {
                "model": {
                    "default": "gpt-5.4",
                    "provider": "custom",
                    "base_url": "https://gflabtoken.cn/v1",
                    "api_mode": "chat_completions",
                },
                "agent": {
                    "reasoning_effort": "xhigh",
                },
            },
            agent_factory=FakeAgent,
        )

        self.assertEqual(result["payload"], {"mentor_critique": {}, "revision_plan": {}})
        self.assertEqual(result["contract"]["model"], "gpt-5.4")
        self.assertEqual(FakeAgent.init_kwargs["model"], "gpt-5.4")
        self.assertEqual(FakeAgent.init_kwargs["provider"], "custom")
        self.assertEqual(FakeAgent.init_kwargs["api_mode"], "chat_completions")
        self.assertEqual(FakeAgent.init_kwargs["reasoning_config"], {"enabled": True, "effort": "xhigh"})
        self.assertEqual(result["proof"]["proof_kind"], "full_agent_loop_aiaagent")
        self.assertTrue(result["proof"]["full_agent_loop_proved"])
        self.assertEqual(result["proof"]["session_id"], "hermes-session-test")
        self.assertEqual(result["proof"]["tool_call_count"], 1)
        self.assertEqual(result["proof"]["event_count"], 4)
        self.assertEqual(result["proof"]["provider_reasoning_status"], "unproven_custom_chat_completions")

    def test_run_hermes_agent_exec_fails_closed_when_no_tool_loop_happens(self) -> None:
        from med_autogrant.hermes_native_executor import run_hermes_agent_exec
        from med_autogrant.workspace import WorkspaceStateError

        class ChatOnlyAgent:
            def __init__(self, **kwargs) -> None:
                self.session_id = "hermes-session-chat-only"
                self.api_mode = kwargs.get("api_mode")

            def run_conversation(self, user_message: str) -> dict[str, object]:
                return {
                    "completed": True,
                    "api_calls": 1,
                    "final_response": '{"mentor_critique": {}, "revision_plan": {}}',
                    "provider": "custom",
                    "model": "gpt-5.4",
                }

            def close(self) -> None:
                return None

        with self.assertRaisesRegex(WorkspaceStateError, "未触发任何工具事件"):
            run_hermes_agent_exec(
                "{}",
                cwd=REPO_ROOT,
                config_loader=lambda: {
                    "model": {
                        "default": "gpt-5.4",
                        "provider": "custom",
                        "base_url": "https://gflabtoken.cn/v1",
                        "api_mode": "chat_completions",
                    },
                    "agent": {
                        "reasoning_effort": "xhigh",
                    },
                },
                agent_factory=ChatOnlyAgent,
            )
