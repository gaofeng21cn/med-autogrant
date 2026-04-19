# Docs Guide

**English** | [中文](./README.zh-CN.md)

This directory is the technical reading layer for `Med Auto Grant`.
The repository home should stay readable for applicants and domain experts.
This guide is for readers who need the technical records, trace records, reference notes, and implementation history behind that public entry.

## Start Here By Audience

| Audience | Start here | Why |
| --- | --- | --- |
| Potential users and domain experts | [Repository home](../README.md), [Domain Positioning](./domain-positioning.md), [MVP Scope](./mvp-scope.md) | Understand what the grant line is for before reading technical internals |
| Technical readers and planners | [Project](./project.md), [Status](./status.md), [Architecture](./architecture.md), [Invariants](./invariants.md), [Decisions](./decisions.md), [Contracts Overview](../contracts/README.md) | Get the current technical shape, boundaries, and mainline direction quickly |
| Developers and maintainers | [Specs directory](./specs/), [References directory](./references/), [Plans directory](./plans/), [History archive](./history/README.md) | Inspect technical records, reference notes, future work, and archival material |

## Current Technical Picture

- `Med Auto Grant` is the author-side medical grant domain gateway under the `OPL` family gateway and handoff surface.
- The formal-entry matrix remains `CLI`, `MCP`, and `controller`.
- `Hermes-Agent` names the external runtime substrate owner; repo-side grant adapters keep authoring truth, direct entry, and route contracts stable above that substrate.
- Historical program records and migration notes stay in `docs/specs/` and `docs/history/` for traceability.
- The frontdesk, user-loop, projections, and local `submission-ready` package are landed. Future hosted product expansion lives in `docs/plans/`.
- `OPL` owns family navigation and domain handoff; MAG owns grant-domain truth, direct grant entry, and execution routing.
- Current controller-owned, read-only projections continue to include `workspace progress`, `workspace cockpit`, `product direct-entry`, and `product user-loop`, with schema-backed boundaries above the author-side line.
- The current grouped public shell also exposes `product build-entry`, `product manifest`, `product frontdesk`, and `package submission-ready` as the public CLI-facing entry surface.
- The current lightweight grant `product entry` shell is the active product-entry shell and internal domain/API catalog builder. Future hosted product work stays in `docs/plans/`.

## Technical Working Set

Read these first before changing repo state:

- [Project](./project.md)
- [Status](./status.md)
- [Architecture](./architecture.md)
- [Invariants](./invariants.md)
- [Decisions](./decisions.md)
- [Contracts Overview](../contracts/README.md)
- [`current-program.json`](../contracts/runtime-program/current-program.json)

Machine-local runtime state stays under `$CODEX_HOME/projects/med-autogrant/runtime-state/`.

## Default Public Surface

- [Repository home](../README.md)
- [Domain Positioning](./domain-positioning.md)
- [MVP Scope](./mvp-scope.md)

These files are the default public-facing entry surfaces and should stay mirrored in English and Chinese where applicable.

## Technical Records

- [`current-program.json`](../contracts/runtime-program/current-program.json)
- [Specs directory](./specs/)
- [Contracts Overview](../contracts/README.md)

The current grant product-entry shell remains available as the domain/API catalog builder. The current schema-backed freeze also keeps `hosted contract bundle`, `domain_entry_contract`, `supported_commands`, and `command_contracts` visible for hosted caller / external caller consumption.

## Trace Records

- [References directory](./references/)
- [History archive](./history/README.md)

## Plans And Historical Planning Artifacts

- [Plans directory](./plans/)

Completed planning artifacts stay in `docs/plans/` for traceability until they are absorbed into longer-term history layers.
Current mainline truth continues to live in the core docs, `docs/specs/`, and [`current-program.json`](../contracts/runtime-program/current-program.json).

## Documentation Rules

- Keep [Repository home](../README.md) readable for grant applicants and non-technical experts.
- Keep the default public docs mirrored in English and Chinese where they are part of the public surface.
- Keep `docs/specs/` authoritative for technical records and activation packages without letting it replace the user-facing home page.
- Keep references, plans, and history available, while keeping the public home page as the default entry.

## Governance

- Documentation governance freezes in [series doc governance checklist](./references/series-doc-governance-checklist.md), the technical working set, and repo-tracked contract/doc surfaces rather than in `AGENTS.md` alone.
- `README*` and `docs/README*` are the default public entry.
- `docs/specs/**` holds technical records and activation packages.
- `docs/references/**` holds internal reference notes.
- `docs/plans/**` and `docs/history/**` are support material for future work and archival traceability.
