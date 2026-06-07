# MAG product-entry test support star facade retirement closeout

Owner: `Med Auto Grant`
Purpose: `product_entry_test_support_star_facade_retirement_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、source tree、tests、CLI/API behavior、runtime receipts 和 repo-native verification。

## Snapshot

- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Worktree: `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-product-entry-support-star-retirement`
- Branch: `codex/mag-product-entry-support-star-retirement`
- Semantic theme: MAG product-entry test-side star import facade retirement.

## Source Of Truth

- `AGENTS.md` and `TASTE.md`: replaced aliases, facades, wrappers, aggregate tests and compatibility re-export surfaces retire directly after active callers move to current owner surfaces.
- `tests/product_entry_cases/support.py`: test support helper module for product-entry cases, not a public test API facade.
- `tests/product_entry_cases/test_dependency_structure.py`: structural no-resurrection guard for product-entry source/test dependency boundaries.

## Change

- Replaced `from product_entry_cases.support import *` in product-entry case tests with explicit imports for each test file's actual helper usage.
- Removed the dynamic `support.py#__all__` export list so support no longer presents every imported helper/module as a package-style facade.
- Added a structure guard that rejects future product-entry case star imports from `product_entry_cases.support` and rejects `support.py` reintroducing `__all__`.

No product-entry payload shape, grant authority function, domain handler behavior, CLI/API command, runtime owner, current-program contract or owner receipt semantics changed.

## Verification

Commands run from the worktree:

```bash
rtk scripts/run-pytest-clean.sh tests/product_entry_cases/test_dependency_structure.py -q
rtk scripts/run-pytest-clean.sh tests/product_entry_cases -q
rtk rg -n "from product_entry_cases\\.support import \\*|__all__ = \\[name for name in globals\\(\\)" tests/product_entry_cases
```

Result:

- Focused dependency-structure pytest passed: `7 passed`.
- Focused product-entry case pytest passed: `172 passed, 208 subtests passed`.
- Retired star import / dynamic `__all__` scan returned no matches.

## Residual Risk

This closeout only retires the test-side star import facade. `tests/product_entry_cases/support.py` remains an active helper module for shared fixtures, constants and assertions used by the focused product-entry test suite.
