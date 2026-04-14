# Docs Guide

**English** | [中文](./README.zh-CN.md)

This directory is the technical reading layer for `Med Auto Grant`.
The repository home should stay readable for applicants and domain experts.
This guide is for readers who need the repo-tracked contracts, current-truth specs, references, and implementation history behind that public entry.

## Start Here By Audience

| Audience | Start here | Why |
| --- | --- | --- |
| Potential users and domain experts | [Repository home](../README.md), [Domain Positioning](./domain-positioning.md), [MVP Scope](./mvp-scope.md) | Understand what the grant line is for before reading technical internals |
| Technical readers and planners | [Project](./project.md), [Status](./status.md), [Architecture](./architecture.md), [Invariants](./invariants.md), [Decisions](./decisions.md), [Contracts Overview](../contracts/README.md) | Get the current truth, boundaries, and mainline direction quickly |
| Developers and maintainers | [Specs directory](./specs/), [References directory](./references/), [Plans directory](./plans/), [History archive](./history/omx/README.md) | Inspect current-truth records, internal references, planning history, and archival material |

## Current Baseline

- `Med Auto Grant` is the active medical `Grant Ops` repository line on the applicant side.
- The current executable runtime line is `CLI-first + real upstream Hermes-Agent runtime substrate`.
- Repo-tracked truth also keeps the phrase real upstream `Hermes-Agent` runtime substrate explicit for this line.
- Legacy repo-local helpers survive only as a compatibility bridge and regression oracle.
- Repo-local adapters preserve grant-domain truth and entry semantics, but they are not the runtime substrate owner.
- The current product-facing shell, projections, and local `submission-ready` package are landed, while a mature hosted grant frontend is still future work.
- Top-level federation admission and handoff wording remain separately gated at `OPL`.
- The formal-entry matrix remains `CLI`, `MCP`, and `controller`.
- Current controller-owned, read-only projections continue to include `grant-progress`, `grant-cockpit`, `grant-direct-entry`, and `grant-user-loop`, with schema-backed boundaries above the author-side line.
- The current lightweight grant `product entry` shell is the active Product-entry shell, while richer hosted product work remains future-facing.

## Technical Working Set

Read these first before changing repo state:

- [Project](./project.md)
- [Status](./status.md)
- [Architecture](./architecture.md)
- [Invariants](./invariants.md)
- [Decisions](./decisions.md)
- [Contracts Overview](../contracts/README.md)
- [`current-program.json`](../contracts/runtime-program/current-program.json)

## Default Public Surface

- [Repository home](../README.md)
- [Domain Positioning](./domain-positioning.md)
- [MVP Scope](./mvp-scope.md)

These files are the default public-facing entry surfaces and should stay mirrored in English and Chinese where applicable.

## Repo-Tracked Technical Docs

### Current truth and activation records

- [`current-program.json`](../contracts/runtime-program/current-program.json)
- [Specs directory](./specs/)
- [Upstream Hermes-Agent fast cutover current truth](./specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md)
- [Lightweight product entry and OPL handoff current truth](./specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md)
- [Schema-backed product entry and routing contract current truth](./specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md)
- [Hosted contract bundle entry and route catalog current truth](./specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md)
- [Hosted caller consumption proof current truth](./specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md)
- [OPL-aligned ideal target and phase map current truth](./specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md)
- [Full grant authoring executor current truth](./specs/2026-04-13-full-grant-authoring-executor-current-truth.md)
- [P4.F local submission-ready package current truth](./specs/2026-04-13-p4f-local-submission-ready-package-current-truth.md)

The lightweight grant `product entry` shell is the current Product-entry shell, and the current schema-backed freeze also keeps `hosted contract bundle`, `domain_entry_contract`, `supported_commands`, and `command_contracts` visible for hosted caller / external caller consumption.

### Contracts and schemas

- [Contracts Overview](../contracts/README.md)
- [`runtime-program/`](../contracts/runtime-program/)
- [`schemas/v1/`](../schemas/v1/)

### Internal references

- [Lightweight product entry and OPL handoff](./references/lightweight_product_entry_and_opl_handoff.md)
- [Series doc governance checklist](./references/series-doc-governance-checklist.md)

### Plans and history

- [Plans directory](./plans/)
- [OPL-aligned target shape and hosted caller plan](./plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md)
- [Minimal Scaffold Plan](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [History archive](./history/omx/README.md)

## Documentation Rules

- Keep [Repository home](../README.md) readable for grant applicants and non-technical experts.
- Keep the default public docs mirrored in English and Chinese where they are part of the public surface.
- Keep `docs/specs/` authoritative for repo-tracked current truth and activation packages without letting it replace the user-facing home page.
- Keep references, plans, and history available, but do not let them become the default public entry path.

## Governance

- Documentation governance freezes in [series doc governance checklist](./references/series-doc-governance-checklist.md), the technical working set, and repo-tracked contract/doc surfaces rather than in `AGENTS.md` alone.
- `README*` and `docs/README*` are the default public entry.
- `docs/specs/**` holds repo-tracked current truth and activation packages.
- `docs/references/**` holds internal reference notes.
- `docs/plans/**` and `docs/history/**` are historical support material.
