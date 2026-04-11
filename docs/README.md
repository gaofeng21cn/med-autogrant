# Docs

**English** | [中文](./README.zh-CN.md)

This bilingual index is the default public surface for `Med Auto Grant`.
It reflects the project truth that the repository is the medical `Grant Ops` `Domain Harness OS` direction on the shared `Unified Harness Engineering Substrate`. The local `R1 -> R5` runtime ladder is already absorbed through `R5.A / Hosted-Friendly Session Boundary`, while the product remains in `baseline freeze / runtime hardening`. Its formal-entry matrix is `CLI` as default formal entry, `MCP` as a reserved future protocol layer, and `controller` as internal control surface. The current repository mainline is `Auto-only`.

## Core Maintainer Working Set

Start here before reading detailed specs:

- [Project](./project.md)
- [Status](./status.md)
- [Architecture](./architecture.md)
- [Invariants](./invariants.md)
- [Decisions](./decisions.md)

## External Bilingual Surface

- [Repository home](../README.md)
- [Domain Positioning](./domain-positioning.md)
- [MVP Scope](./mvp-scope.md)

This index plus the repository home forms the default bilingual face shown on GitHub.

## Repo-Tracked Internal Design & Planning Docs

These documents are internal design references and default to Chinese.

- [Domain Harness OS Positioning](./domain-harness-os-positioning.md)
- [Top-Level Design](./specs/2026-04-06-med-auto-grant-top-level-design.md)
- [NSFC Main Flow And Critique Loop](./specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [Object Model Schema V1](./specs/2026-04-06-object-model-schema-v1.md)
- [Formal Entry Matrix Current Truth](./specs/2026-04-07-formal-entry-matrix-current-truth.md)
- [Durability Model Clarification](./specs/2026-04-07-durability-model-clarification.md)
- [Post-R5A local runtime hardening brief](./specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md) (next-line hardening brief, Chinese only)
- [Post-R5A revised-workspace validator and operator alignment](./specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md) (Chinese only)
- [Post-R5A local runtime walkthrough and output consistency current truth](./specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md) (Chinese only)
## Historical Planning Artifacts

- [Minimal Scaffold Plan](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [P1 Formal Entry And Durability Planning Brief](./plans/2026-04-07-p1-formal-entry-and-durability-planning-brief.md)
- [OMX historical archive](./history/omx/README.md)

## Reading Order

1. Start with the [Core Maintainer Working Set](#core-maintainer-working-set).
2. Continue with [Domain Positioning](./domain-positioning.md) and [MVP Scope](./mvp-scope.md).
3. For the absorbed current runtime truth, prioritize:
   - [Formal Entry Matrix Current Truth](./specs/2026-04-07-formal-entry-matrix-current-truth.md)
   - [Durability Model Clarification](./specs/2026-04-07-durability-model-clarification.md)
   - [Post-R5A revised-workspace validator and operator alignment](./specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md) (Chinese only)
   - [Post-R5A local runtime walkthrough and output consistency current truth](./specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md) (Chinese only)
4. For the next honest continuation line after `R5.A`, read [Post-R5A local runtime hardening brief](./specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md) (Chinese only).
5. Read the [OMX historical archive](./history/omx/README.md) only when you need OMX-era migration provenance.
6. Read other historical planning artifacts only when you need provenance.

For the current canonical local operator path, read the post-`R5.A` walkthrough truth first, then use the “Minimal Runtime Commands” section in the repository home README as its public command mirror.

## Status Note

`Med Auto Grant` is still under active development.
The local runtime ladder `R1 -> R5` is already absorbed through `R5.A`, and the current honest continuation is `post-R5A local runtime hardening`; the maturity level still remains in `baseline freeze / runtime hardening`, and the full grant authoring runtime is not yet complete.

## Documentation Boundary

- `README*` and `docs/README*`: default bilingual public surface.
- `docs/project.md`, `docs/status.md`, `docs/architecture.md`, `docs/invariants.md`, `docs/decisions.md`: AI / maintainer core working set.
- `docs/domain-harness-os-positioning.md`, `docs/specs/**`, and `docs/plans/**`: internal technical/design docs by default.
- `docs/history/omx/**`: historical OMX archive only, never an active workflow entry.
- Public docs must ship with synchronized English and Chinese mirrors.
- Internal technical, planning, and memo docs default to Chinese.
- Avoid unnecessary mixed-language prose; reserve English for fixed terms, file paths, commands, and code identifiers.
