# 文档索引

[English](./README.md) | **中文**

这里是 `Med Auto Grant` 的文档索引，默认先读核心骨架，再看 specs/plans/history 的来源与细节。
当前公开 runtime topology 是：已经有可用的本地 `CLI` runtime 基线，但上游 `Hermes-Agent` 集成尚未落地；`MCP` 继续是 supported protocol layer，`controller` 继续是 internal surface。
repo-tracked current-program truth 固定在 `contracts/runtime-program/current-program.json`，机器本地 runtime state 统一落在 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。

## 先读核心骨架

- [项目概览](./project.md)
- [当前状态](./status.md)
- [架构概览](./architecture.md)
- [不变量](./invariants.md)
- [决策记录](./decisions.md)

## 文档角色说明

- `README*` 与 `docs/README*`：对外入口与索引。
- 对外公开文档必须同步提供中英双语镜像。
- 核心骨架（`docs/project.md`、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、`docs/decisions.md`）：项目真相与工作约束。
- `docs/specs/**`：repo-tracked current truth、activation package 与设计冻结文档。
- `docs/plans/**`：历史规划工件，仅用于追溯。
- `docs/history/**`：历史归档入口（含 OMX）。

## 默认对外双语公开面

- [仓库首页](../README.zh-CN.md)
- [领域定位](./domain-positioning.zh-CN.md)
- [MVP 范围](./mvp-scope.zh-CN.md)

## Specs（current truth / activation package）

- [Upstream Hermes-Agent truth reset current truth](./specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md)
- [Formal Entry Matrix Current Truth](./specs/2026-04-07-formal-entry-matrix-current-truth.md)
- [Durability Model Clarification](./specs/2026-04-07-durability-model-clarification.md)
- [Post-R5A 本地 runtime hardening brief](./specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md)
- [Post-R5A revised-workspace validator 与 operator alignment](./specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md)
- [Post-R5A 本地 runtime walkthrough 与 output consistency current truth](./specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md)
- [Post-R5A 本地 runtime 上限与 honest stop current truth](./specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md)

Specs 是 repo-tracked 的权威 current truth/activation package，但不替代核心骨架。

## 当前基线、长线目标与任务层级

- 当前 repo-verified 迁移基线：已 absorbed 的 `CLI-first + host-agent runtime` 线现在收口于 `R5.A` honest upper bound，只保留为 migration baseline / compatibility bridge / regression oracle。
- 当前可执行 runtime 主线：本地 `CLI-first` runtime，runtime helper 仍由仓内代码持有。
- 当前任务梯子：先保持当前本地 runtime 诚实，再把 substrate 责任迁到真实的上游 `Hermes-Agent` pilot，同时保持对象边界与 authoring semantics 稳定。
- 历史 bridge / OMX 资料只负责追溯，不再构成当前入口。

## Plans 与历史归档

- [最小 Scaffold 计划](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [P1 Formal Entry And Durability Planning Brief](./plans/2026-04-07-p1-formal-entry-and-durability-planning-brief.md)
- [OMX 历史资料索引](./history/omx/README.zh-CN.md)
