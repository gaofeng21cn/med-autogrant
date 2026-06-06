# MAG runtime topology project-overview SSOT closeout

Owner: `Med Auto Grant`
Purpose: `docs_portfolio_coverage_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、contracts、schemas、source、CLI/API behavior、product-entry manifest、runtime receipts 和语义化 `human_doc:*` id。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T08:15:00Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Semantic theme: `runtime topology and project overview boundary`
- Governance mode: SSOT-first content-level consolidation, not file-level polishing.

## Single Source Of Truth

### Current machine truth

- `contracts/runtime-program/current-program.json`
  - `default_task_runtime_owner = one-person-lab`
  - `default_runtime_substrate = temporal`
  - `mag_implements_daemon = false`
  - `mag_implements_scheduler = false`
  - `mag_implements_attempt_loop = false`
  - `mag_owns_attempt_ledger = false`
  - `default_stage_executor = codex_cli`
- `product-entry-manifest` runtime and consumer-thinning surfaces
  - expose descriptor/projection/refs-only handoff to OPL.
  - do not move grant truth, fundability verdict, authoring quality verdict, export verdict, package body, memory body, or owner receipt authority out of MAG.
- `contracts/private_functional_surface_policy.json` and `contracts/foundry_agent_series.json`
  - hold purpose-first owner-delta and direct-retirement gates for handwritten product/status/user-loop/domain-handler/runtime-control shell surfaces.

### Current docs owner

- `docs/status.md` owns current runtime owner/status/evidence-gate summary.
- `docs/architecture.md` owns architecture and owner split detail.
- `docs/invariants.md` owns stable no-resurrection and runtime-authority constraints.
- `docs/active/mag-ideal-state-cross-repo-gap-plan.md` owns current active gap, evidence tail, and physical-delete authorization gate.
- `docs/active/opl-private-implementation-migration-inventory.md` owns per-surface private-platform residue, active caller, classification, migration gate, and verification entry.
- `docs/runtime/README.md` is a thin runtime support index only.
- `docs/project.md` owns project role and boundary only; it must not duplicate runtime topology, manifest handoff, active gap, or private inventory detail.

Machine contracts and source-backed manifests win over prose. Among human docs, each owner above wins only inside its purpose boundary; no peer doc should preserve a parallel current narrative for the same runtime topology.

## Peer Docs Classification

| Document / section | Classification | Action |
| --- | --- | --- |
| `docs/project.md` / project positioning, goals, current shape | `covered_by_ssot` duplication plus project-overview role pollution | Rewrote into a compact project role/boundary page and pointers. Removed detailed runtime topology, domain-handler, memory apply, product projection, and long goal list duplication. |
| `docs/status.md` / current conclusion and machine facts | `current_truth_owner` | No edit; it remains the status/evidence-gate owner. |
| `docs/architecture.md` / main chain, OPL handoff, runtime/product shell | `more_specific_detail` | No edit; architecture remains the owner of detailed owner split and route topology. |
| `docs/invariants.md` / identity, OPL boundary, standard agent target | `current_stable_constraint_owner` | No edit; invariant wording already guards no-resurrection and runtime-owner boundaries. |
| `docs/active/mag-ideal-state-cross-repo-gap-plan.md` | `current_active_gap_owner` | No edit; it already separates functional/structure gaps from evidence gates and forbids readiness overclaims. |
| `docs/active/opl-private-implementation-migration-inventory.md` | `more_specific_detail` | No edit; it remains the per-surface inventory and deletion-gate owner. |
| `docs/runtime/README.md` | `thin_support_index` | No edit; it already says runtime truth belongs to contracts/source/status/specs and forbids MAG-owned generic runtime wording. |
| `docs/README.md` | `reader_routing` | No edit; it already routes runtime topology to current owner docs and warns history/human_doc ids do not promote old files. |

No current non-history doc in this lane was classified as `conflicts_with_ssot`. The live issue was semantic duplication: `docs/project.md` was carrying enough runtime topology and handoff detail to act as a parallel current truth source.

## Modifications

- Rewrote `docs/project.md` from a detailed runtime/project ledger into a compact project overview.
- Kept the current MAG role, direct skill / CLI / `MedAutoGrantDomainEntry` boundary, OPL/Temporal runtime owner line, retained MAG authority list, and direct-retirement posture.
- Moved runtime topology detail by pointer to status, architecture, invariants, active gap plan, private inventory, and current-program pointer.
- Did not add compatibility wording, legacy alias, facade, wrapper, fallback, or compatibility-test preservation language.

## Verification

Commands run from `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-runtime-topology-ssot-20260606`:

```bash
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" docs/project.md docs/history/docs-portfolio-coverage-ledger/2026-06-06-mag-runtime-topology-project-overview-ssot-closeout.md docs/history/docs-portfolio-coverage-ledger/README.md
rtk rg -n "default.*Hermes|Hermes.*default|Gateway/local-manager.*default|MAG-owned scheduler|MAG-owned.*attempt ledger|compatibility shim|re-export facade|compatibility-only" README* docs --glob '*.md' --glob '!docs/history/**'
rtk /Users/gaofeng/.local/bin/opl-doc-doctor doctor . --format json
```

Result:

- `git diff --check`: pass.
- Conflict-marker scan over edited docs: pass.
- Targeted stale scan over current docs excluding `docs/history/**`: remaining matches are current negative guards, support lifecycle guards, or current owner statements; no selected match re-promotes Hermes/Gateway/local-manager/local-journal/attempt-ledger wording as the default MAG runtime owner.
- `opl-doc-doctor`: pass after removing active-path `Hermes-first` wording from `docs/project.md`; `finding_count = 0`, active truth owner `docs/active/mag-ideal-state-cross-repo-gap-plan.md`, `markdown_doc_count = 127`.

## Remaining Scope

This tranche covers only the runtime topology / project overview boundary. It does not complete full MAG docs portfolio governance.

Carry forward:

- Continue semantic lanes over `README*` and `docs/**/*.md`.
- Keep runtime topology truth in contracts/source/status/architecture/active plan/private inventory.
- Keep history specs and dated closeouts under `docs/history/**` unless a current owner explicitly extracts a still-current rule.

## Next Write Scope

Recommended next MAG lane:

- Semantic theme: `active plan and private inventory long-list compression`
- Candidate SSOT owner: `docs/active/mag-ideal-state-cross-repo-gap-plan.md` plus `docs/active/opl-private-implementation-migration-inventory.md`
- Peer docs: `docs/active/README.md`, `docs/docs_portfolio_consolidation.md`, `docs/specs/specs_lifecycle_map.md`, and current support indexes.
