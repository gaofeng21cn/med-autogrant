# Docs

**English** | [中文](./README.zh-CN.md)

This index is the default documentation surface for `Med Auto Grant`.
Start with the core skeleton, then use specs/plans/history for deeper provenance.
The current public runtime topology is: `CLI-first + real upstream Hermes-Agent runtime substrate`. `MCP` remains the supported protocol layer and `controller` remains the internal surface.
Repo-tracked current-program truth lives at `contracts/runtime-program/current-program.json`, while machine-local runtime state lives under `$CODEX_HOME/projects/med-autogrant/runtime-state/`.
The current entry truth is also explicit: `operator entry` and `agent entry` are real today, and the lightweight grant `product entry` shell is now landed. `product-entry-manifest` is now the machine-readable discovery surface for that shell, `product-frontdesk` now freezes the controller-owned direct front door above it, and the shared envelope plus routing surfaces are frozen as schema-backed contract surfaces. The first honest `P4.A` direct-product projection is now also landed through `grant-progress` and `grant-cockpit`, the next honest `P4.B` direct-entry composition is now landed through `grant-direct-entry`, the current `P4.C` companion layer is now landed through `mainline-status`, `mainline-phase`, and `grant-user-loop`, `P4.D` now lands the full authoring executor ladder from `direction_screening` to `frozen`, `P4.E` now lands independently schema-backed `product-entry-manifest` / `product-frontdesk` frontdoor contracts, and `P4.F` now lands fail-closed local `submission-ready` package export through `build-submission-ready-package`; all of these product-facing and route-facing surfaces are repo-tracked and fail-closed, while a richer grant-facing product experience still remains future work.
The hosted-friendly contract bundle now also ships a machine-readable catalog through `domain_entry_contract`, `schema_contract`, and `authoring_contract`, so future hosted / `OPL` callers can consume the same frozen entry, schema, and route truth.
That shared `domain_entry_contract` now also exposes `supported_commands` and `command_contracts`, and the hosted caller consumption proof is now landed.

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
- [Schema-backed product entry and routing contract current truth](./specs/2026-04-12-schema-backed-product-entry-and-routing-contract-current-truth.md) (Chinese only)
- [Hosted contract bundle entry and route catalog current truth](./specs/2026-04-12-hosted-contract-bundle-entry-and-route-catalog-current-truth.md) (Chinese only)
- [Hosted caller consumption proof current truth](./specs/2026-04-12-hosted-caller-consumption-proof-current-truth.md) (Chinese only)
- [OPL-aligned ideal target and phase map current truth](./specs/2026-04-12-opl-aligned-ideal-target-and-phase-map-current-truth.md) (Chinese only)
- [Lightweight product entry and OPL handoff current truth](./specs/2026-04-12-lightweight-product-entry-and-opl-handoff-current-truth.md) (Chinese only)
- [P4.A direct grant cockpit and progress projection current truth](./specs/2026-04-12-p4a-direct-grant-cockpit-and-progress-projection-current-truth.md) (Chinese only)
- [P4.B direct grant entry composition current truth](./specs/2026-04-12-p4b-direct-grant-entry-composition-current-truth.md) (Chinese only)
- [P4.C mainline status and grant user loop current truth](./specs/2026-04-12-p4c-mainline-status-and-grant-user-loop-current-truth.md) (Chinese only)
- [Full grant authoring executor current truth](./specs/2026-04-13-full-grant-authoring-executor-current-truth.md) (Chinese only)
- [P4.E schema-backed frontdesk and manifest current truth](./specs/2026-04-13-p4e-schema-backed-frontdesk-and-manifest-current-truth.md) (Chinese only)
- [P4.F local submission-ready package current truth](./specs/2026-04-13-p4f-local-submission-ready-package-current-truth.md) (Chinese only)
- [Pending authoring route handoff matrix current truth](./specs/2026-04-12-pending-authoring-route-handoff-matrix-current-truth.md) (Chinese only)
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
- Product-entry shell: the lightweight grant `product entry` shell is now landed through `build-product-entry`, reusable both directly and through `OPL` handoff.
- Product-entry discovery surface: `product-entry-manifest` now freezes the current grant shell, shared handoff templates, and current mainline snapshot into one machine-readable manifest for direct callers and `OPL`, and it is now fail-closed by `product-entry-manifest.schema.json`.
- Product frontdesk surface: `product-frontdesk` now freezes the controller-owned direct front door above the grant shell into one machine-readable frontdesk contract, including the family-level `product_entry_readiness` companion plus the domain-deep `grant_authoring_readiness` companion, and it is now fail-closed by `product-frontdesk.schema.json`.
- Local submission-ready delivery surface: `build-submission-ready-package` now fail-closes on incomplete frozen workspaces and exports a local `submission_ready_package` only when mandatory sections, evidence, outputs, projects, and freeze gates all line up.
- Direct-product projection: `grant-progress` and `grant-cockpit` are now landed as controller-owned, read-only product projections. They consume existing route/audit truth and `build-product-entry` contract hints, are frozen by `grant-progress.schema.json` and `grant-cockpit.schema.json`, and are intentionally not new `domain_entry_contract` executor commands or hosted bundle command catalog entries.
- Direct-entry composition: `grant-direct-entry` now packages `grant-progress`, `grant-cockpit`, and both `build-product-entry` modes into one controller-owned direct-entry contract. It is frozen by `grant-direct-entry.schema.json` and still remains outside the service-safe domain command catalog.
- Current user loop: `mainline-status`, `mainline-phase`, and `grant-user-loop` now expose the repo mainline snapshot, current direct-entry composition, and route-derived next action as the current inbox-like shell. `grant-user-loop` is frozen by `grant-user-loop.schema.json` and still remains outside the service-safe domain command catalog.
- Schema-backed contract closeout: the landed `product entry` shell, `product-entry-manifest`, `product-frontdesk`, `executor_routing_contract`, the full authoring command surface, `grant-progress`, `grant-cockpit`, `grant-direct-entry`, `grant-user-loop`, and service-safe route surfaces are now indexed under `schemas/v1/` and validated fail-closed at generation time.
- Hosted contract bundle closeout: `build-hosted-contract-bundle` now exports `domain_entry_contract`, `schema_contract`, and `authoring_contract` alongside the existing runtime/state/operator surfaces, and the whole bundle is validated through `hosted-contract-bundle.schema.json`.
- Hosted caller proof closeout: external caller consumption is now repo-verified through the shared `domain_entry_contract`, including `supported_commands` and `command_contracts`, without repo-local helper code.
- Fastest cutover board: [Upstream Hermes-Agent fast cutover board](./specs/2026-04-12-upstream-hermes-agent-fast-cutover-board.md) (Chinese only)
- Active task ladder: keep the landed Hermes substrate, service-safe domain entry, hosted caller proof, and author-side object boundaries green while the old host-agent line remains only as a regression oracle.
- Historical bridge / OMX materials remain traceability aids only and must not be treated as current entrypoints.

## Plans & History

- [Minimal Scaffold Plan](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [P1 Formal Entry And Durability Planning Brief](./plans/2026-04-07-p1-formal-entry-and-durability-planning-brief.md)
- [OPL-aligned target shape and hosted caller plan](./plans/2026-04-12-opl-aligned-target-shape-and-hosted-caller-plan.md)
- [Lightweight product entry and OPL handoff](./references/lightweight_product_entry_and_opl_handoff.md) (Chinese only)
- [OMX historical archive](./history/omx/README.md)
