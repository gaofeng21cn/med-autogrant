# MAG docs portfolio coverage ledger

Owner: `Med Auto Grant`
Purpose: `docs_portfolio_coverage_ledger_index`
State: `historical_archive_index`
Machine boundary: 本文是人读历史 coverage ledger 索引。当前机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API 行为、runtime receipts、owner receipts、typed blockers 和语义化 `human_doc:*` id。

## 读法

本目录只保留 MAG docs portfolio、private-surface、runtime/entrypoint retirement 和 no-resurrection 的压缩 provenance。历史过程按主题保留，不维护逐日 closeout 长清单。若某条历史结论仍有当前规则价值，先折回 `docs/docs_portfolio_consolidation.md`、核心五件套、active gap plan、private inventory、spec lifecycle map、contract/schema/source/test owner 或 runtime receipt，再把过程记录压缩在本目录。

这些材料不能作为 MAG 当前 active gap plan、runtime owner、grant readiness、submission readiness、production readiness、App/workbench consumption、owner delete authorization、keep-as-authority-adapter authorization 或 physical-delete authority。

## Single Source Of Truth

| Theme | Current owner |
| --- | --- |
| 当前完成口径、功能/结构差距、测试/证据差距、下一轮 prompt | `docs/active/mag-ideal-state-cross-repo-gap-plan.md` |
| per-surface private implementation / physical morphology inventory | `docs/active/opl-private-implementation-migration-inventory.md` |
| 文档生命周期、目录职责、direct-retirement posture、long-list governance | `docs/docs_portfolio_consolidation.md` |
| 当前状态和 evidence boundary | `docs/status.md` |
| runtime owner、architecture split、no-resurrection invariants、active decisions | `docs/project.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md` |
| active specs / support specs lifecycle | `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md` |
| MAG north-star / OPL adoption / series governance checklist | `docs/references/**` |
| product/delivery/source/runtime thin support | `docs/product/README.md`, `docs/delivery/README.md`, `docs/source/README.md`, `docs/runtime/README.md` |
| machine truth and retirement guards | `contracts/runtime-program/current-program.json`, private surface contracts, Foundry series contract, product-entry manifest / functional audits, source, CLI/API behavior, tests, runtime receipts |
| Retired surface no-resurrection provenance | [`retired-surface-provenance.md`](./retired-surface-provenance.md) |

## Compressed Provenance

| Provenance group | Current read |
| --- | --- |
| Docs lifecycle and coverage | Dated coverage ledger、frozen inventory、doctor transcript、worktree closeout、proof-by-proof table 不作为当前 truth 维护；本索引只保留主题级 coverage 与 reopen 入口。 |
| Retired command / module / facade / helper / test tails | `retired-surface-provenance.md` 保留 no-resurrection rules 和 current owner refs。Old runtime command family、helper shims、private re-export facade、dynamic export lists、test star facades、stale test-level facade closeouts、package root facades、Sentrux runtime facade、patch bridge、legacy flat aliases 和 compatibility aggregate tests 已压缩。 |
| Default caller / physical delete / evidence gates | 当前读法回到 active plan、private inventory、private surface contracts、Foundry series policy、product-entry manifest、source/tests、runtime receipts 和 OPL read-model。Observed prerequisites do not authorize physical delete. |
| Product / runtime / delivery / source support | 当前 support 只保留 thin index 与 owner pointers。Dated no-rewrite / SSOT closeout 不再作为入口文件维护；durable rules 已折回 owner docs 或 machine surfaces。 |
| Specs and history bodies | Dense dated specs 通过 `docs/specs/specs_lifecycle_map.md` 和 `docs/history/specs/README.md` 读取。Historical files with `Current Truth` titles are provenance unless a current owner explicitly promotes a subsection. |

## Coverage Summary

| Theme | Current coverage | Remaining scope / next write |
| --- | --- | --- |
| MAG docs portfolio scope | Root `README*`, `docs/*.md`, `docs/active/*.md`, `docs/public/*.md`, `docs/product/*.md`, `docs/runtime/*.md`, `docs/delivery/*.md`, `docs/source/*.md`, `docs/policies/*.md`, `docs/specs/*.md`, `docs/references/**/*.md` and `docs/history/docs-portfolio-coverage-ledger/*.md` have lifecycle roles routed through `docs/docs_portfolio_consolidation.md`, specs lifecycle maps, this coverage ledger and retired-surface provenance. | Reopen a precise document body only when a fresh scan finds active-looking checklist text, reusable prompt material, current-owner conflict, stale SSOT duplication or machine surface dependence on historical prose. |
| Active truth owners | `docs/active/mag-ideal-state-cross-repo-gap-plan.md` remains the only active gap / completion owner. `docs/active/opl-private-implementation-migration-inventory.md` remains the private surface-id and path-level implementation owner. `docs/specs/specs_lifecycle_map.md` owns dense spec lifecycle; this file only keeps coverage provenance. | New private-inventory refreshes should start from `contracts/private_functional_surface_policy.json` surface ids, then fold concrete source/test/workflow/package retirement candidates into the active inventory or retired-surface provenance. Production/default-caller evidence tails remain active work under the active plan, not this history ledger. |
| Content-level consolidation | Active-shell SSOT, Foundry command-surface field retirement, authoring-route history, foundation history, P2/P3/P4 authoring-review-verification history, runtime-first / post-R5A / P5 future activation history, Hermes/upstream provider-proof history, hosted caller / product-entry support history, product/runtime/delivery/source/policies thin-support indexes, specs lifecycle map and history specs index are represented by the provenance groups above and owner docs. Detailed deletion / field-retirement facts stay recoverable from git history and `retired-surface-provenance.md`; current rules stay in owner docs and machine surfaces. | Do not add file-by-file closeout logs here. If a historical rule is still current, fold it back into the owner doc, spec lifecycle map, contract, source or test before compressing the process trace. |
| Retired / guarded surfaces | This ledger records no source, contract, test, workflow, package or CLI/API deletion authority by itself. Guarded retired surfaces remain `run-local`, `runtime-run`, `runtime-resume`, `probe-upstream-hermes`, active `frontdoor` fields/help wording, local journal / attempt ledger, Gateway/local-manager default path, flat aliases, facades, patch bridge, stale test-level facade closeouts, compatibility aggregate tests and physical-delete-by-read-model claims. | Concrete retirement lanes need no-active-caller, replacement owner, MAG owner receipt / typed blocker roundtrip, no-forbidden-write proof and tombstone/provenance pointer before physical delete or test/interface retirement. |
| Parent OPL series goal | Active/support specs and product/runtime/delivery/source/policies thin-support bodies are covered by their directory indexes and `docs/specs/specs_lifecycle_map.md`; historical specs are covered by `docs/history/specs/README.md` for docs lifecycle purposes. This is a tranche-level foldback, not six-repo completion. | Next write scope is one precise SSOT theme, a triggered spec/history-body reopening or one physical-delete candidate. Do not expand this ledger or the active gap plan back into dated proof logs or path-level shell inventories. |
