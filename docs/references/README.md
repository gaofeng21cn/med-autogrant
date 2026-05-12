# References Guide

[中文](./README.zh-CN.md)

This directory holds reference material for `Med Auto Grant`.

Lifecycle:

- `owner`: MAG maintainers and the cross-repo lane that owns the referenced boundary.
- `purpose`: preserve stable explanatory notes for OPL handoff, family contracts, runtime layering, and documentation governance.
- `state`: `reference`.
- `machine boundary`: human-readable only. Machine-readable surfaces must use contracts, schemas, source paths, or semantic `human_doc:*` ids.

Reference notes should not replace current product truth. Current MAG grant product truth remains in the core docs, active specs, and `contracts/runtime-program/current-program.json`.

Historical/provider-specific handoff notes that no longer explain a current boundary have been moved to [History archive](../history/README.md). In particular, the old OPL Runtime Manager three-layer note and the older lightweight product-entry handoff note now live under `docs/history/` because their current content is absorbed by the core docs, `OPL Family Contract Adoption`, and the active specs map.

Current reference entries:

- [Grant Strategy Memory Policy](./grant_strategy_memory_policy.md): explains how fundability, specific aims, reviewer grammar, and template-strategy experience should be kept as natural-language memory while quality/controller/export surfaces remain structured authority.
- [OPL Family Contract Adoption](./opl_family_contract_adoption.md): explains how MAG exposes descriptors and projections to the OPL stage-led runtime framework with Agent executors as the minimum execution unit while retaining grant truth, quality, route, and export authority.
