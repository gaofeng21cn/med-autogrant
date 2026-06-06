# Critique Codex CLI Executor Current Truth

Owner: `Med Auto Grant`
Purpose: `critique_executor_vocabulary_active_spec`
State: `active_current_spec`
Machine boundary: 本文是人读 active spec，只冻结 critique executor vocabulary 与 Codex CLI route。当前产品状态、runtime owner、App/workbench 和 evidence gate 继续归核心五件套、active gap plan、contracts/schema/source 与 `contracts/runtime-program/current-program.json`。
Date: `2026-04-13`

## Activation Status

- Phase: `P4 mature direct grant product entry`
- Active tranche: `P4.D full grant authoring executor landing`
- Status: `landed / current truth`

## Goal

冻结 `critique` route 已经 landed 的当前真相，并把 executor vocabulary 收口成：

- 默认输入/输出：`codex_cli`
- 显式 receipt lane：`hermes_agent`

这条 current truth 解决的是：

- `critique` 不再继续写成 `pending / handoff-required`
- external caller / `product_entry` / hosted bundle 能看到同一份 landed route truth
- 默认模型与默认 reasoning 继续继承本机 Codex 默认

## Landed Facts

### 1. `critique` route 现在已经是 landed command surface

当前 route contract 对 `critique` 的 landed 口径是：

- `route_id = critique`
- `route_status = landed`
- `execution_surface.command = execute-critique-pass`
- `handoff_contract_kind = service-safe-domain-entry-command`

这同时适用于：

- `product_entry.executor_routing_contract.current_stage_route`
- `build-product-entry.product_entry.executor_routing_contract.current_stage_route`
- `drafting -> critique` 的 `recommended_executor_route`
- `revision(completed revised switch) -> critique` 的 `recommended_executor_route`

也就是说，`critique` 已经和 `revision / artifact_bundle / final_package / hosted_contract_bundle` 一起进入当前 landed route catalog。

### 2. landed critique 当前固定走 `Codex CLI executor`

当前 `execute-critique-pass` 的实现链路是：

- `MagDomainRuntime.execute_critique_pass(...)`
- `build_critique_execution_document(...)`
- `run_codex_exec(...)`
- `codex exec --json --ephemeral ...`

`critique_execution.executor` 会显式写出：

- `kind = codex_cli`
- `model = model_selection`
- `reasoning_effort = reasoning_selection`

这是当前 docs / contract 对执行器身份的事实来源。

`executor_kind` 输入面也已经收口成同一 vocabulary：

- 省略时默认走 `codex_cli`
- 显式 `codex_cli` 仍然走默认路由
- 显式 `hermes_agent` 进入 OPL-backed receipt lane
- 其他值 fail-closed

### 3. 默认模型与默认 reasoning 都继承本机 Codex 默认

`read_codex_cli_contract()` 当前默认值是：

- `DEFAULT_CODEX_MODEL = inherit_local_codex_default`
- `DEFAULT_CODEX_REASONING_EFFORT = inherit_local_codex_default`

因此在未显式设置下面环境变量时：

- `MED_AUTOGRANT_CODEX_MODEL`
- `MED_AUTOGRANT_CODEX_REASONING_EFFORT`

`run_codex_exec(...)` 不会固定 repo-local `gpt-5.4 / xhigh`，而是跟随本机 Codex 默认配置；只有显式覆盖时，才会把 override 传进 `codex exec`。

### 4. 当前 landed executor 的默认 authoring path 由 Codex CLI 持有

当前成立的是：

- `Codex CLI` 是当前第一公民 concrete executor
- `critique` 的默认 concrete executor 已统一到 `Codex CLI`
- `Hermes-Agent` 只作为显式 `hermes_agent` receipt lane，经 OPL generic Agent Executor Adapter 接入

当前不成立的是：

- `critique` 的默认 concrete executor 已经离开 `Codex CLI`
- MAG runtime、authoring executor、grant truth 或 quality verdict 由显式 receipt lane 持有

只有带 session substrate、route orchestration、domain mutation、durable state transition 与 OPL `AgentExecutionReceipt` 风格 proof 的 full agent loop 才算显式 receipt lane；chat relay / prompt relay / 单次 chat completion 不算。

### 5. critique pending handoff contract 退为历史资料

`2026-04-12` 的 critique pending handoff contract 只保留为历史 superseded note。

当前 route 真相已经不是：

- `critique-product-status-required`

而是：

- landed `execute-critique-pass`
- `Codex CLI executor`
- default model / reasoning inherit local Codex default
- 旧 proof alias 已移到 `docs/history/specs/` tombstone

## Verification

本 vocabulary 收口至少应覆盖：

- `tests/test_critique_executor.py`
- `tests/test_domain_runtime.py`
- `tests/test_domain_entry.py`
- `tests/test_program_control_surfaces.py`
- `tests/test_repository_hygiene.py`

并验证：

- `critique` 在 route contract 中是 landed
- `execute-critique-pass` 会通过 `run_codex_exec(...)` 调用 `codex exec`
- `critique_execution.executor` 会写出 `kind = codex_cli`
- `executor_kind = hermes_agent` 仍会进入 explicit receipt lane
- 退役 executor alias 会 fail-closed
- `model_selection / reasoning_selection` 默认是 `inherit_local_codex_default`

## Honest Boundary

这条 current truth 只说明：

- `critique` route 已经 landed
- 当前默认 concrete executor 是 `Codex CLI`
- 默认模型与默认 reasoning 都继承本机 Codex 默认
- `hermes_agent` 仍然只是显式 receipt lane
- 非默认 executor 只承诺可接入、可回执、可审计、fail-closed，不承诺效果等价
- 其他 executor 值会 fail-closed

明确不表示以下内容已经成立或需要恢复：

- 不表示 `critique` 的默认 executor 已经离开 `Codex CLI`
- 不表示这份文档单独定义 full authoring route catalog；那部分真相应以 `2026-04-13-full-grant-authoring-executor-current-truth.md` 为准
- 不表示 actual hosted runtime 已完成
