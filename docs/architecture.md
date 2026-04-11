# 架构概览

## 入口与执行

- CLI 是唯一正式入口：`validate-workspace`、`summarize-workspace`、`next-step`、`critique-summary`、`stage-route-report`。
- 本地运行时入口：`run-local` 与 `resume-local`，以 journal 串联多次本地 pass。
- 产物面：`build-artifact-bundle`、`execute-revision-pass`、`build-final-package`、`build-hosted-contract-bundle`。

## 数据与对象模型

- `schemas/v1/nsfc-workspace.schema.json` 定义 workspace 结构与关键对象。
- `grant_run_id` 仅作为执行句柄；`workspace_id`、`draft_id`、`program_id` 保持边界分离。

## 控制面与报告

- `.runtime-program/**` 仅承担本地 control-plane：`context/`、`plans/`、`reports/`。
- `reports/med-autogrant-mainline` 维护 `LATEST_STATUS`、`ITERATION_LOG`、`OPEN_ISSUES` 的同步规则。

## 文档层次

- 核心骨架：`docs/project.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`、`docs/status.md`。
- Repo-tracked current truth 与 activation package：`docs/specs/**`。
- 历史规划：`docs/plans/**`；历史归档：`docs/history/**`。
