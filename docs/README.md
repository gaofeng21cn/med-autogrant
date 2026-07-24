# 文档索引

Owner: `Med Auto Grant`
Purpose: `documentation_index`
State: `current`
Machine boundary: 本文是人读索引。机器真相归 root contracts、schemas、source、CLI/API behavior、runtime receipts 与 workspace/artifact outputs。

## 先读

1. [项目概览](./project.md)
2. [当前状态](./status.md)
3. [架构](./architecture.md)
4. [不变量](./invariants.md)
5. [决策](./decisions.md)

这五份文档是当前人读 truth set。它们不作为脚本、测试或 runtime 的机器接口。
OPL Package 跨仓目标、迁移顺序与删除门禁只在 Framework 的
[平台组合迁移 SSOT](https://github.com/gaofeng21cn/one-person-lab/blob/main/docs/active/opl-package-platform-composition-migration.md)
维护；本仓只记录 MAG owner 边界，不复制整套平台计划。

## 当前计划

- [MAG Active Truth：外部 Owner Evidence Tail](./active/mag-ideal-state-cross-repo-gap-plan.md)
- [私有面 machine owner 导航](./active/opl-private-implementation-migration-inventory.md)
- [Foundry Agent OS 目标差异](./active/foundry-agent-os-target-delta.md)

结构 cleanup 已收口；active plan 只保留 live owner evidence 与下一轮执行 baton，私有面导航只指向 machine owners，不维护已删除 wrapper、固定 path inventory 或 scanner snapshot。

## 目录

| 目录 | 角色 |
| --- | --- |
| `active/` | 唯一 Active Truth、外部 evidence gaps 与 owner 路由 |
| `public/` | 公开定位与 MVP 边界 |
| `product/` | app skill 和 generated product surface 支撑 |
| `runtime/` | OPL-hosted runtime 与 MAG authority 边界 |
| `delivery/` | package/export/manual portal 支撑 |
| `source/` | workspace/source body 边界 |
| `policies/` | 稳定治理规则 |
| `specs/` | active/support specs 与 lifecycle map |
| `references/` | 非 current owner 的参考材料 |
| `history/` | 旧计划、旧 specs、proof 与 tombstone |

## Machine Entry

- Current program: `contracts/runtime-program/current-program.json`
- Pack input: `contracts/pack_compiler_input.json`
- Stage source: `agent/stages/manifest.json`
- Generated stage plane locator: `/product_entry_manifest/family_stage_control_plane`
- Functional audit: `contracts/functional_privatization_audit.json`
- Receipt contract: `contracts/owner_receipt_contract.json`
- Live progress: `contracts/live_stage_run_progress_evidence.json`

OPL structure currentness 使用 canonical conformance scanner，不使用 MAG 私有 source-purity wrapper。

## 文档纪律

- Active current facts 进入核心五件套、active plan、contract 或 source owner。
- Dated proof、worktree/branch closeout、旧 snapshot 和 provider history 进入 `history/`。
- 不把旧路径恢复为 compatibility entry，不用测试固定 prose。
