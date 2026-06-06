# MAG stale export surfaces closeout

Owner: `Med Auto Grant`
Purpose: `stale_export_surface_retirement_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、source tree、tests、CLI/API behavior、runtime receipts 和 repo-native verification。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T13:07:27Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Worktree: `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-thin-stale-exports-20260606`
- Branch: `codex/mag-thin-stale-exports-20260606`
- Semantic theme: stale aggregate re-export retirement and thin MAG domain runtime public export surface.

## Source Of Truth

- `AGENTS.md` and `TASTE.md`: replaced owner surfaces should be retired directly; compatibility re-export facades should not remain as active surfaces.
- `contracts/runtime-program/current-program.json`: MAG stays a grant-domain authority surface; OPL/Temporal owns default durable runtime and MAG does not own generic daemon, scheduler, attempt loop or default task runtime.
- Live source/test caller scan: external imports of `med_autogrant.domain_runtime_parts.substrate` resolve to `MagDomainRuntime`; `src/med_autogrant/product_entry_parts/shared.py` has no active source or test caller.
- Existing runtime split tests and product-entry dependency tests own no-resurrection guards for stale facade / bridge surfaces.

## Change

- Deleted `src/med_autogrant/product_entry_parts/shared.py`, the unused aggregate product-entry re-export module.
- Replaced the dynamic `src/med_autogrant/domain_runtime_parts/substrate.py#__all__` export surface with an explicit `["MagDomainRuntime"]` list.
- Added structure guards that assert the deleted product-entry shared re-export file remains absent and substrate exports only the public MAG domain runtime adapter.

## Verification

Commands run from the worktree:

```bash
rtk ./scripts/run-pytest-clean.sh tests/product_entry_cases/test_dependency_structure.py tests/test_domain_runtime_split.py tests/test_domain_runtime.py tests/test_hosted_contract_bundle.py tests/test_structural_direct_coverage.py -q
rtk ./scripts/verify.sh
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" src tests docs/history/docs-portfolio-coverage-ledger
```

Result:

- Focused pytest passed: `41 passed, 15 subtests passed`.
- Final `scripts/verify.sh` passed: line-budget check, CLI smoke `4 passed`, fast tests `239 passed`, `472 deselected`, `154 subtests passed`.
- `git diff --check` passed.
- Conflict-marker scan found no matches.

## Residual Risk

This closeout only retires stale aggregate export surfaces. It does not change MAG domain runtime behavior, domain entry dispatch, package/export authority, product-entry manifest semantics, CLI/API command coverage or runtime ownership.
