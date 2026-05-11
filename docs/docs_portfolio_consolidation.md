# Docs Portfolio Consolidation

Date: `2026-05-11`

This note freezes the documentation portfolio boundary after the May 2026 consolidation and the OPL stage-led runtime alignment pass.

## Lifecycle Signals

Each docs layer is governed by four lifecycle signals:

- `owner`: the surface owner responsible for keeping the document aligned.
- `purpose`: the reason the document exists in the portfolio.
- `state`: one of `current`, `reference`, or `history`.
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
5. Entry pages should first show current state, hierarchy, old/new
   relationship, and next reading step. Active specs, historical specs,
   references, verification notes, and completed plans should appear under
   their lifecycle roles.

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

The 2026-05-11 OPL alignment pass further clarifies that older `OPL Runtime Manager`, Temporal, Hermes-first, gateway, monorepo, active-adapter, and local host runtime language is historical/provider-specific unless the active layer or a machine-readable contract explicitly promotes it. Current MAG docs should describe OPL as a Codex-first, stage-led agent runtime framework that may consume MAG as an external domain dependency, with `Codex CLI` as the minimum execution unit and MAG retaining grant truth, quality, route, and export authority.

## Root AGENTS Alignment

Root `AGENTS.md` stays a work-method file. It should point maintainers to the
current docs reading order and lifecycle rules, while project truth remains in
the core docs, active specs, contracts, schemas, source, and generated
artifacts. When AGENTS wording drifts from this portfolio, update AGENTS to
match the docs/contract owner split and keep it as routing guidance.
