# Docs Portfolio Consolidation

Date: `2026-05-06`

This note freezes the documentation portfolio boundary after the May 2026 consolidation and the second-round content alignment pass.

## Active Layer

- `README*`
- `docs/README*`
- `docs/domain-positioning*`
- `docs/mvp-scope*`
- `docs/project.md`
- `docs/status.md`
- `docs/architecture.md`
- `docs/invariants.md`
- `docs/decisions.md`
- `contracts/runtime-program/current-program.json`

These files are the active reading path for public positioning, current technical truth, and maintainer context.

## Reference Layer

- `docs/references/**`
- `docs/specs/README*`
- active specs listed in `docs/specs/README*`
- repo-tracked truth surfaces listed by `contracts/runtime-program/current-program.json`

These files explain stable boundaries or current technical records without replacing the core docs.

## History Layer

- `docs/history/**`
- `docs/history/plans/**`
- `docs/history/specs/README*`
- `docs/history/domain-harness-os-positioning.md`
- older dated specs still stored under `docs/specs/*.md` for path stability but indexed as historical records

Historical files are provenance and audit material. They may preserve old task wording, old path references, and superseded tranche labels; they do not override the active layer.

The second-round review intentionally did not bulk-move older specs out of `docs/specs/`: many historical notes, rollout records, and current-program pointers still reference those original paths. The archive boundary is therefore enforced by the README/index layer rather than by rewriting every dated spec path.
