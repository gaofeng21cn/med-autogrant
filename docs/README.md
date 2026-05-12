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
| Developers and maintainers | [Specs guide](./specs/README.md), [Specs lifecycle map](./specs/specs_lifecycle_map.md), [References directory](./references/), [Active plans](./plans/README.md), [History archive](./history/README.md) | Inspect technical records, reference notes, future work, and archival material |

## Current Technical Picture

- `Med Auto Grant` is an independent medical grant domain agent whose first public surface is the single Med Auto Grant app skill. The stable callable surface underneath it is `CLI`, `MedAutoGrantDomainEntry`, local scripts, and schema-backed contracts.
- The formal-entry matrix remains `CLI`, `MCP`, and `controller`.
- OPL is the stage-led runtime framework with Agent executors as the minimum execution unit. It may host MAG as an external domain dependency, and `Codex CLI` is the minimum execution unit for stage attempts unless an active contract explicitly selects another provider.
- OPL may consume MAG runtime_control, runtime_continuity, workspace projection, artifact locator, and explicit wakeup/TODO queues for scheduling, wakeup, handoff, receipt, retry, and projection. It does not own MAG grant truth, authoring execution, fundability judgment, quality verdicts, or submission-ready export authority.
- Older `OPL Runtime Manager`, Temporal, Hermes-first, gateway, and local-host runtime notes remain as provenance or provider-specific implementation records, not the default MAG/OPL boundary.
- `Hermes-Agent`-related lanes stay in explicit hosted/proof or technical-reference positions; the default public capability contract remains the MAG direct grant-authoring surface plus OPL stage-led framework consumption.
- [Docs portfolio consolidation boundary](./docs_portfolio_consolidation.md) is the current docs lifecycle owner. It records partition owners, absorbed content, and why old OPL Runtime Manager / lightweight handoff notes now live in history.
- Historical program records and migration notes stay reachable through `docs/history/`; older dated specs can remain in `docs/specs/` for provenance, while machine-readable surfaces refer to them through semantic `human_doc:*` ids rather than path-stability constraints.
- The product status, user-loop, projections, and local `submission-ready` package are landed as internal command contracts and direct-product projections under the app skill. The active task boundary now distinguishes scientific review readiness from the stricter local export gate; external funding-portal submission remains a separate supervised step. Future hosted product expansion belongs in `docs/plans/` only when there is an active plan.
- `OPL` family routing and `Codex` skill activation consume the same MAG capability surface; MAG keeps grant-domain truth, direct grant entry, and execution routing.
- The active MAG task boundary is specified-funder body authoring; scientific completion and formal/objective supplement completion are explicitly separated layers.
- The scientific completion layer delivers a review-ready package for author and reviewer decision flow.
- Formal/objective supplements default to `TODO + explicit wakeup`; they become body-authoring blockers only when they directly invalidate scientific claims.
- Human gates are scoped to author decisions within the same funding-call task; cross-funder reselection requires a separate task.
- Current controller-owned, read-only projections continue to include `workspace progress`, `workspace cockpit`, `product direct-entry`, and `product user-loop`, with schema-backed boundaries above the author-side line.
- MAG now exposes controlled grant-stage domain memory apply proof through `controlled_domain_memory_apply_proof`: consumed grant strategy memory refs, writeback proposal, MAG accept/reject decision, operator receipt projection, and repo-source layout audit are verifiable without storing memory body, grant artifacts, or receipt instances in repo source.
- The current grouped shell also exposes `product build-entry`, `product manifest`, `product status`, and `package submission-ready` as the skill-backed CLI command surface.
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
- [Specs lifecycle map](./specs/specs_lifecycle_map.md)

Machine-local runtime state stays under `$CODEX_HOME/projects/med-autogrant/runtime-state/`.

## Default Public Surface

- [Repository home](../README.md)
- [Domain Positioning](./domain-positioning.md)
- [MVP Scope](./mvp-scope.md)

These files are the default public-facing entry surfaces and should stay mirrored in English and Chinese where applicable.
The root public-doc allowlist is intentionally sparse:

- `README*` is the public first page.
- `docs/domain-positioning*` remains current for MAG owner, public subject, and OPL/provider boundary.
- `docs/mvp-scope*` remains current for the NSFC MVP scope and non-goals.

## Technical Records

- [`current-program.json`](../contracts/runtime-program/current-program.json)
- [Specs guide](./specs/README.md)
- [Specs lifecycle map](./specs/specs_lifecycle_map.md)
- [AI-first quality boundary current truth](./specs/2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./specs/2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./specs/2026-04-22-quality-autonomy-family-grammar-current-truth.md)
- [Contracts Overview](../contracts/README.md)
- [Grant Strategy Memory Policy](./references/grant_strategy_memory_policy.md)

The current grant product-entry shell remains available as the internal domain/API catalog builder behind the app skill and as part of the stable callable surface. The current schema-backed freeze also keeps `hosted contract bundle`, `domain_entry_contract`, `supported_commands`, and `command_contracts` visible as integration/reference surfaces for hosted caller / external caller consumption.
Fundability, specific aims, reviewer grammar, and template strategy experience is managed as natural-language memory. `domain_memory_descriptor_locator` and `controlled_domain_memory_apply_proof` project writeback proposal / accept-reject / receipt refs and repo-source layout audit only; they do not write real memory entries or grant artifacts into repo source. `workspace quality-scorecard`, `grant-quality-closure-dossier`, autonomy-controller reports, and submission-ready packages remain structured authority.
The quality and autonomy schemas are tracked in [`schema-index.json`](../schemas/v1/schema-index.json) and in the current-program truth surface.
For the complete repo-tracked truth-surface list, read `repo_tracked_truth_surfaces` in [`current-program.json`](../contracts/runtime-program/current-program.json); contract/schema/source surfaces stay as repo paths, and prose docs are referenced by semantic `human_doc:*` ids. The specs guide and specs lifecycle map separate active boundary records, support records, and historical provenance records.

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

The default local verification entry is `./scripts/verify.sh`. It runs the
line-budget check once, then the small `smoke` lane and the fast non-regression
core lane without optional proof dependencies. Heavier matrix, runtime/session,
hosted/export, product-entry, and provenance-oracle regression coverage belongs to
`./scripts/verify.sh regression`; explicit Hermes hosted/proof checks belong to
`./scripts/verify.sh proof` and use the `proof` extra. The
product-entry case modules under `tests/product_entry_cases/` are directly
collected there; the old `tests/test_product_entry.py` aggregation surface has
been removed. Full-suite baselines remain available through
`./scripts/verify.sh full`.

Repository hygiene is enforced in the meta verification surface through
`tests/test_repository_hygiene.py`. The repo-tracked mainline must not contain
generated or local-state payloads such as `dist/`, `build/`, `out/`,
`__pycache__`, `*.egg-info`, `.DS_Store`, `.codex/`, `.omx/`,
`.runtime-program/`, `runtime-state/`, or `.agent-contract-baseline.json`.
The only tracked `.agents/` entrypoint is `.agents/plugins/marketplace.json`.
The same test also keeps tracked source and test files within the current line
budget unless a legacy baseline is explicitly recorded.

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
- Treat `README*` and `docs/**` as human-readable surfaces. Do not make scripts, tests, runtime status, or contracts depend on their concrete paths; use schema/source paths or semantic `human_doc:*` ids where machine surfaces need a doc relationship.
- Each doc lane carries lifecycle signals: `owner`, `purpose`, `state`, and `machine boundary`.
- Use `state=current` only for the public entry, core docs, active specs, and current contract pointers. Use `state=reference` for stable explanatory material and `state=history` for provenance.

## Governance

- Documentation governance freezes in [series doc governance checklist](./references/series-doc-governance-checklist.md), the technical working set, and repo-tracked contract/doc surfaces rather than in `AGENTS.md` alone.
- `README*` and `docs/README*` are the default public entry.
- `docs/specs/**` holds active technical records plus older provenance specs; `docs/history/specs/` is the archival reading index for older dated records.
- `docs/references/**` holds internal reference notes.
- `docs/plans/**` is reserved for active future work; `docs/history/**` holds completed plans and archival traceability.
