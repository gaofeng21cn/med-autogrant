# 架构概览

## 主链路

当前主链路是本地 `CLI-first` runtime：

`operator / agent -> CLI -> repo-local runtime helper -> MedAutoGrant domain logic -> critique / export / stage surfaces -> durable artifacts`

formal-entry matrix 继续固定为：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。

## 入口与执行

- CLI 是唯一正式入口：`validate-workspace`、`summarize-workspace`、`next-step`、`critique-summary`、`stage-route-report`。
- 当前 repo-local runtime helper 负责 runtime dispatch、workspace/final-package 输入加载、journal / stop reason orchestration，以及 revision/final/export 的执行路径。
- 本地运行时入口：`run-local` 与 `resume-local`，继续以 journal 串联多次 pass；当前 owner 仍是仓内代码，而不是上游 `Hermes-Agent`。
- `src/med_autogrant/local_runtime.py` 与 `src/med_autogrant/hermes_runtime.py` 都属于本地 runtime 线：前者更多保留历史 closeout 责任，后者承担当前 migration scaffold 责任。
- `execute-revision-pass`、`build-artifact-bundle`、`build-final-package`、`build-hosted-contract-bundle` 当前都仍通过 repo-local helper 持有输入加载、identity guard 与输出 handoff。
- `build-hosted-contract-bundle` 当前还会把 `runtime_substrate_contract`、`runtime_state_contract` 与 `operator_contract` 一并导出，作为 future upstream `Hermes-Agent` host 需要兼容的托管友好 handoff contract。
- 产物面：`build-artifact-bundle`、`execute-revision-pass`、`build-final-package`、`build-hosted-contract-bundle`。

## 数据与对象模型

- `schemas/v1/nsfc-workspace.schema.json` 定义 workspace 结构与关键对象。
- `grant_run_id` 仅作为执行句柄；`workspace_id`、`draft_id`、`program_id` 保持边界分离。
- `workspace.py`、`stage_router.py`、`revision_executor.py`、`final_package.py` 等继续承载 MedAutoGrant 的 author-side domain logic；它们不应被未来的上游 substrate 目标或当前 repo-local helper 偷换成新的 authoring semantics。

## 控制面与报告

- `contracts/runtime-program/current-program.json` 是 repo-tracked current-program pointer。
- 机器本地 runtime state 统一下沉到 `$CODEX_HOME/projects/med-autogrant/runtime-state/`，用于 session / log / report / prompt 等非仓库真相面状态。
- `run-local / resume-local` 的默认 local run journal 落点固定为 `$CODEX_HOME/projects/med-autogrant/runtime-state/sessions/<grant_run_id>.json`；显式 `--journal` 仍可覆盖该默认值。
- 旧 local host-agent runtime 只保留为 compatibility bridge / regression oracle，不再作为长期产品 runtime owner。
- 上游 `Hermes-Agent` 仍是未来要真正接住 runtime substrate 的目标形态，不是当前已落地事实。

## 文档层次

- Public surface：`README*`、`docs/README*`、`docs/domain-positioning*`、`docs/mvp-scope*`。
- 核心骨架：`docs/project.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`、`docs/status.md`。
- Repo-tracked current truth 与 activation package：`docs/specs/**`。
- 历史规划：`docs/plans/**`；历史归档：`docs/history/**`。

## 历史边界

- OMX 已退场，仅保留历史入口。
