# MAG delivery/package lifecycle SSOT closeout

Owner: `Med Auto Grant`
Purpose: `delivery_package_lifecycle_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `src/med_autogrant/submission_ready.py`、`src/med_autogrant/artifact_bundle.py`、`src/med_autogrant/final_package.py`、`src/med_autogrant/hosted_contract_bundle.py`、`src/med_autogrant/product_entry_parts/package_lifecycle_handoff.py`、domain entry / route / operator contract builders、CLI/API behavior、runtime receipts 和语义化 `human_doc:*` id。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T09:59:42Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Semantic theme: `delivery/package lifecycle route and contract test SSOT`
- Governance mode: remove test-side second truth sources; keep active package authority until OPL/App hosted replacement has machine evidence.

## Single Source Of Truth

Machine SSOT:

- `src/med_autogrant/domain_runtime_parts/shared.py`
  - owns `AUTHOR_SIDE_ROUTE_IDS`.
- `src/med_autogrant/domain_runtime_parts/contracts.py`
  - owns `build_author_side_route_contract(...)` and `build_operator_contract()["canonical_export_surfaces"]`.
- `src/med_autogrant/domain_entry_contract.py`
  - owns `build_domain_entry_contract()` and command contracts.
- Package authority remains in MAG domain source:
  - `submission_ready.py`
  - `artifact_bundle.py`
  - `final_package.py`
  - `hosted_contract_bundle.py`
  - `product_entry_parts/package_lifecycle_handoff.py`

Human-doc support:

- This closeout records the retirement of the test-side duplicate contract surface only.
- Current delivery/package reader guidance remains under `docs/delivery/`, `docs/product/`, active specs lifecycle owners and current contracts/source/tests.

## Peer Surface Classification

| Surface | Classification | Action |
| --- | --- | --- |
| `tests/support/domain_contracts.py` | `conflicts_with_ssot` | Deleted. It duplicated route ids, domain entry command contracts and canonical export surfaces that are now derived from production builders/constants. |
| `tests/product_entry_cases/support.py` | `covered_by_ssot` support helper | Replaced support constants and hand-written landed route map with production `build_domain_entry_contract()`, `build_operator_contract()`, `AUTHOR_SIDE_ROUTE_IDS` and `build_author_side_route_contract(...)`. Removed unused pending-route helper block from the pre-landed handoff era. |
| `tests/test_domain_runtime.py` | `covered_by_ssot` support helper | Replaced hand-written landed route map and old pending-route requirements with production route builder and route ids. |
| hosted contract bundle tests | `covered_by_ssot` assertions | Replaced imports from deleted test facade with production operator contract / route id sources. |
| Package public commands and implementations | `active_domain_authority` | Kept. `package artifact-bundle`, `package final-package`, `package hosted-contract-bundle` and `package submission-ready` still back active MAG package/export authority and cannot be physically deleted in this lane. |

## Content-Level Consolidation

- Tests no longer own a parallel domain command catalog, export surface list or author-side route id list.
- Expected author-side route payloads are produced through the same production route builder that runtime/product-entry/hosted contract surfaces use.
- Old pending handoff route helpers were removed from tests because current author-side route catalog is fully landed.
- This lane does not authorize package authority deletion. Physical deletion requires OPL/App generated replacement proof, direct/hosted parity, owner receipt or typed blocker roundtrip, no-active-caller proof, and MAG owner physical-delete receipt.

## Verification

Commands run from `/Users/gaofeng/workspace/med-autogrant/.worktrees/mag-delivery-package-lifecycle-ssot`:

```bash
rtk ./scripts/verify.sh
rtk ./scripts/run-pytest-clean.sh -q tests/test_domain_runtime.py tests/test_hosted_contract_bundle.py tests/test_hosted_contract_bundle_control_plane.py tests/test_hosted_contract_bundle_checkpoint_cases.py tests/product_entry_cases/test_direct_entry.py tests/product_entry_cases/test_failure_modes.py tests/product_entry_cases/test_entry_envelope.py tests/product_entry_cases/test_package_lifecycle_handoff.py
rtk rg -n "support\\.domain_contracts|tests/support/domain_contracts|_expected_pending_route|PENDING_ROUTE_REQUIREMENTS|_expected_landed_route|_service_safe_surface|DOMAIN_ENTRY_COMMAND_CONTRACTS = \\[|SUPPORTED_DOMAIN_ENTRY_COMMANDS = \\[|CANONICAL_EXPORT_SURFACES = \\[" tests src contracts
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" docs/history/docs-portfolio-coverage-ledger/README.md docs/history/docs-portfolio-coverage-ledger/2026-06-06-mag-delivery-package-lifecycle-ssot-closeout.md tests/product_entry_cases/support.py tests/test_domain_runtime.py tests/test_hosted_contract_bundle.py tests/test_hosted_contract_bundle_checkpoint_cases.py tests/test_hosted_contract_bundle_control_plane.py
rtk /Users/gaofeng/.local/bin/opl-doc-doctor doctor . --format json
```

Result:

- Baseline `scripts/verify.sh` passed before edits: line-budget check, CLI smoke `4 passed`, fast tests `239 passed`, `464 deselected`, `154 subtests passed`.
- Focused pytest passed after edits: `45 passed, 37 subtests passed`.
- Final `scripts/verify.sh` passed after edits: line-budget check, CLI smoke `4 passed`, fast tests `239 passed`, `464 deselected`, `154 subtests passed`.
- `git diff --check` passed.
- Conflict-marker scan found no matches.
- Duplicate test facade / old helper scan found no matches.
- OPL Doc doctor reported `finding_count=0`.

## Remaining Scope

This lane closes only delivery/package lifecycle test SSOT duplication and old pre-landed route helper residue.

Carry forward:

- Physical retirement of package commands or implementation remains blocked until OPL/App hosted package lifecycle replacement and MAG owner receipt evidence exist.
- Direct/hosted parity, generated default caller evidence, no-active-caller proof and package physical-delete receipt remain separate evidence gates.
