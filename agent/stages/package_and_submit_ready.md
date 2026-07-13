# Package And Submit Ready Policy

## Entry Conditions

- Review gate receipt or quality verdict ref exists, with residual package-facing requirements visible.
- Final draft/package artifact refs, required attachments, and portal constraints are available.
- MAG package authority is available for export verdict and package mutation receipts.

## Stage Work

- Verify local submission-ready package refs, required sections, attachments, provenance, quality closure, export constraints, and manual portal boundary.
- Materialize package refs only through MAG owner authority.
- Return exact blockers for real artifact, quality, provenance, or authority gaps; use `human_gate_ref` for human portal actions.

## Exit Conditions

- `submission_ready_package_receipt_recorded` exists with export verdict ref and package refs; or
- `completed_and_wait_owner` records a required human portal action with `human_gate_ref`; or
- A `route_back_ref` records an ordinary quality, artifact, or provenance repair target; or
- A quality-debt diagnostic records semantic or provenance gaps; a typed blocker is reserved for unsafe export, authority, wrong-target identity/currentness, irreversible action, unavailable executor, or explicit human decision; or
- A MAG owner receipt signs terminal package/export state.

## Handoff

- Handoff target: terminal stage or human portal handoff.
- Handoff must include package refs, export verdict ref or blocker, manual portal boundary, provenance refs, and owner authority evidence.
- Human portal handoff uses `completed_and_wait_owner` plus `human_gate_ref`; it must not be encoded as `blocked` plus `typed_blocker_ref`.
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
