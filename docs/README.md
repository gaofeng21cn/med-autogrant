# Docs

**English** | [中文](./README.zh-CN.md)

This index is the default documentation surface for `Med Auto Grant`.
Start with the core skeleton, then use specs/plans/history for deeper provenance.
The current public runtime topology is `CLI-first + Hermes-backed runtime`; `MCP` remains the supported protocol layer and `controller` remains the internal surface.

## Start Here: Core Docs

- [Project](./project.md)
- [Status](./status.md)
- [Architecture](./architecture.md)
- [Invariants](./invariants.md)
- [Decisions](./decisions.md)

## Document Roles

- `README*` and `docs/README*`: public entry points and indexes.
- Public docs must ship with synchronized English and Chinese mirrors.
- Core skeleton (`docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`): canonical overview and working constraints.
- `docs/specs/**`: repo-tracked current truth, activation packages, and design freezes.
- `docs/plans/**`: historical planning artifacts only.
- `docs/history/**`: archival material (including OMX).

## Public Bilingual Surface

- [Repository home](../README.md)
- [Domain Positioning](./domain-positioning.md)
- [MVP Scope](./mvp-scope.md)

## Specs (Current Truth / Activation Packages)

- [Hermes-backed runtime substrate program current truth](./specs/2026-04-11-hermes-backed-runtime-substrate-program-current-truth.md)
- [Hermes-backed runtime capability migration map current truth](./specs/2026-04-11-hermes-backed-runtime-capability-migration-map-current-truth.md)
- [Formal Entry Matrix Current Truth](./specs/2026-04-07-formal-entry-matrix-current-truth.md)
- [Durability Model Clarification](./specs/2026-04-07-durability-model-clarification.md)
- [Post-R5A local runtime hardening brief](./specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md) (Chinese only)
- [Post-R5A revised-workspace validator and operator alignment](./specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md)
- [Post-R5A local runtime walkthrough and output consistency current truth](./specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md)
- [Post-R5A local runtime upper-bound honest stop current truth](./specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md)

Specs are repo-tracked and authoritative for activation packages and current truth, but they do not replace the core skeleton.

## Current Baseline, Long-Line Target, And Task Ladder

- Current repo-verified migration baseline: the absorbed `CLI-first + host-agent runtime` line now closes at the `R5.A` honest upper bound and is retained only as a migration baseline / compatibility bridge / regression oracle.
- Current product runtime mainline: `CLI-first + Hermes-backed runtime`.
- Active task ladder: continue the `Hermes Runtime Substrate Program` under `H1 / Hermes-Owned Runtime Path`, while keeping object boundaries and authoring semantics stable.
- Historical bridge / OMX materials remain traceability aids only and must not be treated as current entrypoints.

## Plans & History

- [Minimal Scaffold Plan](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [P1 Formal Entry And Durability Planning Brief](./plans/2026-04-07-p1-formal-entry-and-durability-planning-brief.md)
- [OMX historical archive](./history/omx/README.md)
