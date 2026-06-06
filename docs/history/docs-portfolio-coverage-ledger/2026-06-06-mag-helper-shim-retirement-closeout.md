# MAG helper shim retirement closeout

Owner: `Med Auto Grant`
Purpose: `helper_shim_retirement_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、source tree、tests、CLI/API behavior、runtime receipts 和 repo-native verification。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T20:25:39Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Worktree: `/Users/gaofeng/workspace/med-autogrant/.worktrees/codex-mag-helper-shim-retirement`
- Branch: `codex/mag-helper-shim-retirement`
- Semantic theme: MAG test convenience helper, identity command normalizer and hosted-contract bundle wrapper retirement.

## Source Of Truth

- `AGENTS.md` and `TASTE.md`: replaced aliases, facades, wrappers and compatibility helper surfaces should retire directly after active callers move to the current owner module.
- `src/med_autogrant/public_cli.py`: public CLI truth is the grouped command catalog, generated-surface refs, command labels and rendered public command strings; argv list conversion is a test harness convenience, not a source public API.
- `src/med_autogrant/domain_entry.py#SERVICE_SAFE_DOMAIN_COMMANDS`: domain entry command truth is the service-safe command catalog plus fail-closed unknown-command behavior; retired command aliases are guarded by existing negative tests and functional closure scans.
- `src/med_autogrant/domain_runtime_parts/io.py`: hosted contract bundle output identity guard and JSON write helpers are the split IO owner helpers. `hosted_contract_bundle.py` should call those owner helpers directly instead of exposing one-line private delegation wrappers.

## Change

- Removed `public_cli_argv()` from `src/med_autogrant/public_cli.py`.
- Added the argv conversion helper to `tests/support/cli.py` and moved tests to import it from test support.
- Removed the identity `_normalize_command()` helper from `src/med_autogrant/domain_entry.py`; dispatch now uses `_require_command(request)` directly.
- Removed `_guard_output_identity()` and `_write_hosted_contract_bundle()` one-line private wrappers from `src/med_autogrant/hosted_contract_bundle.py`; hosted bundle payload construction now calls the split IO owner helpers directly.
- Updated hosted bundle unit patch targets to patch the current owner helpers.

## Verification

Commands run from the worktree:

```bash
rtk ./scripts/run-pytest-clean.sh tests/test_domain_entry.py tests/product_entry_cases/test_functional_closure.py -q
rtk ./scripts/run-pytest-clean.sh tests/test_domain_runtime.py tests/test_hosted_contract_bundle.py tests/test_hosted_contract_bundle_control_plane.py tests/test_hosted_contract_bundle_checkpoint_cases.py -q
rtk ./scripts/run-pytest-clean.sh tests/test_funding_discovery_cli.py tests/test_profile_selection_cli.py tests/test_grant_autonomy_cli.py tests/test_authoring_mainline_cli.py tests/test_revision_executor.py tests/test_grant_quality_cli.py tests/test_critique_loop_cli.py tests/product_entry_cases/test_cli_dispatch.py tests/product_entry_cases/test_closeout_cli_dispatch.py tests/product_entry_cases/test_production_live_acceptance_cli.py tests/product_entry_cases/test_opl_owner_payload_response_cli.py tests/product_entry_cases/test_receipt_readiness.py -q
rtk ./scripts/verify.sh
rtk git diff --check
rtk rg -n "public_cli_argv|_normalize_command|_guard_output_identity|_write_hosted_contract_bundle" src docs contracts
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" src tests docs/history/docs-portfolio-coverage-ledger
```

Result:

- Domain-entry / functional closure pytest passed: `31 passed, 73 subtests passed`.
- Hosted contract bundle pytest passed: `31 passed, 30 subtests passed`.
- CLI argv affected pytest passed: `49 passed, 22 subtests passed`.
- Final `scripts/verify.sh` passed: line-budget check, CLI smoke `4 passed`, fast tests `239 passed`, `473 deselected`, `154 subtests passed`.
- `git diff --check` passed.
- Target retired symbol scans found no `public_cli_argv` or `_normalize_command` in `src` / `contracts`, and no hosted-bundle private wrapper definitions or call sites in `hosted_contract_bundle.py` / `tests/test_domain_runtime.py`.
- Conflict-marker scan found no matches.

## Residual Risk

This closeout only retires helper/shim surfaces that had no MAG business semantics. It does not change grouped public CLI command mapping, domain entry command catalog, package/export authority, hosted contract bundle schema, final package validation, product-entry behavior, runtime ownership or grant-domain authority.
