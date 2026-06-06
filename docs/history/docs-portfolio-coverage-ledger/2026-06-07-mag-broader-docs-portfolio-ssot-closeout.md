# MAG broader docs portfolio SSOT closeout

Owner: `Med Auto Grant`
Purpose: `broader_docs_portfolio_ssot_closeout`
State: `history_provenance`
Machine boundary: Human-readable governance closeout. Current machine truth stays in `contracts/runtime-program/current-program.json`, contracts, schemas, source, CLI/API behavior, product-entry manifest, runtime receipts, owner receipts, MAG grant authority surfaces and current owner docs. This document is not grant readiness, submission readiness, production readiness, OPL-hosted long-soak, App/workbench consumption, owner delete authorization, keep-as-authority-adapter authorization or physical-delete authority.

This file records the 2026-06-07 broader MAG docs portfolio SSOT coverage lane. The lane did not rewrite active/current docs because the current portfolio already has one owner split: lifecycle governance in `docs/docs_portfolio_consolidation.md`, docs navigation in `docs/README.md`, current project truth in the core five docs, current gaps in `docs/active/mag-ideal-state-cross-repo-gap-plan.md`, per-surface private implementation residue in `docs/active/opl-private-implementation-migration-inventory.md`, specs lifecycle in `docs/specs/README.md` and `docs/specs/specs_lifecycle_map.md`, and dated proof / closeout evidence in `docs/history/**`.

## Semantic Theme

The theme was whether any stale MAG module/interface/test/docs surface still appears as current truth after the recent product-entry, package/export, source/workspace, Sentrux, runtime-topology, active-inventory, default-caller, stale-export, consumer-audit, `human_doc:*` and governance-checklist lanes.

Scope covered:

- Root and near-root entries: `README.md`, `README.zh-CN.md`, `agent/README.md`, `contracts/README.md`, `runtime/README.md`.
- Docs index and lifecycle owner: `docs/README.md`, `docs/docs_portfolio_consolidation.md`.
- Core current docs: `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`.
- Active truth and inventory: `docs/active/mag-ideal-state-cross-repo-gap-plan.md`, `docs/active/opl-private-implementation-migration-inventory.md`.
- Public/product/runtime/delivery/source/policies/specs/references support docs.
- Existing process history index and recent closeouts under `docs/history/docs-portfolio-coverage-ledger/**`.
- MAG contracts, source and tests only as machine-truth cross-checks for physical-delete, readiness, long-soak and no-resurrection claims.

## Portfolio Classification

| Surface | Classification | Governance action |
| --- | --- | --- |
| Root `README*` | `public_entry` | Kept. Public identity stays user-facing and does not own runtime truth, grant readiness, production readiness or physical-delete authority. |
| `agent/README.md` | `declarative_pack_index` | Kept. It indexes grant pack semantics and explicitly excludes grant artifacts, receipt instances, memory bodies and readiness verdicts. |
| `contracts/README.md` | `machine_surface_index` | Kept. It points to contract surfaces and repeats no-ready / no-physical-delete boundaries for machine evidence. |
| `runtime/README.md` | `authority_function_index` | Kept. It explains runtime-facing authority anchors without turning repo source into runtime state or package body storage. |
| `docs/README.md` | `docs_entry_index` | Kept. It routes readers to owner docs and lifecycle governance rather than carrying a second current-truth ledger. |
| `docs/docs_portfolio_consolidation.md` | `lifecycle_governance_owner` | Kept. It owns directory roles, direct-retirement posture, long-list governance and history foldback rules. |
| Core five docs | `current_truth_owner` | Kept. They explain MAG role, owner split, evidence gates, non-goals and current decisions without proof ledgers. |
| `docs/active/mag-ideal-state-cross-repo-gap-plan.md` | `single_active_gap_owner` | Kept. It owns current gaps, evidence gates, next prompt and no-ready-overclaim posture. |
| `docs/active/opl-private-implementation-migration-inventory.md` | `private_inventory_owner` | Kept. It owns per-surface active caller, classification, retained authority, migration candidate and retirement gate. |
| `docs/public/product/runtime/delivery/source/policies/**` | `thin_support_index` | Kept. These directories provide support routing and do not duplicate machine truth. |
| `docs/specs/**` | `active_or_support_spec_layer` | Kept. Active/support subsections are read through `docs/specs/README.md` and `docs/specs/specs_lifecycle_map.md`; historical specs stay provenance only. |
| `docs/references/**` | `reference_support` | Kept. North-star, OPL adoption, memory policy and governance checklist are support material, not current status or lifecycle owner. |
| `docs/history/**` | `process_provenance` | Kept. It owns dated closeouts, old specs, old provider/runtime proof, coverage ledgers and tombstones. |

## Content-Level Consolidation

- Old `OPL Runtime Manager`, Gateway/federation, local-manager, local journal, attempt ledger, upstream Hermes default provider, flat shell aliases, facade patch bridge and compatibility aggregate tests remain bounded as history, tombstone, explicit proof history, regression oracle or negative guard material.
- Current product-entry, product-status, user-loop, domain-handler, grouped CLI, runtime/control projection and lifecycle shell are not compatibility promises or long-term MAG-owned platform surfaces. They are read as direct handler targets, refs-only adapters, minimal authority functions, diagnostics or migration inputs until MAG owner receipt / typed blocker / no-active-caller / direct-hosted parity evidence authorizes physical cleanup.
- `mag_functional_structure_gap_count=0` and `standard_agent_source_shape_status=landed` remain structure classification signals only; they do not mean strict source-purity, production/default caller completion, App/workbench sustained consumption or Temporal long-soak completion.
- `claims_domain_repo_physical_delete_authorized=false`, `claims_all_bridge_exits_complete=false` and `claims_production_long_run_soak_complete=false` remain the current machine boundary.
- `submission_ready_export_gate` remains a blocking human gate. Package existence, schema completeness, stage replay projection, OPL ledger verification, provider completion, grouped CLI success, product-entry manifest success or refs-only accounting closeout cannot become grant-ready, fundability-ready, quality-ready, export-ready or submission-ready evidence.
- No current doc scan showed a stale old public path compatibility claim, active Gateway/Hermes/local-manager runtime owner, compatibility alias/facade authorization, production-ready claim, grant-ready claim, submission-ready claim, physical-delete authorization or owner-decision outcome from prose.
- No source, contract, test, workflow, CLI/API entry, runtime behavior, grant authority surface or physical module retirement changed in this lane.

## Verification

Commands run from `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-broader-docs-portfolio-ssot-20260607` before adding this closeout:

```bash
git status --short --branch
find docs -path 'docs/history' -prune -o -name '*.md' -print | sort | wc -l
find docs/history -name '*.md' -print | sort | wc -l
find docs -name '*.md' -print | sort | wc -l
find . -maxdepth 2 -name 'README*' -print | sort
rg -n "Gateway|gateway|federation|frontdesk|frontdoor|local-manager|Runtime Manager|runtime manager|Hermes-first|hosted handoff|compatibility|compat alias|alias|facade|wrapper|fallback|patch bridge|aggregate test|run-local|runtime-run|runtime-resume|probe-upstream-hermes|physical delete|delete authorized|production ready|domain ready|grant-ready|submission-ready|fundability-ready|quality-ready|export-ready|App sustained|default caller|direct/hosted parity|long soak|long-soak|human gate|readiness" README.md README.zh-CN.md agent/README.md contracts/README.md runtime/README.md docs/README.md docs/docs_portfolio_consolidation.md docs/project.md docs/status.md docs/architecture.md docs/invariants.md docs/decisions.md docs/active docs/public docs/product docs/runtime docs/delivery docs/source docs/policies docs/specs docs/references
rg -n "claims_domain_repo_physical_delete_authorized|claims_all_bridge_exits_complete|claims_production_long_run_soak_complete|physical_delete_authorized|default_caller_delete_ready|owner_decision_required|legacy_active_path_residue|mag_functional_structure_gap_count|standard_agent_source_shape_status|submission_ready_export_gate" contracts src tests docs/active docs/status.md docs/architecture.md docs/invariants.md docs/decisions.md docs/docs_portfolio_consolidation.md docs/README.md
```

Result before adding this closeout:

- Worktree started clean on `codex/mag-broader-docs-portfolio-ssot`.
- Inventory was `docs/**/*.md=134`, non-history `docs/**/*.md=34`, `docs/history/**/*.md=100`.
- Targeted scans returned current owner split, explicit negative guards, tombstone/provenance wording, active-gate owner routing, support-spec lifecycle guards and machine contract/test no-ready / no-physical-delete assertions.
- Current docs and machine cross-check surfaces still report physical delete and production long-soak as not authorized / not complete.
- No active-current docs scan showed grant-ready, fundability-ready, quality-ready, export-ready, submission-ready, production-ready, active old runtime owner, compatibility alias/facade authorization or MAG owner delete/keep decision from docs prose.

Result after adding this closeout:

- Inventory is `docs/**/*.md=135`, non-history `docs/**/*.md=34`, `docs/history/**/*.md=101`, confirming this lane added only history provenance and did not expand current docs.
- `git diff --check` passed for this closeout and the coverage ledger index update.
- Conflict-marker scan passed.
- MAG OPL Doc doctor reported `finding_count=0`.

## Remaining Scope

This lane closes only broader MAG docs portfolio SSOT routing for this OPL series tranche. It does not claim grant readiness, fundability readiness, quality readiness, export readiness, submission readiness, domain readiness, production readiness, physical delete authorization, keep-as-authority-adapter authorization, App/workbench sustained consumption, direct/hosted parity completion or Temporal long-soak completion.

Open carry-forward:

- Actual MAG owner delete authorization / keep-as-authority-adapter receipt / typed blocker outcome remains separate from docs portfolio currentness.
- Direct/hosted parity follow-through, production/App sustained consumption, Temporal long-soak and production evidence tails remain separate lanes.
- Physical cleanup of active handler/adapter shell remains gated by generated/default caller consumption, no-active-caller proof, owner receipt / typed blocker roundtrip, continuous no-forbidden-write and explicit MAG owner physical-delete/tombstone receipt.
