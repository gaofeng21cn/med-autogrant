# Specs Lifecycle Map

Status: `active specs governance`
Owner: `Med Auto Grant`
Purpose: classify the dense `docs/specs/` portfolio without breaking path-stable provenance
State: `current index`
Machine boundary: human-readable index only; machine surfaces must use `contracts/runtime-program/current-program.json`, schemas, source files, CLI/API behavior, or semantic `human_doc:*` ids.

## Why This Exists

`docs/specs/` contains current truth records, support records, activation packages, fail-closed hardening notes, and historical tranche documents. A bulk physical move would break old audit paths and make `current-program.json` harder to interpret.

The current rule is therefore index-first lifecycle management:

- keep path-stable specs in `docs/specs/` while they are still cited by current-program, history, or old audit evidence;
- classify their lifecycle state here and in `docs/specs/README*`;
- keep a first-screen lifecycle note in dated support/history specs so direct-file readers do not mistake old `Current Truth` titles for the current owner line;
- avoid adding new dated root specs unless the file is explicitly admitted as a current owner surface;
- move records physically only in small batches after inbound path references are gone.

## Active Current Specs

These records are still directly linked from the docs guide or current status and define specific active boundaries. They are current only for the boundary named in the second column; the core docs and `current-program.json` still own the overall product state.

| Spec | Active boundary |
| --- | --- |
| [Critique Codex CLI Executor Current Truth](./2026-04-13-critique-codex-cli-executor-current-truth.md) | critique executor vocabulary and Codex CLI route |
| [AI-first Quality Boundary Current Truth](./2026-04-27-ai-first-quality-boundary-current-truth.md) | AI-first quality ownership and projection boundary |
| [Authoring Completion Semantics Current Truth](./2026-04-23-authoring-completion-semantics-current-truth.md) | authoring completion semantics |
| [Quality Governance, Autonomy Controller, And Family Grammar Current Truth](./2026-04-22-quality-autonomy-family-grammar-current-truth.md) | quality governance, autonomy controller, and family grammar |

## File-Level Lifecycle Table

This table is the direct-reader guard for the dense path-stable specs set. It
uses exact files where the file is an active owner or a high-risk singleton, and
exact filename families where a batch shares the same lifecycle, owner, and next
hop. A file can remain under `docs/specs/` for path stability while its current
content owner is elsewhere.

| File or exact family | Lifecycle | Current owner / replacement | Reader action |
| --- | --- | --- | --- |
| `2026-04-13-critique-codex-cli-executor-current-truth.md` | `active_current_spec` | active spec + core docs | Read for critique executor vocabulary and Codex CLI route. |
| `2026-04-27-ai-first-quality-boundary-current-truth.md` | `active_current_spec` | active spec + quality owner docs | Read for AI-first quality boundary. |
| `2026-04-23-authoring-completion-semantics-current-truth.md` | `active_current_spec` | active spec + authoring completion owner docs | Read for completion semantics. |
| `2026-04-22-quality-autonomy-family-grammar-current-truth.md` | `active_current_spec` | active spec + current quality/autonomy docs | Read for quality governance, autonomy controller, and family grammar. |
| `2026-04-07-formal-entry-matrix-current-truth.md` | `support_current_truth` | core five + `current-program.json` | Use as formal-entry support; do not treat as full product truth. |
| `2026-04-07-durability-model-clarification.md` | `support_reference` | architecture/status + runtime-state docs | Use for durability vocabulary only. |
| `2026-04-07-p2a-*`, `2026-04-07-p2b-*`, `2026-04-07-p2c-*` | `absorbed_support` | current authoring pass docs, route catalog, core docs | Use retained content as authoring-flow provenance; current route truth lives in source/contracts. |
| `2026-04-07-p3a-*`, `2026-04-08-p3b-*`, `2026-04-08-p3c-*` | `absorbed_support` | current critique/revision and quality docs | Use for mentor/review/rollback provenance; do not revive phase backlog. |
| `2026-04-08-p4a-*`, `2026-04-08-p4b-*` | `absorbed_support` | product projection, verification, and checkpoint owners | Use for direct cockpit/progress and verification lessons only. |
| `2026-04-12-p4a-*`, `2026-04-12-p4b-*`, `2026-04-12-p4c-*`, `2026-04-13-p4e-*`, `2026-04-13-p4f-*` | `support_current_truth` | product-entry/product-status/user-loop/package owners | Use for product-entry internals; public identity remains single MAG app skill. |
| `2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md` | `support_current_truth` | schemas/source + product-entry manifest | Use for schema-backed route/product-entry contract support. |
| `2026-04-13-full-grant-authoring-executor-current-truth.md` | `support_current_truth` | route-selected executor docs + default Codex CLI owner | Use for landed authoring executor scope; it does not promote hosted proof lanes. |
| `2026-04-12-author-side-executor-routing-contract-current-truth.md` | `support_current_truth` | executor routing schema/source | Use for route-selected executor contract support. |
| `2026-04-12-hosted-caller-consumption-proof-current-truth.md`, `2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md` | `integration_reference` | hosted contract bundle + references | Use for hosted caller consumption proof; not public hosted runtime maturity. |
| `2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md` | `integration_reference` | product-entry manifest + OPL handoff refs | Use for OPL handoff shape; old Gateway wording is provenance. |
| `2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md` | `superseded_reference` | OPL stage-led framework roadmap + MAG status | Use only after applying current OPL/MAG owner split. |
| `2026-04-06-*` | `historical_provenance` | core five + history/specs index | Use for early foundation design only. |
| `2026-04-08-p5a-*`, `2026-04-08-p5b-*` | `future_activation_history` | domain admission/future planning owners | Do not treat as active P5 backlog. |
| `2026-04-08-r1a-*`, `2026-04-08-r1b-*`, `2026-04-08-r2a-*`, `2026-04-08-r3a-*`, `2026-04-09-r3a-*`, `2026-04-09-r4a-*`, `2026-04-09-r5a-*` | `historical_activation_package` | current pass/package/runtime docs + history/specs index | Use for activation provenance; current behavior lives in source/contracts. |
| `2026-04-08-runtime-first-productization-program.md`, `2026-04-08-runtime-first-r1-to-r5-boundary-map.md` | `historical_program_record` | core docs + history/specs index | Use for R1-R5 formation history, not current execution order. |
| `2026-04-09-post-r5a-local-runtime-hardening-brief.md`, `2026-04-10-post-r5a-local-runtime-*`, `2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md` | `support_or_history_by_subsection` | core docs + route/runtime owner docs | Use fail-closed and honest-stop lessons; do not restore old local runtime owner. |
| `2026-04-10-post-r5a-final-package-*`, `2026-04-10-post-r5a-hosted-contract-bundle-*`, `2026-04-10-post-r5a-stage-route-*`, `2026-04-10-post-r5a-worktree-aware-*`, `2026-04-10-post-r5a-revised-*` | `historical_fail_closed_record` | package/export schemas + history/specs index | Use for fail-closed provenance and path-stable audit. |
| `2026-04-11-hermes-backed-*`, `2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`, `2026-04-12-upstream-hermes-agent-fast-cutover-*` | `superseded_provider_proof` | current core docs + explicit hosted/proof refs | Use as Hermes proof/provenance only; default runtime owner remains `codex_cli`. |

## Support Current-Truth Records

These records still explain current or recently landed machinery, but they are not the default reading path. Treat them as support references below the core docs and `current-program.json`.

Support records are valid only for their still-current subsection. If they contain old provider, gateway, hosted, or pending-route wording, read that part as history unless a current owner doc promotes it.

| Group | Records |
| --- | --- |
| Formal entry / durability | `2026-04-07-formal-entry-matrix-current-truth.md`, `2026-04-07-durability-model-clarification.md` |
| P2-P4 absorbed grant flow | `2026-04-07-p2a-*`, `2026-04-07-p2b-*`, `2026-04-07-p2c-*`, `2026-04-07-p3a-*`, `2026-04-08-p3b-*`, `2026-04-08-p3c-*`, `2026-04-08-p4a-*`, `2026-04-08-p4b-*` |
| Local runtime closeout / output consistency | `2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md`, `2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md`; useful for fail-closed and honest-stop lessons; current runtime owner wording lives in the core docs and active specs |
| Hosted / OPL handoff support | `2026-04-12-hosted-*`, `2026-04-12-opl-aligned-*`, `2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md`; useful for contract consumption and route/export handoff, while old `OPL Gateway` or hosted-product completion language remains provenance |
| Product entry and package surfaces | `2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md`, `2026-04-12-p4a-*`, `2026-04-12-p4b-*`, `2026-04-12-p4c-*`, `2026-04-13-full-grant-authoring-executor-current-truth.md`, `2026-04-13-p4e-*`, `2026-04-13-p4f-*` |

## Provider And Hosted Wording Disposition

The content audit assigns older provider-runtime families to these current dispositions:

| Wording family | Current disposition |
| --- | --- |
| `Hermes-backed runtime substrate owner` in `2026-04-11-hermes-backed-*` | Historical/provider-specific. Current default execution is Codex CLI, with Hermes kept as explicit hosted/proof lane or external provider only when selected. |
| `upstream Hermes-Agent fast cutover` board and proof records | Historical/proof context. They remain useful for proof-lane vocabulary and fail-closed evidence; default install/runtime ownership lives in the current owner docs. |
| `OPL Gateway`, `gateway/federation`, and `future P5` language | Historical or future activation context unless the core docs or current contracts explicitly promote it. |
| `OPL Runtime Manager`, Temporal target, provider-backed runtime, or active-adapter wording | Historical/provider-specific migration context. Current MAG wording is that OPL is a stage-led framework with Agent executors as the minimum execution unit, consuming MAG-owned descriptor/projection; MAG retains grant truth, quality, route, and export authority. |
| `hosted contract bundle` | Current integration/reference export surface. Hosted runtime, Web UI, and external portal submission need separate current owner evidence. |

## Historical Provenance Records

These records are retained for auditability and path stability. They do not define current truth unless another active surface explicitly points to a still-valid subsection.

| Group | Records |
| --- | --- |
| Foundation design | `2026-04-06-*` |
| Future activation packages | `2026-04-08-p5a-*`, `2026-04-08-p5b-*` |
| Runtime-first R packages | `2026-04-08-r1a-*`, `2026-04-08-r1b-*`, `2026-04-08-r2a-*`, `2026-04-08-r3a-*`, `2026-04-08-runtime-first-*` |
| R3/R4/R5 activation packages | `2026-04-09-*` |
| Post-R5A fail-closed artifact-bundle notes | `2026-04-10-post-r5a-final-package-*`, `2026-04-10-post-r5a-hosted-contract-bundle-*`, malformed/fail-closed variants |
| Other post-R5A activation notes | `2026-04-10-post-r5a-local-runtime-validation-*`, `2026-04-10-post-r5a-revised-*`, `2026-04-10-post-r5a-stage-route-*`, `2026-04-10-post-r5a-worktree-aware-*` |
| Superseded Hermes/provider records | `2026-04-11-hermes-backed-*`, `2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md`, `2026-04-12-upstream-hermes-agent-fast-cutover-board.md`, `2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md` |

The archive reading entry for these groups remains [Historical specs](../history/specs/README.md).

## Admission Rule

New technical records should not default to another dated file in `docs/specs/`.

Use this decision path:

1. If it changes current public role, runtime boundary, authoring quality, or active command semantics, update the core five, `current-program.json`, schemas/source, and a small active spec only when the boundary needs a narrative explanation.
2. If it is implementation work still in progress, put it in `docs/plans/` while active and move it to `docs/history/plans/` after closeout.
3. If it is background, OPL handoff, distribution, or support material, put it in `docs/references/`.
4. If it is a completed activation package, migration record, or superseded tranche, put it in `docs/history/` or leave it path-stable under `docs/specs/` with this map marking it historical.
