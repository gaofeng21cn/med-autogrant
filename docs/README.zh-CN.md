# 文档索引

[English](./README.md) | **中文**

这里是 `Med Auto Grant` 的文档索引，默认先读核心骨架，再看 specs/plans/history 的来源与细节。
当前公开 runtime topology 是：`CLI-first + real upstream Hermes-Agent runtime substrate`；`MCP` 继续是 supported protocol layer，`controller` 继续是 internal surface。
repo-tracked current-program truth 固定在 `contracts/runtime-program/current-program.json`，机器本地 runtime state 统一落在 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
当前入口真相也已经明确：现在真实存在的是 `operator entry` 与 `agent entry`，轻量 grant `product entry` shell 也已经 landed；它的 shared envelope 与 routing surface 还已经进一步冻结成 schema-backed contract，并在生成时 fail-closed；但更完整的 grant-facing 产品体验仍未完成。
当前 hosted-friendly contract bundle 也已经补出可机器读取的合同目录：`domain_entry_contract`、`schema_contract`、`authoring_contract` 一起进入 bundle，让 future hosted / `OPL` caller 能直接消费同一份 entry、schema 与 route truth。

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
- `docs/references/**`：仓库跟踪的内部参考文档，默认中文维护。
- `docs/plans/**`：历史规划工件，仅用于追溯。
- `docs/history/**`：历史归档入口（含 OMX）。

## 默认对外双语公开面

- [仓库首页](../README.zh-CN.md)
- [领域定位](./domain-positioning.zh-CN.md)
- [MVP 范围](./mvp-scope.zh-CN.md)

## Specs（current truth / activation package）

- [Upstream Hermes-Agent fast cutover current truth](./specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md)
- [Schema-backed product entry and routing contract current truth](./specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md)
- [Hosted contract bundle entry and route catalog current truth](./specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md)
- [OPL 对齐的理想目标与阶段图 current truth](./specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md)
- [Lightweight product entry and OPL handoff current truth](./specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md)
- [Pending authoring route handoff matrix current truth](./specs/2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md)
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
- 当前可执行 runtime 主线：`CLI-first` 形态下的真实 upstream Hermes substrate，repo-side 只保留 domain/entry adapter。
- 产品入口 shell：`build-product-entry` 已经把可直接进入、也可被 `OPL` handoff 调起的轻量 grant `product entry` shell 落到仓库里。
- schema-backed contract 收口：已 landed 的 `product entry` shell、`executor_routing_contract`、`pending_handoff_requirements` 与 service-safe route surface 现在都已进入 `schemas/v1/`，并且会在生成时 fail-closed。
- hosted contract bundle 收口：`build-hosted-contract-bundle` 现在会在既有 runtime/state/operator surface 之外，再显式导出 `domain_entry_contract`、`schema_contract` 与 `authoring_contract`，并统一受 `hosted-contract-bundle.schema.json` 约束。
- 当前任务梯子：保持已 landed 的 Hermes substrate、service-safe domain entry 与 author-side object boundary 持续全绿；旧 host-agent 线只作为回归 oracle。
- 历史 bridge / OMX 资料只负责追溯，不再构成当前入口。

## Plans 与历史归档

- [最小 Scaffold 计划](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [P1 Formal Entry And Durability Planning Brief](./plans/2026-04-07-p1-formal-entry-and-durability-planning-brief.md)
- [OPL 对齐目标形态与 hosted caller 计划](./plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md)
- [轻量产品入口与 OPL Handoff](./references/lightweight_product_entry_and_opl_handoff.md)
- [OMX 历史资料索引](./history/omx/README.zh-CN.md)
