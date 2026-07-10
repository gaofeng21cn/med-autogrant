# 项目概览

Owner: `Med Auto Grant`
Purpose: `project_role_and_boundary`
State: `current`
Machine boundary: 本文是人读项目概览。机器真相归 `contracts/runtime-program/current-program.json`、根层 contracts、schemas、source、CLI/API 行为、runtime receipts 与 workspace/artifact outputs。

## 定位

`Med Auto Grant` 是独立的医学基金申请 domain agent，也是 canonical id 为 `mag` 的 OPL Foundry Agent package。`med-autogrant` 只作为仓库、Python package、plugin 和 skill locator。

长期形态固定为：

`Declarative Grant Pack + OPL generated/hosted surfaces + minimal MAG authority functions`

OPL/Temporal 持有 generic runtime、stage attempt lifecycle、queue/wakeup、retry/resume、attempt ledger、generated caller 与 App/workbench shell。MAG 持有 grant truth、fundability/quality/export verdict、package authority、memory accept/reject、owner receipt、typed blocker、transition oracle 与 grant-native helper。

## 当前入口

- `medautogrant` grouped CLI
- `MedAutoGrantDomainEntry`
- `domain-handler export`
- `domain-handler dispatch`
- `agent/primary_skill/SKILL.md`

Domain handler dispatch 只允许 `domain-memory/propose`、`domain-memory/decide`、`stage-attempt/closeout`。旧 product/status/user-loop/runtime/workbench wrapper 已退役；对应用户面由 OPL/App generated surfaces 提供。

## 目标

- 在同一 funding call 下保持 workspace、draft、route、quality 与 package identity 稳定。
- 让 direct path 与 OPL-hosted path 回到同一 MAG authority surface。
- 让 OPL 只消费 descriptor、refs、receipt 与 blocker，不读取或改写 grant/memory/artifact/package body。
- 保持 submission-ready package fail closed；它不等于外部 portal 已提交。

## 非目标

- 不拥有 generic scheduler、daemon、queue、attempt ledger、session store、workbench 或 generated product shell。
- 不恢复旧 wrapper、facade、flat CLI alias、compatibility test 或私有 pack compiler。
- 不把 schema、conformance、focused tests、provider completion 或 refs-only ledger 写成 grant-ready、submission-ready 或 production-ready。

## 下一跳

- [当前状态](./status.md)
- [架构](./architecture.md)
- [不变量](./invariants.md)
- [决策](./decisions.md)
- [当前计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- [迁移台账](./active/opl-private-implementation-migration-inventory.md)
