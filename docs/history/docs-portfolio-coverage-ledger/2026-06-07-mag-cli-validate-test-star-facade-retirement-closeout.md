# MAG CLI validate test star facade retirement closeout

Owner: `Med Auto Grant`
Purpose: `cli_validate_test_star_facade_retirement_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、source tree、tests、CLI/API behavior、runtime receipts 和 repo-native verification。

## Snapshot

- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Worktree: `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-cli-validate-star-facade-retirement`
- Branch: `codex/mag-cli-validate-star-facade-retirement`
- Semantic theme: MAG CLI validate workspace test-side star import facade retirement.

## Source Of Truth

- `AGENTS.md` and `TASTE.md`: replaced aliases, facades, wrappers, aggregate tests and compatibility re-export surfaces retire directly after active callers move to current owner surfaces.
- `tests/cli_validate_cases.py`: shared base test helper module for CLI validate workspace tests, not a broad public test API import facade.
- `tests/test_repository_hygiene.py`: repo-tracked no-resurrection guard for test-side compatibility and facade claims.

## Change

- Replaced `from cli_validate_cases import *` in the three split CLI validate workspace test files with explicit imports for each file's actual helper usage.
- Moved standard-library dependencies (`json`, `os`, `subprocess`, `sys`, `tempfile`, `Path`) into the consuming test files that use them.
- Added a repository hygiene guard that rejects future star imports from `cli_validate_cases` in split `test_cli_validate_workspace_*` tests.

No CLI command mapping, workspace validation behavior, product-entry payload shape, domain handler behavior, current-program contract, runtime owner or grant authority semantics changed.

## Verification

Commands run from the worktree:

```bash
rtk scripts/run-pytest-clean.sh tests/test_cli_validate_workspace_error_cases.py tests/test_cli_validate_workspace_product_entry_cases.py tests/test_cli_validate_workspace_revision_cases.py -q
rtk scripts/run-pytest-clean.sh tests/test_repository_hygiene.py -q
rtk rg -n "from cli_validate_cases import \\*" tests
rtk scripts/verify.sh
rtk git diff --check
rtk /Users/gaofeng/.local/bin/opl-doc-doctor doctor . --format json
```

Result:

- Focused CLI validate split pytest passed: `45 passed, 2 subtests passed`.
- Repository hygiene pytest passed: `9 passed`.
- Retired star import scan returned no matches.
- Default verification passed: CLI smoke `4 passed`; fast test lane `239 passed, 154 subtests passed`; line budget remained advisory only.
- `git diff --check` passed.
- MAG doctor returned `finding_count=0`, `active_truth_health.status=pass`.

## Residual Risk

This closeout only retires the test-side broad star import facade. `tests/cli_validate_cases.py` remains an active helper module for shared CLI validate fixtures, base class methods and example path constants used by the split CLI validate test suite.
