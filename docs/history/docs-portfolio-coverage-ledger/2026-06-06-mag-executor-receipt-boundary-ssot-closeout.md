# MAG executor receipt boundary SSOT closeout

Owner: `Med Auto Grant`
Purpose: `docs_portfolio_coverage_closeout`
State: `history_provenance`
Machine boundary: 本文是人读 closeout ledger。当前机器真相继续归 `contracts/runtime-program/current-program.json`、`contracts/private_functional_surface_policy.json`、source、tests、CLI/API behavior、runtime receipts 和语义化 `human_doc:*` id。

## Snapshot

- `RUN_SNAPSHOT_TS`: `2026-06-06T07:28:54Z`
- Repo: `/Users/gaofeng/workspace/med-autogrant`
- Semantic theme: `explicit non-default executor receipt boundary`
- Governance mode: SSOT-first content-level consolidation, not file-level polishing.

## Single Source Of Truth

### Current machine truth

- `contracts/runtime-program/current-program.json`
  - `default_stage_executor = codex_cli`
  - `executor_defaults.default_executor_name = codex_cli`
  - `executor_statuses.codex_cli = default`
  - `executor_statuses.hermes_agent = experimental`
  - `non_default_executor_requires_explicit_selection = true`
  - `non_default_executor_forbids_silent_codex_fallback = true`
- `contracts/private_functional_surface_policy.json`
  - `hermes_agent_role = explicit_non_default_opl_executor_adapter_receipt_lane_only`
  - `required_default_executor = codex_cli`
- `src/med_autogrant/critique_executor.py`
  - `DEFAULT_CRITIQUE_EXECUTOR_KIND = "codex_cli"`
  - `HERMES_AGENT_EXECUTOR_KIND = "hermes_agent"`
  - omitted `executor_kind` resolves to `codex_cli`
  - explicit `hermes_agent` requires an OPL agent execution receipt shape
- `tests/test_critique_executor.py`, `tests/test_domain_runtime.py`, `tests/test_domain_entry.py`, `tests/test_cli_validate_workspace.py`
  - cover default `codex_cli`
  - cover explicit `hermes_agent`
  - assert retired executor aliases fail closed
  - assert receipt shape is required for the Hermes proof lane

### Current docs owner

- `docs/active/mag-ideal-state-cross-repo-gap-plan.md` owns current gap/progress framing for MAG as a standard OPL Agent.
- `docs/specs/specs_lifecycle_map.md` and `docs/specs/README.md` own `docs/specs/` placement and direct-reader lifecycle rules.
- The three dated executor/product-entry specs below remain support records only within their current subsections.

The machine truth wins over dated support specs because the current default executor and non-default receipt contract are enforced by repo-tracked contracts/source/tests. The dated specs are human-readable support/provenance and cannot promote Hermes-Agent, Gateway/federation, hosted runtime, or compatibility bridge wording back into active owner truth.

## Peer Docs Classification

| Document / section | Classification | Action |
| --- | --- | --- |
| `docs/specs/2026-04-13-critique-codex-cli-executor-current-truth.md` / Honest Boundary | `more_specific_detail` with direct-reader stale-risk | Hardened wording so each negative claim explicitly says `不表示 ...`; kept `codex_cli` default and explicit `hermes_agent` receipt lane truth. |
| `docs/specs/2026-04-13-full-grant-authoring-executor-current-truth.md` / Honest Boundary | `more_specific_detail` with direct-reader stale-risk | Hardened wording so hosted runtime, OPL Gateway, and Hermes-native full-loop claims cannot be read as current state. |
| `docs/specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md` / Honest Boundary | `support_current_truth` with direct-reader stale-risk | Hardened wording and redirected critique executor truth to the active critique spec plus source/tests. |
| `docs/specs/specs_lifecycle_map.md` | `covered_by_ssot` for specs lifecycle | No content edit needed; it already classifies Hermes/Gateway/provider proof records as history/provenance and identifies current owners. |
| `docs/specs/README.md` | `covered_by_ssot` for specs index | No content edit needed; it already warns direct readers not to elevate support specs or history terms into current owner truth. |
| `docs/status.md` | `covered_by_ssot` for current status | No edit in this lane; no conflicting default-Hermes wording was selected for this semantic theme. |
| `docs/docs_portfolio_consolidation.md` | `out_of_scope` for this narrow lane | No edit; portfolio taxonomy already routes dated evidence to history/support layers. |
| `docs/history/specs/README.md` | `history_or_provenance` | No edit; historical Hermes/Gateway/provider records remain history-only. |

No section in this lane was classified as `conflicts_with_ssot` after the wording hardening. The previous risk was direct-reader ambiguity in negated bullet lists, not a machine-truth conflict.

## Modifications

- Rewrote three `Honest Boundary` negative lists from `它不意味着` to explicit `不表示 ...` phrasing.
- Kept support specs in place because `docs/specs/specs_lifecycle_map.md`, `docs/specs/README.md`, and `current-program.json` still reference their current subsections.
- Did not add compatibility wording, alias, facade, wrapper, fallback, or legacy test preservation language.

## Verification

Commands run from `/Users/gaofeng/workspace/med-autogrant`:

```bash
rtk git diff --check
rtk rg -n "^(<<<<<<<|=======|>>>>>>>)" docs/specs/2026-04-13-critique-codex-cli-executor-current-truth.md docs/specs/2026-04-13-full-grant-authoring-executor-current-truth.md docs/specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md docs/history/docs-portfolio-coverage-ledger/2026-06-06-mag-executor-receipt-boundary-ssot-closeout.md docs/history/docs-portfolio-coverage-ledger/README.md
rtk rg -n "Hermes-Agent default executor|critique.*默认.*Hermes|默认.*Hermes-Agent|hosted runtime 已完成|compatibility bridge 是当前目标" README* docs --glob '*.md' --glob '!docs/history/**'
rtk /Users/gaofeng/.local/bin/opl-doc-doctor doctor . --format json
```

Result:

- `git diff --check`: pass.
- Conflict-marker scan over edited docs: pass.
- Targeted stale scan over current docs excluding `docs/history/**`: no `Hermes-Agent default executor`, `critique.*默认.*Hermes`, or `默认.*Hermes-Agent` matches remain; remaining matches are current owner statements or explicit `不表示 ...` negative guards.
- `opl-doc-doctor`: pass, `finding_count = 0`, active truth owner `docs/active/mag-ideal-state-cross-repo-gap-plan.md`, `markdown_doc_count = 120`.

Dirty-boundary note: after this docs lane started, `src/med_autogrant/product_entry_parts/opl_owner_payload_response.py` and `tests/product_entry_cases/test_opl_owner_payload_response.py` appeared dirty. They were not read as this lane's write surface and were left untouched as external source/test changes.

## Remaining Scope

This tranche covers only the executor receipt boundary across the current specs/support records. It does not complete full MAG docs portfolio governance.

Carry forward:

- Review `docs/product/**`, `docs/runtime/**`, `docs/delivery/**`, and `docs/source/**` for long incremental lists and stale local-runtime/workspace/package helper surfaces.
- Continue checking `README*` and `docs/**/*.md` by semantic theme, with one SSOT owner per theme.
- Keep old Gateway/Hermes/provider/local-runtime records in `docs/history/**` unless a current owner explicitly reactivates a subsection with machine truth.

## Next Write Scope

Recommended next MAG lane:

- Semantic theme: `product-entry and package authority boundary`
- Candidate SSOT owner: `contracts/runtime-program/current-program.json`, product-entry schemas/source, `docs/specs/product-entry-support-record.md`, and active gap plan.
- Peer docs: `docs/product/**`, `docs/delivery/**`, `docs/specs/product-entry-support-record.md`, `docs/specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md`, `docs/history/specs/README.md`.
