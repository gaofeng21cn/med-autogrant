# 架构概览

## 主链路

当前主链路是 `CLI-first + real upstream Hermes-Agent runtime substrate`：

`operator / agent / future gateway caller -> CLI or MedAutoGrantDomainEntry -> upstream Hermes session substrate -> MedAutoGrant domain logic -> critique / export / stage surfaces -> durable artifacts`

formal-entry matrix 继续固定为：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。

## 入口 taxonomy 与 OPL handoff

当前需要明确区分三层入口：

- `operator entry`
  - 给人类操作同事使用的命令、workspace 准备、检查与显式 gate
- `agent entry`
  - 给 `Codex`、Claude Code、OpenClaw 等 host-agent 使用的 `CLI` / `MedAutoGrantDomainEntry`
- `product entry`
  - 给最终用户直接进入的产品入口

当前真实状态是：前两层已经存在，第三层的轻量结构化 shell 也已经 landed，但成熟用户级前台仍未落地。

目标中的 domain 级链路应是：

`User -> Med Auto Grant Product Entry -> MedAutoGrantDomainEntry -> Hermes Kernel -> Med Auto Grant Domain Harness OS`

与 `OPL` 的家族级衔接应是：

`User -> OPL Product Entry -> OPL Gateway -> Hermes Kernel -> Domain Handoff -> Med Auto Grant Product Entry / MedAutoGrantDomainEntry`

`OPL -> Med Auto Grant` 的最小 handoff envelope 至少包括：

- `target_domain_id`
- `task_intent`
- `entry_mode`
- `workspace_locator`
- `runtime_session_contract`
- `return_surface_contract`

在这层公共 envelope 之上，grant 域继续补充 `workspace_id`、`draft_id`、`funding_call` 等 domain payload。

## Hermes substrate 与 grant executor 的分工

在当前架构里，`Hermes-Agent` 已经承担：

- session substrate
- runtime state / attempt ledger durability
- gateway / interrupt / resume / scheduling 这类长期在线 runtime 能力

`Med Auto Grant` 自己继续承担：

- workspace / draft / critique / revision / export 的 domain truth
- author-side object model 与 identity guard
- stage routing、artifact assembly 与 hosted handoff contract

因此，这里真实成立的是：

- runtime substrate owner 已切到上游 `Hermes-Agent`
- repo-side `domain logic + executor adapter` 仍然负责 grant authoring 流程

这不等于“所有单步 authoring 都已经迁成 Hermes-native executor”。
如果未来某条 critique / revision / export route 要替换执行器，也必须按 route 单独冻结 truth 与 proof，而不是因为 substrate 已统一就自动把 authoring semantics 一起改掉。

## 入口与执行

- CLI 仍是唯一 formal entry：`validate-workspace`、`summarize-workspace`、`next-step`、`critique-summary`、`stage-route-report`。
- `src/med_autogrant/domain_entry.py` 现在提供结构化 `MedAutoGrantDomainEntry`，把 CLI 与 future gateway caller 收口到同一条 service-safe command contract。
- `src/med_autogrant/product_entry.py` 现在提供 `MedAutoGrantProductEntry`；`build-product-entry` 通过 `MedAutoGrantDomainEntry` 复用已 landed 的 route / summary / runtime contract，统一生成 `direct` 与 `opl-handoff` 共用的 shared envelope，并显式导出 `executor_routing_contract`。
- `src/med_autogrant/upstream_hermes.py` 负责真实 upstream 依赖探测、runtime root 决议与基于 `hermes_state.SessionDB` 的 attempt ledger。
- `run-local` 与 `resume-local` 继续以 journal 串联多次 pass，但 attempt index 现在来自真实上游 Hermes session substrate。
- 对 valid workspace，Hermes session handle 继续沿用 `grant_run_id`；对 `validation_failed` path，只允许使用 journal-scoped substrate session handle 持续 durability，不得伪造新的 domain `grant_run_id`。
- `src/med_autogrant/hermes_runtime.py` 现在应被理解为 repo-side domain adapter / orchestrator，而不是 runtime substrate owner。
- `src/med_autogrant/local_runtime.py` 只保留 compatibility bridge 责任。
- `execute-revision-pass`、`build-artifact-bundle`、`build-final-package`、`build-hosted-contract-bundle` 继续由 repo-side domain logic 持有输入加载、identity guard 与输出 handoff。
- `build-hosted-contract-bundle` 继续把 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract` 一并导出，作为 future host 需要兼容的托管友好 handoff contract。
- 当前 author-side executor routing 继续按 route 单独冻结：`revision / artifact_bundle / final_package / hosted_contract_bundle` 已有 landed service-safe command surface，而所有非落地 stage 都只允许输出 `pending / handoff-required`。
- `direction_screening / question_refinement / argument_building / fit_alignment / outline / drafting / critique / frozen` 现在都会额外导出 route-specific `handoff_requirements`，并且只引用 `summarize-workspace / stage-route-report / critique-summary` 这些已存在的 domain surfaces。
- `critique-summary` 只有在 source workspace 已经位于 `critique / revision / frozen` review context 时才会被要求；`drafting -> critique` 这类 pre-review handoff 不能错误依赖它。
- 产物面：`build-artifact-bundle`、`execute-revision-pass`、`build-final-package`、`build-hosted-contract-bundle`。

## 数据与对象模型

- `schemas/v1/nsfc-workspace.schema.json` 定义 workspace 结构与关键对象。
- `grant_run_id` 仅作为执行句柄；`workspace_id`、`draft_id`、`program_id` 保持边界分离。
- `workspace.py`、`stage_router.py`、`revision_executor.py`、`final_package.py` 等继续承载 MedAutoGrant 的 author-side domain logic；它们不应被未来的上游 substrate 目标或当前 repo-local helper 偷换成新的 authoring semantics。

## 控制面与报告

- `contracts/runtime-program/current-program.json` 是 repo-tracked current-program pointer。
- 机器本地 runtime state 统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`，用于 session / log / report / prompt 等非仓库真相面状态。
- `run-local / resume-local` 的默认 local run journal 落点固定为 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/<grant_run_id>.json`；显式 `--journal` 仍可覆盖该默认值。
- Hermes substrate state db 默认落在 `$CODEX_HOME/projects/med-autogrant/runtime-state/hermes/state.db`；如需显式隔离，可通过 `MED_AUTOGRANT_HERMES_HOME` 覆盖。
- 旧 local host-agent runtime 只保留为 compatibility bridge / regression oracle，不再作为长期产品 runtime owner。

## 文档层次

- Public surface：`README*`、`docs/README*`、`docs/domain-positioning*`、`docs/mvp-scope*`。
- 核心骨架：`docs/project.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`、`docs/status.md`。
- Repo-tracked current truth 与 activation package：`docs/specs/**`。
- 历史规划：`docs/plans/**`；历史归档：`docs/history/**`。

## 历史边界

- OMX 已退场，仅保留历史入口。
