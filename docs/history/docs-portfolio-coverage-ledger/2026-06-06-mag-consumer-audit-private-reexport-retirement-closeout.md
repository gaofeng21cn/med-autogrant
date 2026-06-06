# MAG consumer audit private re-export closeout

Owner: `Med Auto Grant`
Purpose: `consumer_audit_private_reexport_retirement_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、source tree、tests、CLI/API behavior、runtime receipts 和 repo-native verification。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T15:20:53Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Worktree: `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-consumer-audit-reexport-retirement-20260606`
- Branch: `codex/mag-consumer-audit-reexport-retirement-20260606`
- Semantic theme: MAG consumer thinning audit private re-export facade retirement.

## Source Of Truth

- `AGENTS.md` and `TASTE.md`: replaced aliases, facades and compatibility re-export surfaces should retire directly after active callers move to the current owner module.
- `docs/active/opl-private-implementation-migration-inventory.md`: MAG current source should keep thin direct adapters and no compatibility alias / re-export facade.
- Live caller scan: the only active `_build_privatized_functional_module_audit` caller was `src/med_autogrant/product_entry_parts/consumer_thinning.py`; the concrete owner function already lives in `consumer_thinning_audit.report`.

## Change

- Rewired `consumer_thinning.py` from the package-level `_build_privatized_functional_module_audit` alias to `consumer_thinning_audit.report.build_privatized_functional_module_audit`.
- Removed package-level `_build_*` assignments and `__all__` entries from `consumer_thinning_audit/__init__.py`.
- Added a focused structure guard that rejects restored package-level `_build_*` re-export facades and the retired consumer-thinning private import path.

## Verification

Commands run from the worktree:

```bash
rtk ./scripts/run-pytest-clean.sh tests/product_entry_cases/test_dependency_structure.py -q
rtk rg -n "from med_autogrant\\.product_entry_parts\\.consumer_thinning_audit import \\(|_build_(default_caller_deletion_bridge_exit_gate|functional_module_audit_item|legacy_exit_gate|privatized_functional_module_audit|retired_functional_module_audit_item)" src tests docs --glob '!docs/history/**'
```

Result:

- Focused structure pytest passed: `6 passed`.
- Retired private re-export scan found no active source/docs callers; remaining matches were the no-resurrection test assertion and internal `_default_*` local dependency-injection variables in `retired_surfaces.py`, not package-level compatibility exports.

## Residual Risk

This closeout only retires package-level private re-export aliases in the consumer thinning audit package. It does not change product-entry manifest semantics, functional audit payload shape, domain handler behavior, CLI/API commands, runtime ownership or grant-domain authority.
