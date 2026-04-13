# 文档索引

[English](./README.md) | **中文**

这里是 `Med Auto Grant` 的文档索引，默认先读核心骨架，再看 specs/plans/history 的来源与细节。
当前公开 runtime topology 是：`CLI-first + real upstream Hermes-Agent runtime substrate`；`MCP` 继续是 supported protocol layer，`controller` 继续是 internal surface。
repo-tracked current-program truth 固定在 `contracts/runtime-program/current-program.json`，机器本地 runtime state 统一落在 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。
当前入口真相也已经明确：现在真实存在的是 `operator entry` 与 `agent entry`，轻量 grant `product entry` shell 也已经 landed；`product-entry-manifest` 现在会把这层 shell 冻结成 machine-readable discovery surface，`product-frontdesk` 现在又把其上方的 controller-owned direct frontdoor 冻结下来，而它的 shared envelope 与 routing surface 还已经进一步冻结成 schema-backed contract，并在生成时 fail-closed。第一棒诚实的 `P4.A` direct-product projection 已经通过 `grant-progress` 与 `grant-cockpit` 落地，下一棒诚实的 `P4.B` direct-entry composition 也已经通过 `grant-direct-entry` 落地，当前 `P4.C` companion layer 也已经通过 `mainline-status`、`mainline-phase` 与 `grant-user-loop` 落地，`P4.D` full authoring executor layer 现在又把 `direction_screening -> frozen` 的 authoring 主线收口成 landed command catalog，而 `P4.E` 现在又把 `product-entry-manifest` / `product-frontdesk` 提升成独立 schema-backed 的 direct frontdoor contract；这些 surface 现在都已经进入 repo-tracked truth，并保持 generation-time fail-closed，但更完整的 grant-facing 产品体验仍未完成。
当前 hosted-friendly contract bundle 也已经补出可机器读取的合同目录：`domain_entry_contract`、`schema_contract`、`authoring_contract` 一起进入 bundle，让 future hosted / `OPL` caller 能直接消费同一份 entry、schema 与 route truth。
这份共享 `domain_entry_contract` 现在还会显式导出 `supported_commands` 与 `command_contracts`，而 hosted caller consumption proof 也已经 landed。

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
- [Hosted caller consumption proof current truth](./specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md)
- [OPL 对齐的理想目标与阶段图 current truth](./specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md)
- [Lightweight product entry and OPL handoff current truth](./specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md)
- [P4.A direct grant cockpit and progress projection current truth](./specs/2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md)
- [P4.B direct grant entry composition current truth](./specs/2026-04-12-p4b-direct-grant-entry-composition-current-truth.md)
- [P4.C mainline status and grant user loop current truth](./specs/2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md)
- [Full grant authoring executor current truth](./specs/2026-04-13-full-grant-authoring-executor-current-truth.md)
- [P4.E schema-backed frontdesk and manifest current truth](./specs/2026-04-13-p4e-schema-backed-frontdesk-and-manifest-current-truth.md)
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
- 产品入口发现面：`product-entry-manifest` 现在会把当前 grant shell、shared handoff 模板与当前 mainline snapshot 一起冻结成 machine-readable manifest，供 direct caller 与 `OPL` 一致消费，并由 `product-entry-manifest.schema.json` 保持 fail-closed。
- 产品 frontdesk 面：`product-frontdesk` 现在会把 grant shell 上方的 controller-owned direct frontdoor 冻结成 machine-readable frontdesk contract，并带出 `grant_authoring_readiness` 成熟度 companion，由 `product-frontdesk.schema.json` 保持 fail-closed。
- direct-product projection：`grant-progress` 与 `grant-cockpit` 现在已经作为 controller-owned、read-only 的产品投影落地；它们只消费现有 route/audit truth 与 `build-product-entry` contract hint，由 `grant-progress.schema.json` 与 `grant-cockpit.schema.json` 冻结，并且故意不是新的 `domain_entry_contract` executor command，也不进入 hosted bundle command catalog。
- direct-entry composition：`grant-direct-entry` 现在会把 `grant-progress`、`grant-cockpit` 与两种 `build-product-entry` mode 收成一份 controller-owned 的 direct-entry contract，由 `grant-direct-entry.schema.json` 冻结，并且继续不进入 service-safe domain command catalog。
- current user loop：`mainline-status`、`mainline-phase` 与 `grant-user-loop` 现在会把 repo 主线快照、当前 direct-entry composition 与 route-derived next action 收成当前 inbox-like shell；其中 `grant-user-loop` 由 `grant-user-loop.schema.json` 冻结，并且继续不进入 service-safe domain command catalog。
- schema-backed contract 收口：已 landed 的 `product entry` shell、`product-entry-manifest`、`product-frontdesk`、`executor_routing_contract`、全链 authoring command surface、`grant-progress`、`grant-cockpit`、`grant-direct-entry`、`grant-user-loop` 与 service-safe route surface 现在都已进入 `schemas/v1/`，并且会在生成时 fail-closed。
- hosted contract bundle 收口：`build-hosted-contract-bundle` 现在会在既有 runtime/state/operator surface 之外，再显式导出 `domain_entry_contract`、`schema_contract` 与 `authoring_contract`，并统一受 `hosted-contract-bundle.schema.json` 约束。
- hosted caller proof 收口：external caller 现在已经可以直接消费共享 `domain_entry_contract` 里的 `supported_commands` 与 `command_contracts`，不再依赖 repo-local helper。
- 当前任务梯子：保持已 landed 的 Hermes substrate、service-safe domain entry、hosted caller proof 与 author-side object boundary 持续全绿；旧 host-agent 线只作为回归 oracle。
- 历史 bridge / OMX 资料只负责追溯，不再构成当前入口。

## Plans 与历史归档

- [最小 Scaffold 计划](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [P1 Formal Entry And Durability Planning Brief](./plans/2026-04-07-p1-formal-entry-and-durability-planning-brief.md)
- [OPL 对齐目标形态与 hosted caller 计划](./plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md)
- [轻量产品入口与 OPL Handoff](./references/lightweight_product_entry_and_opl_handoff.md)
- [OMX 历史资料索引](./history/omx/README.zh-CN.md)
