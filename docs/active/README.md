# 活跃文档

Owner: `MedAutoGrant`
Purpose: `active_execution_and_gap_index`
State: `active_support`
Machine boundary: 人读索引。机器真相继续归 contracts、schemas、source、current-program records、runtime evidence 与 grant artifacts。

本目录是 OPL-family canonical 目录中承接 MAG 当前执行、当前计划、当前差距、active baton 和 closeout evidence 的位置。

旧 `docs/plans/` 活跃计划层已物理退役。新的 recurring active material 直接进入本目录。

当前入口先看：

- [文档索引](../README.md)
- [当前状态](../status.md)
- [MAG 理想目标态差距与完善计划](./mag-ideal-state-cross-repo-gap-plan.md)

当前 active plan 采用 direct retirement posture：旧模块、旧接口、旧 CLI alias、facade patch bridge、兼容聚合测试或旧 runtime owner wording 若已被当前 owner surface 替代，应先迁移 active caller，再删除或归入 history/tombstone，不新增 compatibility shell。该 posture 也被 `product-entry-manifest` 的 `ideal_state_closure_status.direct_retirement_posture` 投影。

MAG-owned transition/oracle 后续工作以 [MAG 理想目标态差距与完善计划](./mag-ideal-state-cross-repo-gap-plan.md) 为唯一 active plan 入口：MAG 负责 grant transition table、guard、typed blocker、owner action 和 oracle fixture；generic state-machine runner、queue、retry/dead-letter 与 provider lifecycle 归 OPL Framework。当前仓内不声明 transition table / oracle fixture 已落地，也不声明 OPL-hosted production long-run soak 已完成。
