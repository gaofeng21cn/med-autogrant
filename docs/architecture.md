# 架构概览

## 主链路

当前主链路是 `CLI-first + real upstream Hermes-Agent runtime substrate`：

`operator / agent / future gateway caller -> CLI or MedAutoGrantDomainEntry -> upstream Hermes session substrate -> MedAutoGrant domain logic -> critique / export / stage surfaces -> durable artifacts`

formal-entry matrix 继续固定为：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。

## 入口与执行

- CLI 仍是唯一 formal entry：`validate-workspace`、`summarize-workspace`、`next-step`、`critique-summary`、`stage-route-report`。
- `src/med_autogrant/domain_entry.py` 现在提供结构化 `MedAutoGrantDomainEntry`，把 CLI 与 future gateway caller 收口到同一条 service-safe command contract。
- `src/med_autogrant/upstream_hermes.py` 负责真实 upstream 依赖探测、runtime root 决议与基于 `hermes_state.SessionDB` 的 attempt ledger。
- `run-local` 与 `resume-local` 继续以 journal 串联多次 pass，但 attempt index 现在来自真实上游 Hermes session substrate。
- 对 valid workspace，Hermes session handle 继续沿用 `grant_run_id`；对 `validation_failed` path，只允许使用 journal-scoped substrate session handle 持续 durability，不得伪造新的 domain `grant_run_id`。
- `src/med_autogrant/hermes_runtime.py` 现在应被理解为 repo-side domain adapter / orchestrator，而不是 runtime substrate owner。
- `src/med_autogrant/local_runtime.py` 只保留 compatibility bridge 责任。
- `execute-revision-pass`、`build-artifact-bundle`、`build-final-package`、`build-hosted-contract-bundle` 继续由 repo-side domain logic 持有输入加载、identity guard 与输出 handoff。
- `build-hosted-contract-bundle` 继续把 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract` 一并导出，作为 future host 需要兼容的托管友好 handoff contract。
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
