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

2026-06-08 MAG public-doc support lifecycle tranche:

- Theme / SSOT: public repository and docs-public narrative support. Public
  first entry remains root `README.md` / `README.zh-CN.md`; docs-public support
  remains `docs/public/README.md`, `docs/public/domain-positioning.md` and
  `docs/public/mvp-scope.md`. Current technical status, runtime owner,
  active evidence gates and grant-readiness boundaries remain the core five
  docs, `docs/active/mag-ideal-state-cross-repo-gap-plan.md`,
  `docs/docs_portfolio_consolidation.md`,
  `contracts/runtime-program/current-program.json`, source/CLI/API behavior and
  focused tests.
- Reviewed: `README.md`, `README.zh-CN.md`, `docs/README.md`,
  `docs/public/README.md`, `docs/public/domain-positioning.md`,
  `docs/public/mvp-scope.md`, `docs/project.md`, `docs/status.md`,
  `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`,
  `docs/docs_portfolio_consolidation.md`,
  `docs/active/mag-ideal-state-cross-repo-gap-plan.md`,
  `contracts/runtime-program/current-program.json`, specs lifecycle public
  identity references, and this coverage ledger.
- Edited: this file only.
- Coverage result: MAG public docs already have one role each. Root README
  files remain public entries; `docs/public/README.md` remains a public support
  index; `domain-positioning.md` explains MAG public identity / OPL-provider
  boundary; `mvp-scope.md` explains NSFC MVP scope and non-goals. They do not
  carry active runtime truth, production readiness, App/workbench consumption,
  grant-ready, fundability-ready, quality/export-ready or submission-ready
  verdicts.
- Retired / guarded: no public doc was retired. The guarded stale surfaces are
  old hosted caller proof, public hosted runtime, Gateway/local-manager,
  `runtime-run` / `runtime-resume`, flat public aliases and compatibility
  product/workbench wording; current public docs either omit them or keep them
  under explicit history / active-evidence-gate language.
- Remaining MAG unreviewed scope under the parent OPL series goal: active/support
  spec bodies, individual historical spec bodies, reference docs beyond public
  identity pointers, active private inventory details and physical-delete
  evidence tails remain open unless covered by another accepted tranche.
- Next write scope: continue with a concrete SSOT theme after fresh intake,
  likely reference docs, active/support specs body governance, physical-delete
  evidence tails, or a clean sibling repo lane.

2026-06-08 MAG product/runtime/delivery/source/policies thin-support lifecycle tranche:

- Theme / SSOT: thin support indexes for product entry, runtime projection,
  delivery/export, source/workspace and stable policy docs. Current SSOT remains
  the core five docs, `docs/active/mag-ideal-state-cross-repo-gap-plan.md`,
  `docs/specs/product-entry-support-record.md`, `docs/specs/README.md`,
  `docs/specs/specs_lifecycle_map.md`,
  `contracts/runtime-program/current-program.json`,
  `contracts/workspace_lifecycle_policy.json`, product-entry manifests,
  source/CLI/API behavior and focused tests.
- Reviewed: `AGENTS.md`, `TASTE.md`, `docs/docs_portfolio_consolidation.md`,
  `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`,
  `docs/decisions.md`, `docs/active/mag-ideal-state-cross-repo-gap-plan.md`,
  `docs/product/README.md`, `docs/runtime/README.md`,
  `docs/delivery/README.md`, `docs/source/README.md`,
  `docs/policies/README.md`, `docs/specs/product-entry-support-record.md`,
  `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`,
  `contracts/runtime-program/current-program.json`,
  `contracts/workspace_lifecycle_policy.json`, product-entry / runtime /
  package lifecycle / source provenance source refs, and this coverage ledger.
- Edited: this file only.
- Coverage result: the five support README files are already thin indexes. They
  point readers back to the current owner docs and machine surfaces instead of
  carrying package/export gates, runtime status, workspace truth, stable policy
  rules, dated proof logs, or product-entry manifests as prose copies. No
  support README should be expanded into a parallel active owner while the
  SSOTs above remain current.
- Retired / guarded: no file, command, contract, source module, test, or support
  README was retired in this tranche. The guarded stale surface is the temptation
  to treat these thin indexes as second truth sources for grant readiness,
  submission readiness, App/workbench consumption, runtime ownership, package
  authority, source truth, or policy enforcement. Keep old runtime commands,
  Gateway/local-manager wording, facade/alias/wrapper residue and compatibility
  tests confined to no-resurrection or history/provenance context.
- Remaining MAG unreviewed scope under the parent OPL series goal: full
  line-by-line semantic governance of active spec bodies, individual historical
  spec bodies, reference docs, public docs, active private inventory details and
  physical-delete evidence tails remains open unless covered by a prior accepted
  tranche.
- Next write scope: continue with a concrete SSOT theme after fresh intake,
  likely active/support specs body governance, reference docs, public docs, or a
  clean sibling repo lane. Do not use this thin-support review as proof that
  every product/runtime/delivery/source/policy-related historical spec body has
  been line-reviewed.

2026-06-08 MAG historical-specs index compression tranche:

- Theme / SSOT: historical specs entry and direct-reader lifecycle guard. Current SSOT is `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/history/specs/README.md`, and machine truth references in `contracts/runtime-program/current-program.json`, `contracts/private_functional_surface_policy.json`, `contracts/stage_run_kernel_profile.json`, `src/med_autogrant/opl_standard_pack.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, and focused tests that retain the Hermes-native tombstone path.
- Reviewed: `AGENTS.md`, `TASTE.md`, `docs/docs_portfolio_consolidation.md`, `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/history/specs/README.md`, this coverage ledger, `docs/history/docs-portfolio-coverage-ledger/retired-surface-provenance.md`, history-specs directory inventory, `contracts/runtime-program/current-program.json`, `contracts/private_functional_surface_policy.json`, `contracts/stage_run_kernel_profile.json`, `src/med_autogrant/opl_standard_pack.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, and the tests that assert the path-stable Hermes-native critique proof tombstone.
- Edited: `docs/history/specs/README.md` and this file.
- Coverage result: the historical specs directory contains 70 Markdown files including `README.md`. The README now keeps a semantic theme index instead of a date/pattern long list. Active/support spec truth remains in `docs/specs/README.md` and `docs/specs/specs_lifecycle_map.md`; historical files stay provenance even when their titles contain `Current Truth`.
- Retired / guarded: no file was moved or deleted in this tranche. Path-stable tombstone refs such as `docs/history/specs/2026-04-13-hermes-native-critique-proof-tombstone.md` remain machine evidence refs and do not authorize restoring Hermes-native, Gateway, local-runtime, hosted runtime, or compatibility command surfaces.
- Remaining MAG unreviewed scope under the parent OPL series goal: full line-by-line semantic governance of individual historical spec bodies remains open, along with product/runtime/delivery/source thin support docs, active specs beyond already reviewed support guards, and physical-delete evidence tails.
- Next write scope: continue with a concrete SSOT theme; likely candidates are product/runtime/delivery/source thin support docs or individual history spec body tombstones. Do not use this compression as proof that every historical spec body has been line-reviewed.

2026-06-08 MAG Progress-First domain-alias semantic audit tranche:

- Theme / SSOT: `grant_work_progress` and `platform_evidence_progress` under the OPL family Progress-First delta contract. Machine SSOT is `contracts/foundry_agent_series.json`, `src/med_autogrant/stage_control_plane.py`, `src/med_autogrant/product_entry_parts/progress_projection_helpers.py`, `schemas/v1/grant-progress.schema.json`, `contracts/stage_control_plane.json`, and focused product-entry / stage-control tests.
- Reviewed: `docs/decisions.md`, `docs/active/mag-ideal-state-cross-repo-gap-plan.md`, `contracts/foundry_agent_series.json`, `contracts/stage_control_plane.json`, `schemas/v1/grant-progress.schema.json`, `src/med_autogrant/stage_control_plane.py`, `src/med_autogrant/product_entry_parts/progress_projection_helpers.py`, `src/med_autogrant/opl_standard_pack.py`, `tests/product_entry_cases/test_status_start_cases.py`, `tests/product_entry_cases/test_progress_cockpit.py`, `tests/product_entry_cases/test_family_stage_control_plane.py`, and `tests/test_opl_family_contract_adoption.py`.
- Edited: this file only.
- Coverage result: these strings are current MAG domain aliases, not stale compatibility aliases. They map grant-facing progress and platform/evidence repair into canonical `deliverable_progress_delta`, `platform_repair_delta`, and `progress_delta_classification`, while tests assert owner and readiness boundaries. They must not be retired without a new machine contract replacing the domain-alias projection and focused tests.
- Retired / guarded: none in this tranche. The correct retirement target remains old runtime commands, wrapper/facade/patch-bridge residue, flat aliases, compatibility aggregate tests, and readiness claims from refs-only accounting; Progress-First MAG aliases stay active.
- Remaining MAG unreviewed scope under the parent OPL series goal: full semantic governance for non-Progress-First alias themes remains open, especially product/runtime/delivery/source thin support docs, active specs beyond already reviewed support guards, and physical-delete evidence tails.
- Next write scope: continue with another concrete SSOT theme after fresh intake; do not delete Progress-First domain aliases unless current contracts/source/tests first move to a replacement machine surface.

2026-06-08 MAG formal-entry / durability retired-command SSOT tranche:

- Theme / SSOT: formal-entry and durability support specs that mention retired runtime commands. Machine SSOT is `MedAutoGrantDomainEntry` behavior, grouped CLI catalogs, `src/med_autogrant/mainline_status.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, `tests/test_domain_entry.py`, `contracts/runtime-program/current-program.json`, and the active no-resurrection gates in `docs/active/mag-ideal-state-cross-repo-gap-plan.md`.
- Reviewed: `docs/specs/2026-04-07-formal-entry-matrix-current-truth.md`, `docs/specs/2026-04-07-durability-model-clarification.md`, `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/history/specs/README.md`, `docs/docs_portfolio_consolidation.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/active/mag-ideal-state-cross-repo-gap-plan.md`, `docs/active/opl-private-implementation-migration-inventory.md`, `docs/runtime/README.md`, `README*`, `src/med_autogrant/mainline_status.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, and negative guard tests for retired runtime commands.
- Edited: this file and `docs/history/docs-portfolio-coverage-ledger/retired-surface-provenance.md`.
- Coverage result: the two support specs are already lifecycle-guarded as `support_current_truth` and only mention `runtime-run`, `runtime-resume`, `probe-upstream-hermes`, and journal wording inside retired/history sections. They remain in `docs/specs/` as support guards rather than active runtime owners; no current MAG doc outside history authorizes a compatibility command surface.
- Retired / guarded: `run-local`, `runtime-run`, `runtime-resume`, and `probe-upstream-hermes` stay absent from active domain-entry/public command catalogs and are covered by fail-closed negative tests and retired-command scan refs. Provenance now points at the concrete source/test owners rather than only generic "negative tests" wording.
- Remaining MAG unreviewed scope under the parent OPL series goal: full line-by-line semantic governance for non-formal-entry/non-durability themes, especially product/runtime/delivery/source thin support docs, active specs beyond the two support guards, and physical-delete evidence tails. Functional and evidence gaps remain in `docs/active/mag-ideal-state-cross-repo-gap-plan.md`.
- Next write scope: continue with a clean sibling repo or another MAG theme only after fresh intake and a concrete SSOT; do not delete active handler/adapter shell without MAG owner delete receipt or typed blocker.

2026-06-08 MAG coverage-ledger compression tranche:

- Reviewed: `AGENTS.md`, `TASTE.md`, `README*`, `docs/README.md`, `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`, `docs/docs_portfolio_consolidation.md`, `docs/active/mag-ideal-state-cross-repo-gap-plan.md`, `docs/active/opl-private-implementation-migration-inventory.md`, `docs/history/README.md`, previous `docs/history/docs-portfolio-coverage-ledger/*.md`, `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `package`/verification metadata, and exact contract/source/test references to dated coverage-ledger files.
- Edited: `docs/history/docs-portfolio-coverage-ledger/README.md`, `docs/history/docs-portfolio-coverage-ledger/retired-surface-provenance.md`, `docs/docs_portfolio_consolidation.md`.
- Compressed / deleted: previous dated MAG docs-portfolio coverage ledger Markdown files under `docs/history/docs-portfolio-coverage-ledger/`, after durable conclusions were folded into current owners above or into `retired-surface-provenance.md`.
- Unreviewed in this tranche: non-ledger MAG docs were read for SSOT alignment and stale dated-reference cleanup only. Full line-by-line governance of all MAG docs remains open under the parent OPL series goal unless covered by prior accepted tranches.
- Remaining stale / retire candidates in MAG coverage ledger: none identified after compression. Open MAG work remains the active evidence/physical-delete tails already listed in `docs/active/mag-ideal-state-cross-repo-gap-plan.md`.
- Next write scope: continue SSOT-first compression on the remaining clean sibling repo, then return to dirty `one-person-lab` and `med-autoscience` only when their concurrent write sets are safe to absorb or disjoint.
