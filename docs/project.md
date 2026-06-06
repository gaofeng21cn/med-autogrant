# 项目概览

Owner: `Med Auto Grant`
Purpose: `project_role_and_boundary`
State: `current`
Machine boundary: 本文是人读项目概览。机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 与 workspace/artifact outputs。

## 项目定位

`Med Auto Grant` 是独立的医学 `Grant Ops` domain agent，面向 author-side、proposal-facing 的基金申请写作主线。对外第一主语是单一 `Med Auto Grant` app skill；repo-local formal entry 仍是 `CLI` / `MedAutoGrantDomainEntry`，用于给 Codex、OPL 和其他通用 agent 按 contract 调用。

任务启动后的默认运行驻留由 OPL/Temporal hosted autonomous runtime 承担；MAG 不实现自己的 daemon、scheduler、attempt loop 或 attempt ledger。默认具体 stage executor 是 `Codex CLI` / `codex_cli`；`Hermes-Agent` 等只作为显式非默认 executor / proof lane 接入，并必须产出可审计 receipt。

MAG 保留 grant truth、fundability / quality / export verdict、package authority、grant strategy memory accept/reject、owner receipt、typed blocker 与 grant-native helper。OPL 只消费 MAG 暴露的 descriptor、projection、refs、owner receipt 和 typed blocker，用于 stage-led runtime、queue/wakeup、handoff、receipt、operator projection、shared contracts/indexes 和 generated/App surfaces；OPL 不生成 grant route、fundability verdict、authoring quality verdict 或 submission-ready export verdict。

## 当前边界

- 当前任务边界：指定基金任务正文 authoring；科学完成可待审包与形式/客观补件完成分层表达。
- 当前入口：`Med Auto Grant app skill -> CLI / MedAutoGrantDomainEntry -> domain-handler export|dispatch target -> MAG-owned pass/package/action surfaces`。
- 当前 OPL 读法：MAG 是 admitted OPL-compatible Foundry Agent package，不是 OPL 内部 workspace 模块。
- 当前 repo-source 读法：`agent/` 是 Declarative Grant Pack；`contracts/` 是机器合同和 schema/index；`runtime/authority_functions/` 是最小 grant authority function anchor；`src/` 是 domain handler、authority adapter、native helper、refs-only adapter 或 diagnostic；`docs/` 是人读治理说明。
- 当前 product/status/user-loop/domain-handler/runtime-control surface：只能作为 app skill 下的 command contract、refs-only projection、direct handler target、migration input 或 OPL/App generated shell target 读取，不是 MAG 长期自有 product/workbench wrapper。

## 项目目标

- 稳定 `CLI / MCP / controller` formal-entry matrix，并保持 `CLI` 是默认正式入口、`MCP` 是 supported protocol layer、`controller` 是 internal surface。
- 保持 Codex App direct skill path 与 OPL-hosted path 的语义等价：两条路径都回到 MAG-owned route truth、workspace truth、quality surface 和 export gate。
- 把 MAG 长期形态收敛到 `Declarative Grant Pack + OPL generated/hosted surfaces + minimal grant authority functions`。
- 让 OPL/App 能读取 MAG stage/action/projection descriptor、owner receipt、typed blocker、package refs、quality/export refs 和 safe action refs，同时不读取 grant body、memory body、verdict body 或 package body。
- 保持 `package submission-ready` 作为本地 fail-closed export surface；它不等于官网已提交，也不替代正文科学质量完成判断。

## 非目标

- 不把 `MCP` 或 `controller` 写成当前 public runtime formal entry。
- 不把 MAG 写成成熟 autopilot、reviewer-owned runtime、repo-owned scheduler、attempt ledger、session store、workbench 或 generic runner。
- 不把 OPL runtime framework、旧 `OPL Runtime Manager`、Gateway/local-manager、本地 journal、attempt ledger 或旧上游 Hermes 默认 provider 口径写成 MAG 默认 runtime owner。
- 不把 `product entry/product status/direct-entry/user-loop`、local scripts、hosted bundle 或 schema completeness 写成 grant-ready、fundability-ready、quality-ready、export-ready、submission-ready 或 production-ready。
- 不保留旧 module、interface、CLI alias、facade、wrapper、patch bridge、compat aggregate test 或旧 docs entry 的 compatibility surface；active caller 迁出并有 owner/delete evidence 后直接删除或归入 history/tombstone。

## 当前阅读入口

- 当前状态和证据门：[当前状态](./status.md)
- 架构与 owner split：[架构概览](./architecture.md)
- 稳定约束：[不变量](./invariants.md)
- 当前决策：[决策记录](./decisions.md)
- 唯一 active gap / plan：[MAG 理想目标态差距与完善计划](./active/mag-ideal-state-cross-repo-gap-plan.md)
- per-surface private implementation inventory：[MAG 私有实现与 OPL 迁移台账](./active/opl-private-implementation-migration-inventory.md)
- 机器 current-program pointer：[`contracts/runtime-program/current-program.json`](../contracts/runtime-program/current-program.json)
