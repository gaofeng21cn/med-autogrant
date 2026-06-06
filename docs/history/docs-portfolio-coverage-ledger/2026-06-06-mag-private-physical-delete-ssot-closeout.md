# MAG private physical-delete SSOT closeout

Owner: `Med Auto Grant`
Purpose: `private_physical_delete_ssot_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、`contracts/private_functional_surface_policy.json`、`contracts/foundry_agent_series.json`、product-entry manifest / functional privatization audit、source/tests、runtime receipts 和 MAG owner receipts / typed blockers。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T09:34:00Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Semantic theme: `private implementation residue / physical-delete gate / direct-retirement posture`
- Governance mode: SSOT-first semantic consolidation; content-level peer doc thinning, not file-level cleanup.

## Single Source Of Truth

Machine SSOT:

- `contracts/runtime-program/current-program.json#/runtime_owner`
  - owns default runtime facts: `default_task_runtime_owner=one-person-lab`, `default_runtime_substrate=temporal`, `default_stage_executor=codex_cli`, and MAG does not implement daemon, scheduler, attempt loop, or attempt ledger.
- `contracts/private_functional_surface_policy.json#/purpose_first_owner_delta_domain_thinning_gate`
  - owns physical-delete prerequisites for product-entry, grouped CLI, status/user-loop, domain-handler, runtime/control projection and lifecycle shell.
  - required gates are generated/default caller consumption, sustained App/default-caller consumption, direct/hosted parity, owner receipt or typed blocker roundtrip, no-active domain repo generic shell caller, continuous no-forbidden-write and MAG physical-delete/tombstone owner receipt.
- `contracts/foundry_agent_series.json#/purpose_first_adapter_thinning_policy`
  - owns retained surface roles and the evidence-tail boundary: structural conformance, grouped CLI success, provider completion or generated surface existence cannot become domain readiness, grant readiness or submission readiness.
- product-entry manifest / functional privatization audit surfaces
  - own the current replacement / no-resurrection projections, including `claims_domain_repo_physical_delete_authorized=false`, thin return shapes, external evidence request refs and legacy tombstone refs.

Human-doc owners:

- `docs/active/mag-ideal-state-cross-repo-gap-plan.md`
  - owns current active gate, production evidence tail, next prompt and forbidden-readiness wording.
- `docs/active/opl-private-implementation-migration-inventory.md`
  - owns per-surface classification, active caller, retained MAG authority, OPL migration candidate domain and retirement gate.

## Peer Surface Classification

| Surface | Classification | Action |
| --- | --- | --- |
| `docs/active/mag-ideal-state-cross-repo-gap-plan.md` | `ssot_active_plan` | Kept as the active gate owner; no prose duplicated into peer docs. |
| `docs/active/opl-private-implementation-migration-inventory.md` | `ssot_inventory_detail` | Kept as the per-surface owner; no path-level rewrite in this lane. |
| `docs/status.md` | `covered_by_ssot` + `entry_pointer_needed` | Thinned retained-surface and physical-cleanup sections into current summary plus pointers to active plan, private inventory and machine gates. |
| `docs/architecture.md` | `covered_by_ssot` + `architecture_summary_needed` | Removed repeated external evidence and physical-delete gate detail; kept owner split and contract role only. |
| `docs/docs_portfolio_consolidation.md` | `covered_by_ssot` + `governance_rule_needed` | Replaced dated retired-command audit detail with no-resurrection rule and owner pointers. |
| `docs/product/README.md`, `docs/runtime/README.md` | `already_thin_support_index` | No edit; they already route readers to product/runtime support owners without duplicating the physical-delete gate. |
| `docs/specs/README.md`, `docs/specs/specs_lifecycle_map.md` | `history_or_provenance_guard` | No edit; they already state old provider/runtime/compat specs remain history or support-only. |
| `docs/history/docs-portfolio-coverage-ledger/2026-06-04-mag-retired-command-family-audit.md` | `history_or_provenance` | Kept as dated audit; current docs now point to it only as provenance. |

## Content-Level Consolidation

- `docs/status.md` now states only current owner/gate status and points detailed physical-delete logic to the active plan, private inventory and contracts.
- `docs/architecture.md` now keeps the architecture-level split: MAG emits refs/receipts/typed blockers and OPL owns generic primitives. It no longer repeats the full evidence request / physical-delete gate list.
- `docs/docs_portfolio_consolidation.md` now records the document-governance rule and SSOT owner chain instead of preserving dated command-audit detail as current text.
- No compatibility wording was added. The retained rule remains direct retirement: stale modules, interfaces, CLI aliases, wrappers, facades, patch bridges, aggregate tests and old workflow entries are deleted or history-tombstoned when replacement and no-active-caller evidence exists.

## Verification

Commands to run from `/Users/gaofeng/workspace/med-autogrant` or this worktree:

```bash
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" docs/status.md docs/architecture.md docs/docs_portfolio_consolidation.md docs/history/docs-portfolio-coverage-ledger/README.md docs/history/docs-portfolio-coverage-ledger/2026-06-06-mag-private-physical-delete-ssot-closeout.md
rtk rg -n "physical delete|physical-delete|direct/hosted parity|owner receipt roundtrip|compat aggregate|compatibility shell|re-export facade|MAG-owned generic runtime" docs/status.md docs/architecture.md docs/docs_portfolio_consolidation.md docs/active/mag-ideal-state-cross-repo-gap-plan.md docs/active/opl-private-implementation-migration-inventory.md
rtk /Users/gaofeng/.local/bin/opl-doc-doctor doctor . --format json
```

Result:

- `git diff --check` passes.
- conflict-marker scan finds no matches.
- targeted scan shows detailed physical-delete gate lists concentrated in active plan and private inventory; peer docs keep only summary/pointer wording.
- OPL Doc doctor reports `finding_count=0`.

## Remaining Scope

This lane closes only the private physical-delete / direct-retirement documentation SSOT consolidation in MAG peer docs.

Carry forward:

- actual physical deletion of product-entry/domain-handler/domain_runtime/autonomy/CLI active shell still requires generated/default caller consumption, sustained App/default-caller consumption, direct/hosted parity, owner receipt or typed blocker roundtrip, no-active domain repo generic shell caller, continuous no-forbidden-write and MAG physical-delete/tombstone owner receipt.
- production App/operator sustained consumption and Temporal long-soak remain evidence gates.
- broader MAG docs portfolio coverage continues by separate semantic themes.
