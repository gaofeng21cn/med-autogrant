# References 索引

[English](./README.md)

本目录承载 `Med Auto Grant` 的参考材料。

生命周期信号：

- `owner`：MAG maintainers，以及对应跨仓 lane 的边界 owner。
- `purpose`：保留 OPL handoff、family contract、runtime 分层与文档治理的稳定解释材料。
- `state`：`reference`。
- `machine boundary`：仅作为人读材料。机器可读面必须使用 contracts、schemas、source path 或语义化 `human_doc:*` 标识。

Reference notes 不能替代当前产品真相。MAG 当前 grant product truth 继续以核心文档、active specs 和 `contracts/runtime-program/current-program.json` 为准。

不再解释当前边界的历史/provider-specific handoff 说明已移入 [历史归档](../history/README.zh-CN.md)。旧 OPL Runtime Manager 三层说明和旧 lightweight product-entry handoff 说明现在位于 `docs/history/`，因为其中仍有效的当前内容已被核心文档、`OPL Family Contract Adoption` 与 specs lifecycle map 吸收。

当前参考入口：

- [Grant Strategy Memory Policy](./grant_strategy_memory_policy.md)：说明 fundability、specific aims、reviewer grammar、template strategy 等经验如何以自然语言 memory 形式沉淀，同时保持 quality/controller/export surface 的结构化权威。
- [OPL Family Contract Adoption](./opl_family_contract_adoption.md)：说明 MAG 如何向 OPL stage-led、以 Agent executor 为最小执行单位 runtime framework 暴露 descriptor/projection，同时保留 grant truth、quality、route 和 export authority。
