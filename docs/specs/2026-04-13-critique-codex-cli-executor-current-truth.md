# Critique Executor Current Truth

Owner: `Med Auto Grant`
Purpose: `critique_executor_vocabulary_active_spec`
State: `active_current_spec`
Machine boundary: 本文冻结 critique 的 domain vocabulary 与 OPL executor-client boundary。机器接口归 source、contracts、OPL `AgentExecutionRequest` / `AgentExecutionReceipt` 和 runtime receipts。
Last reviewed: `2026-07-12`

## Current Route

`critique` 是 landed service-safe domain route：

- `route_id = critique`
- command = `execute-critique-pass`
- 默认 executor kind = `codex_cli`
- 显式非默认 lane = `hermes_agent`
- 其他 executor kind fail closed

`codex_cli` 是默认 concrete executor，但 Codex transport 不归 MAG。默认与非默认 executor 都通过 `opl_framework.executor_client.run_agent_execution_request` 进入 OPL Runway。

## Owner Boundary

OPL 持有：

- `opl executor run --request`
- Codex / Hermes 等 concrete executor discovery 与 subprocess
- timeout、process-group cleanup、JSON event/receipt envelope
- canonical `AgentExecutionReceipt`

MAG 持有：

- grant critique prompt 与 policy/persona
- `executor_kind` allow-list
- `domain_stage_closeout_packet` contract
- `mentor_critique` / `revision_plan` domain output normalization
- grant quality evidence、owner metadata 和 workspace mutation

MAG 不读取 Codex config，不声明 model/reasoning override 环境变量，不 spawn `codex exec`，也不从 stdout 或 final-message 文件恢复 domain output。

## Typed Closeout

executor 必须返回 canonical receipt，其中 `closeout_packet` 为：

```json
{
  "surface_kind": "domain_stage_closeout_packet",
  "route_id": "critique",
  "domain_output_kind": "mag_critique_output",
  "domain_output": {
    "mentor_critique": {},
    "revision_plan": {}
  }
}
```

缺少 receipt、executor kind 不一致、非零 exit code、closeout kind/route 不一致或 domain output 非 object 时，MAG fail closed；不得回退到 repo-local Codex transport。

## Verification

- `tests/test_critique_executor.py`
- `tests/test_ai_first_quality_boundary.py`
- `tests/test_authoring_executor.py`
- OPL standard-agent conformance / default-caller readback
- source scan必须保持 repo-local Codex/OPL subprocess transport为 0

这些结构与行为验证不证明 live grant ready、quality ready、provider long-soak 或 production readiness。
