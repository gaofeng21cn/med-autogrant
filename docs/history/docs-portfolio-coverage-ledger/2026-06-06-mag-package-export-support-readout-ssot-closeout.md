# MAG package/export support readout SSOT closeout

Owner: `Med Auto Grant`
Purpose: `package_export_support_readout_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `agent/knowledge/package_authority.md`、`agent/quality_gates/export_and_package.md`、`contracts/stage_control_plane.json`、`contracts/private_functional_surface_policy.json`、`src/med_autogrant/product_entry_parts/package_lifecycle_handoff.py`、package/export source、owner receipts、typed blockers 和相关 tests。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T10:06:15Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Semantic theme: `package/export support current-truth readout`
- Governance mode: content-level SSOT clarification; no source, contract, test or command-surface change.

## Single Source Of Truth

Machine SSOT:

- MAG authority truth:
  - `agent/knowledge/package_authority.md`
  - `agent/quality_gates/export_and_package.md`
  - `contracts/stage_control_plane.json`
  - `contracts/private_functional_surface_policy.json`
  - package/export source, owner receipts and typed blockers.
- Refs-only handoff truth:
  - `src/med_autogrant/product_entry_parts/package_lifecycle_handoff.py`
  - `tests/product_entry_cases/test_package_lifecycle_handoff.py`

Human support SSOT:

- `docs/specs/product-entry-support-record.md`

`docs/delivery/README.md` remains a thin support index and pointer. It does not duplicate package/export gates, active evidence ledgers or submission-ready status.

## Peer Surface Classification

| Surface | Classification | Action |
| --- | --- | --- |
| `docs/specs/product-entry-support-record.md` | `more_specific_detail` owner | Added a package/export SSOT readout that separates scientific review-ready, local submission-ready package/export gate, and external portal submission. |
| `docs/delivery/README.md` | `covered_by_ssot` thin pointer | Kept unchanged; it already points readers to Product Entry Support Record and forbids copying package/export gate status into delivery index. |
| `docs/active/mag-ideal-state-cross-repo-gap-plan.md` | `covered_by_ssot` active gap owner | Kept unchanged; it already states `submission_ready_export_gate` remains blocked by MAG human-gate receipt or typed blocker and forbids package existence/provider completion as readiness evidence. |
| `docs/status.md` / `docs/architecture.md` | `covered_by_ssot` current boundary docs | Kept unchanged; both already state MAG owns package/export authority and OPL consumes refs without ready-verdict authority. |
| `agent/knowledge/package_authority.md` / `agent/quality_gates/export_and_package.md` | `machine_authority_support` | Read as package/export authority source, not edited. |
| `src/med_autogrant/product_entry_parts/package_lifecycle_handoff.py` / focused test | `machine_refs_only_handoff` | Read as refs-only projection truth, not edited. |

## Content-Level Consolidation

- The support record now makes the three readiness layers explicit:
  - scientific review-ready;
  - local submission-ready package / export gate;
  - external submitted / portal submission.
- The support record now states that package existence, schema completeness, lifecycle completion, provider completion and grouped CLI success cannot declare ready status.
- The support record now routes unique detail into the right owner system:
  - MAG package authority and export verdict stay with MAG authority sources and owner receipts;
  - package lifecycle handoff stays refs-only and body-free;
  - OPL artifact/package lifecycle shell can consume refs but cannot hold MAG package authority or issue MAG ready verdicts.

## Verification

Commands run from `/Users/gaofeng/workspace/med-autogrant`:

```bash
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" docs
rtk /Users/gaofeng/.local/bin/opl-doc-doctor doctor . --format json
rtk ./scripts/run-pytest-clean.sh tests/product_entry_cases/test_package_lifecycle_handoff.py
```

Result:

- `git diff --check` passed.
- Conflict-marker scan found no matches.
- OPL Doc doctor reported `finding_count=0`.
- Focused package lifecycle handoff pytest passed: `6 passed`.

## Remaining Scope

This lane does not authorize source, contract, workflow, CLI or test retirement. Package command and implementation retirement remains blocked until OPL/App generated/default caller replacement, direct/hosted parity, owner receipt or typed blocker roundtrip, no-active-caller proof, continuous no-forbidden-write evidence, and explicit MAG physical-delete/tombstone owner receipt exist.
