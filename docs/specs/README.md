# Specs Guide

This directory keeps the current technical record layer for `Med Auto Grant`.

Lifecycle:

- `owner`: MAG maintainers and the owning runtime/product-governance lane for each active spec.
- `purpose`: index active current-truth records and route older dated records to historical reading.
- `state`: `current` for active specs listed below; `history` for older dated specs retained here for path provenance.
- `machine boundary`: specs are human-readable current-truth records. Machine consumers should use `contracts/runtime-program/current-program.json`, schema files, source files, or semantic `human_doc:*` ids rather than depending on prose paths.

The highest-priority active current-truth specs are the small set still referenced directly from the docs guide or current status:

- [Critique executor vocabulary current truth](./2026-04-13-critique-codex-cli-executor-current-truth.md)
- [AI-first quality boundary current truth](./2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./2026-04-22-quality-autonomy-family-grammar-current-truth.md)

The dense specs portfolio is classified in [Specs Lifecycle Map](./specs_lifecycle_map.md). Use that map to distinguish active records, support current-truth records, and historical provenance before editing or moving any dated spec.

Every dated support/history spec that remains in this directory now carries a first-screen lifecycle note. That note is intentionally stronger than the old `Current Truth` filenames: open a single spec only after checking whether it is active, support-only, or historical in this guide and the lifecycle map.

`contracts/runtime-program/current-program.json` remains the canonical pointer for the full repo-tracked truth-surface list. Some listed route, executor-vocabulary, hosted-caller, product-entry, and Hermes reset specs still live here because current-program or historical audit paths point to them directly.

Current OPL wording is centralized in the core docs: OPL is a stage-led runtime framework with Agent executors as the minimum execution unit that may consume MAG-owned descriptors and projections. Older specs that say `OPL Runtime Manager`, Temporal target, Hermes-first, active adapter, gateway, or monorepo should be read as provider-specific migration context unless the current owner docs explicitly promote that wording.

The `hosted contract bundle` remains an integration/reference export surface. Hosted runtime, Web UI, public MCP runtime, external portal submission, and mature gateway/federation each require their own current owner evidence.

Older dated `P*`, `R*`, `post-R5A`, activation-package, migration-board, and superseded tranche current-truth files are historical technical records. They remain here as repo-tracked provenance to avoid rewriting old audit paths, but their reading entry is now:

- [Historical specs index](../history/specs/README.md)

Current product truth is not derived by choosing the newest spec by filename alone. Read the core docs and `current-program.json` first, then use active specs for the specific boundary they freeze. Historical files can preserve old task wording, old paths, and superseded tranche labels.
