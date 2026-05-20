# Package Authority Knowledge

## Purpose

This knowledge boundary defines the MAG package authority surface for local submission-ready export.

## Scope

- MAG package authority covers local package materialization, grant-owned package refs, required blocker shapes, manual portal boundary, and owner receipt requirements.
- OPL artifact lifecycle shells can carry refs and receipts only.
- External funding portal submission remains human-supervised and outside MAG automated completion claims.

## Readiness Layers

- Scientific review-ready means the proposal passed authoring quality review for the locked call.
- Local submission-ready means required package files, attachments, provenance, export constraints, and manual portal boundary are satisfied.
- External submitted means human portal action has happened and is proven by a separate human-supervised receipt.

## Package Gate Requirements

- Quality verdict or review gate receipt exists.
- Required sections, attachments, budget/support material, and portal-facing files are present by ref.
- Package refs trace to accepted draft/source/owner receipt evidence.
- Manual portal actions are listed explicitly and not silently claimed complete.

## Forbidden Uses

- Do not declare export-ready from package existence, command success, lifecycle completion, provider completion, or schema completeness.
- Do not mutate package artifacts without MAG package authority.
- Do not store package bodies or verdict bodies in `agent/` or OPL generated surfaces.
- Do not collapse review-ready, local submission-ready, and external submitted into one status.

## Receipt Expectations

- `submission_ready_export_verdict` must include `owner`, `export_verdict_ref`, `source_kind`, and `provenance_ref`.
- Package receipts must name package refs, quality gate state, unresolved portal actions, blocker state, and owner authority evidence.
- Blocked packages must name the exact missing artifact, unresolved issue, provenance gap, or human action.

## Review Questions

- Is the package merely generated, or has MAG accepted export readiness?
- Are portal-only steps visible to the human operator?
- Can each package ref trace back to accepted draft, source, and quality evidence?
