# Package And Submit Ready Policy

## Entry Conditions

- Review gate receipt or quality verdict ref exists, with residual package-facing requirements visible.
- Final draft/package artifact refs, required attachments, and portal constraints are available.
- MAG package authority is available for export verdict and package mutation receipts.

## Stage Work

- Verify local submission-ready package refs, required sections, attachments, provenance, quality closure, export constraints, and manual portal boundary.
- Materialize package refs only through MAG owner authority.
- Bind exact refs and hashes for all four final package artifacts, then require a fresh reviewer over those bytes before MAG owner authority can evaluate local `submission_ready`.
- Keep local repair to assembly, manifest, and provenance projection; route upstream content, evidence, quality-closure, attachment-owner, or export-verdict defects to their earliest owning Stage.
- Return exact blockers for real artifact, quality, provenance, or authority gaps; use `human_gate_ref` for human portal actions.

## Exit Conditions

- The StageRunController has materialized an exact-hash-bound `opl_stage_review_receipt`, and MAG owner authority has consumed that receipt plus the current package refs before recording a local export/readiness verdict; or
- `completed_and_wait_owner` records a required human portal action with `human_gate_ref`; or
- A `route_back_ref` records an ordinary quality, artifact, or provenance repair target; or
- A quality-debt diagnostic records semantic or provenance gaps; a typed blocker is reserved for unsafe export, authority, wrong-target identity/currentness, irreversible action, unavailable executor, or explicit human decision; or
- A MAG owner receipt signs terminal local package/export state after consuming the current `opl_stage_review_receipt`.

## Handoff

- Handoff target: terminal stage or human portal handoff.
- Handoff must include package refs, export verdict ref or blocker, manual portal boundary, provenance refs, and owner authority evidence.
- Human portal handoff uses `completed_and_wait_owner` plus `human_gate_ref`; it must not be encoded as `blocked` plus `typed_blocker_ref`.
- Terminal handoff means local package readiness, not external portal submission completion.

## Independent Review And Gate Expectation

- Independent gate must confirm against the exact current four-artifact generation that quality closure, package completeness, provenance, and portal boundary are all explicit.
- Required gates: `export_and_package`, `quality`, and `authority_boundaries`.
- Package existence, lifecycle completion, provider completion, producer self-check, or helper success cannot declare submission-ready export. Reviewer/re-reviewer closeout can support the exact-byte Review receipt, but local readiness still requires a separate MAG-owned export/owner verdict.
- Producer and repairer closeouts may only recommend a declared route. `same_stage_repair_required` continues the package assembly/manifest/provenance quality loop while budget remains. `cross_stage_route_back_before_budget_exhaustion` lets a reviewer/re-reviewer return terminal `repair_required + stage_route_decision(decision_kind=route_back)` only when the earliest canonical owner is a different declared Stage; no other pre-exhaustion terminal route is allowed. When no repair budget remains and the exact package generation is consumable, that reviewer/re-reviewer is the terminal decisive Attempt and supplies `route_impact.stage_route_decision` while the controller projects `completed_with_quality_debt`. A hard-boundary reviewer/re-reviewer returns no route output. No Attempt creates the authoritative Review receipt, and OPL cannot sign the MAG owner verdict.

## OPL Role Boundary

- OPL role: lifecycle shell, Stage Review receipt materializer, and package ref consumer.
- OPL artifact lifecycle may carry refs and receipts only; MAG owns package authority and export verdict.
- Allowed action refs: `build_submission_ready_package`, `inspect_progress`.

## Non-Pass Signals

- Package readiness is inferred from generated files without quality/provenance refs.
- Human portal actions are omitted or described as already complete without receipt.
