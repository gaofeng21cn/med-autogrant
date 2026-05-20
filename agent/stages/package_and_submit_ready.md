# Package And Submit Ready Policy

## Entry Conditions

- Review gate receipt or quality verdict ref exists, with residual package-facing requirements visible.
- Final draft/package artifact refs, required attachments, and portal constraints are available.
- MAG package authority is available for export verdict and package mutation receipts.

## Stage Work

- Verify local submission-ready package refs, required sections, attachments, provenance, quality closure, export constraints, and manual portal boundary.
- Materialize package refs only through MAG owner authority.
- Return exact blockers for missing artifacts, unresolved quality issues, provenance gaps, or human portal actions.

## Exit Conditions

- `submission_ready_package_receipt_recorded` exists with export verdict ref and package refs; or
- A typed blocker records unclosed quality gate, missing required artifact, missing provenance, manual portal action, or mechanical export-ready attempt; or
- A MAG owner receipt signs terminal package/export state.

## Handoff

- Handoff target: terminal stage or human portal handoff.
- Handoff must include package refs, export verdict ref or blocker, manual portal boundary, provenance refs, and owner authority evidence.
- Terminal handoff means local package readiness, not external portal submission completion.

## Independent Review And Gate Expectation

- Independent gate must confirm that quality closure, package completeness, provenance, and portal boundary are all explicit.
- Required gates: `export_and_package`, `quality`, and `authority_boundaries`.
- Package existence, lifecycle completion, or provider completion cannot declare submission-ready export.

## OPL Role Boundary

- OPL role: lifecycle shell, receipt, and package ref consumer.
- OPL artifact lifecycle may carry refs and receipts only; MAG owns package authority and export verdict.
- Allowed action refs: `build_submission_ready_package`, `inspect_progress`.

## Non-Pass Signals

- Package readiness is inferred from generated files without quality/provenance refs.
- Human portal actions are omitted or described as already complete without receipt.
