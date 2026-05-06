# Specs Guide

This directory keeps the current technical record layer for `Med Auto Grant`.

The highest-priority active current-truth specs are the small set still referenced directly from the docs guide or current status:

- [AI-first quality boundary current truth](./2026-04-27-ai-first-quality-boundary-current-truth.md)
- [Authoring completion semantics current truth](./2026-04-23-authoring-completion-semantics-current-truth.md)
- [Quality governance, autonomy controller, and family grammar current truth](./2026-04-22-quality-autonomy-family-grammar-current-truth.md)

`contracts/runtime-program/current-program.json` remains the canonical pointer for the full repo-tracked truth-surface list. Some listed route, hosted-caller, product-entry, and Hermes reset specs still live here because current-program or historical audit paths point to them directly.

Older dated `P*`, `R*`, `post-R5A`, activation-package, migration-board, and superseded tranche current-truth files are historical technical records. They remain here as repo-tracked provenance to avoid rewriting old audit paths, but their reading entry is now:

- [Historical specs index](../history/specs/README.md)

Current product truth is not derived by choosing the newest spec by filename alone. Read the core docs and `current-program.json` first, then use active specs for the specific boundary they freeze. Historical files can preserve old task wording, old paths, and superseded tranche labels.
