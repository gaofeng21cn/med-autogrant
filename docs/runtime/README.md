# Runtime 文档

Owner: `MedAutoGrant`
Purpose: `grant_runtime_support`
State: `active_support`
Machine boundary: 人读索引。Runtime truth 继续归 contracts、schemas、source、current-program records、runtime evidence 与 owner receipts。

本目录承接 MAG runtime/control/projection 支撑和 direct/hosted 边界说明。可跨 MAS/MAG/RCA 复用的通用 runtime primitive 应记录为 MAG-to-OPL 上收候选。

当前入口先看：

- [架构](../architecture.md)
- [当前状态](../status.md)
- [Current program](../../contracts/runtime-program/current-program.json)

当前 OPL substrate adapter/export 入口：

- `product-entry-manifest.opl_substrate_adapter_export`
- `product sidecar export` 输出内的 `sidecar_export.opl_substrate_adapter_export`

该导出面只给 OPL 消费 opaque workspace refs、source JSON pointer refs、artifact locator/index refs、memory locator/receipt refs、lifecycle receipt refs 与 projection refs。grant truth、fundability verdict、authoring quality verdict、submission-ready export verdict、package body、memory body 和 owner receipt authority 继续由 MAG 持有。
