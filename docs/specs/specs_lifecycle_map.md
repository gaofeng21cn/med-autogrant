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
| `OPL Runtime Manager`, Temporal target, provider-backed runtime, or active-adapter wording | Historical/provider-specific migration context. Current MAG wording is OPL Codex-first stage-led framework consuming MAG-owned descriptor/projection; MAG retains grant truth, quality, route, and export authority. |
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
