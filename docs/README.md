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
OPL Package 跨仓目标、阶段门、迁移顺序、验收与删除授权只在 App 的
[跨仓总体迁移 SSOT](https://github.com/gaofeng21cn/one-person-lab-app/blob/main/docs/active/opl-package-platform-composition-migration.md)
维护。Framework 同名文档只是 Framework compatibility inventory、repo-local
migration 与 deletion appendix；本仓只记录 MAG owner 边界，不复制整套平台计划。

## 当前计划

- [MAG 外部 Owner Evidence](./active/mag-ideal-state-cross-repo-gap-plan.md)

## 目录

| 目录 | 角色 |
| --- | --- |
| `active/` | 当前外部 evidence gaps |
| `public/` | 公开定位与 MVP 边界 |
| `product/` | app skill 和 generated product surface 支撑 |
| `runtime/` | OPL-hosted runtime 与 MAG authority 边界 |
| `delivery/` | package/export/manual portal 支撑 |
| `source/` | workspace/source body 边界 |
| `policies/` | 稳定规则索引 |
| `specs/` | current 与 support specs |
| `references/` | 非 current owner 的参考材料 |

## Machine Entry

- Current program: `contracts/runtime-program/current-program.json`
- Pack input: `contracts/pack_compiler_input.json`
- Stage source: `agent/stages/manifest.json`
- Generated stage plane locator: `/product_entry_manifest/family_stage_control_plane`
- Functional audit: `contracts/functional_privatization_audit.json`
- Receipt contract: `contracts/owner_receipt_contract.json`
- Live progress: `contracts/live_stage_run_progress_evidence.json`

OPL structure currentness 使用 canonical conformance scanner，不使用 MAG 私有 source-purity wrapper。

完成过程和旧版本从 Git 历史读取；当前事实直接更新核心文档、active evidence 表或对应机器 owner。
