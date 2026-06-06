# MAG source/workspace lifecycle SSOT closeout

Owner: `Med Auto Grant`
Purpose: `source_workspace_lifecycle_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/workspace_lifecycle_policy.json`、`contracts/runtime-program/opl-family-contract-adoption.json#source_provenance`、`product-entry-manifest.source_provenance`、source/domain-handler source/tests、CLI/API behavior、runtime receipts 和语义化 `human_doc:*` id。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T07:28:54Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Semantic theme: `source/workspace lifecycle policy and source provenance refs`
- Governance mode: SSOT-first contract/test/docs consolidation, not prose expansion.

## Single Source Of Truth

Machine SSOT:

- `contracts/workspace_lifecycle_policy.json`
  - owns the OPL-owned workspace/file lifecycle structural policy for MAG.
  - repo source may keep only locator/index/schema/receipt refs and no-forbidden-write proof.
  - true workspace/runtime artifacts stay outside repo source.
  - domain-owned authority vocabulary must use MAG grant semantics: domain truth, fundability / quality / export / submission verdict, artifact body authority, memory body accept/reject and owner receipt.
- `contracts/runtime-program/opl-family-contract-adoption.json#source_provenance`
  - owns OPL family adoption projection for body-free source refs.
- `product-entry-manifest.source_provenance` and `domain_handler_export.source_provenance`
  - expose the same body-free refs for OPL locator/index/projection consumption.
- `tests/test_workspace_lifecycle_policy_contract.py`
  - guards OPL-owned lifecycle policy, externalized roots, locator refs and MAG grant authority vocabulary.

Human-doc support:

- `docs/source/README.md`
  - remains a thin support index and direct-reader guard for source/workspace refs.
- `contracts/README.md`
  - indexes the machine contract and authority split; it does not become a lifecycle truth owner.

## Peer Surface Classification

| Surface | Classification | Action |
| --- | --- | --- |
| `contracts/workspace_lifecycle_policy.json#lifecycle_authority_split.domain_owned_authority` | `conflicts_with_ssot` | Replaced cross-domain `quality_export_visual_verdict` vocabulary with MAG-specific `fundability_quality_export_submission_verdict`. |
| `tests/test_workspace_lifecycle_policy_contract.py` | `covered_by_ssot` guard gap | Added focused meta tests for OPL-owned lifecycle policy, externalized roots, locator refs and MAG authority vocabulary. |
| `docs/source/README.md` | `covered_by_ssot` + `entry_pointer_needed` | Added direct pointers to `contracts/workspace_lifecycle_policy.json` and source provenance machine surfaces; kept docs/source as support index only. |
| `contracts/README.md` | `covered_by_ssot` + `entry_pointer_needed` | Added direct machine-contract index entry for source/workspace/file lifecycle. |

## Content-Level Consolidation

- OPL owns generic workspace/source/file lifecycle, locator/index, restore/retention and operator projection primitives.
- MAG repo source keeps only pack, contracts, schemas, locator refs, policy refs, receipt refs, no-forbidden-write proof and domain code.
- MAG keeps grant source truth, workspace truth, fundability / quality / export / submission verdicts, artifact body authority, memory accept/reject and owner receipt.
- `docs/source/README.md` is not a workspace truth plan, source intake plan, runtime artifact root or generic workspace/source shell.
- This lane does not authorize physical deletion of active workspace/source/domain-handler/product-entry code. Physical cleanup still requires generated/default caller evidence, direct/hosted parity, owner receipt / typed blocker roundtrip, no-active-caller proof, no-forbidden-write proof and MAG owner physical-delete receipt.

## Verification

Commands run from `/Users/gaofeng/workspace/med-autogrant` worktree:

```bash
rtk ./scripts/verify.sh
rtk ./scripts/run-pytest-clean.sh -q tests/test_workspace_lifecycle_policy_contract.py tests/test_opl_family_contract_adoption.py tests/product_entry_cases/test_manifest_and_status.py tests/product_entry_cases/test_domain_handler.py
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" contracts/workspace_lifecycle_policy.json contracts/README.md docs/source/README.md docs/history/docs-portfolio-coverage-ledger/README.md docs/history/docs-portfolio-coverage-ledger/2026-06-06-mag-source-workspace-lifecycle-ssot-closeout.md tests/test_workspace_lifecycle_policy_contract.py
rtk rg -n "quality_export_visual_verdict" contracts/workspace_lifecycle_policy.json docs/source/README.md contracts/README.md
/Users/gaofeng/.local/bin/opl-doc-doctor doctor . --format json
```

Result:

- Focused pytest passed: `29 passed, 31 subtests passed`.
- `scripts/verify.sh` passed: line-budget check, CLI smoke `4 passed`, fast tests `239 passed`, `464 deselected`, `154 subtests passed`.
- `git diff --check` passed.
- Conflict-marker scan found no matches.
- Targeted current contract/docs stale scan found no matches; the retired `quality_export_visual_verdict` term remains only in the new negative guard test and this provenance closeout.
- OPL Doc doctor reported `finding_count=0`.

## Remaining Scope

This lane closes only source/workspace lifecycle policy vocabulary drift and thin source-support index pointers.

Carry forward:

- Product-entry/domain-handler generated default caller evidence, direct/hosted parity, no-active-caller proof and physical-delete owner receipt remain separate evidence gates.
- Delivery/package lifecycle, runtime topology, broader docs portfolio, App/operator sustained consumption and Temporal long-soak remain separate lanes.
