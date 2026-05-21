# Runtime 文档

Owner: `MedAutoGrant`
Purpose: `grant_runtime_support`
State: `active_support`
Machine boundary: 人读索引。Runtime truth 继续归 contracts、schemas、source、current-program records、runtime evidence 与 owner receipts。

本目录承接 MAG runtime/control/projection 支撑和 direct/hosted 边界说明。任务启动后的默认运行 owner 是 OPL/Temporal hosted autonomous runtime；通用 runtime primitive 的 owner 是 OPL Framework / shared family layer；MAG 只保留 grant-domain handler、refs-only projection、owner receipt、typed blocker 和 authority refs。

当前本目录只做 runtime/control/projection 支撑索引；不复制核心五件套、active plan 或 contract 中的 runtime 状态。新增内容只能解释 MAG 如何把 descriptor、projection、sidecar receipt、owner receipt、typed blocker 和 refs-only evidence 交给 OPL；不能把 product-entry、sidecar、domain_runtime、runtime registration、lifecycle adapter、workbench/scheduler metadata 写成 MAG-owned generic runtime。

当前入口先看：

- [架构](../architecture.md)
- [当前状态](../status.md)
- [Current program](../../contracts/runtime-program/current-program.json)

当前 OPL provider / substrate refs-only export 入口：

- `product-entry-manifest.opl_provider_runtime_contract`
- `product-entry-manifest.source_provenance`
- `product-entry-manifest.opl_substrate_adapter_export`
- `product sidecar export` 输出内的 `sidecar_export.source_provenance`
- `product sidecar export` 输出内的 `sidecar_export.opl_substrate_adapter_export`

这些导出面只给 OPL 消费 opaque workspace refs、body-free source provenance refs、source JSON pointer refs、artifact locator/index refs、memory locator/receipt refs、lifecycle receipt refs、runtime_control refs 与 projection refs。grant truth、fundability verdict、authoring quality verdict、submission-ready export verdict、package body、memory body 和 owner receipt authority 继续由 MAG 持有。`source_provenance` 是 OPL `substrate projections` 可直接解析的顶层 source refs surface；它不让 MAG 持有通用 workspace/source intake shell、runtime、workbench、ledger 或 scheduler。

已退役的 local journal、attempt ledger、`runtime-run` / `runtime-resume`、Hermes/Gateway/local-manager probe 和 compatibility alias 只从 `docs/history/**` 或 tombstone/provenance 语境阅读；不得写回 current runtime owner。

MAG 不内置 daemon、scheduler、attempt loop 或 attempt ledger。`Codex CLI` 是默认 stage executor，不是默认 task runtime owner；持久在线调度、唤醒、retry、resume 和 provider residency 由 OPL/Temporal 承担。
