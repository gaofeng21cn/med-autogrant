# MAG product-entry/package authority SSOT closeout

Owner: `Med Auto Grant`
Purpose: `product_entry_package_authority_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、`contracts/stage_control_plane.json`、`src/med_autogrant/product_entry_contract_api.py`、stage control source、product-entry source/tests、CLI/API behavior、runtime receipts 和语义化 `human_doc:*` id。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T07:28:54Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Semantic theme: `product-entry public bridge and package/canonical pointer authority`
- Governance mode: SSOT-first code/contract/test consolidation, not prose polishing.

## Single Source Of Truth

Machine SSOT:

- `src/med_autogrant/product_entry_contract_api.py`
  - owns the product-entry contract API bridge consumed by product-entry runtime contract helpers.
  - public export surface must expose stable public bridge functions and schema constants, not private `_build_*`, `_read_*`, or `_validate_*` aliases.
- `src/med_autogrant/stage_control_plane_parts/artifact_contracts.py`
  - owns stage-native artifact authority boundary source.
  - OPL may index refs and rebuild projections; MAG owns current/canonical pointer authority, package authority, grant truth, quality/export/submission verdicts, owner receipts, typed blockers, and artifact bodies.
- `contracts/stage_control_plane.json`
  - generated contract mirror from `med_autogrant.opl_standard_pack.sync_standard_pack()`.
  - must say `opl_can_index_canonical_pointer_ref=true` and `opl_can_promote_canonical_pointer=false`.
- `tests/product_entry_cases/test_dependency_structure.py`
  - guards product-entry contract API export shape.
- `tests/product_entry_cases/test_family_stage_control_plane.py`
  - guards OPL refs/index role versus MAG pointer promotion authority.

Human-doc owners:

- `docs/status.md`, `docs/invariants.md`, `docs/decisions.md`, and `docs/active/mag-ideal-state-cross-repo-gap-plan.md`
  - already state that MAG retains package authority, owner receipts, quality/export/submission verdicts, and grant truth.
  - no prose edit was required in this lane.

## Peer Surface Classification

| Surface | Classification | Action |
| --- | --- | --- |
| `src/med_autogrant/product_entry_contract_api.py#__all__` | `conflicts_with_ssot` | Replaced dynamic private-name export with an explicit public bridge export list. |
| `tests/product_entry_cases/test_dependency_structure.py` | `covered_by_ssot` guard gap | Added a focused assertion that `__all__` exports only public bridge names and schema constants. |
| `src/med_autogrant/stage_control_plane_parts/artifact_contracts.py#authority_boundary` | `conflicts_with_ssot` | Replaced `opl_can_promote_canonical_pointer=true` with `opl_can_promote_canonical_pointer=false` and added `opl_can_index_canonical_pointer_ref=true`. |
| `contracts/stage_control_plane.json` | `generated_contract` | Regenerated through `./scripts/run-python-clean.sh -m med_autogrant.opl_standard_pack`; only the pointer authority fields changed. |
| `tests/product_entry_cases/test_family_stage_control_plane.py` | `covered_by_ssot` guard gap | Added assertions for canonical pointer ref indexing and no OPL canonical pointer promotion. |
| `docs/status.md`, `docs/invariants.md`, `docs/decisions.md`, `docs/active/mag-ideal-state-cross-repo-gap-plan.md` | `covered_by_ssot` human support | Already state MAG-owned package authority and no OPL readiness/verdict authority. No edit. |

## Content-Level Consolidation

- Product-entry contract API is a public thin bridge, not a private compatibility facade.
- OPL can index canonical pointer refs and rebuild projections for App/workbench consumption.
- OPL cannot promote MAG canonical pointers, advance current pointers, sign MAG owner receipts, interpret grant quality, write grant truth, mutate artifact bodies, or declare export/submission readiness.
- MAG keeps package/canonical pointer authority and emits owner receipt or typed blocker refs when a package/pointer change is valid or blocked.

## Verification

Commands run from `/Users/gaofeng/workspace/med-autogrant`:

```bash
rtk ./scripts/run-python-clean.sh -m med_autogrant.opl_standard_pack
rtk ./scripts/run-pytest-clean.sh -q tests/product_entry_cases/test_dependency_structure.py tests/product_entry_cases/test_family_stage_control_plane.py tests/product_entry_cases/test_package_lifecycle_handoff.py tests/test_submission_ready_package.py tests/test_opl_standard_pack.py
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" docs contracts src tests
rtk rg -n '"opl_can_promote_canonical_pointer": true|__all__ = \[name for name in globals\(\) if name.startswith\("_"\) or name.endswith\("_SCHEMA_FILE"\)\]' src/med_autogrant/product_entry_contract_api.py contracts/stage_control_plane.json src/med_autogrant/stage_control_plane_parts/artifact_contracts.py tests/product_entry_cases
rtk ./scripts/verify.sh
```

Result:

- Pack sync passed and rewrote `contracts/stage_control_plane.json` from source.
- Focused pytest passed: `24 passed, 11 subtests passed`.
- `git diff --check` passed.
- Conflict-marker scan found no matches.
- Targeted stale scan found no matches.
- `scripts/verify.sh` passed: line-budget check, CLI smoke `4 passed`, fast tests `239 passed`, `462 deselected`, `154 subtests passed`.

## Remaining Scope

This lane closes only product-entry public bridge export shape and package/canonical pointer authority drift.

Carry forward:

- Product-entry/domain-handler generated default caller evidence, direct/hosted parity, no-active-caller proof, and physical-delete owner receipt remain separate evidence gates.
- Source/workspace lifecycle, delivery lifecycle, runtime topology, and broader MAG docs portfolio remain separate lanes.
