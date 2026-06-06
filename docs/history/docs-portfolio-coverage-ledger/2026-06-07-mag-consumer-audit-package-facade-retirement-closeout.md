# MAG consumer audit package facade retirement closeout

Owner: `Med Auto Grant`
Purpose: `consumer_audit_package_facade_retirement_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、source tree、tests、CLI/API behavior、runtime receipts 和 repo-native verification。

## Snapshot

- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Worktree: `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-consumer-audit-init-facade-retirement`
- Branch: `codex/mag-consumer-audit-init-facade-retirement`
- Semantic theme: MAG consumer thinning audit package-level builder re-export facade retirement.

## Source Of Truth

- `AGENTS.md` and `TASTE.md`: replaced aliases, facades, wrappers and compatibility re-export surfaces retire directly after active callers move to the current owner module.
- `src/med_autogrant/product_entry_parts/consumer_thinning.py`: active caller imports `build_privatized_functional_module_audit` from the concrete owner module `consumer_thinning_audit.report`.
- `consumer_thinning_audit.evidence_gates`, `consumer_thinning_audit.model`, `consumer_thinning_audit.retired_surfaces`, `consumer_thinning_audit.classification` and `consumer_thinning_audit.report`: concrete owner modules keep the actual builder functions.

## Change

- `consumer_thinning_audit/__init__.py` was reduced to a package marker and no longer imports or exports any builder.
- `tests/product_entry_cases/test_dependency_structure.py` now rejects package-level consumer audit builder exports, `__all__`, and package-root owner-module imports.
- No product-entry manifest payload shape, domain handler behavior, CLI/API command, grant authority function, runtime owner or current-program contract semantics changed.

## Verification

Commands run from the worktree:

```bash
rtk ./scripts/run-pytest-clean.sh tests/product_entry_cases/test_dependency_structure.py -q
rtk ./scripts/run-pytest-clean.sh tests/product_entry_cases/test_dependency_structure.py tests/product_entry_cases/test_functional_closure.py tests/product_entry_cases/test_domain_handler.py -q
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" src/med_autogrant/product_entry_parts/consumer_thinning_audit/__init__.py tests/product_entry_cases/test_dependency_structure.py docs/history/docs-portfolio-coverage-ledger/README.md docs/history/docs-portfolio-coverage-ledger/2026-06-07-mag-consumer-audit-package-facade-retirement-closeout.md
rtk rg -n "from med_autogrant\\.product_entry_parts\\.consumer_thinning_audit import|__all__|build_default_caller_deletion_bridge_exit_gate|build_functional_module_audit_item|build_legacy_exit_gate|build_privatized_functional_module_audit|build_retired_functional_module_audit_item" src/med_autogrant/product_entry_parts/consumer_thinning_audit/__init__.py
rtk ./scripts/verify.sh
rtk /Users/gaofeng/.local/bin/opl-doc-doctor doctor . --format json
```

Result:

- Focused structure pytest passed before implementation: `6 passed`.
- Final focused product-entry structure / functional closure / domain-handler run passed: `21 passed, 91 subtests passed`.
- `git diff --check`: passed.
- Conflict-marker scan over touched files: no matches.
- Package-root consumer audit builder / `__all__` scan: no matches.
- Default `scripts/verify.sh`: passed with CLI smoke `4 passed` and fast tests `239 passed, 154 subtests passed`.
- OPL Doc doctor: passed with `finding_count=0` and `active_truth_health.status=pass`.

## Residual Risk

This closeout only retires the package-root re-export facade for consumer thinning audit builders. The concrete builder modules remain active because they own current audit payload construction.
