# 2026-04-13：Hermes-native critique experimental proof Tombstone

状态：`historical tombstone / superseded`

## 这次真正落了什么

本次落地的不是默认执行器替换，而是：

- 在现有 `execute-critique-pass` 上新增一条显式 opt-in 的 experimental proof lane
- 调用方式固定为 `executor_kind = hermes_native_proof`
- 默认 concrete executor 仍然是 `Codex CLI autonomous`

也就是说，当前真实状态是：

- `execute-critique-pass`
  - 默认：`Codex CLI autonomous`
  - experimental proof：`Hermes-native full agent loop`

## 当前调用链

当 caller 显式传入 `executor_kind = hermes_native_proof` 时，当前真实调用链是：

- `execute-critique-pass`
- `MedAutoGrantDomainEntry.dispatch(...)`
- `HermesRuntimeSubstrate.execute_critique_pass(..., executor_kind="hermes_native_proof")`
- `build_critique_execution_document(..., executor_kind="hermes_native_proof")`
- `run_hermes_agent_exec(...)`
- `read_hermes_agent_contract(...)`
- `run_agent.AIAgent.run_conversation(...)`

当前 proof lane 不走：

- repo-local 小步 planner 先拆任务再逐步喂模型
- 单次 `chat completion`
- chat relay

## 当前配置解析口径

当前 `Hermes-native` proof lane 不在 repo 内固定 model pin，而是显式读取本机 Hermes 配置：

- `~/.hermes/config.yaml`
  - `model.default`
  - `model.provider`
  - `model.base_url`
  - `model.api_mode`
  - `agent.reasoning_effort`

只有显式设置以下环境变量时才会覆盖本机 Hermes 默认：

- `MED_AUTOGRANT_HERMES_MODEL`
- `MED_AUTOGRANT_HERMES_PROVIDER`
- `MED_AUTOGRANT_HERMES_BASE_URL`
- `MED_AUTOGRANT_HERMES_API_MODE`
- `MED_AUTOGRANT_HERMES_REASONING_EFFORT`

当前实现之所以必须显式读 local Hermes config，是因为直接裸实例化 `AIAgent()` 时，provider 侧可能不会自动补齐 `model.default`；如果不给 `model`，实际请求会 fail-closed。

## 当前 fail-closed 门槛

当前 experimental proof lane 只有在以下条件同时满足时才承认自己是 `Hermes-native`：

1. 成功实例化 `run_agent.AIAgent`
2. `run_conversation(...)` 完整跑完
3. 运行过程中确实出现工具事件
4. 至少出现一组 `tool_start / tool_complete`
5. 最终返回合法 JSON object

只要缺失其中任一项，当前实现就直接报错，不会静默退化成普通 chat。

## 当前输出真相

当 proof lane 成功时，`critique_execution.executor` 会写出：

- `kind = hermes_native_full_agent_loop`
- `mode = experimental_proof`
- `entrypoint = run_agent.AIAgent.run_conversation`
- `model / provider / api_mode / reasoning_effort`
- `full_agent_loop_proved = true`
- `session_id`
- `api_calls`
- `tool_call_count`
- `event_count`
- `event_stream`
- `reasoning_semantics_status`

其中 `event_stream` 当前来自真实 `AIAgent` 回调，而不是 repo-local 伪造的 chat log。

## 归档边界

这条 lane 当时只证明了一件事：

- `Med Auto Grant critique` 已经具备一条真实可跑的 `Hermes-native full agent loop` 备选 proof route

这条 lane 还没有证明：

- 它已经等价于默认 `Codex CLI autonomous`
- `custom + chat_completions` 路径下 provider 侧 reasoning 语义已经被 repo 级证明

因此这份 tombstone 只能写成：

- `FULL_AGENT_LOOP_PRESENT_BUT_NOT_YET_EQUIVALENT_TO_CODEX`
- 若本机 Hermes 仍是 `provider=custom + api_mode=chat_completions`，则 `PROVIDER_REASONING_NOT_PROVED_KEEP_DEFAULT`

而不能写成：

- `Hermes-native 已替代默认 critique executor`
- `Hermes-native 已经 repo-verified 等价于 Codex CLI`

当前活跃真相入口改为：

- `docs/specs/2026-04-13-critique-codex-cli-executor-current-truth.md`
