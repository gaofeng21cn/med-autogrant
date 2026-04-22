# 文档索引

[English](./README.md) | **中文**

这个目录是 `Med Auto Grant` 的第二层技术阅读面。
仓库首页应优先写给申请人、领域专家和非技术读者。
而这里负责承接其后的技术记录、追溯记录、参考说明和实现历史。

## 按读者类型进入

| 读者 | 建议起点 | 目的 |
| --- | --- | --- |
| 潜在用户与领域专家 | [仓库首页](../README.zh-CN.md)、[领域定位](./domain-positioning.zh-CN.md)、[MVP 范围](./mvp-scope.zh-CN.md) | 先理解这条基金主线是干什么的，再决定是否进入技术细节 |
| 技术规划者、架构读者、方向同步读者 | [项目概览](./project.md)、[当前状态](./status.md)、[架构](./architecture.md)、[不变量](./invariants.md)、[决策记录](./decisions.md)、[合同说明](../contracts/README.md) | 快速抓住当前技术形态、边界和主线方向 |
| 开发者与维护者 | [Specs 目录](./specs/)、[References 目录](./references/)、[Plans 目录](./plans/)、[历史归档](./history/README.zh-CN.md) | 查看技术记录、内部参考、未来工作和归档材料 |

## 当前技术图景

- `Med Auto Grant` 是位于 `OPL` family gateway 与 handoff surface 之下的 author-side 医学基金 domain gateway。
- formal-entry matrix 继续固定为 `CLI`、`MCP` 与 `controller`。
- `Hermes-Agent` 指外部 runtime substrate owner；repo-side grant adapter 继续在其上方稳定 grant truth、direct entry 与 route contract。
- 历史 program 记录与迁移说明继续留在 `docs/specs/` 与 `docs/history/` 中供追溯。
- frontdesk、user-loop、projection 与本地 `submission-ready` package 已落地；未来 hosted 产品扩展统一留在 `docs/plans/`。
- `OPL` 负责 family navigation 与 domain handoff；MAG 负责 grant-domain truth、direct grant entry 与 execution routing。
- 当前 controller-owned、read-only 的 projection 继续包括 `workspace progress`、`workspace cockpit`、`product direct-entry` 与 `product user-loop`，并在作者侧主线之上保持 schema-backed 边界。
- 当前 grouped public shell 也已经把 `product build-entry`、`product manifest`、`product frontdesk` 与 `package submission-ready` 暴露成公开 CLI 入口面。
- 当前轻量 grant `product entry` shell 就是现在的产品入口 shell 与内部 domain/API catalog builder；未来 hosted 产品形态统一留在 `docs/plans/`。
- 质量治理已经通过 `workspace quality-scorecard` 与 `workspace quality-diff` 收成 schema-backed surface。
- 长时间自治已经通过 `pass autonomy-controller` 暴露为正式入口，并输出结构化 blocker 与 evidence-gap report。
- 通用 grant grammar 与 funder-specific family profile 规则已在 `grant_family_registry.py` 分层；NSFC、NIH R21 和 Wellcome Discovery 已共用同一套 admitted registry 形状，同时保留 Wellcome placeholder 作为后续 family scaffold。

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

## 技术记录

- [`current-program.json`](../contracts/runtime-program/current-program.json)
- [Specs 目录](./specs/)
- [合同说明](../contracts/README.md)

当前 grant product-entry shell 继续作为 domain/API catalog builder；当前 schema-backed 冻结也会把 `hosted contract bundle`、`domain_entry_contract`、`supported_commands` 与 `command_contracts` 继续暴露给 hosted caller / 外部 caller 使用。
质量治理与自治 controller schema 已进入 [`schema-index.json`](../schemas/v1/schema-index.json) 和 current-program truth surface。

## 追溯记录

- [References 目录](./references/)
- [历史归档](./history/README.zh-CN.md)

## Plans 与历史规划工件

- [Plans 目录](./plans/)

已完成的规划工件继续保留在 `docs/plans/` 中供追溯，直到后续被吸收到更长期的历史层。
当前主线真相继续以核心文档、`docs/specs/` 和 [`current-program.json`](../contracts/runtime-program/current-program.json) 为准。

## 文档规则

- 继续把 [仓库首页](../README.zh-CN.md) 保持成申请人和非技术专家可读的入口。
- 继续把默认公开文档保持成中英双语镜像。
- `docs/specs/` 继续是技术记录和 activation package 的权威位置，但不能取代用户入口首页。
- references、plans 和 history 可以保留，但不能占据默认公开阅读路径。

## 治理说明

- 文档治理统一冻结在 [系列项目文档治理清单](./references/series-doc-governance-checklist.md)、技术工作集和仓库跟踪的 contract/doc surface 中，而不再只写在 `AGENTS.md`。
- `README*` 与 `docs/README*` 是默认公开入口。
- `docs/specs/**` 承载技术记录与 activation package。
- `docs/references/**` 承载内部参考说明。
- `docs/plans/**` 与 `docs/history/**` 承载未来工作与历史支持材料。
