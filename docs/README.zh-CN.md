# 文档索引

[English](./README.md) | **中文**

这个目录是 `Med Auto Grant` 的第二层技术阅读面。
仓库首页应优先写给申请人、领域专家和非技术读者。
而这里负责承接其后的 contract、current-truth spec、参考说明和实现历史。

## 按读者类型进入

| 读者 | 建议起点 | 目的 |
| --- | --- | --- |
| 潜在用户与领域专家 | [仓库首页](../README.zh-CN.md)、[领域定位](./domain-positioning.zh-CN.md)、[MVP 范围](./mvp-scope.zh-CN.md) | 先理解这条基金主线是干什么的，再决定是否进入技术细节 |
| 技术规划者、架构读者、方向同步读者 | [项目概览](./project.md)、[当前状态](./status.md)、[架构](./architecture.md)、[不变量](./invariants.md)、[决策记录](./decisions.md)、[合同说明](../contracts/README.md) | 快速抓住当前真相、边界和主线方向 |
| 开发者与维护者 | [Specs 目录](./specs/)、[References 目录](./references/)、[Plans 目录](./plans/)、[历史归档](./history/omx/README.zh-CN.md) | 查看 current truth、内部参考、规划历史和归档材料 |

## 当前基线

- `Med Auto Grant` 是 `OPL` GUI / management shell 下的一级医学基金 domain module / agent。
- Codex 是基金 authoring route 的默认交互与执行路径。
- `Hermes-Agent` 是显式选择时的备用模式与长久在线网关，用于长期运行或 route-specific proof 工作。
- 历史 closeout 与迁移记录继续留在 `docs/specs/` 与 `docs/history/` 中供追溯。
- 仓内 repo-local adapter 保留 grant-domain truth、入口语义与 route contract。
- 当前 frontdesk、user-loop、projection 与本地 `submission-ready` package 已落地，但成熟 hosted 基金前台仍是后续工作。
- `OPL` 负责 family navigation 与 management-shell 可见性；MAG 负责 grant-domain truth 与 execution routing。
- 当前 formal-entry matrix 仍是 `CLI`、`MCP` 与 `controller`。
- 当前 controller-owned、read-only 的 projection 继续包括 `workspace progress`、`workspace cockpit`、`product direct-entry` 与 `product user-loop`，并在作者侧主线之上保持 schema-backed 边界。
- 当前 grouped public shell 也已经把 `product build-entry`、`product manifest`、`product frontdesk` 与 `package submission-ready` 暴露成公开 CLI 入口面。
- 当前轻量 grant `product entry` shell 就是现在的产品入口 shell 与内部 domain/API catalog builder，更完整的 hosted 产品形态仍属后续工作。

## 技术工作集

开始改仓库状态前，先读这些文件：

- [项目概览](./project.md)
- [当前状态](./status.md)
- [架构](./architecture.md)
- [不变量](./invariants.md)
- [决策记录](./decisions.md)
- [合同说明](../contracts/README.md)
- [`current-program.json`](../contracts/runtime-program/current-program.json)

机器本地 runtime state 继续统一放在 `$CODEX_HOME/projects/med-autogrant/runtime-state/`。

## 默认公开入口

- [仓库首页](../README.zh-CN.md)
- [领域定位](./domain-positioning.zh-CN.md)
- [MVP 范围](./mvp-scope.zh-CN.md)

这些文件构成默认公开入口；凡是属于公开表面的内容，应在适用时保持中英双语镜像。

## 仓库跟踪的技术文档

### 当前真相与活跃 frontdoor 记录

- [`current-program.json`](../contracts/runtime-program/current-program.json)
- [Specs 目录](./specs/)
- [Schema-backed product entry and routing contract current truth](./specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md)
- [P4.F local submission-ready package current truth](./specs/2026-04-13-p4f-local-submission-ready-package-current-truth.md)

当前 grant product-entry shell 继续作为 domain/API catalog builder；当前 schema-backed 冻结也会把 `hosted contract bundle`、`domain_entry_contract`、`supported_commands` 与 `command_contracts` 继续暴露给 hosted caller / 外部 caller 使用。

### 追溯记录

- [Upstream Hermes-Agent Fast Cutover current truth](./specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md)
- [Lightweight product entry and OPL handoff current truth](./specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md)
- [Hosted contract bundle entry and route catalog current truth](./specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md)
- [Hosted caller consumption proof current truth](./specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md)
- [OPL-aligned ideal target and phase map current truth](./specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md)
- [Full grant authoring executor current truth](./specs/2026-04-13-full-grant-authoring-executor-current-truth.md)

### Contracts 与 schema

- [合同说明](../contracts/README.md)
- [`runtime-program/`](../contracts/runtime-program/)
- [`schemas/v1/`](../schemas/v1/)

### 内部参考说明

- [轻量产品入口与 OPL Handoff](./references/lightweight_product_entry_and_opl_handoff.md)：legacy / internal entry-mode 参考
- [OPL 托管运行时三层合同](./references/opl_managed_runtime_three_layer_contract.md)：历史 owner-split 参考
- [系列项目文档治理清单](./references/series-doc-governance-checklist.md)

### Plans 与历史

- [Plans 目录](./plans/)
- [OPL 对齐目标形态与 hosted caller 计划](./plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md)
- [最小 Scaffold 计划](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [历史归档](./history/omx/README.zh-CN.md)

## 文档规则

- 继续把 [仓库首页](../README.zh-CN.md) 保持成申请人和非技术专家可读的入口。
- 继续把默认公开文档保持成中英双语镜像。
- `docs/specs/` 继续是 repo-tracked current truth 和 activation package 的权威位置，但不能取代用户入口首页。
- references、plans 和 history 可以保留，但不能再占据默认公开阅读路径。

## 治理说明

- 文档治理统一冻结在 [系列项目文档治理清单](./references/series-doc-governance-checklist.md)、技术工作集和仓库跟踪的 contract/doc surface 中，而不再只写在 `AGENTS.md`。
- `README*` 与 `docs/README*` 是默认公开入口。
- `docs/specs/**` 承载 repo-tracked current truth 与 activation package。
- `docs/references/**` 承载内部参考说明。
- `docs/plans/**` 与 `docs/history/**` 承载历史支持材料。
