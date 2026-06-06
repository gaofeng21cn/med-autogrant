# MAG active plan / private inventory long-list no-rewrite closeout

Owner: `Med Auto Grant`
Purpose: `docs_portfolio_coverage_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、`contracts/private_functional_surface_policy.json`、`contracts/foundry_agent_series.json`、product-entry manifest、source、tests、runtime receipts 和语义化 `human_doc:*` id。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T08:45:00Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Semantic theme: `active plan and private inventory long-list compression`
- Governance mode: SSOT-first content-level audit. This lane intentionally does not rewrite the active owner docs after verifying that their tables are current semantic owner views, not historical increment logs.

## Single Source Of Truth

### Machine truth

- `contracts/runtime-program/current-program.json`
  - `mag_functional_structure_gap_count = 0`
  - `standard_agent_source_shape_status = landed`
  - `claims_domain_repo_physical_delete_authorized = false`
  - `claims_all_bridge_exits_complete = false`
  - `claims_production_long_run_soak_complete = false`
- `contracts/private_functional_surface_policy.json#/physical_source_morphology_policy`
  - `surface_classification_count = 14`
  - `claims_physical_cleanup_complete = false`
  - `retirement_gate.state = active_caller_migration_evidence_required`
  - `compatibility_alias_allowed = false`
  - `facade_reexport_allowed = false`
- `contracts/foundry_agent_series.json#/purpose_first_adapter_thinning_policy`
  - holds the purpose-first adapter thinning policy and physical-delete required gates.

### Current docs owner

- `docs/active/mag-ideal-state-cross-repo-gap-plan.md`
  - owns current active gap/progress framing, evidence gates, next prompt and no-ready-overclaim posture.
  - intentionally does not list every path-level surface.
- `docs/active/opl-private-implementation-migration-inventory.md`
  - owns per-surface private-platform residue, active caller, current classification, retained MAG authority, OPL migration candidate area, retirement gate and verification entry.
  - its tables are current inventory views, not dated process logs.
- `docs/history/docs-portfolio-coverage-ledger/**`
  - owns dated closeout, frozen inventory snapshots and proof/read-model foldback provenance.

## Peer Docs Classification

| Document / section | Classification | Action |
| --- | --- | --- |
| `docs/active/mag-ideal-state-cross-repo-gap-plan.md` / current progress, functional gaps, evidence gaps, next prompt | `current_active_gap_owner` | No rewrite. The doc is 192 lines, separates current completion, functional/structural gaps, evidence gaps and next prompt, and explicitly routes proof transcripts / dated closeout / receipt ids to history or contracts. |
| `docs/active/opl-private-implementation-migration-inventory.md` / current inventory and path-level checkpoints | `current_private_inventory_owner` | No rewrite. The doc is 95 lines and maps current active caller / class / authority / migration gate by surface. This is not a historical increment list; it is the current per-surface governance owner. |
| `contracts/private_functional_surface_policy.json` / physical source morphology policy | `machine_truth_owner` | No edit. It lists 14 current surface classifications and the physical retirement gate. |
| `contracts/runtime-program/current-program.json` / privatized functional module audit | `machine_truth_owner` | No edit. It keeps aggregate classification counts and confirms physical delete is not authorized. |
| `docs/active/README.md` | `reader_routing` | No edit. It correctly points active readers to active plan and private inventory, while routing dated evidence to history. |
| `docs/docs_portfolio_consolidation.md` | `docs_lifecycle_support` | No edit. It already states active/gap owner, direct retirement posture and long-list governance rules. |

No section in this lane was classified as `conflicts_with_ssot` or `stale_or_superseded`. The risk hypothesis was "historical increment long list"; live-read showed that both tables are current semantic owner views with bounded size and explicit machine-boundary routing.

## No-Rewrite Decision

Do not compress `docs/active/mag-ideal-state-cross-repo-gap-plan.md` or `docs/active/opl-private-implementation-migration-inventory.md` in this tranche.

Reason:

- The active plan owns `current state -> functional/structural gaps -> evidence gaps -> next prompt`.
- The private inventory owns `surface family/path -> active caller -> classification -> retained MAG authority -> OPL migration candidate -> retirement gate -> verification`.
- Merging the private inventory into the active plan would recreate a long path-level list in the active plan.
- Deleting the path-level inventory would remove the current source-facing governance view needed to decide no-active-caller, retained authority and direct-retirement gates.
- The machine contracts already provide aggregate truth and enforce no-resurrection / physical-delete gate semantics; the docs only explain how to read those surfaces.

## Verification

Commands run from `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-active-inventory-longlist-ssot-20260606`:

```bash
rtk wc -l docs/active/mag-ideal-state-cross-repo-gap-plan.md docs/active/opl-private-implementation-migration-inventory.md docs/active/README.md docs/docs_portfolio_consolidation.md
rtk python - <<'PY'
import json
from pathlib import Path
p=json.loads(Path('contracts/private_functional_surface_policy.json').read_text())
print(len(p['physical_source_morphology_policy']['surface_classifications']))
PY
rtk python - <<'PY'
import json
from pathlib import Path
cp=json.loads(Path('contracts/runtime-program/current-program.json').read_text())
a=cp['runtime_owner']['stage_led_framework_boundary']['consumer_thinning_contract']['privatized_functional_module_audit']
print(a['claims_domain_repo_physical_delete_authorized'])
PY
```

Result:

- Active docs line counts: `192` active plan, `95` private inventory, `25` active README, `116` docs portfolio governance.
- `private_functional_surface_policy.json` exposes `14` current physical-source surface classifications.
- `current-program.json` keeps `claims_domain_repo_physical_delete_authorized = false`.

Additional final verification for this docs-only closeout:

- `git diff --check`: pending final commit verification.
- conflict-marker scan over edited closeout/index docs: pending final commit verification.
- `opl-doc-doctor`: pending final commit verification.

## Remaining Scope

This lane closes only the active-plan/private-inventory long-list compression question.

Carry forward:

- Actual product-entry/domain-handler generated default caller evidence, direct/hosted parity, no-active-caller proof, physical-delete owner receipt and production long-soak remain open evidence gates.
- Broader MAG docs portfolio governance remains open by semantic theme.
- Future compression should happen only when a path-level surface gets deleted, migrated, tombstoned or loses current governance value.

## Next Write Scope

Recommended next MAG lane:

- Semantic theme: `default caller / generated caller evidence gate and no-active-caller proof`
- Candidate SSOT owner: `contracts/private_functional_surface_policy.json`, `contracts/runtime-program/current-program.json`, product-entry manifest, OPL/App read-model evidence, active plan and private inventory.
