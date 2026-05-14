# Docs Portfolio Consolidation

Date: `2026-05-11`
Last updated: `2026-05-14`

This note freezes the documentation portfolio boundary after the May 2026 consolidation and the OPL stage-led runtime alignment pass. The May 14 plan refresh also freezes direct retirement as the cleanup posture for obsolete modules, interfaces, CLI aliases, facade patch bridges, and aggregate compatibility tests.

## Lifecycle Signals

Each docs layer is governed by four lifecycle signals:

- `owner`: the surface owner responsible for keeping the document aligned.
- `purpose`: the reason the document exists in the portfolio.
- `state`: one of `current`, `reference`, `history`, or `active_plan`
  for work that is still explicitly tracked under `docs/plans/`.
- `machine boundary`: whether machine consumers may rely on the surface directly.

`README*` and `docs/**` are human-readable surfaces. Machine-readable control must use contract/schema/source paths, or semantic `human_doc:*` ids when a machine surface needs to relate to prose. Prose paths are navigation aids, not API stability promises.

## Content-Level Consolidation Rule

Lifecycle decisions are made at the content level first.
A single document can contain current facts, support explanation, historical
provider notes, and completed plan text. Maintainers should separate those
roles before expanding or moving the file:

1. Merge current facts into the core docs, active specs, or the current-program
   truth surface.
2. Keep active future work in `docs/plans/` only while it still needs owner,
   gate, or closeout tracking.
3. Keep support material in `docs/references/` or an active spec only when it
   explains current behavior or a current boundary.
4. Treat older dated specs and completed plans as history/provenance even when
   path stability keeps them under `docs/specs/`.
5. When a new owner surface replaces an old module, interface, test entry,
   facade patch bridge, or CLI shell alias, move any active caller to the new
   surface and retire the old one directly. Do not add compatibility shims,
   aliases, re-export facades, or compatibility-only aggregate tests.
6. Entry pages should first show current state, hierarchy, old/new
   relationship, and next reading step. Active specs, historical specs,
   references, verification notes, and completed plans should appear under
   their lifecycle roles.

## Current State Owner Map

The May 11 content audit assigns one current owner for each recurring theme:

| Theme | Current owner | Support owner | History owner |
| --- | --- | --- | --- |
| Public product identity | `README*`, `docs/domain-positioning*`, `docs/mvp-scope*` | `docs/README*` | `docs/history/domain-harness-os-positioning.md` |
| MAG as independent grant domain agent | `docs/project.md`, `docs/status.md`, `docs/architecture.md` | `docs/invariants.md`, `docs/decisions.md` | older `Grant Foundry`, `Domain Harness OS`, and gateway wording |
| OPL relationship | `docs/status.md`, `docs/architecture.md`, `docs/decisions.md` | `docs/references/opl_family_contract_adoption.md` | old OPL Runtime Manager, Temporal target, Hermes-first, gateway, monorepo, and active-adapter notes |
| Stage semantics | `docs/status.md`, `docs/architecture.md` | `docs/references/opl_family_contract_adoption.md`, `docs/specs/2026-04-13-full-grant-authoring-executor-current-truth.md` | old pending handoff and future P5 activation packages |
| Default execution owner | `docs/project.md`, `docs/architecture.md`, `docs/invariants.md` | `docs/specs/2026-04-13-critique-codex-cli-executor-current-truth.md` | old Hermes-backed runtime owner specs and proof boards |
| Authoring quality and completion | `docs/status.md`, `docs/invariants.md` | `docs/specs/2026-04-27-ai-first-quality-boundary-current-truth.md`, `docs/specs/2026-04-23-authoring-completion-semantics-current-truth.md`, `docs/specs/2026-04-22-quality-autonomy-family-grammar-current-truth.md` | completed quality/autonomy planning notes |
| Submission-ready export | `docs/project.md`, `docs/architecture.md` | `docs/specs/2026-04-13-p4f-local-submission-ready-package-current-truth.md` | post-R5A local export hardening notes |
| Docs lifecycle | this file | `docs/README*`, `docs/specs/specs_lifecycle_map.md`, `docs/references/series-doc-governance-checklist.md` | prior plans and historical specs indexes |

When two documents appear to provide parallel current statements, update the
owner above and reclassify the other file as support or history. Each theme has
one active owner surface.

## Partition Disposition

| Partition | Current role | Absorbed / historical handling |
| --- | --- | --- |
| `README*` | Public first page for applicants, domain experts, and agents. | Keep sparse and bilingual. Move implementation or provider detail into docs/specs/references/history. |
| `docs/README*` | Technical route map and current-state summary. | It may summarize old/new relationships, but should send old routes to history instead of restating them as live options. |
| Core five | Current owner set for project, status, architecture, invariants, and decisions. | Superseded decisions remain in `docs/decisions.md` only when explicitly marked superseded and explained as provenance. |
| `docs/domain-positioning*` and `docs/mvp-scope*` | Root public-doc allowlist for domain role and MVP scope. | Update for public-facing current boundary changes; runtime/provider histories belong in specs, references, or history. |
| `docs/specs/` | Mixed path-stable technical record layer. Only the active specs in `docs/specs/README*` are current owner records. | Older dated specs remain in place for audit path stability and are classified through `docs/specs/specs_lifecycle_map.md` plus `docs/history/specs/README*`. |
| `docs/references/` | Support material for current boundaries: memory policy, OPL family adoption, MAG north-star target state, and series doc governance. | Historical/provider-specific handoff notes have been moved to `docs/history/`. New reference docs must explain a current boundary or explicitly mark itself as target-state support material. |
| `docs/plans/` | Active-plan lane. It currently tracks the MAG ideal-state cross-repo gap and completion plan. | Completed plans live under `docs/history/plans/`; active plans stay here only while they still need owner, gate, or closeout tracking. Current plans use direct retirement for obsolete compatibility surfaces rather than preserving old aliases or aggregate tests. |
| `docs/history/` | Archive entry for retired lanes, completed plans, superseded specs, old provider notes, and positioning history. | History docs can preserve old wording, but must point readers back to current owner docs for live truth. |

## Key Document Disposition Table

| Document or group | Disposition | Reason |
| --- | --- | --- |
| `docs/docs_portfolio_consolidation.md` | Current docs lifecycle owner. | Holds the content-level owner map and partition rules for future maintainers. |
| `docs/specs/specs_lifecycle_map.md` | Current lifecycle index. | Classifies dense specs without breaking path-stable audit links; product truth remains in the core docs, active specs, and `current-program.json`. |
| `docs/specs/2026-04-13-critique-codex-cli-executor-current-truth.md` | Active spec. | Freezes default critique executor vocabulary and Codex CLI route. |
| `docs/specs/2026-04-13-full-grant-authoring-executor-current-truth.md` | Support current-truth spec. | Explains landed `direction_screening -> frozen` route catalog, while core docs own the current product summary. |
| `docs/specs/2026-04-22-quality-autonomy-family-grammar-current-truth.md` | Active spec. | Owns quality governance, autonomy controller, and family grammar detail below the core docs. |
| `docs/specs/2026-04-23-authoring-completion-semantics-current-truth.md` | Active spec. | Owns authoring completion semantics and the `TODO + explicit wakeup` boundary. |
| `docs/specs/2026-04-27-ai-first-quality-boundary-current-truth.md` | Active spec. | Owns AI-first quality boundary and prevents schema/controller layers from becoming hidden reviewers. |
| `docs/specs/2026-04-11-hermes-backed-*` | Historical/provider-specific support. | Their old Hermes-backed owner claims are superseded by Codex-default execution plus explicit hosted/proof lanes and OPL stage-led framework wording. |
| `docs/specs/2026-04-12-upstream-hermes-agent-fast-cutover*` | Historical/proof-lane context. | Useful for audit and proof vocabulary; default runtime truth lives in the current owner docs. |
| `docs/specs/2026-04-12-hosted-*` | Support/history depending on subsection. | Hosted bundle contract remains integration/reference; hosted runtime or gateway completion claims are historical. |
| `docs/specs/2026-04-08-p5*` | Historical future activation packages. | They describe earlier gateway/federation expansion prerequisites as archive material. |
| `docs/specs/2026-04-08-r*`, `2026-04-09-*`, `2026-04-10-post-r5a-*` | Historical local-runtime ladder and hardening provenance. | Their valid export/checkpoint lessons are absorbed into current owner docs and active specs; old local runtime maturity wording stays archival. |
| `docs/references/opl_family_contract_adoption.md` | Current reference. | Explains current descriptor/projection adoption under OPL stage-led framework while preserving MAG authority. |
| `docs/references/grant_strategy_memory_policy.md` | Current reference. | Explains current memory boundary without moving quality/fundability authority into memory. |
| `docs/references/med-auto-grant-ideal-state.zh-CN.md` | Active support reference. | Preserves the MAG north-star target state while pointing live truth back to core docs and `current-program.json`. |
| `docs/plans/mag-ideal-state-cross-repo-gap-plan.zh-CN.md` | Active plan. | Tracks the gap between the MAG north-star target, current MAG state, and current OPL/MAS/RCA family evidence; it guides production closure work without replacing current truth. It now treats obsolete modules/interfaces/tests as direct-retirement targets, not compatibility surfaces. |
| `docs/history/opl_managed_runtime_three_layer_contract.md` | Moved to history. | The old OPL Runtime Manager / provider owner framing is superseded by current OPL stage-led framework wording. |
| `docs/history/lightweight_product_entry_and_opl_handoff.md` | Moved to history. | The useful current handoff content is absorbed by core docs, active specs, and `opl_family_contract_adoption.md`; old Hermes Kernel wording is historical. |
| `docs/history/plans/**` | History. | Completed one-time plans and provenance records. |
| `docs/history/specs/**` | History. | Superseded handoff/proof specs and archive indexes. |

## Active Layer

- `README*`
- `docs/README*`
- `docs/domain-positioning*`
- `docs/mvp-scope*`
- `docs/project.md`
- `docs/status.md`
- `docs/architecture.md`
- `docs/invariants.md`
- `docs/decisions.md`
- `contracts/runtime-program/current-program.json`

These files are the active reading path for public positioning, current technical truth, and maintainer context.

Lifecycle:

- `owner`: MAG maintainers.
- `purpose`: public entry, current technical orientation, and maintainer routing.
- `state`: `current`.
- `machine boundary`: not directly machine-consumed, except for `contracts/runtime-program/current-program.json`; machine surfaces should reference prose through semantic `human_doc:*` ids.

Root-doc allowlist:

- `README*` stays intentionally sparse as the public first page.
- `docs/domain-positioning*` remains current because it states the active domain owner, public subject, and OPL/Hermes boundary.
- `docs/mvp-scope*` remains current because it states the current NSFC MVP scope and non-goals.
- No other root-level docs should be added to the default public path without updating this portfolio note and the docs guide.

## Active Plan Layer

- `docs/plans/mag-ideal-state-cross-repo-gap-plan.zh-CN.md`

Active plans are owner-tracked future work. They may compare target state,
current state, and completion gates, but they do not replace the core docs,
active specs, contracts, schemas, source, generated artifacts, or
`contracts/runtime-program/current-program.json`.
They also must not keep old modules, old CLI aliases, facade patch bridges, or
aggregate compatibility tests alive after the latest owner surface has replaced
them.

Lifecycle:

- `owner`: MAG maintainers.
- `purpose`: track explicit future work until absorbed into current owner docs,
  machine contracts, implementation, or history.
- `state`: `active_plan`.
- `machine boundary`: not machine-consumed; machine surfaces must use
  contracts/schema/source paths or semantic `human_doc:*` ids.

## Reference Layer

- `docs/references/**`
- `docs/specs/README*`
- `docs/specs/specs_lifecycle_map.md`
- active specs listed in `docs/specs/README*`
- repo-tracked truth surfaces listed by `contracts/runtime-program/current-program.json`

These files explain stable boundaries or current technical records without replacing the core docs.

Lifecycle:

- `owner`: the MAG subsystem or governance lane that owns the referenced boundary.
- `purpose`: explain stable context, cross-repo handoff, active spec routing, or maintainer governance.
- `state`: `reference`, unless a specs README explicitly indexes an active current-truth record.
- `machine boundary`: not directly machine-consumed; use schema/source paths for contracts and semantic `human_doc:*` ids for prose references.

## History Layer

- `docs/history/**`
- `docs/history/plans/**`
- `docs/history/specs/README*`
- `docs/history/domain-harness-os-positioning.md`
- older dated specs still stored under `docs/specs/*.md` for path stability but indexed as historical records

Historical files are provenance and audit material. They may preserve old task wording, old path references, and superseded tranche labels; they do not override the active layer.

Lifecycle:

- `owner`: MAG maintainers for archive integrity.
- `purpose`: preserve provenance, audit context, superseded positioning, and completed plans.
- `state`: `history`.
- `machine boundary`: not machine-consumed as current truth; any remaining machine surface must point to current contracts/schema/source or semantic `human_doc:*` ids.

The second-round review intentionally did not bulk-move older specs out of `docs/specs/`: many historical notes, rollout records, and current-program pointers still reference those original paths. The archive boundary is therefore enforced by the README/index layer rather than by rewriting every dated spec path.

The 2026-05-09 family docs governance pass made that rule explicit in [Specs Lifecycle Map](./specs/specs_lifecycle_map.md): active specs, support current-truth records, and historical provenance records can share the path-stable directory only while the README/index layer makes their lifecycle state unambiguous.

The 2026-05-11 OPL alignment pass further clarifies that older `OPL Runtime Manager`, Temporal, Hermes-first, gateway, monorepo, active-adapter, and local host runtime language is historical/provider-specific unless the active layer or a machine-readable contract explicitly promotes it. Current MAG docs should describe OPL as a stage-led runtime framework with Agent executors as the minimum execution unit that may consume MAG as an external domain dependency, with `Codex CLI` as the minimum execution unit and MAG retaining grant truth, quality, route, and export authority.

## Root AGENTS Alignment

Root `AGENTS.md` stays a work-method file. It should point maintainers to the
current docs reading order and lifecycle rules, while project truth remains in
the core docs, active specs, contracts, schemas, source, and generated
artifacts. When AGENTS wording drifts from this portfolio, update AGENTS to
match the docs/contract owner split and keep it as routing guidance.
