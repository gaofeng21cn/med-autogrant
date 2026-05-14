# 活跃计划

本目录只保留尚未被核心文档、合同面或历史归档吸收的活跃计划，或明确仍属于未来推进的计划。

当前计划组采用直接退休口径：已经被核心文档、合同面、源码或测试替代的旧模块、旧接口、旧 CLI shell alias、旧 facade patch bridge 和旧聚合测试入口，不再保留兼容性接口；后续若仍有 active caller，先改到最新 owner surface，再删除或归档旧面。

当前活跃计划：

- [MAG 理想目标态差距与完善计划](./mag-ideal-state-cross-repo-gap-plan.zh-CN.md)：当前聚焦 production live soak、no-regression evidence、memory apply 泛化、OPL generic primitive absorption，以及 legacy direct retirement。

已完成的一次性计划工件已迁入：

- [历史 plans](../history/plans/README.zh-CN.md)

当前项目真相和维护者入口统一回到：

- [文档索引](../README.zh-CN.md)
- [项目概览](../project.md)
- [当前状态](../status.md)
- [架构](../architecture.md)
- [不变量](../invariants.md)
- [决策记录](../decisions.md)
- [`current-program.json`](../../contracts/runtime-program/current-program.json)
