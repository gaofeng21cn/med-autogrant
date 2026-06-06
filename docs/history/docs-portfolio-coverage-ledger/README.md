# MAG docs portfolio coverage ledger

Owner: `Med Auto Grant`
Purpose: `docs_portfolio_coverage_ledger_index`
State: `history_index`
Machine boundary: 本文是人读历史 coverage ledger 索引。当前机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API 行为、runtime receipts 和语义化 `human_doc:*` id。

本目录保存从 active governance 文档移出的 dated docs coverage、frozen inventory、proof/read-model 折返和 no-retirement 过程记录。它们只说明当时如何审计和折回结论，不作为 MAG 当前 active gap plan、runtime owner、grant readiness、submission readiness、production readiness 或 physical-delete authority。

当前 MAG docs lifecycle truth 回到：

- [MAG 文档组合治理](../../docs_portfolio_consolidation.md)
- [MAG 当前状态](../../status.md)
- [MAG ideal-state cross-repo gap plan](../../active/mag-ideal-state-cross-repo-gap-plan.md)
- [Specs 生命周期地图](../../specs/specs_lifecycle_map.md)
- `contracts/runtime-program/current-program.json`

## Ledger

| 文件 | 内容 | 当前读法 |
| --- | --- | --- |
| [2026-06-06-mag-active-inventory-longlist-no-rewrite-closeout.md](./2026-06-06-mag-active-inventory-longlist-no-rewrite-closeout.md) | MAG active plan / private inventory 长清单压缩问题的 no-rewrite SSOT closeout。 | 只读 provenance；当前 active gap truth 继续归 active plan，per-surface private inventory truth 继续归 private inventory，机器 gate 继续归 private surface policy、Foundry Agent series policy、current-program、product-entry manifest、source/tests 和 runtime receipts。 |
| [2026-06-06-mag-runtime-topology-project-overview-ssot-closeout.md](./2026-06-06-mag-runtime-topology-project-overview-ssot-closeout.md) | MAG runtime topology 与 project overview role boundary 的 SSOT closeout。 | 只读 provenance；当前 runtime topology truth 继续归 `current-program.json`、product-entry manifest/private surface contracts、`docs/status.md`、`docs/architecture.md`、`docs/invariants.md`、active gap plan、private inventory、source/tests 和 runtime receipts。 |
| [2026-06-06-mag-private-physical-delete-ssot-closeout.md](./2026-06-06-mag-private-physical-delete-ssot-closeout.md) | MAG private implementation residue、physical-delete gate 与 direct-retirement posture 的 SSOT closeout。 | 只读 provenance；当前 physical-delete truth 继续归 active gap plan、private inventory、private surface policy、Foundry Agent series policy、product-entry manifest / functional audit、source/tests、runtime receipts 和 MAG owner receipts / typed blockers。 |
| [2026-06-06-mag-sentrux-runtime-facade-retirement-closeout.md](./2026-06-06-mag-sentrux-runtime-facade-retirement-closeout.md) | MAG Sentrux sidecar 中已不存在 `src/med_autogrant/hermes_runtime.py` 对应 `runtime_facade` layer 的退役 closeout。 | 只读 provenance；当前结构边界继续归 `.sentrux/rules.toml`、source tree、tests、Sentrux advisory gate 和 runtime owner contracts。 |
| [2026-06-06-mag-package-export-support-readout-ssot-closeout.md](./2026-06-06-mag-package-export-support-readout-ssot-closeout.md) | MAG package/export support current-truth readout 的 SSOT closeout。 | 只读 provenance；当前 package/export truth 继续归 MAG package authority source、package/export gate、stage control plane、private surface policy、package lifecycle handoff projection、owner receipts 和 typed blockers。 |
| [2026-06-06-mag-delivery-package-lifecycle-ssot-closeout.md](./2026-06-06-mag-delivery-package-lifecycle-ssot-closeout.md) | MAG delivery/package lifecycle route、domain entry command contract 与 canonical export surface 测试侧第二真相源清理 closeout。 | 只读 provenance；当前 delivery/package lifecycle truth 继续归 MAG package authority source、domain entry / route / operator contract builders、CLI/API behavior、runtime receipts 和 MAG owner physical-delete gate。 |
| [2026-06-06-mag-source-workspace-lifecycle-ssot-closeout.md](./2026-06-06-mag-source-workspace-lifecycle-ssot-closeout.md) | MAG source/workspace/file lifecycle policy、source refs support index 与 OPL-owned workspace/source shell boundary 的 SSOT closeout。 | 只读 provenance；当前 source/workspace lifecycle truth 继续归 `contracts/workspace_lifecycle_policy.json`、`contracts/runtime-program/opl-family-contract-adoption.json#source_provenance`、`product-entry-manifest.source_provenance`、source/domain-handler tests、CLI/API behavior 和 MAG owner receipts / typed blockers。 |
| [2026-06-06-mag-product-entry-package-authority-ssot-closeout.md](./2026-06-06-mag-product-entry-package-authority-ssot-closeout.md) | MAG product-entry public bridge、product/delivery support 指针与 package/canonical pointer authority 的 SSOT closeout。 | 只读 provenance；当前 product-entry/package support truth 继续归 `docs/specs/product-entry-support-record.md`，机器 authority truth 继续归 `product_entry_contract_api.py`、stage control source、`contracts/stage_control_plane.json`、product-entry tests、CLI/API behavior 和 MAG owner receipts / typed blockers。 |
| [2026-06-06-mag-executor-receipt-boundary-ssot-closeout.md](./2026-06-06-mag-executor-receipt-boundary-ssot-closeout.md) | MAG `codex_cli` 默认 executor 与显式非默认 `hermes_agent` receipt/proof lane 的 SSOT 治理 closeout。 | 只读 provenance；当前 executor truth 继续归 `current-program.json`、private surface policy、source/tests 与 active specs lifecycle owner。 |
| [2026-06-04-mag-retired-command-family-audit.md](./2026-06-04-mag-retired-command-family-audit.md) | MAG 旧 public/domain-entry runtime command family 的 coverage 与 retirement audit。 | 只读 provenance；当前 no-resurrection truth 继续归 source/tests/contracts 与 active gap plan。 |
| [2026-06-02-mag-docs-portfolio-coverage-ledger-archive.md](./2026-06-02-mag-docs-portfolio-coverage-ledger-archive.md) | 原 `docs/docs_portfolio_consolidation.md` 中的 MAG dated coverage ledger。 | 只读 provenance；durable 规则已折回 active governance、core docs、active gap plan、spec lifecycle map、contracts/source/tests。 |
