# 活跃文档

Owner: `MedAutoGrant`
Purpose: `active_execution_and_gap_index`
State: `active_support`
Machine boundary: 人读索引。机器真相继续归 contracts、schemas、source、current-program records、runtime evidence 与 grant artifacts。

本目录是 OPL-family canonical 目录中承接 MAG 当前执行、当前计划、当前差距、active baton 和当前完成门槛的位置。dated closeout evidence、receipt/proof 流水和历史演变进入 `../history/**`。

旧 `docs/plans/` 活跃计划层已物理退役。新的 recurring active material 直接进入本目录。

当前入口先看：

- [文档索引](../README.md)
- [当前状态](../status.md)
- [MAG 理想目标态差距与完善计划](./mag-ideal-state-cross-repo-gap-plan.md)
- [MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md)

当前 active plan 采用 direct retirement posture：旧模块、旧接口、旧 CLI alias、facade patch bridge、兼容聚合测试或旧 runtime owner wording 若已被当前 owner surface 替代，应先迁移 active caller，再删除或归入 history/tombstone，不新增 compatibility shell。该 posture 也被 `product-entry-manifest` 的 `ideal_state_closure_status.direct_retirement_posture` 投影。

MAG-owned transition/oracle 后续工作以 [MAG 理想目标态差距与完善计划](./mag-ideal-state-cross-repo-gap-plan.md) 为唯一 active plan 入口：MAG 负责 grant transition table、guard、typed blocker、owner action 和 oracle fixture；generic state-machine runner、queue、retry/dead-letter 与 provider lifecycle 归 OPL Framework。当前仓内 transition table / oracle fixture 已落地，并有 oracle -> domain_handler `stage-attempt/closeout` -> owner/no-regression receipt refs 的 focused proof；这仍不等于 OPL-hosted production long-run soak 已完成。

[MAG 私有实现与 OPL 迁移台账](./opl-private-implementation-migration-inventory.md) 是当前 physical morphology / private platform residue 的明细 inventory：它记录 product-entry、domain_handler、CLI、autonomy controller、domain-runtime 命名面的 active caller、分类、保留 authority、可上收 generic 子域、迁移门槛和验证入口。该台账不替代 `mag-ideal-state-cross-repo-gap-plan.md`，也不把台账化写成 production/default caller 已迁移完成。

新增 active 文档必须先证明不能由 `mag-ideal-state-cross-repo-gap-plan.md`、核心五件套、`docs/specs/specs_lifecycle_map.md`、当前 contract/source surface 或 `docs/history/**` 承接。历史 spec、closeout、provider proof、旧 runtime/local-manager/Gateway/Hermes 记录和 dated evidence 不进入本目录；若仍有 current 规则，先抽取到对应 owner，再把原文保留为 provenance。
