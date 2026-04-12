# Docs

**English** | [中文](./README.zh-CN.md)

This index is the default documentation surface for `Med Auto Grant`.
Start with the core skeleton, then use specs/plans/history for deeper provenance.
The current public runtime topology is: `CLI-first + real upstream Hermes-Agent runtime substrate`. `MCP` remains the supported protocol layer and `controller` remains the internal surface.
Repo-tracked current-program truth lives at `contracts/runtime-program/current-program.json`, while machine-local runtime state lives under `$CODEX_HOME/projects/med-autogrant/runtime-state/`.
The current entry truth is also explicit: `operator entry` and `agent entry` are real today, while a mature grant-facing `product entry` is still the next product-layer gap.

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
- `docs/references/**`: repo-tracked internal reference notes, Chinese by default.
- `docs/plans/**`: historical planning artifacts only.
- `docs/history/**`: archival material (including OMX).

## Public Bilingual Surface

- [Repository home](../README.md)
- [Domain Positioning](./domain-positioning.md)
- [MVP Scope](./mvp-scope.md)

## Specs (Current Truth / Activation Packages)

- [Upstream Hermes-Agent fast cutover current truth](./specs/2026-04-12-upstream-hermes-agent-fast-cutover-current-truth.md) (Chinese only)
- [Upstream Hermes-Agent truth reset current truth](./specs/2026-04-11-upstream-hermes-agent-truth-reset-current-truth.md)
- [Upstream Hermes-Agent fast cutover board](./specs/2026-04-12-upstream-hermes-agent-fast-cutover-board.md) (Chinese only)
- [Formal Entry Matrix Current Truth](./specs/2026-04-07-formal-entry-matrix-current-truth.md)
- [Durability Model Clarification](./specs/2026-04-07-durability-model-clarification.md)
- [Post-R5A local runtime hardening brief](./specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md) (Chinese only)
- [Post-R5A revised-workspace validator and operator alignment](./specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md)
- [Post-R5A local runtime walkthrough and output consistency current truth](./specs/2026-04-10-post-r5a-local-runtime-walkthrough-and-output-consistency-current-truth.md)
- [Post-R5A local runtime upper-bound honest stop current truth](./specs/2026-04-11-post-r5a-local-runtime-upper-bound-honest-stop-current-truth.md)

Specs are repo-tracked and authoritative for activation packages and current truth, but they do not replace the core skeleton.

## Current Baseline, Long-Line Target, And Task Ladder

- Current repo-verified migration baseline: the absorbed `CLI-first + host-agent runtime` line now closes at the `R5.A` honest upper bound and is retained only as a migration baseline / compatibility bridge / regression oracle.
- Current executable runtime mainline: `CLI-first` runtime on real upstream Hermes substrate, with repo-side domain/entry adapters preserving Med Auto Grant semantics.
- Product-entry target: build a lightweight grant `product entry` on top of the landed runtime substrate, reusable both directly and through `OPL` handoff.
- Fastest cutover board: [Upstream Hermes-Agent fast cutover board](./specs/2026-04-12-upstream-hermes-agent-fast-cutover-board.md) (Chinese only)
- Active task ladder: keep the landed Hermes substrate, service-safe domain entry, and author-side object boundaries green while the old host-agent line remains only as a regression oracle.
- Historical bridge / OMX materials remain traceability aids only and must not be treated as current entrypoints.

## Plans & History

- [Minimal Scaffold Plan](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [P1 Formal Entry And Durability Planning Brief](./plans/2026-04-07-p1-formal-entry-and-durability-planning-brief.md)
- [Lightweight product entry and OPL handoff](./references/lightweight_product_entry_and_opl_handoff.md) (Chinese only)
- [OMX historical archive](./history/omx/README.md)
