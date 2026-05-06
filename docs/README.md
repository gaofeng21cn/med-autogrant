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
| Developers and maintainers | [Specs guide](./specs/README.md), [References directory](./references/), [Active plans](./plans/README.md), [History archive](./history/README.md) | Inspect technical records, reference notes, future work, and archival material |

## Current Technical Picture

- `Med Auto Grant` is an independent medical grant domain agent whose first public surface is the single Med Auto Grant app skill. The stable callable surface underneath it is `CLI`, `MedAutoGrantDomainEntry`, local scripts, and schema-backed contracts.
- The formal-entry matrix remains `CLI`, `MCP`, and `controller`.
- Default authoring execution inherits local `Codex` defaults through the existing route-selected executor path.
- `OPL Runtime Manager` is the target OPL-side thin manager over the external `Hermes-Agent` substrate; it may consume MAG runtime_control, runtime_continuity, workspace projection, artifact locator, and explicit wakeup/TODO queues, but it does not own MAG grant truth or authoring execution.
- `Hermes-Agent`-related lanes stay in explicit hosted/proof or technical-reference positions; they do not redefine the default public capability contract.
- Historical program records and migration notes stay reachable through `docs/history/`; older dated specs remain in `docs/specs/` as provenance and are indexed from `docs/history/specs/`.
- The frontdesk, user-loop, projections, and local `submission-ready` package are landed as internal command contracts and direct-product projections under the app skill. The active task boundary now distinguishes scientific review readiness from the stricter local export gate, and that export gate does not imply external funding-portal submission. Future hosted product expansion belongs in `docs/plans/` only when there is an active plan.
- `OPL` family routing and `Codex` skill activation consume the same MAG capability surface; MAG keeps grant-domain truth, direct grant entry, and execution routing.
- The active MAG task boundary is specified-funder body authoring; scientific completion and formal/objective supplement completion are explicitly separated layers.
- The scientific completion layer delivers a review-ready package for author and reviewer decision flow.
- Formal/objective supplements default to `TODO + explicit wakeup`; they are not body-authoring blockers unless they directly invalidate scientific claims.
- Human gates are scoped to author decisions within the same funding-call task, not cross-funder reselection.
- Current controller-owned, read-only projections continue to include `workspace progress`, `workspace cockpit`, `product direct-entry`, and `product user-loop`, with schema-backed boundaries above the author-side line.
- The current grouped shell also exposes `product build-entry`, `product manifest`, `product frontdesk`, and `package submission-ready` as the skill-backed CLI command surface.
- The current lightweight grant `product entry` shell is the internal product-entry shell and domain/API catalog builder behind the app skill. Future hosted product work stays in `docs/plans/` only while it is active, then moves to history.
- Quality governance is now schema-backed through `workspace quality-scorecard` and `workspace quality-diff`.
- Long-horizon autonomy is now exposed as `pass autonomy-controller`, with structured blocker and evidence-gap reporting.
- Common grant grammar and funder-specific family profile rules remain separated in `grant_family_registry.py`, while cross-funder reselection stays outside default body-authoring gate semantics.

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
- [Specs guide](./specs/README.md)
- [AI-first quality boundary current truth](./specs/2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./specs/2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./specs/2026-04-22-quality-autonomy-family-grammar-current-truth.md)
- [Contracts Overview](../contracts/README.md)

The current grant product-entry shell remains available as the internal domain/API catalog builder behind the app skill and as part of the stable callable surface. The current schema-backed freeze also keeps `hosted contract bundle`, `domain_entry_contract`, `supported_commands`, and `command_contracts` visible as integration/reference surfaces for hosted caller / external caller consumption.
The quality and autonomy schemas are tracked in [`schema-index.json`](../schemas/v1/schema-index.json) and in the current-program truth surface.

## Trace Records

- [References directory](./references/)
- [History archive](./history/README.md)
- [Historical specs index](./history/specs/README.md)
- [Historical plans index](./history/plans/README.md)
- [Docs portfolio consolidation boundary](./docs_portfolio_consolidation.md)

## Structural Quality Verification

Sentrux is tracked as an advisory architecture signal. Maintainers should run
`sentrux gate .` before absorbing structural changes, and `sentrux check .`
when changing dependency direction, package/export builders, runtime adapters,
or product-entry internals. The CI workflow is intentionally advisory while the
current baseline is tightened through focused cleanup lanes. Merge decisions
must prioritize product semantics and repo-native verification: large
unexplained structural drops, cycle regressions, rule violations, or failing
tests should block absorption, while a small score movement is acceptable when
the dependency ownership becomes clearer.

The local `structure` lane and advisory workflow also write OPL quality details
sidecars under `artifacts/opl-quality-details/`: markdown output from
`/Users/gaofeng/workspace/one-person-lab/bin/opl quality details --root . --format markdown --limit 20`,
JSON output from the same command with `--format json`, and a complete
`.sentrux/rules.toml` sidecar. If Sentrux gate/check fails, these diagnostics
are generated and printed before the lane reports the Sentrux failure.

## Plans And Historical Planning Artifacts

- [Active plans](./plans/README.md)
- [Historical plans](./history/plans/README.md)

Completed planning artifacts now live in `docs/history/plans/`.
Current mainline truth continues to live in the core docs, active specs listed in `docs/specs/README.md`, and [`current-program.json`](../contracts/runtime-program/current-program.json).

## Documentation Rules

- Keep [Repository home](../README.md) readable for grant applicants and non-technical experts.
- Keep the default public docs mirrored in English and Chinese where they are part of the public surface.
- Keep active specs listed in `docs/specs/README.md` authoritative for their specific technical boundaries without letting them replace the user-facing home page.
- Keep references, plans, and history available, while keeping the public home page as the default entry.

## Governance

- Documentation governance freezes in [series doc governance checklist](./references/series-doc-governance-checklist.md), the technical working set, and repo-tracked contract/doc surfaces rather than in `AGENTS.md` alone.
- `README*` and `docs/README*` are the default public entry.
- `docs/specs/**` holds active technical records plus older provenance specs; `docs/history/specs/` is the archival reading index for older dated records.
- `docs/references/**` holds internal reference notes.
- `docs/plans/**` is reserved for active future work; `docs/history/**` holds completed plans and archival traceability.
