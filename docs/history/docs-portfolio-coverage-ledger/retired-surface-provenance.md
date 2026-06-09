# MAG Retired Surface Provenance

Owner: `Med Auto Grant`
Purpose: `retired_surface_no_resurrection_provenance`
State: `historical_provenance`
Machine boundary: 本文只压缩记录已退役 surface、dated coverage foldback 和 no-resurrection 规则。当前机器真相继续归 `contracts/runtime-program/current-program.json`、schemas、source、CLI/API behavior、runtime receipts、owner receipts、typed blockers、private surface contracts、Foundry series policy、product-entry manifest、tests 和语义化 `human_doc:*` id。

## Current Owner Map

| Theme | Current owner |
| --- | --- |
| MAG active gap / physical-delete gate / evidence tail | `docs/active/mag-ideal-state-cross-repo-gap-plan.md` |
| per-surface private implementation inventory | `docs/active/opl-private-implementation-migration-inventory.md` |
| docs lifecycle and direct-retirement posture | `docs/docs_portfolio_consolidation.md` |
| runtime owner and non-ready status | `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md` |
| specs lifecycle | `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md`, `docs/history/specs/README.md` |
| product-entry/package support | `docs/specs/product-entry-support-record.md`, product-entry source/tests, stage control source/contracts |
| source/workspace lifecycle | `contracts/workspace_lifecycle_policy.json`, OPL family contract adoption source provenance, product-entry manifest, source/domain-handler tests |
| package/export authority | MAG package authority source, stage control plane, package/export gates, owner receipts, typed blockers |
| default caller / physical delete / direct retirement machine gates | `contracts/private_functional_surface_policy.json`, `contracts/foundry_agent_series.json`, `contracts/runtime-program/current-program.json`, product-entry manifest / functional audit, source/tests, OPL read-model |

## Retired Surfaces

| Retired surface | Current replacement / evidence | No-resurrection rule |
| --- | --- | --- |
| old public/domain-entry runtime commands: `run-local`, `runtime-run`, `runtime-resume`, `probe-upstream-hermes` | grouped public CLI catalog, service-safe domain command catalog, `src/med_autogrant/mainline_status.py`, `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`, `tests/test_domain_entry.py`, current-program runtime owner fields, active plan no-resurrection tail, and the runtime-first R1-R5 compression record in `docs/history/specs/README.md` | Do not restore flat runtime commands, local journal owner, attempt ledger, Hermes probe, Gateway/local-manager default path, hosted runtime claim, or compatibility public command aliases. |
| Foundry Agent active `frontdoor` projection fields and help wording: `status.public_frontdoor`, `status.executable_frontdoors`, `interfaces.ordinary_public_frontdoor_spine`, `validation.checked_frontdoor_operations`, `missing_frontdoor_operation:*`, and executable frontdoor help text | MAG Foundry command-surface projection in `src/med_autogrant/foundry_series_cli.py`, `src/med_autogrant/cli.py`, grouped public command routing, root README quickstart, `docs/architecture.md`, and `tests/test_cli_smoke.py` | Do not restore active CLI JSON/help/test/status wording under `frontdoor`. Historical `frontdoor` text may remain only in history/provenance or no-resurrection/negative-guard context. |
| local runtime journal, attempt ledger, repo-owned scheduler/daemon, Gateway/local-manager default path | OPL/Temporal runtime owner, typed queue/attempt ledger outside MAG, current-program, active plan, status, source/tests | MAG may keep domain handler / refs-only adapter / minimal authority functions; it must not recreate a generic runtime platform or local-manager compatibility route. |
| helper shims: source-side test convenience helper, identity command normalizer, hosted-contract bundle one-line private wrapper | grouped command catalog, service-safe command catalog, split IO owner helpers, schemas/source/tests, CLI/API behavior | Do not reintroduce wrapper helpers or one-line private facades as compatibility convenience. |
| package root / private re-export facades in product-entry parts and consumer thinning audit | concrete owner modules, direct imports, source tree, structure tests, CLI/API behavior | Do not restore package-root lazy `MedAutoGrantProductEntry` re-export, builder re-export facades, private `_build_*` re-export surfaces, or import-shortcut compatibility paths. |
| dynamic private-name export lists in product-entry public bridge and test support | explicit public bridge export list, explicit test imports, helper definitions, dependency-structure tests | Do not restore `__all__` as a dynamic private-name or star-import surface. Tests and callers import concrete helpers. |
| test-side `import *` facades in CLI validate and product-entry test support | explicit test imports, helper definition modules, repository hygiene guard, source tree, CLI/API behavior | Do not restore star facades, dynamic test support exports, or compatibility aggregate imports. |
| stale test-level facade negative assertions: `facade_exports.py` absence check, `_render_text` re-export absence check, and duplicated workspace-index facade helper closeout | `tests/test_workspace_index.py`, CLI/output behavior tests, `cli_rendering_parts` owner module, dependency-structure tests, domain-runtime split tests, runtime CLI structural helper tests, repository hygiene guard, source tree | Do not recreate per-tranche stale-test closeout docs or prose-oracle tests for already covered facade absence. Current behavior and no-resurrection policy must be tested through concrete owner modules, contracts, source scans, and focused structure guards. |
| Sentrux `runtime_facade` layer for missing `src/med_autogrant/hermes_runtime.py` | `.sentrux/rules.toml`, source tree, tests, Sentrux advisory gate, runtime owner contracts | Do not recreate a Hermes runtime facade just to satisfy advisory architecture categories. |
| `product-entry` / `domain_runtime` stale aggregate exports and `domain_runtime_parts.patch_targets` patch bridge | source tree, `substrate.__all__`, structure tests, CLI/API behavior, runtime receipts, private inventory | Do not restore aggregate re-export, patch bridge, facade target, or compatibility-only tests after active caller migration. |
| dated `human_doc:*` hosted/proof/handoff ids as active truth surfaces | `human_doc:product_entry_support_record`, specs lifecycle map, history specs, current-program no-resurrection guards | Do not put historical dated ids back into current-program active truth surfaces or source-owned active maintainer refs. |
| default caller deletion as automatic physical-delete authority | active plan, private inventory, private surface policy, Foundry series policy, current-program, OPL read-model, MAG owner delete / keep-as-authority-adapter / typed blocker receipt | Observed default caller prerequisites do not authorize physical delete. Require explicit MAG owner receipt and all no-active-caller / parity / no-forbidden-write gates. |
| no-rewrite / SSOT closeout files as current truth | core docs, active plan, private inventory, specs lifecycle map, contracts/source/tests/CLI/API/runtime receipts | Do not link per-tranche closeouts as current evidence. Durable conclusions must live in current owners; this file keeps compressed provenance. |
| grant readiness, submission readiness, production readiness, App/workbench consumption, long-soak completion inferred from docs, refs-only accounting, schema completeness, package existence, provider completion, grouped CLI success, or product-entry manifest success | MAG owner receipts, typed blockers, real human gate receipts, sustained App/operator consumption, Temporal long-soak evidence, source/test/runtime receipts | Do not upgrade structural/read-model proof into grant/fundability/quality/export/submission/production ready claims. |

## Evidence Boundary

This provenance can prove retired-surface intent, current owner refs, and no-resurrection rules. It cannot prove grant readiness, fundability readiness, quality/export verdict, submission-ready approval, production readiness, App/workbench sustained consumption, Temporal long-soak completion, owner delete authorization, keep-as-authority-adapter authorization, or physical-delete authority.

When a retired surface becomes necessary again, reopen the relevant current owner contract, source module, test, CLI/API behavior, active owner doc, private inventory, runtime receipt, or owner receipt first. Do not restore it as compatibility, fallback, alias, facade, wrapper, star import, dynamic export, prose oracle, aggregate test, patch bridge, or process-history shortcut.
