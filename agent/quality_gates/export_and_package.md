# Export And Package Gate

## Gate Purpose

This gate decides whether MAG can produce a local submission-ready package and export verdict.

## Evidence To Review

- Quality verdict or review gate receipt.
- Final draft refs, package manifest refs, required sections, required attachments, budget/support material refs, and portal instructions.
- Provenance refs tying package artifacts back to accepted drafts, source evidence, and owner receipts.
- Manual portal boundary and human-supervised submission requirements.

## AI/Owner-Backed Judgment Standard

- Submission-ready export requires MAG package/export stage evidence, AI-backed reviewer/export artifact, or MAG owner receipt.
- Mechanical package completeness is a lower-bound check only.
- Package mutation and release require MAG package authority.

## Forbidden Decision Sources

- Package file presence.
- Generic lifecycle completion.
- OPL provider completion.
- Schema completeness.
- Quality scorecard values without review closure.
- External portal assumptions without human-supervised receipt.

## Required Output

- `submission_ready_export_verdict` with `owner`, `export_verdict_ref`, `source_kind`, and `provenance_ref`; or
- `submission_ready_package_receipt_recorded` with package refs and manual portal boundary; or
- Typed blocker with exact missing artifact, quality issue, provenance gap, or portal action.

## Blocker Shapes

- `quality_gate_unclosed`.
- `required_artifact_missing`.
- `export_provenance_missing`.
- `manual_portal_action_required`.
- `mechanical_export_ready_attempted`.

## Pass Condition

The local package is ready for human-supervised submission, all provenance is traceable, and no external portal action is silently claimed complete.
