# 架构概览

## 主链路

当前主链路是 `CLI-first + Hermes-backed runtime`：

`operator / agent -> CLI -> Hermes substrate -> MedAutoGrant domain logic -> critique / export / stage surfaces -> durable artifacts`

formal-entry matrix 继续固定为：`CLI` 是 formal entry，`MCP` 是 supported protocol layer，`controller` 是 internal surface。

## 入口与执行

- CLI 是唯一正式入口：`validate-workspace`、`summarize-workspace`、`next-step`、`critique-summary`、`stage-route-report`。
- Hermes substrate 负责 runtime dispatch、workspace/final-package 输入加载、journal / stop reason orchestration，以及 revision/final/export 的执行路径。
- 本地运行时入口：`run-local` 与 `resume-local`，继续以 journal 串联多次 pass，但产品 owner 已切到 `src/med_autogrant/hermes_runtime.py`。
- `src/med_autogrant/local_runtime.py` 只保留为 compatibility bridge / regression oracle wrapper，不再承载长期产品 runtime owner 语义。
- `build-hosted-contract-bundle` 的 final-package 读取、`program_id` control-plane 解析、identity guard 与输出 handoff 也由 `src/med_autogrant/hermes_runtime.py` 接管。
- 产物面：`build-artifact-bundle`、`execute-revision-pass`、`build-final-package`、`build-hosted-contract-bundle`。

## 数据与对象模型

- `schemas/v1/nsfc-workspace.schema.json` 定义 workspace 结构与关键对象。
- `grant_run_id` 仅作为执行句柄；`workspace_id`、`draft_id`、`program_id` 保持边界分离。
- `workspace.py`、`stage_router.py`、`revision_executor.py`、`final_package.py` 等继续承载 MedAutoGrant 的 author-side domain logic；它们不被 Hermes substrate 改写成新的 authoring semantics。

## 控制面与报告

- `.runtime-program/**` 仅承担本地 control-plane：`context/`、`plans/`、`reports/`。
- `reports/med-autogrant-mainline` 维护 `LATEST_STATUS`、`ITERATION_LOG`、`OPEN_ISSUES` 的同步规则。
- 旧 local host-agent runtime 只保留为 compatibility bridge / regression oracle，不再作为长期产品 runtime owner。

## 文档层次

- Public surface：`README*`、`docs/README*`、`docs/domain-positioning*`、`docs/mvp-scope*`。
- 核心骨架：`docs/project.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`、`docs/status.md`。
- Repo-tracked current truth 与 activation package：`docs/specs/**`。
- 历史规划：`docs/plans/**`；历史归档：`docs/history/**`。

## 历史边界

- OMX 已退场，仅保留历史入口。
