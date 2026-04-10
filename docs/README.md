# Docs

**English** | [中文](./README.zh-CN.md)

This bilingual index is the default public surface for `Med Auto Grant`.
It reflects the project truth that the repository is the medical `Grant Ops` `Domain Harness OS` direction on the shared `Unified Harness Engineering Substrate`, currently in `baseline freeze / runtime hardening`. Its formal-entry matrix is `CLI` as default formal entry, `MCP` as a reserved future protocol layer, and `controller` as internal control surface. The current repository mainline is `Auto-only`.

## Unified Documentation Governance

- External documents must ship as paired English `.md` and Chinese `.zh-CN.md` files that stay synchronized.
- Internal design, planning, and memo documents default to Chinese unless they are explicitly promoted into the bilingual surface.
- Terminology may remain English when it represents stable domain language, but avoid unnecessary mixed-language prose.
- `docs/README*` should keep one consistent structure so readers can quickly distinguish public bilingual surfaces from internal reference material.
- For more detail, see [Documentation Governance](documentation-governance.md) (Chinese only).

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
- [Mainline And OMX Bridge](./specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md)
- [Formal Entry Matrix Current Truth](./specs/2026-04-07-formal-entry-matrix-current-truth.md)
- [Durability Model Clarification](./specs/2026-04-07-durability-model-clarification.md)
- [Post-R5A local runtime hardening brief](./specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md) (Chinese only)
- [Post-R5A revised-workspace validator and operator alignment](./specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md) (Chinese only)
- [Documentation Governance](documentation-governance.md) (Chinese only)

## Historical Planning Artifacts

- [Minimal Scaffold Plan](./plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)
- [P1 Formal Entry And Durability Planning Brief](./plans/2026-04-07-p1-formal-entry-and-durability-planning-brief.md)

## Reading Order

1. Start with [Domain Positioning](./domain-positioning.md).
2. Continue with [MVP Scope](./mvp-scope.md).
3. For current internal operating truth, prioritize:
   - [Mainline And OMX Bridge](./specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md)
   - [Formal Entry Matrix Current Truth](./specs/2026-04-07-formal-entry-matrix-current-truth.md)
   - [Durability Model Clarification](./specs/2026-04-07-durability-model-clarification.md)
   - [Post-R5A local runtime hardening brief](./specs/2026-04-09-post-r5a-local-runtime-hardening-brief.md) (Chinese only)
   - [Post-R5A revised-workspace validator and operator alignment](./specs/2026-04-10-post-r5a-revised-workspace-validator-and-operator-alignment.md) (Chinese only)
4. Read historical planning artifacts only when you need provenance.

For the current canonical local operator path, use the “Minimal Runtime Commands” section in the repository home README.

## Status Note

`Med Auto Grant` is still under active development with a minimal runtime baseline.
The maturity level remains in `baseline freeze / runtime hardening`, and the full grant authoring runtime is not yet complete.

## Documentation Boundary

- `README*` and `docs/README*`: default bilingual public surface.
- `docs/domain-harness-os-positioning.md`, `docs/specs/**`, and `docs/plans/**`: internal technical/design docs by default.
- Public docs must ship with synchronized English and Chinese mirrors.
- Internal technical, planning, and memo docs default to Chinese.
- Avoid unnecessary mixed-language prose; reserve English for fixed terms, file paths, commands, and code identifiers.
