# 项目概览

Owner: `Med Auto Grant`
Purpose: `project_role_and_boundary`
State: `current`
Machine boundary: 本文是人读项目概览。机器真相归 `contracts/runtime-program/current-program.json`、根层 contracts、schemas、source、CLI/API 行为、runtime receipts 与 workspace/artifact outputs。

## 定位

`Med Auto Grant` 是独立的医学基金申请 domain agent。它的 OPL canonical agent id 与 OPL Agent Package id 都是 `mag`，唯一 OCI Package repository 是 `ghcr.io/gaofeng21cn/one-person-lab-packages/mag`；`med-autogrant` 只作为仓库、Python distribution 与 plugin/skill carrier locator，`medautogrant` 只作为 module/CLI locator。

生态定位遵循 `OPL Base ~= R`、`OPL App ~= RStudio`、`OPL Package ~= R Package`。
MAG 是 `OPL Package(kind=agent)`，自己定义 executor-neutral identity、capabilities、
required/optional dependency intent、grant business task 与 typed views。Codex-first 是当前
最低成本实现路径，不是 MAG identity 或长期生态边界。

长期形态固定为：

`Declarative Grant Pack + OPL generated/hosted surfaces + minimal MAG authority functions`

Temporal 持有 execution facts；OPL 持有 generic runtime、stage attempt lifecycle、
queue/wakeup、retry/resume、attempt ledger、carrier readback 聚合、generated caller 与
App/workbench shell。MAG 持有 grant business lifecycle、grant truth、
fundability/quality/export verdict、submission package authority、memory accept/reject、
owner receipt、typed blocker 与 grant-native helper。领域语义 route 由
`semantic_route_decision_owner=decisive_codex_attempt` 给出；
`stage_transition_materialization_owner=opl_stage_run_controller` 只校验并物化该决定，
不取得 grant-semantic approval authority。

## 当前入口

- `medautogrant` grouped CLI
- `MedAutoGrantDomainEntry`
- `domain-handler export`
- `domain-handler dispatch`
- `agent/primary_skill/SKILL.md`

Domain handler dispatch 只允许 `domain-memory/propose`、`domain-memory/decide`、`stage-attempt/closeout`。旧 product/status/user-loop/runtime/workbench wrapper 已退役；对应用户面由 OPL/App generated surfaces 提供。

所有 executor kind 由 MAG 组装 grant prompt 和 domain payload，再交给 OPL Python
executor client；MAG 不实现 Codex/OPL subprocess、timeout、process cleanup 或 receipt
transport，只解析 canonical receipt 和 typed grant closeout。`opl packages
install|update|uninstall mag` 是 Framework 聚合的稳定用户动作入口，实际 bytes 与
lifecycle 由 carrier 承担。目标发布权威是 MAG owner 独立推进本包 GHCR
`latest-stable`；其 live 迁移状态以 [当前状态](./status.md) 为准。Codex Plugin 只投影
Plugin/config/cache，不能单独证明完整 MAG runtime installed。本仓不提供用户目录
symlink/marketplace mutation。

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
- [私有面 machine owner 导航](./active/opl-private-implementation-migration-inventory.md)
