# MAG docs portfolio coverage ledger

Owner: `Med Auto Grant`
Purpose: `docs_portfolio_coverage_ledger_index`
State: `historical_archive_index`
Machine boundary: 本文是人读历史 coverage ledger 索引。当前机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API 行为、runtime receipts、owner receipts、typed blockers 和语义化 `human_doc:*` id。

## 读法

本目录只保留 MAG docs portfolio、private-surface、runtime/entrypoint retirement 和 no-resurrection 的压缩 provenance。历史过程按主题保留，不再维护逐日 closeout 长清单。若某条历史结论仍有当前规则价值，先折回 `docs/docs_portfolio_consolidation.md`、核心五件套、active gap plan、private inventory、spec lifecycle map、contract/schema/source/test owner 或 runtime receipt，再把过程记录压缩在本目录。

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

| Provenance group | What remains here | What moved out |
| --- | --- | --- |
| Docs lifecycle and coverage | 本索引只记录 current owner、coverage snapshot 和 reopen 入口。 | Dated coverage ledger、frozen inventory、doctor transcript、worktree closeout、proof-by-proof table 不再以单独 Markdown 文件维护。 |
| Retired command / module / facade / helper / test tails | `retired-surface-provenance.md` 保留 no-resurrection rules 和 current owner refs。 | old runtime command family、helper shims、private re-export facade、dynamic export lists、test star facades、package root facades、Sentrux runtime facade、patch bridge、legacy flat aliases 和 compatibility aggregate tests 的 closeout 文件已压缩。 |
| Default caller / physical delete / evidence gates | 当前读法回到 active plan、private inventory、private surface contracts、Foundry series policy、product-entry manifest、source/tests、runtime receipts 和 OPL read-model。 | dated default-caller, physical-delete, consumer audit, active inventory, package/export, source/workspace, executor receipt 和 owner-decision closeout 不再作为当前 truth 保存。 |
| Product / runtime / delivery / source support | 当前 support 只保留 thin index 与 owner pointers。 | dated no-rewrite / SSOT closeout 不再作为入口文件维护； durable rules 已折回 owner docs 或 machine surfaces。 |

## Coverage Snapshot

2026-06-08 MAG coverage-ledger compression tranche:

- Reviewed: `AGENTS.md`, `TASTE.md`, `README*`, `docs/README.md`, `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`, `docs/docs_portfolio_consolidation.md`, `docs/active/mag-ideal-state-cross-repo-gap-plan.md`, `docs/active/opl-private-implementation-migration-inventory.md`, `docs/history/README.md`, previous `docs/history/docs-portfolio-coverage-ledger/*.md`, `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `package`/verification metadata, and exact contract/source/test references to dated coverage-ledger files.
- Edited: `docs/history/docs-portfolio-coverage-ledger/README.md`, `docs/history/docs-portfolio-coverage-ledger/retired-surface-provenance.md`, `docs/docs_portfolio_consolidation.md`.
- Compressed / deleted: previous dated MAG docs-portfolio coverage ledger Markdown files under `docs/history/docs-portfolio-coverage-ledger/`, after durable conclusions were folded into current owners above or into `retired-surface-provenance.md`.
- Unreviewed in this tranche: non-ledger MAG docs were read for SSOT alignment and stale dated-reference cleanup only. Full line-by-line governance of all MAG docs remains open under the parent OPL series goal unless covered by prior accepted tranches.
- Remaining stale / retire candidates in MAG coverage ledger: none identified after compression. Open MAG work remains the active evidence/physical-delete tails already listed in `docs/active/mag-ideal-state-cross-repo-gap-plan.md`.
- Next write scope: continue SSOT-first compression on the remaining clean sibling repo, then return to dirty `one-person-lab` and `med-autoscience` only when their concurrent write sets are safe to absorb or disjoint.
