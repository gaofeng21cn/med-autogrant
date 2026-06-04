# MAG retired command family audit

Owner: `Med Auto Grant`
Purpose: `docs_portfolio_coverage_and_retirement_audit`
State: `history_provenance`
Machine boundary: 本文是人读 coverage / retirement ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、contracts、schemas、source、CLI/API 行为、product-entry manifest、runtime receipts 和 workspace/artifact outputs。

## Snapshot

`RUN_SNAPSHOT_TS=2026-06-04T17:02:16Z`。本条目基于 fresh `origin/main` governance worktree `codex/automation-2-governance-20260604-mag`，不读取本地 diverged `main` 作为 MAG current truth。

本轮覆盖一个 coherent 文档治理簇：

- current owner docs: `docs/docs_portfolio_consolidation.md`、`docs/status.md`、`docs/architecture.md`、`docs/active/mag-ideal-state-cross-repo-gap-plan.md`、`docs/active/opl-private-implementation-migration-inventory.md`
- support/index docs: `docs/active/README.md`、`docs/runtime/README.md`、`docs/product/README.md`、`docs/history/docs-portfolio-coverage-ledger/README.md`
- machine/source/test truth: `src/med_autogrant/domain_entry.py`、`src/med_autogrant/cli.py`、`src/med_autogrant/public_cli.py`、`src/med_autogrant/product_entry_parts/functional_closure_skeleton.py`、`tests/test_domain_entry.py`、`tests/test_repository_hygiene.py`、`tests/product_entry_cases/test_domain_handler.py`、`pyproject.toml`、`Makefile`、`contracts/private_functional_surface_policy.json`、`contracts/functional_privatization_audit.json`、`contracts/production_acceptance/mag-executor-first-landing.json`

Fresh OPL Doc doctor on the governance worktree reported `finding_count=0` and `active_truth_health.status=pass`; this was used only as a shape risk map.

## Docs Lifecycle Result

`docs/docs_portfolio_consolidation.md` now carries the current inventory count and points dated coverage / retirement audit material back to this history ledger. The active governance document keeps current lifecycle rules, owner split and direct-retirement posture; it does not absorb frozen inventory, command transcripts, branch/worktree closeout, receipt ledgers or proof-by-proof audit text.

Reviewed but not rewritten:

- `docs/status.md` already states the current owner boundary: OPL/Temporal is the task runtime owner, MAG retains grant authority, and active product/domain-handler/runtime/CLI shells are handler or refs-only adapter targets until explicit physical-delete authority exists.
- `docs/active/mag-ideal-state-cross-repo-gap-plan.md` already holds the active gap, evidence gates and next-round prompt fields.
- `docs/active/opl-private-implementation-migration-inventory.md` already holds per-surface physical morphology details and no-resurrection rules.
- `docs/runtime/README.md` and `docs/product/README.md` already keep runtime/product support as thin indexes instead of second truth sources.

## Retirement Candidate Audit

Concrete candidate family: retired public/domain-entry runtime commands:

```text
run-local
runtime-run
runtime-resume
probe-upstream-hermes
```

Live source and test evidence:

- `src/med_autogrant/domain_entry.py` exposes `SERVICE_SAFE_DOMAIN_COMMANDS`; the four retired command tokens are absent, and `MedAutoGrantDomainEntry.dispatch` fails closed for unknown commands.
- `src/med_autogrant/public_cli.py` exposes the grouped public CLI catalog; the active groups are `workspace`, `mainline`, `domain-handler`, `authority`, `pass` and `package`, with no retired runtime command label.
- `pyproject.toml` exposes only the `medautogrant` console script, not legacy command aliases.
- `tests/test_domain_entry.py` has focused fail-closed tests for `run-local`, `runtime-run`, `runtime-resume` and `probe-upstream-hermes`.
- `src/med_autogrant/product_entry_parts/functional_closure_skeleton.py` keeps `_RETIRED_PUBLIC_COMMANDS` and `_build_retired_public_command_scan()` as the repo-local no-resurrection scan over `SERVICE_SAFE_DOMAIN_COMMANDS` and public CLI labels.
- `tests/test_repository_hygiene.py` blocks resurrection of compatibility-alias claims in machine surfaces.
- `tests/product_entry_cases/test_domain_handler.py` keeps generic product/workbench dispatch actions rejected by the domain-handler guarded action surface.

Current references to the retired command strings are acceptable only in:

- fail-closed tests;
- no-resurrection scan / negative guard contracts;
- active/support wording that says the commands are retired and cannot be restored as current runtime owner;
- `docs/history/**` provenance.

No physical source delete remained for this candidate: the command family is already absent from active domain-entry and public CLI catalogs. No compatibility alias, facade, wrapper, re-export or fallback was added.

## Retained Surfaces

The following surfaces remain public or active for current MAG authority reasons:

- `medautogrant` console script and grouped CLI commands under `workspace`, `mainline`, `domain-handler`, `authority`, `pass` and `package`;
- `MedAutoGrantDomainEntry` as the structured domain action target;
- `domain-handler export|dispatch` as the guarded OPL handler target returning refs, owner receipt, typed blocker, verdict refs and authority action metadata;
- product/status/user-loop/runtime/lifecycle/memory/package shell code only as refs-only adapter, direct handler target, minimal authority function, diagnostic or migration input until explicit MAG owner physical-delete receipt exists.

## Remaining Candidates

Remaining retirement/evidence tails are unchanged:

- active product/domain-handler/runtime/autonomy/CLI handler or adapter shells still need production default caller, direct/hosted parity, owner receipt roundtrip, continuous no-forbidden-write, App/workbench consumption and explicit physical-delete owner receipt before deletion;
- `submission_ready_export_gate` still needs a real human-gate receipt or updated MAG-owned typed blocker;
- Temporal long-soak and sustained App/operator/release consumption remain evidence gates;
- any future text that turns provider completion, grouped CLI success, product-entry manifest success, refs-only accounting or no-resurrection scans into grant-ready, fundability-ready, quality/export-ready, submission-ready, production-ready or physical-delete authority is stale pollution.

## Verification

Minimum verification for this docs / retirement-audit tranche:

- `git diff --check -- docs/docs_portfolio_consolidation.md docs/history/docs-portfolio-coverage-ledger/README.md docs/history/docs-portfolio-coverage-ledger/2026-06-04-mag-retired-command-family-audit.md`
- strict conflict-marker scan over edited docs;
- OPL Doc doctor on the MAG governance worktree;
- focused no-resurrection tests covering the retired command family.
