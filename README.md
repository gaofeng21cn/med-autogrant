<p align="center">
  <a href="./README.md"><strong>English</strong></a> | <a href="./README.zh-CN.md">中文</a>
</p>

# Med Auto Grant

**The document-first scaffold for the future medical implementation of `Grant Foundry`**

`Med Auto Grant` is the first medical implementation scaffold under the `Grant Foundry` line.
It is being shaped as a future `Grant Ops` medical domain gateway and harness, with the first MVP focused on a medical `NSFC` generic application skeleton.

## Current Position

- current stage: repository scaffold, not a mature runtime
- domain role: future author-side, proposal-facing `Grant Ops` surface
- first MVP: medical `NSFC` generic grant-writing workflow
- relation to `Research Ops`: high asset reuse, but independent domain boundary

## Shared Operating Pattern

`Med Auto Grant` follows the same top-level doctrine frozen in `OPL`:

- `Agent-first` rather than `fixed-code-first`
- one shared base with two modes:
  - `Auto`
  - `Human-in-the-loop`

The goal is not just to fill sections of an application form.
The system centers on scientific-question refinement, argument-chain construction, mentor-style critique, and revision loops.

## Public Docs

- [Domain Positioning](./docs/domain-positioning.md)
- [MVP Scope](./docs/mvp-scope.md)

## Minimal Runtime

The repository now includes a minimal Python runtime scaffold for the frozen `NSFCWorkspace` contract.

Quickstart:

```bash
PYTHONPATH=src python3 -m med_autogrant validate-workspace --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant summarize-workspace --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant next-step --input examples/nsfc_workspace_minimal.json
PYTHONPATH=src python3 -m med_autogrant critique-summary --input examples/nsfc_workspace_minimal.json
```

Current CLI scope:

- validate the frozen `NSFCWorkspace` schema subset plus key runtime constraints
- summarize the active direction/question/draft/revision state
- route the next recommended stage from `lifecycle_stage`, `gates`, and critique verdict
- export a structured mentor-critique summary around the `60/30/10` frame

## Internal Docs

The repository keeps internal planning and design notes in Chinese only.
See:

- [`docs/specs/2026-04-06-med-auto-grant-top-level-design.md`](./docs/specs/2026-04-06-med-auto-grant-top-level-design.md)
- [`docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md`](./docs/specs/2026-04-06-nsfc-main-flow-and-critique-loop.md)
- [`docs/specs/2026-04-06-object-model-schema-v1.md`](./docs/specs/2026-04-06-object-model-schema-v1.md)
- [`docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md`](./docs/specs/2026-04-06-med-autogrant-mainline-and-omx-bridge.md)
- [`docs/plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md`](./docs/plans/2026-04-06-med-autogrant-minimal-scaffold-plan.md)

The repository also now carries repo-managed internal `Codex App <-> OMX` control surfaces under `.omx/context`, `.omx/plans`, and `.omx/reports`.
