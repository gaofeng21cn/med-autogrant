# Docs Guide

**English** | [中文](./README.zh-CN.md)

This directory is the technical reading layer for `Med Auto Grant`. The repository home remains the user-facing entry for applicants, domain experts, and non-technical readers. This page is for readers who need the current technical truth, active support material, historical traceability, and documentation lifecycle map.

## Current Mainline

- `Med Auto Grant` is an independent medical grant domain agent whose first public surface is the single `Med Auto Grant` app skill.
- The stable capability surface is built from `CLI`, `MCP`, `controller`, `MedAutoGrantDomainEntry`, local scripts, and schema-backed contracts.
- `OPL` is the Codex-first, stage-led agent runtime framework that may host MAG stage attempts. `Codex CLI` is the default smallest execution unit inside a stage.
- MAG owns grant truth, authoring execution, fundability / quality verdicts, route ownership, and submission-ready export authority. OPL consumes MAG projections, wakeups, receipts, and artifact locators for scheduling, handoff, retry, and projection.
- The current task boundary is specified-funder body authoring. Scientific completion, formal/objective supplement completion, local export gates, and external funding-portal submission are separate states.
- The current repo-tracked truth surface entry is [`contracts/runtime-program/current-program.json`](../contracts/runtime-program/current-program.json).

## Start Here By Audience

| Audience | Start here | Why |
| --- | --- | --- |
| Potential users and domain experts | [Repository home](../README.md), [Domain Positioning](./domain-positioning.md), [MVP Scope](./mvp-scope.md) | Understand what the grant line does. |
| Technical readers and planners | [Project](./project.md), [Status](./status.md), [Architecture](./architecture.md), [Invariants](./invariants.md), [Decisions](./decisions.md), [Contracts Overview](../contracts/README.md) | Read the current boundary, execution model, and owner split. |
| Developers and maintainers | [Docs portfolio consolidation](./docs_portfolio_consolidation.md), [Specs guide](./specs/README.md), [Specs lifecycle map](./specs/specs_lifecycle_map.md), [References](./references/), [Active plans](./plans/README.md), [History archive](./history/README.md) | Separate current truth, support references, active future work, and history. |

## Current Technical Truth

| Layer | Entry | Meaning |
| --- | --- | --- |
| Core truth | [Project](./project.md), [Status](./status.md), [Architecture](./architecture.md), [Invariants](./invariants.md), [Decisions](./decisions.md) | Product role, runtime boundary, constraints, and durable decisions. |
| Machine truth | [`current-program.json`](../contracts/runtime-program/current-program.json), [schema index](../schemas/v1/schema-index.json), [Contracts Overview](../contracts/README.md) | Repo-tracked truth surfaces, schemas, source paths, and executable contracts. |
| Active specs | [Specs guide](./specs/README.md), [Specs lifecycle map](./specs/specs_lifecycle_map.md) | The small set of specs that still carry current technical boundaries. |
| Active future work | [Active plans](./plans/README.md) | Currently empty; future hosted/product expansion belongs here only while active, then moves to history. |

## Active Support And References

- `docs/references/`: strategy memory, cross-repo handoff, maintainer governance, and other support references.
- `docs/specs/`: active specs plus older dated specs retained for path provenance; use the README and lifecycle map to separate current, support, and history.
- `docs/plans/`: active plans not yet absorbed by core docs, contracts, or history.
- `$CODEX_HOME/projects/med-autogrant/runtime-state/`: machine-local runtime state.

## History And Traceability

- [History archive](./history/README.md)
- [Historical specs index](./history/specs/README.md)
- [Historical plans index](./history/plans/README.md)
- Older `OPL Runtime Manager`, Temporal, Hermes-first, gateway, monorepo, active-adapter, and local-host runtime material is current only when promoted by the active layer or a machine-readable contract. Otherwise it is provider-specific or historical provenance.

## Verification And Governance

- Default local verification entry: `./scripts/verify.sh`.
- `./scripts/verify.sh regression`: heavier matrix, runtime/session, hosted/export, product-entry, and compatibility coverage.
- `./scripts/verify.sh proof`: explicit Hermes hosted/proof checks with the `proof` extra.
- Structural quality and repo hygiene live in Sentrux advisory, `tests/test_repository_hygiene.py`, and repo-native verify lanes. Narrative docs-only changes use human review, `git diff --check`, and targeted link spot-checks.

## Documentation Rules

- Govern docs by content lifecycle; use filename, date, and path as secondary signals.
- Entry docs should show current state, hierarchy, old/new relationship, and the next reading step first. Historical specs, old hosted/provider notes, completed plans, and trace records are provenance.
- `README*` and `docs/**` are human-readable surfaces. Scripts, tests, runtime status, and contracts use schema/source paths, contract paths, or semantic `human_doc:*` IDs for doc relationships.
- Every docs lane should make `owner`, `purpose`, `state`, and `machine boundary` clear.
