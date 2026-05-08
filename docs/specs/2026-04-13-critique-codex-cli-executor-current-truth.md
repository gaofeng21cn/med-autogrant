# Critique Codex CLI Executor Current Truth

Date: `2026-04-13`

## Activation Status

- Phase: `P4 mature direct grant product entry`
- Active tranche: `P4.D full grant authoring executor landing`
- Status: `landed / current truth`

## Goal

冻结 `critique` route 已经 landed 的当前真相，并把 executor vocabulary 收口成：

- 默认输入/输出：`codex_cli`
- 显式 proof lane：`hermes_agent`

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

- `runtime-run.stage_action_envelope.executor_routing_contract.current_stage_route`
- `build-product-entry.product_entry.executor_routing_contract.current_stage_route`
- `drafting -> critique` 的 `recommended_executor_route`
- `revision(completed revised switch) -> critique` 的 `recommended_executor_route`

也就是说，`critique` 已经和 `revision / artifact_bundle / final_package / hosted_contract_bundle` 一起进入当前 landed route catalog。

### 2. landed critique 当前固定走 `Codex CLI executor`

当前 `execute-critique-pass` 的实现链路是：

- `HermesRuntimeSubstrate.execute_critique_pass(...)`
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
- 显式 `hermes_agent` 进入 proof lane
- 其他值 fail-closed

### 3. 默认模型与默认 reasoning 都继承本机 Codex 默认

`read_codex_cli_contract()` 当前默认值是：

- `DEFAULT_CODEX_MODEL = inherit_local_codex_default`
- `DEFAULT_CODEX_REASONING_EFFORT = inherit_local_codex_default`

因此在未显式设置下面环境变量时：

- `MED_AUTOGRANT_CODEX_MODEL`
- `MED_AUTOGRANT_CODEX_REASONING_EFFORT`

`run_codex_exec(...)` 不会固定 repo-local `gpt-5.4 / xhigh`，而是跟随本机 Codex 默认配置；只有显式覆盖时，才会把 override 传进 `codex exec`。

### 4. 当前 landed executor 不把 Hermes-Agent 当作默认 authoring executor

当前成立的是：

- `Hermes-Agent` 已承担 runtime substrate / orchestration owner
- `critique` 的默认 concrete executor 已统一到 `Codex CLI`

当前不成立的是：

- `critique` 的默认 concrete executor 已经切换到 `Hermes-Agent`

只有带 session substrate、route orchestration、domain mutation 与 durable state transition 的 full agent loop 才算显式 proof lane；chat relay / prompt relay / 单次 chat completion 不算。

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
- `tests/test_hermes_runtime.py`
- `tests/test_domain_entry.py`
- `tests/test_program_control_surfaces.py`
- `tests/test_repository_hygiene.py`

并验证：

- `critique` 在 route contract 中是 landed
- `execute-critique-pass` 会通过 `run_codex_exec(...)` 调用 `codex exec`
- `critique_execution.executor` 会写出 `kind = codex_cli`
- `executor_kind = hermes_agent` 仍会进入 explicit proof lane
- 退役 executor alias 会 fail-closed
- `model_selection / reasoning_selection` 默认是 `inherit_local_codex_default`

## Honest Boundary

这条 current truth 只说明：

- `critique` route 已经 landed
- 当前默认 concrete executor 是 `Codex CLI`
- 默认模型与默认 reasoning 都继承本机 Codex 默认
- `hermes_agent` 仍然只是显式 proof lane
- 其他 executor 值会 fail-closed

它不意味着：

- `critique` 已经变成 Hermes-Agent default executor
- 这份文档单独定义了 full authoring route catalog；那部分真相应以 `2026-04-13-full-grant-authoring-executor-current-truth.md` 为准
- actual hosted runtime 已完成
