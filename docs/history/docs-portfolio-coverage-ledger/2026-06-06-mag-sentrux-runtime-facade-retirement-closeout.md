# MAG Sentrux runtime facade retirement closeout

Owner: `Med Auto Grant`
Purpose: `sentrux_runtime_facade_retirement_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `.sentrux/rules.toml`、source tree、tests、CLI/API behavior、contracts/runtime-program/current-program.json 和 repo-native verification。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T10:52:33Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Worktree: `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-sentrux-runtime-facade-retirement`
- Branch: `codex/mag-sentrux-runtime-facade-retirement`
- Semantic theme: Sentrux architecture sidecar no longer treats the retired MAG-owned runtime facade as an active layer.

## Source Of Truth

- `AGENTS.md` and `TASTE.md`: direct retirement posture; removed facades should not be kept as compatibility layers.
- `.sentrux/rules.toml`: Sentrux layer graph and forbidden dependency boundaries.
- `tests/test_sentrux_governance.py`: meta governance assertions for the Sentrux sidecar.
- Current source tree: `src/med_autogrant/hermes_runtime.py` is absent.
- Runtime owner truth: MAG does not own a generic daemon, scheduler, attempt loop or default task runtime; OPL/Temporal owns default durable runtime.

## Change

- Removed the `runtime_facade` layer from `.sentrux/rules.toml`.
- Removed the `export_package -> runtime_facade` boundary because its target layer pointed at the absent `src/med_autogrant/hermes_runtime.py`.
- Renumbered the remaining `domain_logic` and `export_package` layer orders to keep the active graph compact.
- Updated `tests/test_sentrux_governance.py` to assert that `runtime_facade` and `src/med_autogrant/hermes_runtime.py` are not present in the active rules and that only current layers remain.

## Verification

Commands run from the worktree:

```bash
rtk ./scripts/run-pytest-clean.sh tests/test_sentrux_governance.py tests/test_domain_runtime_split.py tests/product_entry_cases/test_dependency_structure.py -q
rtk ./scripts/run-structural-quality-gate.sh --advisory
rtk sentrux check .
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" .sentrux tests docs/history/docs-portfolio-coverage-ledger
```

Result:

- Focused pytest passed: `19 passed`.
- Structural quality gate exited `0` in advisory mode. After rebasing onto current `main`, the worktree run still emitted advisory Sentrux output for three oversized generated/contract files, the existing `export_package -> product_entry` layer violation in `hosted_contract_bundle.py`, `max_depth 20 > 14`, and an advisory baseline-regression readout relative to `origin/main`. In that same worktree run, OPL quality-details Markdown generation reported an external OPL CLI import error from `/Users/gaofeng/workspace/one-person-lab`; the Sentrux result remained the authority for this MAG lane. A main-checkout advisory rerun generated OPL quality details successfully and kept the same existing Sentrux findings.
- Direct `sentrux check .` comparison confirmed the same two rule violations in the main checkout and this worktree; this lane reduced the checked rule count from `8` to `7` by removing the obsolete `runtime_facade` boundary, without introducing a new violation.
- `git diff --check` passed, and the conflict-marker scan found no matches in the edited Sentrux, test and history ledger paths.

## Residual Risk

This closeout only retires the obsolete Sentrux sidecar layer and its governance assertion. It does not change production runtime ownership, MAG domain handler behavior, package/export authority, CLI/API behavior, or any physical source surface beyond confirming that `src/med_autogrant/hermes_runtime.py` remains absent.
